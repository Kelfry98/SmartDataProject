# Databricks notebook source
# Load (Golden) — consolida silver.covid_unified con métricas finales y per-cápita → golden.covid_summary_by_country.

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
environment = dbutils.widgets.get("environment")
catalog = f"{environment}_catalog"

# COMMAND ----------

from pyspark.sql import functions as F

silver_df = spark.table(f"{catalog}.silver.covid_unified")

# COMMAND ----------

# Métricas finales: WHO primero, historical de respaldo (coalesce). Population solo de historical.
consolidated = silver_df.select(
    "country_norm",
    "year_month",
    "data_sources",
    F.coalesce(F.col("who_new_cases"), F.col("hist_new_cases")).alias("final_new_cases"),
    F.coalesce(F.col("who_new_deaths"), F.col("hist_new_deaths")).alias("final_new_deaths"),
    F.coalesce(F.col("who_cumulative_cases"), F.col("hist_total_cases")).alias("final_cumulative_cases"),
    F.coalesce(F.col("who_cumulative_deaths"), F.col("hist_total_deaths")).alias("final_cumulative_deaths"),
    F.col("hist_population").alias("population"),
)

# COMMAND ----------

# Per-cápita: NULL si el denominador es 0/NULL (when sin otherwise, en vez de error o Infinity).
golden = (
    consolidated
    .withColumn(
        "cases_per_million",
        F.when(
            F.col("population").isNotNull() & (F.col("population") != 0),
            (F.col("final_cumulative_cases") / F.col("population")) * 1000000,
        ),
    )
    .withColumn(
        "deaths_per_million",
        F.when(
            F.col("population").isNotNull() & (F.col("population") != 0),
            (F.col("final_cumulative_deaths") / F.col("population")) * 1000000,
        ),
    )
    .withColumn(
        "case_fatality_rate",
        F.when(
            F.col("final_cumulative_cases").isNotNull() & (F.col("final_cumulative_cases") != 0),
            F.col("final_cumulative_deaths") / F.col("final_cumulative_cases"),
        ),
    )
)

# COMMAND ----------

golden_table = f"{catalog}.golden.covid_summary_by_country"
golden.write.mode("overwrite").saveAsTable(golden_table)

# COMMAND ----------

dbutils.notebook.exit(golden_table)
