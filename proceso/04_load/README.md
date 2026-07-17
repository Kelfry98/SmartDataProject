# proceso/04_load

Notebook `.py` de Load (Golden). 100% PySpark DataFrame API, sin Spark SQL.

**Decisión**: un solo notebook, [load_covid_summary_by_country.py](load_covid_summary_by_country.py)
— igual que Transform, porque el objetivo es consolidar `silver.covid_unified` (que ya
tiene ambas fuentes cruzadas) en una sola verdad, no procesar cada fuente por separado.

## Regla de consolidación — por qué WHO primero, historical de respaldo

`silver.covid_unified` trae columnas separadas por fuente (`who_*` / `hist_*`) para el
mismo país+mes. Golden las consolida con `coalesce(who_*, hist_*)`:

- **WHO es la fuente primaria**: es la organización oficial que certifica estos números,
  más consistente en el tiempo (100% diaria desde 2020).
- **historical es el respaldo**: se usa solo cuando WHO no tiene dato para ese país+mes
  (ej. tramos donde historical es mensual pero WHO tiene el dato diario agregado, o países
  que WHO no cubre). También es la **única fuente con `population`** — WHO no la reporta.

## Métricas per-cápita — cuidado con división por cero

`cases_per_million`, `deaths_per_million` y `case_fatality_rate` dividen por `population` o
por `final_cumulative_cases`, que pueden ser `NULL` o `0`. Se calculan con `F.when(...)`
**sin** `.otherwise(...)`: si la condición no se cumple, la columna queda en `NULL` en vez
de tirar error o `Infinity` — el equivalente a un `NULLIF` de SQL hecho con DataFrame API.

## Tabla resultante — `{catalog}.golden.covid_summary_by_country`

| Columna | Cómo se calcula |
|---|---|
| `country_norm`, `year_month` | igual que Silver |
| `data_sources` | heredado de Silver (`WHO` / `HISTORICAL` / `WHO+HISTORICAL`) |
| `final_new_cases`, `final_new_deaths` | `coalesce(who_new_*, hist_new_*)` |
| `final_cumulative_cases`, `final_cumulative_deaths` | `coalesce(who_cumulative_*, hist_total_*)` |
| `population` | `hist_population` (única fuente que la tiene) |
| `cases_per_million`, `deaths_per_million` | `(final_cumulative_* / population) * 1,000,000`, `NULL` si `population` es nulo/cero |
| `case_fatality_rate` | `final_cumulative_deaths / final_cumulative_cases`, `NULL` si el denominador es nulo/cero |

Granularidad: país + `year_month` (igual que Silver) — sirve tanto para tendencia en el
tiempo como para agregar por país completo en el dashboard.

`{catalog}` se resuelve dinámicamente vía el widget `environment`, igual que en
Extract/Transform.
