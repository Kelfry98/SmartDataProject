-- SELECT sobre las tablas finales de cada capa.
-- golden.covid_summary_by_country es la más importante de las cuatro: es la que lee el
-- dashboard de Databricks Lakeview.
--
-- Placeholder {catalog} sustituido por proceso/05_grants/grants.py.

GRANT SELECT ON TABLE {catalog}.bronze.who_covid_daily TO `account users`;
GRANT SELECT ON TABLE {catalog}.bronze.covid_historical_series TO `account users`;
GRANT SELECT ON TABLE {catalog}.silver.covid_unified TO `account users`;
GRANT SELECT ON TABLE {catalog}.golden.covid_summary_by_country TO `account users`;
