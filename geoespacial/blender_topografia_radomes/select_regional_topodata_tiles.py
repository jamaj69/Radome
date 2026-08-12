"""Seleciona somente as folhas TOPODATA ausentes para uma moldura regional."""
import argparse
import json
from pathlib import Path

from regional_terrain_geometry import checked_bounds, regional_bounds


def tile_name(latitude, longitude):
    """Nome oficial da folha cuja borda superior esquerda contém o ponto."""
    import math
    latitude_degree = math.floor(abs(latitude)) if latitude < 0 else math.ceil(latitude)
    hemisphere = "S" if latitude < 0 else "N"
    west = math.ceil(abs(longitude) / 1.5 - 1e-12) * 1.5
    longitude_part = f"{int(west):02d}_" if west.is_integer() else f"{int(west):02d}5"
    return f"{latitude_degree:02d}{hemisphere}{longitude_part}ZN.zip"


def required_names(bounds, spacing=.02):
    west, south, east, north = bounds
    if spacing <= 0:
        raise ValueError("O espaçamento precisa ser positivo")
    names = set()
    latitude = south
    while latitude <= north + spacing * .01:
        longitude = west
        while longitude <= east + spacing * .01:
            names.add(tile_name(latitude, longitude))
            longitude += spacing
        latitude += spacing
    return sorted(names)


def build(selection, manifest, existing_dir, output, margin_degrees=.25, spacing=.02, bbox=None):
    sites = json.loads(selection.read_text(encoding="utf-8"))["selected_sites"]
    bounds = checked_bounds(bbox) if bbox is not None else regional_bounds(sites, margin_degrees)
    inventory = {item["name"]: item for item in json.loads(manifest.read_text(encoding="utf-8"))["archives"]}
    required = required_names(bounds, spacing)
    unavailable = sorted(name for name in required if name not in inventory)
    if unavailable:
        raise ValueError(f"Folhas não publicadas no inventário oficial: {unavailable}")
    existing = {path.name for path in existing_dir.glob("*.zip")}
    new = [inventory[name] for name in required if name not in existing]
    result = {
        "schema_version": 1,
        "selection": str(selection), "manifest": str(manifest), "existing_directory": str(existing_dir),
        "bbox_wgs84": list(bounds), "sample_spacing_degrees": spacing,
        "required_archive_count": len(required), "already_local_archive_count": len(required) - len(new),
        "new_archive_count": len(new), "new_listed_size_bytes": sum(item["listed_size_bytes"] for item in new),
        "required_archive_names": required, "missing_archive_names": [], "archives": [inventory[name] for name in required],
        "selection_semantics": "Folhas ZN oficiais necessárias à moldura regional. A aquisição reutiliza ZIPs presentes, mas a extração revalida todas as folhas requeridas; o processo não altera cotas nem infere adequação de sítio.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--selection", type=Path, required=True); parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--existing-dir", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--margin-degrees", type=float, default=.25); parser.add_argument("--spacing-degrees", type=float, default=.02)
    parser.add_argument("--bbox", type=float, nargs=4, metavar=("WEST", "SOUTH", "EAST", "NORTH"))
    arguments = parser.parse_args()
    build(arguments.selection, arguments.manifest, arguments.existing_dir, arguments.output, arguments.margin_degrees, arguments.spacing_degrees, arguments.bbox)
