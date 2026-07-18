# Databricks notebook source
# DBTITLE 1,Cell 1
# Prepara el ambiente (dev|prod) en Unity Catalog: catalog, schemas, storage credential y external location.

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

# Ruta a PrepAmb/, carpeta hermana de proceso/ en la raíz del repo.
NOTEBOOK_DIR = "/Workspace" + os.path.dirname(
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
)
PREPAMB_DIR = os.path.normpath(os.path.join(NOTEBOOK_DIR, "..", "..", "PrepAmb"))


def run_sql_file(filename: str, **params: str) -> None:
    path = os.path.join(PREPAMB_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        # Descarta líneas de comentario antes de separar por ";".
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

# 03 — Storage Credential (Managed Identity) vía Databricks SDK.
storage_credential = load_module("03_storage_credential.py")
storage_credential.create_storage_credential(
    name="raw_sc",
    access_connector_id=access_connector_id,
    comment="Managed identity credential for raw layer",
)

# COMMAND ----------

# 04 — External Location al contenedor Raw. Depende de que raw_sc (paso 03) exista.
run_sql_file("04_external_location.sql")

# COMMAND ----------

dbutils.notebook.exit(catalog)
