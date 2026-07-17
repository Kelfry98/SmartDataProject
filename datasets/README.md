# datasets/

**Esta carpeta es solo referencia/documentación** — no contiene los CSV reales. Los datos
viven en el contenedor `raw` de Azure Blob Storage (ADLS Gen2), subidos ahí manualmente
una sola vez, fuera del pipeline. Databricks nunca descarga nada en tiempo de ejecución:
el notebook de Extract lee directo desde esa external location vía Managed Identity.

## Datasets (ambos sobre COVID-19)

- [who-covid-daily/](who-covid-daily/) — Kaggle: [Worldwide COVID-19 Data from WHO](https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who) → tabla Bronze `who_covid_daily`
- [covid-historical-series/](covid-historical-series/) — Kaggle: [Coronavirus (COVID-19) Worldwide Data (2018-2026)](https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026) → tabla Bronze `covid_historical_series`

## Flujo real de los datos

1. Se descarga el CSV de Kaggle manualmente (una sola vez).
2. Ya está subido al contenedor `raw` en Azure Blob Storage, uno por carpeta (mismo nombre
   que la subcarpeta aquí):
   - `raw/who-covid-daily/WHO-COVID-19-global-daily-data.csv`
   - `raw/covid-historical-series/covid_historical_time_series.csv`
3. Databricks lo lee directo del archivo vía `abfss://raw@stdbkprojectsraw.dfs.core.windows.net/<carpeta>/<archivo>.csv`,
   autenticado con el Storage Credential `raw_sc` + External Location `raw_ext_loc` de
   Unity Catalog, creados en [PrepAmb/](../PrepAmb/) — sin DBFS, sin Volumes, sin API keys.

No se usa Kaggle MCP ni ninguna conexión en vivo a Kaggle en el pipeline de producción.
