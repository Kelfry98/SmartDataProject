# proceso/

Notebooks `.py` (100% PySpark, sin Spark SQL) que implementan el pipeline ETL medallion.
Esta carpeta completa es lo que se despliega a producción vía CI/CD.

Orden de ejecución del pipeline:

1. [01_prepamb/](01_prepamb/) — ejecuta los `.sql` de [PrepAmb/](../PrepAmb/) (catalog, schemas, external location)
2. [02_extract/](02_extract/) — Extract: lee Raw (Azure Blob Storage vía Managed Identity) y escribe Bronze
3. [03_transform/](03_transform/) — Transform: limpia/transforma Bronze y escribe Silver
4. [04_load/](04_load/) — Load: modela/agrega Silver y escribe Golden
5. [05_grants/](05_grants/) — aplica los `.sql` de [seguridad/](../seguridad/) sobre catalog/schemas/tablas

Cada dataset (ambos de COVID-19: [worldwide-covid-19-who](../datasets/worldwide-covid-19-who/)
y [coronavirus-covid-19-worldwide-2018-2026](../datasets/coronavirus-covid-19-worldwide-2018-2026/))
tiene su propio notebook en cada etapa (extract/transform/load), o un notebook parametrizado
por dataset — a definir al implementar.
