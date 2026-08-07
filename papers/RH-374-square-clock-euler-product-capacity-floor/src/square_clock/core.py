"""Exact arithmetic for the RH-374 square-clock selector theorem.

The theorem concerns a sequence of fixed clocks

    q_y = 4 * product_{i <= y} p_i^2,

where 3=p_1<p_2<... are the odd primes.  All theorem rows below use integers
or :class:`fractions.Fraction`.  The only floating-point-like output is the
explicitly labelled Euler-product diagnostic, whose analytic tail enclosure
is computed with high-precision decimal arithmetic and is not used as proof.
"""

from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_FLOOR, localcontext
from fractions import Fraction
from functools import lru_cache
import hashlib
import json
from math import isqrt


ALPHABET = (-1, 0, 1)


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    for divisor in range(3, isqrt(value) + 1, 2):
        if value % divisor == 0:
            return False
    return True


def first_odd_primes(count: int) -> tuple[int, ...]:
    """Return the first ``count`` odd primes, beginning with 3."""

    if type(count) is not int or count < 1:
        raise ValueError("count must be a positive integer")
    output: list[int] = []
    candidate = 3
    while len(output) < count:
        if _is_prime(candidate):
            output.append(candidate)
        candidate += 2
    return tuple(output)


def _product(values: list[int] | tuple[int, ...]) -> int:
    result = 1
    for value in values:
        result *= value
    return result


def clock_parameters(y: int) -> tuple[tuple[int, ...], int, int, int]:
    primes = first_odd_primes(y)
    period = _product(tuple(prime * prime for prime in primes))
    admissible = _product(tuple(prime * prime - 1 for prime in primes))
    return primes, period, 4 * period, admissible


def e_products(y: int) -> dict[int, Fraction]:
    """Return ``E_m^(y)=prod_{i<=y}(1-m/p_i^2)`` for 1<=m<=9."""

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


def positive_word(y: int, repeats: int = 1) -> tuple[int, ...]:
    """Return the odd-phase word ``w_y(k)`` over ``repeats`` periods."""

    if type(repeats) is not int or repeats < 1:
        raise ValueError("repeats must be a positive integer")
    if y > 3:
        raise ValueError("direct word generation is intentionally capped at y<=3")
    primes, period, _, _ = clock_parameters(y)
    base = tuple(
        int(all((2 * k + 1) % (prime * prime) != 0 for prime in primes))
        for k in range(period)
    )
    return base * repeats


