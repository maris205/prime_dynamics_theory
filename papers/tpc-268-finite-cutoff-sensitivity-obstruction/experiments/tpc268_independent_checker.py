#!/usr/bin/env python3
"""Independent float replay of the TPC-268 cutoff-sensitivity audit."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc268_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_LITERAL_V59_CUTOFF_SENSITIVITY_OBSTRUCTION"
THRESHOLD = 0.25
PRIMES = []


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


C2_BY_Z: dict[int, float] = {}


def comparison_constant(z: int) -> float:
    if z not in C2_BY_Z:
        C2_BY_Z[z] = math.prod(
            1.0 - 1.0 / (p - 1) ** 2 for p in PRIMES if p > z)
    return C2_BY_Z[z]


def comparison(value: int, z: int) -> float:
    if value % 2 == 0:
        return 0.0
    for p in PRIMES:
        if p > z:
            break
        if (value + 2) % p == 0:
            return 0.0
    result = comparison_constant(z)
    for p in PRIMES:
        if p > z:
            break
        result *= p / (p - 1)
    for p in factors(value):
        if p > z:
            result *= (p - 1) / (p - 2)
    return result


def lambda_value(value: int) -> float:
    power = prime_power(value)
    return 0.0 if power is None else math.log(power[0])


def replay(scale: int, height: int, q0: int, exponent: int,
           z: int) -> float:
    indices = list(range(scale // 2 + 1, scale + 1))
    bs = [beta(value, scale) for value in indices]
    ws = [lambda_value(value + 2) - comparison(value, z)
          for value in indices]
    shell = [p for p in PRIMES if q0 < p <= 2 * q0]
    output: list[float] = []
    for u in indices:
        total = 0.0
        for t, b_t in zip(indices, bs):
            if u == t:
                continue
            for q in shell:
                if u % q == 0 or t % q == 0:
                    continue
                kernel = height ** (2 * exponent) / (
                    height * height + (u - t) ** 2) ** exponent
                centered = (1.0 if u % q == t % q else 0.0) - 1.0 / (q - 1)
                total += q * kernel * centered * b_t
        output.append(total)

    block = len(indices) // 4
    blocks = [range(j * block, (j + 1) * block) for j in range(4)]
    w_blocks = [sum(ws[j] for j in row) for row in blocks]
    g_blocks = [sum(output[j] for j in row) for row in blocks]
    contrasts = ((1.0, 1.0, -1.0, -1.0),
                 (1.0, -1.0, 0.0, 0.0),
                 (0.0, 0.0, 1.0, -1.0))
    denominators = (4 * block, 2 * block, 2 * block)
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
    need(w_residual > 0 and g_residual > 0, "positive residual norms")
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
        if payload["schema"] != "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1":
            return False
        if theorem["matched_control_cases"] != 6 or \
                theorem["certified_obstruction_cases"] != 6 or \
                theorem["total_cases"] != 16:
            return False
        if theorem["universal_quarter_claim"] != \
                "REFUTED_SCOPED_FINITE_PARAMETER_FAMILY":
            return False
        if firewall["TPC268_FINITE_CUTOFF_OBSTRUCTION"] != \
                "NUMERICALLY_CERTIFIED":
            return False
        if firewall["TPC268_ACTUAL_V59_RADIUS"] != "OPEN_ASYMPTOTIC":
            return False
        if firewall["TPC268_FIXED_POWER_CREDIT"] != 0:
            return False
        if len(cases) != 16:
            return False
        for case in cases:
            rho = float(case["rho_upper"])
            lo, hi = (float(value) for value in case["rho_squared_interval"])
            if not (0.0 < lo <= hi and float(case["radius_squared_interval"][0]) > 0):
                return False
            if not (case["classification"] in {"CONTRACTION", "OBSTRUCTION"}):
                return False
            if case["classification"] == "CONTRACTION":
                if not (hi < 1.0 / 16.0 and rho < THRESHOLD):
                    return False
            else:
                if not (lo > 1.0 / 16.0 and rho > THRESHOLD):
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

    mutate(("payload", "schema"), "TPC268_V0")
    mutate(("claim_status",), "PROVED")
    mutate(("payload", "finite_theorem", "certified_obstruction_cases"), 0)
    mutate(("payload", "cases", 0, "classification"), "OBSTRUCTION")
    mutate(("payload", "cases", 7, "rho_upper"), "0.1")
    mutate(("payload", "firewall", "TPC268_FIXED_POWER_CREDIT"), 1)
    mutate(("payload", "firewall", "TPC268_ACTUAL_V59_RADIUS"), "PAID")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def run() -> None:
    need(RESULT.is_file(), "certificate missing")
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    need(semantic(data), "certificate semantics")
    cases = data["payload"]["cases"]
    controls = obstructions = 0
    for case in cases:
        observed = replay(case["scale"], case["H"], case["Q"],
                          case["kernel_exponent"],
                          case["comparison_cutoff_z"])
        if case["classification"] == "CONTRACTION":
            need(observed < THRESHOLD, "control replay crossed threshold")
            controls += 1
        else:
            need(observed > THRESHOLD, "obstruction replay missed")
            obstructions += 1
    rejected = mutation_audit(data)
    need(controls == 10 and obstructions == 6,
         "classification count")
    print("TPC268_INDEPENDENT_CHECK=PASS "
          f"replayed_cases={len(cases)} controls={controls} "
          f"obstructions={obstructions} mutations_rejected={rejected} "
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
        print("TPC268_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
