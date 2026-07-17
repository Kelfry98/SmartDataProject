-- Revierte la tabla creada por proceso/02_extract/extract_who_covid_daily.py
-- Placeholder {catalog} — reemplazar por dev_catalog o prod_catalog según corresponda.

DROP TABLE IF EXISTS {catalog}.bronze.who_covid_daily;
