# proceso/02_extract

Notebooks `.py` de Extract (Bronze). 100% PySpark.

Leen los CSV directo desde el contenedor `raw` en Azure Blob Storage (ADLS Gen2) vía la
external location de Unity Catalog, autenticando únicamente con Managed Identity (Storage
Credential + External Location — sin DBFS, sin Volumes, sin access keys, sin Kaggle MCP ni
ninguna llamada a Kaggle en tiempo de ejecución). Los CSV se subieron ahí manualmente, una
sola vez, fuera del pipeline — ver [datasets/](../../datasets/). Escriben tal cual (con
metadata de ingesta) a las tablas Bronze en Unity Catalog.

- [extract_who_covid.py](extract_who_covid.py) — dataset [worldwide-covid-19-who](../../datasets/worldwide-covid-19-who/) → `bronze.who_covid`
- [extract_covid_worldwide.py](extract_covid_worldwide.py) — dataset [coronavirus-covid-19-worldwide-2018-2026](../../datasets/coronavirus-covid-19-worldwide-2018-2026/) → `bronze.covid_worldwide`

Pendiente: subir los CSV reales a Azure y correr los notebooks para validar el schema.
