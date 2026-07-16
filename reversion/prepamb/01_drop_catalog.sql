-- Revierte lo creado por PrepAmb/01_catalog.sql y PrepAmb/02_schemas.sql para UN
-- ambiente. CASCADE porque borra el catalog completo, incluyendo bronze/silver/golden
-- y todas sus tablas: úsalo solo para desmantelar un ambiente por completo.
--
-- Placeholder {catalog} — reemplazar por dev_catalog o prod_catalog según corresponda.

DROP CATALOG IF EXISTS {catalog} CASCADE;
