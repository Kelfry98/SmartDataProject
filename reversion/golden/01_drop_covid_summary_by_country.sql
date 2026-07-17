-- Revierte la tabla creada por proceso/04_load/load_covid_summary_by_country.py
-- Placeholder {catalog} — reemplazar por dev_catalog o prod_catalog según corresponda.

DROP TABLE IF EXISTS {catalog}.golden.covid_summary_by_country;
