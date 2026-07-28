"""Reconnect the rank-growing resonance atlas to the fixed-noise det2 variable."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path.insert(0, str(ROOT / "src"))

from fredholm_dictionary import (  # noqa: E402
    reciprocal_polynomial_identity_error,
    reciprocal_zeros,
    regularized_fredholm_product,
)


GRID = tuple(
    radius * np.exp(2j * np.pi * index / 24)
    for radius in (0.25, 0.5, 0.75, 1.0)
    for index in range(24)
)


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def conjugacy_error(roots: np.ndarray) -> float:
    return float(max(np.min(np.abs(roots - np.conj(value))) for value in roots))


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in source["endpoint_rows"]:
        resonances = values(endpoint["selected_roots"])
        zeros = reciprocal_zeros(resonances)
        identity_errors = [reciprocal_polynomial_identity_error(resonances, z) for z in GRID]
        raw_zero_residuals = [abs(regularized_fredholm_product(resonances, zero)) for zero in zeros]
        factor_residuals = [float(np.min(np.abs(1.0 - zero * resonances))) for zero in zeros]
        archived_zeros = values(endpoint["reciprocal_zeros"])
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "rank": endpoint["actual_rank"],
            "maximum_reciprocal_polynomial_identity_error": max(identity_errors),
            "maximum_fredholm_zero_factor_residual": max(factor_residuals),
            "maximum_raw_det2_zero_evaluation_residual": max(raw_zero_residuals),
            "maximum_archived_reciprocal_error": float(np.max(np.abs(zeros - archived_zeros))),
            "reciprocal_conjugacy_error": conjugacy_error(zeros),
            "minimum_reciprocal_modulus": float(np.min(np.abs(zeros))),
            "maximum_reciprocal_modulus": float(np.max(np.abs(zeros))),
            "all_reciprocal_zeros_outside_unit_disk": bool(np.min(np.abs(zeros)) > 1.0),
        })
    return {
        "status": "rh226_reciprocal_resonance_fredholm_dictionary",
        "endpoint_count": len(rows),
        "grid_point_count": len(GRID),
        "maximum_reciprocal_polynomial_identity_error": max(row["maximum_reciprocal_polynomial_identity_error"] for row in rows),
        "maximum_fredholm_zero_factor_residual": max(row["maximum_fredholm_zero_factor_residual"] for row in rows),
        "maximum_raw_det2_zero_evaluation_residual": max(row["maximum_raw_det2_zero_evaluation_residual"] for row in rows),
        "maximum_archived_reciprocal_error": max(row["maximum_archived_reciprocal_error"] for row in rows),
        "maximum_reciprocal_conjugacy_error": max(row["reciprocal_conjugacy_error"] for row in rows),
        "minimum_reciprocal_modulus": min(row["minimum_reciprocal_modulus"] for row in rows),
        "maximum_reciprocal_modulus": max(row["maximum_reciprocal_modulus"] for row in rows),
        "all_reciprocal_zeros_outside_unit_disk": all(row["all_reciprocal_zeros_outside_unit_disk"] for row in rows),
        "endpoint_rows": rows,
        "theorem_boundary": {
            "finite_reciprocal_polynomial_identity": True,
            "det2_zeros_are_reciprocal_resonances": True,
            "fixed_noise_hilbert_schmidt_det2_inherited_from_RH7": True,
            "small_noise_local_uniform_limit": False,
            "self_adjoint_energy_interpretation": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/fredholm_dictionary_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "identity_error": payload["maximum_reciprocal_polynomial_identity_error"],
        "zero_factor_residual": payload["maximum_fredholm_zero_factor_residual"],
        "raw_zero_evaluation_residual": payload["maximum_raw_det2_zero_evaluation_residual"],
        "reciprocal_range": [payload["minimum_reciprocal_modulus"], payload["maximum_reciprocal_modulus"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
