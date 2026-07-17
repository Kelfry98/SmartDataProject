# proceso/05_grants

[grants.py](grants.py) — notebook que lee y aplica los `.sql` de
[seguridad/](../../seguridad/) sobre el catalog del ambiente actual. Último nodo del DAG
del pipeline (después de [04_load](../04_load/)).

Usa `spark.sql()` para los `GRANT` — misma excepción a "100% PySpark" ya documentada en
[01_prepamb/](../01_prepamb/): `GRANT`/`USE CATALOG`/`USE SCHEMA` son DDL de Unity Catalog
sin equivalente en el DataFrame API. Extract/Transform/Load sí son 100% PySpark.

## Qué otorga, en orden

1. `USE CATALOG` sobre `{catalog}` ([01_grants_catalog.sql](../../seguridad/01_grants_catalog.sql))
2. `USE SCHEMA` sobre `bronze`, `silver`, `golden` ([02_grants_schemas.sql](../../seguridad/02_grants_schemas.sql))
3. `SELECT` sobre `bronze.who_covid_daily`, `bronze.covid_historical_series`,
   `silver.covid_unified`, `golden.covid_summary_by_country` ([03_grants_tablas.sql](../../seguridad/03_grants_tablas.sql))

Los tres pasos son necesarios porque los permisos de Unity Catalog son jerárquicos:
`SELECT` en una tabla no alcanza si falta `USE CATALOG`/`USE SCHEMA` en el nivel de arriba.

Principal y criterio de acceso (`account users`) documentados en
[seguridad/README.md](../../seguridad/README.md).

`{catalog}` se resuelve dinámicamente vía el widget `environment`, igual que en el resto
del pipeline.
