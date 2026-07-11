-- =====================================================================
-- Validación de f1_dw en Hue (paso 6.3)
-- Ejecutar bloque por bloque; capturar pantalla de cada resultado
-- como evidencia para el informe.
-- =====================================================================

USE f1_dw;

-- 1. Existencia: deben listarse las 7 tablas
SHOW TABLES;

-- 2. Conteos: deben coincidir con los verificados al escribir /MDL
--    dim_driver 881, dim_constructor 214, dim_circuit 78, dim_status 136,
--    dim_race 503, fact_results 10550, fact_constructor_standings 276
SELECT 'dim_driver' AS t, COUNT(*) AS n FROM dim_driver
UNION ALL SELECT 'dim_constructor', COUNT(*) FROM dim_constructor
UNION ALL SELECT 'dim_circuit', COUNT(*) FROM dim_circuit
UNION ALL SELECT 'dim_status', COUNT(*) FROM dim_status
UNION ALL SELECT 'dim_race', COUNT(*) FROM dim_race
UNION ALL SELECT 'fact_results', COUNT(*) FROM fact_results
UNION ALL SELECT 'fact_constructor_standings', COUNT(*) FROM fact_constructor_standings;

-- 3. Tipos declarados: revisar que coincidan con el diagrama del modelo
DESCRIBE dim_driver;
DESCRIBE dim_constructor;
DESCRIBE dim_circuit;
DESCRIBE dim_status;
DESCRIBE dim_race;
DESCRIBE fact_results;
DESCRIBE fact_constructor_standings;

-- 4. Tipos en lectura: si algún tipo no coincidiera con el Parquet real,
--    estas agregaciones fallarían o darían valores absurdos.
--    Esperado: seasons 2000-2025, fechas dentro de ese rango, coords válidas.
SELECT MIN(season) AS min_season, MAX(season) AS max_season,
       MIN(`date`) AS min_date,   MAX(`date`)  AS max_date
FROM dim_race;

SELECT MIN(latitude) AS min_lat, MAX(latitude) AS max_lat,
       MIN(longitude) AS min_lon, MAX(longitude) AS max_lon
FROM dim_circuit;

SELECT SUM(points) AS total_points, MAX(laps) AS max_laps FROM fact_results;

-- 5. Integridad referencial: todas deben dar 0 huérfanos
SELECT COUNT(*) AS orfanos_driver
FROM fact_results f LEFT JOIN dim_driver d ON f.driverId = d.driverId
WHERE d.driverId IS NULL;

SELECT COUNT(*) AS orfanos_constructor
FROM fact_results f LEFT JOIN dim_constructor c ON f.constructorId = c.constructorId
WHERE c.constructorId IS NULL;

SELECT COUNT(*) AS orfanos_race
FROM fact_results f LEFT JOIN dim_race r ON f.raceId = r.raceId
WHERE r.raceId IS NULL;

SELECT COUNT(*) AS orfanos_status
FROM fact_results f LEFT JOIN dim_status s ON f.statusId = s.statusId
WHERE s.statusId IS NULL;

-- statusId derivado por join de texto en el modelado: no debe haber nulos
SELECT COUNT(*) AS status_nulos FROM fact_results WHERE statusId IS NULL;

SELECT COUNT(*) AS orfanos_cs_constructor
FROM fact_constructor_standings f LEFT JOIN dim_constructor c ON f.constructorId = c.constructorId
WHERE c.constructorId IS NULL;

SELECT COUNT(*) AS orfanos_race_circuit
FROM dim_race r LEFT JOIN dim_circuit c ON r.circuitId = c.circuitId
WHERE c.circuitId IS NULL;
