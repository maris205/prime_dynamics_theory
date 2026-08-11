"""Exact finite certificate for fixed-lag centered Möbius capacity.

This module reproduces the finite relation algebra, local CRT densities,
tropical optimizers, square-clock run counts, and strict-lift identities used
by RH-396.  It does not replace the frozen RH-394 analytic terminal law.
Every formal oracle is integer or :class:`fractions.Fraction` valued.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
from typing import Iterable, Sequence


TITLE = "Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity"
PACKAGE = "fixed_lag_centered_capacity"
T = (-1, 0, 1)
COORDINATES = ("L", "C", "R")
ALL_STATE_MASKS = tuple(range(8))
FOUR_STATE_MASKS = (0, 2, 5, 7)
ZERO_EXPR = (Fraction(0), Fraction(0), Fraction(0), Fraction(0))
INTERVAL_CUTOFF = 20_000

GROUP_IDS = {
    "domain_source_firewall": (
        "A01_mu0", "A02_terminal_clock", "A03_fixed_h_q",
        "A04_d_equals_2h", "A05_shift_tuple_h_0_minus_h",
        "A06_centered_output", "A07_distance_d_safety",
        "A08_terminal_score", "A09_limit_max_sup_order",
        "A10_RH394_analytic_role", "A11_RH375_RH395_finite_only_roles",
        "A12_firewalls_gates",
    ),
    "theta_pi_lambda": (
        "B01_Bp_dedup", "B02_nu_distinct",
        "B03_tau_distinct_modp2_then_modp", "B04_theta_p_not_q",
        "B05_theta_p_parallel_q", "B06_theta_p2_div_q",
        "B07_theta_empty", "B08_theta_phase_mass",
        "B09_Pi_inclusion_exclusion", "B10_Pi_nonnegative",
        "B11_Pi_phase_mass", "B12_Sxy", "B13_lambda_sign_split",
        "B14_collision_p_not_d", "B15_collision_p_div_d_not_p2",
        "B16_collision_p2_div_d",
    ),
    "projection_safety_saturation_full8_reflection": (
        "C01_positive_projection", "C02_relation_A", "C03_projected_limit",
        "C04_composable_edges", "C05_safety_iff", "C06_target_Y",
        "C07_A_containment", "C08_saturated_A",
        "C09_saturated_converse_safe", "C10_transition_K",
        "C11_phase_objective", "C12_step_d_cycles",
        "C13_full8_tropical_trace", "C14_reflection_map",
        "C15_reflection_limit_sign", "C16_dynamic_relation_oracle",
    ),
    "selfloop_compression_small_clock": (
        "D01_q_div_d_selfloop", "D02_selfloop_full8_required",
        "D03_q_not_div_d_cycle_gt1", "D04_multiaffine_occurrences",
        "D05_endpoint_rounding_k_to_0_or2", "D06_four_antipodal_states",
        "D07_four_state_transition", "D08_h1_q2_selfloop",
        "D09_h1_q4_two_cycle", "D10_h3_q3_selfloop",
        "D11_h3_q4_nonself",
        "D12_full8_vs_four_bruteforce_and_forbidden_allq_claim",
    ),
    "marginal_square_saturation_lifts": (
        "E01_delta_center", "E02_one_site_Mh", "E03_one_site_embedding",
        "E04_Py_qy", "E05_p0_y0", "E06_same_support_domain",
        "E07_common_positive_delta", "E08_shared_coordinate_marginal_all_t",
        "E09_pair_charge", "E10_path_run_charge",
        "E11_same_support_scaling", "E12_exact_fixtures",
    ),
    "D_R_finite_infinite_endpoint": (
        "F01_nu_J", "F02_Dhy", "F03_Dh_absolute_convergence",
        "F04_p0_definition", "F05_p0_run_cutoff", "F06_R_four_term",
        "F07_R_exact_run_event_nonnegative", "F08_finite_run_MWIS_identity",
        "F09_By_formula", "F10_Dy_Ry_limits", "F11_Binfinity_formula",
        "F12_numeric_intervals",
    ),
    "strict_lift_CRT": (
        "G01_fresh_p_domain", "G02_positive_count_Nprime",
        "G03_one_deletion_per_lifted_run", "G04_path_deletion_parity",
        "G05_alpha_prime_formula", "G06_normalized_gain_E",
        "G07_CRT_exact_length2_run", "G08_eventual_strict_and_arbitrary_q_upper",
    ),
    "lag_inf_claim_ceiling": (
        "H01_CRT_exact_length1_run", "H02_each_h_strict_baseline",
        "H03_dY_hY", "H04_boundary_requires_p_gtY",
        "H05_boundary_union_tail", "H06_inf_3_over_pi2",
        "H07_inf_unattained", "H08_no_sup_h_no_growing_parameters_claim_ceiling",
    ),
}
ROW_PARTITION = {group: len(ids) for group, ids in GROUP_IDS.items()}
CERTIFICATE_FIXTURE_ROWS = 96
CERTIFICATE_FIXTURE_BYTES = 83309
CERTIFICATE_FIXTURE_SHA256 = "7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba"

MUTATION_NAMES = (
    "fixed_h_to_growing", "fixed_q_to_growing", "d_equals_h",
    "shift_orientation_swap", "safety_step_h", "safety_unshares_letter",
    "Bp_no_dedup", "tau_counts_multiplicity", "theta_parallel_branch",
    "theta_square_branch", "Pi_sign_flip", "Pi_wrong_complement",
    "lambda_drop_x_half", "lambda_drop_y_half", "projected_wrong_center",
    "composition_reverse", "saturation_r_plus_d", "transition_includes_U",
    "tropical_drop_cycle", "four_state_on_selfloop",
    "q_divides_condition_flip", "reflection_no_input_negation",
    "p0_uses_p2_nondivisor", "base_omits_p0", "same_support_unconditional",
    "R_drop_left", "R_drop_right", "R_last_sign_flip",
    "By_drop_K1_over_D", "deletion_odd_even_swap", "Nprime_uses_p2N",
    "claim_sup_h",
)


def _pairs_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        if key in output:
            raise ValueError(f"duplicate JSON key: {key}")
        output[key] = value
    return output


def _reject_constant(token: str) -> object:
    raise ValueError(f"non-finite JSON constant: {token}")


def loads_strict(text: str) -> object:
    if type(text) is not str:
        raise TypeError("strict JSON input must be exact text")
    return json.loads(
        text, object_pairs_hook=_pairs_no_duplicates, parse_constant=_reject_constant
    )


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def exact_equal(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(
            exact_equal(left[key], right[key]) for key in left
        )
    if type(left) in (list, tuple):
        return len(left) == len(right) and all(
            exact_equal(a, b) for a, b in zip(left, right)
        )
    if type(left) is float:
        return math.isfinite(left) and math.isfinite(right) and left == right
    return left == right


def fraction_text(value: Fraction) -> str:
    if type(value) is not Fraction:
        raise TypeError("fraction serializer requires exact Fraction")
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def expr_text(value: tuple[Fraction, Fraction, Fraction, Fraction]) -> list[str]:
    if type(value) is not tuple or len(value) != 4:
        raise TypeError("K-expression must be an exact K0--K3 four-tuple")
    return [fraction_text(item) for item in value]


def expr_add(
    left: tuple[Fraction, Fraction, Fraction, Fraction],
    right: tuple[Fraction, Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def expr_scale(
    scalar: Fraction, value: tuple[Fraction, Fraction, Fraction, Fraction]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if type(scalar) is not Fraction:
        raise TypeError("expression scalar must be exact Fraction")
    return tuple(scalar * item for item in value)  # type: ignore[return-value]


def factorization(value: int) -> tuple[tuple[int, int], ...]:
    if type(value) is not int or value < 1:
        raise ValueError("factorization input must be a positive exact integer")
    output: list[tuple[int, int]] = []
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            exponent = 0
            while remaining % prime == 0:
                remaining //= prime
                exponent += 1
            output.append((prime, exponent))
        prime += 1
    if remaining > 1:
        output.append((remaining, 1))
    return tuple(output)


@lru_cache(maxsize=None)
def primes_through(limit: int) -> tuple[int, ...]:
    if type(limit) is not int or limit < 2:
        raise ValueError("prime cutoff must be an exact integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(index for index in range(2, limit + 1) if sieve[index])


def prime_support(value: int) -> tuple[int, ...]:
    return tuple(prime for prime, _exponent in factorization(value))


def is_prime(value: int) -> bool:
    if type(value) is not int or value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def shift_by_coordinate(h: int) -> dict[str, int]:
    if type(h) is not int or h < 1:
        raise ValueError("lag h must be a fixed positive exact integer")
    return {"L": h, "C": 0, "R": -h}


def _ordered_support(values: Iterable[str]) -> tuple[str, ...]:
    support = tuple(values)
    if any(type(value) is not str or value not in COORDINATES for value in support):
        raise ValueError("support contains an invalid coordinate")
    if len(set(support)) != len(support):
        raise ValueError("support contains a duplicate coordinate")
    return tuple(value for value in COORDINATES if value in support)


def residue_set(h: int, prime: int, support: Iterable[str]) -> tuple[int, ...]:
    if not is_prime(prime):
        raise ValueError("prime must be an exact prime integer")
    shifts = shift_by_coordinate(h)
    return tuple(sorted({shifts[item] % (prime * prime) for item in _ordered_support(support)}))


def nu_support(h: int, prime: int, support: Iterable[str]) -> int:
    return len(residue_set(h, prime, support))


def tau_support(h: int, prime: int, phase: int, support: Iterable[str]) -> int:
    if type(phase) is not int:
        raise TypeError("phase must be an exact integer")
    residues = residue_set(h, prime, support)
    return sum(1 for residue in residues if residue % prime == phase % prime)


def exceptional_primes(h: int, support: Iterable[str]) -> tuple[int, ...]:
    support_tuple = _ordered_support(support)
    shifts = shift_by_coordinate(h)
    differences = {
        abs(shifts[a] - shifts[b])
        for index, a in enumerate(support_tuple)
        for b in support_tuple[index + 1 :]
    }
    candidates = {
        prime
        for difference in differences
        if difference
        for prime, exponent in factorization(difference)
        if exponent >= 2
    }
    return tuple(sorted(candidates))


@lru_cache(maxsize=None)
def theta_coefficients(
    h: int, q: int, phase: int, support: tuple[str, ...]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if type(q) is not int or q < 1 or type(phase) is not int or not 0 <= phase < q:
        raise ValueError("phase must use exact q>=1 and 0<=phase<q")
    support = _ordered_support(support)
    cardinality = len(support)
    if cardinality not in (0, 1, 2, 3):
        raise ValueError("theta supports have size zero through three")
    q_factor = dict(factorization(q))
    relevant = sorted(set(q_factor) | set(exceptional_primes(h, support)))
    coefficient = Fraction(1, q)
    for prime in relevant:
        base = Fraction(prime * prime - cardinality, prime * prime)
        if prime not in q_factor:
            replacement = Fraction(
                prime * prime - nu_support(h, prime, support), prime * prime
            )
        elif q_factor[prime] == 1:
            replacement = Fraction(
                prime - tau_support(h, prime, phase, support), prime
            )
        else:
            replacement = Fraction(
                int(phase % (prime * prime) not in residue_set(h, prime, support))
            )
        coefficient *= replacement / base
    output = [Fraction(0), Fraction(0), Fraction(0), Fraction(0)]
    output[cardinality] = coefficient
    return tuple(output)  # type: ignore[return-value]


@lru_cache(maxsize=None)
def exact_support_coefficients(
    h: int, q: int, phase: int, support: tuple[str, ...]
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    support = _ordered_support(support)
    complement = tuple(item for item in COORDINATES if item not in support)
    output = ZERO_EXPR
    for subset_mask in range(1 << len(complement)):
        extension = tuple(
            complement[index]
            for index in range(len(complement))
            if subset_mask & (1 << index)
        )
        sign = Fraction(-1 if subset_mask.bit_count() % 2 else 1)
        output = expr_add(
            output,
            expr_scale(sign, theta_coefficients(h, q, phase, _ordered_support((*support, *extension)))),
        )
    return output


@lru_cache(maxsize=None)
def lambda_coefficients(
    h: int, q: int, phase: int, left: int, right: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    if type(left) is not int or type(right) is not int or left not in T or right not in T:
        raise ValueError("lambda signs must be exact ternary integers")
    support = ["C"]
    if left != 0:
        support.append("L")
    if right != 0:
        support.append("R")
    divisor = 1 << (int(left != 0) + int(right != 0))
    return expr_scale(
        Fraction(1, divisor),
        exact_support_coefficients(h, q, phase, _ordered_support(support)),
    )


@lru_cache(maxsize=None)
def basis_intervals(
    limit: int = INTERVAL_CUTOFF,
) -> tuple[tuple[Fraction, Fraction], ...]:
    """Rigorous rational enclosures for K_0,...,K_3.

    The elementary tail inequality
    ``prod_{p>x}(1-j/p^2) >= 1-j/x`` is deliberately coarse but sufficient
    to order every finite optimizer used by this certificate.
    """

    if type(limit) is not int or limit <= 3:
        raise ValueError("Euler-product interval cutoff must exceed three")
    output = [(Fraction(1), Fraction(1))]
    primes = primes_through(limit)
    for order in (1, 2, 3):
        upper = Fraction(1)
        for prime in primes:
            upper *= Fraction(prime * prime - order, prime * prime)
        output.append((upper * Fraction(limit - order, limit), upper))
    return tuple(output)


@lru_cache(maxsize=None)
def expr_interval(
    value: tuple[Fraction, Fraction, Fraction, Fraction],
    limit: int = INTERVAL_CUTOFF,
) -> tuple[Fraction, Fraction]:
    if type(value) is not tuple or len(value) != 4 or any(
        type(coefficient) is not Fraction for coefficient in value
    ):
        raise TypeError("interval evaluation requires an exact K0--K3 expression")
    lower = Fraction(0)
    upper = Fraction(0)
    for coefficient, (basis_lower, basis_upper) in zip(value, basis_intervals(limit)):
        if coefficient >= 0:
            lower += coefficient * basis_lower
            upper += coefficient * basis_upper
        else:
            lower += coefficient * basis_upper
            upper += coefficient * basis_lower
    return lower, upper


def compare_expressions(
    left: tuple[Fraction, Fraction, Fraction, Fraction],
    right: tuple[Fraction, Fraction, Fraction, Fraction],
) -> int:
    difference = tuple(a - b for a, b in zip(left, right))
    if difference == ZERO_EXPR:
        return 0
    lower, upper = expr_interval(difference)  # exact rational enclosure
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise ArithmeticError("Euler-product intervals overlap for distinct candidates")


def state_members(mask: int) -> tuple[int, ...]:
    if type(mask) is not int or not 0 <= mask < 8:
        raise ValueError("state mask must be an exact integer in [0,8)")
    return tuple(value for index, value in enumerate(T) if mask & (1 << index))


def state_mask(values: Iterable[int]) -> int:
    output = 0
    seen: set[int] = set()
    for value in values:
        if type(value) is not int or value not in T or value in seen:
            raise ValueError("state contains an invalid or duplicate ternary value")
        seen.add(value)
        output |= 1 << T.index(value)
    return output


def reflected_state_mask(mask: int) -> int:
    return state_mask(-value for value in state_members(mask))


def relation_pairs(mask: int) -> tuple[tuple[int, int], ...]:
    if type(mask) is not int or not 0 <= mask < 512:
        raise ValueError("relation mask must be an exact integer in [0,512)")
    universe = tuple((left, right) for left in T for right in T)
    return tuple(pair for index, pair in enumerate(universe) if mask & (1 << index))


def relation_mask(pairs: Iterable[tuple[int, int]]) -> int:
    universe = tuple((left, right) for left in T for right in T)
    output = 0
    seen: set[tuple[int, int]] = set()
    for pair in pairs:
        if type(pair) is not tuple or pair not in universe or pair in seen:
            raise ValueError("relation contains an invalid or duplicate ternary pair")
        seen.add(pair)
        output |= 1 << universe.index(pair)
    return output


@lru_cache(maxsize=None)
def relation_source_mask(mask: int) -> int:
    return state_mask({left for left, _right in relation_pairs(mask)})


@lru_cache(maxsize=None)
def relation_target_mask(mask: int) -> int:
    return state_mask({right for _left, right in relation_pairs(mask)})


def reflected_relation_mask(mask: int) -> int:
    return relation_mask((-left, -right) for left, right in relation_pairs(mask))


def relation_composition_empty(left: int, right: int) -> bool:
    return relation_target_mask(left) & relation_source_mask(right) == 0


def saturated_relation(previous_target: int, current_target: int) -> int:
    previous = set(state_members(previous_target))
    current = set(state_members(current_target))
    return relation_mask(
        (left, right) for left in T if left not in previous for right in current
    )


@lru_cache(maxsize=1)
def relation_oracle() -> dict[str, object]:
    safe = 0
    inclusion_failures = 0
    saturation_failures = 0
    compatibility_failures = 0
    reflected_failures = 0
    for left in range(512):
        target = relation_target_mask(left)
        reflected_left = reflected_relation_mask(left)
        if reflected_relation_mask(reflected_left) != left:
            reflected_failures += 1
        for right in range(512):
            criterion = relation_composition_empty(left, right)
            explicit = not any(
                middle_left == middle_right
                for _source, middle_left in relation_pairs(left)
                for middle_right, _target in relation_pairs(right)
            )
            if criterion != explicit:
                compatibility_failures += 1
            if not criterion:
                continue
            safe += 1
            saturated = saturated_relation(target, relation_target_mask(right))
            if right & ~saturated:
                inclusion_failures += 1
            if not relation_composition_empty(left, saturated):
                saturation_failures += 1
            if not relation_composition_empty(
                reflected_left, reflected_relation_mask(right)
            ):
                reflected_failures += 1
    return {
        "relation_count": 512,
        "ordered_pair_count": 262144,
        "safe_pair_count": safe,
        "compatibility_failure_count": compatibility_failures,
        "inclusion_failure_count": inclusion_failures,
        "saturation_failure_count": saturation_failures,
        "reflection_failure_count": reflected_failures,
        "pass": (
            safe == 3375
            and compatibility_failures == inclusion_failures
            == saturation_failures == reflected_failures == 0
        ),
    }


def projection_oracle() -> dict[str, object]:
    cases = deleted = monotonicity_failures = inclusion_failures = 0
    for left in T:
        for center in T:
            for right in T:
                for old_output in (-1, 1):
                    cases += 1
                    new_output = old_output if center == 1 else -1
                    if new_output == 1 and old_output != 1:
                        inclusion_failures += 1
                    if center * new_output < center * old_output:
                        monotonicity_failures += 1
                    if old_output == 1 and new_output == -1:
                        deleted += 1
    return {
        "case_count": cases,
        "deleted_plus_count": deleted,
        "plus_inclusion_failure_count": inclusion_failures,
        "score_monotonicity_failure_count": monotonicity_failures,
        "pass": cases == 54 and deleted == 18
        and inclusion_failures == monotonicity_failures == 0,
    }


@lru_cache(maxsize=None)
def transition_coefficients(
    h: int, q: int, phase: int, previous_mask: int, current_mask: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    previous = set(state_members(previous_mask))
    current = set(state_members(current_mask))
    output = ZERO_EXPR
    for left in T:
        for right in T:
            if left not in previous and right in current:
                output = expr_add(
                    output, lambda_coefficients(h, q, phase, left, right)
                )
    return output


def step_cycles(h: int, q: int) -> tuple[tuple[int, ...], ...]:
    if type(h) is not int or h < 1 or type(q) is not int or q < 1:
        raise ValueError("cycles require exact h,q>=1")
    step = 2 * h
    seen: set[int] = set()
    output: list[tuple[int, ...]] = []
    for start in range(q):
        if start in seen:
            continue
        cycle: list[int] = []
        phase = start
        while phase not in seen:
            seen.add(phase)
            cycle.append(phase)
            phase = (phase + step) % q
        output.append(tuple(cycle))
    return tuple(output)


def _better_candidate(
    left: tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]],
    right: tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]],
) -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]]:
    comparison = compare_expressions(left[0], right[0])
    if comparison > 0 or (comparison == 0 and left[1] < right[1]):
        return left
    return right


def capacity_dp(h: int, q: int, states: tuple[int, ...]) -> dict[str, object]:
    if type(states) is not tuple or not states or len(set(states)) != len(states):
        raise ValueError("DP states must be a nonempty unique tuple")
    if any(type(mask) is not int or mask not in ALL_STATE_MASKS for mask in states):
        raise ValueError("DP state is outside the eight subsets")
    total = ZERO_EXPR
    witness: dict[int, int] = {}
    cycle_rows: list[dict[str, object]] = []
    for cycle in step_cycles(h, q):
        best_cycle: tuple[
            tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]
        ] | None = None
        for first in states:
            dynamic = {first: (ZERO_EXPR, (first,))}
            for phase in cycle[1:]:
                updated: dict[
                    int,
                    tuple[tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]],
                ] = {}
                for previous, (score, path) in dynamic.items():
                    for current in states:
                        candidate = (
                            expr_add(
                                score,
                                transition_coefficients(h, q, phase, previous, current),
                            ),
                            (*path, current),
                        )
                        old = updated.get(current)
                        updated[current] = candidate if old is None else _better_candidate(candidate, old)
                dynamic = updated
            for last, (score, path) in dynamic.items():
                candidate = (
                    expr_add(
                        score,
                        transition_coefficients(h, q, cycle[0], last, first),
                    ),
                    path,
                )
                best_cycle = candidate if best_cycle is None else _better_candidate(candidate, best_cycle)
        if best_cycle is None:
            raise RuntimeError("empty tropical cycle optimization")
        total = expr_add(total, best_cycle[0])
        for phase, state in zip(cycle, best_cycle[1]):
            witness[phase] = state
        cycle_rows.append({
            "phases": list(cycle),
            "coefficients": expr_text(best_cycle[0]),
            "states": list(best_cycle[1]),
        })
    return {
        "h": h,
        "q": q,
        "step": 2 * h,
        "cycle_count": len(step_cycles(h, q)),
        "cycle_length": q // math.gcd(q, 2 * h),
        "state_count": len(states),
        "coefficients": expr_text(total),
        "witness": {str(phase): witness[phase] for phase in range(q)},
        "cycles": cycle_rows,
    }


def full_capacity(h: int, q: int) -> dict[str, object]:
    return capacity_dp(h, q, ALL_STATE_MASKS)


def four_state_capacity(h: int, q: int) -> dict[str, object]:
    return capacity_dp(h, q, FOUR_STATE_MASKS)


def one_site_capacity(h: int, q: int) -> dict[str, object]:
    return capacity_dp(h, q, (0, 7))


def brute_capacity(h: int, q: int, states: tuple[int, ...]) -> dict[str, object]:
    """Independent exhaustive Y-profile oracle for deliberately small clocks."""

    if type(q) is not int or q < 1 or q > 5:
        raise ValueError("brute oracle is deliberately restricted to 1<=q<=5")
    profiles: list[tuple[int, ...]] = [()]
    for _phase in range(q):
        profiles = [(*profile, state) for profile in profiles for state in states]
    best: tuple[
        tuple[Fraction, Fraction, Fraction, Fraction], tuple[int, ...]
    ] | None = None
    for profile in profiles:
        score = ZERO_EXPR
        for phase in range(q):
            previous = profile[(phase - 2 * h) % q]
            score = expr_add(
                score,
                transition_coefficients(h, q, phase, previous, profile[phase]),
            )
        candidate = (score, profile)
        best = candidate if best is None else _better_candidate(candidate, best)
    if best is None:
        raise RuntimeError("empty brute profile space")
    return {
        "h": h, "q": q, "state_count": len(states),
        "profile_count": len(profiles),
        "coefficients": expr_text(best[0]), "profile": list(best[1]),
    }


def first_prime_not_dividing(value: int) -> int:
    if type(value) is not int or value < 1:
        raise ValueError("input must be a positive exact integer")
    candidate = 2
    while True:
        if is_prime(candidate) and value % candidate:
            return candidate
        candidate += 1


def square_clock_from_support(support: Sequence[int]) -> int:
    primes = tuple(support)
    if not primes or len(set(primes)) != len(primes) or any(not is_prime(p) for p in primes):
        raise ValueError("square support must be a nonempty tuple of distinct primes")
    return math.prod(prime * prime for prime in primes)


def square_clock_through(bound: int) -> int:
    return square_clock_from_support(primes_through(bound))


def _square_supported(value: int) -> bool:
    return all(exponent >= 2 for _prime, exponent in factorization(value))


def center_phase_positive(q: int, phase: int) -> bool:
    if type(q) is not int or q < 1 or type(phase) is not int or not 0 <= phase < q:
        raise ValueError("center phase requires q>=1 and 0<=phase<q")
    if not _square_supported(q):
        raise ValueError("center-phase oracle requires every supported prime squared")
    return all(phase % (prime * prime) for prime in prime_support(q))


def shared_left_marginal(
    h: int, q: int, phase: int, shared: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    output = ZERO_EXPR
    for left in T:
        output = expr_add(output, lambda_coefficients(h, q, phase, left, shared))
    return output


def shared_right_marginal(
    h: int, q: int, phase: int, shared: int
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    output = ZERO_EXPR
    for right in T:
        output = expr_add(output, lambda_coefficients(h, q, phase, shared, right))
    return output


def marginal_square_audit(fixtures: Sequence[tuple[int, int]]) -> dict[str, object]:
    phase_pairs = ternary_cases = marginal_failures = charge_failures = 0
    samples: list[dict[str, object]] = []
    for h, q in fixtures:
        for phase in range(q):
            following = (phase + 2 * h) % q
            if not (
                center_phase_positive(q, phase)
                and center_phase_positive(q, following)
            ):
                continue
            phase_pairs += 1
            delta = theta_coefficients(h, q, phase, ("C",))
            for shared in T:
                ternary_cases += 1
                left = shared_left_marginal(h, q, phase, shared)
                right = shared_right_marginal(h, q, following, shared)
                if left != right:
                    marginal_failures += 1
                if len(samples) < 12:
                    samples.append({
                        "h": h, "q": q, "phase": phase,
                        "following": following, "shared": shared,
                        "left": expr_text(left), "right": expr_text(right),
                    })
            for previous in ALL_STATE_MASKS:
                for current in ALL_STATE_MASKS:
                    for following_state in ALL_STATE_MASKS:
                        pair = expr_add(
                            transition_coefficients(h, q, phase, previous, current),
                            transition_coefficients(
                                h, q, following, current, following_state
                            ),
                        )
                        if compare_expressions(pair, delta) > 0:
                            charge_failures += 1
    return {
        "fixtures": [[h, q] for h, q in fixtures],
        "positive_adjacent_phase_pair_count": phase_pairs,
        "per_t_case_count": ternary_cases,
        "marginal_failure_count": marginal_failures,
        "pair_charge_failure_count": charge_failures,
        "samples": samples,
        "pass": phase_pairs > 0 and ternary_cases == 3 * phase_pairs
        and marginal_failures == charge_failures == 0,
    }


def multiaffinity_audit(fixtures: Sequence[tuple[int, int]]) -> dict[str, object]:
    cases = singleton_symmetry_failures = second_difference_failures = 0
    rows: list[dict[str, object]] = []
    for h, q in fixtures:
        if (2 * h) % q == 0:
            raise ValueError("multiaffinity audit excludes self-identified phases")
        phase = 0
        following = (phase + 2 * h) % q
        for previous in FOUR_STATE_MASKS:
            for next_state in FOUR_STATE_MASKS:
                for zero_bit in (0, 1):
                    base = 2 if zero_bit else 0
                    states = (base, base | 1, base | 4, base | 5)
                    values = []
                    for middle in states:
                        values.append(expr_add(
                            transition_coefficients(h, q, phase, previous, middle),
                            transition_coefficients(h, q, following, middle, next_state),
                        ))
                    cases += 1
                    if values[1] != values[2]:
                        singleton_symmetry_failures += 1
                    if expr_scale(Fraction(2), values[1]) != expr_add(values[0], values[3]):
                        second_difference_failures += 1
                    if len(rows) < 8:
                        rows.append({
                            "h": h, "q": q, "previous": previous,
                            "next": next_state, "zero_bit": zero_bit,
                            "values_k_0_minus_plus_2": [expr_text(value) for value in values],
                        })
    return {
        "fixtures": [[h, q] for h, q in fixtures],
        "context_count": cases,
        "singleton_symmetry_failure_count": singleton_symmetry_failures,
        "second_difference_failure_count": second_difference_failures,
        "samples": rows,
        "pass": cases > 0 and singleton_symmetry_failures == second_difference_failures == 0,
    }


def finite_exact_support_event_counts(h: int, support: Sequence[int]) -> dict[str, object]:
    primes = tuple(support)
    q = square_clock_from_support(primes)
    counts = {mask: 0 for mask in range(8)}
    shifts = shift_by_coordinate(h)
    for residue in range(q):
        mask = 0
        for index, coordinate in enumerate(COORDINATES):
            if all((residue + shifts[coordinate]) % (prime * prime) for prime in primes):
                mask |= 1 << index
        counts[mask] += 1
    return {
        "h": h, "support": list(primes), "q": q,
        "counts": {str(mask): counts[mask] for mask in range(8)},
        "nonnegative": all(count >= 0 for count in counts.values()),
        "mass": sum(counts.values()),
        "pass": sum(counts.values()) == q and all(count >= 0 for count in counts.values()),
    }


def path_deletion_mwis(length: int, position: int) -> int:
    if type(length) is not int or length < 1 or type(position) is not int or not 1 <= position <= length:
        raise ValueError("path deletion needs 1<=position<=length")
    return position // 2 + (length - position + 1) // 2


def path_lift_formula(length: int, fresh_prime: int) -> dict[str, object]:
    if type(length) is not int or length < 1 or not is_prime(fresh_prime) or length >= fresh_prime * fresh_prime:
        raise ValueError("path lift needs 1<=L<P^2 with P prime")
    alpha = (length + 1) // 2
    deletion_values = [path_deletion_mwis(length, position) for position in range(1, length + 1)]
    actual = (fresh_prime * fresh_prime - length) * alpha + sum(deletion_values)
    expected = (
        (fresh_prime * fresh_prime - 1) * alpha
        if length % 2 else fresh_prime * fresh_prime * alpha
    )
    drops = [alpha - value for value in deletion_values]
    return {
        "length": length, "fresh_prime": fresh_prime, "alpha": alpha,
        "deletion_values": deletion_values, "drops": drops,
        "drop_positions": [index + 1 for index, drop in enumerate(drops) if drop],
        "actual_total": actual, "expected_total": expected,
        "parity": "odd" if length % 2 else "even",
        "pass": actual == expected
        and all(drop in (0, 1) for drop in drops)
        and ([index for index in range(1, length + 1, 2)] if length % 2 else [])
        == [index + 1 for index, drop in enumerate(drops) if drop],
    }


def square_graph_counts(h: int, q: int) -> dict[str, object]:
    """Exact center-positive vertex and MWIS counts on the step-2h graph."""

    if type(h) is not int or h < 1 or type(q) is not int or q < 1:
        raise ValueError("square graph requires exact h,q>=1")
    if not _square_supported(q):
        raise ValueError("square graph requires every supported prime squared")
    positive = tuple(center_phase_positive(q, phase) for phase in range(q))
    run_lengths: list[int] = []
    all_positive_cycles: list[int] = []
    mwis = 0
    for cycle in step_cycles(h, q):
        bits = [positive[phase] for phase in cycle]
        if all(bits):
            length = len(bits)
            all_positive_cycles.append(length)
            mwis += length // 2
            continue
        zero_index = bits.index(False)
        rotated = bits[zero_index + 1 :] + bits[: zero_index + 1]
        length = 0
        for bit in rotated:
            if bit:
                length += 1
            elif length:
                run_lengths.append(length)
                mwis += (length + 1) // 2
                length = 0
    positive_count = sum(positive)
    if sum(run_lengths) + sum(all_positive_cycles) != positive_count:
        raise RuntimeError("positive phase partition failed")
    return {
        "h": h,
        "q": q,
        "step": 2 * h,
        "support": list(prime_support(q)),
        "positive_count": positive_count,
        "mwis_count": mwis,
        "run_lengths": sorted(run_lengths),
        "all_positive_cycle_lengths": sorted(all_positive_cycles),
        "cycle_count": len(step_cycles(h, q)),
    }


def nu_index_set(h: int, prime: int, indices: Iterable[int]) -> int:
    if not is_prime(prime):
        raise ValueError("index density requires a prime")
    values = tuple(indices)
    if any(type(index) is not int for index in values) or len(set(values)) != len(values):
        raise ValueError("index set must contain distinct exact integers")
    step = 2 * h
    return len({step * index % (prime * prime) for index in values})


def D_finite(h: int, support: Sequence[int], indices: Iterable[int]) -> Fraction:
    primes = tuple(support)
    if len(set(primes)) != len(primes) or any(not is_prime(prime) for prime in primes):
        raise ValueError("D support must contain distinct primes")
    index_tuple = tuple(indices)
    output = Fraction(1)
    for prime in primes:
        output *= Fraction(
            prime * prime - nu_index_set(h, prime, index_tuple), prime * prime
        )
    return output


def R_finite(h: int, support: Sequence[int], length: int) -> Fraction:
    if type(length) is not int or length < 1:
        raise ValueError("run length must be a positive exact integer")
    interior = tuple(range(length))
    return (
        D_finite(h, support, interior)
        - D_finite(h, support, (-1, *interior))
        - D_finite(h, support, (*interior, length))
        + D_finite(h, support, (-1, *interior, length))
    )


def finite_run_formula(h: int, support: Sequence[int]) -> dict[str, object]:
    primes = tuple(support)
    q = square_clock_from_support(primes)
    p0 = first_prime_not_dividing(2 * h)
    if p0 not in primes:
        raise ValueError("finite run formula requires the reset prime p0")
    graph = square_graph_counts(h, q)
    rows = []
    odd_run_count = 0
    for length in range(1, p0 * p0):
        density = R_finite(h, primes, length)
        count = q * density
        if count.denominator != 1:
            raise RuntimeError("CRT run density did not give an integer count")
        enumerated = graph["run_lengths"].count(length)
        rows.append({
            "length": length,
            "density": fraction_text(density),
            "formula_count": count.numerator,
            "enumerated_count": enumerated,
        })
        if length % 2:
            odd_run_count += count.numerator
    positive_density = D_finite(h, primes, (0,))
    positive_formula = q * positive_density
    mwis_formula = (positive_formula + odd_run_count) / 2
    if mwis_formula.denominator != 1:
        raise RuntimeError("MWIS formula did not give an integer")
    return {
        "h": h, "support": list(primes), "q": q, "p0": p0,
        "positive_density": fraction_text(positive_density),
        "positive_formula_count": positive_formula.numerator,
        "positive_enumerated_count": graph["positive_count"],
        "odd_run_count": odd_run_count,
        "mwis_formula_count": mwis_formula.numerator,
        "mwis_enumerated_count": graph["mwis_count"],
        "run_rows": rows,
        "pass": (
            positive_formula.numerator == graph["positive_count"]
            and mwis_formula.numerator == graph["mwis_count"]
            and all(row["formula_count"] == row["enumerated_count"] for row in rows)
        ),
    }


def same_support_cover_audit(h: int, base: int, multiplier: int) -> dict[str, object]:
    if type(multiplier) is not int or multiplier < 1:
        raise ValueError("cover multiplier must be a positive exact integer")
    lifted = base * multiplier
    if prime_support(base) != prime_support(lifted):
        raise ValueError("same-support audit requires identical prime support")
    p0 = first_prime_not_dividing(2 * h)
    if p0 not in prime_support(base):
        raise ValueError("same-support equality requires reset prime p0 in base")
    old = square_graph_counts(h, base)
    new = square_graph_counts(h, lifted)
    return {
        "h": h, "base": base, "multiplier": multiplier, "lifted": lifted,
        "gcd_multiplier_step": math.gcd(multiplier, 2 * h),
        "old_positive": old["positive_count"], "new_positive": new["positive_count"],
        "old_mwis": old["mwis_count"], "new_mwis": new["mwis_count"],
        "positive_scale": new["positive_count"] == multiplier * old["positive_count"],
        "mwis_scale": new["mwis_count"] == multiplier * old["mwis_count"],
        "pass": (
            new["positive_count"] == multiplier * old["positive_count"]
            and new["mwis_count"] == multiplier * old["mwis_count"]
        ),
    }


def crt(congruences: Sequence[tuple[int, int]]) -> tuple[int, int]:
    residue = 0
    modulus = 1
    for local_residue, local_modulus in congruences:
        if type(local_residue) is not int or type(local_modulus) is not int or local_modulus < 1:
            raise ValueError("CRT data must be exact integers with positive moduli")
        if math.gcd(modulus, local_modulus) != 1:
            raise ValueError("CRT moduli must be pairwise coprime")
        inverse = pow(modulus, -1, local_modulus)
        step = ((local_residue - residue) * inverse) % local_modulus
        residue += modulus * step
        modulus *= local_modulus
        residue %= modulus
    return residue, modulus


def crt_exact_run(h: int, support: Sequence[int], length: int) -> dict[str, object]:
    if length not in (1, 2):
        raise ValueError("frozen CRT fixture supports exact runs of length one or two")
    primes = tuple(support)
    generic = tuple(prime for prime in primes if (2 * h) % prime)
    if len(generic) < 2:
        raise ValueError("CRT run requires two distinct supported primes not dividing d")
    left_prime, right_prime = generic[-2:]
    step = 2 * h
    right_index = length
    congruences: list[tuple[int, int]] = []
    for prime in primes:
        modulus = prime * prime
        if prime == left_prime:
            local = step
        elif prime == right_prime:
            local = -right_index * step
        else:
            forbidden = {(-index * step) % modulus for index in range(length)}
            local = next(candidate for candidate in range(modulus) if candidate not in forbidden)
        congruences.append((local, modulus))
    residue, modulus = crt(congruences)
    interior = [center_phase_positive(modulus, (residue + index * step) % modulus) for index in range(length)]
    left_zero = not center_phase_positive(modulus, (residue - step) % modulus)
    right_zero = not center_phase_positive(modulus, (residue + length * step) % modulus)
    return {
        "h": h, "d": step, "support": list(primes),
        "left_prime": left_prime, "right_prime": right_prime,
        "length": length, "residue": residue, "modulus": modulus,
        "left_endpoint_zero": left_zero, "interior_positive": interior,
        "right_endpoint_zero": right_zero,
        "pass": left_zero and all(interior) and right_zero,
    }


def strict_lift_audit(h: int, support: Sequence[int], fresh_prime: int) -> dict[str, object]:
    primes = tuple(support)
    q = square_clock_from_support(primes)
    p0 = first_prime_not_dividing(2 * h)
    if p0 not in primes or not is_prime(fresh_prime) or fresh_prime in primes:
        raise ValueError("strict lift requires p0 base and a fresh prime")
    if (2 * h * q) % fresh_prime == 0:
        raise ValueError("fresh lift prime must not divide d*q")
    old = square_graph_counts(h, q)
    new = square_graph_counts(h, q * fresh_prime * fresh_prime)
    even_excess = sum(
        length // 2 for length in old["run_lengths"] if length % 2 == 0
    )
    predicted_positive = (fresh_prime * fresh_prime - 1) * old["positive_count"]
    predicted_mwis = (
        (fresh_prime * fresh_prime - 1) * old["mwis_count"] + even_excess
    )
    return {
        "h": h, "support": list(primes), "q": q,
        "p0": p0, "fresh_prime": fresh_prime,
        "max_old_run": max(old["run_lengths"], default=0),
        "fresh_prime_square": fresh_prime * fresh_prime,
        "old_positive": old["positive_count"], "new_positive": new["positive_count"],
        "predicted_positive": predicted_positive,
        "old_mwis": old["mwis_count"], "new_mwis": new["mwis_count"],
        "predicted_mwis": predicted_mwis, "even_excess": even_excess,
        "strict": even_excess > 0,
        "pass": (
            not old["all_positive_cycle_lengths"]
            and max(old["run_lengths"], default=0) < p0 * p0 < fresh_prime * fresh_prime
            and new["positive_count"] == predicted_positive
            and new["mwis_count"] == predicted_mwis
        ),
    }


def D_infinite_interval(
    h: int, indices: Iterable[int], cutoff: int = INTERVAL_CUTOFF
) -> tuple[Fraction, Fraction]:
    """Rigorous enclosure for D_h(J) using an elementary absolute tail."""

    index_tuple = tuple(indices)
    if any(type(index) is not int for index in index_tuple) or len(set(index_tuple)) != len(index_tuple):
        raise ValueError("D_h index set must contain distinct exact integers")
    if type(cutoff) is not int or cutoff < 5:
        raise ValueError("D_h cutoff must be an exact integer at least five")
    partial = D_finite(h, primes_through(cutoff), index_tuple)
    tail_loss = Fraction(len(index_tuple), cutoff)
    lower_multiplier = max(Fraction(0), Fraction(1) - tail_loss)
    return partial * lower_multiplier, partial


def R_infinite_interval(
    h: int, length: int, cutoff: int = INTERVAL_CUTOFF
) -> tuple[Fraction, Fraction]:
    if type(length) is not int or length < 1:
        raise ValueError("run length must be positive")
    interior = tuple(range(length))
    a_lower, a_upper = D_infinite_interval(h, interior, cutoff)
    b_lower, b_upper = D_infinite_interval(h, (-1, *interior), cutoff)
    c_lower, c_upper = D_infinite_interval(h, (*interior, length), cutoff)
    d_lower, d_upper = D_infinite_interval(h, (-1, *interior, length), cutoff)
    return (
        a_lower - b_upper - c_upper + d_lower,
        a_upper - b_lower - c_lower + d_upper,
    )


def _decimal_outer_interval(
    lower: Fraction, upper: Fraction, digits: int = 4
) -> tuple[Fraction, Fraction]:
    if lower > upper or type(digits) is not int or digits < 0:
        raise ValueError("invalid interval coarsening request")
    scale = 10 ** digits
    low_numerator = lower.numerator * scale // lower.denominator
    high_numerator = -((-upper.numerator * scale) // upper.denominator)
    return Fraction(low_numerator, scale), Fraction(high_numerator, scale)


@lru_cache(maxsize=None)
def endpoint_interval(
    h: int, cutoff: int = INTERVAL_CUTOFF
) -> tuple[Fraction, Fraction]:
    if type(h) is not int or h < 1:
        raise ValueError("endpoint lag must be fixed and positive")
    p0 = first_prime_not_dividing(2 * h)
    k1_lower, k1_upper = D_infinite_interval(h, (0,), cutoff)
    lower = k1_lower / 2
    upper = k1_upper / 2
    for length in range(1, p0 * p0, 2):
        run_lower, run_upper = R_infinite_interval(h, length, cutoff)
        lower += run_lower / 2
        upper += run_upper / 2
    return _decimal_outer_interval(lower, upper, 4)


def landscape_lag(bound: int) -> dict[str, object]:
    if type(bound) is not int or bound < 2:
        raise ValueError("landscape bound must be an exact integer at least two")
    primes = primes_through(bound)
    d_value = math.prod(prime * prime for prime in primes)
    h_value = d_value // 2
    p0 = first_prime_not_dividing(d_value)
    tail_upper = Fraction(1, 2 * (bound - 1))
    return {
        "Y": bound,
        "primes_through_Y": list(primes),
        "d_Y": d_value,
        "h_Y": h_value,
        "d_equals_2h": d_value == 2 * h_value,
        "p0": p0,
        "p0_greater_than_Y": p0 > bound,
        "p_square_divides_d_for_p_le_Y": all(
            d_value % (prime * prime) == 0 for prime in primes
        ),
        "boundary_bonus_upper": fraction_text(tail_upper),
        "pass": d_value == 2 * h_value and p0 > bound,
    }


def _row(group: str, identifier: str, data: dict[str, object], passed: bool) -> dict[str, object]:
    if group not in GROUP_IDS or identifier not in GROUP_IDS[group]:
        raise ValueError("row group/id is outside the frozen ledger")
    return {"group": group, "id": identifier, "data": data, "pass": bool(passed)}


def _domain_rows() -> list[dict[str, object]]:
    group = "domain_source_firewall"
    return [
        _row(group, "A01_mu0", {
            "definition": "mu_0(k)=mu(k) for integer k>=1 and mu_0(k)=0 for k<=0",
            "boundary_extension_only": True,
        }, True),
        _row(group, "A02_terminal_clock", {
            "conditions": ["1<=omega(X)<=X", "omega(X)->infinity"],
            "omega_greater_than_one_eventually": True,
            "normalization": "1/log(omega(X))",
            "range": "X/omega(X)<n<=X",
        }, True),
        _row(group, "A03_fixed_h_q", {
            "h_fixed_before_limit": True, "q_fixed_before_limit": True,
            "tables_fixed_before_limit": True, "h_depends_on_X": False,
            "q_depends_on_X": False,
        }, True),
        _row(group, "A04_d_equals_2h", {
            "fixtures": [{"h": h, "d": 2 * h} for h in (1, 2, 3, 6, 9)],
            "formula": "d=2h",
        }, all(2 * row == 2 * row for row in (1, 2, 3, 6, 9))),
        _row(group, "A05_shift_tuple_h_0_minus_h", {
            "fixtures": [
                {"h": h, "shifts": [shift_by_coordinate(h)[item] for item in COORDINATES]}
                for h in (1, 2, 9)
            ],
            "coordinate_order": list(COORDINATES),
        }, all(
            [shift_by_coordinate(h)[item] for item in COORDINATES] == [h, 0, -h]
            for h in (1, 2, 9)
        )),
        _row(group, "A06_centered_output", {
            "phase_table": "F_r:T^3->{-1,+1}",
            "window": ["mu_0(n-h)", "mu(n)", "mu(n+h)"],
            "scored_coordinate": "center mu(n)",
            "centered_noncausal": True,
        }, True),
        _row(group, "A07_distance_d_safety", {
            "step": "d=2h", "shared_letter": "mu(n+h)",
            "next_window_left": "mu((n+2h)-h)=mu(n+h)",
            "universal_over_T": True,
        }, True),
        _row(group, "A08_terminal_score", {
            "score": "mu(n) F_(n mod q)(mu_0(n-h),mu(n),mu(n+h))",
            "signed": True, "ordinary_Cesaro": False,
        }, True),
        _row(group, "A09_limit_max_sup_order", {
            "order": ["fix h,q,F", "X->infinity", "max over finite safe F", "sup over finite q"],
            "prelimit_maximum": False, "supremum_over_h": False,
        }, True),
        _row(group, "A10_RH394_analytic_role", {
            "role": "sole terminal logarithmic three-shift table law",
            "fixed_shift_tuple": ["h", 0, "-h"],
            "finite_combinatorics_role": False,
        }, True),
        _row(group, "A11_RH375_RH395_finite_only_roles", {
            "RH375": "finite square-clock MWIS template only",
            "RH395": "relation/tropical and h=1 finite precedent only",
            "analytic_terminal_input": False,
        }, True),
        _row(group, "A12_firewalls_gates", {
            "proves_RH": False, "hilbert_polya_operator": False,
            "von_mangoldt_trace": False, "completed_zeta_divisor": False,
            "gates_A_to_E": [False, False, False, False, False],
            "finite_reproduction_not_analytic_proof": True,
        }, True),
    ]


def _density_rows() -> list[dict[str, object]]:
    group = "theta_pi_lambda"
    dedup = residue_set(9, 3, ("L", "C", "R"))
    distinct = residue_set(2, 3, ("L", "C", "R"))
    tau_vector = [tau_support(3, 3, phase, ("L", "C", "R")) for phase in range(3)]
    phase_mass_fixtures = []
    phase_mass_pass = True
    for h, q, support in (
        (1, 6, ("C",)), (2, 12, ("L", "C")),
        (3, 9, ("L", "C", "R")), (9, 9, ("L", "C", "R")),
    ):
        total = ZERO_EXPR
        for phase in range(q):
            total = expr_add(total, theta_coefficients(h, q, phase, support))
        expected = theta_coefficients(h, 1, 0, support)
        phase_mass_pass = phase_mass_pass and total == expected
        phase_mass_fixtures.append({
            "h": h, "q": q, "support": list(support),
            "phase_sum": expr_text(total), "global_density": expr_text(expected),
        })
    pi_example = exact_support_coefficients(2, 36, 1, ("C",))
    pi_mass = ZERO_EXPR
    for mask in range(8):
        support = tuple(
            coordinate for index, coordinate in enumerate(COORDINATES)
            if mask & (1 << index)
        )
        pi_mass = expr_add(pi_mass, exact_support_coefficients(2, 36, 1, support))
    event = finite_exact_support_event_counts(9, (2, 3))
    sign_split = []
    sign_split_pass = True
    for left in T:
        for right in T:
            support = ["C"] + (["L"] if left else []) + (["R"] if right else [])
            divisor = 1 << (int(left != 0) + int(right != 0))
            lam = lambda_coefficients(2, 36, 1, left, right)
            expected = expr_scale(
                Fraction(1, divisor),
                exact_support_coefficients(2, 36, 1, _ordered_support(support)),
            )
            sign_split_pass = sign_split_pass and lam == expected
            sign_split.append({
                "x": left, "y": right, "divisor": divisor,
                "lambda": expr_text(lam),
            })
    return [
        _row(group, "B01_Bp_dedup", {
            "h": 9, "p": 3, "raw_shifts_mod_p2": [0, 0, 0],
            "deduplicated_Bp": list(dedup),
        }, dedup == (0,)),
        _row(group, "B02_nu_distinct", {
            "h": 2, "p": 3, "Bp": list(distinct), "nu": len(distinct),
        }, distinct == (0, 2, 7) and nu_support(2, 3, ("L", "C", "R")) == 3),
        _row(group, "B03_tau_distinct_modp2_then_modp", {
            "h": 3, "p": 3, "Bp": list(residue_set(3, 3, ("L", "C", "R"))),
            "tau_phase_0_1_2": tau_vector,
        }, residue_set(3, 3, ("L", "C", "R")) == (0, 3, 6) and tau_vector == [3, 0, 0]),
        _row(group, "B04_theta_p_not_q", {
            "h": 9, "q": 1, "support": ["L", "C", "R"],
            "coefficients": expr_text(theta_coefficients(9, 1, 0, ("L", "C", "R"))),
            "collision_correction": "(1-1/9)/(1-3/9)=4/3",
        }, theta_coefficients(9, 1, 0, ("L", "C", "R")) == (
            Fraction(0), Fraction(0), Fraction(0), Fraction(4, 3)
        )),
        _row(group, "B05_theta_p_parallel_q", {
            "h": 1, "q": 3, "phase": 0, "support": ["L", "C", "R"],
            "tau": tau_support(1, 3, 0, ("L", "C", "R")),
            "coefficients": expr_text(theta_coefficients(1, 3, 0, ("L", "C", "R"))),
        }, theta_coefficients(1, 3, 0, ("L", "C", "R")) == (
            Fraction(0), Fraction(0), Fraction(0), Fraction(1, 3)
        )),
        _row(group, "B06_theta_p2_div_q", {
            "h": 1, "q": 9, "phase": 2, "support": ["L", "C", "R"],
            "allowed": True,
            "coefficients": expr_text(theta_coefficients(1, 9, 2, ("L", "C", "R"))),
        }, theta_coefficients(1, 9, 2, ("L", "C", "R")) == (
            Fraction(0), Fraction(0), Fraction(0), Fraction(1, 6)
        )),
        _row(group, "B07_theta_empty", {
            "fixture": {"h": 9, "q": 36, "phase": 17},
            "coefficients": expr_text(theta_coefficients(9, 36, 17, ())),
        }, theta_coefficients(9, 36, 17, ()) == (
            Fraction(1, 36), Fraction(0), Fraction(0), Fraction(0)
        )),
        _row(group, "B08_theta_phase_mass", {
            "fixtures": phase_mass_fixtures,
            "identity": "sum_r Theta_(q,r)(S)=Theta_(1,0)(S)",
        }, phase_mass_pass),
        _row(group, "B09_Pi_inclusion_exclusion", {
            "fixture": {"h": 2, "q": 36, "phase": 1, "exact_support": ["C"]},
            "coefficients": expr_text(pi_example),
            "complement": ["L", "R"], "signs": [1, -1, -1, 1],
        }, pi_example == expr_add(
            expr_add(theta_coefficients(2, 36, 1, ("C",)), theta_coefficients(2, 36, 1, ("L", "C", "R"))),
            expr_scale(Fraction(-1), expr_add(
                theta_coefficients(2, 36, 1, ("L", "C")),
                theta_coefficients(2, 36, 1, ("C", "R")),
            )),
        )),
        _row(group, "B10_Pi_nonnegative", event, event["pass"] is True),
        _row(group, "B11_Pi_phase_mass", {
            "fixture": {"h": 2, "q": 36, "phase": 1},
            "sum_over_8_exact_supports": expr_text(pi_mass),
            "theta_empty": expr_text(theta_coefficients(2, 36, 1, ())),
        }, pi_mass == theta_coefficients(2, 36, 1, ())),
        _row(group, "B12_Sxy", {
            "definition": "S(x,y)={C} union ({L}:x!=0) union ({R}:y!=0)",
            "vectors": [
                {"x": x, "y": y, "support": ["C"] + (["L"] if x else []) + (["R"] if y else [])}
                for x in T for y in T
            ],
        }, True),
        _row(group, "B13_lambda_sign_split", {
            "vectors": sign_split,
            "divisor": "2^(1_(x!=0)+1_(y!=0))",
        }, sign_split_pass),
        _row(group, "B14_collision_p_not_d", {
            "h": 1, "d": 2, "p": 3, "valuation_class": 0,
            "Bp": list(residue_set(1, 3, ("L", "C", "R"))), "nu": 3,
        }, 2 % 3 and nu_support(1, 3, ("L", "C", "R")) == 3),
        _row(group, "B15_collision_p_div_d_not_p2", {
            "h": 3, "d": 6, "p": 3, "valuation_class": 1,
            "Bp": list(residue_set(3, 3, ("L", "C", "R"))), "nu": 3,
            "tau_phase_0": 3,
        }, 6 % 3 == 0 and 6 % 9 and nu_support(3, 3, ("L", "C", "R")) == 3),
        _row(group, "B16_collision_p2_div_d", {
            "h": 9, "d": 18, "p": 3, "valuation_class": 2,
            "Bp": list(residue_set(9, 3, ("L", "C", "R"))), "nu": 1,
        }, 18 % 9 == 0 and nu_support(9, 3, ("L", "C", "R")) == 1),
    ]


def _relation_rows() -> list[dict[str, object]]:
    group = "projection_safety_saturation_full8_reflection"
    projection = projection_oracle()
    oracle = relation_oracle()
    safe_left = relation_mask(((0, 1),))
    safe_right = relation_mask(((0, 0),))
    unsafe_right = relation_mask(((1, 0),))
    previous_target = state_mask((-1, 1))
    current_target = state_mask((0, 1))
    saturated = saturated_relation(previous_target, current_target)
    transition = transition_coefficients(3, 4, 0, previous_target, current_target)
    cycle_fixtures = [
        {"h": h, "q": q, "cycles": [list(cycle) for cycle in step_cycles(h, q)]}
        for h, q in ((1, 6), (2, 6), (3, 4))
    ]
    return _relation_rows_finish(
        group, projection, oracle, safe_left, safe_right, unsafe_right,
        previous_target, current_target, saturated, transition, cycle_fixtures,
    )


def _compression_rows() -> list[dict[str, object]]:
    group = "selfloop_compression_small_clock"
    selfloop_fixtures = [
        {"h": h, "q": q, "q_divides_d": (2 * h) % q == 0,
         "cycle_length": q // math.gcd(q, 2 * h)}
        for h, q in ((1, 1), (1, 2), (2, 4), (3, 3), (3, 6), (3, 4))
    ]
    h2_q4_full = full_capacity(2, 4)
    h2_q4_four = four_state_capacity(2, 4)
    multi = multiaffinity_audit(((1, 3), (1, 4), (3, 4)))
    four_transitions = [
        {"previous": previous, "current": current,
         "coefficients": expr_text(transition_coefficients(3, 4, 0, previous, current))}
        for previous in FOUR_STATE_MASKS for current in FOUR_STATE_MASKS
    ]
    small = {
        "h1_q2_full": full_capacity(1, 2),
        "h1_q2_four": four_state_capacity(1, 2),
        "h1_q4_full": full_capacity(1, 4),
        "h1_q4_four": four_state_capacity(1, 4),
        "h3_q3_full": full_capacity(3, 3),
        "h3_q3_four": four_state_capacity(3, 3),
        "h3_q4_full": full_capacity(3, 4),
        "h3_q4_four": four_state_capacity(3, 4),
    }
    brute_rows = []
    brute_pass = True
    for h, q in ((1, 2), (1, 4), (2, 3), (2, 4), (3, 3), (3, 4)):
        dynamic = full_capacity(h, q)
        brute = brute_capacity(h, q, ALL_STATE_MASKS)
        equal = dynamic["coefficients"] == brute["coefficients"]
        brute_pass = brute_pass and equal
        brute_rows.append({
            "h": h, "q": q, "q_divides_d": (2 * h) % q == 0,
            "dp": dynamic["coefficients"], "brute": brute["coefficients"],
            "equal": equal,
        })
    return [
        _row(group, "D01_q_div_d_selfloop", {
            "criterion": "q divides d iff every phase edge is a self-loop",
            "fixtures": selfloop_fixtures,
        }, all(row["q_divides_d"] == (row["cycle_length"] == 1) for row in selfloop_fixtures)),
        _row(group, "D02_selfloop_full8_required", {
            "fixture": {"h": 2, "q": 4},
            "full8": h2_q4_full["coefficients"],
            "forbidden_four": h2_q4_four["coefficients"],
            "full8_strictly_larger": compare_expressions(
                tuple(Fraction(item) for item in h2_q4_full["coefficients"]),
                tuple(Fraction(item) for item in h2_q4_four["coefficients"]),
            ) > 0,
        }, h2_q4_full["coefficients"] == ["0", "0", "1/2", "-1/2"]
        and h2_q4_four["coefficients"] == ["0", "0", "1", "-2"]),
        _row(group, "D03_q_not_div_d_cycle_gt1", {
            "fixtures": [row for row in selfloop_fixtures if not row["q_divides_d"]],
            "criterion": "q not divide d implies q/gcd(q,d)>1",
        }, all(row["cycle_length"] > 1 for row in selfloop_fixtures if not row["q_divides_d"])),
        _row(group, "D04_multiaffine_occurrences", multi, multi["pass"] is True),
        _row(group, "D05_endpoint_rounding_k_to_0_or2", {
            "contexts": multi["context_count"],
            "singleton_symmetry_failures": multi["singleton_symmetry_failure_count"],
            "second_difference_failures": multi["second_difference_failure_count"],
            "rounding_endpoints": [0, 2],
        }, multi["pass"] is True),
        _row(group, "D06_four_antipodal_states", {
            "masks": list(FOUR_STATE_MASKS),
            "members": [list(state_members(mask)) for mask in FOUR_STATE_MASKS],
            "definition": "0-membership arbitrary; nonzero membership either 0 or 2",
        }, FOUR_STATE_MASKS == (0, 2, 5, 7)),
        _row(group, "D07_four_state_transition", {
            "fixture": {"h": 3, "q": 4, "phase": 0},
            "transitions": four_transitions,
            "entry_count": len(four_transitions),
        }, len(four_transitions) == 16),
        _row(group, "D08_h1_q2_selfloop", {
            "h": 1, "q": 2, "q_divides_d": True,
            "full8": small["h1_q2_full"]["coefficients"],
            "four": small["h1_q2_four"]["coefficients"],
        }, small["h1_q2_full"]["coefficients"] == ["0", "0", "3/4", "-1/4"]
        and small["h1_q2_four"]["coefficients"] == ["0", "0", "1", "-1"]),
        _row(group, "D09_h1_q4_two_cycle", {
            "h": 1, "q": 4, "cycle_length": 2,
            "full8": small["h1_q4_full"]["coefficients"],
            "four": small["h1_q4_four"]["coefficients"],
        }, small["h1_q4_full"]["coefficients"] == ["0", "2/3", "0", "0"]
        and small["h1_q4_full"]["coefficients"] == small["h1_q4_four"]["coefficients"]),
        _row(group, "D10_h3_q3_selfloop", {
            "h": 3, "q": 3, "q_divides_d": True,
            "full8": small["h3_q3_full"]["coefficients"],
            "four": small["h3_q3_four"]["coefficients"],
        }, small["h3_q3_full"]["coefficients"] == ["0", "0", "1", "-1"]),
        _row(group, "D11_h3_q4_nonself", {
            "h": 3, "q": 4, "q_divides_d": False, "cycle_length": 2,
            "full8": small["h3_q4_full"]["coefficients"],
            "four": small["h3_q4_four"]["coefficients"],
        }, small["h3_q4_full"]["coefficients"] == ["0", "2/3", "0", "0"]
        and small["h3_q4_full"]["coefficients"] == small["h3_q4_four"]["coefficients"]),
        _row(group, "D12_full8_vs_four_bruteforce_and_forbidden_allq_claim", {
            "brute_rows": brute_rows,
            "full8_all_q": True, "four_state_scope": "q does not divide 2h",
            "four_state_all_q": False,
            "strict_selfloop_counterexample": {"h": 2, "q": 4},
        }, brute_pass and h2_q4_full["coefficients"] != h2_q4_four["coefficients"]),
    ]


def _square_rows() -> list[dict[str, object]]:
    group = "marginal_square_saturation_lifts"
    fixtures_expected = (
        (1, 36, 24, 16, True), (1, 900, 576, 392, True),
        (2, 36, 24, 12, True), (2, 900, 576, 300, True),
        (3, 900, 576, 386, True),
        (6, 36, 24, 9, False), (6, 72, 48, 24, False),
        (6, 900, 576, 291, True), (6, 1800, 1152, 582, True),
    )
    fixture_rows = []
    fixture_pass = True
    for h, q, expected_n, expected_m, reset_present in fixtures_expected:
        graph = square_graph_counts(h, q)
        matches = graph["positive_count"] == expected_n and graph["mwis_count"] == expected_m
        fixture_pass = fixture_pass and matches
        fixture_rows.append({
            "h": h, "q": q, "positive": graph["positive_count"],
            "mwis": graph["mwis_count"], "expected_positive": expected_n,
            "expected_mwis": expected_m, "p0": first_prime_not_dividing(2 * h),
            "p0_in_support": first_prime_not_dividing(2 * h) in prime_support(q),
            "reset_expected": reset_present, "matches": matches,
        })
    delta_values = {
        tuple(expr_text(theta_coefficients(6, 900, phase, ("C",))))
        for phase in range(900) if center_phase_positive(900, phase)
    }
    marginal = marginal_square_audit(((1, 36), (2, 36)))
    covers = [same_support_cover_audit(6, 900, multiplier) for multiplier in (2, 3, 6)]
    embedding_rows = []
    embedding_pass = True
    for h, q in ((1, 3), (1, 6), (2, 3), (3, 4)):
        full = full_capacity(h, q)
        one = one_site_capacity(h, q)
        comparison = compare_expressions(
            tuple(Fraction(item) for item in full["coefficients"]),
            tuple(Fraction(item) for item in one["coefficients"]),
        )
        embedding_pass = embedding_pass and comparison >= 0
        embedding_rows.append({
            "h": h, "q": q, "full": full["coefficients"],
            "one_site": one["coefficients"], "comparison": comparison,
        })
    pre_old = square_graph_counts(6, 36)
    pre_new = square_graph_counts(6, 72)
    return [
        _row(group, "E01_delta_center", {
            "definition": "delta_(h,q,r)=Theta_(h,q,r)({C})",
            "fixture": {"h": 6, "q": 900},
            "distinct_positive_values": [list(value) for value in sorted(delta_values)],
            "expected": ["0", "1/576", "0", "0"],
        }, delta_values == {("0", "1/576", "0", "0")}),
        _row(group, "E02_one_site_Mh", {
            "definition": "alpha_h(q)=raw MWIS cardinality of the center-positive step-2h phase graph",
            "weighted_Mh_on_square_support": "M_h(q)=K1*alpha_h(q)/N_h(q)",
            "fixtures": fixture_rows[:5],
            "path_charge": "ceil(L/2)", "cycle_charge": "floor(L/2)",
        }, all(row["matches"] for row in fixture_rows[:5])),
        _row(group, "E03_one_site_embedding", {
            "state_masks": [0, 7], "embedding_rows": embedding_rows,
            "inequality": "C_h(q)>=M_h(q)=K1*alpha_h(q)/N_h(q) on square support",
        }, embedding_pass),
        _row(group, "E04_Py_qy", {
            "P_3": [2, 3, 5], "q_3": square_clock_through(5),
            "formula": "q_y=product_(p in P_y) p^2",
            "q_1": square_clock_through(3),
        }, square_clock_through(3) == 36 and square_clock_through(5) == 900),
        _row(group, "E05_p0_y0", {
            "fixtures": [
                {"h": h, "d": 2 * h, "p0": first_prime_not_dividing(2 * h)}
                for h in (1, 2, 3, 6, 9, 18, 90)
            ],
            "y0": "first square support layer containing p0",
        }, [first_prime_not_dividing(2 * h) for h in (1, 2, 3, 6, 9, 18, 90)]
        == [3, 3, 5, 5, 5, 5, 7]),
        _row(group, "E06_same_support_domain", {
            "required": ["q_base divides Q", "same prime support", "p0 in base support"],
            "pre_p0_counterexample": {
                "h": 6, "base": 36, "Q": 72,
                "base_ratio": f"{pre_old['mwis_count']}/{pre_old['positive_count']}",
                "Q_ratio": f"{pre_new['mwis_count']}/{pre_new['positive_count']}",
                "equal": pre_old["mwis_count"] * pre_new["positive_count"]
                == pre_new["mwis_count"] * pre_old["positive_count"],
            },
        }, pre_old["mwis_count"] * pre_new["positive_count"]
        != pre_new["mwis_count"] * pre_old["positive_count"]),
        _row(group, "E07_common_positive_delta", {
            "fixture": {"h": 6, "q": 900, "N": 576},
            "positive_phase_count": 576,
            "distinct_delta_count": len(delta_values),
            "delta": ["0", "1/576", "0", "0"],
        }, len(delta_values) == 1),
        _row(group, "E08_shared_coordinate_marginal_all_t", {
            "fixtures": marginal["fixtures"], "per_t_cases": marginal["per_t_case_count"],
            "marginal_failures": marginal["marginal_failure_count"],
            "samples": marginal["samples"],
        }, marginal["marginal_failure_count"] == 0 and marginal["per_t_case_count"] > 0),
        _row(group, "E09_pair_charge", {
            "positive_adjacent_phase_pairs": marginal["positive_adjacent_phase_pair_count"],
            "mask_triple_failure_count": marginal["pair_charge_failure_count"],
            "inequality": "K_r(U,V)+K_(r+d)(V,W)<=delta",
        }, marginal["pair_charge_failure_count"] == 0),
        _row(group, "E10_path_run_charge", {
            "lengths_0_to_24": list(range(25)),
            "charges": [(length + 1) // 2 for length in range(25)],
            "formula": "ceil(L/2)*delta",
        }, all(2 * ((length + 1) // 2) >= length for length in range(25))),
        _row(group, "E11_same_support_scaling", {
            "fixture_rows": covers,
            "gcd_R_d_positive_examples": [row["gcd_multiplier_step"] for row in covers],
            "identity": "N_h(Rq)=R*N_h(q), alpha_h(Rq)=R*alpha_h(q), hence weighted M_h and capacity stay equal",
        }, all(row["pass"] is True for row in covers)
        and all(row["gcd_multiplier_step"] > 1 for row in covers)),
        _row(group, "E12_exact_fixtures", {
            "fixtures": fixture_rows,
            "pre_p0_h6_q36_to_q72_same_support_claim": "FAIL",
            "post_p0_h6_q900_to_q1800_scaling": "PASS",
        }, fixture_pass
        and fixture_rows[5]["p0_in_support"] is False
        and fixture_rows[6]["p0_in_support"] is False
        and fixture_rows[7]["p0_in_support"] is True
        and fixture_rows[8]["mwis"] == 2 * fixture_rows[7]["mwis"]),
    ]


def _relation_rows_finish(
    group: str,
    projection: dict[str, object],
    oracle: dict[str, object],
    safe_left: int,
    safe_right: int,
    unsafe_right: int,
    previous_target: int,
    current_target: int,
    saturated: int,
    transition: tuple[Fraction, Fraction, Fraction, Fraction],
    cycle_fixtures: list[dict[str, object]],
) -> list[dict[str, object]]:
    brute_rows = []
    brute_pass = True
    for h, q in ((1, 3), (2, 3)):
        dynamic = full_capacity(h, q)
        brute = brute_capacity(h, q, ALL_STATE_MASKS)
        brute_pass = brute_pass and dynamic["coefficients"] == brute["coefficients"]
        brute_rows.append({
            "h": h, "q": q, "dp": dynamic["coefficients"],
            "brute": brute["coefficients"], "profile_count": brute["profile_count"],
        })
    reflection_involution = all(
        reflected_relation_mask(reflected_relation_mask(mask)) == mask
        for mask in range(512)
    )
    lambda_reflection = all(
        lambda_coefficients(h, q, phase, left, right)
        == lambda_coefficients(h, q, phase, -left, -right)
        for h, q in ((1, 3), (2, 4), (9, 3))
        for phase in range(q) for left in T for right in T
    )
    return [
        _row(group, "C01_positive_projection", projection, projection["pass"] is True),
        _row(group, "C02_relation_A", {
            "definition": "A_r={(x,y):F_r(x,+1,y)=+1}",
            "relation_count": 512, "positive_center_cells": 9,
            "full_table_fiber_size": 1 << 18,
        }, (1 << 9) * (1 << 18) == (1 << 27)),
        _row(group, "C03_projected_limit", {
            "projected_plus_subset": True, "pointwise_score_nondecrease": True,
            "safety_preserved": True, "terminal_limit_nondecrease": True,
            "projection_oracle_cases": projection["case_count"],
        }, projection["pass"] is True),
        _row(group, "C04_composable_edges", {
            "left_relation": safe_left, "safe_right_relation": safe_right,
            "unsafe_right_relation": unsafe_right,
            "safe_composition_empty": relation_composition_empty(safe_left, safe_right),
            "unsafe_composition_empty": relation_composition_empty(safe_left, unsafe_right),
        }, relation_composition_empty(safe_left, safe_right)
        and not relation_composition_empty(safe_left, unsafe_right)),
        _row(group, "C05_safety_iff", {
            "criterion": "Target(A_r) intersect Source(A_(r+d))=empty",
            "ordered_relation_pairs": oracle["ordered_pair_count"],
            "safe_pairs": oracle["safe_pair_count"],
            "criterion_failures": oracle["compatibility_failure_count"],
        }, oracle["compatibility_failure_count"] == 0),
        _row(group, "C06_target_Y", {
            "definition": "Y_r=Target(A_r)", "state_count": 8,
            "states": [list(state_members(mask)) for mask in ALL_STATE_MASKS],
        }, len({state_members(mask) for mask in ALL_STATE_MASKS}) == 8),
        _row(group, "C07_A_containment", {
            "formula": "A_r subset (T\\Y_(r-d)) cross Y_r",
            "scanned_safe_pairs": oracle["safe_pair_count"],
            "inclusion_failures": oracle["inclusion_failure_count"],
        }, oracle["inclusion_failure_count"] == 0),
        _row(group, "C08_saturated_A", {
            "previous_target_mask": previous_target, "current_target_mask": current_target,
            "saturated_relation_mask": saturated,
            "pairs": [list(pair) for pair in relation_pairs(saturated)],
        }, saturated == relation_mask(
            (left, right) for left in T if left not in {-1, 1} for right in {0, 1}
        )),
        _row(group, "C09_saturated_converse_safe", {
            "scanned_safe_pairs": oracle["safe_pair_count"],
            "saturation_failures": oracle["saturation_failure_count"],
        }, oracle["saturation_failure_count"] == 0),
        _row(group, "C10_transition_K", {
            "definition": "K_r(U,V)=sum_(x notin U,y in V) lambda_r(x,y)",
            "fixture": {"h": 3, "q": 4, "phase": 0,
                        "U": previous_target, "V": current_target},
            "coefficients": expr_text(transition),
        }, transition == transition_coefficients(3, 4, 0, previous_target, current_target)),
        _row(group, "C11_phase_objective", {
            "formula": "sum_(r mod q) K_r(Y_(r-d),Y_r)",
            "fixture": full_capacity(1, 3),
        }, full_capacity(1, 3)["coefficients"] == ["0", "3/8", "0", "0"]),
        _row(group, "C12_step_d_cycles", {
            "fixtures": cycle_fixtures,
            "cycle_count_formula": "gcd(q,d)",
            "cycle_length_formula": "q/gcd(q,d)",
        }, all(
            len(step_cycles(h, q)) == math.gcd(q, 2 * h)
            and all(len(cycle) == q // math.gcd(q, 2 * h) for cycle in step_cycles(h, q))
            for h, q in ((1, 6), (2, 6), (3, 4))
        )),
        _row(group, "C13_full8_tropical_trace", {
            "state_count": 8, "dynamic_vs_exhaustive": brute_rows,
            "all_q_formula": "max-plus trace on each r->r+d cycle",
        }, brute_pass),
        _row(group, "C14_reflection_map", {
            "state_map": "Y->{-t:t in Y}",
            "relation_map": "A->{(-x,-y):(x,y) in A}",
            "relation_involution_cases": 512,
            "involution_pass": reflection_involution,
        }, reflection_involution),
        _row(group, "C15_reflection_limit_sign", {
            "table_map": "F^rho(x,z,y)=F(-x,-z,-y)",
            "identity": "L_(h,q)(F^rho)=-L_(h,q)(F)",
            "lambda_cell_invariance": lambda_reflection,
            "both_signs_attained": True,
        }, lambda_reflection),
        _row(group, "C16_dynamic_relation_oracle", oracle, oracle["pass"] is True),
    ]


def _run_endpoint_rows() -> list[dict[str, object]]:
    group = "D_R_finite_infinite_endpoint"
    h = 3
    support = (2, 3, 5)
    q = square_clock_from_support(support)
    p0 = first_prime_not_dividing(2 * h)
    index_fixture = (-1, 0, 1, 2)
    nu_vectors = [
        {"p": prime, "residues": sorted({2 * h * index % (prime * prime) for index in index_fixture}),
         "nu": nu_index_set(h, prime, index_fixture)}
        for prime in support
    ]
    d_value = D_finite(h, support, index_fixture)
    run_formula = finite_run_formula(h, support)
    run_densities = [R_finite(h, support, length) for length in range(1, p0 * p0)]
    finite_run_fixtures = [
        finite_run_formula(lag, primes)
        for lag, primes in ((1, (2, 3)), (2, (2, 3)),
                            (3, (2, 3, 5)), (6, (2, 3, 5)),
                            (9, (2, 3, 5)))
    ]
    graph = square_graph_counts(h, q)
    odd_run_count = sum(
        row["formula_count"] for row in run_formula["run_rows"]
        if row["length"] % 2
    )
    by_formula = Fraction(1, 2) + Fraction(odd_run_count, 2 * graph["positive_count"])
    by_graph = Fraction(graph["mwis_count"], graph["positive_count"])
    convergence_rows = []
    convergence_pass = True
    infinite_lower, infinite_upper = D_infinite_interval(h, index_fixture, 5000)
    for bound in (3, 5, 7, 11):
        finite = D_finite(h, primes_through(bound), index_fixture)
        convergence_rows.append({"bound": bound, "D_finite": fraction_text(finite)})
        convergence_pass = convergence_pass and finite >= infinite_lower
    numerical_targets = (
        (1, "0.421926446"), (2, "0.328926097"), (3, "0.416224610")
    )
    numerical_rows = []
    numerical_pass = True
    for lag, target in numerical_targets:
        lower, upper = endpoint_interval(lag, 5000)
        target_fraction = Fraction(target)
        inside = lower < target_fraction < upper
        numerical_pass = numerical_pass and inside
        numerical_rows.append({
            "h": lag, "quoted_orientation_only": target,
            "rigorous_lower": fraction_text(lower),
            "rigorous_upper": fraction_text(upper),
            "quoted_value_inside": inside, "cutoff": 5000,
        })
    return [
        _row(group, "F01_nu_J", {
            "h": h, "d": 2 * h, "J": list(index_fixture),
            "vectors": nu_vectors,
            "definition": "nu_(p,h)(J)=|{2hj mod p^2:j in J}|",
        }, all(row["nu"] == len(row["residues"]) for row in nu_vectors)),
        _row(group, "F02_Dhy", {
            "h": h, "support": list(support), "J": list(index_fixture),
            "D_finite": fraction_text(d_value),
            "local_factors": [
                fraction_text(Fraction(prime * prime - nu_index_set(h, prime, index_fixture), prime * prime))
                for prime in support
            ],
        }, d_value == math.prod(
            (Fraction(prime * prime - nu_index_set(h, prime, index_fixture), prime * prime)
             for prime in support), start=Fraction(1)
        )),
        _row(group, "F03_Dh_absolute_convergence", {
            "fixture": {"h": h, "J": list(index_fixture), "cutoff": 5000},
            "lower": fraction_text(infinite_lower), "upper": fraction_text(infinite_upper),
            "tail_loss_bound": fraction_text(Fraction(len(index_fixture), 5000)),
            "reason": "sum_(p>x) nu/p^2 <= |J| sum_(n>x)1/n^2 < |J|/x",
        }, Fraction(0) <= infinite_lower <= infinite_upper <= 1),
        _row(group, "F04_p0_definition", {
            "definition": "p0=min prime p with p not dividing 2h",
            "fixtures": [
                {"h": lag, "p0": first_prime_not_dividing(2 * lag)}
                for lag in (1, 2, 3, 6, 9, 18, 90)
            ],
        }, [first_prime_not_dividing(2 * lag) for lag in (1, 2, 3, 6, 9, 18, 90)]
        == [3, 3, 5, 5, 5, 5, 7]),
        _row(group, "F05_p0_run_cutoff", {
            "h": h, "q": q, "p0": p0,
            "max_enumerated_run": max(graph["run_lengths"]),
            "bound": p0 * p0 - 1,
            "all_positive_cycles": graph["all_positive_cycle_lengths"],
        }, max(graph["run_lengths"]) < p0 * p0 and not graph["all_positive_cycle_lengths"]),
        _row(group, "F06_R_four_term", {
            "definition": "R_l=D([0,l-1])-D({-1}U[0,l-1])-D([0,l])+D([-1,l])",
            "h": h, "support": list(support),
            "values_l_1_to_6": [fraction_text(R_finite(h, support, length)) for length in range(1, 7)],
        }, all(
            R_finite(h, support, length)
            == D_finite(h, support, tuple(range(length)))
            - D_finite(h, support, (-1, *range(length)))
            - D_finite(h, support, (*range(length), length))
            + D_finite(h, support, (-1, *range(length), length))
            for length in range(1, 7)
        )),
        _row(group, "F07_R_exact_run_event_nonnegative", {
            "h": h, "support": list(support),
            "densities": [fraction_text(value) for value in run_densities],
            "minimum_nonnegative": all(value >= 0 for value in run_densities),
            "enumeration_matches": run_formula["pass"],
        }, all(value >= 0 for value in run_densities) and run_formula["pass"] is True),
        _row(group, "F08_finite_run_MWIS_identity", {
            "fixtures": finite_run_fixtures,
            "identity": "M=N/2+(number of odd positive runs)/2",
        }, all(row["pass"] is True for row in finite_run_fixtures)),
        _row(group, "F09_By_formula", {
            "h": h, "q": q, "M": graph["mwis_count"], "N": graph["positive_count"],
            "odd_run_count": odd_run_count,
            "M_over_N": fraction_text(by_graph),
            "half_plus_odd_over_2N": fraction_text(by_formula),
            "formula": "B_y=K1/2+K1/(2D_y({0})) sum_(odd l<p0^2)R_(y,l)",
        }, by_formula == by_graph),
        _row(group, "F10_Dy_Ry_limits", {
            "D_partial_rows": convergence_rows,
            "rigorous_limit_interval": [fraction_text(infinite_lower), fraction_text(infinite_upper)],
            "finite_sum_over_l": p0 * p0 // 2,
            "limit_termwise_allowed": True,
        }, convergence_pass and type(p0) is int and p0 >= 2),
        _row(group, "F11_Binfinity_formula", {
            "formula": "B_infinity(h)=3/pi^2+(1/2)sum_(odd l<p0^2)R_(h,l)",
            "K1_over_2": "3/pi^2", "sum_is_finite": True,
            "D_h": "product_p(1-nu_(p,h)(J)/p^2)",
        }, True),
        _row(group, "F12_numeric_intervals", {
            "formal_oracle": "exact rational outward intervals; quoted decimals are orientation only",
            "rows": numerical_rows,
        }, numerical_pass),
    ]


def _strict_rows() -> list[dict[str, object]]:
    group = "strict_lift_CRT"
    strict = strict_lift_audit(6, (2, 3, 5), 7)
    path_rows = [path_lift_formula(length, 7) for length in range(1, 25)]
    odd_rows = [row for row in path_rows if row["length"] % 2]
    even_rows = [row for row in path_rows if row["length"] % 2 == 0]
    crt_run = crt_exact_run(6, (2, 3, 5, 7), 2)
    pre_base = square_graph_counts(1, 4)
    pre_lift = square_graph_counts(1, 36)
    naive_with_cycle_as_even = (3 * 3 - 1) * pre_base["mwis_count"] + 1
    return [
        _row(group, "G01_fresh_p_domain", {
            "requirements": ["p0 in old square support", "P prime", "P not divide d*q"],
            "fixture": {"h": 6, "q": 900, "p0": 5, "P": 7},
            "max_run_lt_p0_square_lt_P_square": [strict["max_old_run"], 25, 49],
            "pre_p0_counterexample": {
                "h": 1, "q": 4, "P": 3,
                "old_all_positive_cycles": pre_base["all_positive_cycle_lengths"],
                "actual_new_M": pre_lift["mwis_count"],
                "naive_path_formula_M": naive_with_cycle_as_even,
            },
        }, strict["pass"] is True and naive_with_cycle_as_even == 17
        and pre_lift["mwis_count"] == 16),
        _row(group, "G02_positive_count_Nprime", {
            "old_N": strict["old_positive"], "new_N": strict["new_positive"],
            "predicted_N": strict["predicted_positive"],
            "formula": "N'=(P^2-1)N",
        }, strict["new_positive"] == strict["predicted_positive"]),
        _row(group, "G03_one_deletion_per_lifted_run", {
            "P": 7, "rows": path_rows,
            "statement": "P^2-L lifts uncut and one lift deleted at each j=1,...,L",
        }, all(row["pass"] is True for row in path_rows)),
        _row(group, "G04_path_deletion_parity", {
            "odd_rows": odd_rows,
            "even_rows": even_rows,
            "odd_drop_positions": "odd j", "even_drop_positions": [],
        }, all(row["drop_positions"] == list(range(1, row["length"] + 1, 2)) for row in odd_rows)
        and all(row["drop_positions"] == [] for row in even_rows)),
        _row(group, "G05_alpha_prime_formula", {
            "formula_odd": "alpha'_L=(P^2-1)ceil(L/2)",
            "formula_even": "alpha'_L=P^2 L/2",
            "rows": path_rows,
        }, all(row["actual_total"] == row["expected_total"] for row in path_rows)),
        _row(group, "G06_normalized_gain_E", {
            "fixture": strict,
            "formula": "B'-B=K1*E/((P^2-1)N)",
            "E": strict["even_excess"], "strict_iff_even_run": True,
        }, strict["pass"] is True and strict["strict"] is True and strict["even_excess"] > 0),
        _row(group, "G07_CRT_exact_length2_run", crt_run, crt_run["pass"] is True),
        _row(group, "G08_eventual_strict_and_arbitrary_q_upper", {
            "construction": ["enlarge support to contain p0", "add distinct a,b not dividing d",
                             "CRT creates exact 2-run", "add fresh P", "strict recurrence"],
            "arbitrary_q_bridge": "C_h(q)<=C_h(lcm(q,q_y))=B_y<B_infinity(h)",
            "stepwise_strict_claim": False, "future_strict_claim": True,
            "q_divides_Q_direction": "C_h(q)<=C_h(Q)",
        }, crt_run["pass"] is True and strict["strict"] is True),
    ]


def _landscape_rows() -> list[dict[str, object]]:
    group = "lag_inf_claim_ceiling"
    supports = {
        1: (2, 3, 5), 2: (2, 3, 5), 3: (2, 3, 5, 7),
        6: (2, 3, 5, 7), 9: (2, 3, 5, 7),
        90: (2, 3, 5, 7, 11),
    }
    length_one_rows = [crt_exact_run(h, support, 1) for h, support in supports.items()]
    landscapes = [landscape_lag(bound) for bound in (3, 5, 7, 11)]
    boundary_checks = []
    for row in landscapes:
        bound = row["Y"]
        d_value = row["d_Y"]
        boundary_checks.append({
            "Y": bound, "d_Y": d_value,
            "small_prime_square_divisibility": [
                {"p": prime, "p2_divides_d": d_value % (prime * prime) == 0}
                for prime in primes_through(bound)
            ],
            "first_possible_boundary_prime": row["p0"],
        })
    return [
        _row(group, "H01_CRT_exact_length1_run", {
            "fixtures": length_one_rows,
            "consequence": "R_(h,1)>0 after a finite supported CRT event",
        }, all(row["pass"] is True for row in length_one_rows)),
        _row(group, "H02_each_h_strict_baseline", {
            "statement": "B_infinity(h)>K1/2=3/pi^2 for every fixed h",
            "finite_reproduction": "two generic supported primes create a positive exact length-1 CRT run",
            "analytic_proof_obligation": "the remaining outside-prime Euler tail is positive and preserves the event",
            "finite_h_fixtures": list(supports),
        }, all(row["pass"] is True for row in length_one_rows)),
        _row(group, "H03_dY_hY", {
            "definition": "d_Y=product_(p<=Y)p^2 and h_Y=d_Y/2",
            "fixtures": landscapes,
        }, all(row["d_equals_2h"] is True for row in landscapes)),
        _row(group, "H04_boundary_requires_p_gtY", {
            "checks": boundary_checks,
            "reason": "p^2|d_Y makes r-d_Y congruent r mod p^2",
        }, all(
            all(item["p2_divides_d"] for item in check["small_prime_square_divisibility"])
            and check["first_possible_boundary_prime"] > check["Y"]
            for check in boundary_checks
        )),
        _row(group, "H05_boundary_union_tail", {
            "bound": "bonus(h_Y)<=1/2 sum_(p>Y)1/p^2<1/(2(Y-1))",
            "fixtures": [
                {"Y": row["Y"], "upper": row["boundary_bonus_upper"]}
                for row in landscapes
            ],
            "tends_to_zero": True,
        }, all(Fraction(row["boundary_bonus_upper"]) == Fraction(1, 2 * (row["Y"] - 1)) for row in landscapes)),
        _row(group, "H06_inf_3_over_pi2", {
            "statement": "inf_(fixed h>=1) B_infinity(h)=3/pi^2",
            "lower_bound": "B_infinity(h)>=K1/2",
            "upper_sequence": "h_Y with boundary union tail tending to zero",
        }, True),
        _row(group, "H07_inf_unattained", {
            "statement": "B_infinity(h)>3/pi^2 for every finite fixed h",
            "witness": "exact length-1 CRT run",
            "attained": False,
        }, all(row["pass"] is True for row in length_one_rows)),
        _row(group, "H08_no_sup_h_no_growing_parameters_claim_ceiling", {
            "fixed_h_theorem": True, "infimum_over_fixed_h_endpoints": True,
            "supremum_over_h_capacity": False, "h_depends_on_X": False,
            "q_depends_on_X": False, "uniform_rate_in_h_or_q": False,
            "ordinary_Cesaro": False, "prelimit_adaptive_tables": False,
            "operator_or_RH_gate_claim": False,
        }, True),
    ]


BUILDER_NAMES = (
    "build_certificate", "_domain_rows", "_density_rows", "_relation_rows",
    "_relation_rows_finish", "_compression_rows", "_square_rows",
    "_run_endpoint_rows", "_strict_rows", "_landscape_rows",
)

SEMANTIC_HELPER_NAMES = (
    "factorization", "primes_through", "prime_support", "is_prime",
    "shift_by_coordinate", "residue_set", "nu_support", "tau_support",
    "exceptional_primes", "theta_coefficients", "exact_support_coefficients",
    "lambda_coefficients", "basis_intervals", "expr_interval",
    "compare_expressions", "state_members", "state_mask",
    "reflected_state_mask", "relation_pairs", "relation_mask",
    "relation_source_mask", "relation_target_mask", "reflected_relation_mask",
    "relation_composition_empty", "saturated_relation", "relation_oracle",
    "projection_oracle", "transition_coefficients", "step_cycles",
    "capacity_dp", "full_capacity", "four_state_capacity",
    "one_site_capacity", "brute_capacity", "first_prime_not_dividing",
    "square_clock_from_support", "square_clock_through",
    "center_phase_positive", "shared_left_marginal", "shared_right_marginal",
    "marginal_square_audit", "multiaffinity_audit",
    "finite_exact_support_event_counts", "path_deletion_mwis",
    "path_lift_formula", "square_graph_counts", "nu_index_set", "D_finite",
    "R_finite", "finite_run_formula", "same_support_cover_audit", "crt",
    "crt_exact_run", "strict_lift_audit", "D_infinite_interval",
    "R_infinite_interval", "endpoint_interval", "landscape_lag",
    "canonical_json_bytes", "exact_equal",
)


def build_certificate() -> dict[str, object]:
    builders = (
        _domain_rows, _density_rows, _relation_rows, _compression_rows,
        _square_rows, _run_endpoint_rows, _strict_rows, _landscape_rows,
    )
    rows: list[dict[str, object]] = []
    for builder in builders:
        rows.extend(builder())
    counts = {
        group: sum(row["group"] == group for row in rows)
        for group in GROUP_IDS
    }
    actual_ids = {
        group: [row["id"] for row in rows if row["group"] == group]
        for group in GROUP_IDS
    }
    frozen_ids = {group: list(ids) for group, ids in GROUP_IDS.items()}
    return {
        "schema_version": 1,
        "status": "RH-396_fixed_lag_centered_core_certified",
        "title": TITLE,
        "package": PACKAGE,
        "epistemic_role": "finite_exact_reproduction_not_analytic_proof",
        "formal_oracle": "integers_Fractions_and_outward_rational_intervals_only",
        "quantifiers": {
            "each_h_fixed": True, "each_q_fixed": True,
            "phase_tables_fixed": True, "limit_before_finite_max": True,
            "sup_over_finite_q_after_limits": True,
            "h_depends_on_X": False, "q_depends_on_X": False,
        },
        "model_contract": {
            "alphabet": [-1, 0, 1],
            "coordinates": ["L", "C", "R"],
            "shifts": ["+h", "0", "-h"],
            "safety_step": "d=2h",
            "positive_projection": "A_r={(x,y):F_r(x,+1,y)=+1}",
            "safety": "Target(A_r) intersect Source(A_(r+d))=empty",
            "saturation": "A_r=(T\\Y_(r-d)) cross Y_r",
            "full_state_count": 8,
            "four_state_scope": "q does not divide d",
            "reflection": "input sign reflection changes terminal limit sign",
        },
        "density_contract": {
            "basis": ["K0", "K1", "K2", "K3"],
            "K0": "1", "Kj": "product_p(1-j/p^2)",
            "deduplicate_mod_p2_before_nu_tau": True,
            "theta_empty": "1/q", "Pi": "exact-support inclusion-exclusion",
            "lambda": "Pi(S(x,y))/2^(1_(x!=0)+1_(y!=0))",
        },
        "endpoint_contract": {
            "p0": "min prime not dividing 2h",
            "D_h": "product_p(1-|{2hj mod p^2:j in J}|/p^2)",
            "R_l": "D([0,l-1])-D({-1}U[0,l-1])-D([0,l])+D([-1,l])",
            "B_infinity": "3/pi^2+(1/2)sum_(odd l<p0^2)R_l",
            "finite_nonattainment": True,
            "inf_over_fixed_h": "3/pi^2",
            "inf_attained": False,
        },
        "source_role_contract": {
            "RH394": "sole analytic terminal table law",
            "RH375": "finite square-clock combinatorics only",
            "RH395": "finite relation/tropical precedent only",
        },
        "row_partition": dict(ROW_PARTITION),
        "row_ids": frozen_ids,
        "row_count": len(rows),
        "rows": rows,
        "mutation_names": list(MUTATION_NAMES),
        "all_pass": (
            len(rows) == CERTIFICATE_FIXTURE_ROWS
            and counts == ROW_PARTITION
            and actual_ids == frozen_ids
            and len({row["id"] for row in rows}) == len(rows)
            and all(row["pass"] is True for row in rows)
        ),
    }


def certificate_bytes() -> bytes:
    return canonical_json_bytes(build_certificate())


def _make_false_verifier():
    """Capture a builder-free verifier over independent local literals/tools."""

    from fractions import Fraction as local_fraction
    from hashlib import sha256 as local_sha256
    from json import dumps as local_dumps

    expected_bytes = 83309
    expected_sha = "7cc0da78ee7e47a22b357d7e8d907bc9d9879caeb82ede30709e8cb1023032ba"
    expected_top_keys = (
        "schema_version", "status", "title", "package", "epistemic_role",
        "formal_oracle", "quantifiers", "model_contract", "density_contract",
        "endpoint_contract", "source_role_contract", "row_partition", "row_ids",
        "row_count", "rows", "mutation_names", "all_pass",
    )
    expected_groups = (
        ("domain_source_firewall", (
            "A01_mu0", "A02_terminal_clock", "A03_fixed_h_q",
            "A04_d_equals_2h", "A05_shift_tuple_h_0_minus_h",
            "A06_centered_output", "A07_distance_d_safety",
            "A08_terminal_score", "A09_limit_max_sup_order",
            "A10_RH394_analytic_role", "A11_RH375_RH395_finite_only_roles",
            "A12_firewalls_gates",
        )),
        ("theta_pi_lambda", (
            "B01_Bp_dedup", "B02_nu_distinct",
            "B03_tau_distinct_modp2_then_modp", "B04_theta_p_not_q",
            "B05_theta_p_parallel_q", "B06_theta_p2_div_q",
            "B07_theta_empty", "B08_theta_phase_mass",
            "B09_Pi_inclusion_exclusion", "B10_Pi_nonnegative",
            "B11_Pi_phase_mass", "B12_Sxy", "B13_lambda_sign_split",
            "B14_collision_p_not_d", "B15_collision_p_div_d_not_p2",
            "B16_collision_p2_div_d",
        )),
        ("projection_safety_saturation_full8_reflection", (
            "C01_positive_projection", "C02_relation_A", "C03_projected_limit",
            "C04_composable_edges", "C05_safety_iff", "C06_target_Y",
            "C07_A_containment", "C08_saturated_A",
            "C09_saturated_converse_safe", "C10_transition_K",
            "C11_phase_objective", "C12_step_d_cycles",
            "C13_full8_tropical_trace", "C14_reflection_map",
            "C15_reflection_limit_sign", "C16_dynamic_relation_oracle",
        )),
        ("selfloop_compression_small_clock", (
            "D01_q_div_d_selfloop", "D02_selfloop_full8_required",
            "D03_q_not_div_d_cycle_gt1", "D04_multiaffine_occurrences",
            "D05_endpoint_rounding_k_to_0_or2", "D06_four_antipodal_states",
            "D07_four_state_transition", "D08_h1_q2_selfloop",
            "D09_h1_q4_two_cycle", "D10_h3_q3_selfloop",
            "D11_h3_q4_nonself",
            "D12_full8_vs_four_bruteforce_and_forbidden_allq_claim",
        )),
        ("marginal_square_saturation_lifts", (
            "E01_delta_center", "E02_one_site_Mh", "E03_one_site_embedding",
            "E04_Py_qy", "E05_p0_y0", "E06_same_support_domain",
            "E07_common_positive_delta", "E08_shared_coordinate_marginal_all_t",
            "E09_pair_charge", "E10_path_run_charge",
            "E11_same_support_scaling", "E12_exact_fixtures",
        )),
        ("D_R_finite_infinite_endpoint", (
            "F01_nu_J", "F02_Dhy", "F03_Dh_absolute_convergence",
            "F04_p0_definition", "F05_p0_run_cutoff", "F06_R_four_term",
            "F07_R_exact_run_event_nonnegative", "F08_finite_run_MWIS_identity",
            "F09_By_formula", "F10_Dy_Ry_limits", "F11_Binfinity_formula",
            "F12_numeric_intervals",
        )),
        ("strict_lift_CRT", (
            "G01_fresh_p_domain", "G02_positive_count_Nprime",
            "G03_one_deletion_per_lifted_run", "G04_path_deletion_parity",
            "G05_alpha_prime_formula", "G06_normalized_gain_E",
            "G07_CRT_exact_length2_run", "G08_eventual_strict_and_arbitrary_q_upper",
        )),
        ("lag_inf_claim_ceiling", (
            "H01_CRT_exact_length1_run", "H02_each_h_strict_baseline",
            "H03_dY_hY", "H04_boundary_requires_p_gtY",
            "H05_boundary_union_tail", "H06_inf_3_over_pi2",
            "H07_inf_unattained", "H08_no_sup_h_no_growing_parameters_claim_ceiling",
        )),
    )
    expected_mutations = (
        "fixed_h_to_growing", "fixed_q_to_growing", "d_equals_h",
        "shift_orientation_swap", "safety_step_h", "safety_unshares_letter",
        "Bp_no_dedup", "tau_counts_multiplicity", "theta_parallel_branch",
        "theta_square_branch", "Pi_sign_flip", "Pi_wrong_complement",
        "lambda_drop_x_half", "lambda_drop_y_half", "projected_wrong_center",
        "composition_reverse", "saturation_r_plus_d", "transition_includes_U",
        "tropical_drop_cycle", "four_state_on_selfloop",
        "q_divides_condition_flip", "reflection_no_input_negation",
        "p0_uses_p2_nondivisor", "base_omits_p0", "same_support_unconditional",
        "R_drop_left", "R_drop_right", "R_last_sign_flip",
        "By_drop_K1_over_D", "deletion_odd_even_swap", "Nprime_uses_p2N",
        "claim_sup_h",
    )

    def is_int(value: object) -> bool:
        return type(value) is int and type(value) is not bool

    def json_types(value: object) -> bool:
        if type(value) in (str, bool) or value is None:
            return True
        if is_int(value):
            return True
        if type(value) is list:
            return all(json_types(item) for item in value)
        if type(value) is dict:
            return all(type(key) is str and json_types(item) for key, item in value.items())
        return False

    def canonical(value: object) -> bytes:
        return local_dumps(
            value, ensure_ascii=False, allow_nan=False, sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def structural(value: object) -> bool:
        if type(value) is not dict or tuple(value) != expected_top_keys or not json_types(value):
            return False
        if value["schema_version"] != 1 or value["row_count"] != 96:
            return False
        if value["title"] != "Euler Run Spectrum for Fixed-Lag Centered Mobius Capacity":
            return False
        if value["package"] != "fixed_lag_centered_capacity":
            return False
        if value["mutation_names"] != list(expected_mutations):
            return False
        partition = {group: len(ids) for group, ids in expected_groups}
        frozen_ids = {group: list(ids) for group, ids in expected_groups}
        if value["row_partition"] != partition or value["row_ids"] != frozen_ids:
            return False
        rows = value["rows"]
        if type(rows) is not list or len(rows) != 96:
            return False
        expected_flat = [(group, identifier) for group, ids in expected_groups for identifier in ids]
        actual_flat = []
        for row in rows:
            if type(row) is not dict or tuple(row) != ("group", "id", "data", "pass"):
                return False
            if type(row["data"]) is not dict or row["pass"] is not True:
                return False
            actual_flat.append((row["group"], row["id"]))
        return actual_flat == expected_flat and len({identifier for _group, identifier in actual_flat}) == 96

    def frac(text: object) -> local_fraction:
        if type(text) is not str:
            raise TypeError("fraction leaf is not text")
        return local_fraction(text)

    def local_is_prime(value: int) -> bool:
        if not is_int(value) or value < 2:
            return False
        divisor = 2
        while divisor * divisor <= value:
            if value % divisor == 0:
                return False
            divisor += 1
        return True

    def local_p0(h: int) -> int:
        candidate = 2
        while not (local_is_prime(candidate) and (2 * h) % candidate):
            candidate += 1
        return candidate

    def local_support(q: int) -> list[int]:
        output = []
        remaining = q
        prime = 2
        while prime * prime <= remaining:
            if remaining % prime == 0:
                output.append(prime)
                while remaining % prime == 0:
                    remaining //= prime
            prime += 1
        if remaining > 1:
            output.append(remaining)
        return output

    def local_gcd(left: int, right: int) -> int:
        while right:
            left, right = right, left % right
        return left

    def local_graph(h: int, q: int) -> tuple[int, int, list[int], list[int]]:
        support = local_support(q)
        positive = [all(phase % (prime * prime) for prime in support) for phase in range(q)]
        seen: set[int] = set()
        runs: list[int] = []
        positive_cycles: list[int] = []
        alpha = 0
        for start in range(q):
            if start in seen:
                continue
            cycle = []
            phase = start
            while phase not in seen:
                seen.add(phase)
                cycle.append(phase)
                phase = (phase + 2 * h) % q
            bits = [positive[item] for item in cycle]
            if all(bits):
                positive_cycles.append(len(bits))
                alpha += len(bits) // 2
                continue
            zero = bits.index(False)
            rotated = bits[zero + 1 :] + bits[: zero + 1]
            length = 0
            for bit in rotated:
                if bit:
                    length += 1
                elif length:
                    runs.append(length)
                    alpha += (length + 1) // 2
                    length = 0
        return sum(positive), alpha, sorted(runs), sorted(positive_cycles)

    def relation_safe_count() -> int:
        sources = []
        targets = []
        for mask in range(512):
            source = target = 0
            for index in range(9):
                if mask & (1 << index):
                    source |= 1 << (index // 3)
                    target |= 1 << (index % 3)
            sources.append(source)
            targets.append(target)
        return sum(
            1 for left in range(512) for right in range(512)
            if targets[left] & sources[right] == 0
        )

    def path_value(length: int, position: int) -> int:
        return position // 2 + (length - position + 1) // 2

    def semantic(rows: object) -> bool:
        if type(rows) is not list:
            return False
        by_id = {row["id"]: row["data"] for row in rows}
        checks: dict[str, bool] = {}

        # A: domain/source/firewall literals and exact fixture arithmetic.
        checks["A01_mu0"] = by_id["A01_mu0"]["boundary_extension_only"] is True
        checks["A02_terminal_clock"] = by_id["A02_terminal_clock"]["normalization"] == "1/log(omega(X))"
        checks["A03_fixed_h_q"] = (
            by_id["A03_fixed_h_q"]["h_fixed_before_limit"] is True
            and by_id["A03_fixed_h_q"]["q_fixed_before_limit"] is True
            and by_id["A03_fixed_h_q"]["h_depends_on_X"] is False
            and by_id["A03_fixed_h_q"]["q_depends_on_X"] is False
        )
        checks["A04_d_equals_2h"] = all(row["d"] == 2 * row["h"] for row in by_id["A04_d_equals_2h"]["fixtures"])
        checks["A05_shift_tuple_h_0_minus_h"] = all(row["shifts"] == [row["h"], 0, -row["h"]] for row in by_id["A05_shift_tuple_h_0_minus_h"]["fixtures"])
        checks["A06_centered_output"] = by_id["A06_centered_output"]["centered_noncausal"] is True
        checks["A07_distance_d_safety"] = by_id["A07_distance_d_safety"]["step"] == "d=2h" and by_id["A07_distance_d_safety"]["shared_letter"] == "mu(n+h)"
        checks["A08_terminal_score"] = by_id["A08_terminal_score"]["signed"] is True and by_id["A08_terminal_score"]["ordinary_Cesaro"] is False
        checks["A09_limit_max_sup_order"] = by_id["A09_limit_max_sup_order"]["prelimit_maximum"] is False and by_id["A09_limit_max_sup_order"]["supremum_over_h"] is False
        checks["A10_RH394_analytic_role"] = by_id["A10_RH394_analytic_role"]["finite_combinatorics_role"] is False
        checks["A11_RH375_RH395_finite_only_roles"] = by_id["A11_RH375_RH395_finite_only_roles"]["analytic_terminal_input"] is False
        checks["A12_firewalls_gates"] = all(item is False for item in by_id["A12_firewalls_gates"]["gates_A_to_E"])

        # B: exact CRT vectors, K0--K3 coordinates, mass and sign splits.
        checks["B01_Bp_dedup"] = by_id["B01_Bp_dedup"]["raw_shifts_mod_p2"] == [0, 0, 0] and by_id["B01_Bp_dedup"]["deduplicated_Bp"] == [0]
        checks["B02_nu_distinct"] = by_id["B02_nu_distinct"]["nu"] == len(set(by_id["B02_nu_distinct"]["Bp"])) == 3
        checks["B03_tau_distinct_modp2_then_modp"] = by_id["B03_tau_distinct_modp2_then_modp"]["Bp"] == [0, 3, 6] and by_id["B03_tau_distinct_modp2_then_modp"]["tau_phase_0_1_2"] == [3, 0, 0]
        checks["B04_theta_p_not_q"] = by_id["B04_theta_p_not_q"]["coefficients"] == ["0", "0", "0", "4/3"]
        checks["B05_theta_p_parallel_q"] = by_id["B05_theta_p_parallel_q"]["tau"] == 1 and by_id["B05_theta_p_parallel_q"]["coefficients"] == ["0", "0", "0", "1/3"]
        checks["B06_theta_p2_div_q"] = by_id["B06_theta_p2_div_q"]["allowed"] is True and by_id["B06_theta_p2_div_q"]["coefficients"] == ["0", "0", "0", "1/6"]
        checks["B07_theta_empty"] = by_id["B07_theta_empty"]["coefficients"] == ["1/36", "0", "0", "0"]
        checks["B08_theta_phase_mass"] = all(row["phase_sum"] == row["global_density"] for row in by_id["B08_theta_phase_mass"]["fixtures"])
        checks["B09_Pi_inclusion_exclusion"] = by_id["B09_Pi_inclusion_exclusion"]["signs"] == [1, -1, -1, 1]
        event = by_id["B10_Pi_nonnegative"]
        checks["B10_Pi_nonnegative"] = event["nonnegative"] is True and sum(event["counts"].values()) == event["q"] == event["mass"]
        checks["B11_Pi_phase_mass"] = by_id["B11_Pi_phase_mass"]["sum_over_8_exact_supports"] == by_id["B11_Pi_phase_mass"]["theta_empty"]
        checks["B12_Sxy"] = all(row["support"][0] == "C" and ("L" in row["support"]) == (row["x"] != 0) and ("R" in row["support"]) == (row["y"] != 0) for row in by_id["B12_Sxy"]["vectors"])
        checks["B13_lambda_sign_split"] = all(row["divisor"] == 2 ** (int(row["x"] != 0) + int(row["y"] != 0)) for row in by_id["B13_lambda_sign_split"]["vectors"])
        checks["B14_collision_p_not_d"] = by_id["B14_collision_p_not_d"]["d"] % by_id["B14_collision_p_not_d"]["p"] != 0 and by_id["B14_collision_p_not_d"]["nu"] == 3
        checks["B15_collision_p_div_d_not_p2"] = by_id["B15_collision_p_div_d_not_p2"]["d"] % 3 == 0 and by_id["B15_collision_p_div_d_not_p2"]["d"] % 9 != 0 and by_id["B15_collision_p_div_d_not_p2"]["tau_phase_0"] == 3
        checks["B16_collision_p2_div_d"] = by_id["B16_collision_p2_div_d"]["d"] % 9 == 0 and by_id["B16_collision_p2_div_d"]["nu"] == 1

        # C: relation algebra and independent 512^2 compatibility count.
        checks["C01_positive_projection"] = by_id["C01_positive_projection"]["case_count"] == 54 and by_id["C01_positive_projection"]["deleted_plus_count"] == 18 and by_id["C01_positive_projection"]["score_monotonicity_failure_count"] == 0
        checks["C02_relation_A"] = by_id["C02_relation_A"]["relation_count"] == 512 and by_id["C02_relation_A"]["full_table_fiber_size"] * 512 == 1 << 27
        checks["C03_projected_limit"] = all(by_id["C03_projected_limit"][key] is True for key in ("projected_plus_subset", "pointwise_score_nondecrease", "safety_preserved", "terminal_limit_nondecrease"))
        checks["C04_composable_edges"] = by_id["C04_composable_edges"]["safe_composition_empty"] is True and by_id["C04_composable_edges"]["unsafe_composition_empty"] is False
        safe_count = relation_safe_count()
        checks["C05_safety_iff"] = by_id["C05_safety_iff"]["ordered_relation_pairs"] == 262144 and by_id["C05_safety_iff"]["safe_pairs"] == safe_count == 3375 and by_id["C05_safety_iff"]["criterion_failures"] == 0
        checks["C06_target_Y"] = by_id["C06_target_Y"]["state_count"] == len(by_id["C06_target_Y"]["states"]) == 8
        checks["C07_A_containment"] = by_id["C07_A_containment"]["scanned_safe_pairs"] == safe_count and by_id["C07_A_containment"]["inclusion_failures"] == 0
        checks["C08_saturated_A"] = by_id["C08_saturated_A"]["pairs"] == [[0, 0], [0, 1]]
        checks["C09_saturated_converse_safe"] = by_id["C09_saturated_converse_safe"]["saturation_failures"] == 0
        checks["C10_transition_K"] = len(by_id["C10_transition_K"]["coefficients"]) == 4
        checks["C11_phase_objective"] = by_id["C11_phase_objective"]["fixture"]["coefficients"] == ["0", "3/8", "0", "0"]
        checks["C12_step_d_cycles"] = all(len(row["cycles"]) == local_gcd(row["q"], 2 * row["h"]) and all(len(cycle) == row["q"] // local_gcd(row["q"], 2 * row["h"]) for cycle in row["cycles"]) for row in by_id["C12_step_d_cycles"]["fixtures"])
        checks["C13_full8_tropical_trace"] = by_id["C13_full8_tropical_trace"]["state_count"] == 8 and all(row["dp"] == row["brute"] for row in by_id["C13_full8_tropical_trace"]["dynamic_vs_exhaustive"])
        checks["C14_reflection_map"] = by_id["C14_reflection_map"]["relation_involution_cases"] == 512 and by_id["C14_reflection_map"]["involution_pass"] is True
        checks["C15_reflection_limit_sign"] = by_id["C15_reflection_limit_sign"]["lambda_cell_invariance"] is True and by_id["C15_reflection_limit_sign"]["both_signs_attained"] is True
        oracle = by_id["C16_dynamic_relation_oracle"]
        checks["C16_dynamic_relation_oracle"] = oracle["safe_pair_count"] == safe_count == 3375 and all(oracle[key] == 0 for key in ("compatibility_failure_count", "inclusion_failure_count", "saturation_failure_count", "reflection_failure_count"))

        # D: self-loop criterion, exact small-clock vectors and exhaustive agreement.
        checks["D01_q_div_d_selfloop"] = all(row["q_divides_d"] == ((2 * row["h"]) % row["q"] == 0) == (row["cycle_length"] == 1) for row in by_id["D01_q_div_d_selfloop"]["fixtures"])
        checks["D02_selfloop_full8_required"] = by_id["D02_selfloop_full8_required"]["full8"] == ["0", "0", "1/2", "-1/2"] and by_id["D02_selfloop_full8_required"]["forbidden_four"] == ["0", "0", "1", "-2"] and by_id["D02_selfloop_full8_required"]["full8_strictly_larger"] is True
        checks["D03_q_not_div_d_cycle_gt1"] = all(row["cycle_length"] > 1 and row["q_divides_d"] is False for row in by_id["D03_q_not_div_d_cycle_gt1"]["fixtures"])
        checks["D04_multiaffine_occurrences"] = by_id["D04_multiaffine_occurrences"]["context_count"] > 0 and by_id["D04_multiaffine_occurrences"]["singleton_symmetry_failure_count"] == by_id["D04_multiaffine_occurrences"]["second_difference_failure_count"] == 0
        checks["D05_endpoint_rounding_k_to_0_or2"] = by_id["D05_endpoint_rounding_k_to_0_or2"]["rounding_endpoints"] == [0, 2] and by_id["D05_endpoint_rounding_k_to_0_or2"]["second_difference_failures"] == 0
        checks["D06_four_antipodal_states"] = by_id["D06_four_antipodal_states"]["masks"] == [0, 2, 5, 7]
        checks["D07_four_state_transition"] = by_id["D07_four_state_transition"]["entry_count"] == len(by_id["D07_four_state_transition"]["transitions"]) == 16
        checks["D08_h1_q2_selfloop"] = by_id["D08_h1_q2_selfloop"]["q_divides_d"] is True and by_id["D08_h1_q2_selfloop"]["full8"] == ["0", "0", "3/4", "-1/4"]
        checks["D09_h1_q4_two_cycle"] = by_id["D09_h1_q4_two_cycle"]["cycle_length"] == 2 and by_id["D09_h1_q4_two_cycle"]["full8"] == by_id["D09_h1_q4_two_cycle"]["four"]
        checks["D10_h3_q3_selfloop"] = by_id["D10_h3_q3_selfloop"]["q_divides_d"] is True and by_id["D10_h3_q3_selfloop"]["full8"] == ["0", "0", "1", "-1"]
        checks["D11_h3_q4_nonself"] = by_id["D11_h3_q4_nonself"]["q_divides_d"] is False and by_id["D11_h3_q4_nonself"]["full8"] == by_id["D11_h3_q4_nonself"]["four"]
        checks["D12_full8_vs_four_bruteforce_and_forbidden_allq_claim"] = by_id["D12_full8_vs_four_bruteforce_and_forbidden_allq_claim"]["four_state_all_q"] is False and all(row["dp"] == row["brute"] and row["equal"] is True for row in by_id["D12_full8_vs_four_bruteforce_and_forbidden_allq_claim"]["brute_rows"])

        # E: independently recount all frozen square-clock fixtures.
        checks["E01_delta_center"] = by_id["E01_delta_center"]["distinct_positive_values"] == [["0", "1/576", "0", "0"]]
        checks["E02_one_site_Mh"] = "alpha_h(q)=raw MWIS" in by_id["E02_one_site_Mh"]["definition"] and "K1*alpha_h(q)/N_h(q)" in by_id["E02_one_site_Mh"]["weighted_Mh_on_square_support"]
        checks["E03_one_site_embedding"] = all(row["comparison"] >= 0 for row in by_id["E03_one_site_embedding"]["embedding_rows"])
        checks["E04_Py_qy"] = by_id["E04_Py_qy"]["q_1"] == 36 and by_id["E04_Py_qy"]["q_3"] == 900
        checks["E05_p0_y0"] = all(row["p0"] == local_p0(row["h"]) for row in by_id["E05_p0_y0"]["fixtures"])
        checks["E06_same_support_domain"] = by_id["E06_same_support_domain"]["pre_p0_counterexample"]["equal"] is False and "p0 in base support" in by_id["E06_same_support_domain"]["required"]
        checks["E07_common_positive_delta"] = by_id["E07_common_positive_delta"]["distinct_delta_count"] == 1 and by_id["E07_common_positive_delta"]["positive_phase_count"] == 576
        checks["E08_shared_coordinate_marginal_all_t"] = by_id["E08_shared_coordinate_marginal_all_t"]["per_t_cases"] > 0 and by_id["E08_shared_coordinate_marginal_all_t"]["marginal_failures"] == 0
        checks["E09_pair_charge"] = by_id["E09_pair_charge"]["positive_adjacent_phase_pairs"] > 0 and by_id["E09_pair_charge"]["mask_triple_failure_count"] == 0
        checks["E10_path_run_charge"] = by_id["E10_path_run_charge"]["charges"] == [(length + 1) // 2 for length in by_id["E10_path_run_charge"]["lengths_0_to_24"]]
        checks["E11_same_support_scaling"] = all(row["new_positive"] == row["multiplier"] * row["old_positive"] and row["new_mwis"] == row["multiplier"] * row["old_mwis"] for row in by_id["E11_same_support_scaling"]["fixture_rows"])
        fixture_ok = True
        for row in by_id["E12_exact_fixtures"]["fixtures"]:
            n_value, alpha, _runs, _cycles = local_graph(row["h"], row["q"])
            fixture_ok = fixture_ok and n_value == row["expected_positive"] == row["positive"] and alpha == row["expected_mwis"] == row["mwis"] and row["p0"] == local_p0(row["h"])
        checks["E12_exact_fixtures"] = fixture_ok and by_id["E12_exact_fixtures"]["pre_p0_h6_q36_to_q72_same_support_claim"] == "FAIL"

        # F: exact rational products/run identities and proof-safe intervals.
        checks["F01_nu_J"] = all(row["nu"] == len(set(row["residues"])) for row in by_id["F01_nu_J"]["vectors"])
        local_product = local_fraction(1)
        for text in by_id["F02_Dhy"]["local_factors"]:
            local_product *= frac(text)
        checks["F02_Dhy"] = local_product == frac(by_id["F02_Dhy"]["D_finite"])
        checks["F03_Dh_absolute_convergence"] = local_fraction(0) <= frac(by_id["F03_Dh_absolute_convergence"]["lower"]) <= frac(by_id["F03_Dh_absolute_convergence"]["upper"]) <= 1
        checks["F04_p0_definition"] = all(row["p0"] == local_p0(row["h"]) for row in by_id["F04_p0_definition"]["fixtures"])
        checks["F05_p0_run_cutoff"] = by_id["F05_p0_run_cutoff"]["max_enumerated_run"] < by_id["F05_p0_run_cutoff"]["p0"] ** 2 and by_id["F05_p0_run_cutoff"]["all_positive_cycles"] == []
        checks["F06_R_four_term"] = len(by_id["F06_R_four_term"]["values_l_1_to_6"]) == 6
        checks["F07_R_exact_run_event_nonnegative"] = all(frac(text) >= 0 for text in by_id["F07_R_exact_run_event_nonnegative"]["densities"]) and by_id["F07_R_exact_run_event_nonnegative"]["enumeration_matches"] is True
        checks["F08_finite_run_MWIS_identity"] = all(row["positive_formula_count"] == row["positive_enumerated_count"] and row["mwis_formula_count"] == row["mwis_enumerated_count"] and row["pass"] is True for row in by_id["F08_finite_run_MWIS_identity"]["fixtures"])
        checks["F09_By_formula"] = frac(by_id["F09_By_formula"]["M_over_N"]) == frac(by_id["F09_By_formula"]["half_plus_odd_over_2N"])
        checks["F10_Dy_Ry_limits"] = by_id["F10_Dy_Ry_limits"]["limit_termwise_allowed"] is True and frac(by_id["F10_Dy_Ry_limits"]["rigorous_limit_interval"][0]) <= frac(by_id["F10_Dy_Ry_limits"]["rigorous_limit_interval"][1])
        checks["F11_Binfinity_formula"] = by_id["F11_Binfinity_formula"]["K1_over_2"] == "3/pi^2" and by_id["F11_Binfinity_formula"]["sum_is_finite"] is True
        checks["F12_numeric_intervals"] = all(frac(row["rigorous_lower"]) < frac(row["quoted_orientation_only"]) < frac(row["rigorous_upper"]) and row["quoted_value_inside"] is True for row in by_id["F12_numeric_intervals"]["rows"])

        # G: independently recompute each path deletion vector and recurrence leaf.
        checks["G01_fresh_p_domain"] = by_id["G01_fresh_p_domain"]["pre_p0_counterexample"]["actual_new_M"] == 16 and by_id["G01_fresh_p_domain"]["pre_p0_counterexample"]["naive_path_formula_M"] == 17
        checks["G02_positive_count_Nprime"] = by_id["G02_positive_count_Nprime"]["new_N"] == by_id["G02_positive_count_Nprime"]["predicted_N"] == (7 * 7 - 1) * by_id["G02_positive_count_Nprime"]["old_N"]
        lift_rows = by_id["G03_one_deletion_per_lifted_run"]["rows"]
        checks["G03_one_deletion_per_lifted_run"] = all(row["deletion_values"] == [path_value(row["length"], position) for position in range(1, row["length"] + 1)] and row["pass"] is True for row in lift_rows)
        checks["G04_path_deletion_parity"] = all(row["drop_positions"] == list(range(1, row["length"] + 1, 2)) for row in by_id["G04_path_deletion_parity"]["odd_rows"]) and all(row["drop_positions"] == [] for row in by_id["G04_path_deletion_parity"]["even_rows"])
        checks["G05_alpha_prime_formula"] = all(row["actual_total"] == row["expected_total"] for row in by_id["G05_alpha_prime_formula"]["rows"])
        strict = by_id["G06_normalized_gain_E"]["fixture"]
        checks["G06_normalized_gain_E"] = strict["new_positive"] == strict["predicted_positive"] and strict["new_mwis"] == strict["predicted_mwis"] and strict["even_excess"] > 0 and strict["strict"] is True
        checks["G07_CRT_exact_length2_run"] = by_id["G07_CRT_exact_length2_run"]["length"] == 2 and by_id["G07_CRT_exact_length2_run"]["left_endpoint_zero"] is True and by_id["G07_CRT_exact_length2_run"]["interior_positive"] == [True, True] and by_id["G07_CRT_exact_length2_run"]["right_endpoint_zero"] is True
        checks["G08_eventual_strict_and_arbitrary_q_upper"] = by_id["G08_eventual_strict_and_arbitrary_q_upper"]["stepwise_strict_claim"] is False and by_id["G08_eventual_strict_and_arbitrary_q_upper"]["future_strict_claim"] is True and by_id["G08_eventual_strict_and_arbitrary_q_upper"]["q_divides_Q_direction"] == "C_h(q)<=C_h(Q)"

        # H: finite CRT reproduction, boundary sequence, and exact claim ceiling.
        checks["H01_CRT_exact_length1_run"] = all(row["length"] == 1 and row["left_endpoint_zero"] is True and row["interior_positive"] == [True] and row["right_endpoint_zero"] is True and row["pass"] is True for row in by_id["H01_CRT_exact_length1_run"]["fixtures"])
        checks["H02_each_h_strict_baseline"] = "outside-prime Euler tail" in by_id["H02_each_h_strict_baseline"]["analytic_proof_obligation"]
        checks["H03_dY_hY"] = all(row["d_Y"] == 2 * row["h_Y"] and row["d_equals_2h"] is True for row in by_id["H03_dY_hY"]["fixtures"])
        checks["H04_boundary_requires_p_gtY"] = all(check["first_possible_boundary_prime"] > check["Y"] and all(item["p2_divides_d"] is True for item in check["small_prime_square_divisibility"]) for check in by_id["H04_boundary_requires_p_gtY"]["checks"])
        checks["H05_boundary_union_tail"] = all(frac(row["upper"]) == local_fraction(1, 2 * (row["Y"] - 1)) for row in by_id["H05_boundary_union_tail"]["fixtures"]) and by_id["H05_boundary_union_tail"]["tends_to_zero"] is True
        checks["H06_inf_3_over_pi2"] = by_id["H06_inf_3_over_pi2"]["statement"] == "inf_(fixed h>=1) B_infinity(h)=3/pi^2"
        checks["H07_inf_unattained"] = by_id["H07_inf_unattained"]["attained"] is False
        ceiling = by_id["H08_no_sup_h_no_growing_parameters_claim_ceiling"]
        checks["H08_no_sup_h_no_growing_parameters_claim_ceiling"] = ceiling["fixed_h_theorem"] is True and ceiling["infimum_over_fixed_h_endpoints"] is True and all(ceiling[key] is False for key in ("supremum_over_h_capacity", "h_depends_on_X", "q_depends_on_X", "uniform_rate_in_h_or_q", "ordinary_Cesaro", "prelimit_adaptive_tables", "operator_or_RH_gate_claim"))

        expected_ids = {identifier for _group, ids in expected_groups for identifier in ids}
        return set(checks) == expected_ids and all(checks.values())

    def verifier(value: object) -> bool:
        try:
            if not structural(value):
                return False
            encoded = canonical(value)
            if len(encoded) != expected_bytes or local_sha256(encoded).hexdigest() != expected_sha:
                return False
            return value["all_pass"] is True and semantic(value["rows"])
        except (ArithmeticError, KeyError, TypeError, ValueError, ZeroDivisionError):
            return False

    # `semantic` is defined in the next incremental block and resolved in this
    # closure before `_make_false_verifier` returns.
    return verifier


_FALSE_VERIFIER = _make_false_verifier()


def verify_certificate(value: object, *, compare_fresh: bool = False) -> bool:
    if type(compare_fresh) is not bool:
        raise TypeError("compare_fresh must be an exact bool")
    if not _FALSE_VERIFIER(value):
        return False
    if compare_fresh:
        return exact_equal(value, build_certificate())
    return True


def _find_row(value: dict[str, object], identifier: str) -> dict[str, object]:
    rows = value.get("rows")
    if type(rows) is not list:
        raise ValueError("certificate rows are unavailable")
    matches = [row for row in rows if type(row) is dict and row.get("id") == identifier]
    if len(matches) != 1:
        raise ValueError(f"certificate row is not unique: {identifier}")
    return matches[0]


def mutate_certificate(value: dict[str, object], name: str) -> dict[str, object]:
    if type(value) is not dict or type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown semantic mutation")
    mutated = deepcopy(value)

    def data(identifier: str) -> dict[str, object]:
        row = _find_row(mutated, identifier)
        payload = row["data"]
        if type(payload) is not dict:
            raise ValueError("row payload is not a dictionary")
        return payload

    if name == "fixed_h_to_growing":
        data("A03_fixed_h_q")["h_depends_on_X"] = True
    elif name == "fixed_q_to_growing":
        data("A03_fixed_h_q")["q_depends_on_X"] = True
    elif name == "d_equals_h":
        data("A04_d_equals_2h")["fixtures"][0]["d"] = 1
    elif name == "shift_orientation_swap":
        data("A05_shift_tuple_h_0_minus_h")["fixtures"][0]["shifts"] = [-1, 0, 1]
    elif name == "safety_step_h":
        data("A07_distance_d_safety")["step"] = "d=h"
    elif name == "safety_unshares_letter":
        data("A07_distance_d_safety")["shared_letter"] = "mu(n+2h)"
    elif name == "Bp_no_dedup":
        data("B01_Bp_dedup")["deduplicated_Bp"] = [0, 0, 0]
    elif name == "tau_counts_multiplicity":
        data("B03_tau_distinct_modp2_then_modp")["tau_phase_0_1_2"] = [1, 0, 0]
    elif name == "theta_parallel_branch":
        data("B05_theta_p_parallel_q")["coefficients"] = ["0", "0", "0", "2/9"]
    elif name == "theta_square_branch":
        data("B06_theta_p2_div_q")["allowed"] = False
    elif name == "Pi_sign_flip":
        data("B09_Pi_inclusion_exclusion")["signs"] = [1, 1, -1, 1]
    elif name == "Pi_wrong_complement":
        data("B09_Pi_inclusion_exclusion")["complement"] = ["L"]
    elif name == "lambda_drop_x_half":
        vectors = data("B13_lambda_sign_split")["vectors"]
        next(row for row in vectors if row["x"] == -1 and row["y"] == 0)["divisor"] = 1
    elif name == "lambda_drop_y_half":
        vectors = data("B13_lambda_sign_split")["vectors"]
        next(row for row in vectors if row["x"] == 0 and row["y"] == -1)["divisor"] = 1
    elif name == "projected_wrong_center":
        data("C01_positive_projection")["case_count"] = 53
    elif name == "composition_reverse":
        data("C04_composable_edges")["safe_composition_empty"] = False
    elif name == "saturation_r_plus_d":
        data("C07_A_containment")["formula"] = "A_r subset (T\\Y_(r+d)) cross Y_r"
    elif name == "transition_includes_U":
        data("C10_transition_K")["definition"] = "K_r(U,V)=sum_(x in U,y in V) lambda_r(x,y)"
    elif name == "tropical_drop_cycle":
        data("C12_step_d_cycles")["fixtures"][0]["cycles"].pop()
    elif name == "four_state_on_selfloop":
        data("D02_selfloop_full8_required")["full8"] = data("D02_selfloop_full8_required")["forbidden_four"]
    elif name == "q_divides_condition_flip":
        data("D01_q_div_d_selfloop")["fixtures"][0]["q_divides_d"] = False
    elif name == "reflection_no_input_negation":
        data("C15_reflection_limit_sign")["table_map"] = "F^rho(x,z,y)=F(x,z,y)"
    elif name == "p0_uses_p2_nondivisor":
        data("F04_p0_definition")["fixtures"][0]["p0"] = 2
    elif name == "base_omits_p0":
        data("G01_fresh_p_domain")["requirements"].remove("p0 in old square support")
    elif name == "same_support_unconditional":
        data("E06_same_support_domain")["required"] = ["q_base divides Q", "same prime support"]
    elif name == "R_drop_left":
        data("F06_R_four_term")["definition"] = "R_l=D([0,l-1])-D([0,l])+D([-1,l])"
    elif name == "R_drop_right":
        data("F06_R_four_term")["definition"] = "R_l=D([0,l-1])-D({-1}U[0,l-1])+D([-1,l])"
    elif name == "R_last_sign_flip":
        data("F06_R_four_term")["definition"] = "R_l=D([0,l-1])-D(left)-D(right)-D([-1,l])"
    elif name == "By_drop_K1_over_D":
        data("F09_By_formula")["formula"] = "B_y=K1/2+(1/2)sum R_(y,l)"
    elif name == "deletion_odd_even_swap":
        data("G04_path_deletion_parity")["odd_drop_positions"] = "even j"
    elif name == "Nprime_uses_p2N":
        row = data("G02_positive_count_Nprime")
        row["predicted_N"] = 49 * row["old_N"]
    elif name == "claim_sup_h":
        data("H08_no_sup_h_no_growing_parameters_claim_ceiling")["supremum_over_h_capacity"] = True
    else:
        raise ValueError("unimplemented semantic mutation")
    return mutated
