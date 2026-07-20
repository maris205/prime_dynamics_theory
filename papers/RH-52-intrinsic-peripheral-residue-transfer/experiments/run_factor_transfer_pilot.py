"""Five-scale intrinsic peripheral-factor and residue audit for RH-52."""

from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
RH48 = PAPERS / "RH-48-intrinsic-riesz-identification"
RH49 = PAPERS / "RH-49-directional-reduced-resolvent"
RH50 = PAPERS / "RH-50-two-pole-hilbert-schmidt-hardy"
for path in (
    ROOT / "src",
    RH14 / "src",
    RH47 / "experiments",
    RH48 / "experiments",
    RH50 / "experiments",
):
    sys.path.insert(0, str(path))

from factor_transfer import (  # noqa: E402
    aggregate_left_masses,
    average_right_values,
    left_haar_detail_l2,
    left_mass_norms,
    normalize_l1,
    normalize_linf,
    rank_one_difference_frobenius,
    rank_one_frobenius,
    right_value_norms,
)
from parity_boundary import sparse_folded_gaussian_matrix  # noqa: E402
from run_dyadic_identification_pilot import haar_compress_matrix  # noqa: E402
from run_peripheral_factor_pilot import resolve_factors  # noqa: E402
from run_two_pole_hardy_pilot import (  # noqa: E402
    biorthogonal_modes,
    coarse_from_fine,
    coupling_actions,
    fine_left_residue_norms,
    coarse_right_residue_norms,
)


OUTPUT = ROOT / "results" / "factor_transfer_pilot.json"
STABLE_AUDIT = RH49 / "results" / "coupling_stable_rank_pilot.json"
FULL_SIGMAS = (0.01, 0.004, 0.002, 0.001, 0.0005)
SMOKE_SIGMAS = (0.01, 0.004)
FINE_RESOLUTION = 20.48


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def align(reference: np.ndarray, candidate: np.ndarray) -> np.ndarray:
    """Align one complex factor with a reference by a unit phase."""

    ref = np.asarray(reference, dtype=np.complex128).reshape(-1)
    value = np.asarray(candidate, dtype=np.complex128).reshape(-1)
    pairing = np.vdot(value, ref)
    if abs(pairing) == 0.0:
        return value
    return value * pairing / abs(pairing)


def fit_power(rows, extractor) -> dict[str, float | int]:
    x = np.log(np.asarray([float(row["sigma"]) for row in rows]))
    y = np.log(np.asarray([float(extractor(row)) for row in rows]))
    slope, intercept = np.polyfit(x, y, 1)
    residual = y - (slope * x + intercept)
    return {
        "sigma_power": float(slope),
        "growth_exponent": float(max(0.0, -slope)),
        "vanishing_exponent": float(max(0.0, slope)),
        "log_intercept": float(intercept),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "levels": len(rows),
    }


def branch_factor_row(
    *,
    mode: str,
    index: int,
    right: np.ndarray,
    left: np.ndarray,
    eigenvalues: np.ndarray,
    sigma: float,
) -> dict[str, object]:
    dimension = right.shape[0]
    cell_width = 2.0 / dimension
    r = np.asarray(right[:, index])
    ell = np.asarray(left[:, index])
    right_norms = right_value_norms(r)
    left_norms = left_mass_norms(ell)
    detail = left_haar_detail_l2(ell)
    projector = rank_one_frobenius(r, ell)
    logarithm = math.log(1.0 / sigma)
    eigenvalue = complex(eigenvalues[index])
    smoothing_denominator = (
        sigma ** -0.5
        * left_norms.l1_or_linf
        / max(abs(eigenvalue), 1.0e-15)
    )
    return {
        "mode": mode,
        "eigenvalue_real": float(eigenvalue.real),
        "eigenvalue_imag": float(eigenvalue.imag),
        "right_linf": right_norms.l1_or_linf,
        "right_l2": right_norms.l2,
        "left_l1": left_norms.l1_or_linf,
        "left_l2": left_norms.l2,
        "weak_condition_product": (
            right_norms.l1_or_linf * left_norms.l1_or_linf
        ),
        "projector_frobenius": projector,
        "projector_square_over_log": projector * projector / logarithm,
        "left_detail_l2": detail,
        "left_detail_over_sharp_h_sigma_inverse": (
            detail / (cell_width * sigma ** -1.0)
        ),
        "left_detail_over_weak_h_sigma_minus_three_halves": (
            detail / (cell_width * sigma ** -1.5)
        ),
        "left_l2_over_weak_smoothing_scale": (
            left_norms.l2 / smoothing_denominator
        ),
    }


