"""Test scalar versus branch-diagonal renormalization of physical residues."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
sys.path.insert(0, str(ROOT / "src"))

from residue_cocycle import diagonal_multipliers, optimal_common_scalar  # noqa: E402


def complex_from(mode: dict[str, object], prefix: str) -> complex:
    return complex(float(mode[f"{prefix}_real"]), float(mode[f"{prefix}_imag"]))


def upper_branch_rows(record: dict[str, object]) -> list[dict[str, object]]:
    rows = []
    for mode in record["modes"]:
        eigenvalue = complex_from(mode, "coarse_eigenvalue")
        if eigenvalue.imag > 0.0:
            rows.append({
                "coarse_eigenvalue": eigenvalue,
                "coarse_residue": complex_from(mode, "coarse_residue"),
                "fine_residue": complex_from(mode, "fine_residue"),
            })
    return sorted(rows, key=lambda row: row["coarse_eigenvalue"].real)


def fields(prefix: str, value: complex) -> dict[str, float]:
    return {f"{prefix}_real": float(value.real), f"{prefix}_imag": float(value.imag), f"{prefix}_modulus": float(abs(value))}


def run() -> dict[str, object]:
    source = json.loads((RH202 / "results/adjacent_transport_audit.json").read_text(encoding="utf-8"))
    rows = []
    branch_lookup = {}
    for record in source["records"]:
        coarse = np.asarray([complex_from(mode, "coarse_residue") for mode in record["modes"]])
        fine = np.asarray([complex_from(mode, "fine_residue") for mode in record["modes"]])
        multipliers = diagonal_multipliers(coarse, fine)
        scalar = optimal_common_scalar(coarse, fine)
        diagonal_residual = float(np.linalg.norm(fine - multipliers * coarse) / np.linalg.norm(fine))
        conjugate_errors = [float(np.min(np.abs(multipliers - np.conj(value)))) for value in multipliers]
        branches = upper_branch_rows(record)
        upper_multipliers = [row["fine_residue"] / row["coarse_residue"] for row in branches]
        key = (float(record["coarse_sigma"]), str(record["side"]))
        branch_lookup[key] = upper_multipliers
        row = {
            "side": record["side"],
            "coarse_sigma": record["coarse_sigma"],
            "fine_sigma": record["fine_sigma"],
            **fields("optimal_common_scalar", complex(scalar["scalar"])),
            "common_scalar_relative_residual": scalar["relative_residual"],
            "diagonal_cocycle_relative_residual": diagonal_residual,
            "maximum_conjugate_multiplier_error": max(conjugate_errors),
            "upper_branch_multipliers": [fields("multiplier", value) for value in upper_multipliers],
        }
        rows.append(row)

    channel_rows = []
    for coarse_sigma in (0.04, 0.02):
        left = branch_lookup[(coarse_sigma, "left")]
        right = branch_lookup[(coarse_sigma, "right")]
        mismatches = [abs(a - b) for a, b in zip(left, right)]
        channel_rows.append({
            "coarse_sigma": coarse_sigma,
            "fine_sigma": coarse_sigma / 2.0,
            "branch_multiplier_mismatches": [float(value) for value in mismatches],
            "maximum_branch_multiplier_mismatch": float(max(mismatches)),
        })

    telescoping_rows = []
    for side in ("left", "right"):
        first = branch_lookup[(0.04, side)]
        second = branch_lookup[(0.02, side)]
        products = [a * b for a, b in zip(first, second)]
        telescoping_rows.append({
            "side": side,
            "two_step_multipliers": [fields("multiplier", value) for value in products],
            "cocycle_composition_is_exact_by_construction": True,
        })
    return {
        "status": "rh206_residue_cocycle_renormalization_obstruction",
        "adjacent_case_count": len(rows),
        "maximum_common_scalar_relative_residual": max(float(row["common_scalar_relative_residual"]) for row in rows),
        "minimum_common_scalar_relative_residual": min(float(row["common_scalar_relative_residual"]) for row in rows),
        "maximum_diagonal_cocycle_relative_residual": max(float(row["diagonal_cocycle_relative_residual"]) for row in rows),
        "maximum_conjugate_multiplier_error": max(float(row["maximum_conjugate_multiplier_error"]) for row in rows),
        "maximum_left_right_multiplier_mismatch": max(float(row["maximum_branch_multiplier_mismatch"]) for row in channel_rows),
        "rows": rows,
        "channel_rows": channel_rows,
        "telescoping_rows": telescoping_rows,
        "theorem_boundary": {
            "residue_gauge_invariance": True,
            "exact_diagonal_residue_cocycle": True,
            "finite_common_scalar_obstruction": True,
            "conjugate_pair_cocycle_symmetry": True,
            "source_independent_cocycle": False,
            "all_level_residue_lower_bound": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/residue_cocycle_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "scalar_residual_max": payload["maximum_common_scalar_relative_residual"],
        "diagonal_residual_max": payload["maximum_diagonal_cocycle_relative_residual"],
        "channel_mismatch_max": payload["maximum_left_right_multiplier_mismatch"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
