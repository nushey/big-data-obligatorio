# Contexto Completo — Obligatorio Big Data (Dataset F1)

> Archivo de contexto para asistentes de IA. Contiene todo lo necesario para trabajar en el obligatorio: curso, infraestructura, dataset, preguntas aprobadas, decisiones tomadas y plan de ejecución.

---

## 1. Curso e infraestructura

- **Materia**: Herramientas de Software para Big Data.
- **Infraestructura**: VM de Azure propia del estudiante, acceso por **SSH**. Todas las herramientas se levantan desde la VM y se accede vía link/URL.
- **Specs de la VM**: Standard_DS2_v3 — 2 vCPU, 8 GiB RAM, 32 GB disco. Recursos limitados: los servicios (Hadoop, NiFi, Hive, Superset) consumen la mayor parte de la RAM.
- **Stack del curso (obligatorio usarlo)**:
  - **HDFS (Hadoop)**: sistema de archivos del datalake, interactúa con NiFi.
  - **NiFi**: ingesta de datos.
  - **Spark + Jupyter (PySpark)**: exploración, limpieza, modelado y consultas.
  - **Hive** (se consulta vía **Hue**): tablas externas sobre HDFS.
  - **Superset**: dashboards.

## 2. Dataset

- **Fuente**: API **jolpica-f1** (open source, sucesora de Ergast F1 API, endpoints backwards-compatible `/ergast/f1/...`). No es Kaggle ✅. No es modelo OBT (viene relacional por entidad) → **no aplica** conversión OBT→normalizado, pero debe constatarse en el informe.
- **Restricciones de la API**: `limit` máx. 100 resultados por llamada, paginación con `offset`, respuestas JSON bajo objeto raíz `MRData`. Tiene rate limits.
- **Tablas a usar (8, cumple mínimo de 4+)**: `seasons`, `drivers`, `constructors`, `circuits`, `races`, `results`, `status`, `constructor_standings`.
- **Temporalidad y volumen**:
  - `/LND`: histórico completo **1950–2025**, tal como llega de la API, sin recorte ni transformación. Volumen estimado: ~26.000+ filas en `results` (guardadas de forma anidada). ⚠️ Cifra de `constructor_standings` (~6.000) sin actualizar — corresponde a la estimación de un recorte anterior 2000–2025; con 75 temporadas debería ser mayor. Recalcular con el conteo real tras el `explode`.
  - `/RFN` en adelante: recorte **2000–2025** aplicado en el Spark de refinamiento. Todo el modelado, Hive y las 5 preguntas trabajan sobre este recorte. Caveat a documentar en el informe: la pregunta 1 (top histórico de victorias) pasa a ser "desde 2000".

## 3. Las 5 preguntas

| # | Pregunta | Enfoque de consulta |
| --- | --- | --- |
| 1 | ¿Cuáles son los 10 pilotos con más victorias (desde 2000)? | JOIN results–drivers, filtro `position = 1`, conteo por piloto |
| 2 | ¿Cuál es la tasa de abandonos (DNF) por circuito? | Proporción de statusId de abandono sobre total de largadas, agrupado por circuito (results + status + races + circuits) |
| 3 | ¿Qué pilotos ganaron más posiciones promedio de largada a meta? | Promedio de `grid − positionOrder` por piloto |
| 4 | ¿Qué combinación piloto–constructor fue la más exitosa en podios? | Agrupar results por driverId + constructorId, posiciones 1-3, contar |
| 5 | ¿Qué escudería tuvo más DNF en los últimos 10 años y cómo influyó en su posición final? | results + status + races para DNFs por año/escudería; JOIN con constructor_standings para comparar |

## 4. Zonas HDFS

| Zona | Ruta | Uso |
| --- | --- | --- |
| Landing | `/LND` | Datos crudos en formato JSON tal como se obtienen de la API. Histórico completo 1950–2025, sin recorte. |
| Refinement | `/RFN` | Salida limpia del EDA en Spark tras aplanar/reestructurar los JSON, **con el recorte 2000–2025 ya aplicado** (formato recomendado: Parquet). |
| Modeling | `/MDL` | Tablas del modelo de datos; aquí apuntan las external tables de Hive. |
| Analitic | `/ANL` | Resultados de las 2 preguntas destinadas a Superset. |

Debe existir un **documento escrito de criterios de uso por zona** (entregable) y respetarse durante todo el trabajo.

## 5. Decisiones de diseño ya tomadas

- **Ingesta (patrón del curso)**: script Python extrae la API paginando y consolida un archivo `.json` por tabla (histórico completo, sin recorte) → se sube a un **repositorio git** → NiFi lo ingiere con **InvokeHTTP** (raw de GitHub) → **UpdateAttribute** (setear `filename`) → **PutHDFS** a `/LND`. Prohibido subir datos a HDFS por comando directo. Usar **process groups** y **funnels** (buenas prácticas exigidas). El script de extracción se entrega como parte del trabajo.

