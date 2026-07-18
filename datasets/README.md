# datasets/

Carpeta de referencia/documentación — no contiene los CSV reales. Los datos viven en el
contenedor `raw` de Azure Blob Storage (ADLS Gen2), subidos manualmente una sola vez. El
notebook de Extract los lee directo desde la external location vía Managed Identity.

## Datasets (ambos sobre COVID-19)

- [who-covid-daily/](who-covid-daily/) — Kaggle: [Worldwide COVID-19 Data from WHO](https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who) → `bronze.who_covid_daily`
- [covid-historical-series/](covid-historical-series/) — Kaggle: [Coronavirus (COVID-19) Worldwide Data (2018-2026)](https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026) → `bronze.covid_historical_series`

## Rutas en Raw

- `raw/who-covid-daily/WHO-COVID-19-global-daily-data.csv`
- `raw/covid-historical-series/covid_historical_time_series.csv`

Acceso: `abfss://raw@stdbkprojectsraw.dfs.core.windows.net/<carpeta>/<archivo>.csv`,
autenticado con el Storage Credential `raw_sc` + External Location `raw_ext_loc` de Unity
Catalog (ver [PrepAmb/](../PrepAmb/)) — sin DBFS, sin Volumes, sin API keys.
