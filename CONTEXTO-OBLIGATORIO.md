# Contexto Completo — Obligatorio Big Data (Dataset F1)

> Archivo de contexto para asistentes de IA. Contiene todo lo necesario para trabajar en el obligatorio: curso, infraestructura, dataset, preguntas aprobadas, decisiones tomadas y plan de ejecución. **Leer completo antes de proponer nada.**

---

## 1. Curso e infraestructura

- **Materia**: Herramientas de Software para Big Data. Trabajo en **equipo de 2**.
- **Infraestructura**: VM de Azure propia del estudiante, acceso por **SSH**. Todas las herramientas se levantan desde la VM y se accede vía link/URL.
- **Specs de la VM**: Standard_DS2_v3 — 2 vCPU, 8 GiB RAM, 32 GB disco. Recursos limitados: los servicios (Hadoop, NiFi, Hive, Superset) consumen la mayor parte de la RAM.
- **Stack del curso (obligatorio usarlo)**:
  - **HDFS (Hadoop)**: sistema de archivos del datalake, interactúa con NiFi.
  - **NiFi**: ingesta de datos.
  - **Spark + Jupyter (PySpark)**: exploración, limpieza, modelado y consultas.
  - **Hive** (se consulta vía **Hue**): tablas externas sobre HDFS.
  - **Superset**: dashboards.

## 2. Dataset (APROBADO por docentes)

- **Fuente**: API **jolpica-f1** (open source, sucesora de Ergast F1 API, endpoints backwards-compatible `/ergast/f1/...`). No es Kaggle ✅. No es modelo OBT (viene relacional por entidad) → **no aplica** conversión OBT→normalizado, pero debe constatarse en el informe.
- **Restricciones de la API**: `limit` máx. 100 resultados por llamada, paginación con `offset`, respuestas JSON bajo objeto raíz `MRData`. Tiene rate limits.
- **Tablas a usar (7, cumple mínimo de 4+)**: `drivers`, `constructors`, `circuits`, `races`, `results`, `status`, `constructor_standings`.
- **`lap_times` NO se usa** (se descartó la pregunta de Monza que la requería).
- **Recorte temporal acordado con el docente** (por limitaciones de la VM): **temporadas 2000–2025**. Volumen estimado: ~11.500 filas en results, ~6.000 en constructor_standings, <10 MB total. Caveat a documentar: la pregunta del top histórico de victorias pasa a ser "desde 2000".

## 3. Las 5 preguntas (APROBADAS)

| # | Pregunta | Enfoque de consulta |
|---|---|---|
| 1 | ¿Cuáles son los 10 pilotos con más victorias (desde 2000)? | JOIN results–drivers, filtro `position = 1`, conteo por piloto |
| 2 | ¿Cuál es la tasa de abandonos (DNF) por circuito? | Proporción de statusId de abandono sobre total de largadas, agrupado por circuito (results + status + races + circuits) |
| 3 | ¿Qué pilotos ganaron más posiciones promedio de largada a meta? | Promedio de `grid − positionOrder` por piloto |
| 4 | ¿Qué combinación piloto–constructor fue la más exitosa en podios? | Agrupar results por driverId + constructorId, posiciones 1-3, contar |
| 5 | ¿Qué escudería tuvo más DNF en los últimos 10 años y cómo influyó en su posición final? | results + status + races para DNFs por año/escudería; JOIN con constructor_standings para comparar |

*(La 6ª pregunta original — evolución de vuelta rápida en Monza — fue descartada.)*

## 4. Zonas HDFS (nomenclatura EXACTA del curso, obligatoria)

| Zona | Ruta | Uso |
|---|---|---|
| Landing | `/LND` | Datos crudos tal como llegan de NiFi (JSON/CSV de la API) |
| Refinement | `/RFN` | Salida limpia del EDA en Spark (formato recomendado: Parquet) |
| Modeling | `/MDL` | Tablas del modelo de datos; aquí apuntan las external tables de Hive |
| Analitic | `/ANL` | Resultados de las 2 preguntas destinadas a Superset |

Debe existir un **documento escrito de criterios de uso por zona** (entregable) y respetarse durante todo el trabajo.

## 5. Decisiones de diseño ya tomadas

- **Ingesta (patrón del curso)**: script Python extrae la API paginando por temporada y consolida un archivo por tabla → se sube a un **repositorio git** → NiFi lo ingiere con **InvokeHTTP** (raw de GitHub) → **UpdateAttribute** (setear `filename`) → **PutHDFS** a `/LND`. Prohibido subir datos a HDFS por comando directo. Usar **process groups** y **funnels** (buenas prácticas exigidas). El script de extracción se entrega como parte del trabajo.
- **Modelo de datos**: **Estrella (desnormalizado)**.
  - Hechos: `fact_results` (position, positionOrder, grid, points; FKs a driver, constructor, race, status) y `fact_constructor_standings` (para la pregunta 5).
  - Dimensiones: `dim_driver`, `dim_constructor`, `dim_circuit`, `dim_status`, `dim_race` (año, ronda, fecha, FK/desnormalización de circuito — decidir y documentar).
  - Justificación: las 5 preguntas son agregaciones sobre hechos agrupadas por dimensiones.
  - Diagrama del esquema requerido (draw.io, Mermaid o Excalidraw).
