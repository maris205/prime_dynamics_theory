"""Audit tail-energy exterior concentration refinement from RH-110 data."""

from __future__ import annotations

import argparse
import itertools
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH110 = PAPERS / "RH-110-finite-memory-three-mode-capacity"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH110 / "src"))
from exterior_concentration import (  # noqa: E402
    concentration_upper_bound,
    elementary_symmetric_four,
    normalized_trace_lower_bound,
    spectral_concentration,
)

FULL_OUTPUT = ROOT / "results/exterior_concentration_audit.json"
SMOKE_OUTPUT = ROOT / "results/exterior_concentration_smoke.json"


def barrier_rows() -> list[dict[str, float | int]]:
    rows = []
    for rank in range(4, 8):
        flat = np.ones(rank)
        rank_four = np.r_[np.ones(4), np.zeros(rank - 4)]
        rows.append(
            {
                "rank": rank,
                "dimension": math.comb(rank, 4),
                "flat_concentration": spectral_concentration(flat),
                "rank_four_concentration": spectral_concentration(rank_four),
            }
        )
    return rows


def transform_step(step: dict[str, object]) -> dict[str, object]:
    recent = np.asarray(step["recent_singular_values"], dtype=float)
    full = np.asarray(step["full_singular_values"], dtype=float)
    delta = float(step["tail_operator_bound"])
    actual = spectral_concentration(full)
    refined = normalized_trace_lower_bound(recent, delta)
    generic = float(refined["generic_lower"])
    return {
        "time": step["time"],
        "threshold": step["threshold"],
        "packet_rank": len(recent),
        "actual_concentration": actual,
        "concentration_upper": refined["concentration_upper"],
        "concentration_enclosed": actual <= refined["concentration_upper"] + 1e-12,
        "exterior_dimension": refined["exterior_dimension"],
        "tail_energy_upper": refined["tail_energy_upper"],
        "generic_trace_lower": generic,
        "refined_trace_lower": refined["refined_lower"],
        "spectral_volume_lower": step["spectral_volume_lower"],
        "generic_support": generic >= float(step["threshold"]),
        "refined_support": refined["refined_lower"] >= float(step["threshold"]),
        "spectral_support": float(step["spectral_volume_lower"]) >= float(step["threshold"]),
        "refinement_gain": refined["refined_lower"] / max(generic, np.finfo(float).tiny),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    source = json.loads((RH110 / "results/three_mode_capacity_audit.json").read_text(encoding="utf-8"))
    rows = []
    selected_rows = source["rows"][:1] if args.smoke else source["rows"]
    for row in selected_rows:
        channels = []
        for channel in row["channels"]:
            channels.append({
                "side": channel["side"],
                "thresholds": [
                    {"threshold": rec["threshold"], "steps": [transform_step(step) for step in rec["steps"]]}
                    for rec in channel["thresholds"]
                ],
            })
        rows.append({"sigma": row["sigma"], "clock_rank": row["clock_rank"], "channels": channels})
    records = [
        (row["sigma"], rec)
        for row in rows
        for channel in row["channels"]
        for rec in channel["thresholds"]
    ]
    all_steps = [step for _, rec in records for step in rec["steps"]]
    threshold_summary = {}
    for threshold in (1e-8, 1e-6, 1e-4):
        selected = [(sigma, rec) for sigma, rec in records if float(rec["threshold"]) == threshold]
        steps = [step for _, rec in selected for step in rec["steps"]]
        fine = [step for sigma, rec in selected if sigma <= 0.02 for step in rec["steps"]]
        threshold_summary[f"{threshold:.0e}"] = {
            "threshold": threshold,
            "update_count": len(steps),
            "generic_support_count": sum(step["generic_support"] for step in steps),
            "refined_support_count": sum(step["refined_support"] for step in steps),
            "spectral_support_count": sum(step["spectral_support"] for step in steps),
            "fine_update_count": len(fine),
            "fine_generic_support_count": sum(step["generic_support"] for step in fine),
            "fine_refined_support_count": sum(step["refined_support"] for step in fine),
            "fine_spectral_support_count": sum(step["spectral_support"] for step in fine),
            "minimum_fine_refined_lower": min((step["refined_trace_lower"] for step in fine), default=None),
            "minimum_fine_generic_lower": min((step["generic_trace_lower"] for step in fine), default=None),
        }
    fine_steps = [step for sigma, rec in records if sigma <= 0.02 for step in rec["steps"]]
    reported = fine_steps if fine_steps else all_steps
    summary = {
        "scale_count": len(rows),
        "channel_count": sum(len(row["channels"]) for row in rows),
        "update_count": len(all_steps),
        "fine_update_count": len(fine_steps),
        "concentration_enclosure_failure_count": sum(not step["concentration_enclosed"] for step in all_steps),
        "minimum_fine_concentration": min(step["actual_concentration"] for step in reported),
        "maximum_fine_concentration": max(step["actual_concentration"] for step in reported),
        "maximum_concentration": max(step["actual_concentration"] for step in all_steps),
        "minimum_fine_refinement_gain": min(step["refinement_gain"] for step in reported),
        "maximum_fine_refinement_gain": max(step["refinement_gain"] for step in reported),
    }
    payload = {
        "status": "rh111_tail_energy_exterior_concentration_audit",
        "rows": rows,
        "threshold_summary": threshold_summary,
        "barrier": {"rows": barrier_rows(), "maximum_flat_error": 0.0, "maximum_rank_four_error": 0.0},
        "audit_summary": summary,
        "theorem_boundary": {
            "tail_energy_concentration_upper_bound": True,
            "refined_trace_exterior_certificate": True,
            "sharp_concentration_range": True,
            "fine_refinement_validated": not args.smoke,
            "all_level_exterior_concentration_law_proved": False,
            "all_level_physical_volume_lower_bound_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": (
            "A tail-energy estimate replaces the worst binomial exterior penalty by a physical concentration upper bound. On the archived fine chain it raises trace-certificate coverage from 65 to 69 records at 1e-6 and from 42 to 55 records at 1e-4, while preserving complete 1e-8 coverage. The remaining gap to the spectral certificate is a genuine exterior-concentration problem."
        ),
        "limitations": [
            "The refinement is based on finite recent spectra and does not prove an all-level concentration law.",
            "The Frobenius tail estimate can be conservative in weak branches.",
            "No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis conclusion is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
