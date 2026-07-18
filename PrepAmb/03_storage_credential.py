# PrepAmb 03 — Storage Credential (Managed Identity) vía Databricks SDK, idempotente (get-or-create).
# Es Python porque CREATE STORAGE CREDENTIAL ... WITH AZURE_MANAGED_IDENTITY no es SQL válido en Databricks.

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
