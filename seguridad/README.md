# seguridad/

Scripts `.sql` con los GRANTS de Unity Catalog para usuarios y grupos: quién puede leer/
escribir sobre catalog, schemas y tablas Bronze/Silver/Golden.

Estos scripts son la fuente de verdad de permisos; el notebook en
[proceso/05_grants/](../proceso/05_grants/) los aplica como parte del despliegue CI/CD.

Convención sugerida:
- `01_grants_catalog.sql` — permisos a nivel catalog
- `02_grants_schemas.sql` — permisos a nivel schema (bronze/silver/golden)
- `03_grants_tablas.sql` — permisos específicos por tabla (si aplica)

Pendiente: definir grupos (ej. `data_engineers`, `analistas`) y sus permisos por capa.
