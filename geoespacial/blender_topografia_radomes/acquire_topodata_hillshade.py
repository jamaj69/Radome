"""Adquire, valida e registra as folhas TOPODATA de relevo sombreado (RS)."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from acquire_topodata_route_tiles import acquire_archive, atomic_json, sha256_file


BASE_URL = "http://www.dsr.inpe.br/topodata/data/geotiff"


def hillshade_archive_name(altitude_tile):
    stem = Path(altitude_tile).stem
    if not stem.endswith("ZN"):
        raise ValueError(f"Folha de altitude inesperada: {altitude_tile}")
    return f"{stem[:-2]}RS.zip"


def acquire(selection, terrain, output_dir, receipt, base_url=BASE_URL):
    sites = json.loads(selection.read_text(encoding="utf-8"))["selected_sites"]
    terrain_sites = json.loads(terrain.read_text(encoding="utf-8"))["sites"]
    terrain_by_name = {item["display_name"]: item for item in terrain_sites}
    archives = []
    for site in sites:
        altitude_tile = terrain_by_name[site["display_name"]]["tile"]
        name = hillshade_archive_name(altitude_tile)
        archives.append({"name": name, "url": f"{base_url}/{name}", "site": site["display_name"]})
    unique = {item["name"]: item for item in archives}
    results = []
    for item in sorted(unique.values(), key=lambda value: value["name"]):
        record = {**item}
        try:
            record.update(acquire_archive(item["url"], output_dir / item["name"]))
        except Exception as error:
            record.update(status="failed", error=f"{type(error).__name__}: {error}")
        results.append(record)
    value = {
        "schema_version": 1, "product": "TOPODATA_RS_hillshade",
        "selection": str(selection), "selection_sha256": sha256_file(selection),
        "terrain": str(terrain), "terrain_sha256": sha256_file(terrain),
        "archives": results,
        "complete": all(item["status"] in {"downloaded", "reused"} for item in results),
        "semantics": "TOPODATA relevo sombreado (RS), apenas para textura cartografica; Z continua derivado de ZN.",
    }
    atomic_json(receipt, value)
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True)
    parser.add_argument("--terrain", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--base-url", default=BASE_URL)
    arguments = parser.parse_args()
    result = acquire(arguments.selection, arguments.terrain, arguments.output_dir, arguments.receipt, arguments.base_url)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["complete"] else 1)
