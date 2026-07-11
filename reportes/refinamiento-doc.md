## **3.2 Limpieza de datos**

Se evidencia una tabla con las acciones realizadas para cada columna, además del motivo de las mismas.

### Colección 1 \- Seasons

| Columna (origen, post-aplanado) | Acción | Explicación |
| :---- | :---- | :---- |
| season | Se mantiene, cast a int. | Viene como string en el JSON, se castea a int para aplicar el recorte temporal 2000–2025 y ordenar el catálogo. Es la única columna útil de la colección. |
| url | Se descarta | No es necesaria para contestar las preguntas. |
| (fila) | Se aplica el recorte 2000–2025 (filas fuera del rango se descartan). | Por alcance del trabajo. |

### Colección 2 \- Drivers

| Columna (origen, post-aplanado) | Acción | Explicación |
| :---- | :---- | :---- |
| driverId | Se mantiene, sin transformar. | PK natural del catálogo de pilotos, FK a dim\_driver. |
| code | Se mantiene. | Código de 3 letras del piloto, puede ser null en pilotos antiguos (no es error). |
| familyName | Se mantiene. | Apellido del piloto. |
| givenName | Se mantiene. | Nombre del piloto. |
| permanentNumber | Se mantiene. | Número permanente del piloto, null en pilotos previos a su introducción. |
| dateOfBirth | Se mantiene, cast a date. | Viene como string en el JSON, se castea a date para tratarlo como fecha real. |
| nationality | Se mantiene. | Nacionalidad del piloto. |
| url | Se descarta. | Enlace a Wikipedia, redundante, no aporta a ninguna de las 5 preguntas. |

### Colección 3 \- Constructors

| Columna (origen, post-aplanado) | Acción | Por qué |
| :---- | :---- | :---- |
| constructorId | Se mantiene, sin transformar.  | PK natural del catálogo de escuderías. FK a dim\_constructor. |
| name | Se mantiene. | Nombre de la escudería. |
| nationality | Se mantiene. | Nacionalidad de la escudería. |
| url | Se descarta. | Enlace a Wikipedia, redundante, no aporta a ninguna de las 5 preguntas. |

### Colección 4 \- Circuits

| Columna (origen, post-aplanado) | Acción | Por qué |
| :---- | :---- | :---- |
| circuitId | Se mantiene, sin transformar.  | PK natural del catálogo de circuitos, FK a dim\_circuit. |
| circuitName | Se mantiene. | Nombre del circuito. |
| url | Se descarta. | Enlace a Wikipedia, redundante, no aporta a ninguna de las 5 preguntas. |
| Location.country | Se aplana a country. | Estaba anidado en el struct Location, se sube a la columna de primer nivel para consultarlo directo. |
| Location.locality | Se aplana a locality. | Mismo motivo que country: se desanida del struct Location. |
| Location.lat | Se aplana y renombra a latitude, cast a double. | Venía como string anidado en Location, se castea a double para usarlo como coordenada en el mapa. |
| Location.long | Se aplana y renombra a longitude, cast a double. | Mismo motivo que latitude: coordenada numérica para el mapa. |

### Colección 5 \- Status

| Columna (origen, post-aplanado) | Acción | Por qué |
| :---- | :---- | :---- |
| statusId | Se mantiene, cast a int.  | Viene como string en el JSON, PK del catálogo de estados y FK statusId de fact\_results. |
| status | Se mantiene, sin transformar. | Es el texto del estado final (ej. "Finished", "Accident", "+1 Lap"). Es la clave de join con results.status, que en jolpica es texto libre (no un id). |
| count | Se descarta. | Es un acumulado global de la API, la tasa de DNF se recalcula directamente desde /RFN, así que no aporta. |

### Colección 6 \- Races

| Columna (origen, post-aplanado) | Acción | Por qué |
| :---- | :---- | :---- |
| season | Se mantiene, cast a int. | Viene como string, se necesita para el recorte y como parte de la clave raceId. |
| round | Se mantiene, cast a int. | Viene como string, parte de la clave raceId. |
| raceName | Se mantiene. | Nombre del Gran Premio. |
| date | Se mantiene, cast a date. | Viene como string, se castea a date para tratarlo como fecha real. |
| Circuit.circuitId | Se aplana a circuitId. | Se conserva solo el id del struct Circuit como FK a dim\_circuit. |
| Circuit (circuitName, Location, url) | Se descartan. | Redundante: los datos del circuito ya viven en dim\_circuit, se resuelven por join vía circuitId. |
| FirstPractice, SecondPractice, ThirdPractice, Qualifying, Sprint, SprintQualifying, SprintShootout | Se descartan. | Datos de sesiones (prácticas, clasificación, sprint) que no aportan a ninguna de las 5 preguntas. |
| url | Se descarta. | Enlace a Wikipedia, redundante. |
| (no existe en origen) | Se agrega raceId, calculando el sha-256 con las columnas de la PK compuesta (season, round). | Clave sintética determinística, misma fórmula que en results para poder unir el fact directo contra dim\_race sin duplicar lógica de join. |
| (colección) | Se aplica el recorte 2000–2025. | Por alcance del trabajo. |

