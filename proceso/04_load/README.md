# proceso/04_load

Notebooks `.py` de Load (Golden). 100% PySpark.

Leen de las tablas Silver en Unity Catalog, agregan/modelan para consumo analítico
(dimensiones, métricas) y escriben a las tablas Golden que alimentan el dashboard de
Databricks Lakeview.

Pendiente:
- `load_who_covid.py`
- `load_covid_worldwide.py`
