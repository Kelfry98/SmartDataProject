# Databricks notebook source
# Transform (Silver) — unifica ambas fuentes Bronze por país normalizado + year_month → silver.covid_unified.

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
environment = dbutils.widgets.get("environment")
catalog = f"{environment}_catalog"

# COMMAND ----------

from pyspark.sql import functions as F

who_df = spark.table(f"{catalog}.bronze.who_covid_daily")
hist_df = spark.table(f"{catalog}.bronze.covid_historical_series")

# COMMAND ----------

# Normaliza el nombre de país (trim + upper + sin acentos) + overrides de casos conocidos
# donde WHO e historical lo nombran distinto (best-effort, no un diccionario ISO completo).

ACCENTS_FROM = "ÁÀÂÃÄÉÈÊËÍÌÎÏÓÒÔÕÖÚÙÛÜÇÑ"
ACCENTS_TO = "AAAAAEEEEIIIIOOOOOUUUUCN"

COUNTRY_NAME_OVERRIDES = {
    "UNITED STATES OF AMERICA": "UNITED STATES",
    "RUSSIAN FEDERATION": "RUSSIA",
    "IRAN (ISLAMIC REPUBLIC OF)": "IRAN",
    "KOREA, REPUBLIC OF": "SOUTH KOREA",
    "VIET NAM": "VIETNAM",
    "CZECHIA": "CZECH REPUBLIC",
    "COTE D'IVOIRE": "IVORY COAST",
}


def normalize_country(column):
    normalized = F.translate(F.upper(F.trim(column)), ACCENTS_FROM, ACCENTS_TO)
    for wrong, right in COUNTRY_NAME_OVERRIDES.items():
        normalized = F.when(normalized == wrong, F.lit(right)).otherwise(normalized)
    return normalized


# COMMAND ----------

# WHO: agregado a país + year_month
who_agg = (
    who_df
    .withColumn("country_norm", normalize_country(F.col("Country")))
    .withColumn("year_month", F.date_format(F.to_date(F.col("Date_reported")), "yyyy-MM"))
    .groupBy("country_norm", "year_month")
    .agg(
        F.sum("New_cases").alias("who_new_cases"),
        F.max("Cumulative_cases").alias("who_cumulative_cases"),
        F.sum("New_deaths").alias("who_new_deaths"),
        F.max("Cumulative_deaths").alias("who_cumulative_deaths"),
    )
    .withColumn("_from_who", F.lit(True))
)

# Historical: agregado a país + year_month (population con avg)
hist_agg = (
    hist_df
    .withColumn("country_norm", normalize_country(F.col("location")))
    .withColumn("year_month", F.date_format(F.to_date(F.col("date")), "yyyy-MM"))
    .groupBy("country_norm", "year_month")
    .agg(
        F.sum("new_cases").alias("hist_new_cases"),
        F.max("total_cases").alias("hist_total_cases"),
        F.sum("new_deaths").alias("hist_new_deaths"),
        F.max("total_deaths").alias("hist_total_deaths"),
        F.avg("population").alias("hist_population"),
    )
    .withColumn("_from_hist", F.lit(True))
)

# COMMAND ----------

unified = who_agg.join(hist_agg, on=["country_norm", "year_month"], how="outer")

unified = (
    unified
    .withColumn(
        "data_sources",
        F.when(F.col("_from_who").isNotNull() & F.col("_from_hist").isNotNull(), F.lit("WHO+HISTORICAL"))
        .when(F.col("_from_who").isNotNull(), F.lit("WHO"))
        .otherwise(F.lit("HISTORICAL")),
    )
    .drop("_from_who", "_from_hist")
)

# COMMAND ----------

silver_table = f"{catalog}.silver.covid_unified"
unified.write.mode("overwrite").saveAsTable(silver_table)

# COMMAND ----------

dbutils.notebook.exit(silver_table)
