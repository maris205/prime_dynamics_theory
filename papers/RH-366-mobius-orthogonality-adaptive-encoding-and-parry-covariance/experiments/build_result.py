"""Build the RH-366 exact finite, source-lock, and claim-boundary ledger."""

from __future__ import annotations

import hashlib
import json
from math import pi, sqrt
from pathlib import Path

from mobius_henon_dichotomy.core import (
    brute_force_extrema,
    capacity_extrema,
    covariance_rows,
    exceptional_score,
    exceptional_signs,
    graph_equivalence_count,
    is_admissible_signs,
    mobius_sieve,
    parry_variance_exact,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "henon_mobius_correlations/THEOREM_PACKAGE.md":
        "634fd9543ceab91c19766015141e83636d64213f131d5c1b098385ef68c3b102",
    "henon_mobius_correlations/paper/main.tex":
        "8b0bf994e599edf11aab758afced7c9c9d3f9a8145db2671bde77e1fe924bb7e",
    "henon_mobius_correlations/paper/main.pdf":
        "9d4294c2e56be39e22ccdb46a21f8278d2ebacf6f9d47ac8006b9ed8fae6885d",
    "henon_mobius_correlations/paper/sections/3_henon_setup.tex":
        "5bee8e61f615d674d92bafb9b00163003dc2f8b91b5c4e63316c46dd27980eb7",
    "henon_mobius_correlations/paper/sections/4_periodic_exceptional.tex":
        "172b8c422dddc0d1a721165449bcbdefbc348322978ed62bea08d931ed458f0a",
    "henon_mobius_correlations/paper/sections/5_parry_typical.tex":
        "045ff9554dae44d923255b8d33d0509b47e01335390839d2253effcad42cd5a7",
    "henon_mobius_correlations/paper/sections/6_capacity_audit.tex":
        "7c04a7c403ca1879f61e4238144d9044f77f05441fdfd3ccc76cc4c743ba2a37",
    "henon_mobius_correlations/research/refine-logs/R001_MOBIUS_DICHOTOMY_PROTOCOL.json":
        "1d6927ab8aecd3f59584ee90136b3b92a05a28cc946bcd8830b3a6b87547bd94",
    "henon_mobius_correlations/results/r001_deterministic.json":
        "b1a0561ee7b1f12b818f3d0b9892ff749942d1a807aeeff03edb491a8b6208ec",
    "henon_mobius_correlations/results/r001_ensembles.json":
        "2da9a0db7b06a4c84b9e15c5718bd2c2e1c69bd6d69d739f03ccd768131710d9",
    "henon_mobius_correlations/results/r001_analysis.json":
        "dd200dc9e2522026a69f03716369b0a25db9c6d97c7c30e93865d357013afcb5",
    "henon_mobius_correlations/results/r001_independent_check.json":
        "bf243698c18cc7d251b45c739ed952bc47c2409c0f7b0f57e4c9fe12d751d7a0",
    "henon_mobius_correlations/scripts/check_r001_independent.py":
        "2085f88c142103007a7cbab90d9369eea76131ba745c116311287b3fbee0f522",
    "henon_weighted_zeta/paper/main.pdf":
        "a4e4770fce02ebf906378b7e2f90465d016c7a2b15734238154cafe8508a9f42",
    "henon_weighted_zeta/paper/sections/B_contraction_proof.tex":
        "0ef59712ee231aac3023d15d3ec857cbedfea884b18be7ec1ac30459757e28a8",
    "henon_weighted_zeta/research/refine-logs/R059_EXPECTED_SYMBOLIC_WORDS.json":
        "6ad7fb768da0a5f8eaf2160062ed3b4b340fc5076db37e48c58aaf3a7f42533a",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/README.md":
        "4882c6d1efefff58d2ac6cd86699a111b91c2aa24e8f83e786ba5a0f17223ff3",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/main.tex":
        "44df56838023323b55fbb0e90e7b47d8d697686dbfddfb245ff3a5dd70917345",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/results/result.json":
        "2d02e456330fb5a7ca161b0cea58ae6f6781ad76c077599e98fd91485cc89478",
    "prime_dynamics_theory/papers/RH-365-prime-return-bouquet-height-radius-and-prime-order-anchors/README.md":
        "855c5e8a00dec31c23270aa3c400f295e934b7648ca47a7eee72e9548cf4dd99",
    "prime_dynamics_theory/papers/RH-365-prime-return-bouquet-height-radius-and-prime-order-anchors/results/result.json":
        "18d4f7f30533df2f741c53f402fdcae71f73c7da3dbc963c348be86b270ca55a",
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
        rows.append({
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "pass": actual == expected,
        })
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
    return {**expected, "pass": all(payload.get(key) == value for key, value in expected.items())}


def finite_checks() -> dict[str, object]:
    mu = mobius_sieve(64)
    direct, identity = exceptional_score(mu)

    capacity_rows = []
    for length in range(1, 13):
        dp_minimum, dp_maximum = capacity_extrema(mu[1:length + 1])
        brute_minimum, brute_maximum = brute_force_extrema(mu[1:length + 1])
        capacity_rows.append({
            "N": length,
            "dp_minimum": dp_minimum,
            "dp_maximum": dp_maximum,
            "brute_minimum": brute_minimum,
            "brute_maximum": brute_maximum,
            "pass": (dp_minimum, dp_maximum) == (brute_minimum, brute_maximum),
        })

    variance_rows = []
    for length in (4, 8, 12, 16):
        exact = parry_variance_exact(mu, length)
        a, b = exact.as_pair()
        numeric = exact.numeric()
        variance_rows.append({
            "N": length,
            "a": a,
            "b": b,
            "numeric": numeric,
            "nonnegative": numeric >= -1.0e-12,
            "sqrt5_bound": numeric <= sqrt(5.0) * length + 1.0e-12,
        })

    graph = graph_equivalence_count(8)
    signs = exceptional_signs(mu)
    return {
        "mobius_mu_1_to_24": mu[1:25],
        "graph_equivalence": graph,
        "exceptional_prefix": {
            "N": 64,
            "direct_score": direct,
            "identity_score": identity,
            "identity_pass": direct == identity,
            "admissible": is_admissible_signs(signs[1:]),
            "raw_correlation": direct / 64.0,
            "theorem_target": 4.0 / pi**2,
        },
        "covariance_rows": covariance_rows(10),
        "variance_rows_exact_Qsqrt5": variance_rows,
        "capacity_rows": capacity_rows,
        "all_capacity_rows_pass": all(row["pass"] for row in capacity_rows),
        "all_variance_rows_pass": all(
            row["nonnegative"] and row["sqrt5_bound"] for row in variance_rows
        ),
    }


def r001_diagnostic() -> dict[str, object]:
    source = WORKSPACE / "henon_mobius_correlations"
    deterministic = json.loads((source / "results/r001_deterministic.json").read_text())
    ensembles = json.loads((source / "results/r001_ensembles.json").read_text())
    analysis = json.loads((source / "results/r001_analysis.json").read_text())
    checker = json.loads((source / "results/r001_independent_check.json").read_text())
    exceptional = deterministic["exceptional_orbit"]["curve"][-1]
    capacity = deterministic["open_path_capacity"][-1]
    variance = deterministic["parry_variance"][-1]
    block = ensembles["block_shuffle_capacity"]
    ratio = (3.0 - sqrt(5.0)) / 2.0
    tolerance = 1.0e-15
    geometric_omission_density_bound = 2.0 * tolerance * ratio / (1.0 - ratio)
    return {
        "N": exceptional["N"],
        "exceptional_raw_sum": exceptional["raw_sum"],
        "exceptional_raw_correlation": exceptional["raw_correlation"],
        "open_minimum_raw_sum": capacity["minimum_raw_sum"],
        "open_maximum_raw_sum": capacity["maximum_raw_sum"],
        "open_absolute_capacity": capacity["absolute_capacity"],
        "variance_per_N_float_diagnostic": variance["variance_per_N"],
        "variance_evaluation_mode": "floating_geometric_cutoff_diagnostic",
        "upstream_geometric_tolerance": tolerance,
        "geometric_omission_bound_per_N_before_roundoff": geometric_omission_density_bound,
        "surrogate_count": len(block["rows"]),
        "surrogate_exceedances": block["exceedances"],
        "rank_p_value": block["rank_p_value"],
        "rank_test_significant_at_0p01": block["significant"],
        "analysis_rejects_natural_coupling":
            "exceptional natural coupling of the real Mobius ordering"
            in analysis["interpretation"]["not_supported"],
        "independent_checker_pass": checker["all_pass"],
        "independent_subset_replays": len(checker["shuffle_subset_replay"]),
        "finite_ordering_result": "SCOPED_NEGATIVE",
    }


def build_payload() -> dict[str, object]:
    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "local_survivor_is_full_henon_nonwandering_set": False,
        "positive_entropy_forces_mobius_correlation": False,
        "exceptional_point_is_selected_independently_of_mu": False,
        "adaptive_encoding_is_spontaneous_arithmetic_coupling": False,
        "exceptional_point_refutes_sarnak_zero_entropy_conjecture": False,
        "parry_typical_result_is_uniform_over_survivor": False,
        "periodic_result_is_uniform_in_growing_period": False,
        "capacity_limit_exists": False,
        "finite_capacity_plateau_is_asymptotic_constant": False,
        "float_variance_decimal_is_exact_algebraic_evaluation": False,
        "logarithmic_chowla_implies_declared_cesaro_limit": False,
        "mobius_orbit_average_is_von_mangoldt_trace": False,
        "canonical_spectral_determinant_constructed": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_spectrally_identified": False,
        "completed_zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }
    return {
        "status": "RH-366_mobius_orthogonality_adaptive_encoding_and_parry_covariance",
        "source_commits": {
            "prime_dynamics_theory_rh365_release":
                "fbc8b00d38e0e83dafb10a1f1316ff8778039075",
            "henon_mobius_correlations":
                "34490443f50cfe9af9ff93888e51e7e7e534a5a7",
            "henon_weighted_zeta":
                "ff44f961261349848c9f65ede6a031b7e155aca9",
        },
        "source_audit": source_audit(),
        "four_volume_foundation_audit": foundation_audit(),
        "finite_checks": finite_checks(),
        "r001_diagnostic": r001_diagnostic(),
        "theorem_flags": {
            "fixed_periodic_orbit_orthogonality": True,
            "parry_almost_sure_simultaneous_continuous_observable_orthogonality": True,
            "offline_mobius_adapted_correlation_four_over_pi_squared": True,
            "exact_parry_covariance": True,
            "unconditional_variance_bound_sqrt5_N": True,
            "ordinary_chowla_variance_density_limit_conditional": True,
            "linear_time_open_capacity_algorithm": True,
            "capacity_liminf_limsup_bracket": True,
            "finite_ordering_null_scoped_negative": True,
        },
        "route": {
            "route_A": "GO",
            "route_B": "STOP_SCOPED",
            "route_B_first_fatal_mismatch":
                "exceptional_initial_condition_is_chosen_after_reading_the_mobius_sequence",
            "route_B_second_fatal_mismatch":
                "orbit_correlations_are_not_operator_traces_or_von_mangoldt_ledgers",
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


def validate_payload_shape(payload: dict[str, object]) -> None:
    expected = {
        "status", "source_commits", "source_audit", "four_volume_foundation_audit",
        "finite_checks", "r001_diagnostic", "theorem_flags", "route", "gates",
        "false_claims", "finite_rows_are_reproduction_only",
    }
    if set(payload) != expected:
        raise RuntimeError("result top-level schema changed")
    if type(payload["status"]) is not str:
        raise TypeError("status must be a string")
    for key in expected - {"status", "finite_rows_are_reproduction_only"}:
        if type(payload[key]) is not dict:
            raise TypeError(f"{key} must be an object")
    if type(payload["finite_rows_are_reproduction_only"]) is not bool:
        raise TypeError("finite_rows_are_reproduction_only must be a boolean")


def main() -> None:
    payload = build_payload()
    validate_payload_shape(payload)
    finite = payload["finite_checks"]
    diagnostic = payload["r001_diagnostic"]
    required = (
        payload["source_audit"]["pass"],
        payload["four_volume_foundation_audit"]["pass"],
        finite["graph_equivalence"]["pass"],
        finite["exceptional_prefix"]["identity_pass"],
        finite["exceptional_prefix"]["admissible"],
        finite["all_capacity_rows_pass"],
        finite["all_variance_rows_pass"],
        diagnostic["independent_checker_pass"],
        diagnostic["surrogate_exceedances"] == 420,
        abs(diagnostic["rank_p_value"] - 421 / 1024) < 1.0e-16,
        diagnostic["finite_ordering_result"] == "SCOPED_NEGATIVE",
        not any(payload["gates"].values()),
        not any(payload["false_claims"].values()),
    )
    if not all(required):
        raise SystemExit("RH-366 theorem, source, or firewall ledger mismatch")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass": True, "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
