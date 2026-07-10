# CLAUDE.md

Contexto de referencia para trabajar en el obligatorio de **Herramientas de Software para Big Data** (dataset F1, API jolpica-f1). Fuentes completas: `CONTEXTO-OBLIGATORIO.md`, `obligatorio.md`, `tipos_datos_columnas.md`, `vista_previa_colecciones.md`.

## Modo de trabajo

- Responder únicamente lo solicitado. No agregar pasos, alternativas ni explicaciones no pedidas.
- Si una tarea implica varios pasos, ejecutarlos de a uno y esperar confirmación antes de continuar. No enumerar todo el plan de antemano salvo que se pida explícitamente.
- Comunicación en español; código, nombres técnicos e identificadores en inglés.
- Ante ambigüedad o regla del curso no documentada aquí, preguntar antes de proceder. No asumir.
- Antes de proponer cambios sobre código o notebooks existentes, pedir o revisar el archivo real primero.
- Tono profesional y directo, sin relleno.

## Infraestructura y stack (obligatorio usar exactamente esto)

VM Azure (Standard_DS2_v3, 2 vCPU, 8 GiB RAM, 32 GB disco), acceso SSH. Recursos limitados.

- **HDFS**: datalake.
- **NiFi**: ingesta (process groups + funnels obligatorio; nada de `put` directo a HDFS).
- **Spark + Jupyter (PySpark)**: EDA, refinamiento, modelado, consultas.
- **Hive** (vía Hue): tablas externas, solo como conector a Superset.
- **Superset**: dashboards.

## Dataset

API **jolpica-f1** (no Kaggle). 8 tablas: `seasons`, `drivers`, `constructors`, `circuits`, `races`, `results`, `status`, `constructor_standings`.

- No es modelo OBT (viene relacional por entidad) → no aplica conversión OBT→normalizado, pero debe constatarse explícitamente en el informe.
- Restricciones de la API: `limit` máx. 100 resultados por llamada, paginación con `offset`, respuestas JSON bajo objeto raíz `MRData`, con rate limits.
- `/LND`: histórico completo 1950–2025, tal como llega de la API, sin recorte.
- `/RFN` en adelante (modelo, Hive, preguntas): recorte 2000–2025 aplicado en el Spark de refinamiento.

Tipos de dato y significado de cada columna: ver `tipos_datos_columnas.md` (fuente de verdad, no reinterpretar). Vista previa/esquema/volumen real por tabla (`/LND`, sin explode): ver `vista_previa_colecciones.md`.

Volumen observado en `/LND` (filas sin `explode`, histórico completo): `seasons` 77, `drivers` 881, `constructors` 214, `status` 136, `circuits` 78, `races` 1171, `results` 1410 (una fila por carrera, cada una con array `Results` anidado), `constructor_standings` 69 (una fila por ronda, con array `ConstructorStandings` anidado). Las estimaciones de ~26.000 filas en `results` y ~6.000 en `constructor_standings` post-`explode` mencionadas en `CONTEXTO-OBLIGATORIO.md` son de un recorte anterior y no están validadas: recalcular el conteo real tras el `explode` en el Spark de refinamiento.

## Zonas HDFS

| Zona | Ruta | Uso |
|---|---|---|
| Landing | `/LND` | JSON crudo, histórico completo, sin transformar. |
| Refinement | `/RFN` | Salida de EDA/Spark, aplanada, recorte 2000–2025, formato Parquet. |
| Modeling | `/MDL` | Tablas del modelo; Hive apunta acá. |
| Analitic | `/ANL` | Resultados de las 2 preguntas para Superset. |

Debe existir un documento escrito de criterios de uso por zona (entregable) y respetarse durante todo el trabajo.

## Decisiones de diseño ya tomadas (no reabrir sin pedir confirmación)

- Ingesta: script Python (`extract_f1_data.py`, entregable) → repo git → NiFi (`InvokeHTTP` → `UpdateAttribute` → `PutHDFS` a `/LND`).
- Recorte temporal aplicado en refinamiento, no en ingesta.
- Claves sintéticas: `raceId` = hash determinístico de `(season, round)`; `resultId` = `sha2(concat_ws("_", season, round, driverId, number), 256)`.
- Modelo: Estrella. Hechos: `fact_results`, `fact_constructor_standings`. Dimensiones: `dim_driver`, `dim_constructor`, `dim_circuit`, `dim_status`, `dim_race`.
- Diagrama del esquema del modelo requerido como entregable (draw.io, Mermaid o Excalidraw).
- Hive: database nuevo (ej. `f1_dw`), tablas externas sobre `/MDL`.
- Visualizaciones en Jupyter (notebook de preguntas): 2 en total — folium (mapa de circuitos por tasa de DNF) y seaborn/matplotlib (heatmap podios o barras top 10).
- Superset: preguntas 3 y 5, resultados en `/ANL`, un dashboard con al menos un chart por pregunta.

