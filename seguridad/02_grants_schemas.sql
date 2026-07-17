-- USE SCHEMA sobre bronze, silver y golden del ambiente. Igual que USE CATALOG, es
-- jerárquico: sin USE SCHEMA en el schema correspondiente, SELECT en una tabla de ese
-- schema no alcanza para consultarla.
--
-- Placeholder {catalog} sustituido por proceso/05_grants/grants.py.

GRANT USE SCHEMA ON SCHEMA {catalog}.bronze TO `account users`;
GRANT USE SCHEMA ON SCHEMA {catalog}.silver TO `account users`;
GRANT USE SCHEMA ON SCHEMA {catalog}.golden TO `account users`;
