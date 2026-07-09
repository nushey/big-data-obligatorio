# Seasons
```txt
===== Tabla: seasons (LND) =====
Filas: 77   |   Columnas: 2
Nombres de columnas: ['season', 'url']

Esquema:
root
 |-- season: string (nullable = true)
 |-- url: string (nullable = true)

Primeras filas:
+------+-----------------------------------------------------+
|season|url                                                  |
+------+-----------------------------------------------------+
|1950  |https://en.wikipedia.org/wiki/1950_Formula_One_season|
|1951  |https://en.wikipedia.org/wiki/1951_Formula_One_season|
|1952  |https://en.wikipedia.org/wiki/1952_Formula_One_season|
|1953  |https://en.wikipedia.org/wiki/1953_Formula_One_season|
|1954  |https://en.wikipedia.org/wiki/1954_Formula_One_season|
+------+-----------------------------------------------------+
only showing top 5 rows
```

# Drivers
```txt
===== Tabla: drivers (LND) =====
Filas: 881   |   Columnas: 8
Nombres de columnas: ['code', 'dateOfBirth', 'driverId', 'familyName', 'givenName', 'nationality', 'permanentNumber', 'url']

Esquema:
root
 |-- code: string (nullable = true)
 |-- dateOfBirth: string (nullable = true)
 |-- driverId: string (nullable = true)
 |-- familyName: string (nullable = true)
 |-- givenName: string (nullable = true)
 |-- nationality: string (nullable = true)
 |-- permanentNumber: string (nullable = true)
 |-- url: string (nullable = true)

Primeras filas:
+----+-----------+---------+----------+---------+-----------+---------------+----------------------------------------------+
|code|dateOfBirth|driverId |familyName|givenName|nationality|permanentNumber|url                                           |
+----+-----------+---------+----------+---------+-----------+---------------+----------------------------------------------+
|null|1932-07-10 |abate    |Abate     |Carlo    |Italian    |null           |http://en.wikipedia.org/wiki/Carlo_Mario_Abate|
|null|1913-03-21 |abecassis|Abecassis |George   |British    |null           |http://en.wikipedia.org/wiki/George_Abecassis |
|null|1957-11-27 |acheson  |Acheson   |Kenny    |British    |null           |http://en.wikipedia.org/wiki/Kenny_Acheson    |
|null|1969-11-19 |adams    |Adams     |Philippe |Belgian    |null           |http://en.wikipedia.org/wiki/Philippe_Adams   |
|null|1913-12-15 |ader     |Ader      |Walt     |American   |null           |http://en.wikipedia.org/wiki/Walt_Ader        |
+----+-----------+---------+----------+---------+-----------+---------------+----------------------------------------------+
only showing top 5 rows
```

# Constructors
```txt
===== Tabla: constructors (LND) =====
Filas: 214   |   Columnas: 4
Nombres de columnas: ['constructorId', 'name', 'nationality', 'url']

Esquema:
root
 |-- constructorId: string (nullable = true)
 |-- name: string (nullable = true)
 |-- nationality: string (nullable = true)
 |-- url: string (nullable = true)

Primeras filas:
+-------------+----------+-----------+------------------------------------------------------------------+
|constructorId|name      |nationality|url                                                               |
+-------------+----------+-----------+------------------------------------------------------------------+
|adams        |Adams     |American   |https://en.wikipedia.org/wiki/Adams_(constructor)                 |
|afm          |AFM       |German     |https://en.wikipedia.org/wiki/Alex_von_Falkenhausen_Motorenbau    |
|ags          |AGS       |French     |https://en.wikipedia.org/wiki/Automobiles_Gonfaronnaises_Sportives|
|alfa         |Alfa Romeo|Swiss      |https://en.wikipedia.org/wiki/Alfa_Romeo_in_Formula_One           |
|alphatauri   |AlphaTauri|Italian    |https://en.wikipedia.org/wiki/Scuderia_AlphaTauri                 |
+-------------+----------+-----------+------------------------------------------------------------------+
only showing top 5 rows
```

# Status
```txt
===== Tabla: status (LND) =====
Filas: 136   |   Columnas: 3
Nombres de columnas: ['count', 'status', 'statusId']

Esquema:
root
 |-- count: string (nullable = true)
 |-- status: string (nullable = true)
 |-- statusId: string (nullable = true)

Primeras filas:
+-----+--------+--------+
|count|status  |statusId|
+-----+--------+--------+
|8093 |Finished|1       |
|3850 |+1 Lap  |11      |
|2011 |Engine  |5       |
|1593 |+2 Laps |12      |
|1047 |Accident|3       |
+-----+--------+--------+
only showing top 5 rows
```

