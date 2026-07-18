# Databricks notebook source
# Grants — último paso del pipeline: aplica los GRANT de seguridad/ sobre catalog, schemas y tablas.

import os

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
environment = dbutils.widgets.get("environment")
catalog = f"{environment}_catalog"

# Ruta a seguridad/, carpeta hermana de proceso/ en la raíz del repo.
NOTEBOOK_DIR = "/Workspace" + os.path.dirname(
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
)
SEGURIDAD_DIR = os.path.normpath(os.path.join(NOTEBOOK_DIR, "..", "..", "seguridad"))


def run_sql_file(filename: str, **params: str) -> None:
    path = os.path.join(SEGURIDAD_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        # Descarta líneas de comentario antes de separar por ";".
        lines = [line for line in f if not line.strip().startswith("--")]
    sql = "".join(lines).format(**params)
    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            spark.sql(statement)


# COMMAND ----------

# 01 — USE CATALOG sobre el catalog del ambiente actual
run_sql_file("01_grants_catalog.sql", catalog=catalog)

# COMMAND ----------

# 02 — USE SCHEMA sobre bronze/silver/golden del ambiente actual
run_sql_file("02_grants_schemas.sql", catalog=catalog)

# COMMAND ----------

# 03 — SELECT sobre las tablas finales de cada capa (bronze x2, silver, golden)
run_sql_file("03_grants_tablas.sql", catalog=catalog)

# COMMAND ----------

dbutils.notebook.exit(catalog)
