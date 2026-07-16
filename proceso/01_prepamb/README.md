# proceso/01_prepamb

[prepamb.py](prepamb.py) — notebook que ejecuta la preparación de ambiente a partir de
[PrepAmb/](../../PrepAmb/), en orden: `01_catalog.sql` → `02_schemas.sql` →
`03_storage_credential.py` → `04_external_location.sql`.

01/02/04 son DDL de Unity Catalog vía `spark.sql(...)` (CREATE CATALOG/SCHEMA/EXTERNAL
LOCATION — sin equivalente en el DataFrame API). 03 es la única excepción a SQL: carga y
ejecuta `PrepAmb/03_storage_credential.py`, que usa el **Databricks SDK**
(`WorkspaceClient`), porque `CREATE STORAGE CREDENTIAL ... WITH AZURE_MANAGED_IDENTITY`
no es un comando SQL válido en Databricks. 04 depende de que 03 haya corrido antes (usa
el storage credential `raw_sc`). Extract/Transform/Load son 100% PySpark.

## Parámetros (widgets)

| Widget | Descripción | Quién lo inyecta |
|---|---|---|
| `environment` | `dev` o `prod` → determina el catalog (`{environment}_catalog`) | Job de Databricks (desde GitHub Actions) |
| `storage_account` | Nombre del Storage Account de Raw | GitHub Secret |
| `container_name` | Contenedor de Raw (default `raw`) | GitHub Secret / default |
| `access_connector_id` | Resource ID del Access Connector for Databricks | GitHub Secret |

## Notas de implementación pendientes de verificar

- El notebook resuelve la ruta a [PrepAmb/](../../PrepAmb/) vía `__file__`, asumiendo que
  corre como parte de un Databricks Repo (Files in Repos). Si el cluster/runtime usado no
  soporta `__file__` en notebooks, hay que ajustar la resolución de ruta (por ejemplo,
  pasando la ruta absoluta del repo como parámetro adicional del job).
- `03_storage_credential.py` importa `databricks.sdk`. En Databricks Runtime 14.3 LTS+ ya
  viene preinstalado; en runtimes más viejos hay que agregar `%pip install databricks-sdk`
  antes de correr este paso.
- `WorkspaceClient()` se autentica automáticamente con el contexto del notebook (no
  necesita host/token explícitos) siempre que el cluster tenga Unity Catalog habilitado.
