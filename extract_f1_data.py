#!/usr/bin/env python3
"""
extract_f1_data.py — Extrae datos CRUDOS de F1 desde la API jolpica-f1 → CSV.

NO se aplica ningún filtro, recorte ni transformación. Los datos llegan tal cual
los devuelve la API. Cualquier filtrado (temporadas, limpieza, tipos) se hace
después en Spark (zona RFN).

Fuente:  https://api.jolpi.ca/ergast/f1/
Tablas:  circuits, drivers, constructors, status, races, results (globales)
         constructor_standings (por temporada, todas las disponibles)

Rate limits respetados:
  - Burst:     4 req/s  → delay de 0.35s entre requests (~2.8 req/s)
  - Sustained: 500 req/h → estimado ~330 requests totales

Uso:
  pip install requests
  python extract_f1_data.py

Genera 7 archivos CSV en ./data/
"""

import csv
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("ERROR: Necesitás instalar requests → pip install requests")
    sys.exit(1)


# ════════════════════════════════════════════════════════════════
# Configuración
# ════════════════════════════════════════════════════════════════

API_BASE    = "https://api.jolpi.ca/ergast/f1"
PAGE_LIMIT  = 100       # máximo permitido por la API
DELAY       = 0.35      # segundos entre requests (~2.8 req/s, burst limit = 4)
MAX_RETRIES = 5
OUTPUT_DIR  = Path("data")


# ════════════════════════════════════════════════════════════════
# Estado global y utilidades
# ════════════════════════════════════════════════════════════════

_stats = {"requests": 0, "errors": 0, "start": None}


def log(msg: str) -> None:
    elapsed = time.time() - _stats["start"] if _stats["start"] else 0
    print(f"[{elapsed:7.1f}s | {_stats['requests']:3d} req] {msg}")


def api_get(url: str) -> dict | None:
    """HTTP GET con reintentos y backoff exponencial ante 429."""
    for attempt in range(MAX_RETRIES):
        time.sleep(DELAY)
        try:
            resp = requests.get(url, timeout=30)
            _stats["requests"] += 1

            if resp.status_code == 200:
                return resp.json()

            if resp.status_code == 429:
                wait = (2 ** attempt) * 5
                log(f"    ⏳ Rate limit (429), esperando {wait}s...")
                time.sleep(wait)
                continue

            log(f"    ⚠  HTTP {resp.status_code}: {url}")

        except requests.RequestException as exc:
            log(f"    ⚠  Error de red: {exc}")

        time.sleep(2)

    _stats["errors"] += 1
    log(f"    ✗  Falló tras {MAX_RETRIES} intentos: {url}")
    return None


def paginate(endpoint: str):
    """Genera el objeto MRData de cada página de un endpoint paginado."""
    offset = 0
    while True:
        url = f"{endpoint}?limit={PAGE_LIMIT}&offset={offset}"
        data = api_get(url)
        if data is None:
            break

        mr = data["MRData"]
        total = int(mr.get("total", 0))

        if total == 0:
            break

        yield mr

        offset += PAGE_LIMIT
        if offset >= total:
            break


def save_csv(filename: str, rows: list[dict], fieldnames: list[str]) -> None:
    """Escribe una lista de dicts como CSV en OUTPUT_DIR."""
    filepath = OUTPUT_DIR / filename
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    size_kb = filepath.stat().st_size / 1024
    log(f"  ✔  {filename}: {len(rows)} filas ({size_kb:.1f} KB)")


# ════════════════════════════════════════════════════════════════
# Extractores — Todos globales, sin filtros
#
# Los .get(key, "") son manejo defensivo de campos opcionales
# en el JSON de la API (ej: un piloto sin 'code'). No filtran
# ni transforman nada: si el campo existe se copia tal cual,
# si no existe queda vacío en el CSV.
# ════════════════════════════════════════════════════════════════

CIRCUITS_COLS = [
    "circuitId", "circuitName", "locality", "country", "lat", "lng", "url",
]

def extract_circuits() -> list[dict]:
    log("📍 Extrayendo circuits...")
    rows = []
    for mr in paginate(f"{API_BASE}/circuits.json"):
        for c in mr["CircuitTable"]["Circuits"]:
            loc = c.get("Location", {})
            rows.append({
                "circuitId":   c["circuitId"],
                "circuitName": c.get("circuitName", ""),
                "locality":    loc.get("locality", ""),
                "country":     loc.get("country", ""),
                "lat":         loc.get("lat", ""),
                "lng":         loc.get("long", ""),
                "url":         c.get("url", ""),
            })
    save_csv("circuits.csv", rows, CIRCUITS_COLS)
    return rows


