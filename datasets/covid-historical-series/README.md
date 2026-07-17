# covid-historical-series

Dataset de Kaggle: **Coronavirus (COVID-19) Worldwide Data (2018-2026)**
https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026

Serie histórica global del COVID-19 (estilo Our World in Data): casos, muertes, tests,
hospitalización, vacunación y contexto demográfico por país/día.

Esta carpeta es solo referencia — el CSV real se descarga manualmente de Kaggle (una sola
vez) y ya está subido a Azure Blob Storage en:

```
abfss://raw@stdbkprojectsraw.dfs.core.windows.net/covid-historical-series/covid_historical_time_series.csv
```

## Schema real

| Columna | Descripción |
|---|---|
| `iso_code` | Código ISO del país |
| `continent` | Continente |
| `location` | País/región |
| `date` | Fecha |
| `total_cases` | Casos totales |
| `new_cases` | Casos nuevos |
| `total_deaths` | Muertes totales |
| `new_deaths` | Muertes nuevas |
| `total_tests` | Tests totales |
| `new_tests` | Tests nuevos |
| `stringency_index` | Índice de restricciones |
| `population` | Población |
| `new_cases_smoothed` | Casos nuevos (promedio móvil) |
| `new_deaths_smoothed` | Muertes nuevas (promedio móvil) |
| `reproduction_rate` | Tasa de reproducción (R) |
| `icu_patients` | Pacientes en UCI |
| `hosp_patients` | Pacientes hospitalizados |
| `positive_rate` | Tasa de positividad |
| `tests_per_case` | Tests por caso confirmado |

El notebook [proceso/02_extract/extract_covid_historical_series.py](../../proceso/02_extract/extract_covid_historical_series.py)
lee de ahí vía Managed Identity y escribe la tabla Bronze `{catalog}.bronze.covid_historical_series`,
tal cual, sin transformar.
