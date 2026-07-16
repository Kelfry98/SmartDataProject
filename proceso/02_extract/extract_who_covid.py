# Databricks notebook source
# Extract (Bronze) — Worldwide COVID-19 Data from WHO
# https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who
#
# 100% PySpark. Lee el CSV directo desde la external location de Unity Catalog
# (abfss://<container>@<storage_account>.dfs.core.windows.net/<raw_path>), creada en
# PrepAmb/04_external_location.sql. Autenticación exclusivamente vía Managed Identity —
# sin DBFS, sin Volumes, sin access keys. El CSV se subió a Azure manualmente, una sola
# vez, fuera de este pipeline (ver datasets/worldwide-covid-19-who/README.md).

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
dbutils.widgets.text("storage_account", "stdbkprojectsraw", "Storage Account de Raw")
dbutils.widgets.text("container_name", "raw", "Contenedor de Raw")
dbutils.widgets.text("raw_path", "worldwide-covid-19-who/", "Ruta dentro del contenedor Raw")

environment = dbutils.widgets.get("environment")
storage_account = dbutils.widgets.get("storage_account")
container_name = dbutils.widgets.get("container_name")
raw_path = dbutils.widgets.get("raw_path")

catalog = f"{environment}_catalog"
bronze_table = f"{catalog}.bronze.who_covid"
raw_url = f"abfss://{container_name}@{storage_account}.dfs.core.windows.net/{raw_path}"

# COMMAND ----------

from pyspark.sql import functions as F

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv(raw_url)
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.input_file_name())
)

# COMMAND ----------

df.write.mode("overwrite").saveAsTable(bronze_table)

# COMMAND ----------

dbutils.notebook.exit(bronze_table)
