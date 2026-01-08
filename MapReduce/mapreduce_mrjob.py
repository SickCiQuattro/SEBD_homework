#!/usr/bin/env python
# coding: utf-8
"""
MapReduce - Analisi Pedaggi Autostradali (mrjob)
Calcola il pedaggio medio per tipo di veicolo (2015 vs 2025)
"""

import sys
import shlex
import time

# --- PATCH PER PYTHON 3.13 ---
# Per mrjob sostituzione 'pipes' con 'shlex' -> modulo moderno equivalente.
if sys.version_info >= (3, 13):
    sys.modules['pipes'] = shlex
# -----------------------------

from mrjob.job import MRJob

class MRAnalisiPedaggi(MRJob):
    """Job MapReduce per calcolare pedaggi medi per tipo veicolo."""

    def mapper(self, _, line):
        """MAP: Estrae (tipo_veicolo, [c15, s15, c25, s25]) da ogni riga."""
        if line.startswith("IDVeicolo"):
            return

        try:
            fields = line.strip().split(',')
            if len(fields) < 7:
                return

            tipo_veicolo = fields[1]
            pedaggio = float(fields[3])
            anno = fields[4].split('/')[-1]  # Estrae anno da GG/MM/YYYY

            if anno == "2015":
                yield tipo_veicolo, [1, pedaggio, 0, 0.0]
            elif anno == "2025":
                yield tipo_veicolo, [0, 0.0, 1, pedaggio]

        except (ValueError, IndexError):
            pass

    def combiner(self, key, values):
        """COMBINE: Aggregazione parziale sul nodo mapper."""
        c15, s15, c25, s25 = 0, 0.0, 0, 0.0
        for v in values:
            c15 += v[0]
            s15 += v[1]
            c25 += v[2]
            s25 += v[3]
        yield key, [c15, s15, c25, s25]

    def reducer(self, key, values):
        """REDUCE: Calcola media finale e variazione."""
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