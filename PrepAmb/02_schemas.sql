-- Schemas de la medallion architecture dentro del catalog del ambiente.
-- Placeholder {catalog} sustituido por proceso/01_prepamb/prepamb.py

CREATE SCHEMA IF NOT EXISTS {catalog}.bronze
COMMENT 'Capa Bronze — datos extraídos tal cual desde Raw (Extract)';

CREATE SCHEMA IF NOT EXISTS {catalog}.silver
COMMENT 'Capa Silver — datos limpios/transformados (Transform)';

CREATE SCHEMA IF NOT EXISTS {catalog}.golden
COMMENT 'Capa Golden — datos modelados para consumo analítico (Load)';
