# who-covid-daily

Kaggle: **Worldwide COVID-19 Data from WHO**
https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who

Datos diarios de COVID-19 reportados por la OMS: casos y muertes nuevas/acumuladas por país.

Ruta en Raw:

```
abfss://raw@stdbkprojectsraw.dfs.core.windows.net/who-covid-daily/WHO-COVID-19-global-daily-data.csv
```

## Schema

| Columna | Descripción |
|---|---|
| `Date_reported` | Fecha del reporte |
| `Country_code` | Código ISO del país |
| `Country` | Nombre del país |
| `WHO_region` | Región OMS |
| `New_cases` | Casos nuevos |
| `Cumulative_cases` | Casos acumulados |
| `New_deaths` | Muertes nuevas |
| `Cumulative_deaths` | Muertes acumuladas |

Lo lee [proceso/02_extract/extract_who_covid_daily.py](../../proceso/02_extract/extract_who_covid_daily.py)
→ tabla Bronze `{catalog}.bronze.who_covid_daily`.