# Circuits
```txt
===== Tabla: circuits (LND) =====
Filas: 78   |   Columnas: 4
Nombres de columnas: ['Location', 'circuitId', 'circuitName', 'url']

Esquema:
root
 |-- Location: struct (nullable = true)
 |    |-- country: string (nullable = true)
 |    |-- lat: string (nullable = true)
 |    |-- locality: string (nullable = true)
 |    |-- long: string (nullable = true)
 |-- circuitId: string (nullable = true)
 |-- circuitName: string (nullable = true)
 |-- url: string (nullable = true)

Primeras filas:
+-----------------------------------------+-----------+------------------------------+----------------------------------------------------------+
|Location                                 |circuitId  |circuitName                   |url                                                       |
+-----------------------------------------+-----------+------------------------------+----------------------------------------------------------+
|{Australia, -34.9272, Adelaide, 138.617} |adelaide   |Adelaide Street Circuit       |https://en.wikipedia.org/wiki/Adelaide_Street_Circuit     |
|{Morocco, 33.5786, Casablanca, -7.6875}  |ain-diab   |Ain Diab                      |https://en.wikipedia.org/wiki/Ain-Diab_Circuit            |
|{UK, 53.4769, Liverpool, -2.94056}       |aintree    |Aintree                       |https://en.wikipedia.org/wiki/Aintree_Motor_Racing_Circuit|
|{Australia, -37.8497, Melbourne, 144.968}|albert_park|Albert Park Grand Prix Circuit|https://en.wikipedia.org/wiki/Albert_Park_Circuit         |
|{USA, 30.1328, Austin, -97.6411}         |americas   |Circuit of the Americas       |https://en.wikipedia.org/wiki/Circuit_of_the_Americas     |
+-----------------------------------------+-----------+------------------------------+----------------------------------------------------------+
only showing top 5 rows
```

# Races
```txt
===== Tabla: races (LND) =====
Filas: 1171   |   Columnas: 14
Nombres de columnas: ['Circuit', 'FirstPractice', 'Qualifying', 'SecondPractice', 'Sprint', 'SprintQualifying', 'SprintShootout', 'ThirdPractice', 'date', 'raceName', 'round', 'season', 'time', 'url']

Esquema:
root
 |-- Circuit: struct (nullable = true)
 |    |-- Location: struct (nullable = true)
 |    |    |-- country: string (nullable = true)
 |    |    |-- lat: string (nullable = true)
 |    |    |-- locality: string (nullable = true)
 |    |    |-- long: string (nullable = true)
 |    |-- circuitId: string (nullable = true)
 |    |-- circuitName: string (nullable = true)
 |    |-- url: string (nullable = true)
 |-- FirstPractice: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- Qualifying: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- SecondPractice: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- Sprint: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- SprintQualifying: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- SprintShootout: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- ThirdPractice: struct (nullable = true)
 |    |-- date: string (nullable = true)
 |    |-- time: string (nullable = true)
 |-- date: string (nullable = true)
 |-- raceName: string (nullable = true)
 |-- round: string (nullable = true)
 |-- season: string (nullable = true)
 |-- time: string (nullable = true)
 |-- url: string (nullable = true)

Primeras filas:
+---------------------------------------------------------------------------------------------------------------------------------------------+-------------+----------+--------------+------+----------------+--------------+-------------+----------+------------------+-----+------+----+-----------------------------------------------------+
|Circuit                                                                                                                                      |FirstPractice|Qualifying|SecondPractice|Sprint|SprintQualifying|SprintShootout|ThirdPractice|date      |raceName          |round|season|time|url                                                  |
+---------------------------------------------------------------------------------------------------------------------------------------------+-------------+----------+--------------+------+----------------+--------------+-------------+----------+------------------+-----+------+----+-----------------------------------------------------+
|{{UK, 52.0786, Silverstone, -1.01694}, silverstone, Silverstone Circuit, https://en.wikipedia.org/wiki/Silverstone_Circuit}                  |null         |null      |null          |null  |null            |null          |null         |1950-05-13|British Grand Prix|1    |1950  |null|https://en.wikipedia.org/wiki/1950_British_Grand_Prix|
|{{Monaco, 43.7347, Monte Carlo, 7.42056}, monaco, Circuit de Monaco, https://en.wikipedia.org/wiki/Circuit_de_Monaco}                        |null         |null      |null          |null  |null            |null          |null         |1950-05-21|Monaco Grand Prix |2    |1950  |null|https://en.wikipedia.org/wiki/1950_Monaco_Grand_Prix |
|{{USA, 39.795, Indianapolis, -86.2347}, indianapolis, Indianapolis Motor Speedway, https://en.wikipedia.org/wiki/Indianapolis_Motor_Speedway}|null         |null      |null          |null  |null            |null          |null         |1950-05-30|Indianapolis 500  |3    |1950  |null|https://en.wikipedia.org/wiki/1950_Indianapolis_500  |
|{{Switzerland, 46.9589, Bern, 7.40194}, bremgarten, Circuit Bremgarten, https://en.wikipedia.org/wiki/Circuit_Bremgarten}                    |null         |null      |null          |null  |null            |null          |null         |1950-06-04|Swiss Grand Prix  |4    |1950  |null|https://en.wikipedia.org/wiki/1950_Swiss_Grand_Prix  |
|{{Belgium, 50.4372, Spa, 5.97139}, spa, Circuit de Spa-Francorchamps, https://en.wikipedia.org/wiki/Circuit_de_Spa-Francorchamps}            |null         |null      |null          |null  |null            |null          |null         |1950-06-18|Belgian Grand Prix|5    |1950  |null|https://en.wikipedia.org/wiki/1950_Belgian_Grand_Prix|
+---------------------------------------------------------------------------------------------------------------------------------------------+-------------+----------+--------------+------+----------------+--------------+-------------+----------+------------------+-----+------+----+-----------------------------------------------------+
only showing top 5 rows
```

