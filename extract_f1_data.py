#!/usr/bin/env python3
"""
extract_f1_data.py — Extrae datos CRUDOS de F1 desde la API jolpica-f1 → JSON.

Descarga los datos estructuralmente intactos tal cual los devuelve la API.
No se aplana el JSON ni se rellenan valores nulos. Todo el procesamiento
estructural (ej. explode de results) se delega a Spark en la zona RFN.
"""

import json
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
PAGE_LIMIT  = 100
DELAY       = 0.35
MAX_RETRIES = 5
OUTPUT_DIR  = Path("data")

_stats = {"requests": 0, "errors": 0, "start": None}

def log(msg: str) -> None:
    elapsed = time.time() - _stats["start"] if _stats["start"] else 0
    print(f"[{elapsed:7.1f}s | {_stats['requests']:3d} req] {msg}")

def api_get(url: str) -> dict | None:
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

def paginate_and_collect(endpoint_url: str, table_key: str, array_key: str) -> list[dict]:
    """Recorre la paginación y extrae el arreglo interno crudo sin aplanar."""
    records = []
    offset = 0
    page = 0
    while True:
        page += 1
        url = f"{endpoint_url}?limit={PAGE_LIMIT}&offset={offset}"
        data = api_get(url)
        if not data:
            break
            
        mr = data.get("MRData", {})
        total = int(mr.get("total", 0))
        
        if page % 25 == 0 or page == 1:
            log(f"    Página {page} (offset {offset} / {total})...")

        items = mr.get(table_key, {}).get(array_key, [])
        records.extend(items)

        offset += PAGE_LIMIT
        if offset >= total or not items:
            break
            
    return records

def save_json(filename: str, data: list[dict]) -> None:
    filepath = OUTPUT_DIR / f"{filename}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        # Se guarda como un array JSON válido
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    size_kb = filepath.stat().st_size / 1024
    log(f"  ✔  {filename}.json: {len(data)} elementos raíz ({size_kb:.1f} KB)")

# ════════════════════════════════════════════════════════════════
# Extractores
# ════════════════════════════════════════════════════════════════

def main():
    _stats["start"] = time.time()
    OUTPUT_DIR.mkdir(exist_ok=True)

    log("=" * 62)
    log("  F1 Data Extractor — API → JSON (100% Crudo)")
    log("=" * 62)

    # 1. Seasons
    log("📅 Extrayendo seasons...")
    seasons_data = paginate_and_collect(f"{API_BASE}/seasons.json", "SeasonTable", "Seasons")
    save_json("seasons", seasons_data)
    
    seasons_list = [s["season"] for s in seasons_data]

    # 2. Entidades Simples
    log("📍 Extrayendo circuits...")
    save_json("circuits", paginate_and_collect(f"{API_BASE}/circuits.json", "CircuitTable", "Circuits"))

    log("🏎  Extrayendo drivers...")
    save_json("drivers", paginate_and_collect(f"{API_BASE}/drivers.json", "DriverTable", "Drivers"))

    log("🏗  Extrayendo constructors...")
    save_json("constructors", paginate_and_collect(f"{API_BASE}/constructors.json", "ConstructorTable", "Constructors"))

    log("🚦 Extrayendo status...")
    save_json("status", paginate_and_collect(f"{API_BASE}/status.json", "StatusTable", "Status"))

    log("🏁 Extrayendo races...")
    save_json("races", paginate_and_collect(f"{API_BASE}/races.json", "RaceTable", "Races"))

    # 3. Results (Mantiene la estructura Race -> [Results] anidada)
    log("🏆 Extrayendo results (histórico completo, anidado)...")
    save_json("results", paginate_and_collect(f"{API_BASE}/results.json", "RaceTable", "Races"))

    # 4. Constructor Standings (Itera por temporada)
    log("📊 Extrayendo constructor_standings por temporada...")
    standings_data = []
    for i, season in enumerate(seasons_list):
        if (i + 1) % 10 == 0 or i == 0:
            log(f"    Temporada {season} ({i+1}/{len(seasons_list)})...")
        url = f"{API_BASE}/{season}/constructorstandings.json"
        standings_data.extend(paginate_and_collect(url, "StandingsTable", "StandingsLists"))
    save_json("constructor_standings", standings_data)

    elapsed = time.time() - _stats["start"]
    log("=" * 62)
    log(f"  ✔  Completado en {elapsed:.0f}s. Requests totales: {_stats['requests']}")

if __name__ == "__main__":
    main()