# proceso/02_extract

Notebooks `.py` de Extract (Bronze). 100% PySpark DataFrame API, sin Spark SQL.

Leen cada CSV directo desde su ruta real en el contenedor `raw` de Azure Blob Storage
(ADLS Gen2) vía la external location de Unity Catalog (`raw_ext_loc`), autenticando
únicamente con Managed Identity (Storage Credential + External Location — sin DBFS, sin
Volumes, sin access keys, sin Kaggle MCP ni ninguna llamada a Kaggle en tiempo de
ejecución). Los CSV ya están subidos ahí manualmente, una sola vez, fuera del pipeline —
ver [datasets/](../../datasets/). Sin transformaciones: escriben el dato crudo tal cual
(con metadata de ingesta `_ingested_at`/`_source_file`) a las tablas Bronze.

**Decisión**: dos notebooks separados (uno por dataset/fuente), en vez de uno solo con dos
bloques — así cada uno se corre/reintenta independientemente en el DAG del job de
Databricks (ver [.github/workflows/deploy.yml](../../.github/workflows/deploy.yml)), y un
fallo en una fuente no bloquea la otra.

| Notebook | Dataset fuente | Ruta en Raw | Tabla Bronze |
|---|---|---|---|
| [extract_who_covid_daily.py](extract_who_covid_daily.py) | [who-covid-daily](../../datasets/who-covid-daily/) | `who-covid-daily/WHO-COVID-19-global-daily-data.csv` | `{catalog}.bronze.who_covid_daily` |
| [extract_covid_historical_series.py](extract_covid_historical_series.py) | [covid-historical-series](../../datasets/covid-historical-series/) | `covid-historical-series/covid_historical_time_series.csv` | `{catalog}.bronze.covid_historical_series` |

`{catalog}` se resuelve dinámicamente en cada notebook a partir del widget `environment`
(`dev` → `dev_catalog`, `prod` → `prod_catalog`), nunca hardcodeado.
