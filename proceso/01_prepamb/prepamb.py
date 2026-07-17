# Databricks notebook source
# Prepara el ambiente (dev|prod) en Unity Catalog, corriendo PrepAmb/ en orden:
# 01_catalog.sql -> 02_schemas.sql -> 03_storage_credential.py -> 04_external_location.sql
#
# 03 es Python (Databricks SDK), no SQL: CREATE STORAGE CREDENTIAL ... WITH
# AZURE_MANAGED_IDENTITY no es un comando SQL válido en Databricks, solo se puede crear
# vía UI o el SDK/CLI (Unity Catalog REST API). 04 depende de que el storage credential
# de 03 ya exista. 01/02/04 sí son DDL válido en SQL (única excepción al "100% PySpark"
# del resto del pipeline: Extract/Transform/Load).

import os
import importlib.util

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
dbutils.widgets.text(
    "access_connector_id",
    "/subscriptions/16103103-9218-4387-9b8a-22036c92db03/resourceGroups/rg-dbk-projects/providers/Microsoft.Databricks/accessConnectors/ac-dbk-projects",
    "Resource ID del Access Connector",
)

environment = dbutils.widgets.get("environment")
access_connector_id = dbutils.widgets.get("access_connector_id")

catalog = f"{environment}_catalog"

# En Databricks Repos este notebook vive en proceso/01_prepamb/, PrepAmb/ es
# hermano de proceso/ en la raíz del repo.
NOTEBOOK_DIR = os.path.dirname(os.path.abspath(__file__))
PREPAMB_DIR = os.path.normpath(os.path.join(NOTEBOOK_DIR, "..", "..", "PrepAmb"))


def run_sql_file(filename: str, **params: str) -> None:
    path = os.path.join(PREPAMB_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        # Se filtran las líneas de comentario ANTES de unir y separar por ";" — si no,
        # un bloque de comentarios pegado (sin ";" de por medio) al primer statement real
        # hace que todo el bloque se lea como "empieza con --" y ese statement se salte.
        lines = [line for line in f if not line.strip().startswith("--")]
    sql = "".join(lines).format(**params)
    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            spark.sql(statement)


def load_module(filename: str):
    path = os.path.join(PREPAMB_DIR, filename)
    module_name = filename.replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# COMMAND ----------

# 01 — Catalog del ambiente actual
run_sql_file("01_catalog.sql", catalog=catalog)

# COMMAND ----------

# 02 — Schemas bronze/silver/golden del ambiente actual
run_sql_file("02_schemas.sql", catalog=catalog)

# COMMAND ----------

# 03 — Storage Credential (Managed Identity), vía Databricks SDK — compartido entre
# ambientes, idempotente (get-or-create dentro del módulo).
storage_credential = load_module("03_storage_credential.py")
storage_credential.create_storage_credential(
    name="raw_sc",
    access_connector_id=access_connector_id,
    comment="Managed identity credential for raw layer",
)

# COMMAND ----------

# 04 — External Location apuntando al contenedor Raw — compartido entre ambientes.
# Depende de que raw_sc (paso 03) ya exista. Valores fijos dentro del .sql (ya creada y
# validada en Azure/Databricks), no toma storage_account/container_name como parámetro.
run_sql_file("04_external_location.sql")

# COMMAND ----------

dbutils.notebook.exit(catalog)
