# seguridad/

Scripts `.sql` con los GRANTS de Unity Catalog: quién puede usar el catalog/schemas y
consultar las tablas Bronze/Silver/Golden. Son la fuente de verdad de permisos; el notebook
[proceso/05_grants/grants.py](../proceso/05_grants/grants.py) los lee y aplica (vía
`spark.sql()`, con `{catalog}` sustituido dinámicamente) como último paso del pipeline.

| Archivo | Qué otorga |
|---|---|
| [01_grants_catalog.sql](01_grants_catalog.sql) | `USE CATALOG` sobre `{catalog}` |
| [02_grants_schemas.sql](02_grants_schemas.sql) | `USE SCHEMA` sobre `bronze`, `silver`, `golden` |
| [03_grants_tablas.sql](03_grants_tablas.sql) | `SELECT` sobre las 4 tablas finales (2 Bronze, 1 Silver, 1 Golden) |

Los permisos de Unity Catalog son jerárquicos: `SELECT` en una tabla no alcanza sin
`USE CATALOG`/`USE SCHEMA` en los niveles de arriba.

## Principal: `account users`

Acceso a todos los usuarios del account de Databricks (`account users`), mismo criterio
usado en [PrepAmb/04_external_location.sql](../PrepAmb/04_external_location.sql). Para
diferenciar por rol, se reemplaza `account users` por grupos específicos en estos archivos,
sin tocar `grants.py`.
