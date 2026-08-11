#!/usr/bin/env python3
"""Inventaria coordenadas, elevação e RF dos auxílios DECEA/ICA baixados."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


LAYER_FIELDS = {
    "vor": {
        "latitude": "latitude", "longitude": "longitude", "elevation": "elevation",
        "elevation_unit": "elevationu", "frequency": "frequency", "frequency_unit": "frequnits",
        "power": "power", "antenna_height": "antennahei", "kind": "vortype",
    },
    "ndb": {
        "latitude": "geolat", "longitude": "geolong", "elevation": "valelev",
        "elevation_unit": "elevationu", "frequency": "valfreq", "frequency_unit": "uomfreq",
        "emission_band": "emissionba", "kind": "tipo",
    },
    "dme": {
        "latitude": "geolat", "longitude": "geolong", "elevation": "valelev",
        "elevation_unit": "elevationu", "channel": "valchannel",
        "paired_frequency": "valghostfr", "paired_frequency_unit": "uomghostfr", "kind": "tipo",
    },
    "navaids": {
        "latitude": "latitude", "longitude": "longitude", "elevation": "elevation",
        "elevation_unit": "elevationu", "kind": "type",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def present(value: object) -> bool:
    return value is not None and value != ""


def inventory_layer(path: Path, fields: dict[str, str]) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    features = data.get("features", [])
    properties = [feature.get("properties", {}) for feature in features]
    completeness = {
        semantic: sum(present(item.get(source)) for item in properties)
        for semantic, source in fields.items()
    }
    kinds = Counter(item.get(fields["kind"]) or "N/I" for item in properties)
    result = {
        "file": str(path), "size_bytes": path.stat().st_size,
        "sha256": sha256(path), "feature_count": len(features),
        "geometry_count": sum(feature.get("geometry") is not None for feature in features),
        "crs": data.get("crs"), "field_mapping": fields,
        "completeness": completeness, "kinds": dict(kinds.most_common()),
    }
    for semantic in ("elevation", "frequency", "channel", "paired_frequency"):
        source = fields.get(semantic)
        values = [item.get(source) for item in properties] if source else []
        numeric = [float(value) for value in values if present(value)]
        if numeric:
            result[f"{semantic}_range"] = [min(numeric), max(numeric)]
    for semantic in ("elevation_unit", "frequency_unit", "paired_frequency_unit"):
        source = fields.get(semantic)
        if source:
            result[f"{semantic}s"] = dict(Counter(item.get(source) or "N/I" for item in properties).most_common())
    emendas = sorted({item.get("emenda") for item in properties if item.get("emenda")})
    result["amendment_dates"] = emendas
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    layers = {
        name: inventory_layer(args.input_dir / f"{name}.geojson", fields)
        for name, fields in LAYER_FIELDS.items()
    }
    result = {
        "schema_version": 1,
        "authority": "DECEA / ICA GEOAISWEB",
        "wfs_url": "https://geoaisweb.decea.mil.br/geoserver/wfs",
        "source_crs": "EPSG:4326",
        "layers": layers,
        "interpretation": {
            "vor": "coordinates, elevation and VOR carrier frequency are explicit; power and antenna height fields are empty",
            "ndb": "coordinates, NDB carrier frequency and partial elevation are explicit; emission bandwidth is almost entirely absent",
            "dme": "coordinates, partial elevation and channel are explicit; valghostfr is the paired VOR/ILS frequency, not the DME RF carrier",
            "navaids": "aggregate ILS/VOR-DME relation layer; coordinates are complete but elevation is partial and frequency is absent",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({name: item["feature_count"] for name, item in layers.items()}, indent=2))


if __name__ == "__main__":
    main()
