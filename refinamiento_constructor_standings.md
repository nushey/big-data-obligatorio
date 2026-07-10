# Refinamiento `constructor_standings` — documentación por columna

Ámbito: transformación `/LND` → `/RFN` de la tabla `constructor_standings`. Criterios externos a la tabla (recorte temporal 2000–2025, formato Parquet, zona destino) se documentan aparte, no en esta tabla.

| Columna (origen, post-aplanado) | Acción | Por qué |
| --- | --- | --- |
| `season` | Se mantiene, cast a `int`. | Viene como string en el JSON; se necesita como `int` para el filtro de recorte y como parte de la clave del fact. |
| `round` | Se renombra a `totalRounds`, cast a `int`. | Se verificó que la API entrega un único registro por temporada (no hay evolución ronda a ronda) y que ese `round` coincide siempre con el total de carreras disputadas en la temporada (validado contra `races`). El nombre original inducía a pensar que había granularidad por ronda. |
| `ConstructorStandings.Constructor.constructorId` | Se mantiene, sin transformar, como `constructorId`. | Es la FK a `dim_constructor`. Se validó que no hay huérfanos (todos los `constructorId` de 2000–2025 existen en `constructors`). |
| `ConstructorStandings.Constructor.name` | Se descarta. | Redundante: el nombre del constructor ya vive en `dim_constructor`, se resuelve por join vía `constructorId`. |
| `ConstructorStandings.Constructor.nationality` | Se descarta. | Redundante, mismo motivo que `name`. |
| `ConstructorStandings.Constructor.url` | Se descarta. | Redundante, mismo motivo que `name`. No aporta a ninguna de las 5 preguntas. |
| `ConstructorStandings.points` | Se mantiene, cast a `double`, como `points`. | Se confirmaron valores con decimales (ej. 613.5 en 2021 por reparto de medio punto), un cast a `int` truncaría datos reales. |
| `ConstructorStandings.position` | Se mantiene, cast a `int`, nullable, como `position`. | Los nulos no son error: corresponden a constructores sin puntos (`positionText="-"`) o excluidos del campeonato (`positionText="E"`, caso McLaren 2007). No se imputan ni se descartan esas filas. |
| `ConstructorStandings.positionText` | Se mantiene, sin transformar, como `positionText`. | Es la columna que explica el porqué de un `position` nulo (`-` o `E`); se conserva como trazabilidad/auditoría. |
| `ConstructorStandings.wins` | Se mantiene, cast a `int`, como `wins`. | Viene como string en el JSON; es un conteo entero sin excepciones detectadas. |
| — (no existe en origen) | Se agrega `raceId`, `sha2(concat_ws("_", season, totalRounds), 256)`. | Clave sintética consistente con la ya definida para `races` (`raceId = hash(season, round)`), para poder unir el fact directo contra `dim_race` sin duplicar lógica de join. |
| — (no existe en origen) | Se agrega `standingId`, `sha2(concat_ws("_", season, constructorId), 256)`. | Clave sintética propia del fact. Como hay un solo registro por temporada, la PK natural real es `(season, constructorId)`; se materializa como hash para tener un identificador único de fila. |
