-- External Location de Unity Catalog apuntando al contenedor Raw en Azure Blob Storage
-- (ADLS Gen2), autenticando vía el Storage Credential "raw_sc" creado en
-- 03_storage_credential.py (Managed Identity — sin DBFS, sin Volumes). Debe correr
-- DESPUÉS de 03_storage_credential.py: depende de que raw_sc ya exista.
--
-- Se crea una sola vez a nivel de metastore (no es específico de dev/prod). Ya creada y
-- validada manualmente en Azure/Databricks — valores fijos, sin placeholders.

CREATE EXTERNAL LOCATION IF NOT EXISTS raw_ext_loc
  URL 'abfss://raw@stdbkprojectsraw.dfs.core.windows.net/'
  WITH (CREDENTIAL raw_sc)
  COMMENT 'Raw layer - COVID-19 datasets (WHO + historical worldwide)';

GRANT READ FILES ON EXTERNAL LOCATION raw_ext_loc TO `account users`;
