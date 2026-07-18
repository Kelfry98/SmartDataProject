-- Schemas de la medallion architecture. {catalog} sustituido por prepamb.py.

CREATE SCHEMA IF NOT EXISTS {catalog}.bronze
COMMENT 'Capa Bronze — datos extraídos tal cual desde Raw (Extract)';

CREATE SCHEMA IF NOT EXISTS {catalog}.silver
COMMENT 'Capa Silver — datos limpios/transformados (Transform)';

CREATE SCHEMA IF NOT EXISTS {catalog}.golden
COMMENT 'Capa Golden — datos modelados para consumo analítico (Load)';
