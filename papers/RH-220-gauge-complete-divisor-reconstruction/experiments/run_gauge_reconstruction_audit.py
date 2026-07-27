"""Reconstruct every raw quartet and decide the next Gate-A subroute."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH212 = PAPERS / "RH-212-intrinsic-quartic-normalization-audit"
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from gauge_divisor import (  # noqa: E402
    coefficient_path_decomposition,
    gauge_shape_parameters,
    raw_coefficients,
    raw_roots,
    route_coordinate,
)


def complex_array(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def matching_error(first: np.ndarray, second: np.ndarray) -> float:
    return float(min(max(abs(first[index] - second[target]) for index, target in enumerate(order)) for order in itertools.permutations(range(4))))


def run() -> dict[str, object]:
    source = json.loads((RH212 / "results/intrinsic_normalization_audit.json").read_text(encoding="utf-8"))
    shape_source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    shape = {(float(row["sigma"]), str(row["side"])): row for row in shape_source["shape_rows"]}
    rows = []
    parameters = {}
    for endpoint in source["endpoint_rows"]:
        sigma = float(endpoint["sigma"])
        side = str(endpoint["side"])
        values = complex_array(endpoint["roots"])
        coefficients = complex_array(endpoint["raw_coefficients"])
        recovered = gauge_shape_parameters(values)
        u = float(shape[(sigma, side)]["u"])
        eta = float(shape[(sigma, side)]["eta"])
        center = complex(endpoint["center"]["real"], endpoint["center"]["imag"])
        radius = float(endpoint["centered_rms_radius"])
        reconstructed_roots = raw_roots(center, radius, u, eta)
        reconstructed_coefficients = raw_coefficients(center, radius, u, eta)
        parameters[(sigma, side)] = (center, radius, u, eta)
        rows.append({
            "sigma": sigma,
            "side": side,
            "center_real": center.real,
            "center_imag": center.imag,
            "radius": radius,
            "u": u,
            "eta": eta,
            "root_reconstruction_error": matching_error(values, reconstructed_roots),
            "coefficient_reconstruction_error": float(np.max(np.abs(coefficients - reconstructed_coefficients))),
            "parameter_recovery_error": float(max(
                abs(complex(recovered["center"]) - center),
                abs(float(recovered["radius"]) - radius),
                abs(float(recovered["u"]) - u),
                abs(float(recovered["eta"]) - eta),
            )),
        })
    sigmas = sorted({row["sigma"] for row in rows}, reverse=True)
    transition_rows = []
    for coarse, fine in zip(sigmas[:-1], sigmas[1:]):
        for side in ("left", "right"):
            decomposition = coefficient_path_decomposition(parameters[(coarse, side)], parameters[(fine, side)])
            transition_rows.append({"coarse_sigma": coarse, "fine_sigma": fine, "side": side, **decomposition})
    channel_rows = []
    for sigma in sigmas:
        left = parameters[(sigma, "left")]
        right = parameters[(sigma, "right")]
        channel_rows.append({
            "sigma": sigma,
            "center_discrepancy": float(abs(left[0] - right[0])),
            "radius_discrepancy": float(abs(left[1] - right[1])),
            "u_discrepancy": float(abs(left[2] - right[2])),
            "eta_discrepancy": float(abs(left[3] - right[3])),
        })
    statuses = {
        "shape_manifold_exact": True,
        "gauge_reconstruction_exact": True,
        "simple_recurrence_rejected": True,
        "fixed_quartic_counting_rejected": True,
        "rank_growing_divisor_constructed": False,
    }
    return {
        "status": "rh220_gauge_complete_divisor_reconstruction",
        "route_coordinate": route_coordinate(statuses),
        "statuses": statuses,
        "endpoint_rows": rows,
        "transition_rows": transition_rows,
        "channel_rows": channel_rows,
        "maximum_root_reconstruction_error": max(row["root_reconstruction_error"] for row in rows),
        "maximum_coefficient_reconstruction_error": max(row["coefficient_reconstruction_error"] for row in rows),
        "maximum_parameter_recovery_error": max(row["parameter_recovery_error"] for row in rows),
        "maximum_path_telescoping_residual": max(row["telescoping_residual"] for row in transition_rows),
        "gauge_dominant_transition_count": sum(row["gauge_leg_norm"] > row["shape_leg_norm"] for row in transition_rows),
        "shape_dominant_transition_count": sum(row["shape_leg_norm"] >= row["gauge_leg_norm"] for row in transition_rows),
        "theorem_boundary": {
            "affine_gauge_reconstruction_exact": True,
            "shape_only_map_noninjective": True,
            "finite_dual_channel_gauge_ledger": True,
            "rank_growing_divisor_constructed": False,
            "locally_uniform_determinant_limit": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/gauge_reconstruction_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "coefficient_error": payload["maximum_coefficient_reconstruction_error"],
        "gauge_dominant": payload["gauge_dominant_transition_count"],
        "shape_dominant": payload["shape_dominant_transition_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
