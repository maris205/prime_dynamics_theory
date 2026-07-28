#!/usr/bin/env python3
"""Generate and verify the TPC-170 metric packet-corridor certificate."""

from __future__ import annotations

import argparse
import cmath
import hashlib
import json
import math
from pathlib import Path
from typing import Any


PAPER = Path(__file__).resolve().parents[1]
REPO = PAPER.parents[1]
UPSTREAM_168 = REPO / "papers" / "tpc-168-separated-phase-registry-sieve"
UPSTREAM_169 = REPO / "papers" / "tpc-169-maximal-prefix-phase-metric"
OUTPUT = PAPER / "experiments" / "tpc170_metric_corridor_audit.json"
SCHEMA = PAPER / "schemas" / "tpc170-metric-corridor-v1.schema.json"
HASH_MODE = "CANONICAL_UTF8_LF_V2"


def canonical_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    if path.suffix == ".json":
        text = json.dumps(
            json.loads(text), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ) + "\n"
    elif not text.endswith("\n"):
        text += "\n"
    return text.encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def e(x: float) -> complex:
    return cmath.exp(2j * math.pi * x)


def mobius(n: int) -> int:
    if n <= 0:
        raise ValueError("fixture Mobius input must be positive")
    value = n
    primes = 0
    factor = 2
    while factor * factor <= value:
        if value % factor == 0:
            value //= factor
            primes += 1
            if value % factor == 0:
                return 0
            while value % factor == 0:
                value //= factor
        factor += 1
    if value > 1:
        primes += 1
    return -1 if primes % 2 else 1


def validate_top_level(obj: dict[str, Any]) -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if set(obj) != set(schema["properties"]):
        raise ValueError("strict top-level schema mismatch")
    if obj["schema"] != schema["properties"]["schema"]["const"]:
        raise ValueError("wrong schema id")
    if obj["status"] != "PASS":
        raise ValueError("non-PASS result")


def validate_semantics(obj: dict[str, Any]) -> None:
    representative = obj["representative_invariance"]
    corridor = obj["packet_borel_cantelli"]
    power = obj["power_corollary"]
    atom = obj["fixed_atom_stop"]
    boundary = obj["claim_boundary"]
    if corridor["status"] != "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR":
        raise ValueError("wrong program status")
    if corridor["analytic_norm"] != "L2_PHASE_MAXIMAL_BC":
        raise ValueError("wrong analytic norm")
    if corridor["program_positive_L2"] is not False or corridor["fixed_atom"] is not False:
        raise ValueError("metric corridor promoted to program L2 or fixed atom")
    if corridor["packet_energy_union_paid"] is not True:
        raise ValueError("packet uniformity has no explicit energy payment")
    if corridor["corridor_uniformity"] != "ONLY_OVER_EXPLICIT_PRESCRIBED_PACKET_LIST":
        raise ValueError("corridor promoted to undeclared packets")
    if representative["representatives_canonicalized"] is not True:
        raise ValueError("Bezout translates counted as independent packets")
    if representative["requires_covariant_multiplier_translation"] is not True:
        raise ValueError("representative shift lost multiplier covariance")
    delta = power["fixture"]["delta"]
    if not (0 < delta < 0.25):
        raise ValueError("power exponent lies outside the proved range")
    if atom["quantifier_proved"] != "LEBESGUE_AE_FIXED_PHASE":
        raise ValueError("wrong metric quantifier")
    if "entire_prescribed_packet_schedule" not in atom["schedule_dependence"]:
        raise ValueError("schedule-dependent null set not recorded")
    required_false = (
        "program_positive_L2",
        "fixed_atom",
        "named_fixed_phase",
        "scale_dependent_phase_selector",
        "production_phase_registry",
        "physical_H3",
        "one_over_400",
        "prime_pair_lower_bound",
        "twin_prime_theorem",
    )
    if any(boundary[key] is not False for key in required_false):
        raise ValueError("claim boundary promotion")


def mutation_rejected(
    obj: dict[str, Any], path: tuple[str, ...], value: Any
) -> bool:
    clone = json.loads(json.dumps(obj))
    target: Any = clone
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    try:
        validate_semantics(clone)
    except ValueError:
        return True
    return False


