# PrepAmb/

Preparación de ambiente: prerequisitos de Azure + scripts de Unity Catalog (catalog,
schemas, storage credential, external location). Son la fuente de verdad; el notebook
[proceso/01_prepamb/prepamb.py](../proceso/01_prepamb/prepamb.py) los ejecuta
(parametrizados), en orden, como primer paso del pipeline.

| # | Archivo | Tipo | Qué crea | Alcance |
|---|---|---|---|---|
| 00 | [00_azure_prerequisites.md](00_azure_prerequisites.md) | doc | Resource Group, Storage Account, contenedor `raw`, Access Connector (Managed Identity), rol IAM | Manual, una sola vez |
| 01 | [01_catalog.sql](01_catalog.sql) | SQL | `CREATE CATALOG {catalog}` con `MANAGED LOCATION` explícita | Por ambiente (dev_catalog / prod_catalog) |
| 02 | [02_schemas.sql](02_schemas.sql) | SQL | Schemas `bronze`, `silver`, `golden` | Por ambiente |
| 03 | [03_storage_credential.py](03_storage_credential.py) | **Python (Databricks SDK)** | Storage Credential `raw_sc` respaldado por la Managed Identity | Compartido (una vez) |
| 04 | [04_external_location.sql](04_external_location.sql) | SQL | External Location `raw_ext_loc` + `GRANT READ FILES` a `account users` | Compartido (una vez), depende de 03 |

El paso 03 es Python (Databricks SDK) porque `CREATE STORAGE CREDENTIAL ... WITH
AZURE_MANAGED_IDENTITY` no es un comando SQL válido en Databricks; se crea vía UI o SDK/CLI.
El orden importa: 04 depende de que `raw_sc` (creado en 03) ya exista.

## Recursos de Azure/Databricks

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

Catalogs separados `dev_catalog` y `prod_catalog` sobre el mismo metastore
(`metastore_azure_eastus2`, compartido por `adbk-dev` y `adbk-prod`). El storage credential
(`raw_sc`) y el external location (`raw_ext_loc`) son compartidos; solo el catalog y sus
schemas son específicos del ambiente. El ambiente (`dev`/`prod`) se pasa como parámetro del
job, según la rama que disparó el pipeline (ver [.github/workflows/README.md](../.github/workflows/README.md)).

## Acceso a Raw

Exclusivamente vía Managed Identity (Storage Credential + External Location). No se usa DBFS
ni Databricks Volumes.

## Reversión

Ver [reversion/prepamb/](../reversion/prepamb/) para los DROP correspondientes.