- **Hive**: database nuevo (ej. `f1_dw`), tablas **externas** apuntando a `/MDL`. Aclaración exigida por la letra para el informe: Hive aquí es solo conector a Superset; no es lo recomendado para producción real.
- **Visualizaciones en Jupyter**: **2 visualizaciones distintas EN TOTAL** sobre los resultados de 3 preguntas (llevados a pandas con `.toPandas()`), con librerías vistas en clase: **matplotlib, seaborn, bokeh, folium, geopandas (+contextily), networkx**. Plan:
  - Viz 1 (**folium**): mapa mundial de circuitos (la tabla `circuits` trae lat/lng) coloreados/dimensionados por tasa de DNF (pregunta 2).
  - Viz 2 (**seaborn/matplotlib**): barras del top 10 de victorias (pregunta 1) o heatmap de podios piloto-constructor (pregunta 4).
- **Superset**: las 2 preguntas restantes (sugerido: preguntas 3 y 5) → resultados guardados como archivo en `/ANL` → nuevas tablas Hive externas → **un dashboard con al menos un chart por pregunta** (para la 5, idealmente comparación DNFs vs posición final).

## 6. Reglas duras de la letra (no violar)

1. Los datos NO se suben a HDFS por comando: solo vía NiFi.
2. EDA y refinamiento **únicamente con Spark** (nada de pandas en esa etapa).
3. Las 5 preguntas se responden **exclusivamente contra tablas Hive** del modelo (Spark SQL o métodos PySpark). Inválido leer archivos a dataframe directo.
4. Pandas solo se usa para llevar **resultados** de consultas a visualización.
5. Zonas HDFS con nombres exactos del curso (LND, RFN, MDL, ANL) + criterios por escrito.
6. Dos notebooks separados: Notebook 1 = EDA/refinamiento; Notebook 2 = preguntas + visualizaciones.
7. NiFi con process groups y funnels.

## 7. Reglas de negocio del dominio (para EDA e informe)

- `\N` de Ergast = null → limpiar.
- `grid = 0` = largada desde pit lane.
- `position` viene null en DNF; **`positionOrder` siempre está poblado** y es la columna confiable para posición final.
- **Criterio DNF**: todo `status` que no sea "Finished" ni "+N Laps" (documentar el criterio elegido).
- Validar unicidad de PKs: `resultId`, `driverId`, `constructorId`, `raceId`, `circuitId`, `statusId`.

## 8. EDA — checklist por tabla (Notebook 1)

Para cada una de las 7 tablas: primeras filas, cantidad de columnas, nombre de cada columna, descripción del significado en el dominio F1, esquema con tipos correctos (`printSchema`), nulos/faltantes y limpieza, duplicados, unicidad de PK. Guardar refinado en `/RFN`.

## 9. Entregables (Parte 1)

- Informe **PDF** (equipo de 2; capturas dentro del PDF o links externos): dominio F1, significado y tipo de **cada columna de cada tabla**, las 5 preguntas planteadas y respondidas, arquitectura del datalake y aporte de cada tecnología, fuente de los datos, criterios de zonas, diagrama del modelo, decisión del recorte 2000–2025.
- Notebook 1 (EDA) y Notebook 2 (preguntas + 2 visualizaciones).
- Dashboard de Superset (capturas/export).
- Evidencias: flujo NiFi (capturas/template), DDLs de Hive, script de extracción de la API, documento de criterios de zonas.

## 10. Parte 2 (teórica, independiente)

Organización real o ficticia con **datos distintos** a la Parte 1. Listar fuentes y esquemas, integración en nuevo modelo de datos, pregunta de negocio. Proponer un datalake con tecnologías **distintas** a las del curso (excepto Spark, que puede repetirse); si se eligen herramientas nativas de una nube, **no mezclar con otra nube**. Explicitar función de cada herramienta, hacer diagrama del stack, y redactar el proceso end-to-end desde el origen hasta los consumidores.

## 11. Orden de ejecución (bloques independientes entre sí, subtareas acopladas)

1. ~~Aprobaciones~~ ✅ (dataset y preguntas aprobadas)
2. Zonas HDFS + documento de criterios
3. Script de extracción de API → repo git → flujo NiFi (InvokeHTTP → UpdateAttribute → PutHDFS) → verificar `/LND`
4. Notebook 1: EDA + refinamiento → `/RFN`
5. Modelo estrella: diagrama + generación de tablas → `/MDL`
6. Hive: database `f1_dw` + tablas externas
7. Notebook 2: las 5 consultas contra Hive
8. 2 visualizaciones (folium + seaborn/matplotlib) sobre 3 preguntas
9. Resultados de 2 preguntas → `/ANL` → tablas Hive → dashboard Superset
10. Informe PDF + empaquetado de entregables
11. Parte 2 (teórica)

## 12. Preferencias de trabajo del estudiante

- Comunicación en español (código y nombres técnicos en inglés está bien).
- No asumir reglas del curso no documentadas aquí: ante ambigüedad, preguntar antes de proceder.
- Antes de proponer código sobre archivos existentes, pedir/ver el código fuente real.
