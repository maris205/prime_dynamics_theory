"""Five-scale unitary Schur packet and path-majorant audit for RH-58."""

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
RH57 = PAPERS / "RH-57-mixed-haar-channel-overlap-budget"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH14 / "src"))

from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from schur_fusion import (  # noqa: E402
    cross_stein_recursion_audit,
    gram_budget,
    ordered_radial_schur,
    scalar_path_majorant,
    schur_source_gram,
    schur_state_gram,
)


OUTPUT = ROOT / "results" / "schur_fusion_pilot.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
SMOKE_SIGMAS = (0.16, 0.08)
FINE_RESOLUTION = 5.12
HARDY_RADIUS = 0.85
RADIAL_CUTS = (0.15, 0.35, 0.55)
RADIAL_NAMES = ("central", "inner_cloud", "middle_cloud", "edge_cloud")
BLOCK_HORIZON = 8


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


def gram_payload(budget) -> dict[str, object]:
    return {
        "exact_reconstructed_energy": budget.exact_energy,
        "square_sum_energy": budget.square_sum_energy,
        "signed_fusion_ratio": budget.signed_fusion_ratio,
        "coherence_constant": budget.coherence_constant,
        "coherence_upper": budget.coherence_upper,
        "absolute_packet_upper": budget.absolute_packet_upper,
        "minimum_gram_eigenvalue": budget.minimum_gram_eigenvalue,
        "normalized_gram_real": budget.normalized_gram.real.tolist(),
        "normalized_gram_imag": budget.normalized_gram.imag.tolist(),
    }


