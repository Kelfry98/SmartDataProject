-- Revierte la tabla creada por proceso/02_extract/extract_covid_historical_series.py
-- Placeholder {catalog} — reemplazar por dev_catalog o prod_catalog según corresponda.

DROP TABLE IF EXISTS {catalog}.bronze.covid_historical_series;
