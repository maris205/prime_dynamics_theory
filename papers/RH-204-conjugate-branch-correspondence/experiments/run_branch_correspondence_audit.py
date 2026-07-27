"""Audit two conjugate spectral branches across levels and channels."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
sys.path.insert(0, str(ROOT / "src"))

from branch_correspondence import branch_matching_data, synchronize_branches  # noqa: E402


SIGMAS = (0.04, 0.02, 0.01)


def values(row: dict[str, object]) -> np.ndarray:
    return np.asarray(row["quartet_values_real"]) + 1j * np.asarray(row["quartet_values_imag"])


def run() -> dict[str, object]:
    source = json.loads((RH202 / "results/adjacent_transport_audit.json").read_text(encoding="utf-8"))
    endpoint = {(float(row["sigma"]), str(row["side"])): values(row) for row in source["endpoint_rows"]}
    adjacent_rows = []
    for coarse, fine in zip(SIGMAS[:-1], SIGMAS[1:]):
        for side in ("left", "right"):
            row = branch_matching_data(endpoint[(coarse, side)], endpoint[(fine, side)])
            row.update({"coarse_sigma": coarse, "fine_sigma": fine, "side": side})
            adjacent_rows.append(row)
    synchronization_rows = []
    for sigma in SIGMAS:
        row = synchronize_branches(endpoint[(sigma, "left")], endpoint[(sigma, "right")])
        row["sigma"] = sigma
        synchronization_rows.append(row)

    first = {row["side"]: row for row in adjacent_rows if row["coarse_sigma"] == 0.04}
    second = {row["side"]: row for row in adjacent_rows if row["coarse_sigma"] == 0.02}
    contraction_rows = [{
        "side": side,
        "first_maximum_displacement": first[side]["maximum_branch_displacement"],
        "second_maximum_displacement": second[side]["maximum_branch_displacement"],
        "descriptive_displacement_ratio": second[side]["maximum_branch_displacement"] / first[side]["maximum_branch_displacement"],
    } for side in ("left", "right")]
    return {
        "status": "rh204_conjugate_branch_correspondence",
        "adjacent_case_count": len(adjacent_rows),
        "synchronization_case_count": len(synchronization_rows),
        "unique_assignment_case_count": sum(bool(row["real_order_assignment_unique"]) for row in adjacent_rows),
        "minimum_assignment_cost_margin": min(float(row["assignment_cost_margin"]) for row in adjacent_rows),
        "minimum_pointwise_assignment_margin": min(float(row["minimum_pointwise_assignment_margin"]) for row in adjacent_rows),
        "maximum_adjacent_branch_displacement": max(float(row["maximum_branch_displacement"]) for row in adjacent_rows),
        "maximum_left_right_branch_mismatch": max(float(row["maximum_branch_mismatch"]) for row in synchronization_rows),
        "maximum_descriptive_displacement_ratio": max(float(row["descriptive_displacement_ratio"]) for row in contraction_rows),
        "adjacent_rows": adjacent_rows,
        "synchronization_rows": synchronization_rows,
        "contraction_rows": contraction_rows,
        "theorem_boundary": {
            "conjugate_representative_reduction": True,
            "finite_unique_branch_correspondence": True,
            "same_branch_labels_both_channels": True,
            "finite_left_right_synchronization": True,
            "asymptotic_branch_convergence": False,
            "all_level_edge_gap": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/branch_correspondence_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "unique_cases": payload["unique_assignment_case_count"],
        "max_channel_mismatch": payload["maximum_left_right_branch_mismatch"],
        "max_displacement_ratio": payload["maximum_descriptive_displacement_ratio"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
