# Databricks notebook source
# Extract (Bronze) — Coronavirus (COVID-19) Worldwide Data (2018-2026)
# https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026
#
# 100% PySpark. Lee el CSV directo desde la external location de Unity Catalog
# (abfss://<container>@<storage_account>.dfs.core.windows.net/<raw_path>), creada en
# PrepAmb/04_external_location.sql. Autenticación exclusivamente vía Managed Identity —
# sin DBFS, sin Volumes, sin access keys. El CSV se subió a Azure manualmente, una sola
# vez, fuera de este pipeline (ver datasets/coronavirus-covid-19-worldwide-2018-2026/README.md).

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
dbutils.widgets.text("storage_account", "stdbkprojectsraw", "Storage Account de Raw")
dbutils.widgets.text("container_name", "raw", "Contenedor de Raw")
dbutils.widgets.text(
    "raw_path", "coronavirus-covid-19-worldwide-2018-2026/", "Ruta dentro del contenedor Raw"
)

environment = dbutils.widgets.get("environment")
storage_account = dbutils.widgets.get("storage_account")
container_name = dbutils.widgets.get("container_name")
raw_path = dbutils.widgets.get("raw_path")

catalog = f"{environment}_catalog"
bronze_table = f"{catalog}.bronze.covid_worldwide"
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
