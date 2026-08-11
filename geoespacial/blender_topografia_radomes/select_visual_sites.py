#!/usr/bin/env /home/python/pyenv/bin/python
"""Seleciona três sítios para a visualização esférica, sem promovê-los a sítios aprovados."""
from __future__ import annotations
import argparse, csv, gzip, json
from pathlib import Path

SEMANTICS = ("visual selection from preliminary multicriteria ranking and geometric infrastructure incidences; "
             "not terrain visibility, RF illumination, feasibility, or operational siting")

def build(ranking: Path, output: Path, minimum_elevation_m: float = 1000.0, minimum_incidence: int = 500) -> dict:
    with gzip.open(ranking, "rt", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    selected = []
    for row in sorted(rows, key=lambda item: int(item["robust_rank"])):
        incidences = sum(int(row[key]) for key in ("nearby_smp_site_count", "nearby_broadcast_site_count", "nearby_radio_link_endpoint_count"))
        if float(row["terrain_elevation_m"]) >= minimum_elevation_m and incidences >= minimum_incidence:
            selected.append({"node_id": row["node_id"], "name": row["name"], "longitude": float(row["longitude"]),
                             "latitude": float(row["latitude"]), "terrain_elevation_m": float(row["terrain_elevation_m"]),
                             "robust_rank": int(row["robust_rank"]), "geometric_illuminator_incidence_count": incidences,
                             "smp_site_count": int(row["nearby_smp_site_count"]), "broadcast_site_count": int(row["nearby_broadcast_site_count"]),
                             "radio_link_endpoint_count": int(row["nearby_radio_link_endpoint_count"]), "semantics": SEMANTICS})
        if len(selected) == 3: break
    if len(selected) != 3: raise ValueError("fewer than three candidates meet the visual-selection thresholds")
    result = {"schema_version": 1, "ranking": str(ranking), "minimum_elevation_m": minimum_elevation_m,
              "minimum_geometric_illuminator_incidence": minimum_incidence, "selected_sites": selected, "semantics": SEMANTICS}
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__); parser.add_argument("--ranking", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--minimum-elevation-m", type=float, default=1000.0); parser.add_argument("--minimum-incidence", type=int, default=500); args = parser.parse_args()
    print(json.dumps(build(args.ranking, args.output, args.minimum_elevation_m, args.minimum_incidence), ensure_ascii=False, indent=2))
