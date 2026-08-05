"""Build the RH-362 finite reproduction and source-lock ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from prime_return_zeta.core import (
    A0,
    first_coordinates,
    gcd_sequence,
    local_cycle_trace,
    low_rank_prime_set,
    modular_return_rank,
    primes_up_to,
    return_divisibility_holds,
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
    "henon_prime_returns/paper/sections/07_discussion.tex":
        "21b819ef36bc1ff9fc43d30e4412bafeff34593d31e312ee0daf5e7a79328ba9",
    "dyna_zeta_map/paper/sections/3_5_core.tex":
        "177b22361ec0c674b0cd8e545dbf3c2a5b96a7445bff4ee100ab62085595a4aa",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_manifest.json":
        "24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897",
    "prime_dynamics_theory/papers/RH-MVP2-corpus-frontier-synthesis/"
    "results/four_volume_archive_verification.json":
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
        path = WORKSPACE / relative
        actual = digest(path)
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


def build_payload() -> dict[str, object]:
    primes = primes_up_to(43)
    ranks = {str(prime): modular_return_rank(A0, prime) for prime in primes}
    coordinates = first_coordinates(A0, 6)
    gcd_terms = gcd_sequence(A0, 6)
    low_rank = low_rank_prime_set(A0, 5)
    trace_rows = [
        {
            "prime": prime,
            "rank": ranks[str(prime)],
            "traces_n_1_to_8": [
                local_cycle_trace(ranks[str(prime)], power)
                for power in range(1, 9)
            ],
        }
        for prime in (2, 3, 5, 7, 11)
    ]
    source = source_audit()
    foundation = foundation_audit()
    escape_prefix_pass = (
        coordinates[:5] == [0, 1, -5, -150, -134994]
        and all(coordinates[index] < 0 for index in range(2, len(coordinates)))
        and all(
            abs(coordinates[index]) > abs(coordinates[index - 1])
            for index in range(3, len(coordinates))
        )
    )
    finite_checks = {
        "a0_first_coordinates": [str(value) for value in coordinates],
        "a0_gcd_terms": [str(value) for value in gcd_terms],
        "a0_escape_prefix_pass": escape_prefix_pass,
        "return_divisibility_primes_through_43_indices_through_12":
            return_divisibility_holds(A0, primes, 12),
        "low_rank_threshold": 5,
        "low_rank_primes_from_product": low_rank,
        "low_rank_primes_from_direct_ranks": sorted(
            prime for prime in primes if ranks[str(prime)] < 5
        ),
        "rank_bound_pass": all(ranks[str(prime)] <= prime * prime for prime in primes),
        "ranks_through_43": ranks,
        "trace_rows": trace_rows,
    }
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
        "clock_renormalization_is_intrinsic": False,
        "finite_rows_are_asymptotic_evidence": False,
        "global_fredholm_identity_on_all_Re_s_positive": False,
        "hilbert_polya_constructed": False,
        "physical_same_clock_D_4k_transport_proved": False,
        "rh241_moving_noisy_envelope_closed": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_spectrally_identified": False,
        "typed_q_or_E_off_closed": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }
    return {
        "status": "RH-362_prime_return_euler_dichotomy_and_clock_obstruction",
        "source_commits": {
            "prime_dynamics_theory_baseline":
                "10efbe0de1d08b512ae765d2c30230b23940f72a",
            "henon_prime_returns":
                "c37d191672d30de49b2054be3a03cf2db068694f",
            "dyna_zeta_map":
                "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
        },
        "source_audit": source,
        "four_volume_foundation_audit": foundation,
        "finite_checks": finite_checks,
        "theorem_flags": {
            "a0_nonperiodic_escape": True,
            "low_rank_prime_finiteness": True,
            "pointed_cycle_local_determinant": True,
            "formal_bouquet_zeta": True,
            "dirichlet_euler_product_holomorphic_zero_free_Re_s_positive": True,
            "dirichlet_coefficients_multiplicative_zero_one": True,
            "ordinary_and_absolute_abscissa_zero": True,
            "natural_cycle_operator_compact_Re_s_positive": True,
            "ordinary_fredholm_identity_only_proved_Re_s_greater_3": True,
            "s_zero_meromorphic_crossing_rejected": True,
            "periodic_seed_branch_is_finite_correction_of_zeta_Ns": True,
            "inverse_length_clock_forces_zeta_but_is_non_schatten": True,
        },
        "route": {
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
        finite["a0_escape_prefix_pass"],
        finite["return_divisibility_primes_through_43_indices_through_12"],
        finite["rank_bound_pass"],
        finite["low_rank_primes_from_product"]
        == finite["low_rank_primes_from_direct_ranks"],
    )
    if not all(required):
        raise SystemExit("finite reproduction failure")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": payload["status"], "pass": True}, sort_keys=True))


if __name__ == "__main__":
    main()
