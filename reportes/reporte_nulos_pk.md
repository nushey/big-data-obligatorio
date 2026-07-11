# Reporte de nulos y PK — post-aplanado (`/LND`)

## seasons

Total de filas (post-aplanado): **77**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| season | 0 | 0 | 77 | 0.0% |
| url | 0 | 0 | 77 | 0.0% |

**PK ['season']: filas=77, combinaciones distintas=77, es única = True**

## drivers

Total de filas (post-aplanado): **881**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| code | 774 | 0 | 107 | 87.9% |
| dateOfBirth | 16 | 0 | 865 | 1.8% |
| driverId | 0 | 0 | 881 | 0.0% |
| familyName | 0 | 0 | 881 | 0.0% |
| givenName | 0 | 0 | 881 | 0.0% |
| nationality | 16 | 0 | 865 | 1.8% |
| permanentNumber | 818 | 0 | 63 | 92.8% |
| url | 16 | 0 | 865 | 1.8% |

**PK ['driverId']: filas=881, combinaciones distintas=881, es única = True**

## constructors

Total de filas (post-aplanado): **214**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| constructorId | 0 | 0 | 214 | 0.0% |
| name | 0 | 0 | 214 | 0.0% |
| nationality | 0 | 0 | 214 | 0.0% |
| url | 0 | 0 | 214 | 0.0% |

**PK ['constructorId']: filas=214, combinaciones distintas=214, es única = True**

## circuits

Total de filas (post-aplanado): **78**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| Location.country | 0 | 0 | 78 | 0.0% |
| Location.lat | 0 | 0 | 78 | 0.0% |
| Location.locality | 0 | 0 | 78 | 0.0% |
| Location.long | 0 | 0 | 78 | 0.0% |
| circuitId | 0 | 0 | 78 | 0.0% |
| circuitName | 0 | 0 | 78 | 0.0% |
| url | 0 | 0 | 78 | 0.0% |

**PK ['circuitId']: filas=78, combinaciones distintas=78, es única = True**

## status

Total de filas (post-aplanado): **136**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| count | 0 | 0 | 136 | 0.0% |
| status | 0 | 0 | 136 | 0.0% |
| statusId | 0 | 0 | 136 | 0.0% |

**PK ['statusId']: filas=136, combinaciones distintas=136, es única = True**

## races

Total de filas (post-aplanado): **1171**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| Circuit.Location.country | 0 | 0 | 1171 | 0.0% |
| Circuit.Location.lat | 0 | 0 | 1171 | 0.0% |
| Circuit.Location.locality | 0 | 0 | 1171 | 0.0% |
| Circuit.Location.long | 0 | 0 | 1171 | 0.0% |
| Circuit.circuitId | 0 | 0 | 1171 | 0.0% |
| Circuit.circuitName | 0 | 0 | 1171 | 0.0% |
| Circuit.url | 0 | 0 | 1171 | 0.0% |
| FirstPractice.date | 750 | 0 | 421 | 64.0% |
| FirstPractice.time | 1057 | 0 | 114 | 90.3% |
| Qualifying.date | 750 | 0 | 421 | 64.0% |
| Qualifying.time | 1057 | 0 | 114 | 90.3% |
| SecondPractice.date | 774 | 0 | 397 | 66.1% |
| SecondPractice.time | 1081 | 0 | 90 | 92.3% |
| Sprint.date | 1141 | 0 | 30 | 97.4% |
| Sprint.time | 1144 | 0 | 27 | 97.7% |
| SprintQualifying.date | 1153 | 0 | 18 | 98.5% |
| SprintQualifying.time | 1153 | 0 | 18 | 98.5% |
| SprintShootout.date | 1165 | 0 | 6 | 99.5% |
| SprintShootout.time | 1165 | 0 | 6 | 99.5% |
| ThirdPractice.date | 780 | 0 | 391 | 66.6% |
| ThirdPractice.time | 1084 | 0 | 87 | 92.6% |
| date | 0 | 0 | 1171 | 0.0% |
| raceName | 0 | 0 | 1171 | 0.0% |
| round | 0 | 0 | 1171 | 0.0% |
| season | 0 | 0 | 1171 | 0.0% |
| time | 731 | 0 | 440 | 62.4% |
| url | 0 | 0 | 1171 | 0.0% |

