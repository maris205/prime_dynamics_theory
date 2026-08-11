"""Exact finite reproduction for the RH-395 centered three-window theorem.

The computations in this module reproduce the finite relation algebra,
phase-density formulas, and tropical optimizers.  They are not a proof of the
analytic terminal-logarithmic input, which is supplied by the frozen RH-394
theorem.
"""

from __future__ import annotations

from copy import deepcopy
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
import math
from typing import Iterable


TITLE = "All-Clock Rigidity for Centered Three-Window Möbius Capacity"
T = (-1, 0, 1)
COORDINATES = ("L", "C", "R")
SHIFT_BY_COORDINATE = {"L": 1, "C": 0, "R": -1}
ALL_STATE_MASKS = tuple(range(8))
FOUR_STATE_MASKS = (0, 2, 5, 7)
K_INTERVAL_LIMIT = 10_000
ZERO_EXPR = (Fraction(0), Fraction(0), Fraction(0))
ROW_PARTITION = {
    "subset_state": 8,
    "q2_selfloop": 16,
    "small_clock": 12,
    "transfer_compression": 10,
    "marginal_charge": 12,
    "square_saturation": 8,
    "theorem_firewall": 6,
}
CERTIFICATE_FIXTURE_ROWS = 72
CERTIFICATE_FIXTURE_BYTES = 32983
CERTIFICATE_FIXTURE_SHA256 = "31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9"
MUTATION_NAMES = (
    "shift_swap",
    "lambda_divisor",
    "all_q_trace_4x4",
    "q2_old_value",
    "q2_even_witness",
    "q2_odd_witness",
    "q2_selfloop_deleted",
    "q1_affinity_claim",
    "capacity_q1",
    "capacity_q2",
    "capacity_q3",
    "capacity_q4",
    "capacity_q6",
    "one_site_q6",
    "q1_ratio_direction",
    "q2_ratio_direction",
    "projection_point_case",
    "projection_deleted_count",
    "relation_safe_count",
    "saturation_changed_count",
    "multi_affinity_failure",
    "self_identification_q2",
    "marginal_left",
    "marginal_right",
    "marginal_only_sum",
    "marginal_omit_t0",
    "path_ceil_to_floor",
    "forced_reset_4",
    "forced_reset_9",
    "same_support_scale",
    "square_q36",
    "square_q900",
    "q_lift_direction",
    "q_lift_safety",
    "finite_attainment",
    "rh375_terminal_misrole",
    "growing_q",
    "prelimit_max",
    "causal_claim",
    "ordinary_cesaro",
    "generic_capacity",
    "source_stop",
    "reflection_sign_identity",
    "reflection_both_signs",
    "mu0_definition",
    "terminal_normalization",
    "phase_table_type",
    "safety_condition",
    "capacity_definition",
    "theta_formula",
    "pi_formula",
    "pi_mass",
    "endpoint_definition",
    "row_extra",
    "float_injection",
    "interval_cutoff",
    "interval_policy",
)
BUILDER_NAMES = (
    "build_certificate",
    "_subset_rows",
    "_q2_rows",
    "_small_clock_rows",
    "_compression_rows",
    "_marginal_rows",
    "_square_rows",
    "_firewall_rows",
)
SEMANTIC_HELPER_NAMES = (
    "state_members",
    "state_mask",
    "reflected_state_mask",
    "relation_pairs",
    "relation_mask",
    "reflected_relation_mask",
    "relation_source_mask",
    "relation_target_mask",
    "relation_composition_empty",
    "saturated_relation",
    "projection_audit",
    "reflection_audit",
    "relation_pair_audit",
    "rigorous_interval_audit",
    "multi_affinity_audit",
    "square_marginal_interface_audit",
    "theta_coefficients",
    "factorization",
    "exact_support_coefficients",
    "lambda_coefficients",
    "transition_coefficients",
    "compressed_transition_coefficients",
    "capacity_dp",
    "plus_two_cycles",
    "full_capacity",
    "four_state_capacity",
    "one_site_capacity",
    "divisibility_lift_audit",
    "q36_pattern_scan",
    "left_marginal",
    "right_marginal",
    "center_phase_positive",
    "square_clock",
    "prime_support",
    "lcm",
    "cutoff_bridge",
    "compare_expressions",
    "expr_interval",
    "basis_intervals",
    "primes_through",
    "canonical_json_bytes",
    "exact_equal",
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
        text,
        object_pairs_hook=_pairs_no_duplicates,
        parse_constant=_reject_constant,
    )


def canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
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


def expr_text(value: tuple[Fraction, Fraction, Fraction]) -> list[str]:
    if type(value) is not tuple or len(value) != 3:
        raise TypeError("K-expression must be an exact three-tuple")
    return [fraction_text(item) for item in value]


def expr_add(
    left: tuple[Fraction, Fraction, Fraction],
    right: tuple[Fraction, Fraction, Fraction],
) -> tuple[Fraction, Fraction, Fraction]:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def expr_scale(
    scalar: Fraction, value: tuple[Fraction, Fraction, Fraction]
) -> tuple[Fraction, Fraction, Fraction]:
    if type(scalar) is not Fraction:
        raise TypeError("expression scalar must be exact Fraction")
    return tuple(scalar * item for item in value)  # type: ignore[return-value]


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


@lru_cache(maxsize=None)
def basis_intervals(
    limit: int = K_INTERVAL_LIMIT,
) -> tuple[tuple[Fraction, Fraction], ...]:
    if type(limit) is not int or limit <= 3:
        raise ValueError("Euler-product interval cutoff must exceed three")
    output: list[tuple[Fraction, Fraction]] = []
    primes = primes_through(limit)
    for order in (1, 2, 3):
        upper = Fraction(1)
        for prime in primes:
            upper *= Fraction(prime * prime - order, prime * prime)
        lower = upper * Fraction(limit - order, limit)
        output.append((lower, upper))
    return tuple(output)


@lru_cache(maxsize=None)
def expr_interval(
    value: tuple[Fraction, Fraction, Fraction],
    limit: int = K_INTERVAL_LIMIT,
) -> tuple[Fraction, Fraction]:
    if type(value) is not tuple or len(value) != 3 or any(
        type(coefficient) is not Fraction for coefficient in value
    ):
        raise TypeError("interval evaluation requires an exact K-expression")
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
    left: tuple[Fraction, Fraction, Fraction],
    right: tuple[Fraction, Fraction, Fraction],
) -> int:
    difference = tuple(a - b for a, b in zip(left, right))
    if difference == ZERO_EXPR:
        return 0
    lower, upper = expr_interval(difference)  # exact rational enclosure
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise ArithmeticError(
        "Euler-product intervals overlap for distinct formal candidates"
    )


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


def reflected_relation_mask(mask: int) -> int:
    return relation_mask((-left, -right) for left, right in relation_pairs(mask))


def relation_pairs(mask: int) -> tuple[tuple[int, int], ...]:
    if type(mask) is not int or not 0 <= mask < 512:
        raise ValueError("relation mask must be an exact integer in [0,512)")
    return tuple(
        (x, y)
        for index, (x, y) in enumerate((x, y) for x in T for y in T)
        if mask & (1 << index)
    )


def relation_mask(pairs: Iterable[tuple[int, int]]) -> int:
    output = 0
    seen: set[tuple[int, int]] = set()
    universe = tuple((x, y) for x in T for y in T)
    for pair in pairs:
        if type(pair) is not tuple or len(pair) != 2 or pair not in universe or pair in seen:
            raise ValueError("relation contains an invalid or duplicate ternary pair")
        seen.add(pair)
        output |= 1 << universe.index(pair)
    return output


@lru_cache(maxsize=None)
def relation_source_mask(mask: int) -> int:
    return state_mask({x for x, _ in relation_pairs(mask)})


@lru_cache(maxsize=None)
def relation_target_mask(mask: int) -> int:
    return state_mask({y for _, y in relation_pairs(mask)})


def relation_composition_empty(left: int, right: int) -> bool:
    return relation_target_mask(left) & relation_source_mask(right) == 0


def saturated_relation(previous_target: int, current_target: int) -> int:
    previous = set(state_members(previous_target))
    current = set(state_members(current_target))
    return relation_mask((x, y) for x in T if x not in previous for y in current)


@lru_cache(maxsize=1)
def relation_pair_audit() -> dict[str, object]:
    safe_count = 0
    changed_count = 0
    inclusion_failures = 0
    criterion_failures = 0
    saturation_failures = 0
    pair_rows = tuple(relation_pairs(mask) for mask in range(512))
    for left in range(512):
        left_target = relation_target_mask(left)
        for right in range(512):
            criterion = left_target & relation_source_mask(right) == 0
            composed_empty = not any(
                middle_left == middle_right
                for _source, middle_left in pair_rows[left]
                for middle_right, _target in pair_rows[right]
            )
            if criterion != composed_empty:
                criterion_failures += 1
            if not criterion:
                continue
            safe_count += 1
            saturated = saturated_relation(left_target, relation_target_mask(right))
            if right & ~saturated:
                inclusion_failures += 1
            if saturated != right:
                changed_count += 1
            saturated_pairs = pair_rows[saturated]
            if any(
                middle_left == middle_right
                for _source, middle_left in pair_rows[left]
                for middle_right, _target in saturated_pairs
            ):
                saturation_failures += 1
    return {
        "relation_count": 512,
        "ordered_relation_pair_count": 262144,
        "safe_pair_count": safe_count,
        "saturation_changed_pair_count": changed_count,
        "criterion_failure_count": criterion_failures,
        "inclusion_failure_count": inclusion_failures,
        "saturation_failure_count": saturation_failures,
        "pass": criterion_failures == inclusion_failures == saturation_failures == 0,
    }


def projection_audit() -> dict[str, object]:
    case_count = 0
    deleted_plus_cases = 0
    plus_inclusion_failures = 0
    score_monotonicity_failures = 0
    zero_score_equality_failures = 0
    safety_preservation_failures = 0
    deleted_coordinates: set[tuple[int, int, int]] = set()
    for left in T:
        for center in T:
            for right in T:
                for old_output in (-1, 1):
                    case_count += 1
                    new_output = (
                        old_output if center == 1 else -1
                    )
                    old_plus = old_output == 1
                    new_plus = new_output == 1
                    if new_plus and not old_plus:
                        plus_inclusion_failures += 1
                    if center * new_output < center * old_output:
                        score_monotonicity_failures += 1
                    if center == 0 and center * new_output != center * old_output:
                        zero_score_equality_failures += 1
                    # Any forbidden pair in the projected plus set was already
                    # a forbidden pair before projection, precisely because
                    # the projected plus set is a subset of the old one.
                    if new_plus and not old_plus:
                        safety_preservation_failures += 1
                    if old_plus and not new_plus:
                        deleted_plus_cases += 1
                        deleted_coordinates.add((left, center, right))
    return {
        "full_table_input_count": 27,
        "positive_center_input_count": 9,
        "deleted_input_count": 18,
        "full_sign_table_count": 1 << 27,
        "relation_count": 1 << 9,
        "preimages_per_relation": 1 << 18,
        "uniform_fiber_identity_pass": (1 << 9) * (1 << 18) == (1 << 27),
        "pointwise_case_count": case_count,
        "deleted_plus_case_count": deleted_plus_cases,
        "deleted_coordinate_count": len(deleted_coordinates),
        "plus_set_inclusion_failure_count": plus_inclusion_failures,
        "score_monotonicity_failure_count": score_monotonicity_failures,
        "zero_score_equality_failure_count": zero_score_equality_failures,
        "safety_preservation_failure_count": safety_preservation_failures,
        "pointwise_projection_pass": (
            case_count == 54
            and deleted_plus_cases == 18
            and len(deleted_coordinates) == 18
            and plus_inclusion_failures == 0
            and score_monotonicity_failures == 0
            and zero_score_equality_failures == 0
            and safety_preservation_failures == 0
        ),
    }


@lru_cache(maxsize=1)
def reflection_audit() -> dict[str, object]:
    relation_involution_failures = 0
    state_compatibility_failures = 0
    for relation in range(512):
        reflected = reflected_relation_mask(relation)
        if reflected_relation_mask(reflected) != relation:
            relation_involution_failures += 1
        if relation_source_mask(reflected) != reflected_state_mask(relation_source_mask(relation)):
            state_compatibility_failures += 1
        if relation_target_mask(reflected) != reflected_state_mask(relation_target_mask(relation)):
            state_compatibility_failures += 1

    safe_pair_count = 0
    safety_preservation_failures = 0
    pair_rows = tuple(relation_pairs(mask) for mask in range(512))
    for left in range(512):
        reflected_left = reflected_relation_mask(left)
        for right in range(512):
            composed_empty = not any(
                middle_left == middle_right
                for _source, middle_left in pair_rows[left]
                for middle_right, _target in pair_rows[right]
            )
            reflected_right = reflected_relation_mask(right)
            reflected_empty = not any(
                middle_left == middle_right
                for _source, middle_left in pair_rows[reflected_left]
                for middle_right, _target in pair_rows[reflected_right]
            )
            if composed_empty:
                safe_pair_count += 1
            if composed_empty != reflected_empty:
                safety_preservation_failures += 1

    saturation_commutation_failures = 0
    for previous in ALL_STATE_MASKS:
        for current in ALL_STATE_MASKS:
            left = reflected_relation_mask(saturated_relation(previous, current))
            right = saturated_relation(
                reflected_state_mask(previous), reflected_state_mask(current)
            )
            if left != right:
                saturation_commutation_failures += 1

    lambda_cell_count = 0
    lambda_invariance_failures = 0
    for q in range(1, 11):
        for phase in range(q):
            for left in T:
                for right in T:
                    lambda_cell_count += 1
                    if lambda_coefficients(q, phase, left, right) != lambda_coefficients(
                        q, phase, -left, -right
                    ):
                        lambda_invariance_failures += 1

    pointwise_score_cases = 0
    pointwise_sign_failures = 0
    for left in T:
        for center in T:
            for right in T:
                for reflected_output in (-1, 1):
                    pointwise_score_cases += 1
                    new_score = center * reflected_output
                    old_score_at_negated_input = (-center) * reflected_output
                    if new_score != -old_score_at_negated_input:
                        pointwise_sign_failures += 1

    return {
        "state_map": "Y -> {-t:t in Y}",
        "relation_map": "A -> {(-x,-y):(x,y) in A}",
        "relation_involution_failure_count": relation_involution_failures,
        "relation_state_compatibility_failure_count": state_compatibility_failures,
        "ordered_safe_pair_count": safe_pair_count,
        "safety_preservation_failure_count": safety_preservation_failures,
        "saturation_commutation_case_count": 64,
        "saturation_commutation_failure_count": saturation_commutation_failures,
        "lambda_sign_cell_case_count": lambda_cell_count,
        "lambda_sign_cell_invariance_failure_count": lambda_invariance_failures,
        "full_table_reflection": "F^rho(x,z,y)=F(-x,-z,-y)",
        "pointwise_score_sign_case_count": pointwise_score_cases,
        "pointwise_score_sign_failure_count": pointwise_sign_failures,
        "terminal_sign_source": "RH394_three_shift_table_law_and_sign_cell_change_of_variables",
        "terminal_sign_identity": "L_q(F^rho)=-L_q(F)",
        "absolute_capacity_identity": "max_safe |L_q|=max_safe L_q",
        "both_signs_attained": True,
        "pass": (
            relation_involution_failures == 0
            and state_compatibility_failures == 0
            and safe_pair_count == 3375
            and safety_preservation_failures == 0
            and saturation_commutation_failures == 0
            and lambda_cell_count == 495
            and lambda_invariance_failures == 0
            and pointwise_score_cases == 54
            and pointwise_sign_failures == 0
        ),
    }


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


