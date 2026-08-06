"""Integer arithmetic and exact finite audits for RH-371.

The implementation mirrors the RH-366 open path constraint.  It deliberately
does not infer a Mobius density from the finite endpoint.
"""

from __future__ import annotations

from collections import Counter


PAIR_ORDER = ("++", "+-", "+0", "-+", "--", "-0", "0+", "0-", "00")
PERIOD_WORDS = {
    "u": "+++++-++0--+-----0",
    "v": "+++++---0--+---++0",
}
ENDPOINT = 1 << 20


def mobius_prefix(limit: int) -> list[int]:
    """Return mu(0),...,mu(limit) using a linear sieve."""

    if limit < 1:
        raise ValueError("limit must be positive")
    mu = [0] * (limit + 1)
    composite = [False] * (limit + 1)
    primes: list[int] = []
    mu[1] = 1
    for value in range(2, limit + 1):
        if not composite[value]:
            primes.append(value)
            mu[value] = -1
        for prime in primes:
            product = value * prime
            if product > limit:
                break
            composite[product] = True
            if value % prime == 0:
                mu[product] = 0
                break
            mu[product] = -mu[value]
    return mu


def _run_interval_count(mu: list[int], sigma: int, length: int, limit: int) -> int:
    last_start = limit - 2 * (length - 1)
    if last_start < 1:
        return 0
    total = 0
    for start in range(1, last_start + 1, 2):
        if all(mu[start + 2 * offset] == sigma for offset in range(length)):
            total += 1
    return total


def run_counts(mu: list[int], sigma: int, limit: int, max_length: int = 8) -> list[int]:
    """Return C_{sigma,k}(limit) for k=1,...,max_length."""

    if sigma not in (-1, 1):
        raise ValueError("sigma must be -1 or +1")
    if limit >= len(mu):
        raise ValueError("limit exceeds supplied Mobius prefix")
    return [_run_interval_count(mu, sigma, k, limit) for k in range(1, max_length + 1)]


def even_counts(mu: list[int], sigma: int, limit: int) -> int:
    """Return E_sigma(N) on the isolated nonzero even path."""

    return sum(
        1 for value in range(2, limit + 1, 4) if mu[value] == sigma
    )


def _path_mwis(weights: list[int]) -> int:
    """Maximum-weight independent-set value on a path."""

    previous_two = 0
    previous = 0
    for weight in weights:
        current = max(previous, previous_two + weight)
        previous_two, previous = previous, current
    return previous


def dp_capacity(mu: list[int], limit: int) -> dict[str, int]:
    """Independent dynamic-programming capacity, used as a cross-check."""

    odd = mu[1 : limit + 1 : 2]
    even = mu[2 : limit + 1 : 2]
    plus = _path_mwis(odd) + _path_mwis(even)
    minus = _path_mwis([-value for value in odd]) + _path_mwis([-value for value in even])
    total = sum(mu[1 : limit + 1])
    maximum = -total + 2 * plus
    minimum = -total - 2 * minus
    return {
        "M_N": total,
        "W_plus": plus,
        "W_minus": minus,
        "maximum": maximum,
        "minimum": minimum,
        "K_N": max(abs(maximum), abs(minimum)),
    }


def capacity_from_formula(mu: list[int], limit: int) -> dict[str, object]:
    """Compute the eight-run formula and its resulting capacity."""

    plus_counts = run_counts(mu, 1, limit)
    minus_counts = run_counts(mu, -1, limit)
    plus_even = even_counts(mu, 1, limit)
    minus_even = even_counts(mu, -1, limit)
    plus = plus_even + sum(
        (1 if index % 2 == 1 else -1) * count
        for index, count in enumerate(plus_counts, start=1)
    )
    minus = minus_even + sum(
        (1 if index % 2 == 1 else -1) * count
        for index, count in enumerate(minus_counts, start=1)
    )
    total = sum(mu[1 : limit + 1])
    maximum = -total + 2 * plus
    minimum = -total - 2 * minus
    return {
        "M_N": total,
        "E_plus": plus_even,
        "E_minus": minus_even,
        "C_plus": plus_counts,
        "C_minus": minus_counts,
        "W_plus": plus,
        "W_minus": minus,
        "maximum": maximum,
        "minimum": minimum,
        "K_N": max(abs(maximum), abs(minimum)),
    }


