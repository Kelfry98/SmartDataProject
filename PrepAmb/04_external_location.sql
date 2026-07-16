-- External Location de Unity Catalog apuntando al contenedor Raw en Azure Blob Storage
-- (ADLS Gen2), autenticando vía el Storage Credential "raw_sc" creado en
-- 03_storage_credential.py (Managed Identity — sin DBFS, sin Volumes). Debe correr
-- DESPUÉS de 03_storage_credential.py: depende de que raw_sc ya exista.
--
-- Se crea una sola vez a nivel de metastore (no es específico de dev/prod).
-- Placeholders {storage_account} y {container_name} sustituidos por
-- proceso/01_prepamb/prepamb.py.

CREATE EXTERNAL LOCATION IF NOT EXISTS raw_ext_loc
URL 'abfss://{container_name}@{storage_account}.dfs.core.windows.net/'
WITH (STORAGE_CREDENTIAL raw_sc)
COMMENT 'Contenedor Raw — fuente de los datasets para la capa Bronze';