def cyclic_run_segments(word: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    """Return ``(start,length)`` for every cyclic positive run.

    The square-clock words always contain a zero because the factor p=3
    removes one residue in every nine.  Requiring a zero makes the cyclic
    parsing convention literal and avoids any all-one special case.
    """

    if not word or any(value not in (0, 1) for value in word):
        raise ValueError("word must be a nonempty binary tuple")
    try:
        zero = word.index(0)
    except ValueError as exc:
        raise ValueError("cyclic word must contain a zero") from exc
    size = len(word)
    runs: list[tuple[int, int]] = []
    run_start = -1
    run_length = 0
    for offset in range(1, size + 1):
        index = (zero + offset) % size
        if word[index]:
            if run_length == 0:
                run_start = index
            run_length += 1
        elif run_length:
            runs.append((run_start, run_length))
            run_start = -1
            run_length = 0
    if run_length:
        raise AssertionError("cyclic parser ended inside a run")
    return tuple(runs)


def run_lengths(y: int) -> tuple[int, ...]:
    return tuple(length for _, length in cyclic_run_segments(positive_word(y)))


def exact_run_counts_formula(y: int) -> dict[int, int]:
    """Return exact run counts from the ``E_j-2E_(j+1)+E_(j+2)`` formula."""

    _, period, _, _ = clock_parameters(y)
    products = e_products(y)
    counts: dict[int, int] = {}
    for length in range(1, 9):
        if length == 8:
            # N_9=0 because p=3 is present, so every length-eight block is
            # already an exact maximal run and R_8=N_8=P E_8.
            value = period * products[8]
        else:
            value = period * (
                products[length] - 2 * products[length + 1] + products[length + 2]
            )
        if value.denominator != 1:
            raise AssertionError("run-count formula was not integral")
        counts[length] = value.numerator
    return counts


def formula_odd_run_count(y: int) -> int:
    return sum(exact_run_counts_formula(y)[length] for length in (1, 3, 5, 7))


def formula_even_run_sites(y: int) -> int:
    """Return the number of one-sites lying in even-length runs."""

    counts = exact_run_counts_formula(y)
    return sum(length * counts[length] for length in (2, 4, 6, 8))


def direct_run_counts(y: int) -> dict[int, int]:
    counts = {length: 0 for length in range(1, 9)}
    for length in run_lengths(y):
        if length not in counts:
            raise AssertionError(f"run length exceeds eight: {length}")
        counts[length] += 1
    return counts


def clock_row(y: int) -> dict[str, int | str]:
    primes, period, clock, admissible = clock_parameters(y)
    odd_runs = formula_odd_run_count(y)
    total = 2 * admissible + odd_runs
    coefficient = Fraction(4) + Fraction(2 * odd_runs, admissible)
    return {
        "y": y,
        "largest_prime": primes[-1],
        "P": period,
        "q": clock,
        "A": admissible,
        "O": odd_runs,
        "L_even": formula_even_run_sites(y),
        "selected_phase_count": total,
        "pi2_times_B": str(coefficient),
    }


def _cyclic_mwis_count(word: tuple[int, ...]) -> int:
    return sum((length + 1) // 2 for _, length in cyclic_run_segments(word))


def brute_phase_mwis_count(y: int) -> int:
    """Compute the phase MWIS directly on the two parity cycles."""

    primes, period, _, _ = clock_parameters(y)
    even_word = tuple(
        int((2 * k) % 4 != 0 and all((2 * k) % (p * p) != 0 for p in primes))
        for k in range(2 * period)
    )
    odd_word = positive_word(y, repeats=2)
    return _cyclic_mwis_count(even_word) + _cyclic_mwis_count(odd_word)


def odd_mwis_indices(y: int) -> frozenset[int]:
    """Return a deterministic MWIS of the length-2P odd-phase cycle."""

    word = positive_word(y, repeats=2)
    selected: set[int] = set()
    for start, length in cyclic_run_segments(word):
        selected.update((start + offset) % len(word) for offset in range(0, length, 2))
    return frozenset(selected)


def phase_selector(y: int) -> frozenset[int]:
    """Return one exact optimal positive-weight phase selector at clock q_y."""

    primes, period, clock, _ = clock_parameters(y)
    even = {
        residue
        for residue in range(0, clock, 2)
        if residue % 4 != 0
        and all(residue % (prime * prime) != 0 for prime in primes)
    }
    odd = {2 * k + 1 for k in odd_mwis_indices(y)}
    selected = frozenset(even | odd)
    if any((residue + 2) % clock in selected for residue in selected):
        raise AssertionError("constructed selector has a distance-two conflict")
    return selected


def selector_digest(selected: frozenset[int]) -> str:
    payload = json.dumps(sorted(selected), separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def universal_selector_audit(y: int) -> tuple[int, bool]:
    """Check every phase/current-input/future-input distance-two row."""

    _, _, clock, _ = clock_parameters(y)
    selected = phase_selector(y)
    rows = 0
    for residue in range(clock):
        for current_input in ALPHABET:
            current = residue in selected and current_input == 1
            for future_input in ALPHABET:
                future = (residue + 2) % clock in selected and future_input == 1
                rows += 1
                if current and future:
                    return rows, False
    return rows, True


def recurrence_audit(y: int) -> dict[str, int | bool]:
    """Audit the recurrence when the next odd prime is adjoined."""

    _, _, _, old_a = clock_parameters(y)
    next_prime = first_odd_primes(y + 1)[-1]
    _, _, _, new_a = clock_parameters(y + 1)
    old_o = formula_odd_run_count(y)
    new_o = formula_odd_run_count(y + 1)
    lengths = run_lengths(y)
    even_run_sites = sum(length for length in lengths if length % 2 == 0)
    if even_run_sites != formula_even_run_sites(y):
        raise AssertionError("direct and formula even-run site counts disagree")
    return {
        "y": y,
        "adjoined_prime": next_prime,
        "p2_greater_than_8": next_prime * next_prime > 8,
        "A_old": old_a,
        "A_new": new_a,
        "A_recurrence_rhs": (next_prime * next_prime - 1) * old_a,
        "O_old": old_o,
        "O_new": new_o,
        "L_even": even_run_sites,
        "O_recurrence_rhs": (next_prime * next_prime - 1) * old_o + even_run_sites,
        "exact_length_8_run": 8 in lengths,
        "strict": even_run_sites > 0,
        "pass": (
            new_a == (next_prime * next_prime - 1) * old_a
            and new_o == (next_prime * next_prime - 1) * old_o + even_run_sites
            and 8 in lengths
            and even_run_sites > 0
        ),
    }


def mobius_prefix(limit: int) -> list[int]:
    """Return ``mu(1),...,mu(limit)`` using an exact linear sieve."""

    if type(limit) is not int or limit < 1:
        raise ValueError("limit must be a positive integer")
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
    mu[1] = 1
    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            multiple = value * prime
            if multiple > limit:
                break
            composite[multiple] = True
            if value % prime == 0:
                mu[multiple] = 0
                break
            mu[multiple] = -mu[value]
    return mu[1:]


def selector_score(mu: list[int], y: int = 2) -> int:
    _, _, clock, _ = clock_parameters(y)
    selected = phase_selector(y)
    return sum(
        value * (1 if index % clock in selected and value == 1 else -1)
        for index, value in enumerate(mu, start=1)
    )


def path_capacity(values: list[int]) -> int:
    """Return the RH-366 open distance-two capacity by two path DPs."""

    def path_mwis(weights: list[int]) -> int:
        skip = 0
        take = 0
        for weight in weights:
            skip, take = max(skip, take), skip + weight
        return max(skip, take)

    odd = values[0::2]
    even = values[1::2]
    plus = path_mwis(odd) + path_mwis(even)
    minus = path_mwis([-value for value in odd]) + path_mwis([-value for value in even])
    total = sum(values)
    maximum = -total + 2 * plus
    minimum = -total - 2 * minus
    return max(abs(maximum), abs(minimum))


def finite_witness(mu: list[int], y: int = 2) -> dict[str, int | bool]:
    score = selector_score(mu, y=y)
    capacity = path_capacity(mu)
    return {
        "N": len(mu),
        "selector_score": score,
        "capacity": capacity,
        "capacity_witness": abs(score) <= capacity,
    }


def _primes_up_to(limit: int) -> tuple[int, ...]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for prime in range(2, isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start : limit + 1 : prime] = b"\x00" * (
                (limit - start) // prime + 1
            )
    return tuple(index for index in range(3, limit + 1, 2) if sieve[index])


@lru_cache(maxsize=4)
def euler_limit_diagnostic(cutoff: int = 200_000) -> dict[str, object]:
    """Return a conservative numerical enclosure for the Euler limit.

    For p>cutoff and 1<=m<=8,

      -log prod(1-m/p^2)
        <= m / (cutoff * (1-m/cutoff^2)).

    This follows by enlarging the prime sum to all integers and using
    ``-log(1-x)<=x/(1-x)``.  Decimal rounding is padded outwards.  The exact
    theorem uses convergence of the products, not these decimal endpoints.
    """

    if type(cutoff) is not int or cutoff < 100:
        raise ValueError("cutoff must be an integer at least 100")
    primes = _primes_up_to(cutoff)
    with localcontext() as context:
        context.prec = 70
        pad = Decimal("1e-55")
        intervals: dict[int, tuple[Decimal, Decimal]] = {}
        tail_bounds: dict[int, Decimal] = {}
        x_cutoff = Decimal(cutoff)
        for m in range(1, 9):
            m_decimal = Decimal(m)
            partial = Decimal(1)
            for prime in primes:
                p2 = Decimal(prime * prime)
                partial *= (p2 - m_decimal) / p2
            bound = m_decimal / (
                x_cutoff * (Decimal(1) - m_decimal / (x_cutoff * x_cutoff))
            )
            lower = max(Decimal(0), partial * (-bound).exp() - pad)
            upper = min(Decimal(1), partial + pad)
            intervals[m] = (lower, upper)
            tail_bounds[m] = bound
        intervals[9] = (Decimal(0), Decimal(0))
        tail_bounds[9] = Decimal(0)

        coefficients = {1: 1, 2: -2, 3: 2, 4: -2, 5: 2, 6: -2, 7: 2, 8: -2, 9: 1}
        s_lower = Decimal(0)
        s_upper = Decimal(0)
        for m, coefficient in coefficients.items():
            lower, upper = intervals[m]
            if coefficient >= 0:
                s_lower += Decimal(coefficient) * lower
                s_upper += Decimal(coefficient) * upper
            else:
                s_lower += Decimal(coefficient) * upper
                s_upper += Decimal(coefficient) * lower
        if s_lower <= 0:
            raise AssertionError("tail enclosure was too coarse to certify C>0")
        e1_lower, e1_upper = intervals[1]
        c_lower = s_lower / e1_upper
        c_upper = s_upper / e1_lower
        coefficient_lower = Decimal(4) + Decimal(2) * c_lower
        coefficient_upper = Decimal(4) + Decimal(2) * c_upper

        pi_lower = Decimal("3.14159265358979323846264338327950288419716939937510")
        pi_upper = pi_lower + Decimal("1e-50")
        b_lower = coefficient_lower / (pi_upper * pi_upper)
        b_upper = coefficient_upper / (pi_lower * pi_lower)
        e1_exact_lower = Decimal(8) / (pi_upper * pi_upper)
        e1_exact_upper = Decimal(8) / (pi_lower * pi_lower)
        e1_identity_enclosed = not (
            e1_upper < e1_exact_lower or e1_lower > e1_exact_upper
        )

        quantum = Decimal("1e-18")

        def render_lower(value: Decimal) -> str:
            return format(value.quantize(quantum, rounding=ROUND_FLOOR), ".18f")

        def render_upper(value: Decimal) -> str:
            return format(value.quantize(quantum, rounding=ROUND_CEILING), ".18f")

        return {
            "status": "diagnostic_only_not_theorem_evidence",
            "prime_cutoff": cutoff,
            "odd_prime_count": len(primes),
            "tail_log_bound_max_m8": render_upper(tail_bounds[8]),
            "e_intervals": {
                str(m): {
                    "lower": render_lower(intervals[m][0]),
                    "upper": render_upper(intervals[m][1]),
                }
                for m in range(1, 10)
            },
            "C_interval": {
                "lower": render_lower(c_lower),
                "upper": render_upper(c_upper),
            },
            "pi2_times_B_infinity_interval": {
                "lower": render_lower(coefficient_lower),
                "upper": render_upper(coefficient_upper),
            },
            "B_infinity_interval": {
                "lower": render_lower(b_lower),
                "upper": render_upper(b_upper),
            },
            "e1_equals_8_over_pi2_enclosed": e1_identity_enclosed,
        }


def verify_certificate() -> dict[str, object]:
    """Run all exact formula, brute-force, recurrence, and finite checks."""

    formula_rows = [clock_row(y) for y in range(1, 7)]
    expected_first_rows = [
        (1, 36, 8, 0, 16, "4"),
        (2, 900, 192, 8, 392, "49/12"),
        (3, 44100, 9216, 544, 18976, "593/144"),
    ]
    row_checks = [
        (
            row["y"], row["q"], row["A"], row["O"],
            row["selected_phase_count"], row["pi2_times_B"],
        ) == expected
        for row, expected in zip(formula_rows, expected_first_rows)
    ]

    run_formula_checks: list[dict[str, object]] = []
    brute_mwis_checks: list[dict[str, object]] = []
    for y in range(1, 4):
        direct = direct_run_counts(y)
        formula = exact_run_counts_formula(y)
        row = clock_row(y)
        brute = brute_phase_mwis_count(y)
        run_formula_checks.append({
            "y": y,
            "direct": {str(key): value for key, value in direct.items()},
            "formula": {str(key): value for key, value in formula.items()},
            "max_run": max(run_lengths(y)),
            "pass": direct == formula,
        })
        brute_mwis_checks.append({
            "y": y,
            "brute_mwis": brute,
            "formula_mwis": row["selected_phase_count"],
            "pass": brute == row["selected_phase_count"],
        })

    recurrences = [recurrence_audit(1), recurrence_audit(2), recurrence_audit(3)]
    selected = phase_selector(2)
    universal_rows, universal_pass = universal_selector_audit(2)
    _, _, q_two, _ = clock_parameters(2)
    conflicts = sorted(
        residue for residue in selected if (residue + 2) % q_two in selected
    )
    q900_primes = first_odd_primes(2)
    inactive_selected = sorted(
        residue
        for residue in selected
        if residue % 4 == 0
        or any(residue % (prime * prime) == 0 for prime in q900_primes)
    )

    mu = mobius_prefix(1 << 16)
    endpoint = finite_witness(mu, y=2)
    prefix_rows = 0
    for limit in range(1, 2049):
        if not finite_witness(mu[:limit], y=2)["capacity_witness"]:
            raise AssertionError(f"finite witness failed at N={limit}")
        prefix_rows += 1

    rh373_coefficient = Fraction(97, 24)
    q900_coefficient = Fraction(49, 12)
    improvement = q900_coefficient - rh373_coefficient
    diagnostic = euler_limit_diagnostic()
    all_pass = (
        all(row_checks)
        and all(item["pass"] for item in run_formula_checks)
        and all(item["pass"] for item in brute_mwis_checks)
        and all(item["pass"] for item in recurrences)
        and len(selected) == 392
        and sum(residue % 2 == 0 for residue in selected) == 192
        and sum(residue % 2 == 1 for residue in selected) == 200
        and not inactive_selected
        and not conflicts
        and universal_rows == 900 * len(ALPHABET) ** 2
        and universal_pass
        and improvement == Fraction(1, 24)
        and endpoint["capacity_witness"]
        and prefix_rows == 2048
        and diagnostic["e1_equals_8_over_pi2_enclosed"]
    )
    return {
        "formula_rows": formula_rows,
        "expected_row_checks": row_checks,
        "run_formula_checks": run_formula_checks,
        "brute_mwis_checks": brute_mwis_checks,
        "recurrence_checks": recurrences,
        "q900_selector": {
            "selected_phase_count": len(selected),
            "even_phase_count": sum(residue % 2 == 0 for residue in selected),
            "odd_phase_count": sum(residue % 2 == 1 for residue in selected),
            "inactive_selected_phases": inactive_selected,
            "distance_two_conflicts": conflicts,
            "universal_rows": universal_rows,
            "universal_pass": universal_pass,
            "sorted_phase_sha256": selector_digest(selected),
        },
        "q900_vs_rh373": {
            "q900_pi2_coefficient": str(q900_coefficient),
            "rh373_pi2_coefficient": str(rh373_coefficient),
            "difference": str(improvement),
        },
        "finite_diagnostic": {
            "endpoint": endpoint,
            "prefix_witness_rows": prefix_rows,
            "label": "non_asymptotic_reproduction_only",
        },
        "euler_product_diagnostic": diagnostic,
        "all_pass": all_pass,
    }
