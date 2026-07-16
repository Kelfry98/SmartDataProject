# datasets/

**Esta carpeta es solo referencia/documentación** — no contiene los CSV reales. Los datos
viven en el contenedor `raw` de Azure Blob Storage (ADLS Gen2), subidos ahí manualmente
una sola vez, fuera del pipeline. Databricks nunca descarga nada en tiempo de ejecución:
el notebook de Extract lee directo desde esa external location vía Managed Identity.

## Datasets (ambos sobre COVID-19)

- [worldwide-covid-19-who/](worldwide-covid-19-who/) — Kaggle: [Worldwide COVID-19 Data from WHO](https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who)
- [coronavirus-covid-19-worldwide-2018-2026/](coronavirus-covid-19-worldwide-2018-2026/) — Kaggle: [Coronavirus (COVID-19) Worldwide Data (2018-2026)](https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026)

## Flujo real de los datos

1. Se descarga el CSV de Kaggle manualmente (una sola vez).
2. Se sube al contenedor `raw` en Azure Blob Storage, en una carpeta por dataset (mismo
   nombre que la subcarpeta aquí, por convención — ver cada README).
3. Databricks lo lee vía `abfss://raw@stdbkprojectsraw.dfs.core.windows.net/<dataset>/`,
   autenticado con el Storage Credential `raw_sc` + External Location `raw_ext_loc` de
   Unity Catalog, creados en [PrepAmb/](../PrepAmb/) — sin DBFS, sin Volumes, sin API keys.

No se usa Kaggle MCP ni ninguna conexión en vivo a Kaggle en el pipeline de producción.
