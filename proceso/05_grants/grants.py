# Databricks notebook source
# Grants — último paso del pipeline: da permisos sobre lo que se acaba de construir para
# que otros usuarios/servicios (ej. el dashboard de Lakeview) puedan consultar los datos.
#
# Usa spark.sql() para los GRANT, igual que PrepAmb/01_catalog.sql, 02_schemas.sql y
# 04_external_location.sql: GRANT es DDL de Unity Catalog sin equivalente en el DataFrame
# API — misma excepción documentada ahí. Lee y aplica los .sql de seguridad/ (fuente de
# verdad de permisos) en vez de tener los GRANT hardcodeados en este notebook.

import os

dbutils.widgets.text("environment", "dev", "Ambiente (dev|prod)")
environment = dbutils.widgets.get("environment")
catalog = f"{environment}_catalog"

# En Databricks Repos este notebook vive en proceso/05_grants/, seguridad/ es hermano de
# proceso/ en la raíz del repo. __file__ no está definido corriendo interactivo (Run all
# en el notebook) — solo es confiable en Jobs. Se resuelve vía el contexto del notebook.
NOTEBOOK_DIR = "/Workspace" + os.path.dirname(
    dbutils.notebook.entry_point.getDbutils().notebook().getContext().notebookPath().get()
)
SEGURIDAD_DIR = os.path.normpath(os.path.join(NOTEBOOK_DIR, "..", "..", "seguridad"))


def run_sql_file(filename: str, **params: str) -> None:
    path = os.path.join(SEGURIDAD_DIR, filename)
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
