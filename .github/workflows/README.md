# .github/workflows/

Workflows de GitHub Actions para el CI/CD del pipeline.

> Nota: la carpeta correcta que reconoce GitHub Actions es `.github/workflows/` (plural).
> El requisito original decía `.github/workflow/`; se corrigió aquí porque con el nombre
> en singular GitHub no descubre ni ejecuta ningún workflow.

## Ramas y ambientes

Dos ramas, dos ambientes — 1:1:

- **`dev`** — rama de trabajo. Push a `dev` dispara el workflow apuntando al workspace
  **`adbk-dev`** / catalog `dev_catalog` (ver [PrepAmb/README.md](../../PrepAmb/README.md)).
- **`main`** — rama de producción. El merge/push a `main` (vía PR desde `dev`) dispara el
  mismo workflow apuntando al workspace **`adbk-prod`** / catalog `prod_catalog`. `main`
  siempre refleja lo que está realmente desplegado en producción.

Ambos workspaces (`adbk-dev`, `adbk-prod`) cuelgan del mismo metastore de Unity Catalog
(`metastore_azure_eastus2`) y comparten el storage credential (`raw_sc`) y external
location (`raw_ext_loc`) — lo único que cambia entre ambientes es el catalog y el
workspace host/token usado por el job de Databricks.

Un solo workflow (usando la plantilla YML3) parametrizado por el ambiente resuelto a partir
de la rama (`github.ref`), en vez de dos workflows separados — evita duplicar los jobs.

## Jobs del pipeline

1. **Prep ambiente** — ejecuta scripts de [PrepAmb/](../../PrepAmb/) (catalog, schemas, external location)
2. **Extract** — corre notebooks de [proceso/02_extract/](../../proceso/02_extract/) (Bronze)
3. **Transform** — corre notebooks de [proceso/03_transform/](../../proceso/03_transform/) (Silver)
4. **Load** — corre notebooks de [proceso/04_load/](../../proceso/04_load/) (Golden)
5. **Grants** — aplica permisos de [seguridad/](../../seguridad/) vía [proceso/05_grants/](../../proceso/05_grants/)

Restricción de infraestructura: un único cluster Databricks encendido, y debe ser el de
producción (los jobs de dev también deben apuntar a ese cluster o usar Jobs Compute
efímero, para no mantener más de un cluster activo).

Pendiente: `deploy.yml` con los jobs anteriores encadenados, trigger `push` en `dev` y
`main`, ambiente resuelto por rama, y `dev`/`prod` configurados como GitHub Environments
(con sus secrets: Databricks host, token/SPN, etc.).
