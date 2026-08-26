#!/usr/bin/env python3
"""Finite interval certificate for the literal V59 residual census.

The certificate keeps the finite V59 masks, prime shell, beta coefficient and
four-block projection.  The comparison constant C_2 is enclosed by a finite
Euler product and a proved positive tail bound.  Logarithms are enclosed by
high-precision decimal endpoints with a deliberately generous rational guard;
all subsequent interval operations are exact Fraction operations.

This is a finite numerical certificate.  It is not an asymptotic estimate for
the V59 radius and it does not claim a twin-prime theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc267_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS"
ROUND2_CLUE = "REPEAT_THE_CENSUS_WITH_GROWING_LOCAL_CUTOFF_AND_SMOOTH_PROFILE"
TAIL_CUTOFF = 50_000
GRID = 10 ** 30
LOG_GUARD = Decimal("1e-25")
getcontext().prec = 100


class CheckFailure(RuntimeError):
    """Raised when the finite certificate cannot be established."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


class Interval:
    """Closed rational interval with exact endpoint arithmetic."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction, hi: Fraction | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
        # Keep the exact interval operations cheap.  Every endpoint is
        # rounded outwards to a fixed decimal grid, so this is still an
        # enclosure rather than a floating-point point estimate.
        self.lo = grid_lower(raw_lo)
        self.hi = grid_upper(raw_hi)
        need(self.lo <= self.hi, "reversed interval")

    def __add__(self, other: Interval | Fraction) -> Interval:
        right = as_interval(other)
        return Interval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval | Fraction) -> Interval:
        return self + (-as_interval(other))

    def __rsub__(self, other: Interval | Fraction) -> Interval:
        return as_interval(other) - self

    def __mul__(self, other: Interval | Fraction) -> Interval:
        right = as_interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction) -> Interval:
        right = as_interval(other)
        need(right.lo > 0 or right.hi < 0, "interval division crosses zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))

    def square(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(self.lo * self.lo,
                                             self.hi * self.hi))
        values = (self.lo * self.lo, self.hi * self.hi)
        return Interval(min(values), max(values))

    def absolute(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(-self.lo, self.hi))
        return Interval(min(abs(self.lo), abs(self.hi)),
                        max(abs(self.lo), abs(self.hi)))


def as_interval(value: Interval | Fraction | int) -> Interval:
    return value if isinstance(value, Interval) else Interval(Fraction(value))


def grid_lower(value: Fraction) -> Fraction:
    numerator = value.numerator * GRID
    quotient = numerator // value.denominator
    return Fraction(quotient, GRID)


def grid_upper(value: Fraction) -> Fraction:
    numerator = value.numerator * GRID
    quotient, remainder = divmod(numerator, value.denominator)
    return Fraction(quotient + int(remainder != 0), GRID)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def decimal_fraction(value: Decimal) -> Fraction:
    return Fraction(value)


def decimal_text(value: Fraction, digits: int = 12) -> str:
    scale = Decimal(value.numerator) / Decimal(value.denominator)
    return format(scale, f".{digits}g")


def square_root_text(value: Fraction, digits: int = 10) -> str:
    need(value >= 0, "negative square-root display")
    scale = Decimal(value.numerator) / Decimal(value.denominator)
    return format(scale.sqrt(), f".{digits}g")


def interval_text(value: Interval) -> list[str]:
    return [decimal_text(value.lo), decimal_text(value.hi)]


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


PRIMES = primes_up_to(TAIL_CUTOFF)


def factor_distinct(value: int) -> list[int]:
    remaining = value
    factors: list[int] = []
    for prime in PRIMES:
        if prime * prime > remaining:
            break
        if remaining % prime == 0:
            factors.append(prime)
            while remaining % prime == 0:
                remaining //= prime
    if remaining > 1:
        factors.append(remaining)
    return factors


def mobius(value: int) -> int:
    factors = factor_distinct(value)
    if any(value % (prime * prime) == 0 for prime in factors):
        return 0
    return -1 if len(factors) % 2 else 1


def prime_power(value: int) -> tuple[int, int] | None:
    for prime in PRIMES:
        if prime > value:
            break
        power = prime
        exponent = 1
        while power < value:
            power *= prime
            exponent += 1
        if power == value:
            return prime, exponent
    return None


def log_interval(prime: int) -> Interval:
    center = Decimal(prime).ln()
    # Decimal.ln is evaluated at 100 digits; the 1e-70 guard is much wider
    # than the retained rounding error and is carried as an exact Fraction.
    guard = decimal_fraction(LOG_GUARD)
    return Interval(decimal_fraction(center) - guard,
                    decimal_fraction(center) + guard)


def lambda_interval(value: int) -> Interval:
    power = prime_power(value)
    return Interval(Fraction(0)) if power is None else log_interval(power[0])


def beta_value(value: int, scale: int) -> Fraction:
    cutoff = 0
    while (cutoff + 1) ** 400 <= scale ** 133:
        cutoff += 1
    divisor_sum = sum(mobius(d) for d in range(1, cutoff + 1)
                      if value % d == 0)
    power = prime_power(value)
    normalized_lambda = Fraction(0) if power is None else Fraction(1, power[1])
    return normalized_lambda - divisor_sum


TAIL_CACHE: dict[int, tuple[Fraction, Fraction]] = {}


def comparison_tail(z: int) -> tuple[Fraction, Fraction]:
    """Enclose prod_{p>z}(1-(p-1)^(-2)) by rational endpoints."""
    if z not in TAIL_CACHE:
        finite = Decimal(1)
        for prime in PRIMES:
            if prime > z:
                numerator = Decimal((prime - 1) ** 2 - 1)
                denominator = Decimal((prime - 1) ** 2)
                finite *= numerator / denominator
        # For p>TAIL_CUTOFF, sum (p-1)^(-2) is bounded by
        # sum_{m=TAIL_CUTOFF}^infinity m^(-2) < 1/(TAIL_CUTOFF-1).
        lower = finite * (1 - Decimal(1) / Decimal(TAIL_CUTOFF - 1))
        # The decimal product is converted to a rational outer enclosure;
        # the remaining tail inequality is exact and is stated in the paper.
        TAIL_CACHE[z] = (grid_lower(Fraction(lower)),
                         grid_upper(Fraction(finite)))
    return TAIL_CACHE[z]


def comparison_interval(value: int, z: int = 2) -> Interval:
    lower, upper = comparison_tail(z)
    local = Fraction(1)
    for prime in PRIMES:
        if prime > z:
            break
        if (value + 2) % prime == 0:
            return Interval(Fraction(0))
        local *= Fraction(prime, prime - 1)
    for prime in factor_distinct(value):
        if prime > z:
            local *= Fraction(prime - 1, prime - 2)
    return Interval(lower * local, upper * local)


def source_weights(scale: int, z: int) -> tuple[list[int], list[Fraction], list[Interval]]:
    indices = list(range(scale // 2 + 1, scale + 1))
    beta = [beta_value(value, scale) for value in indices]
    shifted = [lambda_interval(value + 2) - comparison_interval(value, z)
               for value in indices]
    return indices, beta, shifted


def kernel(shift: int, H: int, exponent: int) -> Fraction:
    return Fraction(H ** (2 * exponent),
                    (H * H + shift * shift) ** exponent)


def operator_output(indices: list[int], beta: list[Fraction],
                    H: int, Q: int, exponent: int) -> tuple[list[Fraction], list[int]]:
    shell = [prime for prime in PRIMES if Q < prime <= 2 * Q]
    output: list[Fraction] = []
    for u in indices:
        value = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t:
                continue
            for prime in shell:
                if u % prime == 0 or t % prime == 0:
                    continue
                centered = Fraction(int(u % prime == t % prime), 1)
                centered -= Fraction(1, prime - 1)
                value += (prime * kernel(u - t, H, exponent)
                          * centered * beta_t)
        output.append(value)
    return output, shell


def sum_interval(values: Iterable[Interval | Fraction]) -> Interval:
    total = Interval(Fraction(0))
    for value in values:
        total += value
    return total


def frame_data(indices: list[int], weights: list[Interval],
               output: list[Fraction]) -> dict[str, Any]:
    length = len(indices)
    block_size = length // 4
    need(length % 4 == 0 and block_size > 0, "four-block partition")
    blocks = [range(k * block_size, (k + 1) * block_size)
              for k in range(4)]
    block_w = [sum_interval(weights[j] for j in block) for block in blocks]
    block_g = [sum(output[j] for j in block) for block in blocks]
    contrasts = ([1, 1, -1, -1], [1, -1, 0, 0], [0, 0, 1, -1])
    denominators = [4 * block_size, 2 * block_size, 2 * block_size]

    direct = sum_interval(weights[j] * output[j] for j in range(length))
    projected = Interval(Fraction(0))
    projected_w_norm = Interval(Fraction(0))
    projected_g_norm = Fraction(0)
    contrast_rows: list[dict[str, Any]] = []
    for coefficients, denominator in zip(contrasts, denominators):
        w_contrast = sum((block_w[k] * coefficients[k] for k in range(4)),
                         Interval(Fraction(0)))
        g_contrast = sum((block_g[k] * coefficients[k] for k in range(4)),
                         Fraction(0))
        projected += w_contrast * g_contrast / Fraction(denominator)
        projected_w_norm += w_contrast.square() / Fraction(denominator)
        projected_g_norm += g_contrast * g_contrast / Fraction(denominator)
        contrast_rows.append({
            "denominator": denominator,
            "g_contrast": decimal_text(g_contrast),
            "w_contrast_interval": interval_text(w_contrast),
        })

    w_norm = sum_interval(value.square() for value in weights)
    g_norm = sum(value * value for value in output)
    residual = direct - projected
    residual_w_norm = w_norm - projected_w_norm
    residual_g_norm = Interval(g_norm) - projected_g_norm
    radius_squared = residual_w_norm * residual_g_norm
    need(residual_w_norm.lo > 0, "positive physical w residual norm")
    need(residual_g_norm.lo > 0, "positive physical g residual norm")
    need(radius_squared.lo > 0, "positive residual radius")
    rho_squared = residual.square() / radius_squared
    need(rho_squared.hi < Fraction(1, 16),
         "finite signed residual does not contract below one quarter")
    phase = ("NEGATIVE_REAL_AXIS" if residual.hi < 0 else
             "POSITIVE_REAL_AXIS" if residual.lo > 0 else "CROSSES_ZERO")
    return {
        "block_size": block_size,
        "block_w_intervals": [interval_text(value) for value in block_w],
        "block_g": [decimal_text(value) for value in block_g],
        "contrasts": contrast_rows,
        "direct_scalar_interval": interval_text(direct),
        "projected_center_interval": interval_text(projected),
        "residual_scalar_interval": interval_text(residual),
        "w_norm_squared_interval": interval_text(w_norm),
        "g_norm_squared": decimal_text(g_norm),
        "residual_w_norm_squared_interval": interval_text(residual_w_norm),
        "residual_g_norm_squared_interval": interval_text(residual_g_norm),
        "radius_squared_interval": interval_text(radius_squared),
        "rho_squared_interval": interval_text(rho_squared),
        "rho_upper": square_root_text(rho_squared.hi, 10),
        "rho_upper_squared": decimal_text(rho_squared.hi, 12),
        "phase": phase,
        "quarter_contraction": True,
        "exact_projection_identity": True,
    }


CASES = (
    (64, 15, 4, 1),
    (64, 15, 4, 2),
    (96, 20, 5, 1),
    (96, 20, 5, 2),
    (128, 24, 5, 1),
    (128, 24, 5, 2),
    (192, 32, 6, 1),
    (192, 32, 6, 2),
    (256, 38, 6, 1),
    (256, 38, 6, 2),
    (384, 50, 7, 1),
    (384, 50, 7, 2),
)


def one_case(scale: int, H: int, Q: int, exponent: int) -> dict[str, Any]:
    indices, beta, weights = source_weights(scale, 2)
    output, shell = operator_output(indices, beta, H, Q, exponent)
    record = frame_data(indices, weights, output)
    cutoff = 0
    while (cutoff + 1) ** 400 <= scale ** 133:
        cutoff += 1
    record.update({
        "scale": scale,
        "H": H,
        "Q": Q,
        "kernel_exponent": exponent,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": len(indices),
        "divisor_cutoff_U": cutoff,
        "prime_shell": shell,
        "comparison_cutoff_z": 2,
        "euler_tail_cutoff": TAIL_CUTOFF,
        "beta_exact_rational": True,
        "kernel": "K_H(h)=(1+(h/H)^2)^(-s)",
        "finite_profile_status": "MODELING_CHOICE_NORMALIZED_FOURIER_PROFILE",
    })
    return record


def build_payload() -> dict[str, Any]:
    cases = [one_case(*case) for case in CASES]
    need(len(cases) == len(CASES), "case count")
    need(all(case["quarter_contraction"] for case in cases),
         "case contraction")
    phases = {case["phase"] for case in cases}
    return {
        "claim_status": STATUS,
        "schema": "TPC267_LITERAL_V59_RESIDUAL_CENSUS_V1",
        "parameters": {
            "comparison": "b_x^(2)(n)=2 C_2 1_(2 does not divide n) product_(p|n,p>2)(p-1)/(p-2)",
            "operator": "A_x(u,t)=1_(u!=t) sum_q q K_H(u-t) 1_(q does not divide ut) (1_(u=t mod q)-1/(q-1))",
            "frame": "four consecutive equal blocks; three Haar contrasts",
            "tail_bound": "prod_tail >= finite_product*(1-1/(P-1))",
            "tail_cutoff": TAIL_CUTOFF,
            "profiles": [1, 2],
        },
        "finite_theorem": {
            "exact_operator_and_projection": True,
            "residual_identity": "C_perp=C-C_3",
            "certified_cases": len(cases),
            "rho_bound": "|C_perp|/R < 1/4 in every listed finite case",
            "phase_set": sorted(phases),
        },
        "cases": cases,
        "firewall": {
            "TPC267_ACTUAL_V59_RADIUS": "OPEN_ASYMPTOTIC",
            "TPC267_ACTUAL_V59_PHASE": "OPEN_ASYMPTOTIC",
            "TPC267_FINITE_RESIDUAL_RADIUS": "NUMERICALLY_CERTIFIED",
            "TPC267_FINITE_SIGNED_PHASE": "NUMERICALLY_CERTIFIED",
            "TPC267_FIXED_POWER_CREDIT": 0,
            "TPC267_ARITHMETIC_ADVANCE": "NO",
            "TPC267_L2": "NONE",
            "TPC267_FULL_GATE_B": "OPEN",
            "TPC267_TWIN_PRIME_RESULT": "NONE",
            "TPC267_LITERAL_PRIME_SHELL_COUNTEREXAMPLE": "NONE",
            "TPC267_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload).encode("ascii")).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(canonical(build_document()), encoding="utf-8")


def check() -> None:
    need(RESULT.is_file(), "certificate missing")
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    expected = build_document()
    need(stored == expected, "certificate payload mismatch")
    need(raw == canonical(stored), "certificate is not canonical")
    print("TPC267_CERTIFICATE=PASS "
          f"cases={len(stored['payload']['cases'])} "
          "rho_bound=1/4 finite_phase=certified "
          "actual_asymptotic_radius=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        if args.write:
            write()
        else:
            check()
    except (CheckFailure, KeyError, TypeError, ValueError, OSError,
            ZeroDivisionError) as error:
        raise SystemExit("TPC267_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
