"""Audit the exact triangle contraction and its all-order limitation."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH238 = PAPERS / "RH-238-trace-adaptive-shell-selection"
sys.path.insert(0, str(ROOT / "src"))

from adaptive_jet import (  # noqa: E402
    complex_values,
    trace_jet_distance,
    triangle_tolerance_bound,
)


def strict_contraction(values: list[float], width: int = 4) -> bool:
    tail = values[-int(width):]
    return all(second < first for first, second in zip(tail[:-1], tail[1:]))


def run() -> dict[str, object]:
    source = json.loads(
        (RH238 / "results/adaptive_shell_selection.json").read_text(encoding="utf-8")
    )
    rows = source["endpoint_rows"]
    endpoint = {
        (float(row["sigma"]), str(row["side"])): row
        for row in rows if row["selection_pass"]
    }
    sigmas = sorted({key[0] for key in endpoint}, reverse=True)
    adjacent_rows = []
    channel_sequences = {}
    for side in ("left", "right"):
        sequence = []
        for coarse, fine in zip(sigmas[:-1], sigmas[1:]):
            first = endpoint[(coarse, side)]
            second = endpoint[(fine, side)]
            distance = trace_jet_distance(
                complex_values(first["adaptive_trace_powers"]),
                complex_values(second["adaptive_trace_powers"]),
            )
            bound = triangle_tolerance_bound(coarse, fine)
            sequence.append(distance)
            adjacent_rows.append({
                "side": side,
                "coarse_sigma": coarse,
                "fine_sigma": fine,
                "actual_trace_jet_distance": distance,
                "triangle_tolerance_bound": bound,
                "bound_slack": bound - distance,
            })
        channel_sequences[side] = {
            "actual_distance_sequence": sequence,
            "last_four_actual_distances_strictly_contract": strict_contraction(sequence),
        }
    channel_rows = []
    for sigma in sigmas:
        left = endpoint[(sigma, "left")]
        right = endpoint[(sigma, "right")]
        distance = trace_jet_distance(
            complex_values(left["adaptive_trace_powers"]),
            complex_values(right["adaptive_trace_powers"]),
        )
        bound = 2.0 * sigma
        channel_rows.append({
            "sigma": sigma,
            "actual_trace_jet_distance": distance,
            "two_sigma_bound": bound,
            "bound_slack": bound - distance,
        })
    return {
        "status": "rh239_adaptive_jet_contraction_obstruction",
        "maximum_order": source["maximum_order"],
        "adjacent_case_count": len(adjacent_rows),
        "channel_case_count": len(channel_rows),
        "minimum_adjacent_bound_slack": min(row["bound_slack"] for row in adjacent_rows),
        "minimum_channel_bound_slack": min(row["bound_slack"] for row in channel_rows),
        "maximum_actual_adjacent_distance": max(
            row["actual_trace_jet_distance"] for row in adjacent_rows
        ),
        "both_actual_tail_sequences_strictly_contract": all(
            row["last_four_actual_distances_strictly_contract"]
            for row in channel_sequences.values()
        ),
        "minimum_admissible_prefix_count": source["minimum_admissible_prefix_count"],
        "maximum_admissible_prefix_count": source["maximum_admissible_prefix_count"],
        "adjacent_rows": adjacent_rows,
        "channel_rows": channel_rows,
        "channel_sequences": channel_sequences,
        "theorem_boundary": {
            "epsilon_to_zero_implies_fixed_finite_jet_cauchy": True,
            "all_archived_triangle_bounds_pass": min(
                row["bound_slack"] for row in adjacent_rows + channel_rows
            ) >= -1.0e-12,
            "actual_adjacent_distances_monotone": all(
                row["last_four_actual_distances_strictly_contract"]
                for row in channel_sequences.values()
            ),
            "finite_jet_contraction_implies_full_det2_convergence": False,
            "deterministic_numerator_identified": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/adaptive_jet_contraction.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "minimum_adjacent_slack": payload["minimum_adjacent_bound_slack"],
        "minimum_channel_slack": payload["minimum_channel_bound_slack"],
        "actual_tail_contraction": payload["both_actual_tail_sequences_strictly_contract"],
        "admissible_prefix_range": [
            payload["minimum_admissible_prefix_count"],
            payload["maximum_admissible_prefix_count"],
        ],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
