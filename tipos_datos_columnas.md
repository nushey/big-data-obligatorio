# Seasons

| Columna | Tipo de dato | Significado |
|---|---|---|
| season | string | Año de la temporada (ej. `"1950"`). |
| url | string | Link a la página de Wikipedia de la temporada. Descartable en refinamiento. |

# Drivers

| Columna | Tipo de dato | Significado |
|---|---|---|
| driverId | string | Identificador único del piloto (clave natural, ej. `"hamilton"`). |
| code | string | Código de 3 letras del piloto (ej. `"HAM"`). Nulo en pilotos previos a ~2014, año en que se adoptó el código. |
| permanentNumber | string | Número permanente elegido por el piloto. Nulo en pilotos previos a ~2014, año en que se instauró la numeración permanente. |
| givenName | string | Nombre de pila del piloto. |
| familyName | string | Apellido del piloto. |
| dateOfBirth | string | Fecha de nacimiento del piloto (formato `YYYY-MM-DD`). |
| nationality | string | Nacionalidad del piloto (gentilicio en inglés, ej. `"Italian"`). |
| url | string | Link a la página de Wikipedia del piloto. Descartable en refinamiento, no aporta a las preguntas. |

# Constructors

| Columna | Tipo de dato | Significado |
|---|---|---|
| constructorId | string | Identificador único de la escudería/constructor (clave natural, ej. `"ferrari"`). |
| name | string | Nombre del constructor (ej. `"Alfa Romeo"`). |
| nationality | string | Nacionalidad del constructor (gentilicio en inglés). |
| url | string | Link a la página de Wikipedia del constructor. Descartable en refinamiento. |

# Status

| Columna | Tipo de dato | Significado |
|---|---|---|
| statusId | string | Identificador único del estado final de una participación en carrera (clave natural). |
| status | string | Descripción del estado (ej. `"Finished"`, `"Accident"`, `"+1 Lap"`). Base para definir el criterio DNF. |
| count | string | Conteo histórico global de ocurrencias de ese estado según la API. No filtrado a 2000-2025, no usar para la pregunta de tasa de DNF. |

# Circuits

| Columna | Tipo de dato | Significado |
|---|---|---|
| circuitId | string | Identificador único del circuito (clave natural, ej. `"monaco"`). |
| circuitName | string | Nombre del circuito (ej. `"Circuit de Monaco"`). |
| Location | struct | Objeto anidado con la ubicación geográfica del circuito. Se aplana en refinamiento. |
| Location.country | string | País donde está el circuito. |
| Location.locality | string | Ciudad/localidad donde está el circuito. |
| Location.lat | string | Latitud del circuito. Se castea a double en refinamiento, usada en el mapa de folium. |
| Location.long | string | Longitud del circuito. Se castea a double en refinamiento, usada en el mapa de folium. |
| url | string | Link a la página de Wikipedia del circuito. Descartable en refinamiento. |

# Races

| Columna | Tipo de dato | Significado |
|---|---|---|
| season | string | Año de la temporada (ej. `"2021"`). |
| round | string | Número de fecha/ronda dentro de la temporada. |
| raceName | string | Nombre del Gran Premio (ej. `"Monaco Grand Prix"`). |
| date | string | Fecha de la carrera (formato `YYYY-MM-DD`). |
| time | string | Hora de largada de la carrera (UTC). Frecuentemente nula en temporadas antiguas. |
| Circuit | struct | Objeto anidado con toda la info del circuito, redundante con la tabla `circuits`. Se descarta en refinamiento, dejando solo `circuitId` como FK. |
| FirstPractice | struct | Fecha/hora de la primera práctica libre. Nula en temporadas antiguas donde la API no la registra. |
| SecondPractice | struct | Fecha/hora de la segunda práctica libre. Nula en temporadas antiguas. |
| ThirdPractice | struct | Fecha/hora de la tercera práctica libre. Nula en fines de semana con formato sprint. |
| Qualifying | struct | Fecha/hora de la clasificación. Nula en temporadas antiguas. |
| Sprint | struct | Fecha/hora de la carrera sprint. Solo aplica desde 2021. |
| SprintQualifying | struct | Fecha/hora de la clasificación sprint. Nomenclatura usada desde 2023. |
| SprintShootout | struct | Fecha/hora del "sprint shootout". Nomenclatura usada solo en 2023. |
| url | string | Link a la página de Wikipedia de la carrera. Descartable en refinamiento. |

# Constructor Standings

| Columna | Tipo de dato | Significado |
|---|---|---|
| season | string | Año de la temporada a la que corresponde el standing. |
| round | string | Ronda/fecha del campeonato hasta la cual está calculado el standing acumulado. |
| ConstructorStandings | array\<struct\> | Arreglo con la posición de cada constructor en el campeonato tras esa ronda. Se explota (`explode`) en refinamiento para obtener una fila por constructor y ronda. |
| ConstructorStandings.Constructor.constructorId | string | Identificador del constructor (clave natural, FK a `constructors`). |
| ConstructorStandings.Constructor.name | string | Nombre del constructor. Redundante con la tabla `constructors`, descartable tras desanidar y quedarse con `constructorId` como FK. |
| ConstructorStandings.Constructor.nationality | string | Nacionalidad del constructor. Redundante con la tabla `constructors`, descartable en refinamiento. |
| ConstructorStandings.Constructor.url | string | Link a Wikipedia del constructor. Descartable en refinamiento. |
| ConstructorStandings.points | string | Puntos acumulados por el constructor hasta esa ronda. |
| ConstructorStandings.position | string | Posición del constructor en el campeonato tras esa ronda. |
| ConstructorStandings.positionText | string | Representación textual de la posición (normalmente igual a `position`, salvo casos de descalificación/exclusión). |
| ConstructorStandings.wins | string | Cantidad de victorias acumuladas del constructor hasta esa ronda. |
