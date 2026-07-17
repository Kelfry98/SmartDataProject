# proceso/03_transform

Notebook `.py` de Transform (Silver). 100% PySpark DataFrame API, sin Spark SQL.

**Decisión**: un solo notebook, [transform_covid_unified.py](transform_covid_unified.py),
en vez de uno por dataset (a diferencia de Extract) — porque el objetivo de esta capa es
**unificar** `bronze.who_covid_daily` y `bronze.covid_historical_series` en una sola tabla
Silver, así que necesita leer ambas fuentes a la vez para cruzarlas.

## Por qué el cruce es por país+mes, no por fecha exacta ni por código ISO

- **Granularidad distinta**: WHO es 100% diaria (2020-2026); historical es mensual antes
  de 2020 y diaria 2020-2024. Cruzar por fecha exacta dejaría nulos masivos en todo el
  tramo mensual de historical.
- **Códigos de país incompatibles**: WHO usa alpha-2 en `Country_code`, historical usa
  alpha-3 en `iso_code` — no son directamente comparables.
- La solución: agregar cada fuente a nivel **país normalizado + year_month** (`yyyy-MM`) y
  cruzarlas por ahí con un `FULL OUTER JOIN`.

## Normalización de país — best-effort, no exhaustiva

El nombre de país se normaliza con `trim` + `upper` + reemplazo de acentos (vía
`F.translate`, sin UDF). Sobre eso se aplica una lista corta de ~7 casos conocidos donde
WHO y historical nombran el mismo país distinto (ej. `RUSSIAN FEDERATION` → `RUSSIA`,
`VIET NAM` → `VIETNAM`). **Esta lista es best-effort, no un diccionario ISO-3166 completo**
— cualquier país fuera de esos ~7 casos que no coincida textualmente entre ambas fuentes
quedará como dos filas separadas tras el `FULL OUTER JOIN` (una con `data_sources = WHO`,
otra con `data_sources = HISTORICAL`) en vez de una sola fila combinada. Aceptable para el
alcance de este proyecto; documentado aquí para que no se lea como un bug.

## Tabla resultante — `{catalog}.silver.covid_unified`

| Columna | Origen |
|---|---|
| `country_norm`, `year_month` | claves del join (`yyyy-MM`) |
| `who_new_cases`, `who_cumulative_cases`, `who_new_deaths`, `who_cumulative_deaths` | agregado de WHO (sum/max) |
| `hist_new_cases`, `hist_total_cases`, `hist_new_deaths`, `hist_total_deaths`, `hist_population` | agregado de historical (sum/max/avg) |
| `data_sources` | `WHO` / `HISTORICAL` / `WHO+HISTORICAL` — de qué fuente(s) viene ese país+mes |

`{catalog}` se resuelve dinámicamente vía el widget `environment`, igual que en Extract.
