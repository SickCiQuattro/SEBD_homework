#!/usr/bin/env python
# coding: utf-8
"""
MapReduce - Analisi Pedaggi Autostradali (PySpark)
Calcola il pedaggio medio per tipo di veicolo (2015 vs 2025)
"""

from pyspark import SparkConf, SparkContext
import time

def main():
    conf = SparkConf().setAppName("PedaggiSinglePass").setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR") 

    input_path = "caselli_autostradali.csv"
    
    start = time.time()

    # Carica il file
    raw_data = sc.textFile(input_path)
    header = raw_data.first()
    rdd = raw_data.filter(lambda x: x != header)

    # Recupero indici delle colonne 
    cols = header.split(",") 
    
    i_tipo, i_data, i_ped = cols.index("TipoVeicolo"), cols.index("DataTransito"), cols.index("Pedaggio")

    # FUNZIONE DI MAP
    def parse_map(line):
        """
        - Chiave: TipoVeicolo
        - Valore: Una tupla di 4 numeri (Somma2015, Count2015, Somma2025, Count2025)
        """
        f = line.split(",") 
        
        try:
            # Estrazione Anno da formato GG/MM/YYYY
            anno = f[i_data].split("/")[-1]
            
            # Filtro anni
            if anno not in ["2015", "2025"]: 
                return None
            
            pedaggio = float(f[i_ped])
            tipo = f[i_tipo]

            # Struttura vettore: (Totale_€_15,  Numero_Transiti_15, Totale_€_25,  Numero_Transiti_25)
            if anno == "2015":
                # Dati primi due slot, zeri negli altri
                return (tipo, (pedaggio, 1, 0.0, 0))
            else: # anno == "2025"
                # Dati ultimi due slot, zeri nei primi
                return (tipo, (0.0, 0, pedaggio, 1))
                
        except (IndexError, ValueError):
            return None

    # ESECUZIONE PIPELINE
    stats = (rdd
            # 1. FASE MAP: Trasforma le righe in vettori
            .map(parse_map)

            # 2. FILTER: Rimuove NON 2015/2025
            .filter(lambda x: x is not None)
            
            # 3. FASE REDUCE: Aggrega i vettori per ogni TipoVeicolo
            #    Somma elemento per elemento:
            #    (Sum15_A + Sum15_B, Count15_A + Count15_B, ...)
            .reduceByKey(lambda a, b: (
                a[0] + b[0], # Totale € 2015
                a[1] + b[1], # Conteggio 2015
                a[2] + b[2], # Totale € 2025
                a[3] + b[3]  # Conteggio 2025
            ))
            
            # 4. FINAL MAP: Calcolo delle medie aritmetiche e della variazione
            #    Input: (Tipo, (Tot15, N15, Tot25, N25))
            .map(lambda x: (
                x[0],                                      # TipoVeicolo
                x[1][0] / x[1][1] if x[1][1] > 0 else 0,   # Media 2015 = Tot / N
                x[1][2] / x[1][3] if x[1][3] > 0 else 0    # Media 2025 = Tot / N
            ))
            
            # 5. POST-PROCESSING: Aggiungo colonna "Delta"
            #    Input: (Tipo, Media15, Media25) -> Output: (Tipo, Media15, Media25, Diff)
            .map(lambda x: (x[0], x[1], x[2], x[2] - x[1]))
            )

    # OUTPUT
    print(f"{'TipoVeicolo':<15} {'Media 2015':>12} {'Media 2025':>12} {'Variazione':>12}")
    print("-" * 60)
    
    for row in stats.collect():
        print(f"{row[0]:<15} {row[1]:>12.2f} {row[2]:>12.2f} {row[3]:>12.2f}")

    end = time.time()
    print(f"\nTempo di esecuzione PySpark: {end - start:.2f} secondi")
    
    sc.stop()

if __name__ == "__main__":
    main()