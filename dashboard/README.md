# dashboard/

Dashboard final (Databricks Lakeview / AI-BI) construido sobre la tabla Golden en Unity
Catalog. Fuente única: `{catalog}.golden.covid_summary_by_country`.

## Archivo

- [`COVID-19 Global Summary.lvdash.json`](COVID-19%20Global%20Summary.lvdash.json) —
  definición del dashboard (datasets + layout de widgets). Es el export de Lakeview,
  versionado en el repo.

## Parametrización por ambiente (dev / prod)

El dashboard **no** tiene el catalog hardcodeado: las 7 queries usan la función
`IDENTIFIER()` de Databricks SQL con un parámetro de dashboard `catalog`:

```sql
SELECT ... FROM IDENTIFIER(:catalog || '.golden.covid_summary_by_country')
```

Los 7 datasets declaran el mismo parámetro (`keyword: "catalog"`), así que Lakeview los
une en **un único control** a nivel de dashboard. El valor por defecto es `dev_catalog`;
para ver los datos de producción se cambia ese parámetro a `prod_catalog` — el mismo JSON
sirve para los dos ambientes, sin editar nada.

> Validado en vivo contra el SQL warehouse de `adbk-dev`: con `catalog=dev_catalog` la
> query resuelve la tabla Golden (25.985 filas); con un catalog inexistente falla con
> `TABLE_OR_VIEW_NOT_FOUND`, confirmando que el parámetro gobierna el `FROM`.

Los dashboards Lakeview **no** se despliegan vía el pipeline de `deploy.yml` (ese solo corre
los notebooks de `proceso/`). Este JSON se importa a mano en el workspace (o vía la Lakeview
API); el parámetro `catalog` es lo que lo hace portable entre `adbk-dev` y `adbk-prod`.

## Widgets

| Widget | Tipo | Métrica |
|---|---|---|
| Casos Acumulados | KPI | `SUM(final_new_cases)` |
| Total Deaths | KPI | `SUM(final_new_deaths)` |
| Avg Case Fatality Rate | KPI | `AVG(case_fatality_rate)` |
| Cumulative Cases by Year & Country | Línea | `MAX(final_cumulative_cases)` por año/país |
| Top 10 Países por Cases per Million | Barras | `cases_per_million` (último mes) |
| Top 10 Países por Deaths per Million | Barras | `deaths_per_million` (2024) |
| Muertes X Países | Mapa coroplético | `deaths_per_million` por país |

## Caveat de nombres de país (mapa)

El mapa usa `INITCAP(LOWER(country_norm))` para matchear nombres `admin0-name-en`. Como
`country_norm` viene normalizado (mayúsculas + tabla de overrides del Transform, ej.
`IVORY COAST`, `RUSSIA`), algunos países pueden no coincidir con el mapa base y quedar sin
pintar. Es el mismo caveat de normalización de país documentado en
[proceso/03_transform/README.md](../proceso/03_transform/README.md); no afecta al resto de
los widgets.
