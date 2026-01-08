from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, element_at, avg, round as spark_round, when
import time

def main():
    # 1. Inizializzazione Sessione Spark (Locale)
    spark = SparkSession.builder \
        .appName("AnalisiPedaggiAutostradali") \
        .master("local[*]") \
        .getOrCreate()

    # Disattiva log troppo verbosi
    spark.sparkContext.setLogLevel("ERROR")

    # Misurazione tempo (esclusa inizializzazione Spark)
    start_time = time.time()

    # 2. Caricamento Dataset CSV
    # Spark gestisce automaticamente header e tipi se richiesto
    df = spark.read.option("header", "True") \
                    .option("inferSchema", "True") \
                    .csv("caselli_autostradali.csv")

    # 3. Pre-processing: Estrazione Anno
    # La data è stringa "dd/mm/yyyy", prendiamo l'ultima parte dopo lo split
    df_with_year = df.withColumn("Anno", element_at(split(col("DataTransito"), "/"), -1))

    # 4. Filtro (Map Phase logica)
    df_filtered = df_with_year.filter(col("Anno").isin("2015", "2025"))

    # 5. Aggregazione (Reduce Phase logica)
    # Calcoliamo la media condizionale per tipo veicolo
    result = df_filtered.groupBy("TipoVeicolo").agg(
        spark_round(avg(when(col("Anno") == "2015", col("Pedaggio"))), 2).alias("Media_2015"),
        spark_round(avg(when(col("Anno") == "2025", col("Pedaggio"))), 2).alias("Media_2025")
    )

    # 6. Calcolo Variazione (Post-processing)
    final_result = result.withColumn("Variazione",  spark_round(col("Media_2025") - col("Media_2015"), 2))

    # 7. Output
    print("\n--- Risultati Analisi PySpark ---")
    final_result.show()

    # Tempo di esecuzione (esclusa inizializzazione JVM/Spark)
    end_time = time.time()
    print(f"Tempo di esecuzione PySpark: {end_time - start_time:.2f} secondi")

    # Salva su file (opzionale, crea una cartella)
    # final_result.write.csv("output_spark", header=True)

    spark.stop()

if __name__ == "__main__":
    main()