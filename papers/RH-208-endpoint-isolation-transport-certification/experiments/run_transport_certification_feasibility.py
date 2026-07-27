"""Separate endpoint isolation feasibility from cross-level transport failure."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eig
from scipy.optimize import linear_sum_assignment


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
sys.path[:0] = [str(ROOT / "src"), str(RH58 / "experiments"), str(RH77 / "experiments")]

from run_effective_rank_audit import build_models  # noqa: E402
from run_schur_fusion_pilot import coarse_embedding  # noqa: E402
from transport_certification import eigenpair_condition, isolation_budget, transport_residual  # noqa: E402


SIGMAS = (0.04, 0.02, 0.01)


def model_spectrum(model: dict[str, object]) -> dict[str, object]:
    operator = np.asarray(model["operator"], dtype=complex)
    values, left, right = eig(operator, left=True, right=True, check_finite=False)
    indices = np.argsort(-np.abs(values))[:4]
    return {"operator": operator, "values": values, "left": left, "right": right, "indices": indices}


def run() -> dict[str, object]:
    spectra = {}
    endpoint_rows = []
    for sigma in SIGMAS:
        _, models = build_models(sigma)
        for model in models:
            side = str(model["side"])
            data = model_spectrum(model)
            spectra[(sigma, side)] = data
            mode_rows = []
            for index in data["indices"]:
                value = complex(data["values"][index])
                vector = data["right"][:, index]
                dual = data["left"][:, index]
                residual = float(np.linalg.norm(data["operator"] @ vector - value * vector))
                separation = float(np.min(np.abs(value - np.delete(data["values"], index))))
                condition = eigenpair_condition(vector, dual)
                ratio = isolation_budget(residual, condition, separation)
                mode_rows.append({
                    "eigenvalue_real": float(value.real),
                    "eigenvalue_imag": float(value.imag),
                    "eigenpair_condition": condition,
                    "eigenpair_residual": residual,
                    "spectral_separation": separation,
                    "conditioning_scaled_isolation_ratio": ratio,
                    "ratio_below_one": ratio < 1.0,
                })
            endpoint_rows.append({
                "sigma": sigma,
                "side": side,
                "operator_dimension": int(data["operator"].shape[0]),
                "maximum_conditioning_scaled_isolation_ratio": max(row["conditioning_scaled_isolation_ratio"] for row in mode_rows),
                "all_endpoint_ratios_below_one": all(row["ratio_below_one"] for row in mode_rows),
                "modes": mode_rows,
            })

    transport_rows = []
    for coarse_sigma, fine_sigma in zip(SIGMAS[:-1], SIGMAS[1:]):
        for side in ("left", "right"):
            coarse = spectra[(coarse_sigma, side)]
            fine = spectra[(fine_sigma, side)]
            coarse_indices = np.asarray(coarse["indices"])
            fine_indices = np.asarray(fine["indices"])
            distance = np.abs(coarse["values"][coarse_indices, None] - fine["values"][fine_indices][None, :])
            rows, columns = linear_sum_assignment(distance)
            assignment = np.empty(4, dtype=int)
            assignment[rows] = fine_indices[columns]
            embedding = coarse_embedding(fine["operator"].shape[0])
            mode_rows = []
            for coarse_index, fine_index in zip(coarse_indices, assignment):
                residual = transport_residual(
                    fine["operator"], embedding, coarse["right"][:, coarse_index], coarse["values"][coarse_index]
                )
                fine_value = fine["values"][fine_index]
                separation = float(np.min(np.abs(fine_value - np.delete(fine["values"], fine_index))))
                condition = eigenpair_condition(fine["right"][:, fine_index], fine["left"][:, fine_index])
                ratio = isolation_budget(residual, condition, separation)
                mode_rows.append({
                    "coarse_eigenvalue_real": float(coarse["values"][coarse_index].real),
                    "coarse_eigenvalue_imag": float(coarse["values"][coarse_index].imag),
                    "matched_fine_eigenvalue_real": float(fine_value.real),
                    "matched_fine_eigenvalue_imag": float(fine_value.imag),
                    "lifted_eigenvector_residual": residual,
                    "matched_fine_condition": condition,
                    "matched_fine_separation": separation,
                    "conditioning_scaled_transport_ratio": ratio,
                    "ratio_below_one": ratio < 1.0,
                })
            transport_rows.append({
                "coarse_sigma": coarse_sigma,
                "fine_sigma": fine_sigma,
                "side": side,
                "minimum_conditioning_scaled_transport_ratio": min(row["conditioning_scaled_transport_ratio"] for row in mode_rows),
                "maximum_conditioning_scaled_transport_ratio": max(row["conditioning_scaled_transport_ratio"] for row in mode_rows),
                "all_transport_ratios_below_one": all(row["ratio_below_one"] for row in mode_rows),
                "modes": mode_rows,
            })
    return {
        "status": "rh208_endpoint_isolation_transport_certification",
        "endpoint_case_count": len(endpoint_rows),
        "transport_case_count": len(transport_rows),
        "endpoint_case_below_one_count": sum(bool(row["all_endpoint_ratios_below_one"]) for row in endpoint_rows),
        "transport_case_below_one_count": sum(bool(row["all_transport_ratios_below_one"]) for row in transport_rows),
        "maximum_endpoint_isolation_ratio": max(float(row["maximum_conditioning_scaled_isolation_ratio"]) for row in endpoint_rows),
        "minimum_transport_ratio": min(float(row["minimum_conditioning_scaled_transport_ratio"]) for row in transport_rows),
        "maximum_transport_ratio": max(float(row["maximum_conditioning_scaled_transport_ratio"]) for row in transport_rows),
        "endpoint_rows": endpoint_rows,
        "transport_rows": transport_rows,
        "theorem_boundary": {
            "finite_backward_residual_budget": True,
            "endpoint_isolation_numerically_feasible": True,
            "naive_transport_budget_fails": True,
            "interval_matrix_input_enclosure": False,
            "validated_riesz_projector": False,
            "validated_cross_level_homotopy": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/transport_certification_feasibility.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "endpoint_green": payload["endpoint_case_below_one_count"],
        "transport_green": payload["transport_case_below_one_count"],
        "transport_ratio_max": payload["maximum_transport_ratio"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
