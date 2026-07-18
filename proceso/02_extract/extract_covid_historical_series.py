# Databricks notebook source
# Extract (Bronze) — COVID-19 serie histórica → bronze.covid_historical_series. Lee el CSV de Raw vía Managed Identity, sin transformar.

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
dbutils.widgets.text("storage_account", "stdbkprojectsraw", "Storage Account de Raw")
dbutils.widgets.text("container_name", "raw", "Contenedor de Raw")
dbutils.widgets.text(
    "raw_path",
    "covid-historical-series/covid_historical_time_series.csv",
    "Ruta del CSV dentro del contenedor Raw",
)

environment = dbutils.widgets.get("environment")
storage_account = dbutils.widgets.get("storage_account")
container_name = dbutils.widgets.get("container_name")
raw_path = dbutils.widgets.get("raw_path")

catalog = f"{environment}_catalog"
bronze_table = f"{catalog}.bronze.covid_historical_series"
raw_url = f"abfss://{container_name}@{storage_account}.dfs.core.windows.net/{raw_path}"

# COMMAND ----------

from pyspark.sql import functions as F

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(raw_url)
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

# COMMAND ----------

df.write.mode("overwrite").saveAsTable(bronze_table)

# COMMAND ----------

dbutils.notebook.exit(bronze_table)
