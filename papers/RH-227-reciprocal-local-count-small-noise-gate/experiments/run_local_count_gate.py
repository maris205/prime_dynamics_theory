"""Test the finite reciprocal-zero count gate on predeclared disks."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path.insert(0, str(ROOT / "src"))

from local_count_gate import contour_clearance, disk_count, tail_is_constant  # noqa: E402


RADII = (1.2, 1.5, 2.0, 3.0, 5.0)
TAIL_WIDTH = 4


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    endpoint_rows = []
    for endpoint in source["endpoint_rows"]:
        zeros = values(endpoint["reciprocal_zeros"])
        endpoint_rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "rank": endpoint["actual_rank"],
            "radius_rows": [
                {
                    "radius": radius,
                    "strict_disk_count": disk_count(zeros, radius),
                    "contour_clearance": contour_clearance(zeros, radius),
                }
                for radius in RADII
            ],
        })
    channel_rows = []
    for side in ("left", "right"):
        endpoints = [row for row in endpoint_rows if row["side"] == side]
        radius_rows = []
        for radius in RADII:
            counts = [
                next(item["strict_disk_count"] for item in row["radius_rows"] if item["radius"] == radius)
                for row in endpoints
            ]
            clearances = [
                next(item["contour_clearance"] for item in row["radius_rows"] if item["radius"] == radius)
                for row in endpoints
            ]
            radius_rows.append({
                "radius": radius,
                "count_sequence": counts,
                "distinct_count_values": len(set(counts)),
                "first_to_last_count_growth": counts[-1] - counts[0],
                "last_four_levels_constant": tail_is_constant(counts, TAIL_WIDTH),
                "minimum_finite_contour_clearance": min(clearances),
            })
        channel_rows.append({
            "side": side,
            "radius_rows": radius_rows,
            "stable_radius_count_in_last_four_levels": sum(row["last_four_levels_constant"] for row in radius_rows),
            "all_radii_stable_in_last_four_levels": all(row["last_four_levels_constant"] for row in radius_rows),
        })
    all_radius_rows = [row for channel in channel_rows for row in channel["radius_rows"]]
    return {
        "status": "rh227_reciprocal_local_count_small_noise_gate",
        "radii": list(RADII),
        "tail_width": TAIL_WIDTH,
        "endpoint_count": len(endpoint_rows),
        "minimum_finite_contour_clearance": min(row["minimum_finite_contour_clearance"] for row in all_radius_rows),
        "maximum_first_to_last_count_growth": max(row["first_to_last_count_growth"] for row in all_radius_rows),
        "all_channel_radius_counts_stable_in_frozen_tail": all(channel["all_radii_stable_in_last_four_levels"] for channel in channel_rows),
        "channel_rows": channel_rows,
        "endpoint_rows": endpoint_rows,
        "theorem_boundary": {
            "rouche_count_stability_necessary_for_nonzero_local_uniform_limit": True,
            "finite_reciprocal_count_gate_passed": False,
            "eventual_count_stability_disproved": False,
            "small_noise_determinant_limit_disproved": False,
            "renormalized_relative_determinant_still_open": True,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/local_count_gate.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "minimum_clearance": payload["minimum_finite_contour_clearance"],
        "maximum_count_growth": payload["maximum_first_to_last_count_growth"],
        "all_tail_counts_stable": payload["all_channel_radius_counts_stable_in_frozen_tail"],
        "stable_radius_counts": [row["stable_radius_count_in_last_four_levels"] for row in payload["channel_rows"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
