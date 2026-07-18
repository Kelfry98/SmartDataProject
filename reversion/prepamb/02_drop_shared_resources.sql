-- DROP del external location y storage credential COMPARTIDOS entre dev y prod.
-- Solo ejecutar si se desmantela el proyecto por completo (el otro ambiente depende de ellos).

DROP EXTERNAL LOCATION IF EXISTS raw_ext_loc;
DROP STORAGE CREDENTIAL IF EXISTS raw_sc;
