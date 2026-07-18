-- Catalog del ambiente (dev_catalog / prod_catalog). {catalog} sustituido por prepamb.py.

CREATE CATALOG IF NOT EXISTS {catalog}
  MANAGED LOCATION 'abfss://raw@stdbkprojectsraw.dfs.core.windows.net/catalog-{catalog}/';