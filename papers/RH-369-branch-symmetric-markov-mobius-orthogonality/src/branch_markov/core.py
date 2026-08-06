"""Integer/rational audits for the RH-369 Markov-family theorem.

The symbolic proof is in ``main.tex``.  This module deliberately uses only
``Fraction`` arithmetic for the matrix, stationary-law, covariance, and
finite Möbius-variance identities.  It does not fit an asymptotic law.
"""

from __future__ import annotations

from fractions import Fraction
from math import log, sqrt


Matrix = tuple[tuple[Fraction, ...], ...]


def _matmul(left: Matrix, right: Matrix) -> Matrix:
    rows, inner, cols = len(left), len(right), len(right[0])
    if len(left[0]) != inner:
        raise ValueError("incompatible matrix dimensions")
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(inner)) for j in range(cols))
        for i in range(rows)
    )


def _matpow(matrix: Matrix, exponent: int) -> Matrix:
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    size = len(matrix)
    result: Matrix = tuple(
        tuple(Fraction(int(i == j), 1) for j in range(size)) for i in range(size)
    )
    base = matrix
    while exponent:
        if exponent & 1:
            result = _matmul(result, base)
        base = _matmul(base, base)
        exponent >>= 1
    return result


def _rowmul(row: tuple[Fraction, ...], matrix: Matrix) -> tuple[Fraction, ...]:
    return tuple(sum(row[i] * matrix[i][j] for i in range(len(row))) for j in range(len(row)))


def _dot(left: tuple[Fraction, ...], right: tuple[Fraction, ...]) -> Fraction:
    return sum(a * b for a, b in zip(left, right))


def transition(t: Fraction) -> Matrix:
    """Return the branch-symmetric transition matrix for ``0<t<1``."""
    t = Fraction(t)
    q = 1 - t
    return (
        (t, Fraction(0), q, Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(0), Fraction(0)),
        (Fraction(0), t, Fraction(0), q),
        (Fraction(0), Fraction(1), Fraction(0), Fraction(0)),
    )


def stationary(t: Fraction) -> tuple[Fraction, ...]:
    """The exact stationary row vector pi_t."""
    t = Fraction(t)
    q = 1 - t
    d = 1 + q
    return (Fraction(1, d * d), q / (d * d), q / (d * d), q * q / (d * d))


SIGN = (Fraction(-1), Fraction(-1), Fraction(1), Fraction(1))


def parameter_checks(t: Fraction) -> dict[str, object]:
    """Check all finite exact identities at one rational interior parameter."""
    t = Fraction(t)
    if not 0 < t < 1:
        raise ValueError("the theorem's parameter domain is 0<t<1")
    q = 1 - t
    d = 1 + q
    matrix = transition(t)
    pi = stationary(t)
    stationary_residual = tuple(a - b for a, b in zip(_rowmul(pi, matrix), pi))
    mean = _dot(pi, SIGN)
    variance = _dot(pi, tuple((x - mean) ** 2 for x in SIGN))
    # Work with the centered vector g; normalization cancels in the identity.
    centered = tuple(x - mean for x in SIGN)
    # Observables propagate by the column action of the row-stochastic matrix.
    p2 = _matpow(matrix, 2)
    p2_column = tuple(sum(p2[i][j] * centered[j] for j in range(4)) for i in range(4))
    eigen_residual = tuple(p2_column[i] + q * centered[i] for i in range(4))
    one_step = tuple(sum(matrix[i][j] * centered[j] for j in range(4)) for i in range(4))
    odd_covariance = sum(pi[i] * centered[i] * one_step[i] for i in range(4))
    p4 = _matpow(matrix, 4)
    p4_positive = all(value > 0 for row in p4 for value in row)
    return {
        "t": str(t),
        "q": str(q),
        "stationary": [str(x) for x in pi],
        "stationary_residual": [str(x) for x in stationary_residual],
        "mean": str(mean),
        "variance": str(variance),
        "expected_mean": str(-t / d),
        "expected_variance": str(4 * q / (d * d)),
        "centered_p2_residual": [str(x) for x in eigen_residual],
        "odd_covariance_residual": str(odd_covariance),
        "p4_positive": p4_positive,
        "characteristic_nontrivial_radius": sqrt(float(q)),
        "pass": (
            all(x == 0 for x in stationary_residual)
            and mean == -t / d
            and variance == 4 * q / (d * d)
            and all(x == 0 for x in eigen_residual)
            and odd_covariance == 0
            and p4_positive
        ),
    }


