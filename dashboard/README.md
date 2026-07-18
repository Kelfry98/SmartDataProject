# dashboard/

Dashboard final (Databricks Lakeview / AI-BI) sobre la tabla Golden en Unity Catalog.
Fuente única: `{catalog}.golden.covid_summary_by_country`.

## Archivo

- [`COVID-19 Global Summary.lvdash.json`](COVID-19%20Global%20Summary.lvdash.json) —
  definición del dashboard (datasets + layout de widgets), export de Lakeview.

## Parametrización por ambiente (dev / prod)

El catalog no está hardcodeado: las 7 queries usan `IDENTIFIER()` de Databricks SQL con un
parámetro de dashboard `catalog`:

```sql
SELECT ... FROM IDENTIFIER(:catalog || '.golden.covid_summary_by_country')
```

Los 7 datasets declaran el mismo parámetro (`keyword: "catalog"`), así que Lakeview los une
en un único control. Por defecto `dev_catalog`; para prod se cambia a `prod_catalog`. El
mismo JSON sirve para los dos ambientes.

Los dashboards Lakeview no se despliegan vía `deploy.yml` (ese solo corre `proceso/`); este
JSON se importa a mano en el workspace o vía la Lakeview API.

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

El mapa matchea `INITCAP(LOWER(country_norm))` contra nombres `admin0-name-en`; algunos
países normalizados pueden no coincidir con el mapa base y quedar sin pintar.
