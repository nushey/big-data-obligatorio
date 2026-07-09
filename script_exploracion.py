# =============================================================================
# Notebook 1 — EDA / Exploración de datos (F1, jolpica-f1)
# Fase: vista previa + esquema, nulos por key aplanada y validación de PKs.
# Cada bloque "# %%" corresponde a una celda del notebook.
# =============================================================================

# %% ------------------------------------------------------------------------
# 1. Conexión Spark
# ----------------------------------------------------------------------------
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, ArrayType

spark = SparkSession.builder \
    .appName("F1_EDA_Refinamiento") \
    .enableHiveSupport() \
    .getOrCreate()

# Reducir ruido de logs para que la demo se vea limpia
spark.sparkContext.setLogLevel("WARN")

LND_PATH = "ort/LND"
RFN_PATH = "ort/RFN"

# %% ------------------------------------------------------------------------
# 2. Carga de tablas desde /LND
# ----------------------------------------------------------------------------
TABLAS_LND = [
    "seasons",
    "drivers",
    "constructors",
    "circuits",
    "status",
    "races",
    "results",
    "constructor_standings",
]

def cargar_tabla(nombre):
    """Lee el JSON multilínea de una tabla desde /LND."""
    return spark.read.option("multiLine", True).json(f"{LND_PATH}/{nombre}.json")

# Un solo dict con todos los DataFrames crudos, indexado por nombre de tabla
DATAFRAMES = {nombre: cargar_tabla(nombre) for nombre in TABLAS_LND}

# %% ------------------------------------------------------------------------
# 3. Helpers generales
# ----------------------------------------------------------------------------
def _q(nombre):
    """Escapa un nombre de columna con backticks (necesario cuando el alias contiene puntos)."""
    return f"`{nombre}`"

def perfil(df, nombre, show_data=True):
    """Vista previa + cantidad/nombre de columnas + esquema."""
    print(f"===== Tabla: {nombre} =====")
    print(f"Filas: {df.count()}   |   Columnas: {len(df.columns)}")
    print(f"Nombres de columnas: {df.columns}\n")
    print("Esquema:")
    df.printSchema()
    if show_data:
        print("Primeras filas:")
        df.show(5, truncate=False)

# %% ------------------------------------------------------------------------
# 4. Aplanado recursivo (structs + arrays -> columnas hoja)
# ----------------------------------------------------------------------------
def aplanar(df, sep="."):
    """Aplana el DataFrame hasta dejar solo columnas hoja (tipos simples).
    - struct  -> una columna por campo, con alias 'padre.hijo'
    - array   -> explode_outer (una fila por elemento; conserva filas con array nulo/vacío)
    ⚠️ Los arrays cambian el grano: la cantidad de filas del resultado no es la original.
    """
    while True:
        complejo = next(
            ((f.name, f.dataType) for f in df.schema.fields
             if isinstance(f.dataType, (StructType, ArrayType))),
            None
        )
        if complejo is None:
            return df
        nombre, tipo = complejo
        if isinstance(tipo, ArrayType):
            df = df.withColumn(nombre, F.explode_outer(F.col(_q(nombre))))
        else:  # StructType: reemplazar la columna por sus campos, respetando el orden
            seleccion = []
            for c in df.columns:
                if c != nombre:
                    seleccion.append(F.col(_q(c)))
                else:
                    for hijo in tipo.fields:
                        seleccion.append(
                            F.col(_q(nombre))[hijo.name].alias(f"{nombre}{sep}{hijo.name}")
                        )
            df = df.select(seleccion)

# %% ------------------------------------------------------------------------
# 5. Nulos
# ----------------------------------------------------------------------------
def reporte_nulos(df, etiqueta_fila="filas"):
    """Reporte de nulos/vacíos por columna sobre un DataFrame ya plano."""
    total = df.count()
    expr_nulos  = [F.count(F.when(F.col(_q(c)).isNull(), True)).alias(c) for c in df.columns]
    expr_vacios = [F.count(F.when(F.col(_q(c)).isNotNull() &
                                  (F.trim(F.col(_q(c)).cast("string")) == ""), True)).alias(c)
                   for c in df.columns]
    fila_nulos  = df.select(expr_nulos).first()
    fila_vacios = df.select(expr_vacios).first()

    ancho = max(len(c) for c in df.columns) + 2
    print(f"Total de {etiqueta_fila}: {total}\n")
    print(f"{'Columna':{ancho}s} | {'Nulos':>7s} | {'Vacíos':>7s} | {'Con dato':>8s} | {'% nulos':>7s}")
    print("-" * (ancho + 42))
    for c in df.columns:
        n, v = fila_nulos[c], fila_vacios[c]
        pct = 100 * n / total if total else 0
        print(f"{c:{ancho}s} | {n:7d} | {v:7d} | {total - n - v:8d} | {pct:6.1f}%")

def nulos_completo(df, nombre):
    """Aplana la tabla (structs + arrays) y reporta nulos/vacíos por cada key hoja."""
    print(f"===== Nulos: {nombre} =====")
    df_plano = aplanar(df).cache()
    reporte_nulos(df_plano, etiqueta_fila="filas (post-aplanado)")
    return df_plano  # se devuelve por si se quiere reutilizar sin recalcular

# %% ------------------------------------------------------------------------
# 6. Validación de PK
# ----------------------------------------------------------------------------
def pk_unica(df, pk):
    """Verifica unicidad de una PK (simple o compuesta) sobre un DataFrame plano."""
    pk = pk if isinstance(pk, list) else [pk]
    total = df.count()
    distintos = df.select([F.col(_q(c)) for c in pk]).distinct().count()
    print(f"PK {pk}: filas={total}, combinaciones distintas={distintos}, es única = {total == distintos}")
    dups = (df.groupBy([F.col(_q(c)) for c in pk])
              .count()
              .filter(F.col("count") > 1)
              .orderBy(F.col("count").desc()))
    if dups.limit(1).count() > 0:
        print("Combinaciones duplicadas de la PK:")
        dups.show(20, truncate=False)

# %% ------------------------------------------------------------------------
# 7. Configuración de PKs por tabla (nombres post-aplanado)
# ----------------------------------------------------------------------------
TABLAS = {
    "seasons":      [["season"]],
    "drivers":      [["driverId"]],
    "constructors": [["constructorId"]],
    "circuits":     [["circuitId"]],
    "status":       [["statusId"]],
    "races":        [["season", "round"]],
    "results": [
        # PK confirmada, base del resultId sintético
        ["season", "round", "Results.Driver.driverId", "Results.number"],
    ],
    "constructor_standings": [
        ["season", "round", "ConstructorStandings.Constructor.constructorId"],
    ],
}

# %% ------------------------------------------------------------------------
# 8. Orquestador
# ----------------------------------------------------------------------------
def explorar(nombre):
    """Corre el análisis de nulos y las validaciones de PK candidatas de una tabla."""
    df_plano = nulos_completo(DATAFRAMES[nombre], nombre)
    print()
    for pk in TABLAS[nombre]:
        pk_unica(df_plano, pk)
    df_plano.unpersist()
    print()