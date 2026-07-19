"""Build the RH-46 mesh-law and double-pole theorem certificate."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
REPOSITORY = PAPERS.parent
RH14 = PAPERS / "RH-14-square-root-parity-boundary-layer"
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH16 = PAPERS / "RH-16-endpoint-gaussian-resolution-rank"
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH45 = PAPERS / "RH-45-bulk-two-step-trace-norm-determinant"
sys.path.insert(0, str(ROOT / "src"))

from small_noise_two_step import (  # noqa: E402
    DETERMINISTIC_LAMBDA,
    bulk_square_mesh_power,
    folded_gaussian_envelope,
    galerkin_resolution_ledger,
    gaussian_row_asymptotic_constant,
    normalizer_linear_lower,
    power_schedule_dimension,
)


OUTPUT = ROOT / "results" / "small_noise_mesh_double_pole_certificate.json"
SIGMAS = (0.03, 0.02, 0.01, 0.004, 0.002, 0.001, 0.0005, 0.0002, 0.0001)
POWERS = (1.0, 1.5, 2.0, 2.25, 2.5)
FIXED_DISK_RADIUS = 0.1
SHRINKING_DISK_MULTIPLE = 1.0


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repository_entry(path: Path) -> dict[str, str]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "sha256": sha256_file(path),
    }


def main() -> None:
    rh14 = load(
        RH14 / "results" / "square_root_boundary_layer_summary.json"
    )
    rh15 = load(RH15 / "results" / "bulk_scattering_summary.json")
    rh16 = load(RH16 / "results" / "endpoint_rank_audit.json")
    rh45 = load(
        RH45 / "results" / "bulk_trace_norm_determinant_certificate.json"
    )
    if rh14["theorem_target"]["law"] != (
        "1+lambda_-(sigma)=C_* sqrt(sigma)+o(sqrt(sigma))"
    ):
        raise RuntimeError("RH-14 parity bridge is not closed")
    if not rh15["analytic_results"]["naive_entire_limit"] is False:
        raise RuntimeError("RH-15 normal-family obstruction is missing")
    if rh45["status"] != (
        "rigorous_full_and_adaptive_bulk_square_trace_norm_and_determinant_convergence"
    ):
        raise RuntimeError("RH-45 fixed-noise determinant is not closed")

    envelope_rows = {
        str(sigma): folded_gaussian_envelope(sigma).as_dict()
        for sigma in SIGMAS
    }
    schedules: dict[str, object] = {}
    for power in POWERS:
        rows = {}
        for sigma in SIGMAS:
            dimension = power_schedule_dimension(sigma, power)
            fixed = galerkin_resolution_ledger(
                sigma,
                dimension,
                determinant_disk_radius=FIXED_DISK_RADIUS,
            )
            shrinking = galerkin_resolution_ledger(
                sigma,
                dimension,
                determinant_disk_radius=(
                    SHRINKING_DISK_MULTIPLE * sigma
                ),
            )
            rows[str(sigma)] = {
                "sigma": sigma,
                "dimension": dimension,
                "fixed_disk": fixed.as_dict(),
                "shrinking_disk": shrinking.as_dict(),
            }
        schedules[str(power)] = {
            "power": power,
            "dimension_law": (
                f"ceil(65536*(0.01/sigma)^{power})"
            ),
            "hilbert_schmidt_leading_exponent": power - 1.5,
            "square_trace_norm_leading_exponent": power - 2.0,
            "shrinking_disk_determinant_leading_exponent": power - 1.0,
            "hilbert_schmidt_converges": power > 1.5,
            "square_trace_norm_converges": power > 2.0,
            "shrinking_disk_determinant_bound_converges": power > 1.0,
            "rows": rows,
        }

    determinant_lambda = float(DETERMINISTIC_LAMBDA)
    payload = {
        "status": (
            "rigorous_markov_mesh_laws_two_step_double_pole_obstruction_and_conditional_bulk_route"
        ),
        "scope": (
            "folded Gaussian Markov Galerkin families for 0<sigma<=0.03, "
            "plus the intrinsic bulk two-step small-noise determinant germ"
        ),
        "evidence_level": (
            "analytic_uniform_gaussian_moment_bounds_plus_exact_prior_deterministic_factorization"
        ),
        "uniform_gaussian_envelope": {
            "sigma_maximum": 0.03,
            "normalizer_linear_lower": normalizer_linear_lower(0.03),
            "kernel_hilbert_schmidt_law": "O(sigma^-1/2)",
            "combined_first_derivative_law": "O(sigma^-3/2)",
            "cell_average_galerkin_error_law": (
                "O(n^-1 sigma^-3/2)"
            ),
            "gaussian_row_sharp_asymptotic_constant": (
                gaussian_row_asymptotic_constant()
            ),
            "rows": envelope_rows,
        },
        "raw_markov_resolution_theorems": {
            "one_step_hilbert_schmidt_sufficient_condition": (
                "n(sigma)*sigma^(3/2)->infinity"
            ),
            "two_step_trace_norm_sufficient_condition": (
                "n(sigma)*sigma^2->infinity"
            ),
            "shrinking_disk_radius": "R_sigma=rho*sigma",
            "shrinking_disk_determinant_sufficient_condition": (
                "n(sigma)*sigma->infinity"
            ),
            "fixed_disk_standard_bound": (
                "requires n sigma^2 to dominate exp(C_R/sigma); this is "
                "a sufficient continuity bound, not a necessity theorem"
            ),
        },
        "power_schedule_audit": schedules,
        "conditional_bulk_extension": {
            "condition_name": "uniform_peripheral_transport_condition",
            "assumption": (
                "||Q_per,sigma||_HS=O(sigma^-q) and "
                "||Q_per,n,sigma-Q_per,sigma||_HS="
                "O(n^-1 sigma^-r)"
            ),
            "one_step_bulk_error_power": "max(3/2,r)",
            "bulk_size_power": "max(1/2,q)",
            "two_step_bulk_mesh_power": "max(1/2,q)+max(3/2,r)",
            "matched_markov_case_q_1_2_r_3_2": bulk_square_mesh_power(
                0.5, 1.5
            ),
            "moving_contour_resolvent_corollary": {
                "premise": (
                    "contour geometry is O(1) and the continuum/discrete "
                    "resolvents are O(sigma^-beta)"
                ),
                "peripheral_size_power_q": "beta",
                "resolvent_identity_error_power_r": "3/2+2 beta",
                "sufficient_two_step_mesh_powers": {
                    str(beta): bulk_square_mesh_power(
                        beta, 1.5 + 2.0 * beta
                    )
                    for beta in (0.0, 0.25, 0.5, 1.0)
                },
            },
            "proved_uniformly_in_sigma": False,
            "fixed_sigma_1e_minus_2_closed_by_rh45": True,
        },
        "two_step_small_noise_obstruction": {
            "one_step_deterministic_bulk_factor": (
                "D_0,bulk,2(z)=G(z)/(1-z^2/lambda)"
            ),
            "one_step_simple_poles": [
                -math.sqrt(determinant_lambda),
                math.sqrt(determinant_lambda),
            ],
            "two_step_variable": "w=z^2",
            "two_step_factor": (
                "D_0,square(w)=H(w)/(1-w/lambda)^2"
            ),
            "two_step_double_pole": determinant_lambda,
            "numerator_holomorphic_nonzero_disk_radius": (
                determinant_lambda * determinant_lambda
            ),
            "coefficientwise_small_noise_bridge": True,
            "locally_uniform_entire_small_noise_limit": False,
            "family_locally_bounded_on_disks_R_gt_lambda": False,
        },
        "canonical_square_cloud_model": {
            "finite_section": "S_N(w)=Pi_N(w/lambda)^2",
            "ideal_cloud_size": "2N one-step resonances",
            "squared_zero_multiplicity": 2,
            "edge_scaling": (
                "S_N(lambda exp(s/(N+1)))/(N+1)^2 "
                "-> ((exp(s)-1)/s)^2"
            ),
            "endpoint_rank_clock": rh16["analytic_results"][
                "threshold_rank"
            ],
            "identification_with_actual_noisy_cloud": "floating_only",
        },
        "dependencies": {
            "rh14_square_root_summary": repository_entry(
                RH14
                / "results"
                / "square_root_boundary_layer_summary.json"
            ),
            "rh15_bulk_scattering_summary": repository_entry(
                RH15 / "results" / "bulk_scattering_summary.json"
            ),
            "rh15_bulk_scattering_manuscript": repository_entry(
                RH15 / "main.tex"
            ),
            "rh16_endpoint_rank_summary": repository_entry(
                RH16 / "results" / "endpoint_rank_audit.json"
            ),
            "rh42_fixed_noise_hilbert_envelope": repository_entry(
                RH42
                / "results"
                / "hilbert_schmidt_envelope_certificate.json"
            ),
            "rh45_fixed_noise_trace_determinant": repository_entry(
                RH45
                / "results"
                / "bulk_trace_norm_determinant_certificate.json"
            ),
        },
        "limitations": [
            "The explicit unconditional mesh theorem concerns the folded Gaussian Markov kernel and its cell-average Galerkin lift.",
            "Uniform small-noise weighted-Riesz contours and peripheral transport are stated as a separate condition and are not proved here.",
            "Midpoint, normalization, and adaptive cutoff have lower-order small-noise derivative scaling under the stated mesh laws, but the displayed explicit constants use the canonical cell-average lift.",
            "The fixed-disk determinant estimate is a deliberately coarse sufficient trace-ideal continuity bound and is not a necessary computational complexity law.",
            "The actual noisy resonance-cloud identification and residual normality remain conjectural; archived cloud comparisons are floating diagnostics.",
            "No arithmetic trace formula, prime-power identity, zeta-zero identification, self-adjoint Hilbert-Polya operator, T log T counting law, or Riemann-hypothesis claim is made.",
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
