"""Audit naive prefixes and candidate-window stability of RH-222 clouds."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH222 / "src")]

from resonance_cloud import (  # noqa: E402
    conjugacy_error,
    conjugate_shells,
    select_shell_complete_cloud,
)
from shell_stability import multiset_matching_error  # noqa: E402


PREFIX_MARGINS = (4, 8, 12, 14)


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in source["endpoint_rows"]:
        candidates = values(endpoint["candidate_roots"])
        reference = values(endpoint["selected_roots"])
        target = int(endpoint["target_rank"])
        naive = candidates[:target]
        naive_error = conjugacy_error(naive)
        margin_rows = []
        for margin in PREFIX_MARGINS:
            prefix = candidates[: min(candidates.size, target + margin)]
            shells = conjugate_shells(prefix)
            candidate, _ = select_shell_complete_cloud(shells, target)
            margin_rows.append({
                "margin": margin,
                "prefix_count": int(prefix.size),
                "actual_rank": int(candidate.size),
                "matching_error_to_reference": multiset_matching_error(candidate, reference),
                "conjugacy_error": conjugacy_error(candidate),
            })
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "target_rank": target,
            "reference_rank": int(reference.size),
            "radial_gap_after_reference": endpoint["radial_gap_after_cloud"],
            "naive_prefix_conjugacy_error": naive_error,
            "naive_prefix_is_conjugate_closed": naive_error < 1.0e-8,
            "reference_rank_overshoot": int(reference.size) - target,
            "margin_rows": margin_rows,
        })
    margin_records = [item for row in rows for item in row["margin_rows"]]
    return {
        "status": "rh223_shell_complete_edge_selection_stability",
        "prefix_margins": list(PREFIX_MARGINS),
        "endpoint_count": len(rows),
        "naive_split_pair_count": sum(not row["naive_prefix_is_conjugate_closed"] for row in rows),
        "shell_completion_overshoot_count": sum(row["reference_rank_overshoot"] == 1 for row in rows),
        "maximum_shell_completion_overshoot": max(row["reference_rank_overshoot"] for row in rows),
        "minimum_reference_radial_gap": min(row["radial_gap_after_reference"] for row in rows),
        "maximum_margin_matching_error": max(item["matching_error_to_reference"] for item in margin_records),
        "maximum_margin_conjugacy_error": max(item["conjugacy_error"] for item in margin_records),
        "all_margin_prefixes_recover_reference": all(item["matching_error_to_reference"] < 1.0e-12 for item in margin_records),
        "endpoint_rows": rows,
        "theorem_boundary": {
            "minimal_shell_completion_exact": True,
            "positive_gap_uniqueness_within_resolved_window": True,
            "finite_candidate_margin_stability": True,
            "certified_infinite_spectrum_ordering": False,
            "canonical_rank_schedule": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/shell_stability_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "naive_split_pairs": payload["naive_split_pair_count"],
        "overshoots": payload["shell_completion_overshoot_count"],
        "maximum_margin_error": payload["maximum_margin_matching_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
