# Contexto Completo — Obligatorio Big Data (Dataset F1)

> Archivo de contexto para asistentes de IA. Contiene todo lo necesario para trabajar en el obligatorio: curso, infraestructura, dataset, preguntas aprobadas, decisiones tomadas y plan de ejecución.

---

## 1. Curso e infraestructura

* **Materia**: Herramientas de Software para Big Data.
* **Infraestructura**: VM de Azure propia del estudiante, acceso por **SSH**. Todas las herramientas se levantan desde la VM y se accede vía link/URL.
* **Specs de la VM**: Standard_DS2_v3 — 2 vCPU, 8 GiB RAM, 32 GB disco. Recursos limitados: los servicios (Hadoop, NiFi, Hive, Superset) consumen la mayor parte de la RAM.
* **Stack del curso (obligatorio usarlo)**:
* **HDFS (Hadoop)**: sistema de archivos del datalake, interactúa con NiFi.
* **NiFi**: ingesta de datos.
* **Spark + Jupyter (PySpark)**: exploración, limpieza, modelado y consultas.
* **Hive** (se consulta vía **Hue**): tablas externas sobre HDFS.
* **Superset**: dashboards.



## 2. Dataset

* **Fuente**: API **jolpica-f1** (open source, sucesora de Ergast F1 API, endpoints backwards-compatible `/ergast/f1/...`). No es Kaggle ✅. No es modelo OBT (viene relacional por entidad) → **no aplica** conversión OBT→normalizado, pero debe constatarse en el informe.
* **Restricciones de la API**: `limit` máx. 100 resultados por llamada, paginación con `offset`, respuestas JSON bajo objeto raíz `MRData`. Tiene rate limits.
* **Tablas a usar (8, cumple mínimo de 4+)**: `seasons`, `drivers`, `constructors`, `circuits`, `races`, `results`, `status`, `constructor_standings`.
* **Temporalidad y volumen**: **Histórico completo (1950–2025)**. Volumen estimado: ~26.000+ filas en `results` (guardadas de forma anidada), ~6.000 en `constructor_standings`. Al almacenarse como JSON crudo optimizado sin transformaciones previas, se procesa el histórico completo.

## 3. Las 5 preguntas

| # | Pregunta | Enfoque de consulta |
| --- | --- | --- |
| 1 | ¿Cuáles son los 10 pilotos con más victorias en la historia? | JOIN results–drivers, filtro `position = 1`, conteo por piloto |
| 2 | ¿Cuál es la tasa de abandonos (DNF) por circuito? | Proporción de statusId de abandono sobre total de largadas, agrupado por circuito (results + status + races + circuits) |
| 3 | ¿Qué pilotos ganaron más posiciones promedio de largada a meta? | Promedio de `grid − positionOrder` por piloto |
| 4 | ¿Qué combinación piloto–constructor fue la más exitosa en podios? | Agrupar results por driverId + constructorId, posiciones 1-3, contar |
| 5 | ¿Qué escudería tuvo más DNF en los últimos 10 años y cómo influyó en su posición final? | results + status + races para DNFs por año/escudería; JOIN con constructor_standings para comparar |

## 4. Zonas HDFS

| Zona | Ruta | Uso |
| --- | --- | --- |
| Landing | `/LND` | Datos crudos en formato JSON tal como se obtienen de la API |
| Refinement | `/RFN` | Salida limpia del EDA en Spark tras aplanar/reestructurar los JSON (formato recomendado: Parquet) |
| Modeling | `/MDL` | Tablas del modelo de datos; aquí apuntan las external tables de Hive |
| Analitic | `/ANL` | Resultados de las 2 preguntas destinadas a Superset |

Debe existir un **documento escrito de criterios de uso por zona** (entregable) y respetarse durante todo el trabajo.

## 5. Decisiones de diseño ya tomadas

* **Ingesta (patrón del curso)**: script Python extrae la API paginando y consolida un archivo `.json` por tabla → se sube a un **repositorio git** → NiFi lo ingiere con **InvokeHTTP** (raw de GitHub) → **UpdateAttribute** (setear `filename`) → **PutHDFS** a `/LND`. Prohibido subir datos a HDFS por comando directo. Usar **process groups** y **funnels** (buenas prácticas exigidas). El script de extracción se entrega como parte del trabajo.
* **Modelo de datos**: **Estrella (desnormalizado)**.
* Hechos: `fact_results` (position, positionOrder, grid, points; FKs a driver, constructor, race, status) y `fact_constructor_standings` (para la pregunta 5).
* Dimensiones: `dim_driver`, `dim_constructor`, `dim_circuit`, `dim_status`, `dim_race` (año, ronda, fecha, FK/desnormalización de circuito — decidir y documentar).
* Justificación: las 5 preguntas son agregaciones sobre hechos agrupadas por dimensiones.
* Diagrama del esquema requerido (draw.io, Mermaid o Excalidraw).


* **Hive**: database nuevo (ej. `f1_dw`), tablas **externas** apuntando a `/MDL`. Hive aquí es solo conector a Superset
* **Visualizaciones en Jupyter**: **2 visualizaciones distintas EN TOTAL** sobre los resultados de 3 preguntas (llevados a pandas con `.toPandas()`), con librerías vistas en clase: **matplotlib, seaborn, bokeh, folium, geopandas (+contextily), networkx**. Plan:
* Viz 1 (**folium**): mapa mundial de circuitos (la tabla `circuits` trae lat/lng) coloreados/dimensionados por tasa de DNF (pregunta 2).
* Viz 2 (**seaborn/matplotlib**): heatmap de podios piloto-constructor (pregunta 4) o barras del top 10 de victorias (pregunta 1).


* **Superset**: las 2 preguntas restantes (sugerido: preguntas 3 y 5) → resultados guardados como archivo en `/ANL` → nuevas tablas Hive externas → **un dashboard con al menos un chart por pregunta**

## 6. Reglas de la letra

1. Los datos NO se suben a HDFS por comando: solo vía NiFi.
2. EDA y refinamiento **únicamente con Spark** (incluyendo la lectura multilínea del JSON y desanidación/flattening mediante `explode`).
3. Las 5 preguntas se responden **exclusivamente contra tablas Hive** del modelo (Spark SQL o métodos PySpark). Inválido leer archivos a dataframe directo.
4. Pandas solo se usa para llevar **resultados** de consultas a visualización.
5. Zonas HDFS con nombres exactos del curso (LND, RFN, MDL, ANL) + criterios por escrito.
6. Dos notebooks separados: Notebook 1 = EDA/refinamiento; Notebook 2 = preguntas + visualizaciones.
7. NiFi con process groups y funnels.

## 7. Preferencias de trabajo

* Comunicación en español (código y nombres técnicos en inglés).
* No asumir reglas del curso no documentadas aquí: ante ambigüedad, preguntar antes de proceder.
* Antes de proponer código sobre archivos existentes, pedir/ver el código fuente real.