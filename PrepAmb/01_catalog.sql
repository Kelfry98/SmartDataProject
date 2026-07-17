-- Catalog de Unity Catalog para el ambiente actual (dev_catalog / prod_catalog).
-- Placeholder {catalog} sustituido por proceso/01_prepamb/prepamb.py según el
-- parámetro `environment` (dev|prod) recibido del job de CI/CD.

CREATE CATALOG IF NOT EXISTS {catalog}
  MANAGED LOCATION 'abfss://raw@stdbkprojectsraw.dfs.core.windows.net/catalog-{catalog}/';