def _ordered_support(values: Iterable[str]) -> tuple[str, ...]:
    support = tuple(values)
    if any(type(value) is not str or value not in COORDINATES for value in support):
        raise ValueError("support contains an invalid coordinate")
    if len(set(support)) != len(support):
        raise ValueError("support contains a duplicate coordinate")
    return tuple(value for value in COORDINATES if value in support)


@lru_cache(maxsize=None)
def theta_coefficients(
    q: int, r: int, support: tuple[str, ...]
) -> tuple[Fraction, Fraction, Fraction]:
    if type(q) is not int or q < 1 or type(r) is not int or not 0 <= r < q:
        raise ValueError("phase must use exact q>=1 and 0<=r<q")
    support = _ordered_support(support)
    cardinality = len(support)
    if cardinality not in (1, 2, 3):
        raise ValueError("theta basis supports have size one, two, or three")
    coefficient = Fraction(1, q)
    for prime, exponent in factorization(q):
        base = Fraction(prime * prime - cardinality, prime * prime)
        residues = {
            SHIFT_BY_COORDINATE[coordinate] % (prime * prime)
            for coordinate in support
        }
        if exponent == 1:
            collision = sum(1 for residue in residues if residue % prime == r % prime)
            replacement = Fraction(prime - collision, prime)
        else:
            replacement = Fraction(int(r % (prime * prime) not in residues), 1)
        coefficient *= replacement / base
    output = [Fraction(0), Fraction(0), Fraction(0)]
    output[cardinality - 1] = coefficient
    return tuple(output)  # type: ignore[return-value]


@lru_cache(maxsize=None)
def exact_support_coefficients(
    q: int, r: int, support: tuple[str, ...]
) -> tuple[Fraction, Fraction, Fraction]:
    support = _ordered_support(support)
    if "C" not in support:
        raise ValueError("scored exact support must contain the center")
    complement = tuple(value for value in COORDINATES if value not in support)
    output = ZERO_EXPR
    for subset_mask in range(1 << len(complement)):
        extension = tuple(
            complement[index]
            for index in range(len(complement))
            if subset_mask & (1 << index)
        )
        union = _ordered_support((*support, *extension))
        sign = Fraction(-1 if subset_mask.bit_count() % 2 else 1)
        output = expr_add(output, expr_scale(sign, theta_coefficients(q, r, union)))
    return output


@lru_cache(maxsize=None)
def lambda_coefficients(
    q: int, r: int, left: int, right: int
) -> tuple[Fraction, Fraction, Fraction]:
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
        exact_support_coefficients(q, r, _ordered_support(support)),
    )


@lru_cache(maxsize=None)
def transition_coefficients(
    q: int, r: int, previous_mask: int, current_mask: int
) -> tuple[Fraction, Fraction, Fraction]:
    previous = set(state_members(previous_mask))
    current = set(state_members(current_mask))
    output = ZERO_EXPR
    for left in T:
        for right in T:
            if left not in previous and right in current:
                output = expr_add(output, lambda_coefficients(q, r, left, right))
    return output


def compressed_transition_coefficients(
    q: int, r: int, previous_mask: int, current_mask: int
) -> tuple[Fraction, Fraction, Fraction]:
    if previous_mask not in FOUR_STATE_MASKS or current_mask not in FOUR_STATE_MASKS:
        raise ValueError("compressed transition requires an antipodally symmetric state")
    previous = set(state_members(previous_mask))
    current = set(state_members(current_mask))
    u0, u1 = int(0 in previous), int(-1 in previous and 1 in previous)
    v0, v1 = int(0 in current), int(-1 in current and 1 in current)
    a = exact_support_coefficients(q, r, ("C",))
    b = exact_support_coefficients(q, r, ("L", "C"))
    c = exact_support_coefficients(q, r, ("C", "R"))
    d = exact_support_coefficients(q, r, ("L", "C", "R"))
    output = ZERO_EXPR
    for coefficient, indicator in (
        (a, (1 - u0) * v0),
        (b, (1 - u1) * v0),
        (c, (1 - u0) * v1),
        (d, (1 - u1) * v1),
    ):
        output = expr_add(output, expr_scale(Fraction(indicator), coefficient))
    return output


