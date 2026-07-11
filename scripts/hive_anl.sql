-- =====================================================================
-- Tablas externas de la zona /ANL (resultados de analíticas para Superset)
-- Preguntas 3 y 5. Mismo criterio que hive_f1_dw.sql: tablas EXTERNAS,
-- STORED AS PARQUET, tipos espejando el esquema escrito por Spark.
-- Ejecutar en Hue. Requiere que los resultados ya esten escritos en /ANL.
-- Las rutas relativas ort/ANL/... resuelven en /user/ort/ort/ANL/...
-- (mismo esquema de LOCATION que funciono para /MDL).
-- =====================================================================

USE f1_dw;

-- ---------------------------------------------------------------------
-- Pregunta 3: pilotos con mas ganancia promedio de posiciones (top 10)
-- Escrita por Spark en ort/ANL/pregunta3.
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS anl_pregunta3;
CREATE EXTERNAL TABLE anl_pregunta3 (
  nombre            STRING,
  apellido          STRING,
  carreras_validas  BIGINT,
  ganancia_promedio DOUBLE,
  pos               INT,
  piloto            STRING
)
STORED AS PARQUET
LOCATION '/user/ort/ort/ANL/pregunta3';

-- ---------------------------------------------------------------------
-- Pregunta 5: escuderia con mas DNF (2016-2025) e impacto en posicion.
-- Escrita por Spark en ort/ANL/pregunta5.
-- NOTA: confirmar nombres/orden/tipos de columnas contra el printSchema()
-- del DataFrame que escribe el companiero antes de correr esto.
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS anl_pregunta5;
CREATE EXTERNAL TABLE anl_pregunta5 (
  constructor        STRING,
  dnf_count          BIGINT,
  starts             BIGINT,
  dnf_rate_pct       DOUBLE,
  seasons            BIGINT,
  avg_final_position DOUBLE
)
STORED AS PARQUET
LOCATION '/user/ort/ort/ANL/pregunta5';

-- =====================================================================
-- Verificacion rapida
-- =====================================================================
-- SELECT * FROM anl_pregunta3 ORDER BY pos;
-- SELECT * FROM anl_pregunta5 ORDER BY dnf_count DESC;
