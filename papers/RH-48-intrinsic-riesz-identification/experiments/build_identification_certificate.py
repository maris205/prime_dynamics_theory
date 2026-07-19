"""Compose the RH-48 Schur, dyadic, power-law, and floating ledgers."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH43 = PAPERS / "RH-43-validated-weighted-riesz-parity-kernel"
RH46 = PAPERS / "RH-46-small-noise-mesh-double-pole"
RH47 = PAPERS / "RH-47-logarithmic-peripheral-conditioning"
sys.path.insert(0, str(ROOT / "src"))

from intrinsic_identification import power_law_ledger  # noqa: E402


PILOT = ROOT / "results" / "dyadic_identification_pilot.json"
HIGH_RESOLUTION = (
    ROOT / "results" / "dyadic_identification_pilot_smoke.json"
)
OUTPUT = ROOT / "results" / "intrinsic_riesz_identification_certificate.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def local_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
    }


def fixed_resolution_fits(
    rows: list[dict[str, object]],
) -> dict[str, dict[str, float]]:
    result: dict[str, dict[str, float]] = {}
    count = len(rows[0]["adjacent_identification_defects"])
    for index in range(count):
        sigma = np.asarray([float(row["sigma"]) for row in rows])
        defects = np.asarray(
            [
                float(
                    row["adjacent_identification_defects"][index][
                        "weighted_defect_frobenius"
                    ]
                )
                for row in rows
            ]
        )
        resolutions = np.asarray(
            [
                float(
                    row["adjacent_identification_defects"][index][
                        "coarse_dimension_times_sigma"
                    ]
                )
                for row in rows
            ]
        )
        if float(np.max(resolutions) - np.min(resolutions)) > 1.0e-10:
            raise RuntimeError("fixed-resolution pilot rows are misaligned")
        slope, intercept = np.polyfit(np.log(sigma), np.log(defects), 1)
        fitted = slope * np.log(sigma) + intercept
        normalized = defects * resolutions**2
        result[f"{resolutions[0]:.2f}"] = {
            "fixed_n_sigma": float(resolutions[0]),
            "fitted_sigma_power": float(slope),
            "log_intercept": float(intercept),
            "maximum_log_residual": float(
                np.max(np.abs(np.log(defects) - fitted))
            ),
            "normalized_n_sigma_square_minimum": float(np.min(normalized)),
            "normalized_n_sigma_square_maximum": float(np.max(normalized)),
            "normalized_relative_spread": float(
                (np.max(normalized) - np.min(normalized))
                / np.mean(normalized)
            ),
        }
    return result


def joint_power_fit(
    rows: list[dict[str, object]],
) -> dict[str, float]:
    design = []
    response = []
    for row in rows:
        sigma = float(row["sigma"])
        for adjacent in row["adjacent_identification_defects"]:
            design.append(
                [
                    np.log(float(adjacent["coarse_dimension"])),
                    np.log(sigma),
                    1.0,
                ]
            )
            response.append(
                np.log(float(adjacent["weighted_defect_frobenius"]))
            )
    matrix = np.asarray(design)
    values = np.asarray(response)
    coefficient = np.linalg.lstsq(matrix, values, rcond=None)[0]
    residual = values - matrix @ coefficient
    return {
        "dimension_power": float(coefficient[0]),
        "sigma_power": float(coefficient[1]),
        "log_prefactor": float(coefficient[2]),
        "prefactor": float(np.exp(coefficient[2])),
        "maximum_log_residual": float(np.max(np.abs(residual))),
        "root_mean_square_log_residual": float(
            np.sqrt(np.mean(residual**2))
        ),
        "observations": int(values.size),
    }


def high_resolution_replay(
    pilot: dict[str, object], high: dict[str, object]
) -> dict[str, object]:
    base_by_sigma = {float(row["sigma"]): row for row in pilot["rows"]}
    comparisons = []
    for row in high["rows"]:
        sigma = float(row["sigma"])
        base = base_by_sigma[sigma]
        for resolution in (20.48, 10.24):
            base_level = min(
                base["adjacent_identification_defects"],
                key=lambda item: abs(
                    float(item["coarse_dimension_times_sigma"])
                    - resolution
                ),
            )
            high_level = min(
                row["adjacent_identification_defects"],
                key=lambda item: abs(
                    float(item["coarse_dimension_times_sigma"])
                    - resolution
                ),
            )
            base_value = float(base_level["weighted_defect_frobenius"])
            high_value = float(high_level["weighted_defect_frobenius"])
            comparisons.append(
                {
                    "sigma": sigma,
                    "coarse_dimension_times_sigma": resolution,
                    "base_fine_resolution": float(
                        pilot["fine_resolution_target"]
                    ),
                    "replay_fine_resolution": float(
                        high["fine_resolution_target"]
                    ),
                    "base_defect": base_value,
                    "replay_defect": high_value,
                    "relative_difference": abs(high_value - base_value)
                    / base_value,
                }
            )
    return {
        "comparisons": comparisons,
        "maximum_relative_difference": max(
            float(item["relative_difference"]) for item in comparisons
        ),
    }


def schedule_audit() -> dict[str, object]:
    result: dict[str, object] = {}
    for gamma in (0.0, 0.25, 0.5, 0.75):
        result[f"gamma={gamma:.2f}"] = {
            f"p={p:.2f}": power_law_ledger(p, gamma).as_dict()
            for p in (2.0, 2.05, 2.25, 2.5, 3.0)
        }
    return result


def main() -> None:
    pilot = load(PILOT)
    high = load(HIGH_RESOLUTION)
    rows = pilot["rows"]
    mesh_powers = [
        float(row["mesh_power_fits"]["weighted_rank_two"]["power"])
        for row in rows
    ]
    finest_rows = [row["adjacent_identification_defects"][0] for row in rows]

    rh43_bounds = RH43 / "src" / "weighted_kernel" / "bounds.py"
    rh46_certificate = (
        RH46
        / "results"
        / "small_noise_mesh_double_pole_certificate.json"
    )
    rh47_certificate = (
        RH47
        / "results"
        / "logarithmic_peripheral_conditioning_certificate.json"
    )
    rh47_manuscript = RH47 / "main.tex"
    dependencies = {
        "rh43_weighted_schur_source": repository_entry(rh43_bounds),
        "rh46_small_noise_mesh_certificate": repository_entry(
            rh46_certificate
        ),
        "rh47_logarithmic_conditioning_certificate": repository_entry(
            rh47_certificate
        ),
        "rh47_logarithmic_conditioning_manuscript": repository_entry(
            rh47_manuscript
        ),
        "local_dyadic_identification_pilot": local_entry(PILOT),
        "local_double_resolution_replay": local_entry(HIGH_RESOLUTION),
    }

    payload = {
        "status": (
            "rigorous_quadratic_schur_and_dyadic_reduction_with_directional_small_noise_gate"
        ),
        "scope": (
            "intrinsic Perron-plus-parity weighted-Riesz identification for nested cell-average Galerkin compressions of the folded-Gaussian operator"
        ),
        "evidence_level": {
            "analytic": (
                "exact Hilbert-space Schur identity, Hilbert-Schmidt directional bound, dyadic telescoping theorem, and conditional small-noise power theorem"
            ),
            "numerical": (
                "binary64 sparse eigendata on exact Haar-compressed finite matrices; not interval validated"
            ),
        },
        "exact_schur_identification": {
            "block_split": "K=[[A,B],[C,D]], A=E_n K E_n",
            "detail_resolvent": "R_D(z)=(z-D)^-1",
            "self_energy": "Sigma_n(z)=B R_D(z) C",
            "schur_inverse": "S_n(z)=(z-A-Sigma_n(z))^-1",
            "identity": (
                "E_n Q_Gamma(K) E_n-Q_Gamma(A)=(2 pi i)^-1 int_Gamma z S_n(z) B R_D(z) C (z-A)^-1 dz"
            ),
            "structural_order": (
                "quadratic in the coarse-detail couplings B and C"
            ),
            "global_full_resolvent_required": False,
        },
        "directional_bound": {
            "left_quantity": "sup_Gamma ||S_n(z) B_n||_S2",
            "right_quantity": "sup_Gamma ||C_n (z-A_n)^-1||",
            "symmetric_alternative": (
                "interchange the Hilbert-Schmidt and operator norms"
            ),
            "bound": (
                "length(Gamma)/(2 pi) max_Gamma|z| sup_Gamma||R_D(z)|| times the product of the two directional quantities"
            ),
            "why_weaker_than_global": (
                "only resolvent action on the two coupling ranges is charged"
            ),
        },
        "residue_reduced_split": {
            "formula": (
                "R(z)=Pi/(z-lambda)+R_circ(z), applied separately to the fine top-left and coarse resolvents"
            ),
            "continuum_residue_growth": "O(sqrt(log(1/sigma))) in L2",
            "coarse_residue_growth_required_for_corollary": (
                "O(sqrt(log(1/sigma))) uniformly over dyadic levels; not proved here"
            ),
            "uniform_reduced_directional_consequence": (
                "directional gain O(log(1/sigma)) after multiplying the two sides"
            ),
            "full_reduced_resolvent_upper_proved_here": False,
            "directional_reduced_resolvent_upper_proved_here": False,
        },
        "gaussian_block_scaling": {
            "detail_to_coarse_hilbert_schmidt": "O(n^-1 sigma^-3/2)",
            "coarse_to_detail_hilbert_schmidt": "O(n^-1 sigma^-3/2)",
            "double_detail_operator": "O(n^-2 sigma^-5/2)",
            "detail_resolvent_under_n_sigma_squared": "O(1)",
            "generic_self_energy": "O(n^-2 sigma^-3)",
        },
        "dyadic_telescoping": {
            "adjacent_defect": (
                "Delta_n=Q_per(A_n)-E_n Q_per(A_2n) E_n"
            ),
            "recursion": "I_n=Delta_n+E_n I_2n E_n",
            "series": (
                "I_n=sum_{j>=0} E_n Delta_(2^j n) E_n"
            ),
            "quadratic_geometric_factor": 4.0 / 3.0,
            "fixed_sigma_limit_input": (
                "standard compact Galerkin spectral convergence"
            ),
        },
        "conditional_small_noise_closure": {
            "directional_gain_condition": (
                "L_sigma=O(sigma^-gamma) uniformly over the two contours and all dyadic refinements"
            ),
            "identification_bound": (
                "||I_n,sigma||_S2=O(n^-2 sigma^-3 L_sigma)"
            ),
            "preserves_every_n_sigma_squared_schedule_when": "gamma<=1/2",
            "polylogarithmic_gain_case": (
                "||I_n,sigma||_S2=O(n^-2 sigma^-3 polylog(1/sigma)) and the defect is lower order than n^-1 sigma^-3/2"
            ),
            "general_pure_power_threshold": "p>max(2,3/2+gamma)",
            "unconditional_for_the_folded_gaussian_family_here": False,
        },
        "floating_exact_haar_audit": {
            "status": pilot["status"],
            "noise_levels": len(rows),
            "adjacent_defects": sum(
                len(row["adjacent_identification_defects"]) for row in rows
            ),
            "largest_dimension": max(
                int(level["dimension"])
                for row in rows
                for level in row["levels"]
            ),
            "largest_nonzeros": max(
                int(level["nonzeros"])
                for row in rows
                for level in row["levels"]
            ),
            "mesh_power_minimum": min(mesh_powers),
            "mesh_power_maximum": max(mesh_powers),
            "joint_power_fit": joint_power_fit(rows),
            "fixed_resolution_fits": fixed_resolution_fits(rows),
            "double_resolution_replay": high_resolution_replay(
                pilot, high
            ),
            "finest_resolution_rows": [
                {
                    "sigma": float(row["sigma"]),
                    "coarse_dimension": int(adjacent["coarse_dimension"]),
                    "coarse_dimension_times_sigma": float(
                        adjacent["coarse_dimension_times_sigma"]
                    ),
                    "weighted_defect_frobenius": float(
                        adjacent["weighted_defect_frobenius"]
                    ),
                    "normalized_n_sigma_square": float(
                        adjacent["weighted_defect_frobenius"]
                    )
                    * float(adjacent["coarse_dimension_times_sigma"]) ** 2,
                    "perron_defect_frobenius": float(
                        adjacent["branches"]["perron"][
                            "defect_frobenius"
                        ]
                    ),
                    "parity_defect_frobenius": float(
                        adjacent["branches"]["parity"][
                            "defect_frobenius"
                        ]
                    ),
                }
                for row, adjacent in zip(rows, finest_rows)
            ],
            "observed_candidate_law": "approximately C (n sigma)^-2",
            "candidate_law_is_a_theorem": False,
        },
        "power_schedule_audit": schedule_audit(),
        "dependencies": dependencies,
        "limitations": [
            "The exact Schur identity and dyadic telescoping theorem are unconditional operator statements, but their uniform small-noise application requires the displayed directional gain condition.",
            "No global or directional reduced L2 resolvent upper is proved for sigma tending to zero.",
            "The observed n^-2 sigma^-2 law is a binary64 finite-matrix fit and is not promoted to an analytic theorem.",
            "The sparse audit uses an eight-sigma cutoff, exact row renormalization, and floating eigensolvers; it is not an interval enclosure.",
            "The theorem concerns intrinsic peripheral identification and bulk-square approximation, not an arithmetic trace formula or prime-power identity.",
            "No zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, or Riemann-hypothesis conclusion is claimed.",
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