# Results
```txt
===== Tabla: results (LND) =====
Filas: 1410   |   Columnas: 8
Nombres de columnas: ['Circuit', 'Results', 'date', 'raceName', 'round', 'season', 'time', 'url']

Esquema:
root
 |-- Circuit: struct (nullable = true)
 |    |-- Location: struct (nullable = true)
 |    |    |-- country: string (nullable = true)
 |    |    |-- lat: string (nullable = true)
 |    |    |-- locality: string (nullable = true)
 |    |    |-- long: string (nullable = true)
 |    |-- circuitId: string (nullable = true)
 |    |-- circuitName: string (nullable = true)
 |    |-- url: string (nullable = true)
 |-- Results: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- Constructor: struct (nullable = true)
 |    |    |    |-- constructorId: string (nullable = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |    |-- nationality: string (nullable = true)
 |    |    |    |-- url: string (nullable = true)
 |    |    |-- Driver: struct (nullable = true)
 |    |    |    |-- code: string (nullable = true)
 |    |    |    |-- dateOfBirth: string (nullable = true)
 |    |    |    |-- driverId: string (nullable = true)
 |    |    |    |-- familyName: string (nullable = true)
 |    |    |    |-- givenName: string (nullable = true)
 |    |    |    |-- nationality: string (nullable = true)
 |    |    |    |-- permanentNumber: string (nullable = true)
 |    |    |    |-- url: string (nullable = true)
 |    |    |-- FastestLap: struct (nullable = true)
 |    |    |    |-- AverageSpeed: struct (nullable = true)
 |    |    |    |    |-- speed: string (nullable = true)
 |    |    |    |    |-- units: string (nullable = true)
 |    |    |    |-- Time: struct (nullable = true)
 |    |    |    |    |-- time: string (nullable = true)
 |    |    |    |-- lap: string (nullable = true)
 |    |    |    |-- rank: string (nullable = true)
 |    |    |-- Time: struct (nullable = true)
 |    |    |    |-- millis: string (nullable = true)
 |    |    |    |-- time: string (nullable = true)
 |    |    |-- grid: string (nullable = true)
 |    |    |-- laps: string (nullable = true)
 |    |    |-- number: string (nullable = true)
 |    |    |-- points: string (nullable = true)
 |    |    |-- position: string (nullable = true)
 |    |    |-- positionText: string (nullable = true)
 |    |    |-- status: string (nullable = true)
 |-- date: string (nullable = true)
 |-- raceName: string (nullable = true)
 |-- round: string (nullable = true)
 |-- season: string (nullable = true)
 |-- time: string (nullable = true)
 |-- url: string (nullable = true)
```

# Results
```txt
===== Tabla: constructors standings (LND) =====
Filas: 69   |   Columnas: 3
Nombres de columnas: ['ConstructorStandings', 'round', 'season']

Esquema:
root
 |-- ConstructorStandings: array (nullable = true)
 |    |-- element: struct (containsNull = true)
 |    |    |-- Constructor: struct (nullable = true)
 |    |    |    |-- constructorId: string (nullable = true)
 |    |    |    |-- name: string (nullable = true)
 |    |    |    |-- nationality: string (nullable = true)
 |    |    |    |-- url: string (nullable = true)
 |    |    |-- points: string (nullable = true)
 |    |    |-- position: string (nullable = true)
 |    |    |-- positionText: string (nullable = true)
 |    |    |-- wins: string (nullable = true)
 |-- round: string (nullable = true)
 |-- season: string (nullable = true)
```
