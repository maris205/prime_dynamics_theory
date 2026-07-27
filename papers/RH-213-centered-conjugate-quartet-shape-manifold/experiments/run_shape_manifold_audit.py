"""Audit the exact shape manifold on the frozen RH-212 quartet ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH212 = PAPERS / "RH-212-intrinsic-quartic-normalization-audit"
sys.path.insert(0, str(ROOT / "src"))

from quartet_shape import (  # noqa: E402
    coefficient_manifold_residual,
    coordinates_from_coefficients,
    coordinates_from_roots,
    shape_coefficients,
    shape_roots,
)


def complex_array(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH212 / "results/intrinsic_normalization_audit.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in source["endpoint_rows"]:
        roots = complex_array(endpoint["centered_rms_roots"])
        coefficients = complex_array(endpoint["centered_rms_coefficients"])
        shape = coordinates_from_roots(roots)
        reconstructed_coefficients = shape_coefficients(shape.u, shape.eta)
        reconstructed_roots = shape_roots(shape.u, shape.eta)
        inferred_u, inferred_eta = coordinates_from_coefficients(coefficients)
        rows.append({
            "sigma": float(endpoint["sigma"]),
            "side": str(endpoint["side"]),
            "u": shape.u,
            "eta": shape.eta,
            "a": shape.axial_coordinate,
            "b": shape.positive_imaginary_height,
            "d": shape.negative_imaginary_height,
            "c2": float(coefficients[2].real),
            "c3": float(coefficients[3].real),
            "c4": float(coefficients[4].real),
            "manifold_identity_residual": coefficient_manifold_residual(coefficients),
            "coefficient_reconstruction_error": float(np.max(np.abs(coefficients - reconstructed_coefficients))),
            "coordinate_reconstruction_error": float(max(abs(shape.u - inferred_u), abs(shape.eta - inferred_eta))),
            "root_multiset_reconstruction_error": float(max(
                min(abs(value - candidate) for candidate in reconstructed_roots) for value in roots
            )),
        })

    rng = np.random.default_rng(213)
    identity_rows = []
    for case in range(400):
        u = float(rng.uniform(1.0e-6, 1.0 - 1.0e-6))
        eta = float(rng.uniform(-1.0, 1.0))
        direct = np.poly(shape_roots(u, eta))
        formula = shape_coefficients(u, eta)
        recovered = coordinates_from_coefficients(formula)
        identity_rows.append({
            "case": case,
            "coefficient_error": float(np.max(np.abs(direct - formula))),
            "coordinate_error": float(max(abs(recovered[0] - u), abs(recovered[1] - eta))),
            "manifold_residual": coefficient_manifold_residual(formula),
        })
    return {
        "status": "rh213_centered_conjugate_quartet_shape_manifold",
        "finite_endpoint_count": len(rows),
        "random_identity_case_count": len(identity_rows),
        "maximum_endpoint_manifold_residual": max(row["manifold_identity_residual"] for row in rows),
        "maximum_endpoint_coefficient_reconstruction_error": max(row["coefficient_reconstruction_error"] for row in rows),
        "maximum_endpoint_coordinate_reconstruction_error": max(row["coordinate_reconstruction_error"] for row in rows),
        "maximum_random_coefficient_error": max(row["coefficient_error"] for row in identity_rows),
        "maximum_random_coordinate_error": max(row["coordinate_error"] for row in identity_rows),
        "shape_rows": rows,
        "identity_rows": identity_rows,
        "theorem_boundary": {
            "shape_parameterization_exact": True,
            "coefficient_relation_exact": True,
            "finite_quartets_on_shape_manifold": True,
            "scale_limit_exists": False,
            "dynamical_semigroup_identified": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/shape_manifold_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoint_residual": payload["maximum_endpoint_manifold_residual"],
        "random_coefficient_error": payload["maximum_random_coefficient_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
