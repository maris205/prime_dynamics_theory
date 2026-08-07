"""Exact arithmetic and finite certificates for RH-379.

The theorem-level quantities are represented as ``u/pi^2 + v*kappa2`` with
``u`` and ``v`` rational.  Comparisons use a rigorously enclosing interval
for ``H = pi^2*kappa2`` and fail closed if that interval cannot decide a
nonzero comparison.  Finite decimal renderings are diagnostics only.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from decimal import Context, Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from math import gcd, lcm


TERNARY = (-1, 0, 1)
EDGE_ORDER = tuple(product(TERNARY, repeat=2))
COEFFICIENT_ORDER = ("c01", "c02", "c11", "c12", "c21", "c22")
ACTIONS = ("0", "J", "I")
ALL_CANONICAL_ACTIONS = ("0", "J", "K", "I")

CANONICAL_EDGES = {
    "0": frozenset(),
    "J": frozenset({(0, 1)}),
    "K": frozenset({(-1, 1), (1, 1)}),
    "I": frozenset({(-1, 1), (0, 1), (1, 1)}),
}

CANONICAL_TARGET = {
    (Fraction(-1), Fraction(0)): "0",
    (Fraction(-1), Fraction(1)): "0",
    (Fraction(-1), Fraction(2)): "K",
    (Fraction(0), Fraction(-1)): "0",
    (Fraction(0), Fraction(0)): "0",
    (Fraction(0), Fraction(1)): "K",
    (Fraction(1), Fraction(-2)): "J",
    (Fraction(1), Fraction(-1)): "J",
    (Fraction(1), Fraction(0)): "I",
}


def fraction_text(value: Fraction) -> str:
    """Return a stable exact rational string."""

    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class EulerValue:
    """An exact element of ``Q/pi^2 + Q*kappa2``."""

    inv_pi2: Fraction = Fraction(0)
    kappa2: Fraction = Fraction(0)

    def __add__(self, other: object) -> "EulerValue":
        if not isinstance(other, EulerValue):
            return NotImplemented
        return EulerValue(self.inv_pi2 + other.inv_pi2, self.kappa2 + other.kappa2)

    def __sub__(self, other: object) -> "EulerValue":
        if not isinstance(other, EulerValue):
            return NotImplemented
        return EulerValue(self.inv_pi2 - other.inv_pi2, self.kappa2 - other.kappa2)

    def __neg__(self) -> "EulerValue":
        return EulerValue(-self.inv_pi2, -self.kappa2)

    def scale(self, scalar: Fraction | int) -> "EulerValue":
        scalar = Fraction(scalar)
        return EulerValue(self.inv_pi2 * scalar, self.kappa2 * scalar)

    def exact_dict(self) -> dict[str, str]:
        return {
            "inv_pi2": fraction_text(self.inv_pi2),
            "kappa2": fraction_text(self.kappa2),
        }

    def formula(self) -> str:
        pieces: list[str] = []
        if self.inv_pi2:
            pieces.append(f"({fraction_text(self.inv_pi2)})/pi^2")
        if self.kappa2:
            magnitude = fraction_text(abs(self.kappa2))
            if self.kappa2 < 0:
                prefix = "-"
            elif pieces:
                prefix = "+"
            else:
                prefix = ""
            pieces.append(f"{prefix}({magnitude})*kappa2")
        return "".join(pieces) if pieces else "0"


ZERO = EulerValue()


def _sieve_primes(limit: int) -> tuple[int, ...]:
    if type(limit) is not int or limit < 2:
        raise ValueError("prime cutoff must be an integer at least two")
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, int(limit**0.5) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (((limit - start) // prime) + 1)
    return tuple(index for index, flag in enumerate(sieve) if flag)


def _atan_interval(reciprocal: int, terms: int) -> tuple[Fraction, Fraction]:
    """Alternating-series enclosure for ``atan(1/reciprocal)``."""

    if reciprocal < 2 or terms < 1:
        raise ValueError("invalid arctangent enclosure parameters")
    total = Fraction(0)
    for index in range(terms):
        term = Fraction(1, (2 * index + 1) * reciprocal ** (2 * index + 1))
        total += term if index % 2 == 0 else -term
    remainder = Fraction(1, (2 * terms + 1) * reciprocal ** (2 * terms + 1))
    if terms % 2 == 0:
        return total, total + remainder
    return total - remainder, total


def pi_interval(terms: int = 24) -> tuple[Fraction, Fraction]:
    """Exact Machin-formula enclosure for pi."""

    a_low, a_high = _atan_interval(5, terms)
    b_low, b_high = _atan_interval(239, terms)
    return 16 * a_low - 4 * b_high, 16 * a_high - 4 * b_low


def _decimal_partial_kappa_interval(
    primes: tuple[int, ...], precision: int
) -> tuple[Fraction, Fraction]:
    """Directed enclosure of ``prod_p(1-2/p^2)`` over ``primes``.

    The quotient direction is reversed by subtraction: the lower factor is
    ``1-q_high`` and the upper factor is ``1-q_low``.  Product endpoints are
    then propagated with floor and ceiling rounding respectively.
    """

    floor_context = Context(prec=precision, rounding=ROUND_FLOOR)
    ceiling_context = Context(prec=precision, rounding=ROUND_CEILING)
    lower = Decimal(1)
    upper = Decimal(1)
    for prime in primes:
        denominator = Decimal(prime * prime)
        with localcontext(floor_context):
            quotient_low = Decimal(2) / denominator
        with localcontext(ceiling_context):
            quotient_high = Decimal(2) / denominator
        with localcontext(floor_context):
            factor_low = Decimal(1) - quotient_high
            lower = lower * factor_low
        with localcontext(ceiling_context):
            factor_high = Decimal(1) - quotient_low
            upper = upper * factor_high
    return Fraction(lower), Fraction(upper)


@dataclass(frozen=True)
class CertifiedConstants:
    cutoff: int
    precision: int
    prime_count: int
    pi2_low: Fraction
    pi2_high: Fraction
    kappa_low: Fraction
    kappa_high: Fraction
    h_low: Fraction
    h_high: Fraction

    def as_dict(self) -> dict[str, object]:
        return {
            "cutoff": self.cutoff,
            "precision": self.precision,
            "prime_count": self.prime_count,
            "pi2_interval": [fraction_text(self.pi2_low), fraction_text(self.pi2_high)],
            "kappa2_interval": [
                fraction_text(self.kappa_low),
                fraction_text(self.kappa_high),
            ],
            "pi2_kappa2_interval": [fraction_text(self.h_low), fraction_text(self.h_high)],
            "tail_inequality": "prod_(p>X)(1-2/p^2) >= 1-2/X",
            "pi_method": "Machin formula with exact alternating-series remainder",
            "product_method": "directed Decimal rounding converted to exact rational endpoints",
        }


@lru_cache(maxsize=4)
def certified_constants(cutoff: int = 500_000, precision: int = 70) -> CertifiedConstants:
    """Build a proof-grade interval for pi^2, kappa2, and their product."""

    primes = _sieve_primes(cutoff)
    partial_low, partial_high = _decimal_partial_kappa_interval(primes, precision)
    tail_lower = Fraction(cutoff - 2, cutoff)
    kappa_low = partial_low * tail_lower
    kappa_high = partial_high
    pi_low, pi_high = pi_interval()
    pi2_low = pi_low * pi_low
    pi2_high = pi_high * pi_high
    return CertifiedConstants(
        cutoff=cutoff,
        precision=precision,
        prime_count=len(primes),
        pi2_low=pi2_low,
        pi2_high=pi2_high,
        kappa_low=kappa_low,
        kappa_high=kappa_high,
        h_low=pi2_low * kappa_low,
        h_high=pi2_high * kappa_high,
    )


def value_sign(value: EulerValue, constants: CertifiedConstants | None = None) -> int:
    """Return a certified sign, raising if a nonzero comparison is unresolved."""

    if value == ZERO:
        return 0
    constants = constants or certified_constants()
    if value.kappa2 >= 0:
        lower = value.inv_pi2 + value.kappa2 * constants.h_low
        upper = value.inv_pi2 + value.kappa2 * constants.h_high
    else:
        lower = value.inv_pi2 + value.kappa2 * constants.h_high
        upper = value.inv_pi2 + value.kappa2 * constants.h_low
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise ArithmeticError(
        "certified Euler-symbol comparison is ambiguous; increase the prime cutoff"
    )


def value_compare(
    left: EulerValue, right: EulerValue, constants: CertifiedConstants | None = None
) -> int:
    return value_sign(left - right, constants)


def value_interval(value: EulerValue) -> tuple[Fraction, Fraction]:
    constants = certified_constants()
    inv_low = Fraction(1, 1) / constants.pi2_high
    inv_high = Fraction(1, 1) / constants.pi2_low
    if value.inv_pi2 >= 0:
        low = value.inv_pi2 * inv_low
        high = value.inv_pi2 * inv_high
    else:
        low = value.inv_pi2 * inv_high
        high = value.inv_pi2 * inv_low
    if value.kappa2 >= 0:
        low += value.kappa2 * constants.kappa_low
        high += value.kappa2 * constants.kappa_high
    else:
        low += value.kappa2 * constants.kappa_high
        high += value.kappa2 * constants.kappa_low
    return low, high


def decimal_interval(value: EulerValue, digits: int = 12) -> dict[str, str]:
    low, high = value_interval(value)
    precision = max(30, digits + 12)
    scale = Decimal(10) ** -digits
    with localcontext(Context(prec=precision, rounding=ROUND_FLOOR)):
        low_decimal = Decimal(low.numerator) / Decimal(low.denominator)
        low_text = str(low_decimal.quantize(scale))
    with localcontext(Context(prec=precision, rounding=ROUND_CEILING)):
        high_decimal = Decimal(high.numerator) / Decimal(high.denominator)
        high_text = str(high_decimal.quantize(scale))
    return {"lower": low_text, "upper": high_text, "label": "diagnostic_only"}


def factorization(value: int) -> tuple[tuple[int, int], ...]:
    if type(value) is not int or value < 1:
        raise ValueError("value must be a positive integer")
    remaining = value
    output: list[tuple[int, int]] = []
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor:
            divisor = 3 if divisor == 2 else divisor + 2
            continue
        exponent = 0
        while remaining % divisor == 0:
            exponent += 1
            remaining //= divisor
        output.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        output.append((remaining, 1))
    return tuple(output)


def squarefree_density_coefficient(q: int, residue: int) -> Fraction:
    """Return the exact coefficient A with delta_(q,r)=A/pi^2."""

    factors = factorization(q)
    residue %= q
    for prime, exponent in factors:
        if exponent >= 2 and residue % (prime * prime) == 0:
            return Fraction(0)
    value = Fraction(6, q)
    for prime, exponent in factors:
        value /= Fraction(prime * prime - 1, prime * prime)
        if exponent == 1 and residue % prime == 0:
            value *= Fraction(prime - 1, prime)
    return value


def squarefree_pair_coefficient(q: int, residue: int) -> Fraction:
    """Return B with dens(mu(n-2)^2 mu(n)^2=1, n=r mod q)=B*kappa2."""

    factors = factorization(q)
    residue %= q
    for prime, exponent in factors:
        square = prime * prime
        if exponent >= 2 and residue % square in (0, 2 % square):
            return Fraction(0)
        if prime == 2 and exponent == 1 and residue % 2 == 0:
            return Fraction(0)
    value = Fraction(1, q)
    for prime, exponent in factors:
        value /= Fraction(prime * prime - 2, prime * prime)
        if prime != 2 and exponent == 1 and residue % prime in (0, 2 % prime):
            value *= Fraction(prime - 1, prime)
    return value


@lru_cache(maxsize=64)
def density_vectors(q: int) -> tuple[tuple[Fraction, ...], tuple[Fraction, ...]]:
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")
    delta = tuple(squarefree_density_coefficient(q, residue) for residue in range(q))
    theta = tuple(squarefree_pair_coefficient(q, residue) for residue in range(q))
    return delta, theta


def density_aggregation_certificate(q: int, Q: int) -> dict[str, object]:
    """Check exact ``q | Q`` aggregation for both progression densities."""

    if type(q) is not int or type(Q) is not int or q < 1 or Q < 1 or Q % q:
        raise ValueError("density aggregation requires positive clocks q | Q")
    coarse_delta, coarse_theta = density_vectors(q)
    fine_delta, fine_theta = density_vectors(Q)
    aggregated_delta = tuple(
        sum(fine_delta[residue:Q:q], Fraction(0)) for residue in range(q)
    )
    aggregated_theta = tuple(
        sum(fine_theta[residue:Q:q], Fraction(0)) for residue in range(q)
    )
    delta_pass = aggregated_delta == coarse_delta
    theta_pass = aggregated_theta == coarse_theta
    return {
        "q": q,
        "Q": Q,
        "fiber_size": Q // q,
        "residue_count": q,
        "delta_aggregation_pass": delta_pass,
        "theta_aggregation_pass": theta_pass,
        "all_pass": delta_pass and theta_pass,
    }


def one_variable_coefficients(values: dict[int, Fraction]) -> tuple[Fraction, ...]:
    minus, zero, plus = (values[value] for value in TERNARY)
    return zero, (plus - minus) / 2, (plus + minus) / 2 - zero


def score_coefficients(plus_edges: frozenset[tuple[int, int]]) -> tuple[Fraction, ...]:
    """Interpolate ``z*f(x,z)`` in the RH-378 six-term order."""

    by_x: dict[int, tuple[Fraction, ...]] = {}
    for x in TERNARY:
        by_x[x] = one_variable_coefficients(
            {z: Fraction(z * (1 if (x, z) in plus_edges else -1)) for z in TERNARY}
        )
    tensor: dict[tuple[int, int], Fraction] = {}
    for z_degree in range(3):
        x_coefficients = one_variable_coefficients(
            {x: by_x[x][z_degree] for x in TERNARY}
        )
        for x_degree, coefficient in enumerate(x_coefficients):
            tensor[(x_degree, z_degree)] = coefficient
    if any(tensor[(degree, 0)] for degree in range(3)):
        raise AssertionError("score did not vanish at current input zero")
    return tuple(
        tensor[index]
        for index in ((0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2))
    )


def compatible(
    earlier: frozenset[tuple[int, int]], later: frozenset[tuple[int, int]]
) -> bool:
    return not any((x, z) in earlier and (z, w) in later for x, z, w in product(TERNARY, repeat=3))


def _dominates_on_density_cone(
    original: tuple[Fraction, Fraction], target: tuple[Fraction, Fraction]
) -> bool:
    """Check target-original is nonnegative for ``0<=theta<=delta``."""

    delta_coefficient = target[0] - original[0]
    theta_coefficient = target[1] - original[1]
    return delta_coefficient >= 0 and delta_coefficient + theta_coefficient >= 0


def edge_rows(edges: frozenset[tuple[int, int]]) -> list[list[int]]:
    return [list(edge) for edge in sorted(edges)]


@lru_cache(maxsize=1)
def canonical_census() -> dict[str, object]:
    """Exhaust all 512 tables and certify the 192-row canonical reduction."""

    c11_histogram: Counter[Fraction] = Counter()
    pair_histogram: Counter[tuple[Fraction, Fraction]] = Counter()
    target_histogram: Counter[str] = Counter()
    row_payload: list[dict[str, object]] = []
    census_lines: list[str] = []
    subset_pass = True
    dominance_pass = True
    reflection_pass = True
    all_edges: list[frozenset[tuple[int, int]]] = []
    all_reflected_edges: list[frozenset[tuple[int, int]]] = []
    for mask in range(1 << len(EDGE_ORDER)):
        edges = frozenset(
            edge for index, edge in enumerate(EDGE_ORDER) if mask & (1 << index)
        )
        coefficients = score_coefficients(edges)
        c02, c11, c22 = coefficients[1], coefficients[2], coefficients[5]
        c11_histogram[c11] += 1
        reflected = frozenset((-x, -z) for x, z in edges)
        all_edges.append(edges)
        all_reflected_edges.append(reflected)
        reflected_coefficients = score_coefficients(reflected)
        reflection_pass = reflection_pass and (
            reflected_coefficients[1] == -c02
            and reflected_coefficients[2] == -c11
            and reflected_coefficients[5] == -c22
            and compatible(edges, edges) == compatible(reflected, reflected)
        )
        census_lines.append(
            f"{mask:03d}|{','.join(fraction_text(value) for value in coefficients)}"
        )
        if c11 != 0:
            continue
        pair = (c02, c22)
        pair_histogram[pair] += 1
        target = CANONICAL_TARGET.get(pair)
        if target is None:
            raise AssertionError(f"unclassified c11=0 main pair {pair}")
        target_histogram[target] += 1
        canonical = CANONICAL_EDGES[target]
        target_coefficients = score_coefficients(canonical)
        subset_pass = subset_pass and canonical <= edges
        dominance_pass = dominance_pass and _dominates_on_density_cone(
            pair, (target_coefficients[1], target_coefficients[5])
        )
        row_payload.append(
            {
                "mask": mask,
                "c02": fraction_text(c02),
                "c22": fraction_text(c22),
                "canonical_target": target,
            }
        )

    reflection_neighbor_pair_checks = 0
    reflection_neighbor_pair_failures = 0
    for earlier, reflected_earlier in zip(all_edges, all_reflected_edges):
        for later, reflected_later in zip(all_edges, all_reflected_edges):
            reflection_neighbor_pair_checks += 1
            if compatible(earlier, later) != compatible(
                reflected_earlier, reflected_later
            ):
                reflection_neighbor_pair_failures += 1
    reflection_pass = reflection_pass and reflection_neighbor_pair_failures == 0

    compatibility_matrix = [
        [compatible(CANONICAL_EDGES[left], CANONICAL_EDGES[right]) for right in ALL_CANONICAL_ACTIONS]
        for left in ALL_CANONICAL_ACTIONS
    ]
    k_index = ALL_CANONICAL_ACTIONS.index("K")
    i_index = ALL_CANONICAL_ACTIONS.index("I")
    compatibility_equivalence = (
        compatibility_matrix[k_index] == compatibility_matrix[i_index]
        and [row[k_index] for row in compatibility_matrix]
        == [row[i_index] for row in compatibility_matrix]
    )
    canonical_coefficients = {
        label: [fraction_text(value) for value in score_coefficients(edges)]
        for label, edges in CANONICAL_EDGES.items()
    }
    expected_pairs = {
        (Fraction(-1), Fraction(0)): 8,
        (Fraction(-1), Fraction(1)): 32,
        (Fraction(-1), Fraction(2)): 8,
        (Fraction(0), Fraction(-1)): 16,
        (Fraction(0), Fraction(0)): 64,
        (Fraction(0), Fraction(1)): 16,
        (Fraction(1), Fraction(-2)): 8,
        (Fraction(1), Fraction(-1)): 32,
        (Fraction(1), Fraction(0)): 8,
    }
    expected_c11 = {
        Fraction(-1): 32,
        Fraction(-1, 2): 128,
        Fraction(0): 192,
        Fraction(1, 2): 128,
        Fraction(1): 32,
    }
    expected_targets = Counter({"0": 120, "J": 40, "K": 24, "I": 8})
    return {
        "total_tables": 512,
        "c11_zero_tables": len(row_payload),
        "c11_histogram": [
            {"c11": fraction_text(key), "count": c11_histogram[key]}
            for key in sorted(c11_histogram)
        ],
        "main_pair_histogram": [
            {
                "c02": fraction_text(pair[0]),
                "c22": fraction_text(pair[1]),
                "count": pair_histogram[pair],
            }
            for pair in sorted(pair_histogram)
        ],
        "canonical_target_counts": {
            label: target_histogram[label] for label in ALL_CANONICAL_ACTIONS
        },
        "canonical_edges": {label: edge_rows(edges) for label, edges in CANONICAL_EDGES.items()},
        "canonical_coefficients": canonical_coefficients,
        "compatibility_order": list(ALL_CANONICAL_ACTIONS),
        "compatibility_matrix": compatibility_matrix,
        "k_i_full_compatibility_equivalent": compatibility_equivalence,
        "subset_reduction_precedes_k_to_i": True,
        "subset_pass": subset_pass,
        "dominance_pass": dominance_pass,
        "input_reflection_pass": reflection_pass,
        "reflection_neighbor_pair_checks": reflection_neighbor_pair_checks,
        "reflection_neighbor_pair_failures": reflection_neighbor_pair_failures,
        "rows": row_payload,
        "census_sha256": sha256(("\n".join(census_lines) + "\n").encode()).hexdigest(),
        "all_pass": (
            c11_histogram == expected_c11
            and pair_histogram == expected_pairs
            and target_histogram == expected_targets
            and subset_pass
            and dominance_pass
            and reflection_pass
            and compatibility_equivalence
        ),
    }


def phase_cycles(q: int) -> tuple[tuple[int, ...], ...]:
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")
    unseen = set(range(q))
    cycles: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        cycle: list[int] = []
        current = start
        while current in unseen:
            unseen.remove(current)
            cycle.append(current)
            current = (current + 2) % q
        if current != start:
            raise AssertionError("addition-by-two orbit did not close")
        cycles.append(tuple(cycle))
    return tuple(cycles)


def action_compatible(left: str, right: str) -> bool:
    return compatible(CANONICAL_EDGES[left], CANONICAL_EDGES[right])


def phase_action_weights(q: int) -> dict[str, tuple[EulerValue, ...]]:
    delta, theta = density_vectors(q)
    return {
        "0": tuple(ZERO for _ in range(q)),
        "J": tuple(
            EulerValue(delta[residue], -theta[residue]) for residue in range(q)
        ),
        "I": tuple(EulerValue(delta[residue], 0) for residue in range(q)),
    }


def _best_candidate(
    candidates: list[tuple[EulerValue, int]], constants: CertifiedConstants
) -> tuple[EulerValue, int]:
    if not candidates:
        raise ValueError("empty max-plus candidate set")
    best_value, best_index = candidates[0]
    for value, index in candidates[1:]:
        comparison = value_compare(value, best_value, constants)
        if comparison > 0 or (comparison == 0 and index < best_index):
            best_value, best_index = value, index
    return best_value, best_index


def _cyclic_max_plus(
    cycle: tuple[int, ...], weights: dict[str, tuple[EulerValue, ...]]
) -> tuple[EulerValue, tuple[str, ...], int]:
    """Exact three-state cyclic max-plus DP with deterministic backtracking."""

    constants = certified_constants()
    action_count = len(ACTIONS)
    best_total: EulerValue | None = None
    best_path: tuple[str, ...] = ()
    comparisons = 0
    for start_index, start_action in enumerate(ACTIONS):
        previous: list[EulerValue | None] = [None] * action_count
        previous[start_index] = weights[start_action][cycle[0]]
        predecessor_rows: list[list[int | None]] = []
        for residue in cycle[1:]:
            current: list[EulerValue | None] = [None] * action_count
            predecessor: list[int | None] = [None] * action_count
            for right_index, right_action in enumerate(ACTIONS):
                candidates: list[tuple[EulerValue, int]] = []
                for left_index, left_action in enumerate(ACTIONS):
                    if previous[left_index] is None or not action_compatible(left_action, right_action):
                        continue
                    candidates.append((previous[left_index] + weights[right_action][residue], left_index))
                if candidates:
                    selected, selected_index = _best_candidate(candidates, constants)
                    comparisons += max(0, len(candidates) - 1)
                    current[right_index] = selected
                    predecessor[right_index] = selected_index
            previous = current
            predecessor_rows.append(predecessor)
        closing = [
            (value, index)
            for index, value in enumerate(previous)
            if value is not None and action_compatible(ACTIONS[index], start_action)
        ]
        if not closing:
            continue
        total, final_index = _best_candidate(closing, constants)
        comparisons += max(0, len(closing) - 1)
        indices = [final_index]
        for predecessor in reversed(predecessor_rows):
            parent = predecessor[indices[-1]]
            if parent is None:
                raise AssertionError("missing max-plus backpointer")
            indices.append(parent)
        indices.reverse()
        path = tuple(ACTIONS[index] for index in indices)
        if path[0] != start_action:
            raise AssertionError("cyclic max-plus start state drifted")
        if best_total is None:
            best_total, best_path = total, path
        else:
            comparison = value_compare(total, best_total, constants)
            comparisons += 1
            if comparison > 0 or (comparison == 0 and path < best_path):
                best_total, best_path = total, path
    if best_total is None:
        raise AssertionError("no cyclic path survived")
    return best_total, best_path, comparisons


@lru_cache(maxsize=32)
def phasewise_optimum(q: int) -> tuple[EulerValue, tuple[str, ...], int]:
    """Return the exact positive fixed-clock optimum G(q) and a witness."""

    weights = phase_action_weights(q)
    total = ZERO
    action_by_phase = ["0"] * q
    comparisons = 0
    for cycle in phase_cycles(q):
        value, path, count = _cyclic_max_plus(cycle, weights)
        total += value
        comparisons += count
        for residue, action in zip(cycle, path):
            action_by_phase[residue] = action
    return total, tuple(action_by_phase), comparisons


def _path_mwis_values(weights: tuple[EulerValue, ...]) -> EulerValue:
    constants = certified_constants()
    if not weights:
        return ZERO
    previous_two = ZERO
    previous_one = weights[0] if value_sign(weights[0], constants) > 0 else ZERO
    for weight in weights[1:]:
        include = previous_two + weight
        if value_compare(include, previous_one, constants) > 0:
            previous_two, previous_one = previous_one, include
        else:
            previous_two, previous_one = previous_one, previous_one
    return previous_one


def _cycle_mwis_value(weights: tuple[EulerValue, ...]) -> EulerValue:
    constants = certified_constants()
    size = len(weights)
    if size == 1:
        return ZERO
    exclude_first = _path_mwis_values(weights[1:])
    include_first = weights[0] + _path_mwis_values(weights[2:-1])
    return include_first if value_compare(include_first, exclude_first, constants) > 0 else exclude_first


def independent_set_reduction(q: int) -> EulerValue:
    """All-J baseline plus MWIS gains ``K_r-J_(r-2)``."""

    delta, theta = density_vectors(q)
    j = tuple(EulerValue(delta[r], -theta[r]) for r in range(q))
    gains = tuple(
        EulerValue(0, theta[r]) - j[(r - 2) % q] for r in range(q)
    )
    total = sum(j, ZERO)
    for cycle in phase_cycles(q):
        total += _cycle_mwis_value(tuple(gains[r] for r in cycle))
    return total


def _action_digest(actions: tuple[str, ...]) -> str:
    return sha256(("".join(actions) + "\n").encode()).hexdigest()


FIXED_CLOCK_EXPECTED = {
    1: EulerValue(Fraction(6), Fraction(-1)),
    2: EulerValue(Fraction(6), Fraction(-1)),
    3: EulerValue(Fraction(9, 2), Fraction(-3, 7)),
    4: EulerValue(Fraction(4), Fraction(0)),
    5: EulerValue(Fraction(15, 4), Fraction(-5, 23)),
    6: EulerValue(Fraction(5), Fraction(-3, 7)),
    36: EulerValue(Fraction(9, 2), Fraction(-1, 7)),
    180: EulerValue(Fraction(73, 16), Fraction(-25, 161)),
    900: EulerValue(Fraction(73, 16), Fraction(-1, 7)),
    44100: EulerValue(Fraction(1177, 256), Fraction(-1105, 7567)),
}


def fixed_clock_certificate(q: int) -> dict[str, object]:
    value, actions, comparisons = phasewise_optimum(q)
    independent_value = independent_set_reduction(q)
    expected = FIXED_CLOCK_EXPECTED.get(q)
    compatible_path = all(
        action_compatible(actions[residue], actions[(residue + 2) % q])
        for residue in range(q)
    )
    return {
        "q": q,
        "G": value.exact_dict(),
        "formula": value.formula(),
        "diagnostic_interval": decimal_interval(value),
        "action_counts": dict(sorted(Counter(actions).items())),
        "action_sha256": _action_digest(actions),
        "max_plus_comparisons": comparisons,
        "cyclic_compatibility_pass": compatible_path,
        "independent_set_reduction": independent_value.exact_dict(),
        "independent_set_crosscheck_pass": value == independent_value,
        "expected_fixture": expected.exact_dict() if expected else None,
        "expected_fixture_pass": expected is None or value == expected,
        "all_pass": (
            compatible_path
            and value == independent_value
            and (expected is None or value == expected)
        ),
    }


def first_odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    output: list[int] = []
    candidate = 3
    while len(output) < count:
        if all(candidate % prime for prime in range(3, int(candidate**0.5) + 1, 2)):
            output.append(candidate)
        candidate += 2
    return tuple(output)


def _fraction_product(values: tuple[Fraction, ...]) -> Fraction:
    output = Fraction(1)
    for value in values:
        output *= value
    return output


def square_clock_parameters(y: int) -> tuple[tuple[int, ...], int, int, int, int]:
    primes = first_odd_primes(y)
    p_product = 1
    a_product = 1
    d_product = 1
    for prime in primes:
        p_product *= prime * prime
        a_product *= prime * prime - 1
        d_product *= prime * prime - 2
    return primes, p_product, 4 * p_product, a_product, d_product


def square_run_counts(y: int) -> dict[int, int]:
    primes, p_product, _, _, _ = square_clock_parameters(y)
    e = {
        length: _fraction_product(
            tuple(Fraction(prime * prime - length, prime * prime) for prime in primes)
        )
        for length in range(1, 10)
    }
    rows = {
        length: int(p_product * (e[length] - 2 * e[length + 1] + e[length + 2]))
        for length in range(1, 8)
    }
    rows[8] = int(p_product * e[8])
    return rows


def square_clock_certificate(y: int, run_dp_check: bool = True) -> dict[str, object]:
    primes, p_product, q, a_product, d_product = square_clock_parameters(y)
    runs = square_run_counts(y)
    odd_runs = sum(runs[length] for length in (1, 3, 5, 7))
    even_runs = sum(runs[length] for length in (2, 4, 6, 8))
    b_y = EulerValue(Fraction(4) + Fraction(2 * odd_runs, a_product), 0)
    delta_y = EulerValue(Fraction(4 * even_runs, a_product), Fraction(-even_runs, d_product))
    g_formula = b_y + delta_y
    constants = certified_constants()
    h_gap = EulerValue(Fraction(4), Fraction(-a_product, d_product))
    strict = even_runs > 0 and value_sign(h_gap, constants) > 0
    dp_value: EulerValue | None = None
    dp_pass: bool | None = None
    if run_dp_check:
        dp_value, _, _ = phasewise_optimum(q)
        dp_pass = dp_value == g_formula
    recurrence_rows = []
    a = EulerValue(Fraction(2, a_product), 0)
    b = EulerValue(0, Fraction(1, 2 * d_product))
    a_b_order = (
        value_compare(b, a.scale(Fraction(1, 2)), constants) > 0
        and value_compare(a, b, constants) > 0
    )
    for length in range(1, 9):
        previous_two = ZERO
        previous_one = a
        if length == 1:
            value = previous_one
        else:
            for _ in range(2, length + 1):
                first = previous_two + a
                second = previous_one + a - b
                value = first if value_compare(first, second, constants) >= 0 else second
                previous_two, previous_one = previous_one, value
        expected = a.scale((length + 1) // 2) if length % 2 else a.scale(length // 2 + 1) - b
        recurrence_rows.append(
            {"length": length, "value": value.exact_dict(), "expected_pass": value == expected}
        )
    h_limit_identity = "H_y=kappa2*A_y/D_y increases to 4/pi^2"
    return {
        "y": y,
        "primes": list(primes),
        "P_y": p_product,
        "q_y": q,
        "A_y": a_product,
        "D_y": d_product,
        "run_counts": {str(key): value for key, value in runs.items()},
        "O_y": odd_runs,
        "mathcal_E_y": even_runs,
        "a_y": a.exact_dict(),
        "b_y_pair_weight": b.exact_dict(),
        "a_half_lt_b_lt_a": a_b_order,
        "run_recurrence": "M_n=max(M_(n-2)+a_y,M_(n-1)+a_y-b_y)",
        "run_recurrence_rows": recurrence_rows,
        "B_y": b_y.exact_dict(),
        "Delta_y": delta_y.exact_dict(),
        "G_formula": g_formula.exact_dict(),
        "G_formula_text": g_formula.formula(),
        "strict_gain": strict,
        "even_run_bound": f"mathcal_E_y/A_y={fraction_text(Fraction(even_runs, a_product))}<=1/2",
        "H_limit": h_limit_identity,
        "Delta_limit_mechanism": "(mathcal_E_y/A_y)*(4/pi^2-H_y) tends to zero",
        "direct_dp": dp_value.exact_dict() if dp_value else None,
        "direct_dp_pass": dp_pass,
        "all_pass": (
            all(row["expected_pass"] for row in recurrence_rows)
            and a_b_order
            and even_runs * 2 <= a_product
            and strict
            and (dp_pass is not False)
        ),
    }


def q36_strict_gain_certificate() -> dict[str, object]:
    g36 = FIXED_CLOCK_EXPECTED[36]
    f36 = EulerValue(Fraction(4), 0)
    gain = g36 - f36
    partial = Fraction(7567, 22050)
    return {
        "G36": g36.exact_dict(),
        "F36": f36.exact_dict(),
        "gain": gain.exact_dict(),
        "proof_chain": [
            "kappa2 < product_(p in {2,3,5,7})(1-2/p^2)=7567/22050",
            "7567/22050 < 7/20",
            "pi^2 < 10 implies 7/20 < 7/(2*pi^2)",
        ],
        "partial_product": fraction_text(partial),
        "partial_lt_7_over_20": partial < Fraction(7, 20),
        "certified_sign_pass": value_sign(gain) > 0,
        "label": "exact_square_clock_strict_gain_not_first_same_clock_gain",
    }


def cofinal_lift_protocol(q: int, y: int) -> dict[str, object]:
    odd_prime_divisors = {prime for prime, _ in factorization(q) if prime != 2}
    primes, _, q_y, a_product, _ = square_clock_parameters(y)
    cover_pass = odd_prime_divisors <= set(primes)
    if not cover_pass:
        raise ValueError("y must contain every odd prime divisor of q")
    Q_y = lcm(q, q_y)
    same_support = {prime for prime, _ in factorization(Q_y)} == {2, *primes}
    aggregation = density_aggregation_certificate(q, Q_y)

    coarse_value, coarse_actions, _ = phasewise_optimum(q)
    fine_actions = tuple(coarse_actions[residue % q] for residue in range(Q_y))
    fine_weights = phase_action_weights(Q_y)
    delta, theta = density_vectors(Q_y)
    lifted_value = sum(
        (fine_weights[action][residue] for residue, action in enumerate(fine_actions)),
        ZERO,
    )

    supported_primes = (2, *primes)
    retained: set[int] = set()
    retained_total = ZERO
    discarded_total = ZERO
    retained_i_count = 0
    retained_j_count = 0
    discarded_j_count = 0
    zero_density_deleted_count = 0
    one_site_weight_pass = True
    discarded_charge_precondition_pass = True
    for residue, action in enumerate(fine_actions):
        if delta[residue] == 0:
            zero_density_deleted_count += 1
            continue
        predecessor_forced = any(
            (residue - 2) % (prime * prime) == 0 for prime in supported_primes
        )
        if action == "I":
            retained.add(residue)
            retained_total += fine_weights[action][residue]
            retained_i_count += 1
            one_site_weight_pass = one_site_weight_pass and (
                fine_actions[(residue - 2) % Q_y] == "0"
                and fine_weights[action][residue] == EulerValue(delta[residue], 0)
            )
        elif action == "J" and predecessor_forced:
            retained.add(residue)
            retained_total += fine_weights[action][residue]
            retained_j_count += 1
            one_site_weight_pass = one_site_weight_pass and (
                theta[residue] == 0
                and delta[(residue - 2) % Q_y] == 0
                and fine_weights[action][residue] == EulerValue(delta[residue], 0)
            )
        elif action == "J":
            discarded_total += fine_weights[action][residue]
            discarded_j_count += 1
            discarded_charge_precondition_pass = (
                discarded_charge_precondition_pass
                and not predecessor_forced
                and all(
                    (residue - 2) % (prime * prime) != 0
                    for prime in supported_primes
                )
            )

    retained_independent_pass = all(
        (residue - 2) % Q_y not in retained for residue in retained
    )
    runs = square_run_counts(y)
    odd_runs = sum(runs[length] for length in (1, 3, 5, 7))
    b_y = EulerValue(Fraction(4) + Fraction(2 * odd_runs, a_product), 0)
    retained_bound_pass = value_compare(retained_total, b_y) <= 0
    lift_score_pass = lifted_value == coarse_value
    decomposition_pass = lifted_value == retained_total + discarded_total
    all_pass = (
        cover_pass
        and same_support
        and bool(aggregation["all_pass"])
        and lift_score_pass
        and decomposition_pass
        and retained_independent_pass
        and one_site_weight_pass
        and retained_bound_pass
        and discarded_charge_precondition_pass
    )
    return {
        "q": q,
        "y": y,
        "q_y": q_y,
        "Q_y": Q_y,
        "odd_prime_cover": sorted(odd_prime_divisors),
        "cover_pass": cover_pass,
        "same_prime_support_as_q_y": same_support,
        "density_aggregation": aggregation,
        "lifted_score": lifted_value.exact_dict(),
        "coarse_score": coarse_value.exact_dict(),
        "lift_score_pass": lift_score_pass,
        "retained_score": retained_total.exact_dict(),
        "discarded_J_score": discarded_total.exact_dict(),
        "decomposition_pass": decomposition_pass,
        "retained_I_count": retained_i_count,
        "retained_J_count": retained_j_count,
        "discarded_J_count": discarded_j_count,
        "zero_density_deleted_count": zero_density_deleted_count,
        "retained_independent_pass": retained_independent_pass,
        "retained_one_site_weight_pass": one_site_weight_pass,
        "retained_bound_value_B_y": b_y.exact_dict(),
        "retained_bound_pass": retained_bound_pass,
        "discarded_charge_precondition_pass": discarded_charge_precondition_pass,
        "order_of_limits": "fix q; fix y and Q_y; take N->infinity; then y->infinity",
        "retained_rule": "retain every I and only J phases whose predecessor is forced divisible by a supported prime square",
        "retained_bound": "after zero-density deletion the retained phases are a one-site +2 independent set, hence <=F(Q_y)=B_y",
        "discarded_charge": "each discarded J is charged to p^2|(n-2) for some p>p_y",
        "tail_bound": "sum_(p>p_y)1/p^2",
        "no_same_support_memory_saturation_claim": True,
        "all_pass": all_pass,
    }


def verify_certificate() -> dict[str, object]:
    """Run the bounded exact RH-379 certificate suite."""

    census = canonical_census()
    small_rows = [fixed_clock_certificate(q) for q in range(1, 7)]
    fixture_rows = [fixed_clock_certificate(q) for q in (36, 180, 900, 44100)]
    square_rows = [
        square_clock_certificate(1, run_dp_check=False),
        square_clock_certificate(2, run_dp_check=False),
        square_clock_certificate(3, run_dp_check=False),
    ]
    source_hashes = {
        "census_sha256": census["census_sha256"],
        "fixture_action_sha256": {
            str(row["q"]): row["action_sha256"] for row in fixture_rows
        },
    }
    density_checks = []
    for q in range(1, 13):
        delta, theta = density_vectors(q)
        density_checks.append(
            {
                "q": q,
                "sum_pi2_delta": fraction_text(sum(delta, Fraction(0))),
                "sum_kappa2_theta_coefficient": fraction_text(sum(theta, Fraction(0))),
                "pass": sum(delta, Fraction(0)) == 6 and sum(theta, Fraction(0)) == 1,
            }
        )
    density_aggregation_rows = [
        density_aggregation_certificate(q, 720)
        for q in (1, 3, 5, 8, 9, 16, 45, 80, 144, 720)
    ]
    cofinal_rows = [
        cofinal_lift_protocol(1, 1),
        cofinal_lift_protocol(36, 1),
        cofinal_lift_protocol(180, 2),
        cofinal_lift_protocol(44100, 3),
    ]
    q1_gain = FIXED_CLOCK_EXPECTED[1]
    return {
        "census": census,
        "certified_constants": certified_constants().as_dict(),
        "density_normalization": density_checks,
        "density_aggregation": density_aggregation_rows,
        "small_clocks": small_rows,
        "fixture_clocks": fixture_rows,
        "square_clocks": square_rows,
        "q36_strict_gain": q36_strict_gain_certificate(),
        "q1_memory_gain_over_F1_zero": {
            "G1": q1_gain.exact_dict(),
            "positive": value_sign(q1_gain) > 0,
        },
        "cofinal_protocol_rows": cofinal_rows,
        "source_hashes": source_hashes,
        "claim_boundary": {
            "fixed_finite_q_before_N_limit": True,
            "phasewise_c11_zero_only": True,
            "input_reflection_for_absolute_value": True,
            "one_site_embedding_for_reverse_supremum": True,
            "finite_clock_attainment_or_nonattainment_not_claimed": True,
            "delta_monotonicity_not_claimed": True,
            "same_support_memory_saturation_not_claimed": True,
            "first_blocker": "phase-weighted D2 cancellation",
            "gates_A_through_E": [False, False, False, False, False],
        },
        "all_pass": (
            bool(census["all_pass"])
            and all(row["pass"] for row in density_checks)
            and all(row["all_pass"] for row in density_aggregation_rows)
            and all(row["all_pass"] for row in cofinal_rows)
            and all(row["all_pass"] for row in small_rows + fixture_rows + square_rows)
            and q36_strict_gain_certificate()["certified_sign_pass"]
        ),
    }
