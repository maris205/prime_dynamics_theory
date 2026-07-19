"""Exact-Frobenius/floating-operator stable-rank audit for RH-49."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.sparse import coo_matrix


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
sys.path.insert(0, str(RH14 / "src"))
sys.path.insert(0, str(ROOT / "experiments"))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_mixed_operator_gain_pilot import (  # noqa: E402
    power_singular_candidate,
)


OUTPUT = ROOT / "results" / "coupling_stable_rank_pilot.json"
FULL_SIGMAS = (0.01, 0.004, 0.002, 0.001, 0.0005)
SMOKE_SIGMAS = (0.01, 0.004)
FINE_RESOLUTION = 20.48


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sparse_haar_couplings(matrix):
    """Materialize exact sparse ``B=U*TV`` and ``C=V*TU`` blocks."""

    if matrix.shape[0] != matrix.shape[1] or matrix.shape[0] % 2:
        raise ValueError("matrix dimension must be even and square")
    values = matrix.tocoo(copy=False)
    dimension = matrix.shape[0] // 2
    rows = values.row // 2
    columns = values.col // 2
    b_sign = np.where(values.col % 2 == 0, 0.5, -0.5)
    c_sign = np.where(values.row % 2 == 0, 0.5, -0.5)
    b = coo_matrix(
        (values.data * b_sign, (rows, columns)),
        shape=(dimension, dimension),
    ).tocsr()
    c = coo_matrix(
        (values.data * c_sign, (rows, columns)),
        shape=(dimension, dimension),
    ).tocsr()
    b.eliminate_zeros()
    c.eliminate_zeros()
    return b, c


def frobenius_norm(matrix) -> float:
    return float(np.sqrt(np.vdot(matrix.data, matrix.data).real))


def operator_candidate(matrix, iterations: int, phase: float):
    return power_singular_candidate(
        lambda vector: matrix @ vector,
        lambda vector: matrix.conjugate().T @ vector,
        matrix.shape[1],
        iterations=iterations,
        phase=phase,
    )


def run_sigma(sigma: float, fine_resolution: float, iterations: int):
    fine_dimension = max(
        128, 2 * int(round(float(fine_resolution) / sigma / 2.0))
    )
    started = time.perf_counter()
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma)
    b, c = sparse_haar_couplings(fine)
    b_hs = frobenius_norm(b)
    c_hs = frobenius_norm(c)
    b_operator = operator_candidate(b, iterations, 0.19)
    c_operator = operator_candidate(c, iterations, 0.31)
    b_op = float(b_operator["singular_candidate"])
    c_op = float(c_operator["singular_candidate"])
    row = {
        "sigma": float(sigma),
        "fine_dimension": fine_dimension,
        "coarse_dimension": fine_dimension // 2,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "fine_nonzeros": int(fine.nnz),
        "B_nonzeros": int(b.nnz),
        "C_nonzeros": int(c.nnz),
        "B_hilbert_schmidt_norm": b_hs,
        "C_hilbert_schmidt_norm": c_hs,
        "B_operator_candidate": b_operator,
        "C_operator_candidate": c_operator,
        "B_sqrt_stable_rank_candidate": b_hs / b_op,
        "C_sqrt_stable_rank_candidate": c_hs / c_op,
        "minimum_sqrt_stable_rank_candidate": min(b_hs / b_op, c_hs / c_op),
        "elapsed_seconds": time.perf_counter() - started,
    }
    del fine, b, c
    gc.collect()
    return row


def fit_power(rows, field: str):
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([float(row[field]) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "field": field,
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--fine-resolution", type=float, default=FINE_RESOLUTION)
    parser.add_argument("--iterations", type=int, default=80)
    args = parser.parse_args()
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(sigma, args.fine_resolution, args.iterations)
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "fine_dimension": row["fine_dimension"],
                    "B_sqrt_stable_rank_candidate": row[
                        "B_sqrt_stable_rank_candidate"
                    ],
                    "C_sqrt_stable_rank_candidate": row[
                        "C_sqrt_stable_rank_candidate"
                    ],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    fields = (
        "B_hilbert_schmidt_norm",
        "C_hilbert_schmidt_norm",
        "B_operator_candidate",
        "C_operator_candidate",
        "B_sqrt_stable_rank_candidate",
        "C_sqrt_stable_rank_candidate",
        "minimum_sqrt_stable_rank_candidate",
    )
    scalar_rows = []
    for row in rows:
        scalar = dict(row)
        scalar["B_operator_candidate"] = row["B_operator_candidate"][
            "singular_candidate"
        ]
        scalar["C_operator_candidate"] = row["C_operator_candidate"][
            "singular_candidate"
        ]
        scalar_rows.append(scalar)
    payload = {
        "status": "exact_frobenius_floating_operator_stable_rank_audit",
        "evidence_level": (
            "exact binary64 sparse Haar Frobenius norms with floating power lower candidates"
        ),
        "fine_resolution_target": float(args.fine_resolution),
        "power_iterations": int(args.iterations),
        "source": {
            "path": str(source_path.relative_to(REPOSITORY)),
            "sha256": sha256_file(source_path),
        },
        "rows": rows,
        "fits": {field: fit_power(scalar_rows, field) for field in fields},
        "limitations": [
            "The sparse Haar Frobenius norms are direct binary64 sums, not interval enclosures.",
            "A power iterate supplies a lower candidate for each operator norm, so the displayed stable-rank ratio is a conservative floating candidate but not a validated upper.",
            "The analytic quarter-power theorem concerns the canonical cell-average family; cutoff and stored-matrix transfer remain separate validation layers.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "coupling_stable_rank_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "minimum_stable_rank_fit": payload["fits"][
                    "minimum_sqrt_stable_rank_candidate"
                ],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
