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

Un solo workflow ([deploy.yml](deploy.yml), basado en la plantilla YML3) parametrizado por
el ambiente resuelto a partir de la rama (`github.ref`), en vez de dos workflows
separados — evita duplicar los jobs. El `environment:` del job de GitHub Actions también
se resuelve por rama (`dev`/`prod`), así `secrets.DATABRICKS_HOST`/`DATABRICKS_TOKEN` toman
el valor correcto según el GitHub Environment configurado.

## Alcance del deploy — SOLO proceso/

El workflow ejecuta **únicamente** los notebooks `.py` dentro de [proceso/](../../proceso/),
en este DAG (ver detalle de cada etapa en su propio README):

1. [proceso/01_prepamb/prepamb.py](../../proceso/01_prepamb/prepamb.py) — lee y aplica
   [PrepAmb/](../../PrepAmb/) (catalog, schemas, storage credential, external location)
2. [proceso/02_extract/](../../proceso/02_extract/) — 2 notebooks en paralelo (uno por
   dataset) → Bronze
3. [proceso/03_transform/](../../proceso/03_transform/) — 1 notebook, une ambas fuentes
   Bronze en una sola tabla Silver (`silver.covid_unified`)
4. [proceso/04_load/](../../proceso/04_load/) — 1 notebook, consolida Silver en
   `golden.covid_summary_by_country` (métricas finales + per-cápita)
5. [proceso/05_grants/](../../proceso/05_grants/) — lee y aplica [seguridad/](../../seguridad/)

`PrepAmb/` y `seguridad/` no se ejecutan directamente ni son "deployados" por sí solos —
son la fuente de verdad (SQL/Python) que los notebooks 01 y 05 leen y aplican en tiempo de
ejecución. Fuera de `proceso/`, ninguna otra carpeta del repo es tocada por el pipeline:
[datasets/](../../datasets/), [dashboard/](../../dashboard/), [certificaciones/](../../certificaciones/)
y [evidencias/](../../evidencias/) son solo documentación/artefactos del repo — existen en
`main` porque `main` refleja el repo completo, pero el workflow nunca los lee ni los corre.

## Cómo cumple "un solo cluster encendido"

`adbk-dev` y `adbk-prod` son workspaces separados — un cluster no se puede compartir entre
ambos, así que "apuntar siempre al cluster de prod" no es viable. En su lugar,
[deploy.yml](deploy.yml) usa **Job Compute efímero** (`new_cluster`, no
`existing_cluster_id`): un único cluster **compartido por todas las tareas** del pipeline
vía `job_cluster_key`, Single Node (`num_workers: 0`), que Databricks levanta al arrancar
el job y apaga solo al terminar. Nunca queda un cluster prendido de forma persistente en
ningún ambiente — en cualquier momento hay como máximo uno encendido, el que está corriendo
esa corrida.

## Cómo se despliega el código — Databricks Repos API

`deploy.yml` **no** copia notebooks sueltos a una carpeta plana del workspace (eso rompería
`proceso/01_prepamb/prepamb.py`, que depende de que `PrepAmb/*.sql` exista como carpeta
hermana vía rutas relativas). En vez de eso, sincroniza el **repo completo** al workspace
usando la [Databricks Repos API](https://docs.databricks.com/api/workspace/repos):
crea (o actualiza) un Repo en `$REPO_PATH` apuntando a este repo de GitHub, en la rama que
disparó el workflow — así se preserva la estructura de carpetas tal cual está en git.

## Prerequisitos manuales (una sola vez, por workspace)

- **Credencial de Git en Databricks**: registrar un GitHub PAT en
  `adbk-dev` y `adbk-prod` (User Settings → Linked accounts → Git integration), para que la
  Repos API pueda clonar este repo (privado).
- **GitHub Environments**: crear `dev` y `prod` en Settings → Environments del repo, cada
  uno con secrets `DATABRICKS_HOST` y `DATABRICKS_TOKEN` apuntando a `adbk-dev` /
  `adbk-prod` respectivamente (token = Databricks PAT o Azure AD app con permisos sobre
  Jobs API y Repos API).
- Ajustar `REPO_PATH` en `deploy.yml` (`/Repos/<git-folder-owner>/SmartDataProject`) al
  usuario/service principal bajo el que quedó registrada la credencial de Git.

## Pendiente

- [x] `proceso/` completo end-to-end (`prepamb → extract x2 → transform → load → grants`) —
      `deploy.yml` referencia los 6 notebooks reales, DAG validado
- [ ] Confirmar cupo de la VM `Standard_DS3_v2` en la suscripción/región (`eastus2`)
- [ ] Completar los prerequisitos manuales de arriba (credencial de Git, GitHub
      Environments/secrets, `REPO_PATH`) y correr el workflow por primera vez