def channel_audit(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    inherited_riesz: dict[str, object],
) -> dict[str, object]:
    controllability = solve_discrete_lyapunov(
        operator, source @ source.conjugate().T
    )
    controllability = 0.5 * (
        controllability + controllability.conjugate().T
    )
    observability = solve_discrete_lyapunov(
        operator.conjugate().T,
        observation.conjugate().T @ observation,
    )
    observability = 0.5 * (observability + observability.conjugate().T)
    direct_squared = float(
        np.trace(
            observation @ controllability @ observation.conjugate().T
        ).real
    )
    dual_squared = float(
        np.trace(source.conjugate().T @ observability @ source).real
    )
    direct_energy = math.sqrt(max(direct_squared, 0.0))

    partition = ordered_radial_schur(
        operator,
        RADIAL_CUTS,
        physical_scale=HARDY_RADIUS,
        names=RADIAL_NAMES,
    )
    state_budget = gram_budget(
        schur_state_gram(controllability, observation, partition),
        tolerance=2.0e-10,
    )
    source_budget = gram_budget(
        schur_source_gram(observability, source, partition),
        tolerance=2.0e-10,
    )
    recursion = cross_stein_recursion_audit(
        controllability, source, partition
    )
    majorant = scalar_path_majorant(
        source,
        observation,
        partition,
        horizon=BLOCK_HORIZON,
    )

    transformed_source = partition.unitary.conjugate().T @ source
    transformed_observation = observation @ partition.unitary
    blocks = []
    for index, (name, block_slice) in enumerate(
        zip(partition.names, partition.slices)
    ):
        moduli = partition.physical_moduli[block_slice]
        diagonal = partition.triangular[block_slice, block_slice]
        blocks.append(
            {
                "name": name,
                "dimension": partition.sizes[index],
                "minimum_physical_modulus": float(np.min(moduli)),
                "maximum_physical_modulus": float(np.max(moduli)),
                "source_packet_norm": float(
                    np.linalg.norm(transformed_source[block_slice, :], "fro")
                ),
                "observation_packet_norm": float(
                    np.linalg.norm(
                        transformed_observation[:, block_slice], "fro"
                    )
                ),
                "source_packet_hardy_energy": float(
                    source_budget.block_energies[index]
                ),
                "state_block_hardy_energy": float(
                    state_budget.block_energies[index]
                ),
                "diagonal_block_norm": float(np.linalg.norm(diagonal, 2)),
                "diagonal_block_spectral_radius": float(
                    np.max(np.abs(np.diag(diagonal)), initial=0.0)
                ),
                "horizon_power_norm": float(
                    majorant.stein_gains.power_norms[index][-1]
                ),
                "diagonal_stein_gain_upper": float(
                    majorant.stein_gains.gains[index, index]
                ),
            }
        )

    off_diagonal_squared = 0.0
    maximum_coupling = 0.0
    for row, left in enumerate(partition.slices):
        for column, right in enumerate(partition.slices):
            if row >= column:
                continue
            block = partition.triangular[left, right]
            off_diagonal_squared += float(np.linalg.norm(block, "fro") ** 2)
            maximum_coupling = max(
                maximum_coupling, float(np.linalg.norm(block, 2))
            )

    recursion_rows = [
        {
            "left_block": item.left_block,
            "right_block": item.right_block,
            "gramian_norm": item.gramian_norm,
            "right_hand_side_norm": item.right_hand_side_norm,
            "source_norm": item.source_norm,
            "feed_forward_norm": item.feed_forward_norm,
            "empirical_gain": item.empirical_gain,
            "residual_norm": item.residual_norm,
        }
        for item in recursion.rows
    ]
    inherited_blocks = inherited_riesz["blocks"]
    return {
        "exact_hardy_energy": direct_energy,
        "primal_dual_energy_squared_relative_defect": abs(
            direct_squared - dual_squared
        )
        / max(direct_squared, 1.0e-300),
        "state_block_gram": gram_payload(state_budget),
        "source_packet_gram": gram_payload(source_budget),
        "state_reconstruction_relative_defect": abs(
            state_budget.exact_energy - direct_energy
        )
        / max(direct_energy, 1.0e-300),
        "source_reconstruction_relative_defect": abs(
            source_budget.exact_energy - direct_energy
        )
        / max(direct_energy, 1.0e-300),
        "scalar_path_majorant": {
            "horizon": majorant.horizon,
            "energy_upper": majorant.energy_upper,
            "energy_upper_over_exact": majorant.energy_upper
            / max(direct_energy, 1.0e-300),
            "maximum_block_stein_gain": majorant.stein_gains.maximum_gain,
            "maximum_terminal_power_norm": (
                majorant.stein_gains.maximum_terminal_power_norm
            ),
            "maximum_gramian_norm_upper": float(
                np.max(majorant.gramian_norm_uppers, initial=0.0)
            ),
        },
        "schur_partition": {
            "reconstruction_defect": partition.reconstruction_defect,
            "unitary_defect": partition.unitary_defect,
            "strict_lower_defect": partition.strict_lower_defect,
            "minimum_radial_cut_gap": partition.minimum_boundary_gap,
            "off_diagonal_block_frobenius_norm": math.sqrt(
                off_diagonal_squared
            ),
            "maximum_off_diagonal_block_norm": maximum_coupling,
        },
        "cross_stein_recursion": {
            "maximum_residual_norm": recursion.maximum_residual_norm,
            "maximum_empirical_gain": recursion.maximum_empirical_gain,
            "rows": recursion_rows,
        },
        "inherited_rh57_radial_riesz": {
            "coherence_upper": inherited_riesz["coherence_upper"],
            "maximum_projector_norm": max(
                float(block["projector_norm"])
                for block in inherited_blocks
            ),
            "signed_fusion_ratio": inherited_riesz["signed_fusion_ratio"],
        },
        "blocks": blocks,
    }


