"""Five-scale phase-aware finite-horizon completion audit for RH-60."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import solve_discrete_lyapunov


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
RH59 = PAPERS / "RH-59-flag-adapted-schur-stein-metrics"
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(RH59 / "src"))
sys.path.insert(0, str(RH59 / "experiments"))
sys.path.insert(0, str(RH58 / "src"))
sys.path.insert(0, str(RH58 / "experiments"))
sys.path.insert(0, str(RH14 / "src"))

from flag_stein import build_flag_metric, scaled_normalized_prefix  # noqa: E402
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from phase_tail import (  # noqa: E402
    finite_horizon_gram,
    geometric_tail_energy_upper,
    make_completion,
    stein_tail_energy_upper,
)
from run_flag_metric_pilot import (  # noqa: E402
    FINE_RESOLUTION,
    HARDY_RADIUS,
    RADIAL_CUTS,
    RADIAL_NAMES,
    coarse_embedding,
    detail_embedding,
    spectral_bulk,
)
from schur_fusion import ordered_radial_schur  # noqa: E402


OUTPUT = ROOT / "results" / "phase_tail_pilot.json"
FULL_SIGMAS = (0.16, 0.08, 0.04, 0.02, 0.01)
SMOKE_SIGMAS = (0.16, 0.08)
HORIZONS = (0, 1, 2, 4, 8, 16, 32, 64)
SELECTED_HORIZON = 32


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def packet_tail_data(
    transformed_source: np.ndarray,
    transformed_observation: np.ndarray,
    partition,
    family,
    packet_index: int,
    packet_record: dict[str, object],
) -> tuple[np.ndarray, np.ndarray, float, float, float]:
    """Return prefix normalized operator, weighted packet source, kappa, q, and exact packet source."""

    log_scales = np.asarray(packet_record["log_scales"], dtype=float)
    prefix = partition.slices[packet_index].stop
    block_slice = partition.slices[packet_index]
    source = np.zeros((prefix, transformed_source.shape[1]), dtype=np.complex128)
    source[block_slice, :] = transformed_source[block_slice, :]
    weighted = np.zeros_like(source)
    for index, local_slice in enumerate(partition.slices[: packet_index + 1]):
        block = family.blocks[index]
        weighted[local_slice, :] = (
            math.exp(float(log_scales[index]))
            * block.square_root
            @ source[local_slice, :]
        )
    normalized = scaled_normalized_prefix(
        family, packet_index, log_scales
    )
    return (
        normalized,
        weighted,
        float(packet_record["kappa"]),
        float(np.linalg.norm(normalized, 2)),
        float(packet_record["exact_packet_energy"]),
    )


def channel_audit(
    operator: np.ndarray,
    source: np.ndarray,
    observation: np.ndarray,
    inherited: dict[str, object],
) -> dict[str, object]:
    observability = solve_discrete_lyapunov(
        operator.conjugate().T,
        observation.conjugate().T @ observation,
    )
    observability = 0.5 * (
        observability + observability.conjugate().T
    )
    exact = math.sqrt(
        max(0.0, float(np.trace(source.conjugate().T @ observability @ source).real))
    )
    partition = ordered_radial_schur(
        operator,
        RADIAL_CUTS,
        physical_scale=HARDY_RADIUS,
        names=RADIAL_NAMES,
    )
    transformed_source = partition.unitary.conjugate().T @ source
    transformed_observation = observation @ partition.unitary
    family = build_flag_metric(partition.triangular, partition.sizes)
    packet_records = inherited["packets"]

    packet_states = []
    for packet_index, packet_record in enumerate(packet_records):
        packet_states.append(
            packet_tail_data(
                transformed_source,
                transformed_observation,
                partition,
                family,
                packet_index,
                packet_record,
            )
        )

    horizons = {}
    for horizon in HORIZONS:
        finite = finite_horizon_gram(
            partition.triangular,
            transformed_source,
            transformed_observation,
            horizon,
            packet_slices=partition.slices,
        )
        tails = []
        geometric_tails = []
        packet_exact = []
        for normalized, weighted, kappa, q, exact_packet in packet_states:
            tails.append(
                stein_tail_energy_upper(
                    normalized, weighted, kappa, horizon
                )
            )
            geometric_tails.append(
                geometric_tail_energy_upper(
                    normalized, weighted, kappa, horizon
                )
            )
            packet_exact.append(exact_packet)
        completion = make_completion(finite, tails)
        horizons[str(horizon)] = {
            "finite_fused_energy": finite.fused_energy,
            "finite_fused_energy_squared": finite.fused_energy_squared,
            "finite_packet_energies": [
                math.sqrt(max(0.0, value))
                for value in finite.packet_energy_squared
            ],
            "finite_gram_minimum_eigenvalue": float(
                np.min(np.linalg.eigvalsh(finite.gram))
            ),
            "tail_energies": tails,
            "geometric_tail_energies": geometric_tails,
            "tail_sum": float(sum(tails)),
            "geometric_tail_sum": float(sum(geometric_tails)),
            "phase_aware_upper": completion.phase_aware_upper,
            "packet_hybrid_absolute_upper": float(
                sum(completion.packet_hybrid_uppers)
            ),
            "packet_hybrid_uppers": list(completion.packet_hybrid_uppers),
            "maximum_tail_over_exact_packet": max(
                tail / max(exact, 1.0e-300)
                for tail, exact in zip(tails, packet_exact)
            ),
        }

    inherited_exact = float(inherited["exact_hardy_energy"])
    selected = horizons[str(SELECTED_HORIZON)]
    return {
        "exact_hardy_energy": exact,
        "rh59_metric_absolute_upper": float(
            horizons["0"]["phase_aware_upper"]
        ),
        "selected_horizon": SELECTED_HORIZON,
        "selected_phase_aware_upper": selected["phase_aware_upper"],
        "selected_phase_aware_upper_over_exact": selected[
            "phase_aware_upper"
        ]
        / max(exact, 1.0e-300),
        "selected_packet_hybrid_absolute_upper": selected[
            "packet_hybrid_absolute_upper"
        ],
        "horizons": horizons,
        "maximum_schur_reconstruction_defect": partition.reconstruction_defect,
        "maximum_schur_unitary_defect": partition.unitary_defect,
        "maximum_local_metric_residual": max(
            block.residual_relative for block in family.blocks
        ),
        "maximum_normalized_contraction": max(
            state[3] for state in packet_states
        ),
        "rh59_exact_relative_defect": abs(exact - inherited_exact)
        / max(inherited_exact, 1.0e-300),
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
    right_source = coupling_c.conjugate().T / np.linalg.norm(
        coupling_c, "fro"
    )
    left_observation = u.T
    right_observation = np.asarray(coarse_data["complement"]).conjugate().T
    return {
        "sigma": sigma,
        "fine_dimension": fine_dimension,
        "coarse_dimension": fine_dimension // 2,
        "fine_dimension_times_sigma": fine_dimension * sigma,
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
        (RH59 / "results" / "flag_metric_pilot.json").read_text(
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
                    "left_phase_aware": row["left"][
                        "selected_phase_aware_upper"
                    ],
                    "right_exact": row["right"]["exact_hardy_energy"],
                    "right_phase_aware": row["right"][
                        "selected_phase_aware_upper"
                    ],
                    "elapsed_seconds": row["elapsed_seconds"],
                },
                sort_keys=True,
            ),
            flush=True,
        )

    payload = {
        "status": "binary64_phase_aware_finite_horizon_stein_tail_audit",
        "evidence_level": (
            "deterministic all-column dense binary64 finite-horizon packet "
            "Gram and inherited flag-metric tail audit; not interval validated"
        ),
        "fine_resolution": FINE_RESOLUTION,
        "hardy_radius": HARDY_RADIUS,
        "radial_cuts": list(RADIAL_CUTS),
        "radial_names": list(RADIAL_NAMES),
        "horizons": list(HORIZONS),
        "selected_horizon": SELECTED_HORIZON,
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
            "rh59_pilot": {
                "path": str(
                    (RH59 / "results" / "flag_metric_pilot.json").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH59 / "results" / "flag_metric_pilot.json"
                ),
            },
            "rh59_algebra": {
                "path": str(
                    (RH59 / "src" / "flag_stein" / "algebra.py").relative_to(
                        REPOSITORY
                    )
                ),
                "sha256": sha256_file(
                    RH59 / "src" / "flag_stein" / "algebra.py"
                ),
            },
        },
        "rows": rows,
        "fits": {
            "left_exact": fit_power(rows, ("left", "exact_hardy_energy")),
            "right_exact": fit_power(rows, ("right", "exact_hardy_energy")),
            "left_phase_aware": fit_power(
                rows, ("left", "selected_phase_aware_upper")
            ),
            "right_phase_aware": fit_power(
                rows, ("right", "selected_phase_aware_upper")
            ),
            "left_horizon_16": fit_horizon(rows, "left", 16),
            "right_horizon_16": fit_horizon(rows, "right", 16),
        },
        "limitations": [
            "Production Schur forms, inherited metrics, and finite Grams are binary64 diagnostics, not interval enclosures.",
            "The finite-horizon Gram is exact only for the stored finite matrix; no continuum phase-coherence theorem is proved.",
            "The tail certificate inherits RH-59 packet metrics and their nonuniform hierarchical weights.",
            "The selected horizon L=32 is fixed for this five-scale audit, not a proved physical-family horizon.",
            "Five levels do not prove a dyadically uniform Hardy budget; Stage A1 and Stage A4 remain open.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "phase_tail_pilot_smoke.json"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(output.relative_to(ROOT))}, sort_keys=True))


def fit_horizon(
    rows: list[dict[str, object]], side: str, horizon: int
) -> dict[str, float]:
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(
        np.asarray(
            [
                float(
                    row[side]["horizons"][str(horizon)]["phase_aware_upper"]
                )
                for row in rows
            ]
        )
    )
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


if __name__ == "__main__":
    main()
