-- =====================================================================
-- f1_dw — Modelo estrella F1 (jolpica)
-- Tablas EXTERNAS sobre la zona /MDL de HDFS (Parquet).
-- Hive se usa únicamente como conector para Superset.
-- Ejecutar en Hue. Requiere /MDL ya escrito por modelado.ipynb.
-- Rutas confirmadas con `hdfs dfs -ls ort/MDL` (home HDFS = /user/ort).
-- =====================================================================

CREATE DATABASE IF NOT EXISTS f1_dw
  COMMENT 'Modelo estrella F1 (jolpica) - tablas externas sobre /MDL';

USE f1_dw;

-- =====================================================================
-- DIMENSIONES
-- =====================================================================

DROP TABLE IF EXISTS dim_driver;
CREATE EXTERNAL TABLE dim_driver (
  driverId        STRING,
  code            STRING,
  familyName      STRING,
  givenName       STRING,
  permanentNumber STRING,
  dateOfBirth     DATE,
  nationality     STRING
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/dim_driver';

DROP TABLE IF EXISTS dim_constructor;
CREATE EXTERNAL TABLE dim_constructor (
  constructorId STRING,
  name          STRING,
  nationality   STRING
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/dim_constructor';

DROP TABLE IF EXISTS dim_circuit;
CREATE EXTERNAL TABLE dim_circuit (
  circuitId   STRING,
  circuitName STRING,
  country     STRING,
  locality    STRING,
  latitude    DOUBLE,
  longitude   DOUBLE
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/dim_circuit';

DROP TABLE IF EXISTS dim_status;
CREATE EXTERNAL TABLE dim_status (
  statusId INT,
  status   STRING
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/dim_status';

DROP TABLE IF EXISTS dim_race;
CREATE EXTERNAL TABLE dim_race (
  raceId    STRING,
  season    INT,
  round     INT,
  raceName  STRING,
  `date`    DATE,
  circuitId STRING
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/dim_race';

-- =====================================================================
-- HECHOS
-- =====================================================================

DROP TABLE IF EXISTS fact_results;
CREATE EXTERNAL TABLE fact_results (
  resultId      STRING,
  raceId        STRING,
  driverId      STRING,
  constructorId STRING,
  statusId      INT,
  grid          INT,
  position      INT,
  positionText  STRING,
  points        DOUBLE,
  laps          INT
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/fact_results';

DROP TABLE IF EXISTS fact_constructor_standings;
CREATE EXTERNAL TABLE fact_constructor_standings (
  standingId    STRING,
  constructorId STRING,
  season        INT,
  totalRounds   INT,
  points        DOUBLE,
  position      INT,
  positionText  STRING,
  wins          INT
)
STORED AS PARQUET
LOCATION '/user/ort/ort/MDL/fact_constructor_standings';

-- =====================================================================
-- Verificación de conteos (esperado):
--   dim_driver 881, dim_constructor 214, dim_circuit 78, dim_status 136,
--   dim_race 503, fact_results 10550, fact_constructor_standings 276
-- =====================================================================
-- USE f1_dw;
-- SELECT 'dim_driver' AS t, COUNT(*) AS n FROM dim_driver
-- UNION ALL SELECT 'dim_constructor', COUNT(*) FROM dim_constructor
-- UNION ALL SELECT 'dim_circuit', COUNT(*) FROM dim_circuit
-- UNION ALL SELECT 'dim_status', COUNT(*) FROM dim_status
-- UNION ALL SELECT 'dim_race', COUNT(*) FROM dim_race
-- UNION ALL SELECT 'fact_results', COUNT(*) FROM fact_results
-- UNION ALL SELECT 'fact_constructor_standings', COUNT(*) FROM fact_constructor_standings;
