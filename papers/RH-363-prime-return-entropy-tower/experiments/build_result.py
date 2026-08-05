"""Build the RH-363 finite reproduction and source-lock ledger."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from return_entropy_tower.core import (
    A0,
    normalized_entropy_fraction,
    pairwise_coprime,
    primes_up_to,
    return_power_moduli,
    return_rank_table,
    truncated_multiples_mobius_recovery,
    universal_first_defect,
)


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[2]
OUTPUT = ROOT / "results" / "result.json"

SOURCE_LOCKS = {
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "README.md":
        "70842cfe7ef7b65b00de27b0280b866bbb56316d778a498133ab3a170e240722",
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "main.tex":
        "1d3909ad8b97d6bb0fc8c861ae0c702908f992cd33c8c1a7a57349b2f8925ccc",
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "THEOREM_LEDGER.md":
        "2fdf7ce5825230b613c0517c803b87c3ddc5179c9c36d1998c512ed930519ed4",
    "prime_dynamics_theory/papers/"
    "RH-362-prime-return-euler-dichotomy-and-clock-renormalization-obstruction/"
    "results/result.json":
        "5edf4ed048e10a008f00a03d62a934630caba1724af529878910892cea7001fc",
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


def fraction_record(value) -> dict[str, object]:
    return {
        "numerator": str(value.numerator),
        "denominator": str(value.denominator),
        "decimal": float(value),
    }


def build_payload() -> dict[str, object]:
    primes = primes_up_to(29)
    ranks = return_rank_table(A0, primes)

    entropy_prefix_rows = []
    for level in (1, 2, 3):
        moduli = return_power_moduli(ranks, level)
        density = normalized_entropy_fraction(moduli)
        entropy_prefix_rows.append(
            {
                "tower_level": level,
                "prime_prefix_maximum": primes[-1],
                "modulus_count": len(moduli),
                "pairwise_coprime": pairwise_coprime(moduli),
                "normalized_entropy_density": fraction_record(density),
                "finite_zeta_radius": 2.0 ** (-float(density)),
            }
        )

    first_defect_rows = []
    expected_triples = {1: (2, 3, 1), 2: (6, 13, 2), 3: (30, 4501, 150)}
    for level in (1, 2, 3):
        for prime_count in (1, 2, 3):
            prefix = dict(list(ranks.items())[:prime_count])
            row = universal_first_defect(prefix, level)
            expected = expected_triples[prime_count]
            row.update(
                {
                    "tower_level": level,
                    "expected_primorial_count_orbit_triple": list(expected),
                    "universal_match": (
                        row["primorial_period"],
                        row["fixed_point_count_at_first_defect"],
                        row["primitive_orbit_defect"],
                    ) == expected,
                }
            )
            first_defect_rows.append(row)

    inversion_rows = []
    inversion_ranks = dict(list(ranks.items())[:6])
    for moment_order in (1, 2, 3):
        row = truncated_multiples_mobius_recovery(
            inversion_ranks,
            moment_order,
            maximum_multiplier=16,
            precision=80,
        )
        inversion_rows.append(
            {
                "moment_order": moment_order,
                "prime_prefix": list(inversion_ranks),
                "maximum_mobius_multiplier": 16,
                "target_moment": str(row["target_moment"]),
                "recovered_truncation": str(row["recovered_truncation"]),
                "absolute_error": str(row["absolute_error"]),
                "absolute_error_below_1e_minus_18":
                    row["absolute_error"] < row["absolute_error"].__class__("1e-18"),
            }
        )

    source = source_audit()
    foundation = foundation_audit()
    finite_checks = {
        "seed": [0, 0],
        "ranks_through_29": {str(prime): rank for prime, rank in ranks.items()},
        "rank_bound_pass": all(1 <= rank <= prime * prime for prime, rank in ranks.items()),
        "entropy_prefix_rows": entropy_prefix_rows,
        "entropy_prefix_strictly_increasing_in_level": all(
            entropy_prefix_rows[index]["normalized_entropy_density"]["decimal"]
            < entropy_prefix_rows[index + 1]["normalized_entropy_density"]["decimal"]
            for index in range(len(entropy_prefix_rows) - 1)
        ),
        "universal_first_defect_rows": first_defect_rows,
        "all_first_defect_rows_match": all(row["universal_match"] for row in first_defect_rows),
        "finite_multiples_mobius_rows": inversion_rows,
        "all_inversion_truncation_errors_below_1e_minus_18": all(
            row["absolute_error_below_1e_minus_18"] for row in inversion_rows
        ),
    }

    gates = {
        "A_canonical_intrinsic_dynamical_spectral_determinant": False,
        "B_time_oriented_scattering_or_unitary_completion": False,
        "C_self_adjoint_generator_and_intrinsic_T_log_T": False,
        "D_von_mangoldt_weighted_prime_power_traces": False,
        "E_completed_zeta_divisor_equality": False,
    }
    false_claims = {
        "admissible_shift_is_full_finite_field_Henon_zeta": False,
        "admissible_shift_is_hasse_weil_zeta": False,
        "entropy_samples_are_signed_operator_traces": False,
        "finite_entropy_table_proves_all_prime_distribution": False,
        "finite_precision_moments_give_stable_exact_rank_recovery": False,
        "hilbert_polya_constructed": False,
        "physical_same_clock_D_4k_transport_proved": False,
        "positive_integer_samples_analytically_continue_Z_P": False,
        "rh241_moving_noisy_envelope_closed": False,
        "riemann_hypothesis_proved": False,
        "riemann_zeros_spectrally_identified": False,
        "von_mangoldt_trace_proved": False,
        "zeta_divisor_equality": False,
    }

    return {
        "status": "RH-363_prime_return_admissible_entropy_tower",
        "source_commits": {
            "prime_dynamics_theory_rh362_release":
                "54709f1c0b30e7970ebca010973a24a1d2656c7e",
            "dyna_zeta_map":
                "7fd3a3fdd5a6a25827a0965345459baf4a47b816",
        },
        "source_audit": source,
        "four_volume_foundation_audit": foundation,
        "finite_checks": finite_checks,
        "theorem_flags": {
            "return_power_family_pairwise_coprime_and_thin": True,
            "all_tower_levels_have_zeta_one_over_one_minus_z": True,
            "normalized_entropy_equals_inverse_return_euler_sample": True,
            "entropy_tower_strictly_increases_to_one": True,
            "multiples_mobius_recovers_all_power_moments": True,
            "moments_recover_all_labeled_return_ranks": True,
            "finite_approximants_have_universal_primorial_first_defect": True,
            "finite_log_and_reduced_zeta_radii_equal_two_to_minus_entropy_density": True,
            "sharp_local_uniform_exhaustion_disk": True,
            "coefficientwise_limit_radius_discontinuity": True,
        },
        "route": {
            "route_A": "GO",
            "route_B": "STOP_SCOPED",
            "route_B_first_fatal_mismatch":
                "topological_entropy_samples_are_not_signed_von_mangoldt_operator_traces",
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
        finite["rank_bound_pass"],
        finite["entropy_prefix_strictly_increasing_in_level"],
        finite["all_first_defect_rows_match"],
        finite["all_inversion_truncation_errors_below_1e_minus_18"],
        all(row["pairwise_coprime"] for row in finite["entropy_prefix_rows"]),
    )
    if not all(required):
        raise SystemExit("finite reproduction failure")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": payload["status"], "pass": True}, sort_keys=True))


if __name__ == "__main__":
    main()
