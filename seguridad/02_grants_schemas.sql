-- USE SCHEMA sobre bronze, silver y golden, para `account users`.
-- {catalog} sustituido por grants.py.

GRANT USE SCHEMA ON SCHEMA {catalog}.bronze TO `account users`;
GRANT USE SCHEMA ON SCHEMA {catalog}.silver TO `account users`;
GRANT USE SCHEMA ON SCHEMA {catalog}.golden TO `account users`;