def adjacent_branch_row(
    *,
    mode: str,
    index: int,
    fine_right: np.ndarray,
    fine_left: np.ndarray,
    fine_eigenvalues: np.ndarray,
    coarse_right: np.ndarray,
    coarse_left: np.ndarray,
    coarse_eigenvalues: np.ndarray,
) -> dict[str, object]:
    aggregated_left = aggregate_left_masses(fine_left[:, index])
    coarse_left_l1 = normalize_l1(coarse_left[:, index])
    aggregated_left_l1 = align(
        coarse_left_l1, normalize_l1(aggregated_left)
    )
    averaged_right = average_right_values(fine_right[:, index])
    coarse_right_linf = normalize_linf(coarse_right[:, index])
    averaged_right_linf = align(
        coarse_right_linf, normalize_linf(averaged_right)
    )

    compressed_right = coarse_from_fine(fine_right[:, index])
    compressed_left = coarse_from_fine(fine_left[:, index])
    projector_difference = rank_one_difference_frobenius(
        coarse_right[:, index],
        coarse_left[:, index],
        compressed_right,
        compressed_left,
    )
    projector_norm = rank_one_frobenius(
        coarse_right[:, index], coarse_left[:, index]
    )
    return {
        "mode": mode,
        "left_l1_normalized_adjacent_error": float(
            np.sum(np.abs(coarse_left_l1 - aggregated_left_l1))
        ),
        "right_linf_normalized_adjacent_error": float(
            np.max(np.abs(coarse_right_linf - averaged_right_linf))
        ),
        "eigenvalue_adjacent_error": float(
            abs(
                complex(fine_eigenvalues[index])
                - complex(coarse_eigenvalues[index])
            )
        ),
        "projector_frobenius_adjacent_defect": projector_difference,
        "projector_relative_adjacent_defect": (
            projector_difference / projector_norm
        ),
    }


def run_sigma(sigma: float, stable_rows) -> dict[str, object]:
    started = time.perf_counter()
    fine_dimension = max(
        128, 2 * int(round(FINE_RESOLUTION / sigma / 2.0))
    )
    coarse_dimension = fine_dimension // 2
    fine = sparse_folded_gaussian_matrix(fine_dimension, sigma)
    coarse = haar_compress_matrix(fine)
    fine_factors = resolve_factors(fine, sigma)
    coarse_factors = resolve_factors(coarse, sigma)
    fine_right, fine_left, fine_values, fine_gram = biorthogonal_modes(
        fine_factors
    )
    coarse_right, coarse_left, coarse_values, coarse_gram = (
        biorthogonal_modes(coarse_factors)
    )
    b, bt, c, _ = coupling_actions(fine)
    stable = min(
        stable_rows, key=lambda row: abs(float(row["sigma"]) - sigma)
    )
    b_hs = float(stable["B_hilbert_schmidt_norm"])
    c_hs = float(stable["C_hilbert_schmidt_norm"])
    h = 1.0 / coarse_dimension

    fine_residues = fine_left_residue_norms(
        right=fine_right,
        left=fine_left,
        b_transpose=bt,
        b_hilbert_schmidt=b_hs,
    )
    right_residues = coarse_right_residue_norms(
        right=coarse_right,
        left=coarse_left,
        c=c,
        c_hilbert_schmidt=c_hs,
    )
    branch_rows = []
    adjacent_rows = []
    right_image_rows = []
    for index, mode in enumerate(("perron", "parity")):
        branch_rows.append(
            branch_factor_row(
                mode=mode,
                index=index,
                right=fine_right,
                left=fine_left,
                eigenvalues=fine_values,
                sigma=sigma,
            )
        )
        adjacent_rows.append(
            adjacent_branch_row(
                mode=mode,
                index=index,
                fine_right=fine_right,
                fine_left=fine_left,
                fine_eigenvalues=fine_values,
                coarse_right=coarse_right,
                coarse_left=coarse_left,
                coarse_eigenvalues=coarse_values,
            )
        )
        image = c(coarse_right[:, index])
        physical_image = float(
            np.linalg.norm(image) / math.sqrt(coarse_dimension)
        )
        right_linf = right_value_norms(
            coarse_right[:, index]
        ).l1_or_linf
        right_image_rows.append(
            {
                "mode": mode,
                "C_right_image_physical_l2": physical_image,
                "C_right_image_over_h_sigma_inverse_linf": (
                    physical_image
                    / (h * sigma ** -1.0 * right_linf)
                ),
            }
        )

    row = {
        "sigma": float(sigma),
        "fine_dimension": fine_dimension,
        "coarse_dimension": coarse_dimension,
        "fine_dimension_times_sigma": fine_dimension * sigma,
        "coarse_cell_width_over_sigma": h / sigma,
        "fine_biorthogonality_defect": float(
            np.max(np.abs(fine_gram - np.eye(2)))
        ),
        "coarse_biorthogonality_defect": float(
            np.max(np.abs(coarse_gram - np.eye(2)))
        ),
        "B_hilbert_schmidt_norm": b_hs,
        "C_hilbert_schmidt_norm": c_hs,
        "B_hilbert_schmidt_over_h_sigma_minus_three_halves": (
            b_hs / (h * sigma ** -1.5)
        ),
        "C_hilbert_schmidt_over_h_sigma_minus_three_halves": (
            c_hs / (h * sigma ** -1.5)
        ),
        "fine_factor_branches": branch_rows,
        "adjacent_factor_transfer": adjacent_rows,
        "fine_left_residue_actions": fine_residues,
        "coarse_right_residue_actions": right_residues,
        "coarse_right_image_scales": right_image_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }
    del fine, coarse, fine_factors, coarse_factors
    gc.collect()
    return row


