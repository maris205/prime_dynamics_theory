#!/usr/bin/env python3
"""Finite adversarial stability certificate for the V59 residual interface.

The physical operator is the same finite operator audited in TPC-267.  This
certificate changes only declared finite interface parameters: the local
comparison cutoff z, the rounded clock H, and the kernel exponent s.  It
certifies both matched z=2 controls and finite rows where the quarter-sector
inequality fails.  No asymptotic conclusion is encoded.
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
RESULT = PROJECT / "results/tpc268_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION"
ROUND2_CLUE = "TEST_GROWING_CUTOFF_UNIFORMITY_BEFORE_ANY_PHASE_PROMOTION"
TAIL_CUTOFF = 50_000
GRID = 10 ** 30
LOG_GUARD = Decimal("1e-25")
THRESHOLD = Fraction(1, 16)
getcontext().prec = 100


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction, hi: Fraction | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
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
        return Interval(min(self.lo * self.lo, self.hi * self.hi),
                        max(self.lo * self.lo, self.hi * self.hi))


def as_interval(value: Interval | Fraction | int) -> Interval:
    return value if isinstance(value, Interval) else Interval(Fraction(value))


def grid_lower(value: Fraction) -> Fraction:
    numerator = value.numerator * GRID
    return Fraction(numerator // value.denominator, GRID)


def grid_upper(value: Fraction) -> Fraction:
    numerator = value.numerator * GRID
    quotient, remainder = divmod(numerator, value.denominator)
    return Fraction(quotient + int(remainder != 0), GRID)


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def decimal_text(value: Fraction, digits: int = 12) -> str:
    return format(Decimal(value.numerator) / Decimal(value.denominator),
                  f".{digits}g")


def square_root_text(value: Fraction, digits: int = 10) -> str:
    need(value >= 0, "negative square root")
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
    guard = Fraction(LOG_GUARD)
    return Interval(Fraction(center) - guard, Fraction(center) + guard)


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
    normalized = Fraction(0) if power is None else Fraction(1, power[1])
    return normalized - divisor_sum


TAIL_CACHE: dict[int, tuple[Fraction, Fraction]] = {}


def comparison_tail(z: int) -> tuple[Fraction, Fraction]:
    if z not in TAIL_CACHE:
        finite = Decimal(1)
        for prime in PRIMES:
            if prime > z:
                factor = Decimal((prime - 1) ** 2 - 1) / Decimal(
                    (prime - 1) ** 2)
                finite *= factor
        lower = finite * (1 - Decimal(1) / Decimal(TAIL_CUTOFF - 1))
        TAIL_CACHE[z] = (grid_lower(Fraction(lower)),
                         grid_upper(Fraction(finite)))
    return TAIL_CACHE[z]


def comparison_interval(value: int, z: int) -> Interval:
    if value % 2 == 0:
        return Interval(Fraction(0))
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


def source_weights(scale: int, z: int) -> tuple[list[int], list[Fraction],
                                                  list[Interval]]:
    indices = list(range(scale // 2 + 1, scale + 1))
    beta = [beta_value(value, scale) for value in indices]
    shifted = [lambda_interval(value + 2) -
               comparison_interval(value, z) for value in indices]
    return indices, beta, shifted


def kernel(shift: int, height: int, exponent: int) -> Fraction:
    return Fraction(height ** (2 * exponent),
                    (height * height + shift * shift) ** exponent)


def operator_output(indices: list[int], beta: list[Fraction], height: int,
                    q0: int, exponent: int) -> tuple[list[Fraction], list[int]]:
    shell = [prime for prime in PRIMES if q0 < prime <= 2 * q0]
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t:
                continue
            for prime in shell:
                if u % prime == 0 or t % prime == 0:
                    continue
                centered = Fraction(int(u % prime == t % prime), 1)
                centered -= Fraction(1, prime - 1)
                total += prime * kernel(u - t, height, exponent) * centered * beta_t
        output.append(total)
    return output, shell


def sum_interval(values: Iterable[Interval | Fraction]) -> Interval:
    total = Interval(Fraction(0))
    for value in values:
        total += value
    return total


def audit_case(scale: int, height: int, q0: int, exponent: int,
               z: int, role: str) -> dict[str, Any]:
    indices, beta, weights = source_weights(scale, z)
    output, shell = operator_output(indices, beta, height, q0, exponent)
    length = len(indices)
    block_size = length // 4
    blocks = [range(k * block_size, (k + 1) * block_size)
              for k in range(4)]
    block_w = [sum_interval(weights[j] for j in block) for block in blocks]
    block_g = [sum(output[j] for j in block) for block in blocks]
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block_size, 2 * block_size, 2 * block_size)
    direct = sum_interval(weights[j] * output[j] for j in range(length))
    projected = Interval(Fraction(0))
    projected_w_norm = Interval(Fraction(0))
    projected_g_norm = Fraction(0)
    contrast_rows: list[dict[str, Any]] = []
    for coefficients, denominator in zip(contrasts, denominators):
        w_contrast = sum((block_w[k] * coefficients[k]
                          for k in range(4)), Interval(Fraction(0)))
        g_contrast = sum((block_g[k] * coefficients[k]
                          for k in range(4)), Fraction(0))
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
    need(residual_w_norm.lo > 0 and residual_g_norm.lo > 0,
         "positive residual norms")
    need(radius_squared.lo > 0, "positive radius")
    rho_squared = residual.square() / radius_squared
    if rho_squared.hi < THRESHOLD:
        result = "CONTRACTION"
    elif rho_squared.lo > THRESHOLD:
        result = "OBSTRUCTION"
    else:
        result = "UNRESOLVED"
    need(result != "UNRESOLVED", "threshold not separated")
    phase = ("NEGATIVE_REAL_AXIS" if residual.hi < 0 else
             "POSITIVE_REAL_AXIS" if residual.lo > 0 else "CROSSES_ZERO")
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "kernel_exponent": exponent,
        "comparison_cutoff_z": z,
        "role": role,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": length,
        "block_size": block_size,
        "divisor_cutoff_U": max(k for k in range(0, scale + 1)
                                if (k + 1) ** 400 <= scale ** 133),
        "prime_shell": shell,
        "beta_exact_rational": True,
        "finite_profile_status": "MODELING_CHOICE_NORMALIZED_FOURIER_PROFILE",
        "kernel": "K_H(h)=(1+(h/H)^2)^(-s)",
        "block_g": [decimal_text(value) for value in block_g],
        "block_w_intervals": [interval_text(value) for value in block_w],
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
        "rho_upper_squared": decimal_text(rho_squared.hi),
        "phase": phase,
        "quarter_contraction": result == "CONTRACTION",
        "certified_obstruction": result == "OBSTRUCTION",
        "classification": result,
        "exact_projection_identity": True,
    }


CASES = (
    (64, 15, 4, 1, 2, "CONTROL_Z2"),
    (96, 20, 5, 1, 2, "CONTROL_Z2"),
    (128, 24, 5, 1, 2, "CONTROL_Z2"),
    (192, 32, 6, 1, 2, "CONTROL_Z2"),
    (256, 38, 6, 1, 2, "CONTROL_Z2"),
    (384, 50, 7, 1, 2, "CONTROL_Z2"),
    (64, 13, 4, 1, 3, "CLOCK_PERTURBATION"),
    (64, 15, 4, 1, 3, "CUTOFF_PERTURBATION"),
    (64, 17, 4, 1, 3, "CLOCK_PERTURBATION"),
    (96, 20, 5, 1, 3, "CUTOFF_PERTURBATION"),
    (96, 20, 5, 2, 3, "KERNEL_AND_CUTOFF_PERTURBATION"),
    (128, 24, 5, 1, 3, "CUTOFF_CONTROL"),
    (64, 15, 4, 1, 5, "CUTOFF_PERTURBATION"),
    (64, 15, 4, 2, 3, "KERNEL_PERTURBATION"),
    (192, 32, 6, 1, 3, "CUTOFF_CONTROL"),
    (384, 50, 7, 1, 3, "CUTOFF_CONTROL"),
)


def build_payload() -> dict[str, Any]:
    cases = [audit_case(*case) for case in CASES]
    controls = [case for case in cases if case["role"] == "CONTROL_Z2"]
    obstructions = [case for case in cases if case["certified_obstruction"]]
    need(len(controls) == 6, "control count")
    need(len(obstructions) == 6, "obstruction count")
    need(all(case["classification"] == "CONTRACTION" for case in controls),
         "control contraction")
    need(any(case["scale"] == 64 and case["comparison_cutoff_z"] == 3
             and case["kernel_exponent"] == 1
             and case["classification"] == "OBSTRUCTION" for case in cases),
         "matched cutoff obstruction")
    return {
        "claim_status": STATUS,
        "schema": "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1",
        "parameters": {
            "operator": "TPC267 literal A with prime shell, masks, and deleted diagonal",
            "comparison_family": "b^(z) with finite Euler tail and local cutoff z",
            "frame": "four consecutive equal blocks; three Haar contrasts",
            "tail_cutoff": TAIL_CUTOFF,
            "threshold_squared": "1/16",
            "profiles": [1, 2, 3],
        },
        "finite_theorem": {
            "matched_control_cases": len(controls),
            "certified_obstruction_cases": len(obstructions),
            "total_cases": len(cases),
            "statement": "same finite operator family changes classification under declared finite perturbations",
            "universal_quarter_claim": "REFUTED_SCOPED_FINITE_PARAMETER_FAMILY",
        },
        "cases": cases,
        "firewall": {
            "TPC268_FINITE_CUTOFF_OBSTRUCTION": "NUMERICALLY_CERTIFIED",
            "TPC268_MATCHED_Z2_CONTROLS": "NUMERICALLY_CERTIFIED",
            "TPC268_CLOCK_STABILITY": "REFUTED_SCOPED",
            "TPC268_KERNEL_STABILITY": "REFUTED_SCOPED",
            "TPC268_ACTUAL_V59_RADIUS": "OPEN_ASYMPTOTIC",
            "TPC268_ACTUAL_V59_PHASE": "OPEN_ASYMPTOTIC",
            "TPC268_FIXED_POWER_CREDIT": 0,
            "TPC268_ARITHMETIC_ADVANCE": "NO",
            "TPC268_L2": "NONE",
            "TPC268_FULL_GATE_B": "OPEN",
            "TPC268_TWIN_PRIME_RESULT": "NONE",
            "TPC268_STATUS": STATUS,
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
    cases = stored["payload"]["cases"]
    obstructions = sum(case["certified_obstruction"] for case in cases)
    print("TPC268_CERTIFICATE=PASS "
          f"cases={len(cases)} obstructions={obstructions} "
          "matched_controls=6 universal_quarter=REFUTED_SCOPED "
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
        raise SystemExit("TPC268_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