### Colección 7 \- Results

| Columna (origen, post-aplanado) | Acción | Por qué |
| :---- | :---- | :---- |
| Results (array) | Se hace explode, una fila por (carrera, piloto). | En el JSON cada carrera trae un array Results con todos los pilotos, se desanida para tener granularidad de resultado individual. |
| Circuit (struct entero) | Se descarta. | Para evitar duplicación de información, se puede obtener mediante races. |
| season | Se mantiene, cast a int. | Viene como string, se necesita para el recorte y como parte de las claves raceId y resultId. |
| round | Se mantiene, cast a int. | Viene como string, parte de las claves raceId y resultId. |
| Results.Constructor.constructorId | Se aplana a constructorId. | FK a dim\_constructor. |
| Results.Constructor (resto del struct)  | Se descarta | Redundante, se obtiene por join mediante constructorId. |
| Results.Driver.driverId | Se aplana a driverId. | FK a dim\_driver. |
| Results.Driver (resto del struct) | Se descarta. | Redundante, se obtiene por join mediante driverId. |
| Results.FastestLap (struct entero) | Se descarta. | Detalle de vueltas más rápidas, no aportan a las consultas. |
| Results.Time (struct entero) | Se descarta. | Detalle de tiempos, no aportan a las consultas. |
| Results.grid | Se mantiene, cast a int, como grid. | Viene como string, posición de largada. |
| Results.laps | Se mantiene, cast a int, como laps. | Viene como string, vueltas completadas. |
| Results.number | Se mantiene, cast a int, como number. | Viene como string, número del auto. Se conserva porque forma parte de resultId (desambigua autos compartidos/relevo). |
| Results.points | Se mantiene, cast a double, como points. | Puede tener decimales (medio punto), un cast a int truncaría datos reales. |
| Results.position | Se mantiene, cast a int, nullable, como position. | Viene como string. Aclaración, los nulos no son datos ausentes, corresponden a los que no terminaron (DNF). No se imputan ni se descartan esas filas. |
| Results.positionText | Se mantiene, como positionText. | Conserva el texto original ("R", "D", "1"…) para dar trazabilidad a los casos de position null. |
| Results.status | Se mantiene, como status (texto). | En jolpica el estado es texto libre (ej. "Finished", "+1 Lap"), no un id. Se resolverá a statusId en el modelado por join contra status.status. |
| (no existe en origen) | Se agrega raceId, calculando el sha-256 con las columnas de la PK compuesta de races (season, round). | FK a dim\_race, misma fórmula que en races para unir sin duplicar lógica de join. |
| (no existe en origen) | Se agrega resultId, calculando el sha-256 con las columnas de la PK compuesta (season, round, driverId, number). | Clave sintética propia del fact (PK de fila), el number desambigua autos compartidos/relevo. |
| (colección) | Se aplica el recorte 2000–2025. | Por alcance del trabajo. |

### Colección 8 \- Constructor Standings

| Columna (origen, post-aplanado) | Acción | Por qué |
| :---- | :---- | :---- |
| season | Se mantiene, cast a int. | Viene como string en el JSON, se necesita como int para el filtro de recorte y como parte de la clave del fact. |
| round | Se renombra a totalRounds, cast a int. | Se verificó que la API entrega un único registro por temporada (no hay evolución de ronda a ronda) y que ese round coincide siempre con el total de carreras disputadas en la temporada (validado contra races). El nombre original inducía a pensar que había granularidad por ronda. |
| ConstructorStandings.Constructor.constructorId | Se mantiene, sin transformar, como constructorId. | Es la FK a dim\_constructor. Se validó que no hay huérfanos (todos los constructorId de 2000–2025 existen en constructors). |
| ConstructorStandings.Constructor (resto del struct) | Se descarta. | Redundante, se obtiene por join mediante constructorId. |
| ConstructorStandings.points | Se mantiene, cast a double, como points. | Puntos acumulados por el constructor hasta esa ronda. |
| ConstructorStandings.position | Se mantiene, cast a int, como position. | Los nulos no son errores: corresponden a constructores sin puntos (positionText="-") o excluidos del campeonato (positionText="E", caso McLaren 2007). No se imputan ni se descartan esas filas. |
| ConstructorStandings.positionText | Se mantiene. | Representación textual de la posición (normalmente igual a position, salvo casos de descalificación/exclusión). |
| ConstructorStandings.wins | Se mantiene, cast a int, como wins. | Viene como string en el JSON, es un conteo entero sin excepciones detectadas. |
| (no existe en origen) | Se agrega standingId, calculando el sha-256 con las columnas de la PK compuesta (season, constructorId). | Clave sintética propia del fact. Como hay un solo registro por temporada, la PK natural real es (season, constructorId), se materializa como hash para tener un identificador único de fila. |
