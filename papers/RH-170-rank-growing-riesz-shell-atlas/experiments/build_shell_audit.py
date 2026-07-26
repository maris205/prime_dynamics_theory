"""Exact diagonal audit of the rank wall and shellwise workaround."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from riesz_shells import finite_partial_cloud, rank_change_norm_floor, shell_tail_bound  # noqa: E402


def main() -> None:
    dimension = 64
    global_distances = []
    rank_floor_failures = 0
    for rank in range(1, dimension):
        p = np.diag([1.0] * rank + [0.0] * (dimension - rank))
        q = np.diag([1.0] * (rank + 1) + [0.0] * (dimension - rank - 1))
        distance = float(np.linalg.norm(q - p, 2))
        global_distances.append(distance)
        rank_floor_failures += int(distance + 1e-15 < rank_change_norm_floor(rank, rank + 1))
    shell_records = []
    for shell in range(1, 9):
        steps = [2.0 ** (-(j + shell)) for j in range(1, 33)]
        shell_records.append({"shell": shell, **shell_tail_bound(steps), **finite_partial_cloud([1] * shell)})
    payload = {
        "status": "rh170_rank_growing_riesz_shell_audit",
        "scale_count": dimension,
        "rank_change_count": len(global_distances),
        "rank_floor_failure_count": rank_floor_failures,
        "minimum_global_rank_change_distance": min(global_distances),
        "maximum_global_rank_change_distance": max(global_distances),
        "shell_records": shell_records,
        "theorem_boundary": {
            "rank_change_norm_obstruction": True,
            "shellwise_summable_limit": True,
            "bounded_infinite_cloud_projection": False,
            "physical_shell_summability": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "shell_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "failures": rank_floor_failures}, sort_keys=True))


if __name__ == "__main__":
    main()