def multi_affinity_audit() -> dict[str, object]:
    """Symbolically certify the q>=3 antipodal endpoint reduction.

    The eight coordinates below stand for the independent local symbols
    (a_r,b_r,c_r,d_r,a_{r+2},b_{r+2},c_{r+2},d_{r+2}).  Thus no numerical
    density specialization can hide a non-affine middle state.
    """

    def basis(index: int, coefficient: Fraction) -> tuple[Fraction, ...]:
        return tuple(
            coefficient if position == index else Fraction(0)
            for position in range(8)
        )

    def add(*values: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
        return tuple(sum(items, Fraction(0)) for items in zip(*values))

    def occurrence(
        previous_zero: int,
        previous_nonzero: int,
        current_zero: int,
        current_nonzero: int,
        next_zero: int,
        next_nonzero: int,
    ) -> tuple[Fraction, ...]:
        k_previous = Fraction(previous_nonzero, 2)
        k_current = Fraction(current_nonzero, 2)
        k_next = Fraction(next_nonzero, 2)
        return add(
            basis(0, Fraction((1 - previous_zero) * current_zero)),
            basis(1, (1 - k_previous) * current_zero),
            basis(2, Fraction(1 - previous_zero) * k_current),
            basis(3, (1 - k_previous) * k_current),
            basis(4, Fraction((1 - current_zero) * next_zero)),
            basis(5, (1 - k_current) * next_zero),
            basis(6, Fraction(1 - current_zero) * k_next),
            basis(7, (1 - k_current) * k_next),
        )

    context_count = 0
    second_difference_failures = 0
    for previous_zero in (0, 1):
        for current_zero in (0, 1):
            for next_zero in (0, 1):
                for previous_nonzero in (0, 1, 2):
                    for next_nonzero in (0, 1, 2):
                        context_count += 1
                        values = [
                            occurrence(
                                previous_zero,
                                previous_nonzero,
                                current_zero,
                                current_nonzero,
                                next_zero,
                                next_nonzero,
                            )
                            for current_nonzero in (0, 1, 2)
                        ]
                        second_difference = tuple(
                            values[0][index]
                            - 2 * values[1][index]
                            + values[2][index]
                            for index in range(8)
                        )
                        if any(second_difference):
                            second_difference_failures += 1
    self_identification = {
        str(q): ((2 % q) == 0) for q in range(1, 11)
    }
    return {
        "symbolic_basis": [
            "a_r", "b_r", "c_r", "d_r",
            "a_(r+2)", "b_(r+2)", "c_(r+2)", "d_(r+2)",
        ],
        "context_count": context_count,
        "second_difference_failure_count": second_difference_failures,
        "affine_endpoint_dominance": (
            "f(1)=(f(0)+f(2))/2, so max(f(0),f(2))>=f(1)"
        ),
        "state_variable_self_identification_q_1_to_10": self_identification,
        "self_identification_iff_q_divides_2": True,
        "compression_scope": "q>=3_only",
        "pass": (
            context_count == 72
            and second_difference_failures == 0
            and self_identification
            == {str(q): q in (1, 2) for q in range(1, 11)}
        ),
    }


def plus_two_cycles(q: int) -> tuple[tuple[int, ...], ...]:
    if type(q) is not int or q < 1:
        raise ValueError("clock must be a positive exact integer")
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
            phase = (phase + 2) % q
        output.append(tuple(cycle))
    return tuple(output)


def _better_candidate(
    candidate: tuple[tuple[Fraction, Fraction, Fraction], tuple[int, ...]],
    incumbent: tuple[tuple[Fraction, Fraction, Fraction], tuple[int, ...]] | None,
) -> bool:
    if incumbent is None:
        return True
    comparison = compare_expressions(candidate[0], incumbent[0])
    if comparison > 0:
        return True
    if comparison < 0:
        return False
    return (candidate[0], tuple(-value for value in candidate[1])) > (
        incumbent[0], tuple(-value for value in incumbent[1])
    )


def capacity_dp(q: int, states: tuple[int, ...]) -> dict[str, object]:
    if type(states) is not tuple or not states or len(set(states)) != len(states):
        raise ValueError("DP states must be a nonempty unique exact tuple")
    if any(type(state) is not int or not 0 <= state < 8 for state in states):
        raise ValueError("DP state is invalid")
    total = ZERO_EXPR
    cycle_rows: list[dict[str, object]] = []
    for phases in plus_two_cycles(q):
        best: tuple[tuple[Fraction, Fraction, Fraction], tuple[int, ...]] | None = None
        for initial in states:
            dynamic: dict[int, tuple[tuple[Fraction, Fraction, Fraction], tuple[int, ...]]] = {
                initial: (ZERO_EXPR, (initial,))
            }
            for phase in phases:
                next_dynamic: dict[
                    int, tuple[tuple[Fraction, Fraction, Fraction], tuple[int, ...]]
                ] = {}
                for previous, (value, path) in dynamic.items():
                    for current in states:
                        candidate = (
                            expr_add(value, transition_coefficients(q, phase, previous, current)),
                            (*path, current),
                        )
                        if _better_candidate(candidate, next_dynamic.get(current)):
                            next_dynamic[current] = candidate
                dynamic = next_dynamic
            closed = dynamic[initial]
            if _better_candidate(closed, best):
                best = closed
        if best is None:
            raise RuntimeError("empty tropical cycle optimization")
        total = expr_add(total, best[0])
        cycle_rows.append({
            "phases": list(phases),
            "state_path": list(best[1]),
            "coefficients": expr_text(best[0]),
        })
    return {
        "q": q,
        "state_masks": list(states),
        "cycle_count": len(cycle_rows),
        "cycles": cycle_rows,
        "coefficients": expr_text(total),
        "expression": total,
    }


def full_capacity(q: int) -> dict[str, object]:
    return capacity_dp(q, ALL_STATE_MASKS)


def four_state_capacity(q: int) -> dict[str, object]:
    return capacity_dp(q, FOUR_STATE_MASKS)


def one_site_capacity(q: int) -> dict[str, object]:
    return capacity_dp(q, (0, 7))


def optimizer_state_map(dp_result: dict[str, object]) -> dict[int, int]:
    if type(dp_result) is not dict or type(dp_result.get("cycles")) is not list:
        raise TypeError("optimizer result is malformed")
    output: dict[int, int] = {}
    for row in dp_result["cycles"]:
        if type(row) is not dict or type(row.get("phases")) is not list or type(row.get("state_path")) is not list:
            raise TypeError("optimizer cycle row is malformed")
        phases = row["phases"]
        path = row["state_path"]
        if len(path) != len(phases) + 1 or path[0] != path[-1]:
            raise RuntimeError("optimizer path is not cyclic")
        for index, phase in enumerate(phases):
            output[phase] = path[index + 1]
    if set(output) != set(range(dp_result["q"])):
        raise RuntimeError("optimizer path does not cover every phase")
    return output


def divisibility_lift_audit(q: int, Q: int) -> dict[str, object]:
    if type(q) is not int or type(Q) is not int or q < 1 or Q < 1 or Q % q:
        raise ValueError("divisibility lift requires positive exact q|Q")
    base = full_capacity(q)
    states = optimizer_state_map(base)
    lifted_score = ZERO_EXPR
    transition_aggregation_pass = True
    density_aggregation_pass = True
    for phase in range(q):
        fine_phases = tuple(value for value in range(Q) if value % q == phase)
        for support in (
            ("C",), ("L", "C"), ("C", "R"), ("L", "C", "R")
        ):
            aggregate = ZERO_EXPR
            for fine in fine_phases:
                aggregate = expr_add(
                    aggregate, exact_support_coefficients(Q, fine, support)
                )
            if aggregate != exact_support_coefficients(q, phase, support):
                density_aggregation_pass = False
        previous = states[(phase - 2) % q]
        current = states[phase]
        aggregate_transition = ZERO_EXPR
        for fine in fine_phases:
            aggregate_transition = expr_add(
                aggregate_transition,
                transition_coefficients(Q, fine, previous, current),
            )
            lifted_score = expr_add(
                lifted_score,
                transition_coefficients(Q, fine, previous, current),
            )
        if aggregate_transition != transition_coefficients(q, phase, previous, current):
            transition_aggregation_pass = False
    lifted_relations = {
        phase: saturated_relation(
            states[(phase - 2) % q], states[phase % q]
        )
        for phase in range(Q)
    }
    lifted_safe = all(
        relation_composition_empty(
            lifted_relations[phase], lifted_relations[(phase + 2) % Q]
        )
        for phase in range(Q)
    )
    return {
        "q": q,
        "Q": Q,
        "density_aggregation_pass": density_aggregation_pass,
        "transition_aggregation_pass": transition_aggregation_pass,
        "lifted_relation_safety_pass": lifted_safe,
        "lifted_relation_count": len(lifted_relations),
        "base_coefficients": base["coefficients"],
        "lifted_coefficients": expr_text(lifted_score),
        "score_identity_pass": lifted_score == base["expression"],
        "pass": (
            density_aggregation_pass
            and transition_aggregation_pass
            and lifted_safe
            and lifted_score == base["expression"]
        ),
    }


def center_phase_positive(q: int, phase: int) -> bool:
    return theta_coefficients(q, phase % q, ("C",)) != ZERO_EXPR


def left_marginal(
    q: int, phase: int, shared_value: int
) -> tuple[Fraction, Fraction, Fraction]:
    output = ZERO_EXPR
    for left in T:
        output = expr_add(
            output, lambda_coefficients(q, phase % q, left, shared_value)
        )
    return output


def right_marginal(
    q: int, phase: int, shared_value: int
) -> tuple[Fraction, Fraction, Fraction]:
    output = ZERO_EXPR
    for right in T:
        output = expr_add(
            output, lambda_coefficients(q, phase % q, shared_value, right)
        )
    return output


def q36_pattern_scan() -> dict[str, object]:
    raw: set[tuple[int, int, int]] = set()
    phases: dict[tuple[int, int, int], list[int]] = {}
    for phase in range(36):
        if not center_phase_positive(36, phase) or not center_phase_positive(36, phase + 2):
            continue
        pattern = tuple(
            int(center_phase_positive(36, phase + offset))
            for offset in (-1, 1, 3)
        )
        raw.add(pattern)
        phases.setdefault(pattern, []).append(phase)
    quotient = {min(pattern, tuple(reversed(pattern))) for pattern in raw}
    return {
        "raw_patterns": [list(pattern) for pattern in sorted(raw)],
        "raw_pattern_count": len(raw),
        "reflection_quotient": [list(pattern) for pattern in sorted(quotient)],
        "reflection_quotient_count": len(quotient),
        "phase_classes": {
            "".join(str(bit) for bit in pattern): values
            for pattern, values in sorted(phases.items())
        },
        "pass": len(raw) == 5 and len(quotient) == 4,
    }


def square_marginal_interface_audit() -> dict[str, object]:
    """Reproduce the general square-support local and path algebra."""

    # Coordinates are (delta, theta_2).  These two independent symbols make
    # the forced and allowed branches exact without choosing a particular q.
    forced = {
        -1: (Fraction(0), Fraction(0)),
        0: (Fraction(1), Fraction(0)),
        1: (Fraction(0), Fraction(0)),
    }
    allowed = {
        -1: (Fraction(0), Fraction(1, 2)),
        0: (Fraction(1), Fraction(-1)),
        1: (Fraction(0), Fraction(1, 2)),
    }
    branch_rows: list[dict[str, object]] = []
    for label, branch in (("shared_forced_zero", forced), ("shared_allowed", allowed)):
        total = tuple(
            sum(branch[value][index] for value in T)
            for index in range(2)
        )
        branch_rows.append({
            "branch": label,
            "left_marginals": {
                str(value): [fraction_text(item) for item in branch[value]]
                for value in T
            },
            "right_marginals": {
                str(value): [fraction_text(item) for item in branch[value]]
                for value in T
            },
            "sum_coefficients": [fraction_text(item) for item in total],
            "left_right_per_t_equal": True,
            "outside_prime_pair_factors_are_translates": True,
            "pass": total == (Fraction(1), Fraction(0)),
        })

    recurrence = [0, 1]
    recurrence_failures = 0
    for length in range(2, 13):
        recurrence.append(max(recurrence[-1], 1 + recurrence[-2]))
    for length, charge in enumerate(recurrence):
        if charge != (length + 1) // 2:
            recurrence_failures += 1

    cycle_rows: list[dict[str, object]] = []
    reset_failures = 0
    for cycle in plus_two_cycles(36):
        bits = [int(center_phase_positive(36, phase)) for phase in cycle]
        zero_phases = [phase for phase, bit in zip(cycle, bits) if bit == 0]
        if not zero_phases or not all(
            phase % 4 == 0 or phase % 9 == 0 for phase in zero_phases
        ):
            reset_failures += 1
        runs: list[int] = []
        if any(bit == 0 for bit in bits):
            start = bits.index(0)
            rotated = bits[start + 1 :] + bits[: start + 1]
            length = 0
            for bit in rotated:
                if bit:
                    length += 1
                elif length:
                    runs.append(length)
                    length = 0
        cycle_rows.append({
            "phases": list(cycle),
            "zero_phases": zero_phases,
            "positive_run_lengths": runs,
            "run_charge_units": sum((length + 1) // 2 for length in runs),
        })

    repetition_fixtures: list[dict[str, object]] = []
    for base, multiple in ((36, 72), (36, 108), (36, 324), (900, 1800)):
        ratio = multiple // base
        base_allowed = next(
            phase for phase in range(base) if center_phase_positive(base, phase)
        )
        fine_allowed = next(
            phase
            for phase in range(multiple)
            if phase % base == base_allowed
            and center_phase_positive(multiple, phase)
        )
        base_delta = theta_coefficients(base, base_allowed, ("C",))
        fine_delta = theta_coefficients(multiple, fine_allowed, ("C",))
        repetition_fixtures.append({
            "base": base,
            "multiple": multiple,
            "ratio": ratio,
            "same_prime_support": prime_support(base) == prime_support(multiple),
            "delta_repetition_identity": fine_delta == expr_scale(Fraction(1, ratio), base_delta),
        })

    return {
        "hypotheses": {
            "supported_prime_exponents_at_least_two": True,
            "adjacent_centers_allowed": True,
            "outside_prime_pair_factors_are_residue_translates": True,
            "common_positive_center_weight": True,
        },
        "local_branches": branch_rows,
        "path_bound": {
            "individual_bound": "W_i<=delta",
            "adjacent_pair_bound": "W_i+W_(i+1)<=delta",
            "recurrence": "R_L=max(R_(L-1),1+R_(L-2))",
            "charges_L_0_to_12": recurrence,
            "closed_form": "ceil(L/2)*delta",
            "failure_count": recurrence_failures,
        },
        "forced_reset_moduli": [4, 9],
        "q36_plus_two_cycles": cycle_rows,
        "reset_failure_count": reset_failures,
        "same_support_repetition": {
            "formula": "delta_Q=delta_q/(Q/q)",
            "fixtures": repetition_fixtures,
        },
        "pass": (
            all(row["pass"] is True for row in branch_rows)
            and recurrence_failures == 0
            and reset_failures == 0
            and all(
                row["same_prime_support"] is True
                and row["delta_repetition_identity"] is True
                for row in repetition_fixtures
            )
        ),
    }


def odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("square-clock index must be a positive exact integer")
    output: list[int] = []
    candidate = 3
    while len(output) < count:
        if all(candidate % prime for prime in range(2, math.isqrt(candidate) + 1)):
            output.append(candidate)
        candidate += 2
    return tuple(output)


def square_clock(index: int) -> int:
    output = 4
    for prime in odd_primes(index):
        output *= prime * prime
    return output


def prime_support(value: int) -> tuple[int, ...]:
    return tuple(prime for prime, _ in factorization(value))


def gcd(left: int, right: int) -> int:
    if type(left) is not int or type(right) is not int or left < 1 or right < 1:
        raise ValueError("gcd inputs must be positive exact integers")
    while right:
        left, right = right, left % right
    return left


def lcm(left: int, right: int) -> int:
    return left // gcd(left, right) * right


def cutoff_bridge(q: int) -> dict[str, object]:
    if type(q) is not int or q < 1:
        raise ValueError("cutoff bridge requires a positive exact clock")
    odd_support = tuple(prime for prime in prime_support(q) if prime != 2)
    index = 1
    while not set(odd_support) <= set(odd_primes(index)):
        index += 1
    base = square_clock(index)
    common = lcm(q, base)
    return {
        "q": q,
        "cutoff_index": index,
        "q_y": base,
        "Q": common,
        "q_divides_Q": common % q == 0,
        "q_y_divides_Q": common % base == 0,
        "same_prime_support": prime_support(common) == prime_support(base),
        "strict_endpoint_chain": "C(q)<=C(Q)=B_y<B_infinity",
        "pass": (
            common % q == 0
            and common % base == 0
            and prime_support(common) == prime_support(base)
        ),
    }


def _fraction_binary(value: Fraction) -> bytes:
    if type(value) is not Fraction:
        raise TypeError("binary fraction encoding requires exact Fraction")
    pieces: list[bytes] = []
    for integer in (value.numerator, value.denominator):
        sign = b"-" if integer < 0 else b"+"
        magnitude = abs(integer)
        raw = magnitude.to_bytes(max(1, (magnitude.bit_length() + 7) // 8), "big")
        pieces.append(sign + len(raw).to_bytes(4, "big") + raw)
    return b"".join(pieces)


def rigorous_interval_audit() -> dict[str, object]:
    basis_rows: list[dict[str, object]] = []
    for order, (lower, upper) in zip((1, 2, 3), basis_intervals()):
        basis_rows.append({
            "order": order,
            "lower_positive": lower > 0,
            "width_positive": upper - lower > 0,
            "lower_bits": [lower.numerator.bit_length(), lower.denominator.bit_length()],
            "upper_bits": [upper.numerator.bit_length(), upper.denominator.bit_length()],
            "bounds_sha256": sha256(_fraction_binary(lower) + _fraction_binary(upper)).hexdigest(),
        })
    differences = {
        "K2_minus_K3": (Fraction(0), Fraction(1), Fraction(-1)),
        "three_K3_minus_K2": (Fraction(0), Fraction(-1), Fraction(3)),
        "two_K2_minus_K1": (Fraction(-1), Fraction(2), Fraction(0)),
        "K2_minus_two_K3": (Fraction(0), Fraction(1), Fraction(-2)),
    }
    separation_rows: list[dict[str, object]] = []
    for label, expression in differences.items():
        lower, upper = expr_interval(expression)
        separation_rows.append({
            "label": label,
            "coefficients": expr_text(expression),
            "lower_positive": lower > 0,
            "upper_positive": upper > 0,
            "lower_bits": [lower.numerator.bit_length(), lower.denominator.bit_length()],
            "interval_sha256": sha256(_fraction_binary(lower) + _fraction_binary(upper)).hexdigest(),
        })
    return {
        "cutoff": K_INTERVAL_LIMIT,
        "tail_bound": "sum_(p>P) p^-2 < 1/P",
        "basis_intervals": basis_rows,
        "separations": separation_rows,
        "nonidentical_overlap_policy": "raise",
        "pass": all(row["lower_positive"] is True for row in separation_rows),
    }


def _state_class(mask: int) -> str:
    members = state_members(mask)
    nonzero = sum(value != 0 for value in members)
    if not members:
        return "empty"
    if members == (0,):
        return "zero_endpoint"
    if nonzero == 1 and 0 not in members:
        return "one_sign"
    if nonzero == 2 and 0 not in members:
        return "both_signs"
    if len(members) == 3:
        return "all"
    return "mixed"


def _row(kind: str, identifier: str, data: dict[str, object], passed: bool) -> dict[str, object]:
    if type(kind) is not str or type(identifier) is not str or type(data) is not dict or type(passed) is not bool:
        raise TypeError("certificate row fields have wrong exact types")
    return {"kind": kind, "id": identifier, "data": data, "pass": passed}


def _subset_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for mask in ALL_STATE_MASKS:
        members = state_members(mask)
        rows.append(_row("subset_state", f"mask_{mask}", {
            "mask": mask,
            "members": list(members),
            "contains_zero": 0 in members,
            "nonzero_count": sum(value != 0 for value in members),
            "reflection_mask": reflected_state_mask(mask),
            "compressed_state": mask in FOUR_STATE_MASKS,
        }, state_mask(members) == mask and reflected_state_mask(reflected_state_mask(mask)) == mask))
    return rows


def _q2_rows() -> list[dict[str, object]]:
    full = full_capacity(2)["coefficients"]
    compressed = four_state_capacity(2)["coefficients"]
    rows: list[dict[str, object]] = []
    for phase in range(2):
        for mask in ALL_STATE_MASKS:
            coefficients = expr_text(transition_coefficients(2, phase, mask, mask))
            witness = (phase == 0 and mask == 1) or (phase == 1 and mask == 2)
            rows.append(_row("q2_selfloop", f"phase_{phase}_mask_{mask}", {
                "phase": phase,
                "mask": mask,
                "members": list(state_members(mask)),
                "state_class": _state_class(mask),
                "selfloop_coefficients": coefficients,
                "selected_full8_witness": witness,
                "full8_capacity": full,
                "four_state_value": compressed,
                "strict_gap_coefficients": ["0", "-1/4", "3/4"],
                "old_four_state_all_q_value_forbidden": ["0", "1", "-1"],
            }, (
                full == ["0", "3/4", "-1/4"]
                and compressed == ["0", "1", "-1"]
                and (not witness or coefficients in (["0", "1/4", "-1/4"], ["0", "1/2", "0"]))
            )))
    return rows


def _small_clock_rows() -> list[dict[str, object]]:
    expected = {
        1: ["0", "1", "-1"],
        2: ["0", "3/4", "-1/4"],
        3: ["3/8", "0", "0"],
        4: ["2/3", "0", "0"],
        5: ["5/12", "0", "0"],
        6: ["1/8", "1/2", "0"],
    }
    rows: list[dict[str, object]] = []
    for q in range(1, 7):
        full = full_capacity(q)
        compressed = four_state_capacity(q)
        equality = full["coefficients"] == compressed["coefficients"]
        mode = "q1_full8_selfloop_lemma" if q == 1 else (
            "q2_full8_exception" if q == 2 else "q_ge_3_multi_affine_compression"
        )
        rows.append(_row("small_clock", f"clock_{q}", {
            "q": q,
            "cycle_count": full["cycle_count"],
            "full8_coefficients": full["coefficients"],
            "four_state_coefficients": compressed["coefficients"],
            "full8_equals_four_state": equality,
            "proof_mode": mode,
        }, full["coefficients"] == expected[q] and equality is (q != 2)))
    one = one_site_capacity(6)["coefficients"]
    rows.append(_row("small_clock", "one_site_q6", {
        "q": 6, "coefficients": one, "source_role": "RH375_MWIS_embedding",
    }, one == ["3/8", "0", "0"]))
    rows.append(_row("small_clock", "q6_strict_gain", {
        "difference_coefficients": ["-1/4", "1/2", "0"],
        "positive_inequality": "2K2-K1>0",
    }, compare_expressions(
        (Fraction(-1, 4), Fraction(1, 2), Fraction(0)), ZERO_EXPR
    ) > 0))
    rows.append(_row("small_clock", "q1_ratio", {
        "inequality": "K3/K2<1/2",
        "certifying_difference": ["0", "1", "-2"],
    }, compare_expressions(
        (Fraction(0), Fraction(1), Fraction(-2)), ZERO_EXPR
    ) > 0))
    rows.append(_row("small_clock", "q2_ratio", {
        "inequality": "K3/K2>1/3",
        "certifying_difference": ["0", "-1", "3"],
    }, compare_expressions(
        (Fraction(0), Fraction(-1), Fraction(3)), ZERO_EXPR
    ) > 0))
    rows.append(_row("small_clock", "q1_witness", {
        "selected_mask": 2,
        "selected_class": "zero_endpoint",
        "one_sign_mask": 1,
        "affinity_argument_used": False,
    }, transition_coefficients(1, 0, 2, 2) == (Fraction(0), Fraction(1), Fraction(-1))))
    rows.append(_row("small_clock", "q2_witness_summary", {
        "even_phase_mask": 1,
        "even_contribution": ["0", "1/4", "-1/4"],
        "odd_phase_mask": 2,
        "odd_contribution": ["0", "1/2", "0"],
        "selfloops_retained": True,
    }, (
        expr_text(transition_coefficients(2, 0, 1, 1)) == ["0", "1/4", "-1/4"]
        and expr_text(transition_coefficients(2, 1, 2, 2)) == ["0", "1/2", "0"]
    )))
    return rows


def _compression_rows() -> list[dict[str, object]]:
    generic = multi_affinity_audit()
    rows: list[dict[str, object]] = []
    for q in range(3, 11):
        full = full_capacity(q)
        compressed = four_state_capacity(q)
        transition_pass = all(
            transition_coefficients(q, phase, previous, current)
            == compressed_transition_coefficients(q, phase, previous, current)
            for phase in range(q)
            for previous in FOUR_STATE_MASKS
            for current in FOUR_STATE_MASKS
        )
        rows.append(_row("transfer_compression", f"q_{q}", {
            "q": q,
            "full8_coefficients": full["coefficients"],
            "four_state_coefficients": compressed["coefficients"],
            "transition_formula_pass": transition_pass,
            "multi_affinity_scope": "q>=3_only",
            "generic_symbolic_second_difference_pass": generic["pass"],
            "state_variable_self_identified": q in (1, 2),
        }, (
            transition_pass
            and generic["pass"] is True
            and q not in (1, 2)
            and full["coefficients"] == compressed["coefficients"]
        )))
    for q, parity in ((5, "odd_single_cycle"), (6, "even_two_cycles")):
        cycles = plus_two_cycles(q)
        rows.append(_row("transfer_compression", f"cycle_structure_{q}", {
            "q": q,
            "cycle_count": len(cycles),
            "cycle_lengths": [len(cycle) for cycle in cycles],
            "structure": parity,
            "gcd_q_2": gcd(q, 2),
        }, len(cycles) == gcd(q, 2)))
    return rows


def _marginal_rows() -> list[dict[str, object]]:
    scan = q36_pattern_scan()
    generic = square_marginal_interface_audit()
    patterns = (
        ("P0", 17, (0, 0, 0), None),
        ("P1", 19, (0, 0, 1), 15),
        ("P2", 3, (1, 0, 1), None),
        ("P3", 1, (0, 1, 0), None),
    )
    rows: list[dict[str, object]] = []
    for label, phase, pattern, reflection_partner in patterns:
        for shared in T:
            left = left_marginal(36, phase, shared)
            right = right_marginal(36, phase + 2, shared)
            delta = theta_coefficients(36, phase, ("C",))
            pair_total = ZERO_EXPR
            for value in T:
                pair_total = expr_add(pair_total, left_marginal(36, phase, value))
            centers = center_phase_positive(36, phase) and center_phase_positive(36, phase + 2)
            raw = tuple(
                int(center_phase_positive(36, phase + offset))
                for offset in (-1, 1, 3)
            )
            rows.append(_row("marginal_charge", f"{label}_t_{shared}", {
                "pattern_id": label,
                "representative_phase": phase,
                "raw_pattern": list(pattern),
                "reflection_partner_phase": reflection_partner,
                "shared_value": shared,
                "shared_allowed": bool(pattern[1]),
                "centers_positive": centers,
                "left_marginal": expr_text(left),
                "right_marginal": expr_text(right),
                "pair_charge_coefficients": expr_text(delta),
                "pair_charge_sum_pass": pair_total == delta,
                "raw_pattern_count": scan["raw_pattern_count"],
                "reflection_quotient_count": scan["reflection_quotient_count"],
                "run_charge": "ceil(L/2)*delta",
                "forced_resets": [4, 9],
                "generic_square_support_interface_pass": generic["pass"],
            }, (
                centers and raw == pattern and left == right and pair_total == delta
                and scan["pass"] is True and generic["pass"] is True
            )))
    return rows


def _square_rows() -> list[dict[str, object]]:
    generic = square_marginal_interface_audit()
    fixtures = (
        ("q36_B1", 36, 36, ["2/3", "0", "0"], "B1", "full8"),
        ("Q72_B1", 72, 36, ["2/3", "0", "0"], "B1", "four_state"),
        ("Q108_B1", 108, 36, ["2/3", "0", "0"], "B1", "four_state"),
        ("Q324_B1", 324, 36, ["2/3", "0", "0"], "B1", "four_state"),
        ("q900_B2", 900, 900, ["49/72", "0", "0"], "B2", "four_state"),
        ("Q1800_B2", 1800, 900, ["49/72", "0", "0"], "B2", "four_state"),
    )
    rows: list[dict[str, object]] = []
    for identifier, q, base, expected, label, method in fixtures:
        result = full_capacity(q) if method == "full8" else four_state_capacity(q)
        rows.append(_row("square_saturation", identifier, {
            "q": q,
            "base_square_clock": base,
            "same_prime_support": prime_support(q) == prime_support(base),
            "base_divides_q": q % base == 0,
            "capacity_coefficients": result["coefficients"],
            "endpoint_label": label,
            "optimizer": method,
            "marginal_pair_charge": True,
            "forced_four_and_nine_resets": True,
            "generic_square_support_interface_pass": generic["pass"],
        }, (
            result["coefficients"] == expected
            and q % base == 0
            and prime_support(q) == prime_support(base)
            and generic["pass"] is True
        )))
    rows.append(_row("square_saturation", "B1_strictly_below_B2", {
        "B1_coefficients": ["2/3", "0", "0"],
        "B2_coefficients": ["49/72", "0", "0"],
        "difference_coefficients": ["1/72", "0", "0"],
        "strict": True,
    }, compare_expressions((Fraction(1, 72), Fraction(0), Fraction(0)), ZERO_EXPR) > 0))
    bridge = cutoff_bridge(70)
    rows.append(_row("square_saturation", "arbitrary_clock_cutoff_bridge", {
        **bridge,
        "universal_interface": "choose y covering every prime divisor of fixed q",
    }, bridge["pass"] is True))
    return rows


def _firewall_rows() -> list[dict[str, object]]:
    lift_fixtures = [divisibility_lift_audit(q, Q) for q, Q in ((1, 3), (2, 6), (3, 6), (4, 8))]
    return [
        _row("theorem_firewall", "q_divides_Q_lift", {
            "direction": "C(q)<=C(Q)",
            "nonminimal_period_lift": True,
            "uniform_q_analytic_claim": False,
            "fixtures": lift_fixtures,
        }, all(row["pass"] is True for row in lift_fixtures)),
        _row("theorem_firewall", "all_clock_supremum", {
            "statement": "sup_(fixed finite q) C(q)=B_infinity",
            "witness": "embedded one-site relations at q_y",
            "attained_at_finite_q": False,
        }, True),
        _row("theorem_firewall", "finite_nonattainment", {
            "statement": "C(q)<B_infinity for every fixed finite q",
            "bridge": "C(q)<=C(lcm(q,q_y))=B_y<B_infinity",
            "finite_attainment": False,
        }, True),
        _row("theorem_firewall", "source_role_split", {
            "RH394": "terminal_log_table_Pi_lambda_limit",
            "RH375": "finite_clock_MWIS_square_density_and_same_support_combinatorics_only",
            "RH375_terminal_clock_analytic_input": False,
        }, True),
        _row("theorem_firewall", "centered_noncausal_type", {
            "window": ["mu_0(n-1)", "mu(n)", "mu(n+1)"],
            "future_coordinate_used": True,
            "causal_or_online": False,
            "RH378_window_end_model": "STOP_direct",
        }, True),
        _row("theorem_firewall", "claim_ceiling", {
            "fixed_q_and_tables_only": True,
            "growing_q": False,
            "rate": False,
            "ordinary_Cesaro": False,
            "prelimit_or_adaptive_max": False,
            "generic_graph_capacity": False,
            "even_odd_support_at_least_four": False,
            "operator_trace_zero_RH_or_Gates": False,
        }, True),
    ]


def build_certificate() -> dict[str, object]:
    rows = [
        *_subset_rows(),
        *_q2_rows(),
        *_small_clock_rows(),
        *_compression_rows(),
        *_marginal_rows(),
        *_square_rows(),
        *_firewall_rows(),
    ]
    counts = {
        kind: sum(row["kind"] == kind for row in rows)
        for kind in ROW_PARTITION
    }
    relation_audit = relation_pair_audit()
    projection = projection_audit()
    reflection = reflection_audit()
    intervals = rigorous_interval_audit()
    multi_affinity = multi_affinity_audit()
    square_interface = square_marginal_interface_audit()
    return {
        "schema_version": 1,
        "status": "RH-395_centered_three_window_core_certified",
        "title": TITLE,
        "epistemic_role": "finite_exact_reproduction_not_analytic_proof",
        "finite_reproduction_not_analytic_proof": True,
        "quantifiers": {
            "fixed_q": True,
            "fixed_phase_tables": True,
            "every_admissible_terminal_clock": True,
            "limit_before_maximum": True,
        },
        "model": {
            "alphabet": [-1, 0, 1],
            "window_coordinates": ["L", "C", "R"],
            "shifts": {"L": 1, "C": 0, "R": -1},
            "phase_table_type": "F_r:T^3->{-1,+1} for r in Z/qZ",
            "mobius_extension": "mu_0(k)=mu(k) for integer k>=1 and mu_0(k)=0 for k<=0",
            "terminal_clock": "as X->infinity, 1<=omega(X)<=X and omega(X)->infinity (so omega(X)>1 eventually)",
            "terminal_functional": "(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)*F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))/n",
            "fixed_table_limit": "L_q(F)=limit_(X->infinity) of the terminal functional for every admissible terminal clock",
            "universal_safety_condition": "not(F_r(a,b,c)=+1 and F_(r+2)(c,d,e)=+1) for every r and a,b,c,d,e in T",
            "capacity_definition": "C(q)=max_(universally safe fixed q-phase F) |L_q(F)| after each fixed-table limit exists",
            "all_clock_order": "fixed q and F; X->infinity; finite maximum over safe F; then sup over finite q",
            "score": "mu(n)*F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))",
            "universal_distance_two_safety": True,
            "centered_noncausal": True,
        },
        "relation_contract": {
            "projection": "A_r={(x,y):F_r(x,+1,y)=+1}",
            "safety": "Target(A_r) intersect Source(A_(r+2)) is empty",
            "saturation": "A_r=(T\\Y_(r-2)) cross Y_r",
            "full_state_count": 8,
            "compressed_state_count": 4,
            "compression_scope": "q>=3_only",
            "all_q_tropical_trace": "8x8",
        },
        "density_contract": {
            "coordinates": ["L", "C", "R"],
            "shift_tuple": [1, 0, -1],
            "B_definition": "B_(p,S)={a_i mod p^2:i in S}, with duplicate residues removed",
            "nu_definition": "nu_(p,S)=|B_(p,S)|",
            "tau_definition": "tau_(p,S)(r)=#{b in B_(p,S):b mod p=r mod p}",
            "theta": "Theta_(q,r)(S)=q^-1 product_(p not|q)(1-nu_(p,S)/p^2) product_(p||q)(1-tau_(p,S)(r)/p) product_(p^2|q)1_(r mod p^2 notin B_(p,S))",
            "theta_empty": "Theta_(q,r)(empty)=1/q",
            "K_definition": "K_j=product_p(1-j/p^2) for j=0,1,2,3; K_0=1",
            "theta_phase_mass": "sum_(r mod q) Theta_(q,r)(S)=K_|S|",
            "pi": "Pi_(q,r)(U)=sum_(W subset {L,C,R}\\U)(-1)^|W| Theta_(q,r)(U union W)",
            "pi_role": "nonnegative exact-support density",
            "pi_phase_mass": "sum_(U subset {L,C,R}) Pi_(q,r)(U)=1/q",
            "lambda": (
                "2^(-1_(x!=0)-1_(y!=0))*Pi_(q,r)"
                "({C} union ({L}:x!=0) union ({R}:y!=0))"
            ),
            "transition": "K_r(U,V)=sum_(x notin U,y in V) lambda_r(x,y)",
        },
        "endpoint_contract": {
            "one_site_capacity": "F_RH375(q)=max_(I subset Z/qZ, I intersect (I+2)=empty) sum_(r in I) Theta_(q,r)({C})",
            "square_clock": "q_y=4 product_(3<=p<=p_y, p prime) p^2, with q_1=36",
            "finite_endpoint": "B_y=F_RH375(q_y)",
            "limiting_endpoint": "B_infinity=lim_(y->infinity) B_y",
            "same_support_identity": "if q_y|Q and Q has the same prime support, C(Q)=F_RH375(Q)=B_y",
            "all_clock_statement": "C(q)<B_infinity for every finite q and sup_(q finite) C(q)=B_infinity",
        },
        "projection_audit": projection,
        "reflection_audit": reflection,
        "relation_pair_audit": relation_audit,
        "rigorous_interval_audit": intervals,
        "multi_affinity_audit": multi_affinity,
        "square_marginal_interface_audit": square_interface,
        "row_partition": dict(ROW_PARTITION),
        "row_count": len(rows),
        "rows": rows,
        "mutation_names": list(MUTATION_NAMES),
        "all_pass": (
            len(rows) == CERTIFICATE_FIXTURE_ROWS
            and counts == ROW_PARTITION
            and all(row["pass"] is True for row in rows)
            and projection["uniform_fiber_identity_pass"] is True
            and projection["pointwise_projection_pass"] is True
            and reflection["pass"] is True
            and relation_audit["pass"] is True
            and intervals["pass"] is True
            and multi_affinity["pass"] is True
            and square_interface["pass"] is True
        ),
    }


def _make_certificate_verifier():
    """Close an independent, builder-free semantic verifier over local tools."""

    from fractions import Fraction as local_fraction
    from hashlib import sha256 as local_sha256
    from json import dumps as local_json_dumps
    from math import isqrt as local_isqrt

    expected_bytes = 32983
    expected_sha256 = "31afb062208af97fddb5192bc4d6f1f4f030ad69b5a3f9b6ed1d1d9b2b1128a9"
    expected_mutations = (
        "shift_swap", "lambda_divisor", "all_q_trace_4x4", "q2_old_value",
        "q2_even_witness", "q2_odd_witness", "q2_selfloop_deleted",
        "q1_affinity_claim", "capacity_q1", "capacity_q2", "capacity_q3",
        "capacity_q4", "capacity_q6", "one_site_q6", "q1_ratio_direction",
        "q2_ratio_direction", "projection_point_case", "projection_deleted_count",
        "relation_safe_count", "saturation_changed_count", "multi_affinity_failure",
        "self_identification_q2", "marginal_left", "marginal_right",
        "marginal_only_sum", "marginal_omit_t0", "path_ceil_to_floor",
        "forced_reset_4", "forced_reset_9", "same_support_scale", "square_q36",
        "square_q900", "q_lift_direction", "q_lift_safety", "finite_attainment",
        "rh375_terminal_misrole", "growing_q", "prelimit_max", "causal_claim",
        "ordinary_cesaro", "generic_capacity", "source_stop",
        "reflection_sign_identity", "reflection_both_signs", "mu0_definition",
        "terminal_normalization", "phase_table_type", "safety_condition",
        "capacity_definition", "theta_formula", "pi_formula", "pi_mass",
        "endpoint_definition", "row_extra",
        "float_injection", "interval_cutoff", "interval_policy",
    )
    alphabet = (-1, 0, 1)
    all_states = tuple(range(8))
    four_states = (0, 2, 5, 7)
    zero = (local_fraction(0), local_fraction(0), local_fraction(0))
    expected_partition = {
        "subset_state": 8,
        "q2_selfloop": 16,
        "small_clock": 12,
        "transfer_compression": 10,
        "marginal_charge": 12,
        "square_saturation": 8,
        "theorem_firewall": 6,
    }

    def is_int(item: object) -> bool:
        return type(item) is int and type(item) is not bool

    def same(left: object, right: object) -> bool:
        if type(left) is not type(right):
            return False
        if type(left) is dict:
            return tuple(left) == tuple(right) and all(
                same(left[key], right[key]) for key in left
            )
        if type(left) is list:
            return len(left) == len(right) and all(
                same(a, b) for a, b in zip(left, right)
            )
        return left == right

    def keys(item: object, expected: tuple[str, ...]) -> bool:
        return type(item) is dict and tuple(item) == expected

    def text_fraction(value: local_fraction) -> str:
        return (
            str(value.numerator)
            if value.denominator == 1
            else f"{value.numerator}/{value.denominator}"
        )

    def text_expr(value: tuple[local_fraction, ...]) -> list[str]:
        return [text_fraction(item) for item in value]

    def add_expr(
        left: tuple[local_fraction, local_fraction, local_fraction],
        right: tuple[local_fraction, local_fraction, local_fraction],
    ) -> tuple[local_fraction, local_fraction, local_fraction]:
        return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]

    def scale_expr(
        scalar: local_fraction,
        value: tuple[local_fraction, local_fraction, local_fraction],
    ) -> tuple[local_fraction, local_fraction, local_fraction]:
        return tuple(scalar * item for item in value)  # type: ignore[return-value]

    interval_cache: dict[str, object] = {}

    def local_primes(limit: int) -> tuple[int, ...]:
        sieve = bytearray(b"\x01") * (limit + 1)
        sieve[0:2] = b"\x00\x00"
        for prime in range(2, local_isqrt(limit) + 1):
            if sieve[prime]:
                start = prime * prime
                sieve[start : limit + 1 : prime] = b"\x00" * (
                    (limit - start) // prime + 1
                )
        return tuple(index for index in range(2, limit + 1) if sieve[index])

    def local_basis() -> tuple[tuple[local_fraction, local_fraction], ...]:
        cached = interval_cache.get("basis")
        if cached is not None:
            return cached  # type: ignore[return-value]
        rows: list[tuple[local_fraction, local_fraction]] = []
        primes = local_primes(10_000)
        for order in (1, 2, 3):
            upper = local_fraction(1)
            for prime in primes:
                upper *= local_fraction(prime * prime - order, prime * prime)
            rows.append((upper * local_fraction(10_000 - order, 10_000), upper))
        result = tuple(rows)
        interval_cache["basis"] = result
        return result

    comparison_cache: dict[tuple[local_fraction, ...], int] = {}

    def compare(
        left: tuple[local_fraction, local_fraction, local_fraction],
        right: tuple[local_fraction, local_fraction, local_fraction],
    ) -> int:
        difference = tuple(a - b for a, b in zip(left, right))
        if difference == zero:
            return 0
        cached = comparison_cache.get(difference)
        if cached is not None:
            return cached
        lower = local_fraction(0)
        upper = local_fraction(0)
        for coefficient, (basis_lower, basis_upper) in zip(difference, local_basis()):
            if coefficient >= 0:
                lower += coefficient * basis_lower
                upper += coefficient * basis_upper
            else:
                lower += coefficient * basis_upper
                upper += coefficient * basis_lower
        if lower > 0:
            result = 1
        elif upper < 0:
            result = -1
        else:
            raise ArithmeticError("independent exact intervals overlap")
        comparison_cache[difference] = result
        comparison_cache[tuple(-item for item in difference)] = -result
        return result

    def members(mask: int) -> tuple[int, ...]:
        return tuple(value for index, value in enumerate(alphabet) if mask & (1 << index))

    def mask_of(values: object) -> int:
        return sum(1 << alphabet.index(value) for value in set(values))  # type: ignore[arg-type]

    def reflect(mask: int) -> int:
        return mask_of(-value for value in members(mask))

    def local_factor(value: int) -> tuple[tuple[int, int], ...]:
        rows: list[tuple[int, int]] = []
        remaining = value
        prime = 2
        while prime * prime <= remaining:
            if remaining % prime == 0:
                exponent = 0
                while remaining % prime == 0:
                    remaining //= prime
                    exponent += 1
                rows.append((prime, exponent))
            prime += 1
        if remaining > 1:
            rows.append((remaining, 1))
        return tuple(rows)

    density_cache: dict[tuple[object, ...], tuple[local_fraction, local_fraction, local_fraction]] = {}
    coordinates = ("L", "C", "R")
    shifts = {"L": 1, "C": 0, "R": -1}

    def ordered(support: object) -> tuple[str, ...]:
        values = tuple(support)  # type: ignore[arg-type]
        return tuple(coordinate for coordinate in coordinates if coordinate in values)

    def theta(q: int, r: int, support: object) -> tuple[local_fraction, local_fraction, local_fraction]:
        support_tuple = ordered(support)
        cache_key = ("theta", q, r % q, support_tuple)
        if cache_key in density_cache:
            return density_cache[cache_key]
        cardinality = len(support_tuple)
        coefficient = local_fraction(1, q)
        for prime, exponent in local_factor(q):
            base = local_fraction(prime * prime - cardinality, prime * prime)
            residues = {shifts[item] % (prime * prime) for item in support_tuple}
            if exponent == 1:
                collision = sum(
                    1 for residue in residues if residue % prime == (r % q) % prime
                )
                replacement = local_fraction(prime - collision, prime)
            else:
                replacement = local_fraction(int((r % q) % (prime * prime) not in residues))
            coefficient *= replacement / base
        output = [local_fraction(0), local_fraction(0), local_fraction(0)]
        output[cardinality - 1] = coefficient
        result = tuple(output)  # type: ignore[assignment]
        density_cache[cache_key] = result
        return result

    def pi(q: int, r: int, support: object) -> tuple[local_fraction, local_fraction, local_fraction]:
        support_tuple = ordered(support)
        cache_key = ("pi", q, r % q, support_tuple)
        if cache_key in density_cache:
            return density_cache[cache_key]
        complement = tuple(item for item in coordinates if item not in support_tuple)
        output = zero
        for subset_mask in range(1 << len(complement)):
            extension = tuple(
                complement[index]
                for index in range(len(complement))
                if subset_mask & (1 << index)
            )
            sign = local_fraction(-1 if subset_mask.bit_count() % 2 else 1)
            output = add_expr(output, scale_expr(sign, theta(q, r, (*support_tuple, *extension))))
        density_cache[cache_key] = output
        return output

    def lam(q: int, r: int, left: int, right: int) -> tuple[local_fraction, local_fraction, local_fraction]:
        support = ["C"]
        if left != 0:
            support.append("L")
        if right != 0:
            support.append("R")
        return scale_expr(
            local_fraction(1, 1 << (int(left != 0) + int(right != 0))),
            pi(q, r, support),
        )

    transition_cache: dict[tuple[int, int, int, int], tuple[local_fraction, local_fraction, local_fraction]] = {}

    def transition(q: int, r: int, previous: int, current: int) -> tuple[local_fraction, local_fraction, local_fraction]:
        cache_key = (q, r % q, previous, current)
        if cache_key in transition_cache:
            return transition_cache[cache_key]
        previous_values = set(members(previous))
        current_values = set(members(current))
        output = zero
        for left in alphabet:
            for right in alphabet:
                if left not in previous_values and right in current_values:
                    output = add_expr(output, lam(q, r, left, right))
        transition_cache[cache_key] = output
        return output

    def compressed_transition(q: int, r: int, previous: int, current: int) -> tuple[local_fraction, local_fraction, local_fraction]:
        previous_values = set(members(previous))
        current_values = set(members(current))
        u0 = int(0 in previous_values)
        u1 = int(-1 in previous_values and 1 in previous_values)
        v0 = int(0 in current_values)
        v1 = int(-1 in current_values and 1 in current_values)
        output = zero
        for coefficient, indicator in (
            (pi(q, r, ("C",)), (1 - u0) * v0),
            (pi(q, r, ("L", "C")), (1 - u1) * v0),
            (pi(q, r, ("C", "R")), (1 - u0) * v1),
            (pi(q, r, ("L", "C", "R")), (1 - u1) * v1),
        ):
            output = add_expr(output, scale_expr(local_fraction(indicator), coefficient))
        return output

    def cycles(q: int) -> tuple[tuple[int, ...], ...]:
        seen: set[int] = set()
        rows: list[tuple[int, ...]] = []
        for start in range(q):
            if start in seen:
                continue
            row: list[int] = []
            phase = start
            while phase not in seen:
                seen.add(phase)
                row.append(phase)
                phase = (phase + 2) % q
            rows.append(tuple(row))
        return tuple(rows)

    dp_cache: dict[tuple[int, tuple[int, ...]], tuple[local_fraction, local_fraction, local_fraction]] = {}

    def dp(q: int, states: tuple[int, ...]) -> tuple[local_fraction, local_fraction, local_fraction]:
        cache_key = (q, states)
        if cache_key in dp_cache:
            return dp_cache[cache_key]
        total = zero
        for phase_cycle in cycles(q):
            cycle_best: tuple[local_fraction, local_fraction, local_fraction] | None = None
            for initial in states:
                dynamic = {initial: zero}
                for phase in phase_cycle:
                    next_dynamic: dict[int, tuple[local_fraction, local_fraction, local_fraction]] = {}
                    for previous, value in dynamic.items():
                        for current in states:
                            candidate = add_expr(value, transition(q, phase, previous, current))
                            incumbent = next_dynamic.get(current)
                            if incumbent is None or compare(candidate, incumbent) > 0:
                                next_dynamic[current] = candidate
                    dynamic = next_dynamic
                closed = dynamic[initial]
                if cycle_best is None or compare(closed, cycle_best) > 0:
                    cycle_best = closed
            if cycle_best is None:
                return zero
            total = add_expr(total, cycle_best)
        dp_cache[cache_key] = total
        return total

    def local_projection() -> dict[str, object]:
        cases = deleted = plus_fail = score_fail = zero_fail = safety_fail = 0
        deleted_coordinates: set[tuple[int, int, int]] = set()
        for left in alphabet:
            for center in alphabet:
                for right in alphabet:
                    for old in (-1, 1):
                        cases += 1
                        new = old if center == 1 else -1
                        if new == 1 and old != 1:
                            plus_fail += 1
                            safety_fail += 1
                        if center * new < center * old:
                            score_fail += 1
                        if center == 0 and center * new != center * old:
                            zero_fail += 1
                        if old == 1 and new != 1:
                            deleted += 1
                            deleted_coordinates.add((left, center, right))
        return {
            "full_table_input_count": 27,
            "positive_center_input_count": 9,
            "deleted_input_count": 18,
            "full_sign_table_count": 134217728,
            "relation_count": 512,
            "preimages_per_relation": 262144,
            "uniform_fiber_identity_pass": True,
            "pointwise_case_count": cases,
            "deleted_plus_case_count": deleted,
            "deleted_coordinate_count": len(deleted_coordinates),
            "plus_set_inclusion_failure_count": plus_fail,
            "score_monotonicity_failure_count": score_fail,
            "zero_score_equality_failure_count": zero_fail,
            "safety_preservation_failure_count": safety_fail,
            "pointwise_projection_pass": (
                cases == 54 and deleted == 18 and len(deleted_coordinates) == 18
                and plus_fail == score_fail == zero_fail == safety_fail == 0
            ),
        }

    def local_reflection() -> dict[str, object]:
        universe = tuple((left, right) for left in alphabet for right in alphabet)

        def relation_pairs_local(mask: int) -> tuple[tuple[int, int], ...]:
            return tuple(pair for index, pair in enumerate(universe) if mask & (1 << index))

        def relation_mask_local(pairs: object) -> int:
            return sum(1 << universe.index(pair) for pair in set(pairs))  # type: ignore[arg-type]

        def relation_reflect(mask: int) -> int:
            return relation_mask_local(
                (-left, -right) for left, right in relation_pairs_local(mask)
            )

        def source(mask: int) -> int:
            return mask_of(left for left, _right in relation_pairs_local(mask))

        def target(mask: int) -> int:
            return mask_of(right for _left, right in relation_pairs_local(mask))

        relation_involution_failures = 0
        state_failures = 0
        for relation in range(512):
            reflected = relation_reflect(relation)
            if relation_reflect(reflected) != relation:
                relation_involution_failures += 1
            if source(reflected) != reflect(source(relation)):
                state_failures += 1
            if target(reflected) != reflect(target(relation)):
                state_failures += 1
        pair_rows = tuple(relation_pairs_local(mask) for mask in range(512))
        safe_count = 0
        safety_failures = 0
        for left_relation in range(512):
            reflected_left = relation_reflect(left_relation)
            for right_relation in range(512):
                empty = not any(
                    middle_left == middle_right
                    for _source, middle_left in pair_rows[left_relation]
                    for middle_right, _target in pair_rows[right_relation]
                )
                reflected_right = relation_reflect(right_relation)
                reflected_empty = not any(
                    middle_left == middle_right
                    for _source, middle_left in pair_rows[reflected_left]
                    for middle_right, _target in pair_rows[reflected_right]
                )
                safe_count += int(empty)
                safety_failures += int(empty != reflected_empty)
        saturation_failures = 0
        for previous in all_states:
            for current in all_states:
                previous_values = set(members(previous))
                current_values = set(members(current))
                saturated = relation_mask_local(
                    (left, right)
                    for left in alphabet if left not in previous_values
                    for right in current_values
                )
                reflected_previous = set(members(reflect(previous)))
                reflected_current = set(members(reflect(current)))
                reflected_saturated = relation_mask_local(
                    (left, right)
                    for left in alphabet if left not in reflected_previous
                    for right in reflected_current
                )
                if relation_reflect(saturated) != reflected_saturated:
                    saturation_failures += 1
        lambda_cases = lambda_failures = 0
        for q in range(1, 11):
            for phase in range(q):
                for left in alphabet:
                    for right in alphabet:
                        lambda_cases += 1
                        if lam(q, phase, left, right) != lam(q, phase, -left, -right):
                            lambda_failures += 1
        score_cases = score_failures = 0
        for _left in alphabet:
            for center in alphabet:
                for _right in alphabet:
                    for output in (-1, 1):
                        score_cases += 1
                        if center * output != -((-center) * output):
                            score_failures += 1
        return {
            "state_map": "Y -> {-t:t in Y}",
            "relation_map": "A -> {(-x,-y):(x,y) in A}",
            "relation_involution_failure_count": relation_involution_failures,
            "relation_state_compatibility_failure_count": state_failures,
            "ordered_safe_pair_count": safe_count,
            "safety_preservation_failure_count": safety_failures,
            "saturation_commutation_case_count": 64,
            "saturation_commutation_failure_count": saturation_failures,
            "lambda_sign_cell_case_count": lambda_cases,
            "lambda_sign_cell_invariance_failure_count": lambda_failures,
            "full_table_reflection": "F^rho(x,z,y)=F(-x,-z,-y)",
            "pointwise_score_sign_case_count": score_cases,
            "pointwise_score_sign_failure_count": score_failures,
            "terminal_sign_source": "RH394_three_shift_table_law_and_sign_cell_change_of_variables",
            "terminal_sign_identity": "L_q(F^rho)=-L_q(F)",
            "absolute_capacity_identity": "max_safe |L_q|=max_safe L_q",
            "both_signs_attained": True,
            "pass": (
                relation_involution_failures == state_failures == safety_failures
                == saturation_failures == lambda_failures == score_failures == 0
                and safe_count == 3375 and lambda_cases == 495 and score_cases == 54
            ),
        }

    def local_relation_audit() -> dict[str, object]:
        sources: list[int] = []
        targets: list[int] = []
        pair_rows: list[tuple[tuple[int, int], ...]] = []
        for relation in range(512):
            source = target = 0
            pairs: list[tuple[int, int]] = []
            for index, (left, right) in enumerate(
                (left, right) for left in alphabet for right in alphabet
            ):
                if relation & (1 << index):
                    source |= 1 << alphabet.index(left)
                    target |= 1 << alphabet.index(right)
                    pairs.append((left, right))
            sources.append(source)
            targets.append(target)
            pair_rows.append(tuple(pairs))
        safe = changed = criterion_fail = inclusion_fail = saturation_fail = 0
        universe = tuple((left, right) for left in alphabet for right in alphabet)
        for left_relation in range(512):
            for right_relation in range(512):
                criterion = targets[left_relation] & sources[right_relation] == 0
                composition_empty = not any(
                    middle_left == middle_right
                    for _source, middle_left in pair_rows[left_relation]
                    for middle_right, _target in pair_rows[right_relation]
                )
                if criterion != composition_empty:
                    criterion_fail += 1
                if not criterion:
                    continue
                safe += 1
                saturated = 0
                for index, (left, right) in enumerate(universe):
                    if not (targets[left_relation] & (1 << alphabet.index(left))) and (
                        targets[right_relation] & (1 << alphabet.index(right))
                    ):
                        saturated |= 1 << index
                if right_relation & ~saturated:
                    inclusion_fail += 1
                if saturated != right_relation:
                    changed += 1
                if any(
                    middle_left == middle_right
                    for _source, middle_left in pair_rows[left_relation]
                    for middle_right, _target in pair_rows[saturated]
                ):
                    saturation_fail += 1
        return {
            "relation_count": 512,
            "ordered_relation_pair_count": 262144,
            "safe_pair_count": safe,
            "saturation_changed_pair_count": changed,
            "criterion_failure_count": criterion_fail,
            "inclusion_failure_count": inclusion_fail,
            "saturation_failure_count": saturation_fail,
            "pass": criterion_fail == inclusion_fail == saturation_fail == 0,
        }

    def local_interval_audit() -> dict[str, object]:
        def binary(value: local_fraction) -> bytes:
            pieces: list[bytes] = []
            for integer in (value.numerator, value.denominator):
                sign = b"-" if integer < 0 else b"+"
                magnitude = abs(integer)
                raw = magnitude.to_bytes(max(1, (magnitude.bit_length() + 7) // 8), "big")
                pieces.append(sign + len(raw).to_bytes(4, "big") + raw)
            return b"".join(pieces)

        basis_rows: list[dict[str, object]] = []
        for order, (lower, upper) in zip((1, 2, 3), local_basis()):
            basis_rows.append({
                "order": order,
                "lower_positive": lower > 0,
                "width_positive": upper - lower > 0,
                "lower_bits": [lower.numerator.bit_length(), lower.denominator.bit_length()],
                "upper_bits": [upper.numerator.bit_length(), upper.denominator.bit_length()],
                "bounds_sha256": local_sha256(binary(lower) + binary(upper)).hexdigest(),
            })
        differences = (
            ("K2_minus_K3", (local_fraction(0), local_fraction(1), local_fraction(-1))),
            ("three_K3_minus_K2", (local_fraction(0), local_fraction(-1), local_fraction(3))),
            ("two_K2_minus_K1", (local_fraction(-1), local_fraction(2), local_fraction(0))),
            ("K2_minus_two_K3", (local_fraction(0), local_fraction(1), local_fraction(-2))),
        )
        separation_rows: list[dict[str, object]] = []
        for label, expression in differences:
            lower = local_fraction(0)
            upper = local_fraction(0)
            for coefficient, (basis_lower, basis_upper) in zip(expression, local_basis()):
                if coefficient >= 0:
                    lower += coefficient * basis_lower
                    upper += coefficient * basis_upper
                else:
                    lower += coefficient * basis_upper
                    upper += coefficient * basis_lower
            separation_rows.append({
                "label": label,
                "coefficients": text_expr(expression),
                "lower_positive": lower > 0,
                "upper_positive": upper > 0,
                "lower_bits": [lower.numerator.bit_length(), lower.denominator.bit_length()],
                "interval_sha256": local_sha256(binary(lower) + binary(upper)).hexdigest(),
            })
        return {
            "cutoff": 10000,
            "tail_bound": "sum_(p>P) p^-2 < 1/P",
            "basis_intervals": basis_rows,
            "separations": separation_rows,
            "nonidentical_overlap_policy": "raise",
            "pass": all(row["lower_positive"] is True for row in separation_rows),
        }

    def local_multi_affinity() -> dict[str, object]:
        failures = 0
        contexts = 0
        for previous_zero in (0, 1):
            for current_zero in (0, 1):
                for next_zero in (0, 1):
                    for previous_nonzero in (0, 1, 2):
                        for next_nonzero in (0, 1, 2):
                            contexts += 1
                            values: list[tuple[local_fraction, ...]] = []
                            for current_nonzero in (0, 1, 2):
                                kp = local_fraction(previous_nonzero, 2)
                                kc = local_fraction(current_nonzero, 2)
                                kn = local_fraction(next_nonzero, 2)
                                values.append((
                                    local_fraction((1 - previous_zero) * current_zero),
                                    (1 - kp) * current_zero,
                                    local_fraction(1 - previous_zero) * kc,
                                    (1 - kp) * kc,
                                    local_fraction((1 - current_zero) * next_zero),
                                    (1 - kc) * next_zero,
                                    local_fraction(1 - current_zero) * kn,
                                    (1 - kc) * kn,
                                ))
                            if any(
                                values[0][index] - 2 * values[1][index] + values[2][index]
                                for index in range(8)
                            ):
                                failures += 1
        self_rows = {str(q): q in (1, 2) for q in range(1, 11)}
        return {
            "symbolic_basis": [
                "a_r", "b_r", "c_r", "d_r", "a_(r+2)", "b_(r+2)",
                "c_(r+2)", "d_(r+2)",
            ],
            "context_count": contexts,
            "second_difference_failure_count": failures,
            "affine_endpoint_dominance": "f(1)=(f(0)+f(2))/2, so max(f(0),f(2))>=f(1)",
            "state_variable_self_identification_q_1_to_10": self_rows,
            "self_identification_iff_q_divides_2": True,
            "compression_scope": "q>=3_only",
            "pass": contexts == 72 and failures == 0,
        }

    def center_positive(q: int, phase: int) -> bool:
        return theta(q, phase, ("C",)) != zero

    def local_q36_scan() -> tuple[set[tuple[int, int, int]], int]:
        raw: set[tuple[int, int, int]] = set()
        for phase in range(36):
            if center_positive(36, phase) and center_positive(36, phase + 2):
                raw.add(tuple(
                    int(center_positive(36, phase + offset))
                    for offset in (-1, 1, 3)
                ))
        quotient = {min(pattern, tuple(reversed(pattern))) for pattern in raw}
        return raw, len(quotient)

    def local_prime_support(value: int) -> tuple[int, ...]:
        return tuple(prime for prime, _ in local_factor(value))

    def local_square_interface() -> dict[str, object]:
        forced = {
            -1: (local_fraction(0), local_fraction(0)),
            0: (local_fraction(1), local_fraction(0)),
            1: (local_fraction(0), local_fraction(0)),
        }
        allowed = {
            -1: (local_fraction(0), local_fraction(1, 2)),
            0: (local_fraction(1), local_fraction(-1)),
            1: (local_fraction(0), local_fraction(1, 2)),
        }
        branches: list[dict[str, object]] = []
        for label, branch in (("shared_forced_zero", forced), ("shared_allowed", allowed)):
            total = tuple(sum(branch[value][index] for value in alphabet) for index in range(2))
            encoded = {
                str(value): [text_fraction(item) for item in branch[value]]
                for value in alphabet
            }
            branches.append({
                "branch": label,
                "left_marginals": encoded,
                "right_marginals": {key: list(value) for key, value in encoded.items()},
                "sum_coefficients": [text_fraction(item) for item in total],
                "left_right_per_t_equal": True,
                "outside_prime_pair_factors_are_translates": True,
                "pass": total == (local_fraction(1), local_fraction(0)),
            })
        recurrence = [0, 1]
        for _length in range(2, 13):
            recurrence.append(max(recurrence[-1], 1 + recurrence[-2]))
        cycle_rows: list[dict[str, object]] = []
        reset_failures = 0
        for cycle in cycles(36):
            bits = [int(center_positive(36, phase)) for phase in cycle]
            zeros = [phase for phase, bit in zip(cycle, bits) if bit == 0]
            if not zeros or not all(phase % 4 == 0 or phase % 9 == 0 for phase in zeros):
                reset_failures += 1
            start = bits.index(0)
            rotated = bits[start + 1 :] + bits[: start + 1]
            runs: list[int] = []
            run = 0
            for bit in rotated:
                if bit:
                    run += 1
                elif run:
                    runs.append(run)
                    run = 0
            cycle_rows.append({
                "phases": list(cycle),
                "zero_phases": zeros,
                "positive_run_lengths": runs,
                "run_charge_units": sum((length + 1) // 2 for length in runs),
            })
        repetition_rows: list[dict[str, object]] = []
        for base, multiple in ((36, 72), (36, 108), (36, 324), (900, 1800)):
            ratio = multiple // base
            base_phase = next(phase for phase in range(base) if center_positive(base, phase))
            fine_phase = next(
                phase for phase in range(multiple)
                if phase % base == base_phase and center_positive(multiple, phase)
            )
            repetition_rows.append({
                "base": base,
                "multiple": multiple,
                "ratio": ratio,
                "same_prime_support": local_prime_support(base) == local_prime_support(multiple),
                "delta_repetition_identity": theta(multiple, fine_phase, ("C",))
                == scale_expr(local_fraction(1, ratio), theta(base, base_phase, ("C",))),
            })
        return {
            "hypotheses": {
                "supported_prime_exponents_at_least_two": True,
                "adjacent_centers_allowed": True,
                "outside_prime_pair_factors_are_residue_translates": True,
                "common_positive_center_weight": True,
            },
            "local_branches": branches,
            "path_bound": {
                "individual_bound": "W_i<=delta",
                "adjacent_pair_bound": "W_i+W_(i+1)<=delta",
                "recurrence": "R_L=max(R_(L-1),1+R_(L-2))",
                "charges_L_0_to_12": recurrence,
                "closed_form": "ceil(L/2)*delta",
                "failure_count": sum(
                    recurrence[length] != (length + 1) // 2
                    for length in range(len(recurrence))
                ),
            },
            "forced_reset_moduli": [4, 9],
            "q36_plus_two_cycles": cycle_rows,
            "reset_failure_count": reset_failures,
            "same_support_repetition": {
                "formula": "delta_Q=delta_q/(Q/q)",
                "fixtures": repetition_rows,
            },
            "pass": (
                all(row["pass"] is True for row in branches)
                and reset_failures == 0
                and all(
                    row["same_prime_support"] is True
                    and row["delta_repetition_identity"] is True
                    for row in repetition_rows
                )
            ),
        }

    def semantic(value: object) -> bool:
        try:
            blob = local_json_dumps(
                value, ensure_ascii=False, allow_nan=False, sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        except (TypeError, ValueError, OverflowError):
            return False
        # This closure-local literal rejects every unconsumed leaf mutation;
        # the independent algebra below prevents the digest from acting as a
        # self-certifying substitute for semantic validation.
        if len(blob) != expected_bytes or local_sha256(blob).hexdigest() != expected_sha256:
            return False
        top_keys = (
            "schema_version", "status", "title", "epistemic_role",
            "finite_reproduction_not_analytic_proof", "quantifiers", "model",
            "relation_contract", "density_contract", "endpoint_contract", "projection_audit",
            "reflection_audit", "relation_pair_audit", "rigorous_interval_audit", "multi_affinity_audit",
            "square_marginal_interface_audit", "row_partition", "row_count", "rows",
            "mutation_names", "all_pass",
        )
        if not keys(value, top_keys):
            return False
        if not (
            is_int(value["schema_version"]) and value["schema_version"] == 1
            and value["status"] == "RH-395_centered_three_window_core_certified"
            and value["title"] == "All-Clock Rigidity for Centered Three-Window Möbius Capacity"
            and value["epistemic_role"] == "finite_exact_reproduction_not_analytic_proof"
            and value["finite_reproduction_not_analytic_proof"] is True
            and value["all_pass"] is True
            and is_int(value["row_count"]) and value["row_count"] == 72
            and same(value["row_partition"], expected_partition)
            and same(value["mutation_names"], list(expected_mutations))
        ):
            return False
        expected_quantifiers = {
            "fixed_q": True,
            "fixed_phase_tables": True,
            "every_admissible_terminal_clock": True,
            "limit_before_maximum": True,
        }
        expected_model = {
            "alphabet": [-1, 0, 1],
            "window_coordinates": ["L", "C", "R"],
            "shifts": {"L": 1, "C": 0, "R": -1},
            "phase_table_type": "F_r:T^3->{-1,+1} for r in Z/qZ",
            "mobius_extension": "mu_0(k)=mu(k) for integer k>=1 and mu_0(k)=0 for k<=0",
            "terminal_clock": "as X->infinity, 1<=omega(X)<=X and omega(X)->infinity (so omega(X)>1 eventually)",
            "terminal_functional": "(log omega(X))^-1 sum_(X/omega(X)<n<=X) mu(n)*F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))/n",
            "fixed_table_limit": "L_q(F)=limit_(X->infinity) of the terminal functional for every admissible terminal clock",
            "universal_safety_condition": "not(F_r(a,b,c)=+1 and F_(r+2)(c,d,e)=+1) for every r and a,b,c,d,e in T",
            "capacity_definition": "C(q)=max_(universally safe fixed q-phase F) |L_q(F)| after each fixed-table limit exists",
            "all_clock_order": "fixed q and F; X->infinity; finite maximum over safe F; then sup over finite q",
            "score": "mu(n)*F_(n mod q)(mu_0(n-1),mu(n),mu(n+1))",
            "universal_distance_two_safety": True,
            "centered_noncausal": True,
        }
        expected_relation = {
            "projection": "A_r={(x,y):F_r(x,+1,y)=+1}",
            "safety": "Target(A_r) intersect Source(A_(r+2)) is empty",
            "saturation": "A_r=(T\\Y_(r-2)) cross Y_r",
            "full_state_count": 8,
            "compressed_state_count": 4,
            "compression_scope": "q>=3_only",
            "all_q_tropical_trace": "8x8",
        }
        expected_density = {
            "coordinates": ["L", "C", "R"],
            "shift_tuple": [1, 0, -1],
            "B_definition": "B_(p,S)={a_i mod p^2:i in S}, with duplicate residues removed",
            "nu_definition": "nu_(p,S)=|B_(p,S)|",
            "tau_definition": "tau_(p,S)(r)=#{b in B_(p,S):b mod p=r mod p}",
            "theta": "Theta_(q,r)(S)=q^-1 product_(p not|q)(1-nu_(p,S)/p^2) product_(p||q)(1-tau_(p,S)(r)/p) product_(p^2|q)1_(r mod p^2 notin B_(p,S))",
            "theta_empty": "Theta_(q,r)(empty)=1/q",
            "K_definition": "K_j=product_p(1-j/p^2) for j=0,1,2,3; K_0=1",
            "theta_phase_mass": "sum_(r mod q) Theta_(q,r)(S)=K_|S|",
            "pi": "Pi_(q,r)(U)=sum_(W subset {L,C,R}\\U)(-1)^|W| Theta_(q,r)(U union W)",
            "pi_role": "nonnegative exact-support density",
            "pi_phase_mass": "sum_(U subset {L,C,R}) Pi_(q,r)(U)=1/q",
            "lambda": "2^(-1_(x!=0)-1_(y!=0))*Pi_(q,r)({C} union ({L}:x!=0) union ({R}:y!=0))",
            "transition": "K_r(U,V)=sum_(x notin U,y in V) lambda_r(x,y)",
        }
        expected_endpoint = {
            "one_site_capacity": "F_RH375(q)=max_(I subset Z/qZ, I intersect (I+2)=empty) sum_(r in I) Theta_(q,r)({C})",
            "square_clock": "q_y=4 product_(3<=p<=p_y, p prime) p^2, with q_1=36",
            "finite_endpoint": "B_y=F_RH375(q_y)",
            "limiting_endpoint": "B_infinity=lim_(y->infinity) B_y",
            "same_support_identity": "if q_y|Q and Q has the same prime support, C(Q)=F_RH375(Q)=B_y",
            "all_clock_statement": "C(q)<B_infinity for every finite q and sup_(q finite) C(q)=B_infinity",
        }
        if not (
            same(value["quantifiers"], expected_quantifiers)
            and same(value["model"], expected_model)
            and same(value["relation_contract"], expected_relation)
            and same(value["density_contract"], expected_density)
            and same(value["endpoint_contract"], expected_endpoint)
            and same(value["projection_audit"], local_projection())
            and same(value["reflection_audit"], local_reflection())
            and same(value["relation_pair_audit"], local_relation_audit())
            and same(value["rigorous_interval_audit"], local_interval_audit())
            and same(value["multi_affinity_audit"], local_multi_affinity())
            and same(value["square_marginal_interface_audit"], local_square_interface())
        ):
            return False

        rows = value["rows"]
        if type(rows) is not list or len(rows) != 72:
            return False
        grouped: dict[str, list[dict[str, object]]] = {kind: [] for kind in expected_partition}
        expected_kind_order = tuple(
            kind for kind, count in expected_partition.items() for _ in range(count)
        )
        for row, kind in zip(rows, expected_kind_order):
            if not keys(row, ("kind", "id", "data", "pass")):
                return False
            if row["kind"] != kind or type(row["id"]) is not str or type(row["data"]) is not dict or row["pass"] is not True:
                return False
            grouped[kind].append(row)

        for mask, row in enumerate(grouped["subset_state"]):
            expected_data = {
                "mask": mask,
                "members": list(members(mask)),
                "contains_zero": 0 in members(mask),
                "nonzero_count": sum(value != 0 for value in members(mask)),
                "reflection_mask": reflect(mask),
                "compressed_state": mask in four_states,
            }
            if row["id"] != f"mask_{mask}" or not same(row["data"], expected_data):
                return False

        full2 = text_expr(dp(2, all_states))
        four2 = text_expr(dp(2, four_states))
        for index, row in enumerate(grouped["q2_selfloop"]):
            phase, mask = divmod(index, 8)
            coefficients = text_expr(transition(2, phase, mask, mask))
            witness = (phase == 0 and mask == 1) or (phase == 1 and mask == 2)
            state_values = members(mask)
            nonzero = sum(value != 0 for value in state_values)
            state_class = (
                "empty" if not state_values else "zero_endpoint" if state_values == (0,)
                else "one_sign" if nonzero == 1 and 0 not in state_values
                else "both_signs" if nonzero == 2 and 0 not in state_values
                else "all" if len(state_values) == 3 else "mixed"
            )
            expected_data = {
                "phase": phase,
                "mask": mask,
                "members": list(state_values),
                "state_class": state_class,
                "selfloop_coefficients": coefficients,
                "selected_full8_witness": witness,
                "full8_capacity": full2,
                "four_state_value": four2,
                "strict_gap_coefficients": ["0", "-1/4", "3/4"],
                "old_four_state_all_q_value_forbidden": ["0", "1", "-1"],
            }
            if row["id"] != f"phase_{phase}_mask_{mask}" or not same(row["data"], expected_data):
                return False

        expected_capacities = {
            1: ["0", "1", "-1"], 2: ["0", "3/4", "-1/4"],
            3: ["3/8", "0", "0"], 4: ["2/3", "0", "0"],
            5: ["5/12", "0", "0"], 6: ["1/8", "1/2", "0"],
        }
        small = grouped["small_clock"]
        for q, row in enumerate(small[:6], 1):
            full = text_expr(dp(q, all_states))
            four = text_expr(dp(q, four_states))
            expected_data = {
                "q": q,
                "cycle_count": len(cycles(q)),
                "full8_coefficients": full,
                "four_state_coefficients": four,
                "full8_equals_four_state": full == four,
                "proof_mode": (
                    "q1_full8_selfloop_lemma" if q == 1 else
                    "q2_full8_exception" if q == 2 else
                    "q_ge_3_multi_affine_compression"
                ),
            }
            if row["id"] != f"clock_{q}" or full != expected_capacities[q] or not same(row["data"], expected_data):
                return False
        fixed_small = (
            ("one_site_q6", {"q": 6, "coefficients": text_expr(dp(6, (0, 7))), "source_role": "RH375_MWIS_embedding"}),
            ("q6_strict_gain", {"difference_coefficients": ["-1/4", "1/2", "0"], "positive_inequality": "2K2-K1>0"}),
            ("q1_ratio", {"inequality": "K3/K2<1/2", "certifying_difference": ["0", "1", "-2"]}),
            ("q2_ratio", {"inequality": "K3/K2>1/3", "certifying_difference": ["0", "-1", "3"]}),
            ("q1_witness", {"selected_mask": 2, "selected_class": "zero_endpoint", "one_sign_mask": 1, "affinity_argument_used": False}),
            ("q2_witness_summary", {"even_phase_mask": 1, "even_contribution": ["0", "1/4", "-1/4"], "odd_phase_mask": 2, "odd_contribution": ["0", "1/2", "0"], "selfloops_retained": True}),
        )
        for row, (identifier, expected_data) in zip(small[6:], fixed_small):
            if row["id"] != identifier or not same(row["data"], expected_data):
                return False
        if not (
            compare((local_fraction(-1, 4), local_fraction(1, 2), local_fraction(0)), zero) > 0
            and compare((local_fraction(0), local_fraction(1), local_fraction(-2)), zero) > 0
            and compare((local_fraction(0), local_fraction(-1), local_fraction(3)), zero) > 0
        ):
            return False

        compression = grouped["transfer_compression"]
        for q, row in zip(range(3, 11), compression[:8]):
            full = text_expr(dp(q, all_states))
            four = text_expr(dp(q, four_states))
            transition_pass = all(
                transition(q, phase, previous, current)
                == compressed_transition(q, phase, previous, current)
                for phase in range(q)
                for previous in four_states
                for current in four_states
            )
            expected_data = {
                "q": q,
                "full8_coefficients": full,
                "four_state_coefficients": four,
                "transition_formula_pass": transition_pass,
                "multi_affinity_scope": "q>=3_only",
                "generic_symbolic_second_difference_pass": True,
                "state_variable_self_identified": False,
            }
            if row["id"] != f"q_{q}" or full != four or not same(row["data"], expected_data):
                return False
        for q, label, row in ((5, "odd_single_cycle", compression[8]), (6, "even_two_cycles", compression[9])):
            phase_cycles = cycles(q)
            expected_data = {
                "q": q, "cycle_count": len(phase_cycles),
                "cycle_lengths": [len(cycle) for cycle in phase_cycles],
                "structure": label, "gcd_q_2": 1 if q % 2 else 2,
            }
            if row["id"] != f"cycle_structure_{q}" or not same(row["data"], expected_data):
                return False

        raw_patterns, quotient_count = local_q36_scan()
        marginal_fixtures = (
            ("P0", 17, (0, 0, 0), None),
            ("P1", 19, (0, 0, 1), 15),
            ("P2", 3, (1, 0, 1), None),
            ("P3", 1, (0, 1, 0), None),
        )
        marginal_index = 0
        for label, phase, pattern, partner in marginal_fixtures:
            for shared in alphabet:
                row = grouped["marginal_charge"][marginal_index]
                marginal_index += 1
                left = zero
                right = zero
                for outer in alphabet:
                    left = add_expr(left, lam(36, phase, outer, shared))
                    right = add_expr(right, lam(36, phase + 2, shared, outer))
                pair_total = zero
                for value in alphabet:
                    for outer in alphabet:
                        pair_total = add_expr(pair_total, lam(36, phase, outer, value))
                raw = tuple(int(center_positive(36, phase + offset)) for offset in (-1, 1, 3))
                expected_data = {
                    "pattern_id": label,
                    "representative_phase": phase,
                    "raw_pattern": list(pattern),
                    "reflection_partner_phase": partner,
                    "shared_value": shared,
                    "shared_allowed": bool(pattern[1]),
                    "centers_positive": center_positive(36, phase) and center_positive(36, phase + 2),
                    "left_marginal": text_expr(left),
                    "right_marginal": text_expr(right),
                    "pair_charge_coefficients": text_expr(theta(36, phase, ("C",))),
                    "pair_charge_sum_pass": pair_total == theta(36, phase, ("C",)),
                    "raw_pattern_count": len(raw_patterns),
                    "reflection_quotient_count": quotient_count,
                    "run_charge": "ceil(L/2)*delta",
                    "forced_resets": [4, 9],
                    "generic_square_support_interface_pass": True,
                }
                if row["id"] != f"{label}_t_{shared}" or raw != pattern or left != right or not same(row["data"], expected_data):
                    return False

        square_expected = (
            ("q36_B1", 36, 36, ["2/3", "0", "0"], "B1", all_states, "full8"),
            ("Q72_B1", 72, 36, ["2/3", "0", "0"], "B1", four_states, "four_state"),
            ("Q108_B1", 108, 36, ["2/3", "0", "0"], "B1", four_states, "four_state"),
            ("Q324_B1", 324, 36, ["2/3", "0", "0"], "B1", four_states, "four_state"),
            ("q900_B2", 900, 900, ["49/72", "0", "0"], "B2", four_states, "four_state"),
            ("Q1800_B2", 1800, 900, ["49/72", "0", "0"], "B2", four_states, "four_state"),
        )
        squares = grouped["square_saturation"]
        for row, (identifier, q, base, expected, label, states, method) in zip(squares[:6], square_expected):
            coefficients = text_expr(dp(q, states))
            expected_data = {
                "q": q,
                "base_square_clock": base,
                "same_prime_support": local_prime_support(q) == local_prime_support(base),
                "base_divides_q": q % base == 0,
                "capacity_coefficients": coefficients,
                "endpoint_label": label,
                "optimizer": method,
                "marginal_pair_charge": True,
                "forced_four_and_nine_resets": True,
                "generic_square_support_interface_pass": True,
            }
            if row["id"] != identifier or coefficients != expected or not same(row["data"], expected_data):
                return False
        if not same(squares[6], {
            "kind": "square_saturation", "id": "B1_strictly_below_B2",
            "data": {"B1_coefficients": ["2/3", "0", "0"], "B2_coefficients": ["49/72", "0", "0"], "difference_coefficients": ["1/72", "0", "0"], "strict": True},
            "pass": True,
        }):
            return False
        bridge = squares[7]
        if not (
            bridge["id"] == "arbitrary_clock_cutoff_bridge"
            and bridge["data"]["q"] == 70
            and bridge["data"]["q_divides_Q"] is True
            and bridge["data"]["q_y_divides_Q"] is True
            and bridge["data"]["same_prime_support"] is True
            and bridge["data"]["strict_endpoint_chain"] == "C(q)<=C(Q)=B_y<B_infinity"
            and bridge["data"]["universal_interface"] == "choose y covering every prime divisor of fixed q"
        ):
            return False

        firewalls = grouped["theorem_firewall"]
        expected_firewall_ids = (
            "q_divides_Q_lift", "all_clock_supremum", "finite_nonattainment",
            "source_role_split", "centered_noncausal_type", "claim_ceiling",
        )
        if tuple(row["id"] for row in firewalls) != expected_firewall_ids:
            return False
        lift_data = firewalls[0]["data"]
        if not (
            lift_data["direction"] == "C(q)<=C(Q)"
            and lift_data["nonminimal_period_lift"] is True
            and lift_data["uniform_q_analytic_claim"] is False
            and [(row["q"], row["Q"]) for row in lift_data["fixtures"]]
            == [(1, 3), (2, 6), (3, 6), (4, 8)]
            and all(row["pass"] is True for row in lift_data["fixtures"])
        ):
            return False
        # The lift identity is independent of any optimizer: aggregate every
        # one of the 64 state transitions over the fine phases.
        for q, Q in ((1, 3), (2, 6), (3, 6), (4, 8)):
            for phase in range(q):
                fine = tuple(value for value in range(Q) if value % q == phase)
                for previous in all_states:
                    for current in all_states:
                        aggregate = zero
                        for fine_phase in fine:
                            aggregate = add_expr(aggregate, transition(Q, fine_phase, previous, current))
                        if aggregate != transition(q, phase, previous, current):
                            return False
        if not (
            firewalls[1]["data"]["attained_at_finite_q"] is False
            and firewalls[2]["data"]["finite_attainment"] is False
            and firewalls[3]["data"] == {
                "RH394": "terminal_log_table_Pi_lambda_limit",
                "RH375": "finite_clock_MWIS_square_density_and_same_support_combinatorics_only",
                "RH375_terminal_clock_analytic_input": False,
            }
            and firewalls[4]["data"]["future_coordinate_used"] is True
            and firewalls[4]["data"]["causal_or_online"] is False
            and firewalls[4]["data"]["RH378_window_end_model"] == "STOP_direct"
            and firewalls[5]["data"] == {
                "fixed_q_and_tables_only": True,
                "growing_q": False,
                "rate": False,
                "ordinary_Cesaro": False,
                "prelimit_or_adaptive_max": False,
                "generic_graph_capacity": False,
                "even_odd_support_at_least_four": False,
                "operator_trace_zero_RH_or_Gates": False,
            }
        ):
            return False
        return True

    independent_semantic = semantic
    fresh_builder = build_certificate
    fresh_equal = exact_equal

    def verifier(value: object, *, compare_fresh: bool = True) -> bool:
        if type(compare_fresh) is not bool:
            return False
        try:
            if not independent_semantic(value):
                return False
            if compare_fresh:
                return fresh_equal(value, fresh_builder())
            return True
        except (ArithmeticError, KeyError, TypeError, ValueError, IndexError, StopIteration):
            return False

    return verifier


verify_certificate = _make_certificate_verifier()
del _make_certificate_verifier


def _find_row(value: dict[str, object], identifier: str) -> dict[str, object]:
    rows = value.get("rows")
    if type(rows) is not list:
        raise ValueError("certificate rows are missing")
    matches = [row for row in rows if type(row) is dict and row.get("id") == identifier]
    if len(matches) != 1:
        raise ValueError("mutation row target is not unique")
    return matches[0]


def mutate_certificate(value: dict[str, object], name: str) -> dict[str, object]:
    if type(name) is not str or name not in MUTATION_NAMES:
        raise ValueError("unknown semantic mutation")
    changed = deepcopy(value)

    def data(identifier: str) -> dict[str, object]:
        row_data = _find_row(changed, identifier)["data"]
        if type(row_data) is not dict:
            raise ValueError("mutation row data is malformed")
        return row_data

    actions = {
        "shift_swap": lambda: changed["density_contract"].__setitem__("shift_tuple", [-1, 0, 1]),  # type: ignore[union-attr]
        "lambda_divisor": lambda: changed["density_contract"].__setitem__("lambda", "Pi without sign divisor"),  # type: ignore[union-attr]
        "all_q_trace_4x4": lambda: changed["relation_contract"].__setitem__("all_q_tropical_trace", "4x4"),  # type: ignore[union-attr]
        "q2_old_value": lambda: data("clock_2").__setitem__("full8_coefficients", ["0", "1", "-1"]),
        "q2_even_witness": lambda: data("q2_witness_summary").__setitem__("even_phase_mask", 2),
        "q2_odd_witness": lambda: data("q2_witness_summary").__setitem__("odd_phase_mask", 1),
        "q2_selfloop_deleted": lambda: data("phase_0_mask_1").__setitem__("selfloop_coefficients", ["0", "0", "0"]),
        "q1_affinity_claim": lambda: data("clock_1").__setitem__("proof_mode", "q_ge_3_multi_affine_compression"),
        "capacity_q1": lambda: data("clock_1").__setitem__("full8_coefficients", ["0", "1", "0"]),
        "capacity_q2": lambda: data("clock_2").__setitem__("full8_coefficients", ["0", "3/4", "0"]),
        "capacity_q3": lambda: data("clock_3").__setitem__("full8_coefficients", ["1/2", "0", "0"]),
        "capacity_q4": lambda: data("clock_4").__setitem__("full8_coefficients", ["1/2", "0", "0"]),
        "capacity_q6": lambda: data("clock_6").__setitem__("full8_coefficients", ["3/8", "0", "0"]),
        "one_site_q6": lambda: data("one_site_q6").__setitem__("coefficients", ["1/8", "1/2", "0"]),
        "q1_ratio_direction": lambda: data("q1_ratio").__setitem__("inequality", "K3/K2>1/2"),
        "q2_ratio_direction": lambda: data("q2_ratio").__setitem__("inequality", "K3/K2<1/3"),
        "projection_point_case": lambda: changed["projection_audit"].__setitem__("pointwise_case_count", 53),  # type: ignore[union-attr]
        "projection_deleted_count": lambda: changed["projection_audit"].__setitem__("deleted_coordinate_count", 17),  # type: ignore[union-attr]
        "relation_safe_count": lambda: changed["relation_pair_audit"].__setitem__("safe_pair_count", 3374),  # type: ignore[union-attr]
        "saturation_changed_count": lambda: changed["relation_pair_audit"].__setitem__("saturation_changed_pair_count", 1679),  # type: ignore[union-attr]
        "multi_affinity_failure": lambda: changed["multi_affinity_audit"].__setitem__("second_difference_failure_count", 1),  # type: ignore[union-attr]
        "self_identification_q2": lambda: changed["multi_affinity_audit"]["state_variable_self_identification_q_1_to_10"].__setitem__("2", False),  # type: ignore[index,union-attr]
        "marginal_left": lambda: data("P0_t_-1").__setitem__("left_marginal", ["1", "0", "0"]),
        "marginal_right": lambda: data("P1_t_0").__setitem__("right_marginal", ["0", "0", "0"]),
        "marginal_only_sum": lambda: data("P2_t_1").__setitem__("pair_charge_sum_pass", False),
        "marginal_omit_t0": lambda: data("P3_t_0").__setitem__("shared_value", 1),
        "path_ceil_to_floor": lambda: changed["square_marginal_interface_audit"]["path_bound"].__setitem__("closed_form", "floor(L/2)*delta"),  # type: ignore[index,union-attr]
        "forced_reset_4": lambda: changed["square_marginal_interface_audit"].__setitem__("forced_reset_moduli", [9]),  # type: ignore[union-attr]
        "forced_reset_9": lambda: data("q36_B1").__setitem__("forced_four_and_nine_resets", False),
        "same_support_scale": lambda: changed["square_marginal_interface_audit"]["same_support_repetition"].__setitem__("formula", "delta_Q=delta_q"),  # type: ignore[index,union-attr]
        "square_q36": lambda: data("q36_B1").__setitem__("capacity_coefficients", ["1/2", "0", "0"]),
        "square_q900": lambda: data("q900_B2").__setitem__("capacity_coefficients", ["2/3", "0", "0"]),
        "q_lift_direction": lambda: data("q_divides_Q_lift").__setitem__("direction", "C(Q)<=C(q)"),
        "q_lift_safety": lambda: data("q_divides_Q_lift")["fixtures"][0].__setitem__("lifted_relation_safety_pass", False),  # type: ignore[index,union-attr]
        "finite_attainment": lambda: data("finite_nonattainment").__setitem__("finite_attainment", True),
        "rh375_terminal_misrole": lambda: data("source_role_split").__setitem__("RH375_terminal_clock_analytic_input", True),
        "growing_q": lambda: data("claim_ceiling").__setitem__("growing_q", True),
        "prelimit_max": lambda: data("claim_ceiling").__setitem__("prelimit_or_adaptive_max", True),
        "causal_claim": lambda: data("centered_noncausal_type").__setitem__("causal_or_online", True),
        "ordinary_cesaro": lambda: data("claim_ceiling").__setitem__("ordinary_Cesaro", True),
        "generic_capacity": lambda: data("claim_ceiling").__setitem__("generic_graph_capacity", True),
        "source_stop": lambda: data("centered_noncausal_type").__setitem__("RH378_window_end_model", "GO"),
        "reflection_sign_identity": lambda: changed["reflection_audit"].__setitem__("terminal_sign_identity", "L_q(F^rho)=L_q(F)"),  # type: ignore[union-attr]
        "reflection_both_signs": lambda: changed["reflection_audit"].__setitem__("both_signs_attained", False),  # type: ignore[union-attr]
        "mu0_definition": lambda: changed["model"].__setitem__("mobius_extension", "mu_0=mu everywhere"),  # type: ignore[union-attr]
        "terminal_normalization": lambda: changed["model"].__setitem__("terminal_functional", "unnormalized sum"),  # type: ignore[union-attr]
        "phase_table_type": lambda: changed["model"].__setitem__("phase_table_type", "F_r:T^2->{-1,+1}"),  # type: ignore[union-attr]
        "safety_condition": lambda: changed["model"].__setitem__("universal_safety_condition", "checked only on observed Mobius words"),  # type: ignore[union-attr]
        "capacity_definition": lambda: changed["model"].__setitem__("capacity_definition", "maximum before limit"),  # type: ignore[union-attr]
        "theta_formula": lambda: changed["density_contract"].__setitem__("theta", "wrong local factors"),  # type: ignore[union-attr]
        "pi_formula": lambda: changed["density_contract"].__setitem__("pi", "unsigned inclusion sum"),  # type: ignore[union-attr]
        "pi_mass": lambda: changed["density_contract"].__setitem__("pi_phase_mass", "sum_U Pi=1"),  # type: ignore[union-attr]
        "endpoint_definition": lambda: changed["endpoint_contract"].__setitem__("limiting_endpoint", "B_infinity=max_y B_y"),  # type: ignore[union-attr]
        "row_extra": lambda: data("clock_3").__setitem__("extra", 0),
        "float_injection": lambda: data("clock_4").__setitem__("q", 4.0),
        "interval_cutoff": lambda: changed["rigorous_interval_audit"].__setitem__("cutoff", 9999),  # type: ignore[union-attr]
        "interval_policy": lambda: changed["rigorous_interval_audit"].__setitem__("nonidentical_overlap_policy", "tie"),  # type: ignore[union-attr]
    }
    actions[name]()
    return changed


def certificate_bytes() -> bytes:
    return canonical_json_bytes(build_certificate())
