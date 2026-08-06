"""Build the RH-365 exact reproduction, schema, and source-lock ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from prime_return_bouquet.core import (
    P0,
    bouquet_traces,
    certified_radius_bracket,
    distinct_prime_factors,
    finite_rank_table,
    first_coordinates,
    gcd_height_bounds,
    gcd_terms,
    height_bounds,
    height_value,
    logarithmic_majorant,
    midpoint_value,
    primitive_rank_counts,
    trace_envelope,
    zeta_coefficients,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "henon_prime_returns/PRIME_RETURN_THEOREMS.md":
        "02898f6f72250fd7c3729b0819caa288fc1fba591c4e67f19b842ca448cca49c",
    "henon_prime_returns/paper/sections/03_reversible_structure.tex":
        "17c635a6285a9b6782d3400b47cf3bd47ff31546366ca53cd1baac19a510330a",
    "henon_prime_returns/paper/sections/04_divisibility.tex":
        "919e61920432b3296bb50c6ee00449005068e5b7d20a7b733349695220b161d9",
    "henon_prime_returns/paper/sections/app_diagnostics.tex":
        "ceb93e2c7394c323b7e605c5ad10824b822f4e4e8305e5d9f7b02e738d88d705",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/README.md":
        "70842cfe7ef7b65b00de27b0280b866bbb56316d778a498133ab3a170e240722",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/main.tex":
        "1d3909ad8b97d6bb0fc8c861ae0c702908f992cd33c8c1a7a57349b2f8925ccc",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/THEOREM_LEDGER.md":
        "2fdf7ce5825230b613c0517c803b87c3ddc5179c9c36d1998c512ed930519ed4",
    "prime_dynamics_theory/papers/RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/results/result.json":
        "5edf4ed048e10a008f00a03d62a934630caba1724af529878910892cea7001fc",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/README.md":
        "4882c6d1efefff58d2ac6cd86699a111b91c2aa24e8f83e786ba5a0f17223ff3",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/main.tex":
        "44df56838023323b55fbb0e90e7b47d8d697686dbfddfb245ff3a5dd70917345",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/THEOREM_LEDGER.md":
        "1a1bbbf5355505cadfd478bd9119db116a451f645f80243f1f3d82f3377373c3",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/UPDATED_ROADMAP.md":
        "ca8e57f6d057e6d2e8df2c87c1fca9bc6a1f4cc1c90009cb41554a797402555f",
    "prime_dynamics_theory/papers/RH-364-weighted-henon-prime-lift-cubic-trace-obstruction/results/result.json":
        "2d02e456330fb5a7ca161b0cea58ae6f6781ad76c077599e98fd91485cc89478",
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


def finite_rows(maximum_order: int = 12) -> dict[str, object]:
    coordinates = first_coordinates(11)
    terms = gcd_terms(maximum_order)
    ranks = finite_rank_table(maximum_order)
    primitive_counts = primitive_rank_counts(maximum_order)
    traces = bouquet_traces(maximum_order)
    zeta = zeta_coefficients(maximum_order)

    midpoint_rows = []
    for order, term in enumerate(terms, start=1):
        midpoint = midpoint_value(order)
        midpoint_rows.append(
            {
                "order": order,
                "a_n": str(term),
                "midpoint": str(midpoint),
                "pass": term == midpoint,
            }
        )

    height_rows = []
    for index in range(2, 11):
        value = height_value(index)
        next_value = height_value(index + 1)
        lower, upper = height_bounds(index)
        height_rows.append(
            {
                "index": index,
                "b_n": str(value),
                "b_next": str(next_value),
                "quadratic_step_pass": 5 * value * value <= next_value <= 6 * value * value,
                "closed_bounds": {"lower": str(lower), "upper": str(upper)},
                "closed_bounds_pass": lower <= value <= upper,
            }
        )

    gcd_bound_rows = []
    for order in range(3, maximum_order + 1):
        lower, upper = gcd_height_bounds(order)
        value = terms[order - 1]
        gcd_bound_rows.append(
            {
                "order": order,
                "a_n": str(value),
                "lower": str(lower),
                "upper": str(upper),
                "pass": lower <= value <= upper,
            }
        )

    anchor_rows = []
    for order in (3, 5, 7, 11):
        value = terms[order - 1]
        factors = distinct_prime_factors(value)
        factor_ranks = [ranks[prime] for prime in factors]
        anchor_rows.append(
            {
                "odd_prime_order": order,
                "a_ell": str(value),
                "distinct_prime_factors": [str(prime) for prime in factors],
                "return_ranks": factor_ranks,
                "c_ell": len(factors),
                "T_ell": traces[order - 1],
                "all_factors_have_exact_rank": all(rank == order for rank in factor_ranks),
            }
        )

    raw_firewall_rows = []
    for order in (7, 11):
        raw_firewall_rows.append(
            {
                "order": order,
                "primitive_euler_exponent": primitive_counts[order - 1],
                "logarithmic_coefficient": traces[order - 1] // order,
                "raw_zeta_coefficient": zeta[order],
                "raw_coefficient_is_not_anchor": zeta[order] != primitive_counts[order - 1],
            }
        )

    return {
        "seed": list(P0),
        "first_coordinates_x_0_to_11": [str(value) for value in coordinates],
        "gcd_terms_a_1_to_12": [str(value) for value in terms],
        "midpoint_rows": midpoint_rows,
        "all_midpoint_rows_pass": all(row["pass"] for row in midpoint_rows),
        "height_rows": height_rows,
        "all_height_rows_pass": all(
            row["quadratic_step_pass"] and row["closed_bounds_pass"]
            for row in height_rows
        ),
        "gcd_height_bound_rows": gcd_bound_rows,
        "all_gcd_height_bounds_pass": all(row["pass"] for row in gcd_bound_rows),
        "rank_table_through_order_12": {str(prime): rank for prime, rank in sorted(ranks.items())},
        "primitive_rank_counts_c_1_to_12": primitive_counts,
        "bouquet_traces_T_1_to_12": traces,
        "trace_envelope_rows": [
            {
                "order": order,
                "T_n": traces[order - 1],
                "envelope": trace_envelope(order),
                "pass": traces[order - 1] <= trace_envelope(order),
            }
            for order in range(1, maximum_order + 1)
        ],
        "zeta_coefficients_q_0_to_12": zeta,
        "odd_prime_anchor_rows": anchor_rows,
        "all_odd_prime_anchor_rows_pass": all(
            row["all_factors_have_exact_rank"] for row in anchor_rows
        ),
        "raw_coefficient_firewall_rows": raw_firewall_rows,
        "all_raw_coefficient_firewalls_pass": all(
            row["raw_coefficient_is_not_anchor"] for row in raw_firewall_rows
        ),
        "analytic_certificate": {
            "origin_radius_bracket": certified_radius_bracket(),
            "majorant_at_one_half": logarithmic_majorant(0.5),
            "majorant_at_zero_point_six_five": logarithmic_majorant(0.65),
            "strict_disk": "abs(z)<2^(-1/2)",
        },
    }


def build_payload() -> dict[str, object]:
    source = source_audit()
    foundation = foundation_audit()
    finite = finite_rows()

    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "bouquet_is_full_H_p_zeta": False,
        "bouquet_is_hasse_weil_zeta": False,
        "bouquet_is_canonical_global_henon_operator": False,
        "T_n_is_hilbert_space_trace_of_naive_direct_sum": False,
        "analytic_product_is_naive_fredholm_determinant": False,
        "raw_zeta_coefficient_equals_prime_order_anchor": False,
        "odd_prime_anchor_proves_composite_zsigmondy": False,
        "prime_order_terms_are_proved_squarefree": False,
        "certified_disk_is_exact_radius": False,
        "unit_circle_natural_boundary_proved": False,
        "von_mangoldt_trace_proved": False,
        "hilbert_polya_constructed": False,
        "riemann_zeros_spectrally_identified": False,
        "completed_zeta_divisor_equality": False,
        "riemann_hypothesis_proved": False,
    }

    return {
        "status": "RH-365_prime_return_bouquet_height_radius_and_prime_order_anchors",
        "source_commits": {
            "prime_dynamics_theory_rh364_release":
                "ba4d11aab349d3301a713e4a6e4f16c0cd84d45a",
            "henon_prime_returns":
                "c37d191672d30de49b2054be3a03cf2db068694f",
        },
        "source_audit": source,
        "four_volume_foundation_audit": foundation,
        "finite_checks": finite,
        "theorem_flags": {
            "exact_reversibility_midpoint_identities": True,
            "two_sided_quadratic_height_scale": True,
            "explicit_two_sided_gcd_height_bounds": True,
            "all_order_bouquet_trace_envelope": True,
            "strict_zero_free_disk_abs_z_below_two_to_minus_half": True,
            "odd_prime_order_primitive_divisor_anchors": True,
            "primitive_anchor_is_log_euler_not_raw_coefficient": True,
            "origin_taylor_radius_bracket": True,
            "naive_direct_sum_noncompact_and_non_schatten": True,
        },
        "route": {
            "route_A": "GO",
            "route_B": "STOP_SCOPED",
            "route_B_first_fatal_mismatch":
                "marked_cycles_across_distinct_finite_fields_are_not_a_canonical_global_operator",
            "route_B_second_fatal_mismatch":
                "fixed_point_counts_are_not_signed_von_mangoldt_operator_traces",
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
    expected_keys = {
        "status",
        "source_commits",
        "source_audit",
        "four_volume_foundation_audit",
        "finite_checks",
        "theorem_flags",
        "route",
        "gates",
        "false_claims",
        "finite_rows_are_reproduction_only",
    }
    if set(payload) != expected_keys:
        raise RuntimeError("result top-level schema changed")
    if not isinstance(payload["status"], str):
        raise TypeError("status must be a string")
    for key in expected_keys - {"status", "finite_rows_are_reproduction_only"}:
        if not isinstance(payload[key], dict):
            raise TypeError(f"{key} must be an object")
    if type(payload["finite_rows_are_reproduction_only"]) is not bool:
        raise TypeError("finite_rows_are_reproduction_only must be a boolean")


def main() -> None:
    payload = build_payload()
    validate_payload_shape(payload)
    finite = payload["finite_checks"]
    required = (
        payload["source_audit"]["pass"],
        payload["four_volume_foundation_audit"]["pass"],
        finite["all_midpoint_rows_pass"],
        finite["all_height_rows_pass"],
        finite["all_gcd_height_bounds_pass"],
        all(row["pass"] for row in finite["trace_envelope_rows"]),
        finite["all_odd_prime_anchor_rows_pass"],
        finite["all_raw_coefficient_firewalls_pass"],
        len(payload["false_claims"]) == 15,
        not any(payload["gates"].values()),
        not any(payload["false_claims"].values()),
    )
    if not all(required):
        raise SystemExit("RH-365 theorem or source ledger mismatch")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass": True, "status": payload["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
