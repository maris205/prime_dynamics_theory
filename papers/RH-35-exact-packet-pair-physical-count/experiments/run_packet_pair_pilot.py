"""Floating packet-pair and physical two-step spectrum pilot for RH-35."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import eigvals, norm


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH24 = PAPERS / "RH-24-contour-feshbach-root-count"
RH25 = PAPERS / "RH-25-directional-rouche-closure"
RH28 = PAPERS / "RH-28-arcwise-rational-arnoldi-enclosure"
RH33 = PAPERS / "RH-33-certified-complement-resolvent-atlas"
sys.path[:0] = [
    str(RH24 / "src"),
    str(RH24 / "experiments"),
    str(RH25 / "src"),
    str(RH25 / "experiments"),
]

import run_contour_feshbach_audit as rh24  # noqa: E402
import run_global_resolvent_probe as rh25_global  # noqa: E402


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def spectral_summary(
    values: np.ndarray, center: complex, radius: float
) -> dict[str, object]:
    signed = np.abs(values - center) - radius
    order = np.argsort(np.abs(signed))
    return {
        "inside_count": int(np.count_nonzero(signed < 0.0)),
        "boundary_clearance": float(np.min(np.abs(signed))),
        "spectral_radius": float(np.max(np.abs(values))),
        "near_zero_count_1e-10": int(np.count_nonzero(np.abs(values) < 1.0e-10)),
        "nearest": [
            {
                "real": float(values[index].real),
                "imag": float(values[index].imag),
                "signed_boundary_distance": float(signed[index]),
            }
            for index in order[:12]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sigma", type=float, default=1.0e-2)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    sigma = float(arguments.sigma)
    settings = rh24.physical_settings()[sigma]

    begun = time.perf_counter()
    environment = rh25_global.build_environment(sigma, settings)
    environment_seconds = time.perf_counter() - begun
    matrix = environment["matrix"]
    spectrum = environment["spectrum"]
    synthesis = np.asarray(environment["synthesis"])
    analysis = np.asarray(environment["analysis"])
    dimension = int(matrix.shape[0])
    rank = int(analysis.shape[0])
    _, two_step = rh24.bulk_operator(matrix, spectrum)

    pair_gram = analysis @ synthesis
    pair_defect = pair_gram - np.eye(rank)
    synthesis_norm = float(norm(synthesis, ord=2))
    analysis_norm = float(norm(analysis, ord=2))
    pair_defect_two_norm = float(norm(pair_defect, ord=2))
    low_rank_factor_bound = (
        synthesis_norm * pair_defect_two_norm * analysis_norm
    )

    begun = time.perf_counter()
    identity = np.eye(dimension, dtype=np.float64)
    physical = np.asarray(two_step(identity))
    assembly_seconds = time.perf_counter() - begun
    identity = None

    correction_right = physical @ synthesis
    corrected_physical = physical + correction_right @ pair_defect @ analysis
    perturbation = corrected_physical - physical
    perturbation_two_norm = float(norm(perturbation, ord=2))
    perturbation_frobenius = float(norm(perturbation, ord="fro"))
    perturbation_factor_bound = float(
        norm(correction_right, ord=2)
        * pair_defect_two_norm
        * analysis_norm
    )

    corrected_analysis = np.linalg.solve(pair_gram, analysis)
    analysis_correction = corrected_analysis - analysis
    original_external = np.eye(dimension) - synthesis @ analysis
    corrected_external = np.eye(dimension) - synthesis @ corrected_analysis
    external_correction = corrected_external - original_external
    original_direct = analysis @ physical @ synthesis
    corrected_direct = corrected_analysis @ physical @ synthesis
    original_forcing = original_external @ physical @ synthesis
    corrected_forcing = corrected_external @ physical @ synthesis
    original_observation = analysis @ physical @ original_external
    corrected_observation = (
        corrected_analysis @ physical @ corrected_external
    )
    original_complement = original_external @ physical @ original_external
    corrected_complement = (
        corrected_external @ physical @ corrected_external
    )
    physical_norm = float(norm(physical, ord=2))
    physical_on_synthesis_norm = float(
        norm(physical @ synthesis, ord=2)
    )
    physical_on_external_norm = float(
        norm(physical @ original_external, ord=2)
    )
    original_external_norm = float(norm(original_external, ord=2))
    original_direct_norm = float(norm(original_direct, ord=2))
    direct_correction_norm = float(
        norm(corrected_direct - original_direct, ord=2)
    )
    forcing_correction_norm = float(
        norm(corrected_forcing - original_forcing, ord=2)
    )
    observation_correction_norm = float(
        norm(corrected_observation - original_observation, ord=2)
    )
    complement_correction_norm = float(
        norm(corrected_complement - original_complement, ord=2)
    )
    original_forcing_norm = float(norm(original_forcing, ord=2))
    corrected_forcing_norm = float(norm(corrected_forcing, ord=2))
    original_observation_norm = float(norm(original_observation, ord=2))
    corrected_observation_norm = float(norm(corrected_observation, ord=2))

    parent_rows = {
        int(row["arc"]): row
        for row in read_csv(RH28 / "results" / "arcwise_contour_arcs.csv")
        if float(row["sigma"]) == sigma
    }
    leaf_rows = read_csv(
        RH33 / "results" / "refined_atlas_sigma_1e-02_leaves.csv"
    )
    gate_rows = []
    for leaf in leaf_rows:
        parent = parent_rows[int(leaf["parent_arc"])]
        complement_inverse = float(leaf["transported_inverse_upper"])
        stored_feshbach_full_ratio = float(
            parent["correction_ratio_upper"]
        ) + complement_inverse * float(
            parent["remainder_coefficient_upper"]
        )
        stored_feshbach_inverse = float(
            parent["projected_inverse_norm_upper"]
        ) / (1.0 - stored_feshbach_full_ratio)
        complement_product = (
            complement_inverse * complement_correction_norm
        )
        corrected_complement_inverse = complement_inverse / (
            1.0 - complement_product
        )
        feshbach_difference = (
            direct_correction_norm
            + observation_correction_norm
            * corrected_complement_inverse
            * corrected_forcing_norm
            + original_observation_norm
            * corrected_complement_inverse
            * complement_correction_norm
            * complement_inverse
            * corrected_forcing_norm
            + original_observation_norm
            * complement_inverse
            * forcing_correction_norm
        )
        gate_rows.append(
            {
                "parent_arc": int(leaf["parent_arc"]),
                "stored_complement_inverse": complement_inverse,
                "stored_feshbach_inverse": stored_feshbach_inverse,
                "stored_feshbach_full_ratio": stored_feshbach_full_ratio,
                "complement_neumann_product": complement_product,
                "corrected_feshbach_difference": feshbach_difference,
                "feshbach_rouche_product": (
                    stored_feshbach_inverse * feshbach_difference
                ),
            }
        )

    scale = next(
        row
        for row in read_csv(RH28 / "results" / "arcwise_scale_summary.csv")
        if float(row["sigma"]) == sigma
    )
    center = complex(
        float(scale["contour_center_real"]),
        float(scale["contour_center_imag"]),
    )
    radius = float(scale["contour_radius"])

    begun = time.perf_counter()
    physical_values = eigvals(
        physical.copy(), overwrite_a=True, check_finite=False
    )
    physical_eigensolve_seconds = time.perf_counter() - begun
    begun = time.perf_counter()
    corrected_values = eigvals(
        corrected_physical.copy(), overwrite_a=True, check_finite=False
    )
    corrected_eigensolve_seconds = time.perf_counter() - begun

    # The augmented block is similar to corrected_physical plus rank zeros
    # whenever J K is invertible.  This small singular-value diagnostic is
    # floating evidence for that exact algebraic decomposition.
    jk = np.eye(dimension) + synthesis @ pair_defect @ analysis
    jk_inverse_defect_candidate = float(
        1.0 - norm(jk - np.eye(dimension), ord=2)
    )

    payload = {
        "status": "floating_packet_pair_physical_count_pilot",
        "evidence_level": "floating_not_validated",
        "sigma": sigma,
        "dimension": dimension,
        "packet_rank": rank,
        "contour_center_real": center.real,
        "contour_center_imag": center.imag,
        "contour_radius": radius,
        "pair_gram": [
            [
                {
                    "real": float(pair_gram[row, column].real),
                    "imag": float(pair_gram[row, column].imag),
                }
                for column in range(rank)
            ]
            for row in range(rank)
        ],
        "pair_defect_two_norm": pair_defect_two_norm,
        "pair_defect_frobenius": float(norm(pair_defect, ord="fro")),
        "synthesis_two_norm": synthesis_norm,
        "analysis_two_norm": analysis_norm,
        "jk_minus_identity_factor_bound": low_rank_factor_bound,
        "jk_invertibility_lower_candidate": jk_inverse_defect_candidate,
        "physical_correction_two_norm": perturbation_two_norm,
        "physical_correction_frobenius": perturbation_frobenius,
        "physical_correction_factor_bound": perturbation_factor_bound,
        "physical_two_norm": physical_norm,
        "physical_on_synthesis_two_norm": physical_on_synthesis_norm,
        "physical_on_external_two_norm": physical_on_external_norm,
        "original_external_two_norm": original_external_norm,
        "original_direct_two_norm": original_direct_norm,
        "analysis_correction_two_norm": float(
            norm(analysis_correction, ord=2)
        ),
        "external_correction_two_norm": float(
            norm(external_correction, ord=2)
        ),
        "direct_correction_two_norm": direct_correction_norm,
        "forcing_correction_two_norm": forcing_correction_norm,
        "observation_correction_two_norm": observation_correction_norm,
        "complement_correction_two_norm": complement_correction_norm,
        "original_forcing_two_norm": original_forcing_norm,
        "corrected_forcing_two_norm": corrected_forcing_norm,
        "original_observation_two_norm": original_observation_norm,
        "corrected_observation_two_norm": corrected_observation_norm,
        "maximum_complement_neumann_product": max(
            row["complement_neumann_product"] for row in gate_rows
        ),
        "maximum_feshbach_rouche_product": max(
            row["feshbach_rouche_product"] for row in gate_rows
        ),
        "worst_feshbach_gate_leaf": max(
            gate_rows, key=lambda row: row["feshbach_rouche_product"]
        ),
        "physical": spectral_summary(physical_values, center, radius),
        "packet_corrected_physical": spectral_summary(
            corrected_values, center, radius
        ),
        "maximum_sorted_eigenvalue_matching_distance": float(
            np.max(
                np.abs(
                    np.sort_complex(physical_values)
                    - np.sort_complex(corrected_values)
                )
            )
        ),
        "environment_seconds": environment_seconds,
        "assembly_seconds": assembly_seconds,
        "physical_eigensolve_seconds": physical_eigensolve_seconds,
        "corrected_eigensolve_seconds": corrected_eigensolve_seconds,
    }
    output = arguments.output
    if output is None:
        output = (
            ROOT / "results" / f"floating_packet_pair_sigma_{sigma:.0e}.json"
        )
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    np.savez_compressed(
        output.with_suffix(".npz"),
        pair_gram=pair_gram,
        pair_defect=pair_defect,
        physical_eigenvalues=physical_values,
        corrected_eigenvalues=corrected_values,
        contour_center=np.asarray(center, dtype=np.complex128),
        contour_radius=np.asarray(radius, dtype=np.float64),
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
