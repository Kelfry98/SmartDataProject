# SmartDataProject

ETL medallion (Bronze → Silver → Golden) en Databricks + Unity Catalog, 100% PySpark,
con la capa Raw en Azure Blob Storage accedida únicamente vía Managed Identity, y CI/CD
con GitHub Actions desplegando de `dev` a `prod`.

> Estado: en construcción. Este README se irá completando a medida que avance el proyecto
> (empezando por [PrepAmb/](PrepAmb/)).

## Arquitectura

```
Kaggle CSV (descarga manual, una sola vez)
                     │
                     ▼
        Azure Blob Storage / ADLS Gen2 (stdbkprojectsraw)
        contenedor "raw"
        [acceso desde Databricks SOLO vía Managed Identity:
         Storage Credential "raw_sc" + External Location "raw_ext_loc"]
                     │
                     ▼
        ┌─────────────────────────┐
        │   BRONZE   (Extract)    │  proceso/02_extract/
        │   Unity Catalog table   │
        └────────────┬─────────────┘
                     ▼
        ┌─────────────────────────┐
        │   SILVER   (Transform)  │  proceso/03_transform/
        │   Unity Catalog table   │
        └────────────┬─────────────┘
                     ▼
        ┌─────────────────────────┐
        │   GOLDEN   (Load)       │  proceso/04_load/
        │   Unity Catalog table   │
        └────────────┬─────────────┘
                     ▼
          Databricks Lakeview Dashboard
```

*(Diagrama definitivo pendiente — se agregará imagen/export en una siguiente iteración.)*

## Datasets

Ambos sobre COVID-19, obtenidos de Kaggle:

- [Worldwide COVID-19 Data from WHO](https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who) — ver [datasets/worldwide-covid-19-who/](datasets/worldwide-covid-19-who/)
- [Coronavirus (COVID-19) Worldwide Data (2018-2026)](https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026) — ver [datasets/coronavirus-covid-19-worldwide-2018-2026/](datasets/coronavirus-covid-19-worldwide-2018-2026/)

Los CSV se descargan de Kaggle **manualmente, una sola vez**, fuera del pipeline, y se
suben directo al contenedor `raw` en Azure Blob Storage (ADLS Gen2) — no se descargan en
tiempo de ejecución ni pasan por la carpeta [datasets/](datasets/) del repo, que queda
solo como referencia de qué se usó y de dónde salió. El notebook de Extract lee esos CSV
directo desde la external location de Unity Catalog vía Managed Identity.

## Recursos de Azure/Databricks

Ya provisionados y confirmados manualmente (detalle completo en [PrepAmb/00_azure_prerequisites.md](PrepAmb/00_azure_prerequisites.md)):

| Recurso | Nombre |
|---|---|
| Resource Group | `rg-dbk-projects` (East US 2) |
| Storage Account (ADLS Gen2) | `stdbkprojectsraw` |
| Contenedor Raw | `raw` |
| Access Connector | `ac-dbk-projects` |
| Storage Credential (Unity Catalog) | `raw_sc` |
| External Location (Unity Catalog) | `raw_ext_loc` |
| Workspaces Databricks | `adbk-dev`, `adbk-prod` — mismo metastore `metastore_azure_eastus2` |

## Estructura del repositorio

| Carpeta | Contenido |
|---|---|
| [datasets/](datasets/) | Solo referencia/documentación de cada dataset (los CSV reales viven en Azure Blob Storage) |
| [dashboard/](dashboard/) | Export del dashboard Lakeview (.json, .png, .pbix) |
| [reversion/](reversion/) | Scripts DROP por capa (bronze/silver/golden) |
| [.github/workflows/](.github/workflows/) | Workflow de CI/CD (GitHub Actions) |
| [seguridad/](seguridad/) | GRANTS de usuarios/grupos en Unity Catalog (.sql) |
| [PrepAmb/](PrepAmb/) | Preparación de ambiente: catalog, schemas, external location (.sql) |
| [proceso/](proceso/) | Notebooks .py del ETL (prepamb, extract, transform, load, grants) — esto se despliega a producción |
| [certificaciones/](certificaciones/) | Certificaciones (bonus) |
| [evidencias/](evidencias/) | Capturas de ejecución correcta (Databricks Workflows, GitHub Actions, Azure) |

## Pipeline CI/CD

Dos ramas, dos ambientes: se trabaja en **`dev`** (push dispara el pipeline apuntando al
ambiente dev) y el pase a **`prod`** ocurre al mergear/pushear a **`main`** (el mismo
workflow, ambiente resuelto por rama). Detalle en [.github/workflows/README.md](.github/workflows/README.md).

Un único workflow de GitHub Actions (plantilla YML3) en este orden: **Prep ambiente →
Extract → Transform → Load → Grants**. Restricción de infraestructura: un solo cluster
Databricks encendido (el de producción).

## Seguridad y acceso a datos

La capa Raw vive en Azure Blob Storage (`stdbkprojectsraw`, contenedor `raw`) y se accede
exclusivamente mediante Managed Identity: Storage Credential `raw_sc` + External Location
`raw_ext_loc` de Unity Catalog. No se usa DBFS ni Databricks Volumes para el acceso a Raw.

## Pendiente

- [x] Rama `dev` creada — trabajo diario aquí, `main` = prod
- [x] Recursos de Azure/Databricks provisionados y confirmados (ver tabla arriba)
- [x] PrepAmb: catalog, schemas, storage credential (scripts listos) — falta correr
      [proceso/01_prepamb/prepamb.py](proceso/01_prepamb/) para crear/confirmar `raw_ext_loc`
- [x] Extract (Bronze) para ambos datasets — notebooks listos, leen vía external
      location (`spark.read.csv` sobre `abfss://...`); falta subir los CSV reales a
      Azure y correrlos
- [ ] Transform (Silver) para ambos datasets
- [ ] Load (Golden) para ambos datasets
- [ ] Grants
- [ ] Workflow de GitHub Actions
- [ ] Dashboard Lakeview
- [ ] Diagrama de arquitectura final
- [ ] Evidencias de ejecución
