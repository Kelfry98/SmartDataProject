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
| `access_connector_id` | Resource ID del Access Connector for Databricks | GitHub Secret |

`storage_account`/`container_name` ya no son parámetros de este notebook: el external
location (`04_external_location.sql`) quedó con la URL fija (`stdbkprojectsraw`/`raw`), ya
creada y validada — no se parametriza.

## Notas de implementación

- **Resolución de ruta a `PrepAmb/`**: probado manualmente en `adbk-dev` corriendo el
  notebook con "Run all" interactivo — `__file__` no está definido en ese modo (solo es
  confiable dentro de un Job). Se corrigió usando el contexto del notebook en su lugar:
  ```python
  NOTEBOOK_DIR = "/Workspace" + os.path.dirname(
      dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
  )
  ```
  Esto funciona tanto en ejecución interactiva como en Jobs. El mismo patrón (y el mismo
  fix) aplica en [proceso/05_grants/grants.py](../05_grants/grants.py), que resuelve la
  ruta a [seguridad/](../../seguridad/) de la misma forma.
- `03_storage_credential.py` importa `databricks.sdk`. En Databricks Runtime 14.3 LTS+ ya
  viene preinstalado; en runtimes más viejos hay que agregar `%pip install databricks-sdk`
  antes de correr este paso.
- `WorkspaceClient()` se autentica automáticamente con el contexto del notebook (no
  necesita host/token explícitos) siempre que el cluster tenga Unity Catalog habilitado.
