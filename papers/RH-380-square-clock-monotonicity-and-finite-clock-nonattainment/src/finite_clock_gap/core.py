"""Exact finite certificates for RH-380.

The theorem uses only fixed finite clocks.  Values are stored in the exact
basis ``u/pi^2 + v*kappa2``.  The executable layer checks combinatorial
identities, source-independent Fraction algebra, special same-support
replication, and the quantitative gap coefficient.  It does not infer an
asymptotic statement from finite rows.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from math import gcd, lcm


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

    def scale(self, scalar: int | Fraction) -> "EulerValue":
        scalar = Fraction(scalar)
        return EulerValue(self.inv_pi2 * scalar, self.kappa2 * scalar)

    def exact_dict(self) -> dict[str, str]:
        return {
            "inv_pi2": fraction_text(self.inv_pi2),
            "kappa2": fraction_text(self.kappa2),
        }


ZERO = EulerValue()

# RH-379 supplies a proof-grade rational enclosure for
# ``H=pi^2*kappa2``.  The release builder verifies that enclosure is a
# strict subset of this deliberately coarse interval before accepting the
# present certificate.  The coarse interval keeps every comparison below
# visibly separated from zero.
H_LOW = Fraction(159, 50)
H_HIGH = Fraction(319, 100)


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


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
            remaining //= divisor
            exponent += 1
        output.append((divisor, exponent))
        divisor = 3 if divisor == 2 else divisor + 2
    if remaining > 1:
        output.append((remaining, 1))
    return tuple(output)


def first_odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    output: list[int] = []
    candidate = 3
    while len(output) < count:
        if all(candidate % divisor for divisor in range(3, int(candidate**0.5) + 1, 2)):
            output.append(candidate)
        candidate += 2
    return tuple(output)


def square_parameters(y: int) -> dict[str, object]:
    primes = first_odd_primes(y)
    p_product = 1
    a_product = 1
    d_product = 1
    for prime in primes:
        p_product *= prime * prime
        a_product *= prime * prime - 1
        d_product *= prime * prime - 2
    return {
        "y": y,
        "primes": primes,
        "P": p_product,
        "q": 4 * p_product,
        "A": a_product,
        "D": d_product,
    }


def _fraction_product(values: tuple[Fraction, ...]) -> Fraction:
    output = Fraction(1)
    for value in values:
        output *= value
    return output


def _exact_integer(value: Fraction, label: str) -> int:
    """Convert an Euler-product count only after proving integrality."""

    if value.denominator != 1:
        raise ArithmeticError(f"{label} is not integral: {fraction_text(value)}")
    return value.numerator


def square_run_counts(y: int) -> dict[int, int]:
    parameters = square_parameters(y)
    primes = parameters["primes"]
    p_product = parameters["P"]
    assert isinstance(primes, tuple) and isinstance(p_product, int)
    euler = {
        length: _fraction_product(
            tuple(Fraction(prime * prime - length, prime * prime) for prime in primes)
        )
        for length in range(1, 10)
    }
    output = {
        length: _exact_integer(
            p_product * (euler[length] - 2 * euler[length + 1] + euler[length + 2]),
            f"R_{length}({y})",
        )
        for length in range(1, 8)
    }
    output[8] = _exact_integer(p_product * euler[8], f"R_8({y})")
    return output


def run_statistics(y: int) -> dict[str, int]:
    runs = square_run_counts(y)
    return {
        "O": sum(runs[length] for length in (1, 3, 5, 7)),
        "E": sum(runs[length] for length in (2, 4, 6, 8)),
        "L": sum(length * runs[length] for length in (2, 4, 6, 8)),
        "M": sum((length - 1) * runs[length] for length in (1, 3, 5, 7)),
        "X": sum((length - 2) * runs[length] for length in (2, 4, 6, 8)),
        "R8": runs[8],
    }


def direct_square_run_counts(y: int) -> dict[int, int]:
    parameters = square_parameters(y)
    primes = parameters["primes"]
    period = parameters["P"]
    assert isinstance(primes, tuple) and isinstance(period, int)
    word = [
        all((2 * index + 1) % (prime * prime) for prime in primes)
        for index in range(period)
    ]
    if not any(word) or all(word):
        raise AssertionError("square word must contain both zero and one sites")
    counts: Counter[int] = Counter()
    for index, value in enumerate(word):
        if not value or word[index - 1]:
            continue
        length = 0
        while word[(index + length) % period]:
            length += 1
        counts[length] += 1
    return {length: counts[length] for length in range(1, 9)}


def even_descendants_from_one_run(length: int, s: int) -> int:
    """Count even positive descendant runs in the deletion ledger."""

    if type(length) is not int or not 1 <= length <= 8:
        raise ValueError("run length must lie in 1..8")
    if type(s) is not int or s <= length:
        raise ValueError("copy count must exceed the run length")
    count = (s - length) if length % 2 == 0 else 0
    for deleted in range(length):
        pieces = (deleted, length - 1 - deleted)
        count += sum(piece > 0 and piece % 2 == 0 for piece in pieces)
    return count


def deletion_ledger() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for length in range(1, 9):
        expected_kind = "s-2" if length % 2 == 0 else "ell-1"
        checks = []
        for s in (25, 49, 121):
            observed = even_descendants_from_one_run(length, s)
            expected = s - 2 if length % 2 == 0 else length - 1
            checks.append({"s": s, "observed": observed, "expected": expected, "pass": observed == expected})
        rows.append(
            {
                "length": length,
                "parity": "even" if length % 2 == 0 else "odd",
                "expected_formula": expected_kind,
                "checks": checks,
                "all_pass": all(row["pass"] for row in checks),
            }
        )
    return rows


def square_g_value(y: int) -> EulerValue:
    parameters = square_parameters(y)
    statistics = run_statistics(y)
    a_product = parameters["A"]
    d_product = parameters["D"]
    assert isinstance(a_product, int) and isinstance(d_product, int)
    return EulerValue(
        Fraction(4) + Fraction(2 * statistics["O"] + 4 * statistics["E"], a_product),
        Fraction(-statistics["E"], d_product),
    )


def square_transition(y: int) -> dict[str, object]:
    current = square_parameters(y)
    following = square_parameters(y + 1)
    stats = run_statistics(y)
    next_stats = run_statistics(y + 1)
    next_prime = following["primes"][-1]
    assert isinstance(next_prime, int)
    s = next_prime * next_prime
    a_product = current["A"]
    d_product = current["D"]
    assert isinstance(a_product, int) and isinstance(d_product, int)

    e_rhs = (s - 2) * stats["E"] + stats["M"]
    o_rhs = (s - 1) * stats["O"] + stats["L"]
    direct_increment = square_g_value(y + 1) - square_g_value(y)
    formula_increment = EulerValue(
        Fraction(2 * stats["X"] + 4 * stats["M"], a_product * (s - 1)),
        Fraction(-stats["M"], d_product * (s - 2)),
    )
    lower_coefficient = Fraction(12, a_product * (s - 1))
    return {
        "y": y,
        "next_prime": next_prime,
        "s": s,
        "A_y": a_product,
        "D_y": d_product,
        "O_y": stats["O"],
        "mathcal_E_y": stats["E"],
        "L_y": stats["L"],
        "M_y": stats["M"],
        "L_minus_2E": stats["X"],
        "R8_y": stats["R8"],
        "mathcal_E_next": next_stats["E"],
        "mathcal_E_recurrence_rhs": e_rhs,
        "mathcal_E_recurrence_pass": next_stats["E"] == e_rhs,
        "O_next": next_stats["O"],
        "O_recurrence_rhs": o_rhs,
        "O_recurrence_pass": next_stats["O"] == o_rhs,
        "A_recurrence_pass": following["A"] == (s - 1) * a_product,
        "D_recurrence_pass": following["D"] == (s - 2) * d_product,
        "G_y": square_g_value(y).exact_dict(),
        "G_next": square_g_value(y + 1).exact_dict(),
        "increment_direct": direct_increment.exact_dict(),
        "increment_formula": formula_increment.exact_dict(),
        "increment_identity_pass": direct_increment == formula_increment,
        "quantitative_lower_inv_pi2": fraction_text(lower_coefficient),
        "persistent_R8_pass": stats["R8"] >= 1,
        "X_at_least_6_pass": stats["X"] >= 6,
        "M_nonnegative_pass": stats["M"] >= 0,
        "strictness_basis": "X>=6 and M>=0, while 4/pi^2-H_(y+1)>0 by the frozen Euler-product identity",
        "all_pass": (
            next_stats["E"] == e_rhs
            and next_stats["O"] == o_rhs
            and following["A"] == (s - 1) * a_product
            and following["D"] == (s - 2) * d_product
            and direct_increment == formula_increment
            and stats["R8"] >= 1
            and stats["X"] >= 6
            and stats["M"] >= 0
        ),
    }


def squarefree_density_coefficient(q: int, residue: int) -> Fraction:
    """Return exact ``a`` in ``delta_(q,r)=a/pi^2``."""

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
    """Return exact ``b`` in ``theta_(q,r)=b*kappa2``."""

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
    return (
        tuple(squarefree_density_coefficient(q, residue) for residue in range(q)),
        tuple(squarefree_pair_coefficient(q, residue) for residue in range(q)),
    )


def value_compare(left: EulerValue, right: EulerValue) -> int:
    """Compare using the release-checked enclosure ``3.18 < pi^2*kappa2 < 3.19``."""

    difference = left - right
    if difference == ZERO:
        return 0
    if difference.kappa2 >= 0:
        lower = difference.inv_pi2 + difference.kappa2 * H_LOW
        upper = difference.inv_pi2 + difference.kappa2 * H_HIGH
    else:
        lower = difference.inv_pi2 + difference.kappa2 * H_HIGH
        upper = difference.inv_pi2 + difference.kappa2 * H_LOW
    if lower > 0:
        return 1
    if upper < 0:
        return -1
    raise ArithmeticError(
        "Euler-value comparison is unresolved by the release-checked H interval"
    )


ACTIONS = ("0", "J", "I")


def action_compatible(left: str, right: str) -> bool:
    if left not in ACTIONS or right not in ACTIONS:
        raise ValueError("unknown action")
    return not (left in ("J", "I") and right == "I")


def phase_action_weights(q: int) -> dict[str, tuple[EulerValue, ...]]:
    delta, theta = density_vectors(q)
    return {
        "0": tuple(ZERO for _ in range(q)),
        "J": tuple(EulerValue(delta[r], -theta[r]) for r in range(q)),
        "I": tuple(EulerValue(delta[r], 0) for r in range(q)),
    }


def _best_value(values: list[EulerValue]) -> tuple[EulerValue, int]:
    if not values:
        raise ValueError("empty max-plus candidate list")
    best = values[0]
    comparisons = 0
    for value in values[1:]:
        comparisons += 1
        if value_compare(value, best) > 0:
            best = value
    return best, comparisons


def _cyclic_max_plus_value(
    cycle: tuple[int, ...], weights: dict[str, tuple[EulerValue, ...]]
) -> tuple[EulerValue, int]:
    """Independent generic three-state cyclic max-plus DP."""

    totals: list[EulerValue] = []
    comparisons = 0
    for start_index, start_action in enumerate(ACTIONS):
        previous: list[EulerValue | None] = [None, None, None]
        previous[start_index] = weights[start_action][cycle[0]]
        for residue in cycle[1:]:
            current: list[EulerValue | None] = [None, None, None]
            for right_index, right_action in enumerate(ACTIONS):
                candidates = [
                    value + weights[right_action][residue]
                    for left_action, value in zip(ACTIONS, previous)
                    if value is not None and action_compatible(left_action, right_action)
                ]
                if candidates:
                    current[right_index], count = _best_value(candidates)
                    comparisons += count
            previous = current
        closing = [
            value
            for left_action, value in zip(ACTIONS, previous)
            if value is not None and action_compatible(left_action, start_action)
        ]
        if closing:
            best, count = _best_value(closing)
            totals.append(best)
            comparisons += count
    best, count = _best_value(totals)
    return best, comparisons + count


@lru_cache(maxsize=64)
def phasewise_optimum(q: int) -> tuple[EulerValue, int]:
    weights = phase_action_weights(q)
    total = ZERO
    comparisons = 0
    for cycle in phase_cycles(q):
        value, count = _cyclic_max_plus_value(cycle, weights)
        total += value
        comparisons += count
    return total, comparisons


def phase_cycles(q: int) -> tuple[tuple[int, ...], ...]:
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")
    cycle_count = gcd(q, 2)
    cycles = []
    for start in range(cycle_count):
        cycle = []
        current = start
        while not cycle or current != start:
            cycle.append(current)
            current = (current + 2) % q
        cycles.append(tuple(cycle))
    if sum(map(len, cycles)) != q:
        raise AssertionError("addition-by-two cycles do not partition the phases")
    return tuple(cycles)


def _cyclic_positive_runs(bits: tuple[bool, ...]) -> tuple[int, ...]:
    if not bits or all(bits):
        raise ValueError("a separator-bearing cycle is required")
    if not any(bits):
        return ()
    lengths: list[int] = []
    for index, value in enumerate(bits):
        if not value or bits[index - 1]:
            continue
        length = 0
        while bits[(index + length) % len(bits)]:
            length += 1
        lengths.append(length)
    return tuple(lengths)


def support_run_histogram(
    q: int, primes: tuple[int, ...]
) -> tuple[dict[int, int], dict[str, object]]:
    supported = (2, *primes)
    histogram: Counter[int] = Counter()
    cycle_rows: list[dict[str, object]] = []
    for cycle in phase_cycles(q):
        bits = tuple(
            all(residue % (prime * prime) for prime in supported)
            for residue in cycle
        )
        parity = "even" if cycle[0] % 2 == 0 else "odd"
        mod4_cause = parity == "even" and any(residue % 4 == 0 for residue in cycle)
        mod9_cause = parity == "odd" and any(residue % 9 == 0 for residue in cycle)
        cause_pass = mod4_cause if parity == "even" else mod9_cause
        cycle_rows.append(
            {
                "parity": parity,
                "length": len(cycle),
                "zero_sites": sum(not bit for bit in bits),
                "not_all_supported_pass": not all(bits),
                "mod4_zero_cause_pass": mod4_cause,
                "mod9_zero_cause_pass": mod9_cause,
                "cause_specific_pass": cause_pass,
            }
        )
        for length in _cyclic_positive_runs(bits):
            histogram[length] += 1
    separator = {
        "cycles": cycle_rows,
        "even_mod4_separator_pass": all(
            row["mod4_zero_cause_pass"] for row in cycle_rows if row["parity"] == "even"
        ),
        "odd_mod9_separator_pass": all(
            row["mod9_zero_cause_pass"] for row in cycle_rows if row["parity"] == "odd"
        ),
        "all_pass": all(row["cause_specific_pass"] for row in cycle_rows),
    }
    return dict(sorted(histogram.items())), separator


def score_support_runs(histogram: dict[int, int], a: Fraction, b: Fraction) -> EulerValue:
    output = ZERO
    for length, count in histogram.items():
        if length % 2:
            value = EulerValue(a * ((length + 1) // 2), Fraction(0))
        else:
            value = EulerValue(a * (length // 2 + 1), -b)
        output += value.scale(count)
    return output


def same_support_saturation(y: int, multiplier: int) -> dict[str, object]:
    if type(multiplier) is not int or multiplier < 1:
        raise ValueError("multiplier must be a positive integer")
    parameters = square_parameters(y)
    primes = parameters["primes"]
    q_y = parameters["q"]
    a_product = parameters["A"]
    d_product = parameters["D"]
    assert isinstance(primes, tuple)
    assert isinstance(q_y, int) and isinstance(a_product, int) and isinstance(d_product, int)
    Q = multiplier * q_y
    expected_support = {2, *primes}
    actual_support = {prime for prime, _ in factorization(Q)}
    if actual_support != expected_support:
        raise ValueError("same-support saturation requires identical prime support")

    base_histogram, base_separators = support_run_histogram(q_y, primes)
    fine_histogram, fine_separators = support_run_histogram(Q, primes)
    scaling_pass = fine_histogram == {
        length: multiplier * count for length, count in base_histogram.items()
    }
    base_delta, base_theta = density_vectors(q_y)
    fine_delta, fine_theta = density_vectors(Q)
    delta_scaling_pass = all(
        fine_delta[residue] == base_delta[residue % q_y] / multiplier
        for residue in range(Q)
    )
    theta_scaling_pass = all(
        fine_theta[residue] == base_theta[residue % q_y] / multiplier
        for residue in range(Q)
    )
    fine_score = score_support_runs(
        fine_histogram,
        Fraction(2, multiplier * a_product),
        Fraction(1, 2 * multiplier * d_product),
    )
    base_score = square_g_value(y)
    dp_score, dp_comparisons = phasewise_optimum(Q)
    return {
        "y": y,
        "multiplier": multiplier,
        "q_y": q_y,
        "Q": Q,
        "prime_support": sorted(expected_support),
        "same_support_pass": actual_support == expected_support,
        "delta_scale_inv_pi2": fraction_text(Fraction(2, multiplier * a_product)),
        "theta_scale_kappa2": fraction_text(Fraction(1, 2 * multiplier * d_product)),
        "fine_residue_count": Q,
        "delta_scaling_pass": delta_scaling_pass,
        "theta_scaling_pass": theta_scaling_pass,
        "density_scaling_pass": delta_scaling_pass and theta_scaling_pass,
        "base_run_histogram": {str(key): value for key, value in base_histogram.items()},
        "fine_run_histogram": {str(key): value for key, value in fine_histogram.items()},
        "run_replication_pass": scaling_pass,
        "base_separator_certificate": base_separators,
        "fine_separator_certificate": fine_separators,
        "maximum_run_length": max(fine_histogram, default=0),
        "G_Q": fine_score.exact_dict(),
        "G_q_y": base_score.exact_dict(),
        "saturation_pass": fine_score == base_score,
        "direct_dp_G_Q": dp_score.exact_dict(),
        "direct_dp_comparisons": dp_comparisons,
        "direct_dp_pass": dp_score == fine_score,
        "all_pass": (
            actual_support == expected_support
            and scaling_pass
            and delta_scaling_pass
            and theta_scaling_pass
            and bool(base_separators["all_pass"])
            and bool(fine_separators["all_pass"])
            and max(fine_histogram, default=0) <= 8
            and fine_score == base_score
            and dp_score == fine_score
        ),
    }


def lcm_gap_row(q: int, y: int) -> dict[str, object]:
    parameters = square_parameters(y)
    primes = parameters["primes"]
    q_y = parameters["q"]
    a_product = parameters["A"]
    assert isinstance(primes, tuple) and isinstance(q_y, int) and isinstance(a_product, int)
    odd_support = {prime for prime, _ in factorization(q) if prime != 2}
    if not odd_support <= set(primes):
        raise ValueError("y must contain every odd prime divisor of q")
    Q = lcm(q, q_y)
    next_prime = first_odd_primes(y + 1)[-1]
    supported = {prime for prime, _ in factorization(Q)}
    expected = {2, *primes}
    gap = Fraction(12, a_product * (next_prime * next_prime - 1))
    return {
        "q": q,
        "y": y,
        "q_y": q_y,
        "Q": Q,
        "q_divides_Q": Q % q == 0,
        "q_y_divides_Q": Q % q_y == 0,
        "same_support_as_q_y": supported == expected,
        "gap_lower_inv_pi2": fraction_text(gap),
        "gap_statement": "B_infinity-G(q) >= gap_lower_inv_pi2/pi^2",
        "all_pass": Q % q == 0 and Q % q_y == 0 and supported == expected and gap > 0,
    }


def verify_certificate() -> dict[str, object]:
    deletion_rows = deletion_ledger()
    direct_rows = []
    for y in (1, 2, 3):
        direct = direct_square_run_counts(y)
        formula = square_run_counts(y)
        direct_rows.append(
            {
                "y": y,
                "direct": {str(key): value for key, value in direct.items()},
                "formula": {str(key): value for key, value in formula.items()},
                "pass": direct == formula,
            }
        )
    transitions = [square_transition(y) for y in (1, 2, 3, 4)]
    saturation_cases = (
        *((1, multiplier) for multiplier in (2, 3, 4, 6, 8, 9)),
        *((2, multiplier) for multiplier in (2, 3, 5)),
    )
    saturation_rows = [same_support_saturation(y, multiplier) for y, multiplier in saturation_cases]
    gap_rows = [
        lcm_gap_row(1, 1),
        lcm_gap_row(8, 1),
        lcm_gap_row(27, 1),
        lcm_gap_row(125, 2),
        lcm_gap_row(180, 2),
        lcm_gap_row(343, 3),
        lcm_gap_row(44100, 3),
    ]
    locked_statistics = [run_statistics(y) for y in (1, 2, 3)]
    expected_statistics = [
        {"E": 1, "L": 8, "M": 0, "X": 6},
        {"E": 23, "L": 160, "M": 24, "X": 114},
        {"E": 1105, "L": 7160, "M": 1512, "X": 4950},
    ]
    statistics_pass = all(
        all(observed[key] == expected[key] for key in expected)
        for observed, expected in zip(locked_statistics, expected_statistics)
    )
    expected_increments = [
        EulerValue(Fraction(1, 16), 0),
        EulerValue(Fraction(9, 256), Fraction(-24, 7567)),
        EulerValue(Fraction(443, 30720), Fraction(-216, 128639)),
    ]
    increment_fixture_pass = all(
        transition["increment_direct"] == expected.exact_dict()
        for transition, expected in zip(transitions[:3], expected_increments)
    )
    all_pass = (
        all(row["all_pass"] for row in deletion_rows)
        and all(row["pass"] for row in direct_rows)
        and all(row["all_pass"] for row in transitions)
        and all(row["all_pass"] for row in saturation_rows)
        and all(row["all_pass"] for row in gap_rows)
        and statistics_pass
        and increment_fixture_pass
    )
    return {
        "deletion_ledger": deletion_rows,
        "direct_run_rows": direct_rows,
        "square_transitions": transitions,
        "same_support_saturation": saturation_rows,
        "lcm_gap_rows": gap_rows,
        "locked_statistics_pass": statistics_pass,
        "increment_fixtures_pass": increment_fixture_pass,
        "claim_boundary": {
            "fixed_finite_q_before_N_limit": True,
            "phasewise_c11_zero_only": True,
            "absolute_value_uses_RH379_input_reflection": True,
            "delta_y_monotonicity_not_claimed": True,
            "general_cover_saturation_not_claimed": True,
            "growing_clock_not_claimed": True,
            "adaptive_capacity_convergence_not_claimed": True,
            "gates_A_through_E": [False, False, False, False, False],
        },
        "all_pass": all_pass,
    }
