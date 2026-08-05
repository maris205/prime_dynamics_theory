"""Build the RH-364 exact reproduction and source-lock ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from weighted_prime_lift.core import (
    A,
    analytic_constants,
    exact_polynomial_coefficients,
    fixed_point_counts,
    primitive_orbit_counts,
    scalar_normalization_ledger,
    survivor_fixed_point_data,
    trace_formula_counts,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "henon_weighted_zeta/paper/sections/3_geometry_setup.tex":
        "491da4fa6c36366cc1c114e135a13ad872ea52a6ca9f203e72dba413b140dd88",
    "henon_weighted_zeta/paper/sections/B_contraction_proof.tex":
        "0ef59712ee231aac3023d15d3ec857cbedfea884b18be7ec1ac30459757e28a8",
    "henon_weighted_zeta/paper/sections/4_weighted_zeta.tex":
        "f9ba822409a29f06cce7e21a89c21a10a353267dcc396fd4573e48dde6e95443",
    "henon_weighted_zeta/paper/sections/5_certified_orbits.tex":
        "52bd65f7f144b4929c981743e0ab3a43c5f06446ea71be12dfcba1cf58d26656",
    "henon_weighted_zeta/paper/sections/7_discussion.tex":
        "bbc6c219546482beb8628ed022a491a6c68582356e88238e6f7529eb0e91906e",
    "henon_weighted_zeta/results/certified_domain_r059.json":
        "7d521ed68e843e356ce230bfb0e81b57bf1a67c2f1948e068dd26f20ac20c77b",
    "henon_prime_returns/paper/sections/07_discussion.tex":
        "21b819ef36bc1ff9fc43d30e4412bafeff34593d31e312ee0daf5e7a79328ba9",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/README.md":
        "81b52a85a982d54f1af75bbd22d859b1efae56b5136b263237c6c4511a1475bb",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/main.tex":
        "4e6bdede6775ff4e21fae928c40ce65aea1887e633684beabd5b4a75f8d7d5f3",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/THEOREM_LEDGER.md":
        "65be6e568ad30189757db695b2ae0baec93bc23ff47ecfd09ccca1703186d2aa",
    "prime_dynamics_theory/papers/RH-363-prime-return-entropy-tower/results/result.json":
        "e448b70e0fa04e8a8ac1a0be36e13e504564e641969d5512f1b8a50e5a935d01",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_manifest.json":
        "24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/results/four_volume_archive_verification.json":
        "b27f120f77c4bbf3afd3a4486fd800a8de93a2db52236c835809aa488d113751",
}

FOUR_VOLUME_VERIFICATION = (
    WORKSPACE
    / "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_verification.json"
)
CERTIFIED_DOMAIN = WORKSPACE / "henon_weighted_zeta/results/certified_domain_r059.json"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            value.update(chunk)
    return value.hexdigest()


def source_audit() -> dict[str, object]:
    rows = []
    for relative, expected in SOURCE_LOCKS.items():
        actual = digest(WORKSPACE / relative)
        rows.append(
            {
                "path": relative,
                "expected_sha256": expected,
                "actual_sha256": actual,
                "pass": actual == expected,
            }
        )
    return {"rows": rows, "pass": all(row["pass"] for row in rows)}


def foundation_audit() -> dict[str, object]:
    payload = json.loads(FOUR_VOLUME_VERIFICATION.read_text())
    expected = {
        "volume_count": 4,
        "numbered_source_count": 361,
        "archive_member_count": 73,
        "dependency_hash_count": 1548,
        "result_hash_count": 8,
        "failure_count": 0,
        "manifest_sha256":
            "24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897",
    }
    return {
        **expected,
        "pass": all(payload.get(key) == value for key, value in expected.items()),
    }


def selected_multiplier_data() -> dict[str, object]:
    payload = json.loads(CERTIFIED_DOMAIN.read_text())
    selected = payload["selected_orbits"]
    period_one = [row for row in selected if row["period"] == 1]
    period_three = [row for row in selected if row["period"] == 3]
    if len(period_one) != 1 or len(period_three) != 1:
        raise RuntimeError("certified fixed/period-three orbit multiplicity changed")
    return {
        "period_one_count": 1,
        "period_three_count": 1,
        "period_one_word": period_one[0]["canonical_word"],
        "period_three_word": period_three[0]["canonical_word"],
        "period_one_unstable_modulus": period_one[0]["unstable_modulus"],
        "period_three_unstable_modulus": period_three[0]["unstable_modulus"],
    }


def build_payload() -> dict[str, object]:
    source = source_audit()
    foundation = foundation_audit()
    multiplier_data = selected_multiplier_data()
    period_three_multiplier = float(multiplier_data["period_three_unstable_modulus"])
    fixed_counts = fixed_point_counts(12)
    primitive_counts = primitive_orbit_counts(12)
    constants = analytic_constants()
    scalar_rows = [
        scalar_normalization_ledger(beta, period_three_multiplier)
        for beta in (0.0, constants["beta_zero"] / 2.0, 1.0)
    ]

    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "prime_copy_is_finite_field_reduction": False,
        "prime_copy_is_hasse_weil_zeta": False,
        "prime_copy_is_full_H_p_zeta": False,
        "prime_copy_is_canonical_global_henon_operator": False,
        "prime_copy_det2_is_physical_noisy_det2": False,
        "weighted_normalized_product_near_s_one_for_all_beta": False,
        "flat_correction_continues_full_euler_determinant": False,
        "finite_section_root_is_certified": False,
        "von_mangoldt_trace_proved": False,
        "hilbert_polya_constructed": False,
        "self_adjoint_generator_constructed": False,
        "intrinsic_T_log_T_proved": False,
        "riemann_zeros_spectrally_identified": False,
        "zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }

    return {
        "status": "RH-364_weighted_henon_prime_lift_cubic_trace_obstruction",
        "source_commits": {
            "prime_dynamics_theory_rh363_release":
                "863aeaadedccb178a3fa9aaeb06ed0a4d33981d3",
            "henon_weighted_zeta":
                "ff44f961261349848c9f65ede6a031b7e155aca9",
            "henon_prime_returns":
                "c37d191672d30de49b2054be3a03cf2db068694f",
        },
        "source_audit": source,
        "four_volume_foundation_audit": foundation,
        "finite_checks": {
            "adjacency_matrix": [list(row) for row in A],
            "characteristic_polynomial_factors": [
                "lambda^2-lambda-1",
                "lambda^2+1",
            ],
            "det_I_minus_zA_coefficients": exact_polynomial_coefficients(),
            "fixed_point_counts_1_to_12": fixed_counts,
            "trace_formula_counts_1_to_12": trace_formula_counts(12),
            "trace_formula_match": fixed_counts == trace_formula_counts(12),
            "primitive_orbit_counts_1_to_12": primitive_counts,
            "expected_primitive_counts_match": primitive_counts
            == [1, 0, 1, 2, 2, 2, 4, 5, 8, 11, 18, 25],
            "first_trace_ledger": fixed_counts[:3],
            "first_primitive_ledger": primitive_counts[:3],
            "certified_multiplier_rows": multiplier_data,
            "survivor_fixed_point": survivor_fixed_point_data(),
            "analytic_constants": constants,
            "scalar_normalization_rows": scalar_rows,
            "all_scalar_rows_Q1_Q2_match": all(
                abs(row["Q1"] - 1.0) < 1e-14 and abs(row["Q2"] - 1.0) < 1e-14
                for row in scalar_rows
            ),
            "all_scalar_rows_Q3_exceed_one": all(row["Q3"] > 1.0 for row in scalar_rows),
        },
        "theorem_flags": {
            "weighted_euler_certified_disk_and_tail": True,
            "flat_correction_larger_zero_free_disk": True,
            "prime_copy_exact_schatten_regions": True,
            "ordinary_fredholm_identity_only_Re_s_greater_1": True,
            "regularized_determinants_on_m_Re_s_greater_1": True,
            "scalar_zeta_factorization": True,
            "natural_weighted_fractional_singularity_beta_positive": True,
            "scalar_normalization_cube_obstruction_all_beta_nonnegative": True,
            "normalized_near_s_one_only_beta_below_beta_zero": True,
        },
        "route": {
            "route_A": "GO",
            "route_B": "STOP_SCOPED",
            "route_B_first_fatal_mismatch":
                "engineered_prime_copy_is_not_a_canonical_global_operator",
            "route_B_second_fatal_mismatch":
                "prime_cube_trace_weight_is_four_not_one",
            "trigger_5_independent_theorem_edge": True,
            "triggers_1_to_4_touched": False,
            "physical_route_coordinate":
                "actual_same_clock_unnormalized_head_transport_open",
            "four_volume_foundation_preserved": True,
        },
        "gates": gates,
        "false_claims": false_claims,
        "finite_rows_are_reproduction_only": True,
    }


def main() -> None:
    payload = build_payload()
    if not payload["source_audit"]["pass"]:
        raise SystemExit("source-lock mismatch")
    if not payload["four_volume_foundation_audit"]["pass"]:
        raise SystemExit("four-volume foundation mismatch")
    finite = payload["finite_checks"]
    required = (
        finite["trace_formula_match"],
        finite["expected_primitive_counts_match"],
        finite["first_trace_ledger"] == [1, 1, 4],
        finite["first_primitive_ledger"] == [1, 0, 1],
        finite["all_scalar_rows_Q1_Q2_match"],
        finite["all_scalar_rows_Q3_exceed_one"],
        not any(payload["gates"].values()),
        not any(payload["false_claims"].values()),
    )
    if not all(required):
        raise SystemExit("finite theorem ledger mismatch")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass": True, "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
