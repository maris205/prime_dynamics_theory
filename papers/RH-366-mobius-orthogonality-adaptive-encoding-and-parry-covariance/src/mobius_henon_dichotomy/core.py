"""Pure-Python exact ledgers used by RH-366.

The all-order Möbius and ergodic statements are proved in the manuscript.
This module reproduces only finite arithmetic, symbolic, algebraic, and
dynamic-programming identities.  In particular it represents the covariance
field Q(sqrt(5)) exactly rather than calling an upstream floating truncation
an exact computation.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import product
from math import sqrt


ADJACENCY = (
    (1, 0, 1, 0),
    (1, 0, 0, 0),
    (0, 1, 0, 1),
    (0, 1, 0, 0),
)
STATE_SIGNS = (-1, -1, 1, 1)
STATE_PAIRS = ((-1, -1), (-1, 1), (1, -1), (1, 1))
PAIR_TO_STATE = {pair: index for index, pair in enumerate(STATE_PAIRS)}


def mobius_sieve(limit: int) -> list[int]:
    """Return mu(0),...,mu(limit) by an integer linear sieve."""

    if limit < 1:
        raise ValueError("limit must be positive")
    mu = [0] * (limit + 1)
    mu[1] = 1
    composite = [False] * (limit + 1)
    primes: list[int] = []
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
    return mu


def is_admissible_signs(signs: list[int] | tuple[int, ...], *, cyclic: bool = False) -> bool:
    """Check the exact rule that two plus signs cannot be distance two apart."""

    values = tuple(signs)
    if not values or any(value not in (-1, 1) for value in values):
        return False
    if cyclic:
        return all(not (values[index] == values[(index + 2) % len(values)] == 1)
                   for index in range(len(values)))
    return all(not (values[index] == values[index + 2] == 1)
               for index in range(max(0, len(values) - 2)))


def cyclic_states_from_signs(signs: list[int] | tuple[int, ...]) -> tuple[int, ...]:
    """Encode w_n=(epsilon_n,epsilon_{n-1}) for a cyclic admissible word."""

    values = tuple(signs)
    if not is_admissible_signs(values, cyclic=True):
        raise ValueError("cyclic word is not admissible")
    states = tuple(
        PAIR_TO_STATE[(values[index], values[index - 1])]
        for index in range(len(values))
    )
    if not all(ADJACENCY[states[index]][states[(index + 1) % len(states)]]
               for index in range(len(states))):
        raise AssertionError("sign rule and graph disagree")
    return states


def exceptional_signs(mu: list[int]) -> list[int]:
    """Return the finite prefix of the offline Möbius-adapted sign word."""

    if len(mu) < 2 or mu[0] != 0:
        raise ValueError("mu must include index zero")
    signs = [-1] * len(mu)
    for index in range(1, len(mu)):
        if mu[index] == 1 and index % 4 in (1, 2):
            signs[index] = 1
    if not is_admissible_signs(signs[1:]):
        raise AssertionError("residue-class word must be admissible")
    return signs


def exceptional_score(mu: list[int]) -> tuple[int, int]:
    """Return direct and identity-form scores for the exceptional prefix."""

    signs = exceptional_signs(mu)
    direct = sum(mu[index] * signs[index] for index in range(1, len(mu)))
    mertens = sum(mu[1:])
    selected = sum(
        1 for index in range(1, len(mu))
        if mu[index] == 1 and index % 4 in (1, 2)
    )
    return direct, -mertens + 2 * selected


def _path_mwis(weights: tuple[int, ...]) -> tuple[int, tuple[bool, ...]]:
    best = [0] * (len(weights) + 1)
    take = [False] * (len(weights) + 1)
    for index in range(1, len(weights) + 1):
        include = weights[index - 1] + (best[index - 2] if index >= 2 else 0)
        exclude = best[index - 1]
        if include > exclude:
            best[index] = include
            take[index] = True
        else:
            best[index] = exclude
    chosen = [False] * len(weights)
    index = len(weights)
    while index >= 1:
        include = weights[index - 1] + (best[index - 2] if index >= 2 else 0)
        if take[index] and best[index] == include:
            chosen[index - 1] = True
            index -= 2
        else:
            index -= 1
    return best[-1], tuple(chosen)


def capacity_extreme(mu_values: list[int] | tuple[int, ...], *, maximize: bool) -> tuple[int, tuple[int, ...]]:
    """Optimize the open raw score and return one witnessing sign word."""

    mu = tuple(int(value) for value in mu_values)
    if not mu:
        raise ValueError("mu_values must be nonempty")
    objective = mu if maximize else tuple(-value for value in mu)
    odd_value, odd_take = _path_mwis(objective[0::2])
    even_value, even_take = _path_mwis(objective[1::2])
    selected = [False] * len(mu)
    selected[0::2] = odd_take
    selected[1::2] = even_take
    signs = tuple(1 if flag else -1 for flag in selected)
    score = sum(value * sign for value, sign in zip(mu, signs))
    expected = -sum(mu) + 2 * (odd_value + even_value)
    if not maximize:
        expected = -sum(mu) - 2 * (odd_value + even_value)
    if score != expected or not is_admissible_signs(signs):
        raise AssertionError("capacity reconstruction failed")
    return score, signs


def capacity_extrema(mu_values: list[int] | tuple[int, ...]) -> tuple[int, int]:
    minimum, _ = capacity_extreme(mu_values, maximize=False)
    maximum, _ = capacity_extreme(mu_values, maximize=True)
    return minimum, maximum


def brute_force_extrema(mu_values: list[int] | tuple[int, ...]) -> tuple[int, int]:
    """Independent exponential checker for short words."""

    mu = tuple(mu_values)
    scores = [
        sum(value * sign for value, sign in zip(mu, signs))
        for signs in product((-1, 1), repeat=len(mu))
        if is_admissible_signs(signs)
    ]
    return min(scores), max(scores)


@dataclass(frozen=True)
class Qsqrt5:
    """The exact number a+b sqrt(5), with rational a,b."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other: "Qsqrt5") -> "Qsqrt5":
        return Qsqrt5(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "Qsqrt5") -> "Qsqrt5":
        return Qsqrt5(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "Qsqrt5") -> "Qsqrt5":
        return Qsqrt5(
            self.a * other.a + 5 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def scale(self, value: int | Fraction) -> "Qsqrt5":
        factor = Fraction(value)
        return Qsqrt5(self.a * factor, self.b * factor)

    def power(self, exponent: int) -> "Qsqrt5":
        if exponent < 0:
            raise ValueError("exponent must be nonnegative")
        result = Qsqrt5(Fraction(1), Fraction(0))
        base = self
        count = exponent
        while count:
            if count & 1:
                result = result * base
            base = base * base
            count //= 2
        return result

    def as_pair(self) -> tuple[str, str]:
        return str(self.a), str(self.b)

    def numeric(self) -> float:
        return float(self.a) + float(self.b) * sqrt(5.0)


EVEN_COVARIANCE_RATIO = Qsqrt5(Fraction(-3, 2), Fraction(1, 2))


def covariance_exact(lag: int) -> Qsqrt5:
    """Return Cov(F,F o sigma^lag) exactly in Q(sqrt(5))."""

    if lag < 0:
        raise ValueError("lag must be nonnegative")
    if lag % 2:
        return Qsqrt5()
    return EVEN_COVARIANCE_RATIO.power(lag // 2)


def parry_variance_exact(mu: list[int], length: int | None = None) -> Qsqrt5:
    """Evaluate the exact finite-prefix variance formula in Q(sqrt(5))."""

    if len(mu) < 2 or mu[0] != 0:
        raise ValueError("mu must include index zero")
    size = len(mu) - 1 if length is None else length
    if size < 1 or size >= len(mu):
        raise ValueError("invalid prefix length")
    value = Qsqrt5(Fraction(sum(mu[index] ** 2 for index in range(1, size + 1))))
    for k in range(1, (size - 1) // 2 + 1):
        correlation = sum(
            mu[index] * mu[index + 2 * k]
            for index in range(1, size - 2 * k + 1)
        )
        value = value + EVEN_COVARIANCE_RATIO.power(k).scale(2 * correlation)
    return value


def covariance_rows(maximum_lag: int = 10) -> list[dict[str, object]]:
    rows = []
    for lag in range(maximum_lag + 1):
        value = covariance_exact(lag)
        a, b = value.as_pair()
        rows.append({"lag": lag, "a": a, "b": b, "numeric": value.numeric()})
    return rows


def graph_equivalence_count(maximum_length: int = 8) -> dict[str, int | bool]:
    """Exhaustively check the sign rule against cyclic graph paths."""

    checked = 0
    admissible = 0
    for length in range(3, maximum_length + 1):
        for signs in product((-1, 1), repeat=length):
            checked += 1
            sign_ok = is_admissible_signs(signs, cyclic=True)
            graph_ok = False
            if sign_ok:
                states = cyclic_states_from_signs(signs)
                graph_ok = all(
                    ADJACENCY[states[index]][states[(index + 1) % length]]
                    for index in range(length)
                )
                admissible += 1
            if sign_ok != graph_ok:
                return {"checked": checked, "admissible": admissible, "pass": False}
    return {"checked": checked, "admissible": admissible, "pass": True}