def mobius_prefix(n: int) -> list[int]:
    """Return [mu(1),...,mu(n)] by a linear sieve."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    mu = [0] * (n + 1)
    primes: list[int] = []
    composite = [False] * (n + 1)
    if n >= 1:
        mu[1] = 1
    for i in range(2, n + 1):
        if not composite[i]:
            primes.append(i)
            mu[i] = -1
        for p in primes:
            value = i * p
            if value > n:
                break
            composite[value] = True
            if i % p == 0:
                mu[value] = 0
                break
            mu[value] = -mu[i]
    return mu[1:]


def two_point_sum(values: list[int], shift: int) -> int:
    """Return sum_n mu(n)mu(n+shift) on the available finite prefix."""
    if shift < 0:
        raise ValueError("shift must be nonnegative")
    return sum(values[i] * values[i + shift] for i in range(len(values) - shift))


def variance_formula(values: list[int], t: Fraction) -> Fraction:
    """Exact finite variance formula from the covariance theorem."""
    t = Fraction(t)
    if not 0 < t < 1:
        raise ValueError("the theorem's parameter domain is 0<t<1")
    q = 1 - t
    result = Fraction(sum(value * value for value in values), 1)
    for k in range(1, (len(values) - 1) // 2 + 1):
        result += 2 * ((-q) ** k) * two_point_sum(values, 2 * k)
    return result


def direct_variance(values: list[int], t: Fraction) -> Fraction:
    """Independent finite expansion using the covariance table."""
    t = Fraction(t)
    q = 1 - t
    result = Fraction(0)
    for i, left in enumerate(values):
        for j, right in enumerate(values):
            lag = abs(i - j)
            covariance = Fraction(0) if lag % 2 else (-q) ** (lag // 2)
            result += left * right * covariance
    return result


def variance_bound_coefficient(t: Fraction) -> Fraction:
    """The geometric absolute bound coefficient (2-t)/t."""
    t = Fraction(t)
    if not 0 < t < 1:
        raise ValueError("the theorem's parameter domain is 0<t<1")
    return (2 - t) / t


def entropy(t: float) -> float:
    """Stationary Markov entropy rate, used only as a diagnostic."""
    if not 0.0 < t < 1.0:
        raise ValueError("the theorem's parameter domain is 0<t<1")
    q = 1.0 - t
    return (-t * log(t) - q * log(q)) / (1.0 + q)


def finite_checks() -> dict[str, object]:
    """Run exact checks at several rational parameters and finite prefixes."""
    parameter_rows = [parameter_checks(Fraction(1, 2)), parameter_checks(Fraction(2, 3)), parameter_checks(Fraction(3, 4))]
    variance_rows = []
    for n in range(1, 15):
        values = mobius_prefix(n)
        for t in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
            formula = variance_formula(values, t)
            direct = direct_variance(values, t)
            bound = variance_bound_coefficient(t) * n
            variance_rows.append({
                "N": n,
                "t": str(t),
                "formula": str(formula),
                "direct": str(direct),
                "formula_equals_direct": formula == direct,
                "nonnegative": formula >= 0,
                "bound_holds": formula <= bound,
            })
    return {
        "parameter_rows": parameter_rows,
        "variance_rows": variance_rows,
        "all_pass": all(row["pass"] for row in parameter_rows)
        and all(
            row["formula_equals_direct"] and row["nonnegative"] and row["bound_holds"]
            for row in variance_rows
        ),
    }
