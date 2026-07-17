# seguridad/

Scripts `.sql` con los GRANTS de Unity Catalog: quién puede usar el catalog/schemas y
consultar las tablas Bronze/Silver/Golden.

Estos scripts son la fuente de verdad de permisos; el notebook
[proceso/05_grants/grants.py](../proceso/05_grants/grants.py) los lee y aplica (vía
`spark.sql()`, con `{catalog}` sustituido dinámicamente) como último paso del pipeline.

| Archivo | Qué otorga |
|---|---|
| [01_grants_catalog.sql](01_grants_catalog.sql) | `USE CATALOG` sobre `{catalog}` |
| [02_grants_schemas.sql](02_grants_schemas.sql) | `USE SCHEMA` sobre `bronze`, `silver`, `golden` |
| [03_grants_tablas.sql](03_grants_tablas.sql) | `SELECT` sobre las 4 tablas finales (2 Bronze, 1 Silver, 1 Golden) |

## Principal: `account users`

Se le da acceso a **todos los usuarios del account de Databricks** (`account users`), no a
un grupo específico — mismo criterio ya usado en
[PrepAmb/04_external_location.sql](../PrepAmb/04_external_location.sql)
(`GRANT READ FILES ... TO \`account users\``), para no mezclar dos modelos de acceso
distintos dentro del mismo proyecto. Razonable para el alcance de este proyecto (datos
públicos de COVID-19, sin información sensible); si más adelante se necesita
diferenciar por rol (ej. `data_engineers` con más permisos que `analistas`), se reemplaza
`account users` por grupos específicos en estos mismos archivos, sin tocar `grants.py`.

## Por qué golden es la tabla más importante de las cuatro

`golden.covid_summary_by_country` es la que va a leer el dashboard de Databricks
Lakeview — si esa tabla no tiene `SELECT` otorgado, el dashboard no carga aunque todo lo
demás del pipeline haya corrido bien.
