# .github/workflows/

Workflows de GitHub Actions para el CI/CD del pipeline.

## Ramas y ambientes

Dos ramas, dos ambientes — 1:1:

- **`dev`** — rama de trabajo. Push a `dev` dispara el workflow apuntando al workspace
  **`adbk-dev`** / catalog `dev_catalog`.
- **`main`** — rama de producción. El merge/push a `main` (vía PR desde `dev`) dispara el
  mismo workflow apuntando a **`adbk-prod`** / catalog `prod_catalog`.

Ambos workspaces cuelgan del mismo metastore (`metastore_azure_eastus2`) y comparten el
storage credential (`raw_sc`) y external location (`raw_ext_loc`); lo único que cambia entre
ambientes es el catalog y el host/token del workspace.

Un solo workflow ([deploy.yml](deploy.yml)) parametrizado por el ambiente resuelto a partir
de la rama (`github.ref`). El `environment:` del job de GitHub Actions también se resuelve
por rama, así `secrets.DATABRICKS_HOST`/`DATABRICKS_TOKEN` toman el valor del GitHub
Environment correspondiente.

## Alcance del deploy — SOLO proceso/

El workflow ejecuta únicamente los notebooks `.py` dentro de [proceso/](../../proceso/), en
este DAG:

1. [proceso/01_prepamb/prepamb.py](../../proceso/01_prepamb/prepamb.py) — aplica [PrepAmb/](../../PrepAmb/)
2. [proceso/02_extract/](../../proceso/02_extract/) — 2 notebooks en paralelo → Bronze
3. [proceso/03_transform/](../../proceso/03_transform/) — 1 notebook → `silver.covid_unified`
4. [proceso/04_load/](../../proceso/04_load/) — 1 notebook → `golden.covid_summary_by_country`
5. [proceso/05_grants/](../../proceso/05_grants/) — aplica [seguridad/](../../seguridad/)

`PrepAmb/` y `seguridad/` no se ejecutan por sí solos: son la fuente de verdad que los
notebooks 01 y 05 leen y aplican en tiempo de ejecución. Fuera de `proceso/`, ninguna otra
carpeta es tocada por el pipeline (`datasets/`, `dashboard/`, `certificaciones/`,
`evidencias/` son solo documentación/artefactos).

## Cluster

[deploy.yml](deploy.yml) usa **Job Compute efímero** (`new_cluster`): un único cluster
compartido por todas las tareas vía `job_cluster_key`, Single Node (`num_workers: 0`), que
Databricks levanta al arrancar el job y apaga al terminar — nunca queda un cluster prendido
de forma persistente. Node type `Standard_D4plds_v6` (ARM), runtime DBR `17.3.x-scala2.13`.

## Despliegue del código — Databricks Repos API

`deploy.yml` sincroniza el repo completo al workspace vía la
[Databricks Repos API](https://docs.databricks.com/api/workspace/repos) (crea/actualiza un
Repo en `$REPO_PATH` en la rama que disparó el workflow), en vez de copiar notebooks sueltos
— así se preserva la estructura de carpetas y `prepamb.py` encuentra `PrepAmb/*.sql` como
carpeta hermana.

## Prerequisitos manuales (una sola vez, por workspace)

- **Credencial de Git en Databricks**: registrar un GitHub PAT en `adbk-dev` y `adbk-prod`
  (User Settings → Linked accounts → Git integration).
- **GitHub Environments**: crear `dev` y `prod` (Settings → Environments), cada uno con
  secrets `DATABRICKS_HOST` y `DATABRICKS_TOKEN` apuntando a `adbk-dev` / `adbk-prod`.
- Ajustar `REPO_PATH` en `deploy.yml` al usuario/service principal bajo el que quedó
  registrada la credencial de Git.

## Cuota Azure

`adbk-dev` y `adbk-prod` comparten la misma suscripción, con un límite de 4 vCPUs totales en
East US 2. Como cada corrida usa un cluster de 4 vCPUs, dev y prod no pueden correr en
paralelo; para habilitarlo, solicitar aumento de cuota a 8 vCPUs.
