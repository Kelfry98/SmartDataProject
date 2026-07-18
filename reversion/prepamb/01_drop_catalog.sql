-- DROP del catalog completo de un ambiente (CASCADE borra schemas y tablas).
-- {catalog} → dev_catalog o prod_catalog.

DROP CATALOG IF EXISTS {catalog} CASCADE;