def branch_value(row, section: str, mode: str, field: str) -> float:
    item = next(
        value for value in row[section] if value["mode"] == mode
    )
    return float(item[field])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    stable = json.loads(STABLE_AUDIT.read_text(encoding="utf-8"))
    rows = []
    for sigma in (SMOKE_SIGMAS if args.smoke else FULL_SIGMAS):
        row = run_sigma(float(sigma), stable["rows"])
        rows.append(row)
        print(
            json.dumps(
                {
                    "sigma": row["sigma"],
                    "fine_dimension": row["fine_dimension"],
                    "parity_weak_condition": branch_value(
                        row,
                        "fine_factor_branches",
                        "parity",
                        "weak_condition_product",
                    ),
                    "parity_sharp_detail_ratio": branch_value(
                        row,
                        "fine_factor_branches",
                        "parity",
                        "left_detail_over_sharp_h_sigma_inverse",
                    ),
                    "fine_parity_residue": branch_value(
                        row,
                        "fine_left_residue_actions",
                        "parity",
                        "left_residue_action_over_B_hilbert_schmidt",
                    ),
                    "right_parity_residue": branch_value(
                        row,
                        "coarse_right_residue_actions",
                        "parity",
                        "right_residue_action_over_C_hilbert_schmidt",
                    ),
                },
                sort_keys=True,
            ),
            flush=True,
        )

    source_path = RH14 / "src" / "parity_boundary" / "operators.py"
    payload = {
        "status": (
            "floating_intrinsic_finite_factor_detail_and_direct_residue_transfer_audit"
        ),
        "evidence_level": (
            "binary64 sparse Perron/parity factors, exact Haar blocks, and direct rank-one residue actions; not interval validated"
        ),
        "fine_resolution_target": FINE_RESOLUTION,
        "sources": {
            "folded_gaussian": {
                "path": str(source_path.relative_to(REPOSITORY)),
                "sha256": sha256_file(source_path),
            },
            "stable_coupling_audit": {
                "path": str(STABLE_AUDIT.relative_to(REPOSITORY)),
                "sha256": sha256_file(STABLE_AUDIT),
            },
            "rh50_manuscript": {
                "path": str((RH50 / "main.tex").relative_to(REPOSITORY)),
                "sha256": sha256_file(RH50 / "main.tex"),
            },
        },
        "rows": rows,
        "fits": {
            "fine_perron_residue": fit_power(
                rows,
                lambda row: branch_value(
                    row,
                    "fine_left_residue_actions",
                    "perron",
                    "left_residue_action_over_B_hilbert_schmidt",
                ),
            ),
            "fine_parity_residue": fit_power(
                rows,
                lambda row: branch_value(
                    row,
                    "fine_left_residue_actions",
                    "parity",
                    "left_residue_action_over_B_hilbert_schmidt",
                ),
            ),
            "right_parity_residue": fit_power(
                rows,
                lambda row: branch_value(
                    row,
                    "coarse_right_residue_actions",
                    "parity",
                    "right_residue_action_over_C_hilbert_schmidt",
                ),
            ),
            "perron_sharp_detail_ratio": fit_power(
                rows,
                lambda row: branch_value(
                    row,
                    "fine_factor_branches",
                    "perron",
                    "left_detail_over_sharp_h_sigma_inverse",
                ),
            ),
            "parity_sharp_detail_ratio": fit_power(
                rows,
                lambda row: branch_value(
                    row,
                    "fine_factor_branches",
                    "parity",
                    "left_detail_over_sharp_h_sigma_inverse",
                ),
            ),
            "parity_projector": fit_power(
                rows,
                lambda row: branch_value(
                    row,
                    "fine_factor_branches",
                    "parity",
                    "projector_frobenius",
                ),
            ),
        },
        "limitations": [
            "The sparse matrices use an eight-sigma hard cutoff followed by exact row renormalization.",
            "All eigenfactors and singular quantities are binary64 and are not interval enclosures.",
            "The fixed N*sigma resolution tests a production discretization, not the asymptotic n*sigma^2 to infinity schedule.",
            "Adjacent weak factor differences compare two finite levels, not either factor with a validated continuum eigenfactor.",
            "Observed sharp h*sigma^(-1) detail transfer is not promoted to an analytic theorem.",
        ],
    }
    output = OUTPUT if not args.smoke else OUTPUT.with_name(
        "factor_transfer_pilot_smoke.json"
    )
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"output": str(output.relative_to(ROOT)), "fits": payload["fits"]},
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