## Las 5 preguntas

1. Top 10 pilotos con más victorias (desde 2000). JOIN `results`–`drivers`, filtro posición 1, conteo por piloto.
2. Tasa de DNF por circuito. `results` + `races` + `circuits`; DNF por criterio propio (ver hallazgos), no por `status.count`.
3. Pilotos con más ganancia promedio de posiciones (grid → meta). **Pendiente de confirmar**: el dataset real no tiene `positionOrder` (ver hallazgos); definir si se usa `position` (excluyendo DNF, donde es null) u otro criterio antes de implementar.
4. Combinación piloto–constructor más exitosa en podios. Agrupar `results` por `driverId` + `constructorId`, posiciones 1-3, contar.
5. Escudería con más DNF en últimos 10 años y su impacto en posición final. `results` + `races` para DNFs por año/escudería, JOIN con `constructor_standings` para comparar impacto.

## Reglas de la letra (no negociables)

1. Nada se sube a HDFS por comando: solo vía NiFi.
2. EDA y refinamiento únicamente con Spark (lectura multilínea + `explode` para desanidar).
3. Las 5 preguntas se responden solo contra tablas Hive del modelo (Spark SQL o PySpark). Inválido leer archivos a dataframe directo.
4. Pandas solo para llevar resultados de consultas a visualización.
5. Nombres de zona exactos (LND, RFN, MDL, ANL) + criterios de uso por escrito.
6. Dos notebooks separados: EDA/refinamiento y preguntas+visualizaciones.
7. NiFi con process groups y funnels.

## Hallazgos del EDA a respetar

- `status.count` es acumulado histórico global, no filtrado; no usar para la pregunta de DNF por circuito.
- Criterio DNF: todo status que no sea "Finished" ni "+N Laps" (lista de `statusId` a documentar).
- `results.Results.status` es texto libre (ej. `"Finished"`, `"Accident"`), **no es un `statusId`**: no hay clave foránea numérica directa a `status`. La FK en `fact_results` a `dim_status` requiere resolver el join por coincidencia de texto/descripción, no por igualdad de ID.
- `position` es null en DNF. `positionText` puede tomar valores no numéricos en DNF/descalificación: no usar para aritmética. **No existe columna `positionOrder`** en el dataset real (a diferencia de los CSV clásicos de Ergast) — corregir cualquier referencia previa a `positionOrder` (afecta directamente a la pregunta 3).
- Relevo de pilotos/autos compartidos: fenómeno anterior a 1960, fuera del recorte 2000–2025, pero la clave sintética se genera igual en `/RFN`.
- Conteos post-`explode` de `results` y `constructor_standings` no confirmados aún: recalcular durante el refinamiento (ver Dataset).

## Parte 2 (segunda entrega, stack alternativo)

- Elegir una organización (real o ficticia); si en la Parte 1 se usó una organización real, se puede reutilizar; si no, usar fuentes distintas.
- Listar fuentes de datos y esquemas, definir cómo se integrarían en un nuevo modelo de datos, y qué pregunta de negocio contestaría.
- Investigar un datalake con tecnologías **distintas** a las de la Parte 1 (excepto Spark, que sí puede repetirse): nativas de nube, open source o propietarias. No mezclar herramientas de más de un proveedor cloud.
- Diagramar el nuevo stack y redactar el proceso completo, desde el origen de los datos hasta los consumidores finales.

## Entrega final

- Informe único cubriendo Parte 1 y Parte 2: dominio de los datos (significado y tipo de cada columna), arquitectura del datalake, tecnologías usadas y cómo contribuyen, preguntas planteadas y respondidas, capturas de pantalla o snippets de código como evidencia.
- Adjuntar también: los notebooks de Jupyter, los dashboards de Superset, y todo material que evidencie el cumplimiento de los pasos de la Parte 1.