DRIVERS_COLS = [
    "driverId", "permanentNumber", "code",
    "givenName", "familyName", "dateOfBirth", "nationality", "url",
]

def extract_drivers() -> list[dict]:
    log("🏎  Extrayendo drivers...")
    rows = []
    for mr in paginate(f"{API_BASE}/drivers.json"):
        for d in mr["DriverTable"]["Drivers"]:
            rows.append({
                "driverId":        d["driverId"],
                "permanentNumber": d.get("permanentNumber", ""),
                "code":            d.get("code", ""),
                "givenName":       d.get("givenName", ""),
                "familyName":      d.get("familyName", ""),
                "dateOfBirth":     d.get("dateOfBirth", ""),
                "nationality":     d.get("nationality", ""),
                "url":             d.get("url", ""),
            })
    save_csv("drivers.csv", rows, DRIVERS_COLS)
    return rows


CONSTRUCTORS_COLS = [
    "constructorId", "name", "nationality", "url",
]

def extract_constructors() -> list[dict]:
    log("🏗  Extrayendo constructors...")
    rows = []
    for mr in paginate(f"{API_BASE}/constructors.json"):
        for c in mr["ConstructorTable"]["Constructors"]:
            rows.append({
                "constructorId": c["constructorId"],
                "name":          c.get("name", ""),
                "nationality":   c.get("nationality", ""),
                "url":           c.get("url", ""),
            })
    save_csv("constructors.csv", rows, CONSTRUCTORS_COLS)
    return rows


STATUS_COLS = ["statusId", "status", "count"]

def extract_status() -> list[dict]:
    log("🚦 Extrayendo status...")
    rows = []
    for mr in paginate(f"{API_BASE}/status.json"):
        for s in mr["StatusTable"]["Status"]:
            rows.append({
                "statusId": s["statusId"],
                "status":   s.get("status", ""),
                "count":    s.get("count", ""),
            })
    save_csv("status.csv", rows, STATUS_COLS)
    return rows


RACES_COLS = [
    "season", "round", "raceName", "circuitId", "date", "time", "url",
]

def extract_races() -> list[dict]:
    log("🏁 Extrayendo races (todas las temporadas)...")
    rows = []
    for mr in paginate(f"{API_BASE}/races.json"):
        for race in mr["RaceTable"]["Races"]:
            circuit = race.get("Circuit", {})
            rows.append({
                "season":    race.get("season", ""),
                "round":     race.get("round", ""),
                "raceName":  race.get("raceName", ""),
                "circuitId": circuit.get("circuitId", ""),
                "date":      race.get("date", ""),
                "time":      race.get("time", ""),
                "url":       race.get("url", ""),
            })
    save_csv("races.csv", rows, RACES_COLS)
    return rows


RESULTS_COLS = [
    "season", "round",
    "driverId", "constructorId",
    "number", "grid", "position", "positionText", "points", "laps",
    "status",
    "timeMillis", "timeText",
    "fastestLapRank", "fastestLapLap", "fastestLapTime",
    "fastestLapSpeed", "fastestLapSpeedUnits",
]

def extract_results() -> list[dict]:
    """
    Extrae TODOS los resultados de carrera de la historia de F1.

    El endpoint global /ergast/f1/results.json pagina sobre el total
    de resultados (~25.000+). Cada página devuelve un subconjunto de
    Races con sus Results anidados. Se aplana a una fila por resultado.
    """
    log("🏆 Extrayendo results (todas las temporadas — esto tarda ~80s)...")
    rows = []
    page = 0
    for mr in paginate(f"{API_BASE}/results.json"):
        page += 1
        total = mr.get("total", "?")
        offset = mr.get("offset", "?")
        if page % 25 == 0 or page == 1:
            log(f"    Página {page} (offset {offset} / {total})...")

        for race in mr["RaceTable"]["Races"]:
            season = race.get("season", "")
            rnd    = race.get("round", "")
            for r in race.get("Results", []):
                driver      = r.get("Driver", {})
                constructor = r.get("Constructor", {})
                time_obj    = r.get("Time", {})
                fastest     = r.get("FastestLap", {})
                fl_time     = fastest.get("Time", {})
                fl_speed    = fastest.get("AverageSpeed", {})

                rows.append({
                    "season":               season,
                    "round":                rnd,
                    "driverId":             driver.get("driverId", ""),
                    "constructorId":        constructor.get("constructorId", ""),
                    "number":               r.get("number", ""),
                    "grid":                 r.get("grid", ""),
                    "position":             r.get("position", ""),
                    "positionText":         r.get("positionText", ""),
                    "points":               r.get("points", ""),
                    "laps":                 r.get("laps", ""),
                    "status":               r.get("status", ""),
                    "timeMillis":           time_obj.get("millis", ""),
                    "timeText":             time_obj.get("time", ""),
                    "fastestLapRank":       fastest.get("rank", ""),
                    "fastestLapLap":        fastest.get("lap", ""),
                    "fastestLapTime":       fl_time.get("time", ""),
                    "fastestLapSpeed":      fl_speed.get("speed", ""),
                    "fastestLapSpeedUnits": fl_speed.get("units", ""),
                })
    save_csv("results.csv", rows, RESULTS_COLS)
    return rows


