from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH153 = PAPERS / "RH-153-congruence-covariant-reset-transport"
sys.path.insert(0, str(ROOT / "src"))

from delayed_suffix import common_suffix_floor, suffix_length, suffix_log_drawdown  # noqa: E402


def fraction_record(rows: list[dict[str, object]], fraction: float) -> dict[str, object]:
    chains = [[item["robust_overlap_lower"] for item in row["transitions"]] for row in rows]
    retained = []
    for row, chain in zip(rows, chains):
        length = suffix_length(len(chain), fraction)
        selected = row["transitions"][-length:]
        retained.append({
            "sigma": row["sigma"],
            "side": row["side"],
            "original_length": len(chain),
            "retained_length": length,
            "start_time": selected[0]["time"],
            "overlap_floor": min(item["robust_overlap_lower"] for item in selected),
            "inverse_overlap_upper": 1.0 / min(item["robust_overlap_lower"] for item in selected),
            "log_inverse_drawdown": suffix_log_drawdown(chain, fraction),
            "correlated_base_floor": min(item["correlated_pulled_base_lower"] for item in selected),
        })
    floor = common_suffix_floor(chains, fraction)
    return {
        "retained_fraction": fraction,
        "retained_transition_count": sum(item["retained_length"] for item in retained),
        "common_overlap_floor": floor,
        "common_inverse_overlap_upper": 1.0 / floor,
        "maximum_chain_log_inverse_drawdown": max(item["log_inverse_drawdown"] for item in retained),
        "minimum_correlated_base_floor": min(item["correlated_base_floor"] for item in retained),
        "channels": retained,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    source = json.loads((RH153 / "results/congruence_audit.json").read_text())
    rows = source["rows"][:2] if args.smoke else source["rows"]
    fractions = [round(value, 2) for value in np.linspace(0.05, 1.0, 20)]
    frontier = [fraction_record(rows, fraction) for fraction in fractions]
    half = fraction_record(rows, 0.5)
    full = fraction_record(rows, 1.0)

    threshold = 0.05
    threshold_channels = []
    for row in rows:
        values = [item["robust_overlap_lower"] for item in row["transitions"]]
        start = next(index for index in range(len(values)) if min(values[index:]) >= threshold)
        threshold_channels.append({
            "sigma": row["sigma"], "side": row["side"],
            "retained_length": len(values) - start,
            "retained_fraction": (len(values) - start) / len(values),
            "start_time": row["transitions"][start]["time"],
        })

    summary = {
        "channel_count": len(rows),
        "full_transition_count": full["retained_transition_count"],
        "half_suffix_transition_count": half["retained_transition_count"],
        "full_common_overlap_floor": full["common_overlap_floor"],
        "half_suffix_common_overlap_floor": half["common_overlap_floor"],
        "full_inverse_overlap_upper": full["common_inverse_overlap_upper"],
        "half_suffix_inverse_overlap_upper": half["common_inverse_overlap_upper"],
        "full_maximum_log_inverse_drawdown": full["maximum_chain_log_inverse_drawdown"],
        "half_suffix_maximum_log_inverse_drawdown": half["maximum_chain_log_inverse_drawdown"],
        "half_suffix_minimum_correlated_base_floor": half["minimum_correlated_base_floor"],
        "minimum_retained_fraction_at_overlap_0_05": min(item["retained_fraction"] for item in threshold_channels),
        "transition_count_at_overlap_0_05": sum(item["retained_length"] for item in threshold_channels),
    }
    payload = {
        "status": "rh154_half_horizon_delayed_reset_suffix",
        "frontier": frontier,
        "half_suffix": half,
        "full_atlas": full,
        "overlap_0_05_suffixes": threshold_channels,
        "audit_summary": summary,
        "theorem_boundary": {
            "finite_prefix_support_invariance": True,
            "finite_prefix_cocycle_invariance": True,
            "sharp_fixed_retention_suffix_floor": True,
            "half_suffix_frozen_certificate": not args.smoke,
            "uniform_all_level_suffix_floor": False,
            "native_reset_tail_assembly": False,
            "stage_A": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "Deleting a finite reset prefix does not change an eventual support or bounded-drawdown theorem. Retaining the terminal half of every frozen chain gives the sharp common overlap floor 0.06664 for that retention rule, reduces the inverse upper to 15.01 and the maximum log drawdown to 8.973, while preserving the positive correlated-base minimum. The next interface is the native reset Gram-tail pair.",
    }
    output = ROOT / "results" / ("suffix_smoke.json" if args.smoke else "suffix_audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