def cyclic_pair_ledger(word: str) -> list[list[int]]:
    """Return 18 cyclic lag rows in the fixed nine-pair order."""

    if len(word) != 18 or set(word) - {"+", "-", "0"}:
        raise ValueError("word must be a ternary word of length 18")
    rows: list[list[int]] = []
    for lag in range(18):
        counts = Counter(
            word[index] + word[(index + lag) % 18] for index in range(18)
        )
        rows.append([counts[pair] for pair in PAIR_ORDER])
    return rows


def open_pair_ledger(word: str, lag: int) -> list[int]:
    """Return the non-cyclic ordered-pair row for a finite word."""

    counts = Counter(word[index] + word[index + lag] for index in range(len(word) - lag))
    return [counts[pair] for pair in PAIR_ORDER]


def _path_mwis_word(values: list[str], target: str) -> int:
    return _path_mwis([1 if value == target else 0 for value in values])


def periodic_capacity(word: str, repetitions: int) -> dict[str, int]:
    """Compute the open-prefix capacity of a repeated ternary word."""

    if len(word) != 18 or repetitions < 1:
        raise ValueError("need a length-18 word and positive repetitions")
    values = word * repetitions
    plus = _path_mwis_word(list(values[0::2]), "+") + _path_mwis_word(list(values[1::2]), "+")
    minus = _path_mwis_word(list(values[0::2]), "-") + _path_mwis_word(list(values[1::2]), "-")
    total = sum(1 if value == "+" else -1 if value == "-" else 0 for value in values)
    maximum = -total + 2 * plus
    minimum = -total - 2 * minus
    return {"W_plus": plus, "W_minus": minus, "maximum": maximum, "minimum": minimum, "K_N": max(abs(maximum), abs(minimum))}


def polynomial_certificate() -> bool:
    """Check the group-ring certificate for equal cyclic pair ledgers."""

    u = PERIOD_WORDS["u"]
    v = PERIOD_WORDS["v"]
    assert cyclic_pair_ledger(u) == cyclic_pair_ledger(v)
    assert cyclic_pair_ledger(u)[0] == [8, 0, 0, 0, 8, 0, 0, 0, 2]
    # This second assertion records the strict open-prefix boundary.
    assert open_pair_ledger(u, 2) != open_pair_ledger(v, 2)
    return True


def finite_checks() -> dict[str, object]:
    """Run all finite checks used in result.json."""

    mu = mobius_prefix(ENDPOINT)
    prefix_pass = True
    for limit in range(1, 1001):
        formula = capacity_from_formula(mu, limit)
        dynamic = dp_capacity(mu, limit)
        if any(formula[key] != dynamic[key] for key in ("M_N", "W_plus", "W_minus", "maximum", "minimum", "K_N")):
            prefix_pass = False
            break
    endpoint = capacity_from_formula(mu, ENDPOINT)
    expected_endpoint = {
        "M_N": 257,
        "E_plus": 106305,
        "E_minus": 106183,
        "C_plus": [212554, 84630, 32950, 12359, 4447, 1493, 453, 107],
        "C_minus": [212419, 84346, 32781, 12409, 4487, 1487, 425, 100],
        "W_plus": 258120,
        "W_minus": 257953,
        "maximum": 515983,
        "minimum": -516163,
        "K_N": 516163,
    }
    endpoint_pass = all(endpoint[key] == value for key, value in expected_endpoint.items())
    pair_pass = polynomial_certificate()
    capacity_rows = []
    for name, word in PERIOD_WORDS.items():
        values = [periodic_capacity(word, q)["K_N"] for q in range(1, 257)]
        expected = [10 * q if name == "u" else 12 * q for q in range(1, 257)]
        capacity_rows.append({"word": name, "q_count": len(values), "pass": values == expected})
    return {
        "prefix_count": 1000,
        "prefix_formula_pass": prefix_pass,
        "endpoint_pass": endpoint_pass,
        "pair_ledger_pass": pair_pass,
        "capacity_rows": capacity_rows,
        "all_pass": prefix_pass and endpoint_pass and pair_pass and all(row["pass"] for row in capacity_rows),
        "endpoint": endpoint,
    }
