# reversion/

Scripts de reversión (rollback) para deshacer lo creado por el pipeline: DROP de tablas,
schemas y objetos de Unity Catalog. Sirven para dejar el ambiente limpio o revertir un
despliegue fallido.

Organizado por capa, en orden inverso de dependencia (Golden → Silver → Bronze → PrepAmb):

- [golden/](golden/) — DROP de tablas Golden
- [silver/](silver/) — DROP de tablas Silver
- [bronze/](bronze/) — DROP de tablas Bronze
- [prepamb/](prepamb/) — DROP de catalog/schemas (por ambiente) y de external
  location/storage credential (compartidos)

Cada script debe ser idempotente (`DROP ... IF EXISTS`). Los DROP de catalog/schema/
external location están en [prepamb/](prepamb/) en vez de mezclarse con los de tablas,
porque son objetos administrativos con distinto alcance (por ambiente vs. compartidos).

Pendiente: escribir los `.py`/`.sql` de reversión junto con cada tabla creada en [proceso/](../proceso/).