def run_sigma(
    sigma: float, inherited_row: dict[str, object]
) -> dict[str, object]:
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
    right_source = (
        coupling_c.conjugate().T / np.linalg.norm(coupling_c, "fro")
    )
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
        "coarse_biorthogonality_defect": coarse_data[
            "biorthogonality_defect"
        ],
        "left": channel_audit(
            fine_operator,
            left_source,
            left_observation,
            inherited_row["left"],
        ),
        "right": channel_audit(
            coarse_operator,
            right_source,
            right_observation,
            inherited_row["right"],
        ),
        "elapsed_seconds": time.perf_counter() - started,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    inherited = json.loads(
        (RH57 / "results" / "mixed_overlap_pilot.json").read_text(
            encoding="utf-8"
        )
    )
    inherited_rows = {
        float(row["sigma"]): row for row in inherited["rows"]
    }
    sigmas = SMOKE_SIGMAS if args.smoke else FULL_SIGMAS
    rows = []
    for sigma in sigmas:
        row = run_sigma(float(sigma), inherited_rows[float(sigma)])
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "dimension": row["fine_dimension"],
                    "left_exact": row["left"]["exact_hardy_energy"],
                    "left_schur_upper": row["left"]["source_packet_gram"][
                        "coherence_upper"
                    ],
                    "left_path_upper": row["left"]["scalar_path_majorant"][
                        "energy_upper"
                    ],
                    "right_exact": row["right"]["exact_hardy_energy"],
                    "right_schur_upper": row["right"]["source_packet_gram"][
                        "coherence_upper"
                    ],
                    "right_path_upper": row["right"]["scalar_path_majorant"][
                        "energy_upper"
                    ],
                    "elapsed_seconds": row["elapsed_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    payload = {
        "status": "binary64_unitary_schur_packet_and_absolute_path_audit",
        "evidence_level": (
            "deterministic all-column dense binary64 controllability, "
            "observability, ordered Schur, and block-power audit; not "
            "interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "radial_cuts": list(RADIAL_CUTS),
        "radial_names": list(RADIAL_NAMES),
        "block_horizon": BLOCK_HORIZON,
        "sources": {
            "folded_gaussian": {
                "path": str(
                    (
                        RH14
                        / "src"
                        / "parity_boundary"
                        / "operators.py"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH14 / "src" / "parity_boundary" / "operators.py"
                ),
            },
            "rh57_pilot": {
                "path": str(
                    (
                        RH57 / "results" / "mixed_overlap_pilot.json"
                    ).relative_to(REPOSITORY)
                ),
                "sha256": sha256_file(
                    RH57 / "results" / "mixed_overlap_pilot.json"
                ),
            },
            "rh57_manuscript": {
                "path": str((RH57 / "main.tex").relative_to(REPOSITORY)),
                "sha256": sha256_file(RH57 / "main.tex"),
            },
        },
        "rows": rows,
        "fits": {
            "left_exact": fit_power(rows, ("left", "exact_hardy_energy")),
            "right_exact": fit_power(rows, ("right", "exact_hardy_energy")),
            "left_source_packet_upper": fit_power(
                rows,
                ("left", "source_packet_gram", "coherence_upper"),
            ),
            "right_source_packet_upper": fit_power(
                rows,
                ("right", "source_packet_gram", "coherence_upper"),
            ),
            "left_state_block_upper": fit_power(
                rows,
                ("left", "state_block_gram", "coherence_upper"),
            ),
            "right_state_block_upper": fit_power(
                rows,
                ("right", "state_block_gram", "coherence_upper"),
            ),
            "left_scalar_path_upper": fit_power(
                rows,
                ("left", "scalar_path_majorant", "energy_upper"),
            ),
            "right_scalar_path_upper": fit_power(
                rows,
                ("right", "scalar_path_majorant", "energy_upper"),
            ),
        },
        "limitations": [
            "The ordered Schur forms and all Lyapunov solves are binary64 diagnostics, not interval enclosures.",
            "The unitary Schur basis is noise-dependent and no continuum regularity of its packet subspaces is proved.",
            "The scalar path majorant is a sufficient norm ledger; its growth does not imply growth of the exact Hardy energy.",
            "The dense audit uses N*sigma=5.12, below the RH-50 production resolution N*sigma=20.48.",
            "Five levels do not prove a dyadically uniform packet Gram budget; Stage A1 and Stage A4 remain open.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "schur_fusion_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


if __name__ == "__main__":
    main()
