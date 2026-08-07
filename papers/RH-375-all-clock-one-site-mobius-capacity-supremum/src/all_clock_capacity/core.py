"""Exact arithmetic for the RH-375 all-clock one-site capacity theorem.

All reported phase weights are ``pi^2 * delta_(q,r)`` and therefore exact
``Fraction`` objects.  Decimal approximations and finite Mobius fitting play
no role.  The bounded scan at the end is explicitly a reproduction check;
the all-clock theorem is proved by divisibility monotonicity and the special
square-clock cofinal lift.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import gcd, isqrt, lcm


INPUTS = (-1, 0, 1)


def _require_clock(q: int) -> None:
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")


def factorization(value: int) -> tuple[tuple[int, int], ...]:
    """Return the prime factorization of a positive integer."""

    _require_clock(value)
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


def _density_pi2_from_factors(
    q: int, residue: int, factors: tuple[tuple[int, int], ...]
) -> Fraction:
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


def density_pi2(q: int, residue: int) -> Fraction:
    r"""Return the exact rational coefficient ``pi^2 delta_(q,residue)``.

    If a class is forced to contain a square divisor its weight is zero.
    Otherwise the local squarefree progression formula is

    ``6/q * prod_(p|q)(1-p^-2)^-1 * prod_(p||q,p|r)(1-p^-1)``.
    """

    _require_clock(q)
    return _density_pi2_from_factors(q, residue, factorization(q))


def density_vector_pi2(q: int) -> tuple[Fraction, ...]:
    _require_clock(q)
    factors = factorization(q)
    return tuple(_density_pi2_from_factors(q, r, factors) for r in range(q))


def phase_cycles(q: int) -> tuple[tuple[int, ...], ...]:
    """Return the cycles of addition by two on ``Z/qZ``."""

    _require_clock(q)
    unseen = set(range(q))
    cycles: list[tuple[int, ...]] = []
    while unseen:
        start = min(unseen)
        cycle: list[int] = []
        value = start
        while value in unseen:
            unseen.remove(value)
            cycle.append(value)
            value = (value + 2) % q
        if value != start:
            raise AssertionError("addition-by-two component did not close")
        cycles.append(tuple(cycle))
    return tuple(cycles)


def _path_mwis(
    indices: tuple[int, ...], weights: tuple[Fraction, ...]
) -> tuple[Fraction, tuple[int, ...]]:
    if len(indices) != len(weights):
        raise ValueError("indices and weights must have equal length")
    size = len(indices)
    if size == 0:
        return Fraction(0), ()
    # Store only scalar DP values, then backtrack once.  Copying a growing
    # witness tuple at every site would turn the long cofinal checks into a
    # quadratic computation.
    dp = [Fraction(0)] * (size + 1)
    dp[1] = max(Fraction(0), weights[0])
    for position in range(2, size + 1):
        dp[position] = max(
            dp[position - 1], dp[position - 2] + weights[position - 1]
        )
    selected: list[int] = []
    position = size
    while position >= 1:
        if dp[position] == dp[position - 1]:
            position -= 1
            continue
        selected.append(indices[position - 1])
        position -= 2
    return dp[-1], tuple(sorted(selected))


def _cycle_mwis(
    indices: tuple[int, ...], weights: tuple[Fraction, ...]
) -> tuple[Fraction, tuple[int, ...]]:
    size = len(indices)
    if size != len(weights) or size < 1:
        raise ValueError("cycle must be nonempty with matching weights")
    if size == 1:
        # Addition by two is a self-loop for q=1,2 components.
        return Fraction(0), ()
    if size == 2:
        if weights[0] >= weights[1]:
            return weights[0], (indices[0],)
        return weights[1], (indices[1],)
    exclude_first = _path_mwis(indices[1:], weights[1:])
    middle_value, middle_set = _path_mwis(indices[2:-1], weights[2:-1])
    include_first = (
        weights[0] + middle_value,
        tuple(sorted((indices[0],) + middle_set)),
    )
    if include_first[0] > exclude_first[0]:
        return include_first
    return exclude_first


def weighted_phase_mwis(q: int) -> tuple[Fraction, tuple[int, ...]]:
    """Return ``pi^2 F(q)`` and a deterministic optimal phase set."""

    weights = density_vector_pi2(q)
    total = Fraction(0)
    selected: list[int] = []
    for cycle in phase_cycles(q):
        value, subset = _cycle_mwis(cycle, tuple(weights[r] for r in cycle))
        total += value
        selected.extend(subset)
    output = tuple(sorted(selected))
    selected_set = set(output)
    if any((residue + 2) % q in selected_set for residue in output):
        raise AssertionError("MWIS reconstruction contains a distance-two conflict")
    return total, output


def active_set_safe(q: int, active: set[int] | frozenset[int]) -> bool:
    return not any((residue + 2) % q in active for residue in active)


def _decode_map(code: int) -> tuple[int, int, int]:
    return tuple(1 if code & (1 << index) else -1 for index in range(3))  # type: ignore[return-value]


def exhaustive_factor_optimum(q: int) -> dict[str, object]:
    """Exhaust all ``8^q`` one-site factor tables for q<=4."""

    _require_clock(q)
    if q > 4:
        raise ValueError("factor-table exhaustion is capped at q<=4")
    weights = density_vector_pi2(q)
    best = Fraction(-1)
    safe_count = 0
    total_count = 0
    best_table: tuple[int, ...] = ()
    for table in product(range(8), repeat=q):
        total_count += 1
        maps = tuple(_decode_map(code) for code in table)
        active = {
            residue for residue, values in enumerate(maps) if any(value == 1 for value in values)
        }
        if not active_set_safe(q, active):
            continue
        safe_count += 1
        correlation = sum(
            weights[residue] * Fraction(values[2] - values[0], 2)
            for residue, values in enumerate(maps)
        )
        if abs(correlation) > best:
            best = abs(correlation)
            best_table = table
    formula, _ = weighted_phase_mwis(q)
    return {
        "q": q,
        "total_tables": total_count,
        "safe_tables": safe_count,
        "brute_pi2_F": str(best),
        "mwis_pi2_F": str(formula),
        "best_table_codes": list(best_table),
        "pass": best == formula,
    }


def exhaustive_subset_optimum(q: int) -> dict[str, object]:
    """Compare the cycle DP with all ``2^q`` phase subsets for q<=12."""

    _require_clock(q)
    if q > 12:
        raise ValueError("subset exhaustion is capped at q<=12")
    weights = density_vector_pi2(q)
    best = Fraction(0)
    safe_count = 0
    for mask in range(1 << q):
        subset = {residue for residue in range(q) if mask & (1 << residue)}
        if not active_set_safe(q, subset):
            continue
        safe_count += 1
        best = max(best, sum(weights[residue] for residue in subset))
    formula, _ = weighted_phase_mwis(q)
    return {
        "q": q,
        "total_subsets": 1 << q,
        "safe_subsets": safe_count,
        "brute_pi2_F": str(best),
        "mwis_pi2_F": str(formula),
        "pass": best == formula,
    }


def divisibility_audit(q: int, Q: int) -> dict[str, object]:
    """Audit density aggregation and ``F(q)<=F(Q)`` for q|Q."""

    _require_clock(q)
    _require_clock(Q)
    if Q % q:
        raise ValueError("q must divide Q")
    small = density_vector_pi2(q)
    large = density_vector_pi2(Q)
    aggregated = tuple(
        sum((large[s] for s in range(residue, Q, q)), Fraction(0))
        for residue in range(q)
    )
    f_small, selected_small = weighted_phase_mwis(q)
    f_large, _ = weighted_phase_mwis(Q)
    selected_small_set = set(selected_small)
    lifted = {s for s in range(Q) if s % q in selected_small_set}
    return {
        "q": q,
        "Q": Q,
        "ratio": Q // q,
        "aggregation_pass": aggregated == small,
        "lift_safe": active_set_safe(Q, lifted),
        "pi2_F_q": str(f_small),
        "pi2_F_Q": str(f_large),
        "monotonicity_pass": f_small <= f_large,
        "pass": aggregated == small and active_set_safe(Q, lifted) and f_small <= f_large,
    }


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    return all(value % divisor for divisor in range(3, isqrt(value) + 1, 2))


def first_odd_primes(count: int) -> tuple[int, ...]:
    if type(count) is not int or count < 1:
        raise ValueError("count must be positive")
    output: list[int] = []
    candidate = 3
    while len(output) < count:
        if _is_prime(candidate):
            output.append(candidate)
        candidate += 2
    return tuple(output)


def _product(values: tuple[int, ...]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def clock_parameters(y: int) -> tuple[tuple[int, ...], int, int, int]:
    primes = first_odd_primes(y)
    period = _product(tuple(prime * prime for prime in primes))
    admissible = _product(tuple(prime * prime - 1 for prime in primes))
    return primes, period, 4 * period, admissible


def _e_products(y: int) -> dict[int, Fraction]:
    primes = first_odd_primes(y)
    return {
        m: _fraction_product(
            tuple(Fraction(prime * prime - m, prime * prime) for prime in primes)
        )
        for m in range(1, 10)
    }


def _fraction_product(values: tuple[Fraction, ...]) -> Fraction:
    result = Fraction(1)
    for value in values:
        result *= value
    return result


def clock_odd_run_count(y: int) -> int:
    _, period, _, _ = clock_parameters(y)
    products = _e_products(y)
    value = period * sum(
        (
            products[j] - 2 * products[j + 1] + products[j + 2]
            for j in (1, 3, 5, 7)
        ),
        Fraction(0),
    )
    if value.denominator != 1:
        raise AssertionError("odd-run formula was not integral")
    return value.numerator


def clock_selected_count(y: int) -> int:
    _, _, _, admissible = clock_parameters(y)
    return 2 * admissible + clock_odd_run_count(y)


def clock_pi2_coefficient(y: int) -> Fraction:
    _, _, _, admissible = clock_parameters(y)
    return Fraction(4) + Fraction(2 * clock_odd_run_count(y), admissible)


def cover_y(q: int) -> int:
    odd_primes = [prime for prime, _ in factorization(q) if prime != 2]
    if not odd_primes:
        return 1
    target = max(odd_primes)
    y = 1
    while first_odd_primes(y)[-1] < target:
        y += 1
    return y


def _uniform_support_mwis_count(q: int) -> tuple[int, int, tuple[Fraction, ...]]:
    weights = density_vector_pi2(q)
    positive = tuple(weight for weight in weights if weight > 0)
    units = tuple(sorted(set(positive)))
    binary = tuple(Fraction(int(weight > 0)) for weight in weights)
    total = 0
    for cycle in phase_cycles(q):
        value, _ = _cycle_mwis(cycle, tuple(binary[r] for r in cycle))
        if value.denominator != 1:
            raise AssertionError("binary MWIS was not integral")
        total += value.numerator
    return total, len(positive), units


def cofinal_lift_audit(q: int) -> dict[str, object]:
    """Audit the special lift to a square clock with the same prime support."""

    y = cover_y(q)
    primes, _, q_y, _ = clock_parameters(y)
    Q = lcm(q, q_y)
    R = Q // q_y
    q_support = {prime for prime, _ in factorization(q)}
    square_support = {2, *primes}
    Q_support = {prime for prime, _ in factorization(Q)}
    count, positive_count, units = _uniform_support_mwis_count(Q)
    expected_count = R * clock_selected_count(y)
    expected_positive = R * sum(
        int(density_pi2(q_y, residue) > 0) for residue in range(q_y)
    )
    if len(units) != 1:
        f_Q = Fraction(-1)
    else:
        f_Q = count * units[0]
    f_q, _ = weighted_phase_mwis(q)
    b_y = clock_pi2_coefficient(y)
    return {
        "q": q,
        "odd_prime_cover_y": y,
        "q_y": q_y,
        "Q": Q,
        "R": R,
        "q_prime_support_subset": q_support <= square_support,
        "Q_same_prime_support": Q_support == square_support,
        "positive_weight_unit_count": len(units),
        "pi2_positive_weight_unit": str(units[0]) if len(units) == 1 else None,
        "positive_phase_count": positive_count,
        "expected_positive_phase_count": expected_positive,
        "support_mwis_count": count,
        "expected_support_mwis_count": expected_count,
        "pi2_F_q": str(f_q),
        "pi2_F_Q": str(f_Q),
        "pi2_B_y": str(b_y),
        "monotonicity_pass": f_q <= f_Q,
        "saturation_pass": f_Q == b_y,
        "pass": (
            q_support <= square_support
            and Q_support == square_support
            and len(units) == 1
            and positive_count == expected_positive
            and count == expected_count
            and f_q <= f_Q == b_y
        ),
    }


def bounded_clock_scan(limit: int = 256) -> dict[str, object]:
    """Scan finitely many clocks; this is reproduction, never theorem evidence."""

    _require_clock(limit)
    records: list[dict[str, object]] = []
    maximum = Fraction(-1)
    achievers: list[int] = []
    for q in range(1, limit + 1):
        value, selected = weighted_phase_mwis(q)
        if value > maximum:
            maximum = value
            achievers = [q]
            records.append({"q": q, "pi2_F": str(value), "selected": len(selected)})
        elif value == maximum:
            achievers.append(q)
    return {
        "label": "bounded_reproduction_only_not_all_clock_evidence",
        "limit": limit,
        "clock_count": limit,
        "record_rows": records,
        "maximum_pi2_F": str(maximum),
        "maximizing_clocks": achievers,
    }


@lru_cache(maxsize=1)
def verify_certificate() -> dict[str, object]:
    """Run all exact density, optimization, lift, and bounded checks."""

    density_examples = [
        {"q": q, "r": r, "pi2_delta": str(density_pi2(q, r))}
        for q, r in ((1, 0), (2, 0), (3, 0), (3, 1), (4, 0), (4, 1), (180, 1), (180, 5))
    ]
    factor_checks = [exhaustive_factor_optimum(q) for q in range(1, 5)]
    subset_checks = [exhaustive_subset_optimum(q) for q in range(1, 11)]
    divisibility_checks = [
        divisibility_audit(q, Q)
        for q, Q in ((1, 2), (2, 4), (3, 12), (4, 36), (5, 100), (6, 180), (12, 180), (25, 900))
    ]
    cofinal_checks = [
        cofinal_lift_audit(q) for q in (1, 2, 3, 5, 8, 16, 25, 27, 125, 343)
    ]
    square_rows = [
        {
            "y": y,
            "q_y": clock_parameters(y)[2],
            "selected_count": clock_selected_count(y),
            "formula_pi2_B_y": str(clock_pi2_coefficient(y)),
            "mwis_pi2_F_q_y": str(weighted_phase_mwis(clock_parameters(y)[2])[0]),
        }
        for y in range(1, 4)
    ]
    square_rows_pass = all(
        row["formula_pi2_B_y"] == row["mwis_pi2_F_q_y"] for row in square_rows
    )
    degeneracy = {
        "q1_pi2_F": str(weighted_phase_mwis(1)[0]),
        "q2_pi2_F": str(weighted_phase_mwis(2)[0]),
        "q1_self_loop": phase_cycles(1) == ((0,),),
        "q2_self_loops": phase_cycles(2) == ((0,), (1,)),
    }
    scan = bounded_clock_scan(256)
    all_pass = (
        all(item["pass"] for item in factor_checks)
        and all(item["pass"] for item in subset_checks)
        and all(item["pass"] for item in divisibility_checks)
        and all(item["pass"] for item in cofinal_checks)
        and square_rows_pass
        and degeneracy["q1_pi2_F"] == "0"
        and degeneracy["q2_pi2_F"] == "0"
        and degeneracy["q1_self_loop"]
        and degeneracy["q2_self_loops"]
        and scan["clock_count"] == 256
    )
    return {
        "density_examples": density_examples,
        "degenerate_clocks": degeneracy,
        "factor_exhaustion": factor_checks,
        "subset_exhaustion": subset_checks,
        "divisibility_checks": divisibility_checks,
        "cofinal_lift_checks": cofinal_checks,
        "square_clock_rows": square_rows,
        "square_clock_rows_pass": square_rows_pass,
        "bounded_clock_scan": scan,
        "all_pass": bool(all_pass),
    }
