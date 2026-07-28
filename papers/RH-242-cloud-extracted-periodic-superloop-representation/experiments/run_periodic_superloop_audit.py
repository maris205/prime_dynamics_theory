"""Audit finite periodic-loop, counterloop, and archived sign identities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH236 = PAPERS / "RH-236-cloud-extracted-trace-moment-atlas"
sys.path.insert(0, str(ROOT / "src"))

from periodic_superloops import (  # noqa: E402
    HARDY_RADIUS,
    atomic_power_trace,
    closed_loop_sum,
    cloud_extracted_trace,
    folded_gaussian_kernel,
    folded_gaussian_matrix,
    graded_supertrace,
    matrix_power_trace,
)


SMALL_CASES = ((4, 0.08), (5, 0.05), (6, 0.03))
ORDERS = (2, 3, 4, 5)


def selected_indices(values: np.ndarray) -> tuple[int, int, list[int], list[int]]:
    roots = np.asarray(values, dtype=complex)
    perron = int(np.argmin(np.abs(roots - 1.0)))
    candidates = [index for index in range(roots.size) if index != perron]
    real_negative = [
        index for index in candidates
        if abs(roots[index].imag) < 1.0e-10 and roots[index].real < 0.0
    ]
    parity = min(real_negative, key=lambda index: roots[index].real)
    remaining = [index for index in candidates if index != parity]
    outer = max(remaining, key=lambda index: abs(roots[index]))
    if abs(roots[outer].imag) < 1.0e-10:
        cloud = [outer]
    else:
        partner = min(
            (index for index in remaining if index != outer),
            key=lambda index: abs(roots[index] - np.conj(roots[outer])),
        )
        cloud = [outer, partner]
    omitted = [index for index in remaining if index not in cloud]
    return perron, parity, cloud, omitted


def complex_payload(value: complex) -> dict[str, float]:
    number = complex(value)
    return {"real": float(number.real), "imag": float(number.imag)}


def run() -> dict[str, object]:
    loop_rows = []
    for dimension, sigma in SMALL_CASES:
        raw = folded_gaussian_matrix(dimension, sigma)
        scaled = raw / HARDY_RADIUS
        eigenvalues = np.linalg.eigvals(raw)
        perron, parity, cloud, omitted = selected_indices(eigenvalues)
        scaled_values = eigenvalues / HARDY_RADIUS
        selected = scaled_values[[perron, parity, *cloud]]
        for order in ORDERS:
            direct = matrix_power_trace(scaled, order)
            loops = closed_loop_sum(scaled, order)
            extracted = cloud_extracted_trace(scaled, selected, order)
            supertrace = graded_supertrace(scaled, selected, order)
            omitted_power = atomic_power_trace(scaled_values[omitted], order)
            loop_rows.append({
                "dimension": dimension,
                "sigma": sigma,
                "order": order,
                "closed_loop_count": dimension**order,
                "direct_trace": complex_payload(direct),
                "loop_trace": complex_payload(loops),
                "cloud_extracted_trace": complex_payload(extracted),
                "omitted_spectral_power": complex_payload(omitted_power),
                "loop_identity_error": float(abs(direct - loops)),
                "supertrace_identity_error": float(abs(extracted - supertrace)),
                "spectral_partition_error": float(abs(extracted - omitted_power)),
            })

    quadrature_nodes, quadrature_weights = np.polynomial.legendre.leggauss(256)
    folded_nodes = 0.5 * (quadrature_nodes + 1.0)
    folded_weights = 0.5 * quadrature_weights
    kernel_rows = []
    for sigma in (0.04, 0.08):
        for source in (0.05, 0.3, 0.7, 0.98):
            values = folded_gaussian_kernel(source, folded_nodes, sigma)
            mass = float(np.dot(folded_weights, values))
            kernel_rows.append({
                "sigma": sigma,
                "source": source,
                "quadrature_mass": mass,
                "row_normalization_error": abs(mass - 1.0),
            })

    atlas = json.loads(
        (RH236 / "results/trace_moment_atlas.json").read_text(encoding="utf-8")
    )
    signs = {"negative": 0, "positive": 0, "zero": 0}
    order_signs = {
        str(order): {"negative": 0, "positive": 0, "zero": 0}
        for order in range(2, 13)
    }
    minimum = None
    maximum = None
    cancellation = None
    for row in atlas["endpoint_rows"]:
        full = np.asarray(row["full_trace_powers"]["real"]) + 1j * np.asarray(
            row["full_trace_powers"]["imag"]
        )
        residual = np.asarray(row["cloud_extracted_trace_powers"]["real"]) + 1j * np.asarray(
            row["cloud_extracted_trace_powers"]["imag"]
        )
        for order in range(2, 13):
            value = complex(residual[order - 1])
            label = "negative" if value.real < 0.0 else "positive" if value.real > 0.0 else "zero"
            signs[label] += 1
            order_signs[str(order)][label] += 1
            item = {
                "sigma": row["sigma"],
                "side": row["side"],
                "order": order,
                "value": value.real,
            }
            if minimum is None or value.real < minimum["value"]:
                minimum = item
            if maximum is None or value.real > maximum["value"]:
                maximum = item
            ratio = float(abs(full[order - 1]) / max(abs(value), np.finfo(float).tiny))
            candidate = {
                "sigma": row["sigma"],
                "side": row["side"],
                "order": order,
                "full_trace_modulus": float(abs(full[order - 1])),
                "residual_modulus": float(abs(value)),
                "full_to_residual_modulus_ratio": ratio,
            }
            if cancellation is None or ratio > cancellation["full_to_residual_modulus_ratio"]:
                cancellation = candidate

    return {
        "status": "rh242_cloud_extracted_periodic_superloop_representation",
        "route_coordinate": "finite_noise_periodic_superloop_open_grouped_envelope_and_anchor",
        "small_matrix_case_count": len(SMALL_CASES),
        "enumerated_loop_identity_case_count": len(loop_rows),
        "enumerated_closed_loop_count": sum(row["closed_loop_count"] for row in loop_rows),
        "maximum_loop_identity_error": max(row["loop_identity_error"] for row in loop_rows),
        "maximum_supertrace_identity_error": max(
            row["supertrace_identity_error"] for row in loop_rows
        ),
        "maximum_spectral_partition_error": max(
            row["spectral_partition_error"] for row in loop_rows
        ),
        "maximum_kernel_row_normalization_error": max(
            row["row_normalization_error"] for row in kernel_rows
        ),
        "loop_rows": loop_rows,
        "kernel_rows": kernel_rows,
        "archived_determinant_relevant_trace_case_count": sum(signs.values()),
        "archived_sign_counts": signs,
        "archived_order_sign_counts": order_signs,
        "every_archived_order_has_both_signs": all(
            row["negative"] > 0 and row["positive"] > 0 for row in order_signs.values()
        ),
        "minimum_archived_real_trace": minimum,
        "maximum_archived_real_trace": maximum,
        "largest_floating_cancellation_indicator": cancellation,
        "logical_separation": {
            "envelope_without_prescribed_anchor": (
                "a fixed finite-support coefficient sequence satisfies a geometric envelope "
                "but can differ from any prescribed anchor"
            ),
            "anchor_without_uniform_envelope": (
                "tau_n^(j)=a_n except for an exp((j+1)^2)(1+|a_(j+1)|) spike at n=j+1 "
                "converges at every fixed order but has no uniform geometric envelope"
            ),
        },
        "theorem_boundary": {
            "fixed_noise_continuum_periodic_loop_identity": True,
            "finite_matrix_closed_loop_identity": True,
            "projection_free_graded_counterloop_representation": True,
            "ordinary_positive_loop_deletion_represents_all_archived_residuals": False,
            "archived_sparse_matrix_to_continuum_uniform_bridge": False,
            "uniform_all_order_trace_envelope": False,
            "deterministic_numerator_coefficient_anchor": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/periodic_superloop_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "loop_cases": payload["enumerated_loop_identity_case_count"],
        "negative_archived_traces": payload["archived_sign_counts"]["negative"],
        "positive_archived_traces": payload["archived_sign_counts"]["positive"],
        "maximum_loop_identity_error": payload["maximum_loop_identity_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
