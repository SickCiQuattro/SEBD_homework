import sys
import shlex
import time

# --- PATCH PER PYTHON 3.13 ---
# Il modulo 'pipes' è stato rimosso in Python 3.13, ma mrjob lo cerca ancora.
# Sostituito con 'shlex' che è il modulo moderno equivalente.
if sys.version_info >= (3, 13):
    sys.modules['pipes'] = shlex
# -----------------------------

from mrjob.job import MRJob

class MRAnalisiPedaggi(MRJob):

    def mapper(self, _, line):
        # Ignora l'intestazione
        if line.startswith("IDVeicolo"):
            return

        try:
            # Parsing CSV delimitatore virgola
            fields = line.strip().split(',')
            
            if len(fields) < 7: return

            tipo_veicolo = fields[1]
            pedaggio = float(fields[3])
            data_transito = fields[4]
            
            # Estrazione anno da formato GG/MM/YYYY
            anno = data_transito.split('/')[-1]

            # Emettiamo un vettore: [count_15, sum_15, count_25, sum_25]
            # Usiamo i float per le somme per evitare problemi di divisione dopo
            if anno == "2015":
                yield tipo_veicolo, [1, pedaggio, 0, 0.0]
            elif anno == "2025":
                yield tipo_veicolo, [0, 0.0, 1, pedaggio]

        except (ValueError, IndexError):
            pass

    def combiner(self, key, values):
        # Somma parziale dei vettori sullo stesso nodo mapper
        c15, s15, c25, s25 = 0, 0.0, 0, 0.0
        
        for v in values:
            c15 += v[0]
            s15 += v[1]
            c25 += v[2]
            s25 += v[3]
            
        yield key, [c15, s15, c25, s25]

    def reducer(self, key, values):
        # Aggregazione finale
        total_c15, total_s15, total_c25, total_s25 = 0, 0.0, 0, 0.0

        for v in values:
            total_c15 += v[0]
            total_s15 += v[1]
            total_c25 += v[2]
            total_s25 += v[3]

        # Calcolo Medie
        avg_2015 = total_s15 / total_c15 if total_c15 > 0 else 0.0
        avg_2025 = total_s25 / total_c25 if total_c25 > 0 else 0.0
        
        # Calcolo Variazione
        delta = avg_2025 - avg_2015
        
        # Output formattato
        yield key, {
            "Media_2015": round(avg_2015, 2),
            "Media_2025": round(avg_2025, 2),
            "Variazione": round(delta, 2)
        }

if __name__ == '__main__':
    start_time = time.time()
    MRAnalisiPedaggi.run()
    end_time = time.time()
    print(f"\nTempo di esecuzione mrjob: {end_time - start_time:.2f} secondi")