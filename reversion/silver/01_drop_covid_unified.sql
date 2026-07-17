-- Revierte la tabla creada por proceso/03_transform/transform_covid_unified.py
-- Placeholder {catalog} — reemplazar por dev_catalog o prod_catalog según corresponda.

DROP TABLE IF EXISTS {catalog}.silver.covid_unified;
