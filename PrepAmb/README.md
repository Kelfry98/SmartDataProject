# PrepAmb/

Preparación de ambiente: prerequisitos de Azure + scripts de Unity Catalog (catalog,
schemas, storage credential, external location). Estos scripts son la fuente de verdad;
el notebook [proceso/01_prepamb/prepamb.py](../proceso/01_prepamb/prepamb.py) los ejecuta
(parametrizados), en orden, como primer paso del pipeline de CI/CD.

| # | Archivo | Tipo | Qué crea | Alcance |
|---|---|---|---|---|
| 00 | [00_azure_prerequisites.md](00_azure_prerequisites.md) | doc | Resource Group, Storage Account, contenedor `raw`, Access Connector (Managed Identity), rol IAM | Manual, una sola vez |
| 01 | [01_catalog.sql](01_catalog.sql) | SQL | `CREATE CATALOG {catalog}` con `MANAGED LOCATION` explícita | Por ambiente (dev_catalog / prod_catalog) |
| 02 | [02_schemas.sql](02_schemas.sql) | SQL | Schemas `bronze`, `silver`, `golden` | Por ambiente |
| 03 | [03_storage_credential.py](03_storage_credential.py) | **Python (Databricks SDK)** | Storage Credential `raw_sc` respaldado por la Managed Identity | Compartido (una vez) |
| 04 | [04_external_location.sql](04_external_location.sql) | SQL | External Location `raw_ext_loc` + `GRANT READ FILES` a `account users` | Compartido (una vez), depende de 03 |

> **Por qué 03 es `.py` y no `.sql`**: `CREATE STORAGE CREDENTIAL ... WITH
> AZURE_MANAGED_IDENTITY` no es un comando SQL válido en Databricks — un Storage
> Credential respaldado por Azure Managed Identity solo se puede crear vía la UI o el
> Databricks SDK/CLI (Unity Catalog REST API). Validado manualmente en adbk-prod. El resto
> del pipeline (01, 02, 04, y Extract/Transform/Load) sí es 100% SQL/PySpark según
> corresponda — esta es la única excepción, y por eso el orden de ejecución
> (01 → 02 → 03 → 04) importa: 04 depende de que `raw_sc` (creado en 03) ya exista.

> **Por qué 01 usa `MANAGED LOCATION` explícita**: probado manualmente en `adbk-dev` — sin
> ella, `CREATE CATALOG` fallaba con `Metastore storage root URL does not exist`, porque el
> metastore (`metastore_azure_eastus2`) no tiene una Default Storage Location configurada a
> nivel de metastore. Se agregó `MANAGED LOCATION 'abfss://raw@stdbkprojectsraw.dfs.core.windows.net/catalog-{catalog}/'`
> en [01_catalog.sql](01_catalog.sql) para que cada catalog defina su propia ubicación
> administrada, reutilizando el mismo storage account/external location ya autorizado vía
> `raw_sc`. Validado: `02_schemas.sql` no necesitó cambios — los schemas heredan la
> ubicación del catalog padre.

## Recursos de Azure/Databricks (confirmados)

| Recurso | Nombre |
|---|---|
| Resource Group | `rg-dbk-projects` (East US 2) |
| Storage Account (ADLS Gen2) | `stdbkprojectsraw` |
| Contenedor Raw | `raw` |
| Access Connector | `ac-dbk-projects` |
| Storage Credential (UC) | `raw_sc` |
| External Location (UC) | `raw_ext_loc` → `abfss://raw@stdbkprojectsraw.dfs.core.windows.net/` |
| Workspaces Databricks | `adbk-dev`, `adbk-prod` — mismo metastore: `metastore_azure_eastus2` |

Detalle completo en [00_azure_prerequisites.md](00_azure_prerequisites.md).

## Estrategia dev/prod

Catalogs separados: `dev_catalog` y `prod_catalog`, sobre el mismo metastore
(`metastore_azure_eastus2`, compartido por `adbk-dev` y `adbk-prod`). El storage
credential (`raw_sc`) y el external location (`raw_ext_loc`) son compartidos — apuntan al
mismo contenedor Raw; solo el catalog y sus schemas son específicos del ambiente. El
ambiente (`dev`/`prod`) se pasa como parámetro del job de Databricks, inyectado por el
workflow de GitHub Actions según la rama que disparó el pipeline: push a `dev` →
workspace `adbk-dev` / `environment=dev`, push/merge a `main` → workspace `adbk-prod` /
`environment=prod` (ver [.github/workflows/README.md](../.github/workflows/README.md)).

## Acceso a Raw

Exclusivamente vía Managed Identity (Storage Credential + External Location). No se usa
DBFS ni Databricks Volumes.

## Reversión

Ver [reversion/prepamb/](../reversion/prepamb/) para los DROP correspondientes.

## Pendiente

- [x] Recursos de Azure confirmados (resource group, storage account, contenedor, access
      connector, storage credential) — ver tabla arriba
- [x] `raw_ext_loc` creada y validada manualmente, `GRANT READ FILES` aplicado a
      `account users`
- [ ] Cargar `access_connector_id` como GitHub Secret (por ambiente)
