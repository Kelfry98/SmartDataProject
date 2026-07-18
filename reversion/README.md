# reversion/

Scripts de reversión (rollback) para deshacer lo creado por el pipeline: DROP de tablas,
schemas y objetos de Unity Catalog. Todos son idempotentes (`DROP ... IF EXISTS`).

Orden inverso de dependencia (Golden → Silver → Bronze → PrepAmb):

- `golden/` — DROP de la tabla Golden
- `silver/` — DROP de la tabla Silver
- `bronze/` — DROP de las tablas Bronze
- `prepamb/` — DROP de catalog/schemas (por ambiente) y de external location/storage
  credential (compartidos entre dev y prod)
