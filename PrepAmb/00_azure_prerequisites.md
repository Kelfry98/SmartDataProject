# 00 — Prerequisitos de Azure (fuera de Databricks)

> **Estado: ya validado manualmente.** Todos los recursos de esta sección, incluyendo
> `raw_ext_loc` y su `GRANT READ FILES`, existen y están confirmados en Azure/Databricks —
> ver [PrepAmb/README.md](README.md).

## Recursos confirmados

| Recurso | Nombre |
|---|---|
| Resource Group | `rg-dbk-projects` (East US 2) |
| Storage Account (ADLS Gen2) | `stdbkprojectsraw` |
| Contenedor Raw | `raw` (dentro de `stdbkprojectsraw`) |
| Access Connector for Databricks | `ac-dbk-projects` |
| Databricks Workspaces | `adbk-dev` y `adbk-prod` — comparten el mismo metastore de Unity Catalog: `metastore_azure_eastus2` |
| Storage Credential (Unity Catalog) | `raw_sc` — Managed Identity, apunta a `ac-dbk-projects` |
| External Location (Unity Catalog) | `raw_ext_loc` — sobre `abfss://raw@stdbkprojectsraw.dfs.core.windows.net/`, creada y validada. `GRANT READ FILES` aplicado a `account users` |

```bash
RESOURCE_GROUP="rg-dbk-projects"
LOCATION="eastus2"
STORAGE_ACCOUNT="stdbkprojectsraw"
CONTAINER_NAME="raw"
ACCESS_CONNECTOR_NAME="ac-dbk-projects"
```

> Resource ID completo del Access Connector:
> `/subscriptions/16103103-9218-4387-9b8a-22036c92db03/resourceGroups/rg-dbk-projects/providers/Microsoft.Databricks/accessConnectors/ac-dbk-projects`
> Es el mismo `ACCESS_CONNECTOR_ID` que se pasa como parámetro `access_connector_id` a
> [03_storage_credential.py](03_storage_credential.py) — se reusa para dev y prod (el
> storage credential y la external location son compartidos entre ambientes, ya que ambos
> workspaces cuelgan del mismo metastore).

Los pasos 1–5 de abajo quedan documentados como referencia de cómo se creó cada recurso
(por si hay que recrearlo en otra suscripción/región).

## 1. Resource Group (si no existe)

```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
```

## 2. Storage Account (ADLS Gen2 — requiere hierarchical namespace habilitado)

```bash
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2 \
  --hierarchical-namespace true
```

## 3. Contenedor Raw

```bash
az storage container create \
  --account-name $STORAGE_ACCOUNT \
  --name $CONTAINER_NAME \
  --auth-mode login
```

Ahí ya están subidos los 2 CSV, uno por carpeta (ver [datasets/](../datasets/)):
- `who-covid-daily/WHO-COVID-19-global-daily-data.csv`
- `covid-historical-series/covid_historical_time_series.csv`

## 4. Access Connector for Databricks (Managed Identity)

Este recurso expone una **System Assigned Managed Identity** que Databricks usa para
autenticarse contra el Storage Account — sin access keys, sin SAS tokens.

Requiere la extensión `databricks` de az cli: `az extension add --name databricks`.

```bash
az databricks access-connector create \
  --name $ACCESS_CONNECTOR_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --identity-type SystemAssigned
```

Guarda el `id` (resource ID) que devuelve este comando — se usa como
`ACCESS_CONNECTOR_ID` en [03_storage_credential.py](03_storage_credential.py). Ver nota
arriba: ya existe (`ac-dbk-projects`), este paso solo aplica si hay que recrearlo en otra
suscripción.

## 5. Asignar rol IAM sobre el Storage Account a la Managed Identity del connector

```bash
CONNECTOR_PRINCIPAL_ID=$(az databricks access-connector show \
  --name $ACCESS_CONNECTOR_NAME \
  --resource-group $RESOURCE_GROUP \
  --query identity.principalId -o tsv)

STORAGE_ID=$(az storage account show \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query id -o tsv)

az role assignment create \
  --assignee-object-id $CONNECTOR_PRINCIPAL_ID \
  --assignee-principal-type ServicePrincipal \
  --role "Storage Blob Data Contributor" \
  --scope $STORAGE_ID
```

> `Storage Blob Data Contributor` permite leer y escribir. Si Raw debe ser estrictamente
> de solo lectura desde Databricks, usar `Storage Blob Data Reader` en su lugar.

## 6. Valores a pasar a Unity Catalog / CI-CD

| Valor | Dónde se usa |
|---|---|
| `ACCESS_CONNECTOR_ID` (ver nota arriba) | [03_storage_credential.py](03_storage_credential.py) |

`STORAGE_ACCOUNT`/`CONTAINER_NAME` ya no se pasan como parámetro: quedaron fijos dentro de
[04_external_location.sql](04_external_location.sql) (`stdbkprojectsraw`/`raw`), ya creada.

`ACCESS_CONNECTOR_ID` se guarda como **GitHub Secret** (por ambiente: dev/prod) y se pasa
como parámetro al job de Databricks que corre [proceso/01_prepamb/prepamb.py](../proceso/01_prepamb/prepamb.py).

Pendiente: cargar `access_connector_id` como GitHub Secret (uno por ambiente, apuntando al
workspace `adbk-dev` o `adbk-prod` correspondiente).
