-- External Location al contenedor Raw, vía el Storage Credential raw_sc (Managed Identity).
-- Depende de que raw_sc (03_storage_credential.py) exista. Compartida entre dev y prod.

CREATE EXTERNAL LOCATION IF NOT EXISTS raw_ext_loc
  URL 'abfss://raw@stdbkprojectsraw.dfs.core.windows.net/'
  WITH (CREDENTIAL raw_sc)
  COMMENT 'Raw layer - COVID-19 datasets (WHO + historical worldwide)';

GRANT READ FILES ON EXTERNAL LOCATION raw_ext_loc TO `account users`;
