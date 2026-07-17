-- USE CATALOG sobre el catalog del ambiente. Sin esto, el principal no puede ni "entrar"
-- al catalog para llegar a bronze/silver/golden, aunque tenga SELECT en las tablas (los
-- permisos de Unity Catalog son jerárquicos: catalog -> schema -> tabla).
--
-- Principal: `account users` (todos los usuarios del account de Databricks) — mismo
-- principal usado en PrepAmb/04_external_location.sql (GRANT READ FILES ... TO
-- `account users`), para mantener el mismo criterio de acceso en todo el proyecto.
--
-- Placeholder {catalog} sustituido por proceso/05_grants/grants.py.

GRANT USE CATALOG ON CATALOG {catalog} TO `account users`;
