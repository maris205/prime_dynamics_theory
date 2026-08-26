#!/usr/bin/env python3
"""Independent finite replay for the TPC-267 residual census.

This file intentionally reimplements the numerical replay without importing
the certificate producer.  It uses a floating-point cross-check only as an
independent audit; the producer's stored interval is the declared certificate.
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc267_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_RESIDUAL_PHASE_CENSUS"


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * (
                (limit - p * p) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(50_000)


def factors(value: int) -> list[int]:
    result: list[int] = []
    remaining = value
    for p in PRIMES:
        if p * p > remaining:
            break
        if remaining % p == 0:
            result.append(p)
            while remaining % p == 0:
                remaining //= p
    if remaining > 1:
        result.append(remaining)
    return result


def mobius(value: int) -> int:
    fs = factors(value)
    if any(value % (p * p) == 0 for p in fs):
        return 0
    return -1 if len(fs) % 2 else 1


def prime_power(value: int) -> tuple[int, int] | None:
    for p in PRIMES:
        if p > value:
            break
        power = p
        exponent = 1
        while power < value:
            power *= p
            exponent += 1
        if power == value:
            return p, exponent
    return None


def beta(value: int, scale: int) -> float:
    cutoff = 0
    while (cutoff + 1) ** 400 <= scale ** 133:
        cutoff += 1
    power = prime_power(value)
    normalized = 0.0 if power is None else 1.0 / power[1]
    return normalized - sum(mobius(d) for d in range(1, cutoff + 1)
                            if value % d == 0)


def lambda_value(value: int) -> float:
    power = prime_power(value)
    return 0.0 if power is None else math.log(power[0])


C2 = math.prod(1.0 - 1.0 / (p - 1) ** 2 for p in PRIMES if p > 2)


def comparison(value: int) -> float:
    if value % 2 == 0:
        return 0.0
    result = 2.0 * C2
    for p in factors(value):
        if p > 2:
            result *= (p - 1) / (p - 2)
    return result


def replay(scale: int, H: int, Q: int, exponent: int) -> float:
    indices = list(range(scale // 2 + 1, scale + 1))
    bs = [beta(n, scale) for n in indices]
    ws = [lambda_value(n + 2) - comparison(n) for n in indices]
    shell = [p for p in PRIMES if Q < p <= 2 * Q]
    output: list[float] = []
    for u in indices:
        total = 0.0
        for t, b_t in zip(indices, bs):
            if u == t:
                continue
            for q in shell:
                if u % q == 0 or t % q == 0:
                    continue
                k = (H ** (2 * exponent) /
                     (H * H + (u - t) ** 2) ** exponent)
                centered = (1.0 if u % q == t % q else 0.0) - 1.0 / (q - 1)
                total += q * k * centered * b_t
        output.append(total)

    block = len(indices) // 4
    blocks = [range(j * block, (j + 1) * block) for j in range(4)]
    contrasts = ([1.0, 1.0, -1.0, -1.0],
                 [1.0, -1.0, 0.0, 0.0],
                 [0.0, 0.0, 1.0, -1.0])
    denominators = (4 * block, 2 * block, 2 * block)
    w_blocks = [sum(ws[j] for j in row) for row in blocks]
    g_blocks = [sum(output[j] for j in row) for row in blocks]
    direct = sum(w * g for w, g in zip(ws, output))
    center = 0.0
    w_projection = 0.0
    g_projection = 0.0
    for c, denominator in zip(contrasts, denominators):
        wc = sum(c[j] * w_blocks[j] for j in range(4))
        gc = sum(c[j] * g_blocks[j] for j in range(4))
        center += wc * gc / denominator
        w_projection += wc * wc / denominator
        g_projection += gc * gc / denominator
    residual = direct - center
    w_residual = sum(w * w for w in ws) - w_projection
    g_residual = sum(g * g for g in output) - g_projection
    need(w_residual > 0 and g_residual > 0, "independent positive residual")
    return abs(residual) / math.sqrt(w_residual * g_residual)


def semantic(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        payload = data["payload"]
        theorem = payload["finite_theorem"]
        firewall = payload["firewall"]
        cases = payload["cases"]
        if data["claim_status"] != STATUS:
            return False
        if payload["schema"] != "TPC267_LITERAL_V59_RESIDUAL_CENSUS_V1":
            return False
        if theorem["certified_cases"] != 12 or theorem["rho_bound"] != \
                "|C_perp|/R < 1/4 in every listed finite case":
            return False
        if firewall["TPC267_FIXED_POWER_CREDIT"] != 0 or \
                firewall["TPC267_ARITHMETIC_ADVANCE"] != "NO":
            return False
        if firewall["TPC267_ACTUAL_V59_RADIUS"] != "OPEN_ASYMPTOTIC":
            return False
        if firewall["TPC267_ACTUAL_V59_PHASE"] != "OPEN_ASYMPTOTIC":
            return False
        if len(cases) != 12:
            return False
        for case in cases:
            if case["comparison_cutoff_z"] != 2 or not case["quarter_contraction"]:
                return False
            if float(case["rho_upper"]) >= 0.25:
                return False
            if case["phase"] not in {"NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS"}:
                return False
            lo, hi = (float(v) for v in case["rho_squared_interval"])
            if not (0.0 <= lo <= hi < 0.0625):
                return False
        return True
    except (KeyError, TypeError, ValueError, IndexError):
        return False


def mutation_audit(data: dict[str, object]) -> int:
    mutations: list[dict[str, object]] = []

    def mutate(path: tuple[object, ...], value: object) -> None:
        candidate = copy.deepcopy(data)
        cursor: object = candidate
        for key in path[:-1]:
            cursor = cursor[key]  # type: ignore[index]
        cursor[path[-1]] = value  # type: ignore[index]
        mutations.append(candidate)

    mutate(("payload", "schema"), "TPC267_V0")
    mutate(("claim_status",), "PROVED")
    mutate(("payload", "finite_theorem", "certified_cases"), 11)
    mutate(("payload", "cases", 0, "rho_upper"), "0.9")
    mutate(("payload", "cases", 0, "phase"), "FREE_PHASE")
    mutate(("payload", "firewall", "TPC267_FIXED_POWER_CREDIT"), 1)
    mutate(("payload", "firewall", "TPC267_ACTUAL_V59_RADIUS"), "PAID")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def run() -> None:
    need(RESULT.is_file(), "certificate missing")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    need(semantic(data), "certificate semantics")
    cases = data["payload"]["cases"]
    replay_cases = 0
    for case in cases:
        observed = replay(case["scale"], case["H"], case["Q"],
                          case["kernel_exponent"])
        need(observed < 0.25, "independent quarter bound")
        need(observed <= float(case["rho_upper"]) + 0.01,
             "stored interval misses replay")
        replay_cases += 1
    rejected = mutation_audit(data)
    print("TPC267_INDEPENDENT_CHECK=PASS "
          f"replayed_cases={replay_cases} mutations_rejected={rejected} "
          "producer_imported=NO asymptotic_promotion=REJECTED")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.check, "--check required")
    run()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print("TPC267_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