STANDINGS_COLS = [
    "season", "round", "constructorId",
    "position", "positionText", "points", "wins",
]

def extract_constructor_standings() -> list[dict]:
    """
    Extrae standings de constructores para TODAS las temporadas disponibles.

    El endpoint de standings requiere un parámetro de temporada en la ruta,
    así que primero se obtienen todas las temporadas desde /seasons.json
    y luego se itera cada una. Temporadas sin campeonato de constructores
    (antes de 1958) devuelven resultado vacío y se omiten sin filtrar.
    """
    # Paso 1: obtener todas las temporadas disponibles
    log("📅 Obteniendo lista de temporadas...")
    seasons = []
    for mr in paginate(f"{API_BASE}/seasons.json"):
        for s in mr["SeasonTable"]["Seasons"]:
            seasons.append(s["season"])
    log(f"    {len(seasons)} temporadas encontradas ({seasons[0]}–{seasons[-1]})")

    # Paso 2: extraer standings de cada temporada
    log("📊 Extrayendo constructor_standings (todas las temporadas)...")
    rows = []
    for i, season in enumerate(seasons):
        if (i + 1) % 10 == 0 or i == 0:
            log(f"    Temporada {season} ({i+1}/{len(seasons)})...")

        for mr in paginate(f"{API_BASE}/{season}/constructorstandings.json"):
            for sl in mr["StandingsTable"]["StandingsLists"]:
                rnd = sl.get("round", "")
                for cs in sl.get("ConstructorStandings", []):
                    constructor = cs.get("Constructor", {})
                    rows.append({
                        "season":        season,
                        "round":         rnd,
                        "constructorId": constructor.get("constructorId", ""),
                        "position":      cs.get("position", ""),
                        "positionText":  cs.get("positionText", ""),
                        "points":        cs.get("points", ""),
                        "wins":          cs.get("wins", ""),
                    })

    save_csv("constructor_standings.csv", rows, STANDINGS_COLS)
    return rows


# ════════════════════════════════════════════════════════════════
# Main
# ════════════════════════════════════════════════════════════════

def main():
    _stats["start"] = time.time()
    OUTPUT_DIR.mkdir(exist_ok=True)

    log("=" * 62)
    log("  F1 Data Extractor — jolpica-f1 API → CSV (datos crudos)")
    log(f"  Destino:    {OUTPUT_DIR.resolve()}")
    log(f"  Rate limit: {DELAY}s entre requests (~{1/DELAY:.1f} req/s)")
    log(f"  Estimado:   ~330 requests, ~2 minutos")
    log("=" * 62)

    extract_circuits()
    extract_drivers()
    extract_constructors()
    extract_status()
    extract_races()
    extract_results()
    extract_constructor_standings()

    # ── Resumen ──
    elapsed = time.time() - _stats["start"]
    log("=" * 62)
    log(f"  ✔  Completado en {elapsed:.0f}s ({elapsed/60:.1f} min)")
    log(f"     Requests totales: {_stats['requests']}")
    log(f"     Errores:          {_stats['errors']}")
    log("")
    log("  Archivos generados:")
    total_kb = 0
    for f in sorted(OUTPUT_DIR.glob("*.csv")):
        size_kb = f.stat().st_size / 1024
        total_kb += size_kb
        log(f"     {f.name:30s} {size_kb:8.1f} KB")
    log(f"     {'TOTAL':30s} {total_kb:8.1f} KB")
    log("=" * 62)

    if _stats["errors"] > 0:
        log("  ⚠  Hubo errores. Revisá la salida de arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
