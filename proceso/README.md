# proceso/

Notebooks `.py` (100% PySpark, sin Spark SQL) que implementan el pipeline ETL medallion.
Esta carpeta completa es lo que se despliega a producción vía CI/CD.

Orden de ejecución del pipeline:

1. [01_prepamb/](01_prepamb/) — ejecuta los `.sql`/`.py` de [PrepAmb/](../PrepAmb/) (catalog, schemas, storage credential, external location)
2. [02_extract/](02_extract/) — Extract: 2 notebooks en paralelo (uno por dataset), leen Raw (Azure Blob Storage vía Managed Identity) y escriben Bronze
3. [03_transform/](03_transform/) — Transform: 1 notebook, une ambas tablas Bronze en una sola tabla Silver (`silver.covid_unified`)
4. [04_load/](04_load/) — Load: 1 notebook, consolida Silver en `golden.covid_summary_by_country` (métricas finales + per-cápita)
5. [05_grants/](05_grants/) — aplica los `.sql` de [seguridad/](../seguridad/) sobre catalog/schemas/tablas

Extract usa **un notebook por dataset** (paralelizable, un fallo no bloquea al otro — ver
[02_extract/README.md](02_extract/README.md)). Transform y Load usan **un solo notebook**
cada uno para ambos datasets, porque su trabajo es justamente cruzarlos/consolidarlos en
una tabla unificada — ver [03_transform/README.md](03_transform/README.md) y
[04_load/README.md](04_load/README.md) para el detalle de cada uno.
