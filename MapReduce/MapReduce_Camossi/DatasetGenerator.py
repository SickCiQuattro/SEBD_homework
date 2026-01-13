#!/usr/bin/env python
# coding: utf-8
"""
Dataset Generator - Caselli Autostradali
Genera un dataset sintetico di 'NUM_RECORDS' transiti autostradali (2015 e 2025)
con inflazione simulata del 15-25% sui pedaggi del 2025.
"""

import csv
import random
import os
from faker import Faker


# Inizializzazione Faker (locale italiano)
fake = Faker('it_IT')

# Configurazione
NUM_RECORDS = 100_000
OUTPUT_FILE = "caselli_autostradali.csv"

# Tipi veicolo con range pedaggi (min, max) in euro
VEICOLI_KEYS = ["Auto", "Moto", "Camion", "Autobus", "Furgone"]
VEICOLI_DATA = {
    "Auto": (2.0, 15.0), 
    "Moto": (1.5, 10.0), 
    "Camion": (5.0, 35.0), 
    "Autobus": (4.0, 25.0), 
    "Furgone": (3.0, 20.0)
}

# Tratte autostradali italiane
TRATTE = [
    "A1-Milano-Bologna", "A1-Bologna-Firenze", "A1-Firenze-Roma", "A1-Roma-Napoli",
    "A4-Torino-Milano", "A4-Milano-Brescia", "A4-Brescia-Padova", "A4-Padova-Venezia",
    "A21-Brescia-Piacenza", "A21-Piacenza-Torino",
    "A14-Bologna-Ancona", "A14-Ancona-Bari",
    "A22-Brennero-Modena", "A12-Genova-Livorno", 
    "A7-Milano-Genova", "A8-Milano-Varese", "A35-Brescia-Milano"
]

FASCE_ORARIE = ["Mattina", "Pomeriggio", "Sera", "Notte"]

def generate_dataset():
    """Genera il dataset CSV con transiti autostradali."""
    filepath = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
    
    print(f"Generazione di {NUM_RECORDS:,} record...")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        
        # Header
        header = ["IDVeicolo", "TipoVeicolo", "Tratta", "Pedaggio", 
                "DataTransito", "FasciaOraria", "Provincia"]
        writer.writerow(header)
        
        count_2015, count_2025 = 0, 0

        for _ in range(NUM_RECORDS):
            # Scelta anno (50% probabilità)
            if random.random() < 0.5:
                anno = 2015
                count_2015 += 1
            else:
                anno = 2025
                count_2025 += 1

            # Selezione veicolo e calcolo pedaggio
            tipo = random.choice(VEICOLI_KEYS)
            min_p, max_p = VEICOLI_DATA[tipo]
            pedaggio = random.uniform(min_p, max_p)
            
            # Inflazione 15-25% per il 2025
            if anno == 2025:
                pedaggio *= random.uniform(1.15, 1.25)

            row = [
                fake.license_plate(),                    # IDVeicolo
                tipo,                                    #TipoVeicolo
                random.choice(TRATTE),                   # Tratta
                round(pedaggio, 2),                      # Pedaggio
                fake.date(pattern='%d/%m') + f'/{anno}', # DataTransito (GG/MM/YYYY)
                random.choice(FASCE_ORARIE),             # FasciaOraria
                fake.city()                              # Provincia
            ]
            writer.writerow(row)

    print(f"Dataset completato: {filepath}")
    print(f"  Totale: {NUM_RECORDS:,} | 2015: {count_2015:,} | 2025: {count_2025:,}")

if __name__ == "__main__":
    generate_dataset()