def build() -> dict[str, Any]:
    audit168_path = UPSTREAM_168 / "experiments" / "tpc168_registry_sieve_audit.json"
    audit169_path = UPSTREAM_169 / "experiments" / "tpc169_maximal_prefix_audit.json"
    audit168 = json.loads(audit168_path.read_text(encoding="utf-8"))
    audit169 = json.loads(audit169_path.read_text(encoding="utf-8"))
    if audit168.get("status") != "PASS" or audit169.get("status") != "PASS":
        raise ValueError("upstream audit is not PASS")

    # Exact determinant-two representative translation fixture.
    a, s, d, u, shift = 3, 5, 1, 1, 4
    d_shifted, u_shifted = d + s * shift, u + a * shift
    determinant_original = s * u - a * d
    determinant_shifted = s * u_shifted - a * d_shifted
    alpha = math.sqrt(2.0)
    period = 3

    def rho(z: int) -> complex:
        return e((z % period) / period)

    z_values = list(range(2, 17))
    translation_rows = []
    for z_new in z_values:
        z_old = z_new + shift
        t_new = a * d_shifted + a * s * z_new
        t_old = a * d + a * s * z_old
        c_new = mobius(d_shifted + s * z_new) * mobius(u_shifted + a * z_new)
        c_old = mobius(d + s * z_old) * mobius(u + a * z_old)
        weighted_new = c_new * rho(z_old) * e(-alpha * z_new)
        weighted_old = c_old * rho(z_old) * e(-alpha * z_old)
        translation_rows.append({
            "z_new": z_new,
            "z_old": z_old,
            "t_match": t_new == t_old,
            "coefficient_match": c_new == c_old,
            "phase_covariance_error": abs(weighted_new - e(alpha * shift) * weighted_old),
        })
    representative_ok = (
        determinant_original == determinant_shifted == 2
        and all(row["t_match"] for row in translation_rows)
        and all(row["coefficient_match"] for row in translation_rows)
        and max(row["phase_covariance_error"] for row in translation_rows) < 1e-12
    )

    # Exact Abel fixture with an additive phase.
    coefficients = [1, -1, 0, 1, -1, 1, 1]
    weights = [2.0, 1.5, 1.5, 0.75, 0.25, 0.25, 0.0]
    phase = 0.173
    twisted = [value * e(-phase * index) for index, value in enumerate(coefficients)]
    partials = []
    running = 0j
    for value in twisted:
        running += value
        partials.append(running)
    differences = [
        weights[index] - weights[index + 1]
        for index in range(len(weights) - 1)
    ] + [weights[-1]]
    direct_weighted = sum(value * weight for value, weight in zip(twisted, weights))
    abel_weighted = sum(value * difference for value, difference in zip(partials, differences))
    variation = sum(abs(value) for value in differences)
    abel_error = abs(direct_weighted - abel_weighted)
    maximal_times_variation = max(abs(value) for value in partials) * variation

    # Ratio-test data for the dyadic power corollary.
    delta_power = 0.20
    eta = 2
    packet_exponent = 3
    polynomial_exponent = eta + packet_exponent + 2
    exponential_decay = 0.5 - 2 * delta_power
    ratio_limit = 2 ** (-exponential_decay)
    sample_terms = [
        (n ** polynomial_exponent) * (2 ** (-exponential_decay * n))
        for n in range(40, 51)
    ]

    # The fixed-atom selector stop: alpha=0 stays bad for constant coefficients.
    selector_lengths = [64, 128, 256, 512]
    selector_values = [
        abs(sum(1 for _ in range(length))) / length
        for length in selector_lengths
    ]

    result = {
        "schema": "tpc-170-metric-corridor-audit-v1",
        "status": "PASS",
        "hash_mode": HASH_MODE,
        "upstream": {
            "TPC168": {
                "audit_sha256": sha256(audit168_path),
                "main_tex_sha256": sha256(UPSTREAM_168 / "main.tex"),
                "audit_status": audit168["status"],
            },
            "TPC169": {
                "audit_sha256": sha256(audit169_path),
                "main_tex_sha256": sha256(UPSTREAM_169 / "main.tex"),
                "audit_status": audit169["status"],
            },
            "hash_semantics": "INTEGRITY_ONLY",
        },
        "representative_invariance": {
            "status": "PROVED_EXACT_CANONICALIZATION",
            "equation": "(d,u)->(d+s*k,u+a*k)",
            "requires_covariant_multiplier_translation": True,
            "representatives_canonicalized": True,
            "fixture": {
                "a": a,
                "s": s,
                "d": d,
                "u": u,
                "shift": shift,
                "d_shifted": d_shifted,
                "u_shifted": u_shifted,
                "determinant_original": determinant_original,
                "determinant_shifted": determinant_shifted,
                "rows": translation_rows,
            },
        },
        "packet_borel_cantelli": {
            "export_id": "A170.metric_packet_corridor",
            "status": "PROVED_L1_ACTUAL_CORE_PHASE_METRIC_PACKET_CORRIDOR",
            "analytic_norm": "L2_PHASE_MAXIMAL_BC",
            "program_positive_L2": False,
            "fixed_atom": False,
            "packet_energy": (
                "V_(n,p)=D_(n,p)^2 ||rho_(n,p)||_infinity^2 "
                "(q_(n,p)/T_(n,p)+q_(n,p)^2/T_(n,p)^2)"
            ),
            "summability_condition": (
                "sum_n lambda_n^(-2) sum_(p in P_n) V_(n,p) < infinity"
            ),
            "conclusion": (
                "for_Lebesgue_almost_every_fixed_alpha_eventually_all_declared_"
                "packets_and_all_prefixes_are_at_most_lambda_n"
            ),
            "independence_required": False,
            "packet_energy_union_paid": True,
            "corridor_uniformity": "ONLY_OVER_EXPLICIT_PRESCRIBED_PACKET_LIST",
        },
        "power_corollary": {
            "X_n": "2^n",
            "terminal_lower_bound": "T_(n,p) >= sqrt(X_n)",
            "q_bound": "(log X_n)^eta",
            "packet_count_bound": "(log X_n)^C",
            "threshold": "lambda_n=X_n^(-delta)",
            "admissible_delta": "every delta<1/4",
            "fixture": {
                "delta": delta_power,
                "eta": eta,
                "packet_exponent_C": packet_exponent,
                "polynomial_exponent": polynomial_exponent,
                "exponential_decay": exponential_decay,
                "ratio_limit": ratio_limit,
                "sample_terms_n40_to_n50": sample_terms,
            },
        },
        "abel_return": {
            "status": "PROVED_EXACT_METRIC_WEIGHTED_RETURN_INTERFACE",
            "bound": "(q/T)|sum b_j e(-alpha z_j)w_j| <= G_T(alpha)*V(w)",
            "atomic_prefix_variation": 1,
            "fixture": {
                "direct_real": direct_weighted.real,
                "direct_imag": direct_weighted.imag,
                "abel_real": abel_weighted.real,
                "abel_imag": abel_weighted.imag,
                "identity_error": abel_error,
                "variation": variation,
                "direct_modulus": abs(direct_weighted),
                "maximal_times_variation": maximal_times_variation,
            },
        },
        "fixed_atom_stop": {
            "status": "PROVED_SCOPED_METRIC_TO_ATOM_NONIMPLICATION",
            "quantifier_proved": "LEBESGUE_AE_FIXED_PHASE",
            "quantifier_not_proved": "NAMED_FIXED_ATOM_OR_SCALE_DEPENDENT_SELECTOR",
            "schedule_dependence": (
                "the_null_set_depends_on_the_entire_prescribed_packet_schedule"
            ),
            "uncontrolled_atomic_registry_obstruction": (
                "an_atomic_registry_may_concentrate_entirely_on_the_metric_null_set"
            ),
            "constant_coefficient_fixture": {
                "phase": 0,
                "lengths": selector_lengths,
                "normalized_values": selector_values,
            },
            "not_a_literal_mobius_lower_bound": True,
        },
        "route_decision": {
            "direct_twist_child": "phase_metric_packet_corridor_advanced",
            "bad_endpoint_child": "phase_metric_all_prefix_advanced",
            "original_fixed_phase_nodes_closed": False,
            "next_object": "source_locked_production_phase_metric_crosswalk_or_pointwise_theorem",
        },
        "claim_boundary": {
            "actual_fixed_h0_core": True,
            "explicit_packet_corridor": True,
            "almost_every_fixed_phase": True,
            "analytic_norm": "L2_PHASE_MAXIMAL_BC",
            "program_positive_L2": False,
            "fixed_atom": False,
            "named_fixed_phase": False,
            "scale_dependent_phase_selector": False,
            "production_phase_registry": False,
            "physical_H3": False,
            "one_over_400": False,
            "prime_pair_lower_bound": False,
            "twin_prime_theorem": False,
        },
        "checks": {
            "upstreams_pass": True,
            "representative_translation_exact": representative_ok,
            "abel_identity_exact_numerically": abel_error < 1e-12,
            "abel_maximal_bound_holds": abs(direct_weighted) <= maximal_times_variation + 1e-12,
            "power_ratio_limit_below_one": ratio_limit < 1,
            "power_exponent_strictly_below_quarter": delta_power < 0.25,
            "fixed_atom_fixture_stays_bad": min(selector_values) == 1.0,
            "packet_and_atom_quantifiers_explicit": True,
        },
        "mutation_regressions": {},
    }
    validate_top_level(result)
    validate_semantics(result)
    result["mutation_regressions"] = {
        "reject_unlisted_packets_in_corridor_uniform_claim": mutation_rejected(
            result,
            ("packet_borel_cantelli", "corridor_uniformity"),
            "ALL_UNDECLARED_PACKETS",
        ),
        "reject_union_without_packet_energy_sum": mutation_rejected(
            result, ("packet_borel_cantelli", "packet_energy_union_paid"), False
        ),
        "reject_duplicate_Bezout_representatives_as_independent_packets": (
            mutation_rejected(
                result,
                ("representative_invariance", "representatives_canonicalized"),
                False,
            )
        ),
        "reject_nontranslated_multiplier_under_representative_shift": (
            mutation_rejected(
                result,
                (
                    "representative_invariance",
                    "requires_covariant_multiplier_translation",
                ),
                False,
            )
        ),
        "reject_Lebesgue_AE_as_named_fixed_atom": mutation_rejected(
            result, ("claim_boundary", "fixed_atom"), True
        ),
        "reject_fixed_phase_as_scale_dependent_selector": mutation_rejected(
            result, ("claim_boundary", "scale_dependent_phase_selector"), True
        ),
        "reject_delta_equal_to_or_above_one_quarter": (
            mutation_rejected(
                result, ("power_corollary", "fixture", "delta"), 0.25
            )
            and mutation_rejected(
                result, ("power_corollary", "fixture", "delta"), 0.30
            )
        ),
        "reject_metric_power_as_physical_H3_or_one_over_400": (
            mutation_rejected(result, ("claim_boundary", "physical_H3"), True)
            and mutation_rejected(
                result, ("claim_boundary", "one_over_400"), True
            )
        ),
    }
    if not all(result["checks"].values()):
        raise AssertionError("TPC-170 check failed")
    if not all(result["mutation_regressions"].values()):
        raise AssertionError("TPC-170 mutation regression failed")
    return result


def render(obj: dict[str, Any]) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    obj = build()
    text = render(obj)
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != text:
            raise SystemExit("TPC-170 CHECK FAIL: stale artifact")
        print("TPC-170 CHECK PASS")
    else:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(text, encoding="utf-8", newline="\n")
        print("TPC-170 GENERATE PASS")
    print(json.dumps({
        "status": obj["packet_borel_cantelli"]["status"],
        "quantifier": obj["fixed_atom_stop"]["quantifier_proved"],
        "fixed_nodes_closed": obj["route_decision"]["original_fixed_phase_nodes_closed"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
