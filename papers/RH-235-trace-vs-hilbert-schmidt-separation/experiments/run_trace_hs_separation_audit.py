"""Compare cloud-extracted second traces with divergent Frobenius budgets."""

from __future__ import annotations

import json
import math
from pathlib import Path
import sys

import numpy as np
from scipy import sparse


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH229 = PAPERS / "RH-229-nonnormal-frobenius-tail-budget-barrier"
sys.path[:0] = [str(ROOT / "src"), str(RH14 / "src")]

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from trace_hs import complement_trace_power, nilpotent_shift, sparse_trace_square  # noqa: E402


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def scalar(payload: dict[str, float]) -> complex:
    return complex(payload["real"], payload["imag"])


def endpoint_matrix(endpoint: dict[str, object]):
    dimension = int(endpoint["dimension"])
    sigma = float(endpoint["sigma"])
    if endpoint["side"] == "left":
        matrix = sparse_folded_gaussian_matrix(dimension, sigma).tocsr()
    else:
        fine_dimension = 2 * dimension
        fine = sparse_folded_gaussian_matrix(fine_dimension, sigma).tocsr()
        rows = np.arange(fine_dimension)
        columns = np.repeat(np.arange(dimension), 2)
        embedding = sparse.coo_matrix(
            (np.full(fine_dimension, 1.0 / math.sqrt(2.0)), (rows, columns)),
            shape=(fine_dimension, dimension),
        ).tocsr()
        matrix = (embedding.T @ fine @ embedding).tocsr()
    return matrix / float(endpoint["hardy_radius"])


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    frobenius = json.loads(
        (RH229 / "results/frobenius_tail_audit.json").read_text(encoding="utf-8")
    )
    frobenius_rows = {
        (float(row["sigma"]), str(row["side"])): row
        for row in frobenius["endpoint_rows"]
    }
    rows = []
    for endpoint in atlas["endpoint_rows"]:
        matrix = endpoint_matrix(endpoint)
        full_trace = sparse_trace_square(matrix)
        residual = complement_trace_power(
            full_trace,
            scalar(endpoint["perron_scaled"]),
            scalar(endpoint["parity_scaled"]),
            values(endpoint["selected_roots"]),
            2,
        )
        budget = frobenius_rows[(float(endpoint["sigma"]), str(endpoint["side"]))]
        hs_squared = float(endpoint["frobenius_tail_budget_after_perron_parity_cloud"])
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "dimension": endpoint["dimension"],
            "full_trace_square": float(full_trace.real),
            "complement_trace_square_real": float(residual.real),
            "complement_trace_square_modulus": float(abs(residual)),
            "complement_hilbert_schmidt_squared_upper": hs_squared,
            "hs_squared_to_trace_square_ratio": hs_squared / max(abs(residual), np.finfo(float).tiny),
            "inherited_det2_frobenius_log_tail_upper": budget["full_frobenius_log_tail_upper"],
        })
    model_rows = []
    for dimension in (16, 64, 256, 1024):
        shift = nilpotent_shift(dimension)
        model_rows.append({
            "dimension": dimension,
            "hilbert_schmidt_squared": float(np.sum(np.abs(shift) ** 2)),
            "trace_square": float(np.trace(shift @ shift)),
            "det2_value": 1.0,
        })
    return {
        "status": "rh235_trace_vs_hilbert_schmidt_separation",
        "endpoint_count": len(rows),
        "maximum_complement_trace_square_modulus": max(
            row["complement_trace_square_modulus"] for row in rows
        ),
        "minimum_complement_trace_square_modulus": min(
            row["complement_trace_square_modulus"] for row in rows
        ),
        "maximum_complement_hilbert_schmidt_squared_upper": max(
            row["complement_hilbert_schmidt_squared_upper"] for row in rows
        ),
        "maximum_hs_squared_to_trace_square_ratio": max(
            row["hs_squared_to_trace_square_ratio"] for row in rows
        ),
        "endpoint_rows": rows,
        "nilpotent_model_rows": model_rows,
        "theorem_boundary": {
            "divergent_hilbert_schmidt_norm_can_coexist_with_trivial_det2": True,
            "cloud_extracted_second_traces_audited": True,
            "frobenius_barrier_implies_determinant_barrier": False,
            "all_order_trace_envelope": False,
            "uniform_relative_det2_family": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/trace_hs_separation_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "trace_square_max": payload["maximum_complement_trace_square_modulus"],
        "hs_squared_max": payload["maximum_complement_hilbert_schmidt_squared_upper"],
        "maximum_ratio": payload["maximum_hs_squared_to_trace_square_ratio"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
