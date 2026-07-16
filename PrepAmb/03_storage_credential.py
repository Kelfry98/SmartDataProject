# PrepAmb 03 — Storage Credential (Managed Identity), vía Databricks SDK.
#
# CREATE STORAGE CREDENTIAL ... WITH AZURE_MANAGED_IDENTITY no es un comando SQL válido
# en Databricks: los Storage Credentials respaldados por Azure Managed Identity solo se
# pueden crear vía la UI o el Databricks SDK/CLI (Unity Catalog REST API) — por eso este
# paso es un script Python, no un .sql como 01/02/04. Validado manualmente en adbk-prod.
#
# Se crea una sola vez a nivel de metastore (no es específico de dev/prod); prepamb.py lo
# invoca en ambos ambientes de forma idempotente (get-or-create).

from databricks.sdk import WorkspaceClient
from databricks.sdk.service import catalog
from databricks.sdk.errors import NotFound


def create_storage_credential(name: str, access_connector_id: str, comment: str = "") -> None:
    w = WorkspaceClient()

    try:
        w.storage_credentials.get(name)
        return  # ya existe — idempotente
    except NotFound:
        pass

    w.storage_credentials.create(
        name=name,
        azure_managed_identity=catalog.AzureManagedIdentityRequest(
            access_connector_id=access_connector_id
        ),
        comment=comment,
    )
