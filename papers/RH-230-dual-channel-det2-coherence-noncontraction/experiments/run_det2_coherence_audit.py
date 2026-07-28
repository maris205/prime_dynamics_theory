"""Compare dual channels and adjacent scales on the closed unit disk grid."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path.insert(0, str(ROOT / "src"))

from det2_coherence import grid_sup_log_difference, strict_tail_contraction  # noqa: E402


GRID = np.concatenate([
    radius * np.exp(2j * np.pi * np.arange(64) / 64)
    for radius in (0.25, 0.5, 0.75, 1.0)
])
CHANNEL_GATE = 0.02
TAIL_WIDTH = 4


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    endpoints = {
        (float(row["sigma"]), str(row["side"])): values(row["selected_roots"])
        for row in source["endpoint_rows"]
    }
    sigmas = [float(value) for value in source["sigmas"]]
    channel_rows = []
    for sigma in sigmas:
        error = grid_sup_log_difference(endpoints[(sigma, "left")], endpoints[(sigma, "right")], GRID)
        channel_rows.append({
            "sigma": sigma,
            "unit_disk_grid_sup_log_difference": error,
            "channel_gate": error < CHANNEL_GATE,
        })
    adjacent_rows = []
    for side in ("left", "right"):
        for coarse, fine in zip(sigmas[:-1], sigmas[1:]):
            adjacent_rows.append({
                "side": side,
                "coarse_sigma": coarse,
                "fine_sigma": fine,
                "unit_disk_grid_sup_log_difference": grid_sup_log_difference(
                    endpoints[(coarse, side)], endpoints[(fine, side)], GRID
                ),
            })
    contraction = {}
    for side in ("left", "right"):
        errors = [row["unit_disk_grid_sup_log_difference"] for row in adjacent_rows if row["side"] == side]
        contraction[side] = {
            "adjacent_error_sequence": errors,
            "last_four_strictly_contracting": strict_tail_contraction(errors, TAIL_WIDTH),
            "minimum_adjacent_error": min(errors),
            "maximum_adjacent_error": max(errors),
            "final_adjacent_error": errors[-1],
        }
    return {
        "status": "rh230_dual_channel_det2_coherence_noncontraction",
        "grid_point_count": int(GRID.size),
        "channel_gate": CHANNEL_GATE,
        "tail_width": TAIL_WIDTH,
        "channel_case_count": len(channel_rows),
        "adjacent_case_count": len(adjacent_rows),
        "channel_gate_pass_count": sum(row["channel_gate"] for row in channel_rows),
        "maximum_channel_log_difference": max(row["unit_disk_grid_sup_log_difference"] for row in channel_rows),
        "minimum_adjacent_log_difference": min(row["unit_disk_grid_sup_log_difference"] for row in adjacent_rows),
        "maximum_adjacent_log_difference": max(row["unit_disk_grid_sup_log_difference"] for row in adjacent_rows),
        "all_channels_pass": all(row["channel_gate"] for row in channel_rows),
        "both_channels_strictly_contract_on_last_four_transitions": all(row["last_four_strictly_contracting"] for row in contraction.values()),
        "channel_rows": channel_rows,
        "adjacent_rows": adjacent_rows,
        "channel_contraction_rows": contraction,
        "theorem_boundary": {
            "branch_free_finite_det2_comparison": True,
            "finite_dual_channel_unit_disk_coherence": True,
            "cross_scale_det2_contraction": False,
            "locally_uniform_small_noise_determinant": False,
            "complement_ideal_control": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/det2_coherence_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "channel_passes": payload["channel_gate_pass_count"],
        "maximum_channel_error": payload["maximum_channel_log_difference"],
        "adjacent_error_range": [payload["minimum_adjacent_log_difference"], payload["maximum_adjacent_log_difference"]],
        "fine_tail_contraction": payload["both_channels_strictly_contract_on_last_four_transitions"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