**PK ['season', 'round']: filas=1171, combinaciones distintas=1171, es única = True**

## results

Total de filas (post-aplanado): **26071**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| Circuit.Location.country | 0 | 0 | 26071 | 0.0% |
| Circuit.Location.lat | 0 | 0 | 26071 | 0.0% |
| Circuit.Location.locality | 0 | 0 | 26071 | 0.0% |
| Circuit.Location.long | 0 | 0 | 26071 | 0.0% |
| Circuit.circuitId | 0 | 0 | 26071 | 0.0% |
| Circuit.circuitName | 0 | 0 | 26071 | 0.0% |
| Circuit.url | 0 | 0 | 26071 | 0.0% |
| Results.Constructor.constructorId | 0 | 0 | 26071 | 0.0% |
| Results.Constructor.name | 0 | 0 | 26071 | 0.0% |
| Results.Constructor.nationality | 0 | 0 | 26071 | 0.0% |
| Results.Constructor.url | 0 | 0 | 26071 | 0.0% |
| Results.Driver.code | 15246 | 0 | 10825 | 58.5% |
| Results.Driver.dateOfBirth | 0 | 0 | 26071 | 0.0% |
| Results.Driver.driverId | 0 | 0 | 26071 | 0.0% |
| Results.Driver.familyName | 0 | 0 | 26071 | 0.0% |
| Results.Driver.givenName | 0 | 0 | 26071 | 0.0% |
| Results.Driver.nationality | 0 | 0 | 26071 | 0.0% |
| Results.Driver.permanentNumber | 18833 | 0 | 7238 | 72.2% |
| Results.Driver.url | 0 | 0 | 26071 | 0.0% |
| Results.FastestLap.AverageSpeed.speed | 17833 | 0 | 8238 | 68.4% |
| Results.FastestLap.AverageSpeed.units | 17833 | 0 | 8238 | 68.4% |
| Results.FastestLap.Time.time | 17157 | 0 | 8914 | 65.8% |
| Results.FastestLap.lap | 17157 | 0 | 8914 | 65.8% |
| Results.FastestLap.rank | 17157 | 0 | 8914 | 65.8% |
| Results.Time.millis | 17587 | 0 | 8484 | 67.5% |
| Results.Time.time | 17587 | 30 | 8454 | 67.5% |
| Results.grid | 0 | 0 | 26071 | 0.0% |
| Results.laps | 0 | 0 | 26071 | 0.0% |
| Results.number | 0 | 0 | 26071 | 0.0% |
| Results.points | 0 | 0 | 26071 | 0.0% |
| Results.position | 0 | 0 | 26071 | 0.0% |
| Results.positionText | 0 | 0 | 26071 | 0.0% |
| Results.status | 0 | 0 | 26071 | 0.0% |
| date | 0 | 0 | 26071 | 0.0% |
| raceName | 0 | 0 | 26071 | 0.0% |
| round | 0 | 0 | 26071 | 0.0% |
| season | 0 | 0 | 26071 | 0.0% |
| time | 17108 | 0 | 8963 | 65.6% |
| url | 0 | 0 | 26071 | 0.0% |

**PK ['season', 'round', 'Results.Driver.driverId', 'Results.number']: filas=26071, combinaciones distintas=26071, es única = True**

## constructor_standings

Total de filas (post-aplanado): **924**

| Columna | Nulos | Vacíos | Con dato | % nulos |
| --- | --- | --- | --- | --- |
| ConstructorStandings.Constructor.constructorId | 0 | 0 | 924 | 0.0% |
| ConstructorStandings.Constructor.name | 0 | 0 | 924 | 0.0% |
| ConstructorStandings.Constructor.nationality | 0 | 0 | 924 | 0.0% |
| ConstructorStandings.Constructor.url | 0 | 0 | 924 | 0.0% |
| ConstructorStandings.points | 0 | 0 | 924 | 0.0% |
| ConstructorStandings.position | 212 | 0 | 712 | 22.9% |
| ConstructorStandings.positionText | 0 | 0 | 924 | 0.0% |
| ConstructorStandings.wins | 0 | 0 | 924 | 0.0% |
| round | 0 | 0 | 924 | 0.0% |
| season | 0 | 0 | 924 | 0.0% |

**PK ['season', 'round', 'ConstructorStandings.Constructor.constructorId']: filas=924, combinaciones distintas=924, es única = True**

