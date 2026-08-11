#!/usr/bin/env python3
"""Solve minimum-cardinality RADOME site selection from a candidate graph.

The geospatial stage produces a JSON instance containing coverage cells and
peer line-of-sight edges.  This module deliberately has no GIS dependency: it
solves and audits the discrete optimization after terrain calculations finish.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    covers: frozenset[str]
    peer_los: frozenset[str]
    peer_los_exempt: bool
    score: float


def load_instance(path: Path) -> tuple[list[Candidate], set[str]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cells = set(raw["required_cells"])
    candidates = [
        Candidate(
            candidate_id=item["id"],
            covers=frozenset(item.get("covers", [])),
            peer_los=frozenset(item.get("peer_los", [])),
            peer_los_exempt=bool(item.get("peer_los_exempt", False)),
            score=float(item.get("score", 0.0)),
        )
        for item in raw["candidates"]
    ]
    if len({candidate.candidate_id for candidate in candidates}) != len(candidates):
        raise ValueError("candidate IDs must be unique")
    unknown = set().union(*(candidate.covers for candidate in candidates)) - cells
    if unknown:
        raise ValueError(f"coverage references unknown cells: {sorted(unknown)}")
    return candidates, cells


def solve(candidates: list[Candidate], required_cells: set[str]) -> dict[str, Any]:
    """Minimize site count, using candidate score only as a tie-breaker."""
    if not candidates:
        raise ValueError("at least one candidate is required")
    if not required_cells:
        raise ValueError("at least one required coverage cell is required")

    by_id = {candidate.candidate_id: index for index, candidate in enumerate(candidates)}
    uncovered = {
        cell for cell in required_cells
        if not any(cell in candidate.covers for candidate in candidates)
    }
    if uncovered:
        raise ValueError(f"cells have no candidate coverage: {sorted(uncovered)}")

    rows = len(required_cells) + sum(not c.peer_los_exempt for c in candidates)
    matrix = lil_matrix((rows, len(candidates)), dtype=float)
    lower = np.full(rows, -np.inf)
    upper = np.full(rows, np.inf)

    row = 0
    for cell in sorted(required_cells):
        for index, candidate in enumerate(candidates):
            if cell in candidate.covers:
                matrix[row, index] = 1.0
        lower[row] = 1.0
        row += 1

    # x_i <= sum(x_j for visible peers). Island candidates are exempt.
    for index, candidate in enumerate(candidates):
        if candidate.peer_los_exempt:
            continue
        matrix[row, index] = 1.0
        for peer_id in candidate.peer_los:
            if peer_id not in by_id:
                raise ValueError(f"{candidate.candidate_id} references unknown peer {peer_id}")
            matrix[row, by_id[peer_id]] -= 1.0
        upper[row] = 0.0
        row += 1

    scores = np.array([candidate.score for candidate in candidates], dtype=float)
    score_span = float(np.ptp(scores))
    normalized = (scores - scores.min()) / score_span if score_span else np.zeros_like(scores)
    # The total tie-break contribution remains below one site, preserving the
    # cardinality objective exactly.
    objective = np.ones(len(candidates)) - normalized / (len(candidates) + 1.0)
    result = milp(
        c=objective,
        integrality=np.ones(len(candidates)),
        bounds=Bounds(0.0, 1.0),
        constraints=LinearConstraint(matrix.tocsr(), lower, upper),
        options={"disp": False},
    )
    if not result.success or result.x is None:
        raise RuntimeError(f"site-selection optimization failed: {result.message}")

    selected = [
        candidate for candidate, value in zip(candidates, result.x, strict=True)
        if value >= 0.5
    ]
    covered = set().union(*(candidate.covers for candidate in selected))
    return {
        "status": "optimal",
        "site_count": len(selected),
        "selected_ids": [candidate.candidate_id for candidate in selected],
        "covered_cell_count": len(covered),
        "required_cell_count": len(required_cells),
        "coverage_fraction": len(covered & required_cells) / len(required_cells),
        "selected_score_sum": sum(candidate.score for candidate in selected),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    candidates, required_cells = load_instance(args.instance)
    solution = solve(candidates, required_cells)
    encoded = json.dumps(solution, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
