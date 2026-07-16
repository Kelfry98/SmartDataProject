-- Revierte los recursos COMPARTIDOS entre dev y prod (external location y storage
-- credential creados en PrepAmb/03_storage_credential.py y PrepAmb/04_external_location.sql).
-- DROP STORAGE CREDENTIAL sí es DDL SQL válido (a diferencia del CREATE con Azure Managed
-- Identity, que requiere el SDK).
--
-- ¡Cuidado! Solo ejecutar si se está desmantelando el proyecto por completo — si el
-- otro ambiente (dev o prod) sigue activo, seguirá dependiendo de estos dos objetos.

DROP EXTERNAL LOCATION IF EXISTS raw_ext_loc;
DROP STORAGE CREDENTIAL IF EXISTS raw_sc;
