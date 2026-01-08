#!/usr/bin/env python
# coding: utf-8
"""
MapReduce - Analisi Pedaggi Autostradali (PySpark RDD API)
Calcola il pedaggio medio per tipo di veicolo (2015 vs 2025)
"""

from pyspark import SparkConf, SparkContext
import os
import time

def main():
    """Funzione principale per l'analisi dei pedaggi con PySpark"""
    
    # -----------------------------
    # Configurazione Spark in locale
    # -----------------------------
    conf = SparkConf() \
        .setAppName("AnalisiPedaggiAutostradali") \
        .setMaster("local[*]")  # usa tutti i core disponibili

    # Forzare filesystem locale (evita errori HDFS)
    conf.set("spark.hadoop.fs.defaultFS", "file:///")

    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")

    # -----------------------------
    # Percorso del file di input
    # -----------------------------
    input_path = "caselli_autostradali.csv"

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File non trovato: {input_path}")

    # Misurazione tempo (esclusa inizializzazione Spark/JVM)
    start_time = time.time()

    # -----------------------------
    # LOAD: Caricamento Dataset CSV
    # -----------------------------
    rdd = sc.textFile(input_path)

    # Estrai header e rimuovilo dal dataset
    header = rdd.first()
    rdd_data = rdd.filter(lambda line: line != header)

    # Parsing header per trovare indici colonne
    cols = header.split(",")
    idx_tipo = cols.index("TipoVeicolo")
    idx_data = cols.index("DataTransito")
    idx_pedaggio = cols.index("Pedaggio")

    # -----------------------------
    # MAP: Parsing righe ed estrazione campi
    # -----------------------------
    def parse_line(line):
        """Estrae (TipoVeicolo, Anno, Pedaggio) da una riga CSV."""
        fields = line.split(",")
        tipo_veicolo = fields[idx_tipo]
        # DataTransito formato GG/MM/YYYY -> estrai anno
        anno = fields[idx_data].split("/")[-1]
        pedaggio = float(fields[idx_pedaggio])
        return (tipo_veicolo, anno, pedaggio)

    rdd_parsed = rdd_data.map(parse_line)

    # -----------------------------
    # FILTER: Solo anni 2015 e 2025
    # -----------------------------
    rdd_filtered = rdd_parsed.filter(lambda x: x[1] in ["2015", "2025"])

    # -----------------------------
    # REDUCE: Calcolo media per (TipoVeicolo, Anno)
    # -----------------------------
    # Chiave: (TipoVeicolo, Anno), Valore: (somma_pedaggi, conteggio)
    rdd_keyed = rdd_filtered.map(lambda x: ((x[0], x[1]), (x[2], 1)))

    # Somma pedaggi e conteggi per chiave
    rdd_summed = rdd_keyed.reduceByKey(lambda a, b: (a[0] + b[0], a[1] + b[1]))

    # Calcola media: somma / conteggio
    rdd_avg = rdd_summed.map(lambda x: ((x[0][0], x[0][1]), round(x[1][0] / x[1][1], 2)))

    # -----------------------------
    # POST-PROCESSING: Riorganizza per TipoVeicolo
    # -----------------------------
    # Converti in: (TipoVeicolo, (Anno, Media))
    rdd_by_tipo = rdd_avg.map(lambda x: (x[0][0], (x[0][1], x[1])))

    # Raggruppa per TipoVeicolo
    rdd_grouped = rdd_by_tipo.groupByKey()

    # Costruisci risultato finale con variazione
    def build_result(item):
        tipo, values = item
        data = dict(values)
        media_2015 = data.get("2015", 0.0)
        media_2025 = data.get("2025", 0.0)
        variazione = round(media_2025 - media_2015, 2)
        return (tipo, media_2015, media_2025, variazione)

    rdd_result = rdd_grouped.map(build_result)

    # -----------------------------
    # OUTPUT
    # -----------------------------
    print("\nRisultati Analisi PySpark:")
    print(f"{'TipoVeicolo':<15} {'Media_2015':>12} {'Media_2025':>12} {'Variazione':>12}")
    print("-" * 55)

    for row in rdd_result.collect():
        print(f"{row[0]:<15} {row[1]:>12.2f} {row[2]:>12.2f} {row[3]:>12.2f}")

    end_time = time.time()
    print(f"\nTempo di esecuzione PySpark: {end_time - start_time:.2f} secondi")

    # -----------------------------
    # Chiudere SparkContext
    # -----------------------------
    sc.stop()

if __name__ == "__main__":
    main()