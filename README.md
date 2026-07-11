# Obligatorio — Herramientas de Software para Big Data

Datalake de datos históricos de Fórmula 1 (API [jolpica-f1](https://github.com/jolpica/jolpica-f1)), construido sobre el stack del curso: NiFi → HDFS (zonas LND/RFN/MDL/ANL) → Spark → Hive → Superset. Se responden 5 preguntas de negocio contra un modelo estrella. Incluye además el diseño de un stack alternativo en AWS (Parte 2).

**Autores:** Franco Pérez, Nahuel Zeballos — Universidad ORT.

## Estructura

| Carpeta / archivo | Contenido |
| --- | --- |
| `datos/` | JSON crudos extraídos de la API (fuente de la ingesta vía NiFi). |
| `scripts/` | Script de extracción (`script_extraccion.py`) y SQL de Hive (creación, validación y tablas ANL). |
| `notebooks/` | Notebooks PySpark por etapa: `RFN/` (EDA y refinamiento), `MDL/` (modelado), `PREGUNTAS/` (respuestas), `ANL/` (resultados para Superset), `VISUALIZACIONES/`. |
| `reportes/` | Documentación de soporte: tipos de dato por columna, vistas previas, nulos/PKs y doc de refinamiento. |
| `capturas/` | Evidencia por herramienta (NiFi, Spark, Hive, Superset, preguntas, diagramas). |
| `obligatorio.md` | Letra del obligatorio. |
