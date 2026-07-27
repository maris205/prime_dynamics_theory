"""Compare the quartet divisor across physical channels and scales."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
sys.path.insert(0, str(ROOT / "src"))

from quartic_flow import coefficient_comparison, monic_coefficients, newton_traces  # noqa: E402


SIGMAS = (0.04, 0.02, 0.01)


def values(row: dict[str, object]) -> np.ndarray:
    return np.asarray(row["quartet_values_real"]) + 1j * np.asarray(row["quartet_values_imag"])


def complex_list(array: np.ndarray) -> dict[str, list[float]]:
    return {
        "real": [float(value.real) for value in array],
        "imag": [float(value.imag) for value in array],
    }


def run() -> dict[str, object]:
    source = json.loads((RH202 / "results/adjacent_transport_audit.json").read_text(encoding="utf-8"))
    endpoint = {(float(row["sigma"]), str(row["side"])): values(row) for row in source["endpoint_rows"]}
    channel_rows = []
    for sigma in SIGMAS:
        left = endpoint[(sigma, "left")]
        right = endpoint[(sigma, "right")]
        comparison = coefficient_comparison(left, right)
        left_coeff = monic_coefficients(left)
        right_coeff = monic_coefficients(right)
        left_traces = newton_traces(left_coeff, 8)
        right_traces = newton_traces(right_coeff, 8)
        channel_rows.append({
            "sigma": sigma,
            **comparison,
            "left_coefficients": complex_list(left_coeff),
            "right_coefficients": complex_list(right_coeff),
            "maximum_trace_difference_through_power_eight": float(np.max(np.abs(left_traces - right_traces))),
        })

    scale_rows = []
    for coarse, fine in zip(SIGMAS[:-1], SIGMAS[1:]):
        for side in ("left", "right"):
            comparison = coefficient_comparison(endpoint[(fine, side)], endpoint[(coarse, side)])
            comparison.update({"coarse_sigma": coarse, "fine_sigma": fine, "side": side})
            scale_rows.append(comparison)

    rng = np.random.default_rng(207)
    identity_rows = []
    for case in range(120):
        roots = rng.normal(size=4) + 1j * rng.normal(size=4)
        coefficients = monic_coefficients(roots)
        reconstructed = newton_traces(coefficients, 10)
        direct = np.asarray([np.sum(roots**power) for power in range(1, 11)])
        identity_rows.append({
            "case": case,
            "maximum_newton_identity_error": float(np.max(np.abs(reconstructed - direct))),
        })
    determinant_errors = [float(row["constant_term_relative_error"]) for row in channel_rows]
    return {
        "status": "rh207_dual_channel_quartic_divisor_flow",
        "channel_case_count": len(channel_rows),
        "scale_transition_count": len(scale_rows),
        "newton_identity_case_count": len(identity_rows),
        "newton_identity_failure_count": sum(row["maximum_newton_identity_error"] > 1e-8 for row in identity_rows),
        "maximum_newton_identity_error": max(float(row["maximum_newton_identity_error"]) for row in identity_rows),
        "maximum_left_right_coefficient_relative_error": max(float(row["relative_l2_error"]) for row in channel_rows),
        "maximum_left_right_constant_term_relative_error": max(determinant_errors),
        "finest_left_right_constant_term_relative_error": determinant_errors[-1],
        "maximum_adjacent_scale_coefficient_relative_error": max(float(row["relative_l2_error"]) for row in scale_rows),
        "minimum_adjacent_scale_coefficient_relative_error": min(float(row["relative_l2_error"]) for row in scale_rows),
        "channel_rows": channel_rows,
        "scale_rows": scale_rows,
        "identity_rows": identity_rows,
        "theorem_boundary": {
            "quartic_divisor_similarity_invariant": True,
            "newton_trace_equivalence": True,
            "finite_dual_channel_coherence": True,
            "finite_scale_flow_nonstationary": True,
            "coefficient_limit_exists": False,
            "fredholm_determinant_constructed": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/quartic_divisor_flow.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "channel_error_max": payload["maximum_left_right_coefficient_relative_error"],
        "scale_flow_max": payload["maximum_adjacent_scale_coefficient_relative_error"],
        "newton_failures": payload["newton_identity_failure_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
