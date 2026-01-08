import csv
import random
import os
from faker import Faker

# Inizializzazione Faker
fake = Faker('it_IT')

# Configurazione
NUM_RECORDS = 100000
OUTPUT_FILE = "caselli_autostradali.csv"

VEICOLI_KEYS = ["Auto", "Moto", "Camion", "Autobus", "Furgone"]
VEICOLI_DATA = {
    "Auto": (2.0, 15.0), 
    "Moto": (1.5, 10.0), 
    "Camion": (5.0, 35.0), 
    "Autobus": (4.0, 25.0), 
    "Furgone": (3.0, 20.0)
}

TRATTE = [
    "A1-Milano-Bologna", 
    "A1-Bologna-Firenze", 
    "A1-Firenze-Roma", 
    "A1-Roma-Napoli",
    
    "A4-Torino-Milano", 
    "A4-Milano-Brescia",
    "A4-Brescia-Padova",
    "A4-Padova-Venezia",
    
    "A21-Brescia-Piacenza",
    "A21-Piacenza-Torino",

    "A14-Bologna-Ancona", 
    "A14-Ancona-Bari",
    "A22-Brennero-Modena", 
    "A12-Genova-Livorno", 
    "A7-Milano-Genova", 
    "A8-Milano-Varese",
    "A35-Brescia-Milano"
]

FASCE_ORARIE = ["Mattina", "Pomeriggio", "Sera", "Notte"]

def generate_dataset():
    filepath = os.path.join(os.path.dirname(__file__), OUTPUT_FILE)
    
    print(f"Inizio generazione di {NUM_RECORDS} record...")
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        
        # Header
        header = ["IDVeicolo", "TipoVeicolo", "Tratta", "Pedaggio", "DataTransito", "FasciaOraria", "Provincia"]
        writer.writerow(header)
        
        # Contatori per verifica
        count_2015 = 0
        count_2025 = 0
        
        for _ in range(NUM_RECORDS):
            # Scelta Anno
            if random.random() < 0.5:
                anno = 2015
                count_2015 += 1
            else:
                anno = 2025
                count_2025 += 1

            # Selezione Veicolo e calcolo Pedaggio
            tipo = random.choice(VEICOLI_KEYS)
            min_p, max_p = VEICOLI_DATA[tipo]
            prezzo_pedaggio = random.uniform(min_p, max_p)
            if anno == 2025: prezzo_pedaggio *= random.uniform(1.15, 1.25) # Aumento pedaggi 2025 per un contesto più realistico
            
            row = [
                fake.license_plate(),           # IDVeicolo
                tipo,                           # TipoVeicolo
                random.choice(TRATTE),          # Tratta
                prezzo_pedaggio,                # Pedaggio
                fake.date(pattern='%d/%m') + f'/{anno}',  # DataTransito
                random.choice(FASCE_ORARIE),    # FasciaOraria
                fake.city()                     # Provincia
            ]
            
            writer.writerow(row)

    print(f"Dataset completato: {filepath}")
    print(f"  Totale: {NUM_RECORDS}")
    print(f"  Record 2015: {count_2015}")
    print(f"  Record 2025: {count_2025}")

if __name__ == "__main__":
    generate_dataset()