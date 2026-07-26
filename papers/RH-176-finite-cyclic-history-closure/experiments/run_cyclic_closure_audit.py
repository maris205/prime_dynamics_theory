"""Audit exact cyclic determinant and local-vs-norm closure behavior."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cyclic_history import cycle_matrix, geometric_section, reduced_cycle_determinant  # noqa: E402


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(176)
    lengths = (3, 5) if smoke else (3, 4, 5, 8, 12, 16, 24, 32, 48, 64)
    trials = 3 if smoke else 24
    determinant_records = []
    closure_records = []
    for length in lengths:
        forward = cycle_matrix(length)
        truncated_shift = forward.copy()
        truncated_shift[0, -1] = 0.0
        vector = np.zeros(length, dtype=complex)
        support = min(3, length - 1)
        vector[:support] = rng.normal(size=support) + 1j * rng.normal(size=support)
        closure_records.append({
            "length": length,
            "operator_norm_wrap_defect": float(np.linalg.norm(forward - truncated_shift, 2)),
            "fixed_support_action_defect": float(np.linalg.norm((forward - truncated_shift) @ vector)),
            "support_size": support,
        })
        for trial in range(trials):
            value = 0.75 * np.exp(2j * np.pi * rng.random()) * rng.random() ** 0.5
            observed = reduced_cycle_determinant(length, value)
            expected = geometric_section(length - 1, value)
            reverse = reduced_cycle_determinant(length, value, direction=-1)
            scale = max(1.0, abs(expected))
            determinant_records.append({
                "length": length,
                "trial": trial,
                "relative_geometric_identity_error": abs(observed - expected) / scale,
                "relative_orientation_determinant_error": abs(observed - reverse) / scale,
            })
    return {
        "status": "rh176_finite_cyclic_history_closure_audit",
        "determinant_case_count": len(determinant_records),
        "maximum_geometric_identity_error": max(record["relative_geometric_identity_error"] for record in determinant_records),
        "maximum_orientation_determinant_error": max(record["relative_orientation_determinant_error"] for record in determinant_records),
        "all_wrap_norm_defects_one": all(abs(record["operator_norm_wrap_defect"] - 1.0) < 1e-14 for record in closure_records),
        "all_fixed_support_defects_zero": all(record["fixed_support_action_defect"] == 0.0 for record in closure_records),
        "determinant_records": determinant_records,
        "closure_records": closure_records,
        "theorem_boundary": {
            "exact_reduced_cycle_determinant": True,
            "strong_local_shift_approximation": True,
            "operator_norm_shift_approximation": False,
            "physical_cycle_selection": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "cyclic_closure_smoke.json" if args.smoke else "cyclic_closure_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "case_count": payload["determinant_case_count"], "maximum_identity_error": payload["maximum_geometric_identity_error"]}, sort_keys=True))


if __name__ == "__main__":
    main()
