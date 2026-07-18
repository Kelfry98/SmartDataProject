-- SELECT sobre las 4 tablas finales (2 Bronze, 1 Silver, 1 Golden), para `account users`.
-- {catalog} sustituido por grants.py.

GRANT SELECT ON TABLE {catalog}.bronze.who_covid_daily TO `account users`;
GRANT SELECT ON TABLE {catalog}.bronze.covid_historical_series TO `account users`;
GRANT SELECT ON TABLE {catalog}.silver.covid_unified TO `account users`;
GRANT SELECT ON TABLE {catalog}.golden.covid_summary_by_country TO `account users`;
