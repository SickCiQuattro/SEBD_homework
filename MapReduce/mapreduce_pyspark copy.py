#!/usr/bin/env python
# coding: utf-8
"""
MapReduce - Analisi Pedaggi Autostradali (PySpark)
Calcola il pedaggio medio per tipo di veicolo (2015 vs 2025)
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, element_at, avg, round as spark_round, when
import time

def main():
    """Funzione principale per l'analisi dei pedaggi con PySpark."""
    
    # Inizializzazione Sessione Spark
    spark = SparkSession.builder \
        .appName("AnalisiPedaggiAutostradali") \
        .master("local[*]") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")

    # Misurazione tempo (esclusa inizializzazione Spark/JVM)
    start_time = time.time()

    # LOAD: Caricamento Dataset CSV
    df = spark.read.option("header", "True") \
                .option("inferSchema", "True") \
                .csv("caselli_autostradali.csv")

    # MAP: Estrazione Anno da DataTransito (formato GG/MM/YYYY)
    df_with_year = df.withColumn(
        "Anno", 
        element_at(split(col("DataTransito"), "/"), -1)
    )

    # FILTER: Solo anni 2015 e 2025
    df_filtered = df_with_year.filter(col("Anno").isin("2015", "2025"))

    # REDUCE: Aggregazione con media condizionale per tipo veicolo
    result = df_filtered.groupBy("TipoVeicolo").agg(
        spark_round(avg(when(col("Anno") == "2015", col("Pedaggio"))), 2).alias("Media_2015"),
        spark_round(avg(when(col("Anno") == "2025", col("Pedaggio"))), 2).alias("Media_2025")
    )

    # POST-PROCESSING: Calcolo variazione
    final_result = result.withColumn(
        "Variazione", 
        spark_round(col("Media_2025") - col("Media_2015"), 2)
    )

    # OUTPUT
    print("\nRisultati Analisi PySpark:")
    final_result.show()

    end_time = time.time()
    print(f"Tempo di esecuzione PySpark: {end_time - start_time:.2f} secondi")

    spark.stop()

if __name__ == "__main__":
    main()