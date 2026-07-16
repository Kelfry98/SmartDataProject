# coronavirus-covid-19-worldwide-2018-2026

Dataset de Kaggle: **Coronavirus (COVID-19) Worldwide Data (2018-2026)**
https://www.kaggle.com/datasets/zkskhurram/coronavirus-covid-19-worldwide-data2018-2026

Datos epidemiológicos globales del COVID-19 con cobertura temporal 2018–2026.

Esta carpeta es solo referencia — el CSV real se descarga manualmente de Kaggle (una sola
vez) y se sube a Azure Blob Storage en:

```
abfss://raw@stdbkprojectsraw.dfs.core.windows.net/coronavirus-covid-19-worldwide-2018-2026/
```

El notebook [proceso/02_extract/extract_covid_worldwide.py](../../proceso/02_extract/extract_covid_worldwide.py)
lee de ahí vía Managed Identity y escribe la tabla Bronze `bronze.covid_worldwide`.

Pendiente:
- [ ] Subir el CSV a la ruta de arriba en Azure
- [ ] Confirmar columnas/schema exacto del dataset
