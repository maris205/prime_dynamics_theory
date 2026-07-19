"""Build the RH-47 logarithmic-conditioning theorem certificate."""

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
RH42 = PAPERS / "RH-42-uniform-euclidean-parity-contour"
RH44 = PAPERS / "RH-44-validated-rank-two-peripheral-complement"
RH46 = PAPERS / "RH-46-small-noise-mesh-double-pole"
sys.path.insert(0, str(ROOT / "src"))

from peripheral_conditioning import (  # noqa: E402
    anchored_bulk_ledger,
    endpoint_log_coefficient,
    endpoint_tail_constant,
    power_schedule_closes,
)


OUTPUT = ROOT / "results" / "logarithmic_peripheral_conditioning_certificate.json"
PILOT = ROOT / "results" / "small_noise_peripheral_factor_pilot.json"
SIGMAS = (0.03, 0.02, 0.01, 0.004, 0.002, 0.001, 0.0005, 0.0002, 0.0001)
POWERS = (1.5, 2.0, 2.25, 2.5)


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


def load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def schedule_dimension(sigma: float, power: float) -> int:
    return max(
        2,
        int(math.ceil(65536.0 * (0.01 / float(sigma)) ** float(power))),
    )


def main() -> None:
    rh14_summary_path = (
        RH14 / "results" / "square_root_boundary_layer_summary.json"
    )
    rh42_path = (
        RH42 / "results" / "uniform_euclidean_parity_certificate.json"
    )
    rh44_path = (
        RH44
        / "results"
        / "validated_rank_two_peripheral_complement.json"
    )
    rh46_path = (
        RH46 / "results" / "small_noise_mesh_double_pole_certificate.json"
    )
    rh14 = load(rh14_summary_path)
    rh42 = load(rh42_path)
    rh44 = load(rh44_path)
    rh46 = load(rh46_path)
    pilot = load(PILOT)
    if rh14["theorem_target"]["law"] != (
        "1+lambda_-(sigma)=C_* sqrt(sigma)+o(sqrt(sigma))"
    ):
        raise RuntimeError("RH-14 small-noise parity branch is unavailable")
    if rh46["conditional_bulk_extension"]["proved_uniformly_in_sigma"]:
        raise RuntimeError("RH-46 peripheral gate was unexpectedly closed")
    if pilot["status"] != (
        "floating_small_noise_peripheral_factor_conditioning_pilot"
    ):
        raise RuntimeError("full peripheral factor pilot is unavailable")
    if float(pilot["rows"][-1]["sigma"]) != 1.0e-4:
        raise RuntimeError("the peripheral pilot does not reach sigma=1e-4")

    schedules = {}
    for power in POWERS:
        rows = {}
        for sigma in SIGMAS:
            dimension = schedule_dimension(sigma, power)
            rows[str(sigma)] = anchored_bulk_ledger(
                sigma,
                dimension,
                peripheral_size_constant=1.0,
                peripheral_error_constant=1.0,
            ).as_dict()
        schedules[str(power)] = {
            **power_schedule_closes(power),
            "dimension_law": f"ceil(65536*(0.01/sigma)^{power})",
            "rows": rows,
        }

    smallest = pilot["rows"][-1]
    payload = {
        "status": (
            "rigorous_logarithmic_peripheral_conditioning_anchored_bulk_mesh_and_intrinsic_identification_boundary"
        ),
        "scope": (
            "small-noise Perron and negative-parity weighted Riesz terms for the folded Gaussian band-merging family, plus continuum-anchored Galerkin deflation"
        ),
        "evidence_level": (
            "analytic_mesoscopic_endpoint_localization_rank_one_calculus_and_gaussian_derivative_bounds_plus_floating_sparse_factor_audit"
        ),
        "mesoscopic_endpoint_theorem": {
            "regime": "sigma/t -> 0 and t -> 0",
            "stationary_density": (
                "sqrt(t) pi_sigma(1-t) -> rho_c/(2 sqrt(u_c))"
            ),
            "signed_parity_density": (
                "-sqrt(t) g_sigma(1-t) -> rho_c/(2 sqrt(u_c))"
            ),
            "endpoint_tail_constant": endpoint_tail_constant(),
            "endpoint_squared_log_coefficient": endpoint_log_coefficient(),
            "proof_inputs": [
                "uniform central density lower and upper bounds",
                "Gaussian localization at x=sqrt(t/u_c)",
                "conditioned normalizer bounded between positive constants",
                "postcritical spike majorants from RH-14",
            ],
        },
        "peripheral_conditioning_theorem": {
            "stationary_density_l2": "Theta(sqrt(log(1/sigma)))",
            "signed_parity_density_l2": "Theta(sqrt(log(1/sigma)))",
            "perron_projector_hilbert_schmidt": (
                "Theta(sqrt(log(1/sigma)))"
            ),
            "parity_projector_hilbert_schmidt": (
                "Theta(sqrt(log(1/sigma)))"
            ),
            "rank_two_weighted_term_upper": (
                "O(sqrt(log(1/sigma)))"
            ),
            "regular_variation_index": 0.0,
            "bounded_in_L2": False,
            "pure_power_interpretation": (
                "O(sigma^-epsilon) for every epsilon>0, but not O(1)"
            ),
        },
        "resolvent_obstruction": {
            "circle_inequality": (
                "sup_Gamma ||(z-K_sigma)^-1|| >= ||P_sigma||/radius(Gamma)"
            ),
            "fixed_geometry_uniform_L2_resolvent": False,
            "forced_lower_growth": "Omega(sqrt(log(1/sigma)))",
            "reduced_resolvent_upper_determined": False,
            "rh46_beta_zero_as_uniform_O1": False,
            "polynomial_beta_identified": False,
        },
        "peripheral_kernel_derivatives": {
            "right_parity_observable": (
                "||h_sigma||_infinity=O(1), ||h_sigma'||_2=O(sigma^-1)"
            ),
            "left_densities": (
                "||pi_sigma'||_2+||g_sigma'||_2=O(sigma^-3/2)"
            ),
            "rank_two_source_derivative": (
                "O(sigma^-1 sqrt(log(1/sigma)))"
            ),
            "rank_two_target_derivative": "O(sigma^-3/2)",
            "cell_average_projection": (
                "||E_n Q_per,sigma E_n-Q_per,sigma||_S2=O(n^-1 sigma^-3/2)"
            ),
        },
        "continuum_anchored_bulk": {
            "definition": (
                "B_tilde_n,sigma=E_n K_sigma E_n-E_n Q_per,sigma E_n=E_n B_sigma E_n"
            ),
            "hilbert_schmidt_error": "O(n^-1 sigma^-3/2)",
            "hilbert_schmidt_size": "O(sigma^-1/2)",
            "square_trace_norm_error": (
                "O(n^-1 sigma^-2)+O(n^-2 sigma^-3)"
            ),
            "sufficient_power_law": "n(sigma) sigma^2 -> infinity",
            "critical_power": 2.0,
            "strict_power_condition": "p>2 for n(sigma)~sigma^-p",
        },
        "intrinsic_discrete_identification_boundary": {
            "defect": (
                "I_n,sigma=Q_per(E_n K_sigma E_n)-E_n Q_per(K_sigma) E_n"
            ),
            "controlled_here": False,
            "sufficient_next_bound": "||I_n,sigma||_S2=O(n^-1 sigma^-3/2)",
            "interpretation": (
                "spatial resolution is closed; identifying the actual discrete Riesz term remains a spectral problem"
            ),
        },
        "normalized_power_schedule_audit": schedules,
        "floating_pilot_summary": {
            "noise_levels": len(pilot["rows"]),
            "smallest_sigma": smallest["sigma"],
            "smallest_dimension": smallest["dimension"],
            "smallest_perron_projector_norm": smallest[
                "perron_projector_norm"
            ],
            "smallest_parity_projector_norm": smallest[
                "parity_projector_norm"
            ],
            "smallest_perron_contour_resolvent_lower": smallest[
                "perron_contour_resolvent_lower"
            ],
            "smallest_parity_contour_resolvent_lower": smallest[
                "parity_contour_resolvent_lower"
            ],
            "smallest_endpoint_perron_tail_coefficient": smallest[
                "endpoint_perron_tail_coefficient"
            ],
            "smallest_endpoint_parity_tail_coefficient": smallest[
                "endpoint_parity_tail_coefficient"
            ],
            "perron_log_fit": pilot["perron_log_fit"],
            "parity_log_fit": pilot["parity_log_fit"],
            "rank_two_log_fit": pilot["rank_two_log_fit"],
            "evidence_level": pilot["evidence_level"],
        },
        "dependencies": {
            "rh14_boundary_layer_manuscript": repository_entry(
                RH14 / "main.tex"
            ),
            "rh14_boundary_layer_summary": repository_entry(
                rh14_summary_path
            ),
            "rh14_boundary_layer_source": repository_entry(
                RH14 / "src" / "parity_boundary" / "boundary_layer.py"
            ),
            "rh14_operator_source": repository_entry(
                RH14 / "src" / "parity_boundary" / "operators.py"
            ),
            "rh42_fixed_noise_euclidean_contour": repository_entry(
                rh42_path
            ),
            "rh44_fixed_noise_rank_two_complement": repository_entry(
                rh44_path
            ),
            "rh46_small_noise_mesh_certificate": repository_entry(
                rh46_path
            ),
            "local_floating_factor_pilot": {
                "path": str(PILOT.relative_to(ROOT)),
                "sha256": sha256_file(PILOT),
            },
        },
        "limitations": [
            "The logarithmic theorem controls the L2 size of the peripheral factors and the fixed-contour resolvent from below; it does not prove a matching upper for the reduced resolvent.",
            "The continuum-anchored Galerkin bulk uses the compressed continuum weighted Riesz kernel, not the actual weighted Riesz term of the finite matrix.",
            "The actual discrete intrinsic identification defect is isolated explicitly and is not proved to satisfy the sufficient small-noise rate here.",
            "The displayed power ledgers normalize unknown theorem constants to one and certify exponents rather than numerical outward constants.",
            "Sparse eigenfactor slopes and endpoint coefficients are floating diagnostics, not validated enclosures.",
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
