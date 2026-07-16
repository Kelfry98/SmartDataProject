# worldwide-covid-19-who

Dataset de Kaggle: **Worldwide COVID-19 Data from WHO**
https://www.kaggle.com/datasets/adilshamim8/worldwide-covid-19-data-from-who

Datos globales de COVID-19 recopilados por la Organización Mundial de la Salud (OMS):
casos confirmados, muertes y tendencias por país/región a lo largo del tiempo.

Esta carpeta es solo referencia — el CSV real se descarga manualmente de Kaggle (una sola
vez) y se sube a Azure Blob Storage en:

```
abfss://raw@stdbkprojectsraw.dfs.core.windows.net/worldwide-covid-19-who/
```

El notebook [proceso/02_extract/extract_who_covid.py](../../proceso/02_extract/extract_who_covid.py)
lee de ahí vía Managed Identity y escribe la tabla Bronze `bronze.who_covid`.

Pendiente:
- [ ] Subir el CSV a la ruta de arriba en Azure
- [ ] Confirmar columnas/schema exacto del dataset
