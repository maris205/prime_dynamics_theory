"""Five-scale grouped-Riesz audit of the RH-57 Hardy budget.

All matrix construction, eigensolvers, and Lyapunov solves are binary64.
The calculation audits invariant blocks rather than individual modal
condition numbers; it is not an interval spectral certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eig, solve_discrete_lyapunov


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH56 = PAPERS / "RH-56-growing-horizon-hard-space-barrier"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH14 / "src"))

from haar_overlap import (  # noqa: E402
    block_gram_from_gramian,
    gram_budget,
    radial_riesz_partition,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402


OUTPUT = ROOT / "results" / "mixed_overlap_pilot.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
SMOKE_SIGMAS = (0.16, 0.08)
FINE_RESOLUTION = 5.12
HARDY_RADIUS = 0.85
RADIAL_CUTS = (0.15, 0.35, 0.55)
RADIAL_NAMES = ("central", "inner_cloud", "middle_cloud", "edge_cloud")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def coarse_embedding(dimension: int) -> np.ndarray:
    coarse = dimension // 2
    result = np.zeros((dimension, coarse), dtype=np.float64)
    indices = np.arange(coarse)
    result[2 * indices, indices] = 1.0 / math.sqrt(2.0)
    result[2 * indices + 1, indices] = 1.0 / math.sqrt(2.0)
    return result


def detail_embedding(dimension: int) -> np.ndarray:
    coarse = dimension // 2
    result = np.zeros((dimension, coarse), dtype=np.float64)
    indices = np.arange(coarse)
    result[2 * indices, indices] = 1.0 / math.sqrt(2.0)
    result[2 * indices + 1, indices] = -1.0 / math.sqrt(2.0)
    return result


def real_if_small(value: np.ndarray, tolerance: float = 2.0e-9) -> np.ndarray:
    array = np.asarray(value)
    if np.max(np.abs(array.imag), initial=0.0) <= tolerance:
        return array.real.astype(np.float64)
    return array.astype(np.complex128)


def spectral_bulk(matrix: np.ndarray) -> dict[str, object]:
    values, left_raw, right_raw = eig(
        matrix, left=True, right=True, check_finite=False
    )
    perron_index = int(np.argmin(np.abs(values - 1.0)))
    real_negative = np.flatnonzero(
        (np.abs(values.imag) < 2.0e-8) & (values.real < -1.0e-8)
    )
    if not real_negative.size:
        raise RuntimeError("no negative real parity eigenvalue was resolved")
    parity_index = int(real_negative[np.argmin(values[real_negative].real)])
    selected = np.asarray(
        (values[perron_index], values[parity_index]), dtype=np.complex128
    )
    right = np.column_stack(
        (np.ones(matrix.shape[0], dtype=np.complex128), right_raw[:, parity_index])
    )
    left = np.column_stack((left_raw[:, perron_index], left_raw[:, parity_index]))
    left = left @ np.linalg.inv(left.conjugate().T @ right).conjugate().T
    projection = right @ left.conjugate().T
    complement = np.eye(matrix.shape[0]) - projection
    bulk = matrix - right @ np.diag(selected) @ left.conjugate().T
    remaining = np.delete(values, (perron_index, parity_index))
    return {
        "bulk": real_if_small(bulk),
        "complement": real_if_small(complement),
        "bulk_radius": float(np.max(np.abs(remaining), initial=0.0)),
        "biorthogonality_defect": float(
            np.linalg.norm(left.conjugate().T @ right - np.eye(2), 2)
        ),
    }


def fit_power(rows: list[dict[str, object]], path: tuple[str, ...]) -> dict[str, float]:
    def extract(row: dict[str, object]) -> float:
        value: object = row
        for key in path:
            value = value[key]  # type: ignore[index]
        return float(value)

    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([extract(row) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def channel_audit(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
) -> dict[str, object]:
    gramian = solve_discrete_lyapunov(
        operator, source @ source.conjugate().T
    )
    gramian = 0.5 * (gramian + gramian.conjugate().T)
    stein_defect = (
        gramian
        - operator @ gramian @ operator.conjugate().T
        - source @ source.conjugate().T
    )
    partition = radial_riesz_partition(
        operator,
        RADIAL_CUTS,
        physical_scale=HARDY_RADIUS,
        names=RADIAL_NAMES,
    )
    block_gram = block_gram_from_gramian(
        gramian, observation, partition.projectors
    )
    budget = gram_budget(block_gram, tolerance=2.0e-10)
    direct_squared = float(
        np.trace(observation @ gramian @ observation.conjugate().T).real
    )
    direct_energy = math.sqrt(max(direct_squared, 0.0))
    blocks = []
    for index, name in enumerate(partition.names):
        assigned = np.digitize(
            partition.physical_moduli, RADIAL_CUTS, right=True
        )
        original_index = RADIAL_NAMES.index(name)
        values = partition.physical_moduli[assigned == original_index]
        blocks.append(
            {
                "name": name,
                "eigenvalue_count": partition.counts[index],
                "minimum_physical_modulus": float(np.min(values))
                if values.size
                else 0.0,
                "maximum_physical_modulus": float(np.max(values))
                if values.size
                else 0.0,
                "hardy_energy": float(budget.block_energies[index]),
                "projector_norm": partition.projector_norms[index],
                "left_right_overlap_condition": (
                    partition.overlap_condition_numbers[index]
                ),
                "idempotence_defect": partition.idempotence_defects[index],
                "commutator_defect": partition.commutator_defects[index],
            }
        )
    return {
        "exact_hardy_energy": direct_energy,
        "block_reconstructed_energy": budget.exact_energy,
        "block_reconstruction_relative_defect": abs(
            budget.exact_energy - direct_energy
        ) / max(direct_energy, 1.0e-300),
        "square_sum_energy": budget.square_sum_energy,
        "signed_fusion_ratio": budget.signed_fusion_ratio,
        "absolute_block_upper": budget.absolute_block_upper,
        "coherence_constant": budget.coherence_constant,
        "coherence_upper": budget.coherence_upper,
        "gershgorin_constant": budget.gershgorin_constant,
        "gershgorin_upper": budget.gershgorin_upper,
        "coherence_upper_over_exact": budget.coherence_upper
        / max(direct_energy, 1.0e-300),
        "absolute_upper_over_exact": budget.absolute_block_upper
        / max(direct_energy, 1.0e-300),
        "minimum_block_gram_eigenvalue": budget.minimum_gram_eigenvalue,
        "normalized_block_gram_real": budget.normalized_gram.real.tolist(),
        "normalized_block_gram_imag": budget.normalized_gram.imag.tolist(),
        "stein_defect_norm": float(np.linalg.norm(stein_defect, 2)),
        "partition_defect": partition.partition_defect,
        "maximum_pairwise_projector_product": partition.pairwise_product_defect,
        "minimum_radial_cut_gap": partition.minimum_boundary_gap,
        "blocks": blocks,
    }


def run_sigma(sigma: float) -> dict[str, object]:
    started = time.perf_counter()
    fine_dimension = max(32, 2 * int(round(FINE_RESOLUTION / sigma / 2.0)))
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma).toarray()
    u = coarse_embedding(fine_dimension)
    w = detail_embedding(fine_dimension)
    fine_u = fine @ u
    coarse = u.T @ fine_u
    coupling_b = u.T @ fine @ w
    coupling_c = w.T @ fine_u
    fine_data = spectral_bulk(fine)
    coarse_data = spectral_bulk(coarse)
    fine_operator = np.asarray(fine_data["bulk"]) / HARDY_RADIUS
    coarse_operator = (
        np.asarray(coarse_data["bulk"]).conjugate().T / HARDY_RADIUS
    )
    left_source = (
        np.asarray(fine_data["complement"])
        @ u
        @ coupling_b
        / np.linalg.norm(coupling_b, "fro")
    )
    right_source = coupling_c.conjugate().T / np.linalg.norm(coupling_c, "fro")
    left_observation = u.T
    right_observation = np.asarray(coarse_data["complement"]).conjugate().T
    return {
        "sigma": sigma,
        "fine_dimension": fine_dimension,
        "coarse_dimension": fine_dimension // 2,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "fine_bulk_radius_candidate": fine_data["bulk_radius"],
        "coarse_bulk_radius_candidate": coarse_data["bulk_radius"],
        "fine_biorthogonality_defect": fine_data["biorthogonality_defect"],
        "coarse_biorthogonality_defect": coarse_data["biorthogonality_defect"],
        "left": channel_audit(fine_operator, left_source, left_observation),
        "right": channel_audit(coarse_operator, right_source, right_observation),
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    rows = []
    for sigma in (SMOKE_SIGMAS if args.smoke else FULL_SIGMAS):
        row = run_sigma(float(sigma))
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "dimension": row["fine_dimension"],
                    "left_energy": row["left"]["exact_hardy_energy"],
                    "left_coherence": row["left"]["coherence_constant"],
                    "right_energy": row["right"]["exact_hardy_energy"],
                    "right_coherence": row["right"]["coherence_constant"],
                    "elapsed_seconds": row["elapsed_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )
    payload = {
        "status": "binary64_grouped_riesz_cross_stein_overlap_audit",
        "evidence_level": (
            "deterministic all-column dense binary64 Lyapunov and grouped "
            "left/right eigenspace audit; not interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "radial_cuts": list(RADIAL_CUTS),
        "radial_names": list(RADIAL_NAMES),
        "sources": {
            "folded_gaussian": {
                "path": str(
                    (RH14 / "src" / "parity_boundary" / "operators.py").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH14 / "src" / "parity_boundary" / "operators.py"
                ),
            },
            "rh56_manuscript": {
                "path": str((RH56 / "main.tex").relative_to(REPOSITORY)),
                "sha256": sha256_file(RH56 / "main.tex"),
            },
        },
        "rows": rows,
        "fits": {
            "left_exact_energy": fit_power(rows, ("left", "exact_hardy_energy")),
            "right_exact_energy": fit_power(rows, ("right", "exact_hardy_energy")),
            "left_square_sum": fit_power(rows, ("left", "square_sum_energy")),
            "right_square_sum": fit_power(rows, ("right", "square_sum_energy")),
            "left_coherence_upper": fit_power(rows, ("left", "coherence_upper")),
            "right_coherence_upper": fit_power(rows, ("right", "coherence_upper")),
            "left_signed_fusion_ratio": fit_power(
                rows, ("left", "signed_fusion_ratio")
            ),
            "right_signed_fusion_ratio": fit_power(
                rows, ("right", "signed_fusion_ratio")
            ),
        },
        "limitations": [
            "The grouped Riesz projectors use binary64 left/right eigenspaces and are not contour enclosures.",
            "The dense audit holds N*sigma=5.12, below the RH-50 production resolution N*sigma=20.48.",
            "Fixed radial cuts audit one invariant-block organization; they do not prove a dyadically uniform physical cloud decomposition.",
            "Five levels and fitted exponents are diagnostics, not small-noise asymptotic theorems.",
            "Stage A1 and unconditional Stage A4 remain open.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "mixed_overlap_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