- **Recorte temporal**: se aplica en el Spark de refinamiento (`/LND` → `/RFN`), no en la ingesta. `/LND` queda como copia fiel de la fuente; `/RFN` en adelante (modelo, Hive, preguntas) trabaja sobre 2000–2025.

- **Claves sintéticas (halladas durante el EDA, decisión tomada)**:
  - `races` no trae `raceId` en el JSON crudo de la API. Clave natural: `(season, round)`. Se genera `raceId` sintético determinístico (hash de `season+round`), no `monotonically_increasing_id()` (no reproducible entre corridas).
  - `results` no tiene PK natural única en `(season, round, driverId)`: en temporadas antiguas (particularmente Indianápolis 500 hasta 1960) existía la práctica de relevo de pilotos entre autos, incluso de distinto constructor, y de un mismo auto compartido por dos pilotos con reparto de puntos. Se genera `resultId` sintético con `sha2(concat_ws("_", "season", "round", "driverId", "number"), 256)`. Documentar el hallazgo en el informe como regla de negocio, no como "limpieza de duplicados". Nota: este fenómeno queda fuera del recorte 2000–2025 usado para responder las preguntas, pero la clave sintética se genera igual en `/RFN` sobre datos ya filtrados, por consistencia del modelo.

- **Modelo de datos**: **Estrella (desnormalizado)**.
  - Hechos: `fact_results` (position, positionOrder, grid, points; FKs a driver, constructor, race, status) y `fact_constructor_standings` (para la pregunta 5).
  - Dimensiones: `dim_driver`, `dim_constructor`, `dim_circuit`, `dim_status`, `dim_race` (año, ronda, fecha, FK/desnormalización de circuito — decidir y documentar).
  - Justificación: las 5 preguntas son agregaciones sobre hechos agrupadas por dimensiones.
  - Diagrama del esquema requerido (draw.io, Mermaid o Excalidraw).

- **Hive**: database nuevo (ej. `f1_dw`), tablas **externas** apuntando a `/MDL`. Hive aquí es solo conector a Superset.

- **Visualizaciones en Jupyter**: **2 visualizaciones distintas EN TOTAL** sobre los resultados de 3 preguntas (llevados a pandas con `.toPandas()`), con librerías vistas en clase: **matplotlib, seaborn, bokeh, folium, geopandas (+contextily), networkx**. Plan:
  - Viz 1 (**folium**): mapa mundial de circuitos (la tabla `circuits` trae lat/lng) coloreados/dimensionados por tasa de DNF (pregunta 2).
  - Viz 2 (**seaborn/matplotlib**): heatmap de podios piloto-constructor (pregunta 4) o barras del top 10 de victorias (pregunta 1).

- **Superset**: las 2 preguntas restantes (sugerido: preguntas 3 y 5) → resultados guardados como archivo en `/ANL` → nuevas tablas Hive externas → **un dashboard con al menos un chart por pregunta**.

## 6. Reglas de negocio / hallazgos del EDA (para el informe)

- `status.count` es un acumulado histórico global provisto por la API (sin filtrar a 2000–2025). No usar directamente para la pregunta 2 (tasa de DNF por circuito): recalcular el conteo desde los datos propios ya filtrados en `/RFN`.
- `driverId` puede repetirse dentro de la misma `(season, round)` en registros de auto compartido/relevo (ver clave sintética arriba). Fenómeno concentrado en temporadas anteriores a 1960, fuera del recorte 2000–2025.
- Criterio DNF: todo `status` que no sea "Finished" ni "+N Laps" (a documentar explícitamente con la lista de `statusId` incluidos).
- `position` viene null en DNF; `positionText`/`positionOrder` es la columna confiable para posición final si está disponible tras el aplanado.

## 7. Reglas de la letra

1. Los datos NO se suben a HDFS por comando: solo vía NiFi.
2. EDA y refinamiento **únicamente con Spark** (incluyendo la lectura multilínea del JSON y desanidación/flattening mediante `explode`).
3. Las 5 preguntas se responden **exclusivamente contra tablas Hive** del modelo (Spark SQL o métodos PySpark). Inválido leer archivos a dataframe directo.
4. Pandas solo se usa para llevar **resultados** de consultas a visualización.
5. Zonas HDFS con nombres exactos del curso (LND, RFN, MDL, ANL) + criterios por escrito.
6. Dos notebooks separados: Notebook 1 = EDA/refinamiento; Notebook 2 = preguntas + visualizaciones.
7. NiFi con process groups y funnels.

## 8. Preferencias de trabajo

- Comunicación en español (código y nombres técnicos en inglés).
- No asumir reglas del curso no documentadas aquí: ante ambigüedad, preguntar antes de proceder.
- Antes de proponer código sobre archivos existentes, pedir/ver el código fuente real.