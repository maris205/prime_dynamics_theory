#!/usr/bin/env python3
"""Standalone floating-point audit for TPC-270 radius normalization."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc270_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT"
PRIMES = []


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def primes_up_to(limit: int) -> list[int]:
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            sieve[p * p:limit + 1:p] = b"\x00" * ((limit - p * p) // p + 1)
    return [p for p in range(2, limit + 1) if sieve[p]]


PRIMES = primes_up_to(50000)


def factors(value: int) -> list[int]:
    result = []
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
        power, exponent = p, 1
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
    divisor_sum = sum(mobius(d) for d in range(1, cutoff + 1)
                      if value % d == 0)
    return normalized - divisor_sum


C2 = {}


def comparison_constant(z: int) -> float:
    if z not in C2:
        C2[z] = math.prod(1.0 - 1.0 / (p - 1) ** 2
                           for p in PRIMES if p > z)
    return C2[z]


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


def growing_cutoff(scale: int) -> int:
    schedule = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    need(scale in schedule, "unregistered scale")
    return schedule[scale]


def lambda_value(value: int) -> float:
    power = prime_power(value)
    return 0.0 if power is None else math.log(power[0])


def radius_squared(scale: int, height: int, q0: int,
                   theta_text: str) -> float:
    z = growing_cutoff(scale)
    numerator, denominator = (int(x) for x in theta_text.split("/"))
    theta = numerator / denominator
    indices = list(range(scale // 2 + 1, scale + 1))
    beta_values = [beta(value, scale) for value in indices]
    weights = [lambda_value(value + 2) - comparison(value, z)
               for value in indices]
    shell = [p for p in PRIMES if q0 < p <= 2 * q0]
    output_one = []
    output_two = []
    for exponent, output in ((1, output_one), (2, output_two)):
        for u in indices:
            total = 0.0
            for t, b_t in zip(indices, beta_values):
                if u == t:
                    continue
                for q in shell:
                    if u % q == 0 or t % q == 0:
                        continue
                    h = u - t
                    kernel = (height * height / (height * height + h * h)) ** exponent
                    centered = (1.0 if u % q == t % q else 0.0) - 1.0 / (q - 1)
                    total += q * kernel * centered * b_t
            output.append(total)
    output = [(1.0 - theta) * one + theta * two
              for one, two in zip(output_one, output_two)]
    block = len(indices) // 4
    blocks = [range(j * block, (j + 1) * block) for j in range(4)]
    wb = [sum(weights[i] for i in row) for row in blocks]
    gb = [sum(output[i] for i in row) for row in blocks]
    contrasts = ((1.0, 1.0, -1.0, -1.0),
                 (1.0, -1.0, 0.0, 0.0),
                 (0.0, 0.0, 1.0, -1.0))
    denominators = (4 * block, 2 * block, 2 * block)
    direct = sum(w * g for w, g in zip(weights, output))
    projected_w = projected_g = center = 0.0
    for contrast, denominator in zip(contrasts, denominators):
        wc = sum(contrast[j] * wb[j] for j in range(4))
        gc = sum(contrast[j] * gb[j] for j in range(4))
        center += wc * gc / denominator
        projected_w += wc * wc / denominator
        projected_g += gc * gc / denominator
    residual_w = sum(w * w for w in weights) - projected_w
    residual_g = sum(g * g for g in output) - projected_g
    need(residual_w > 0 and residual_g > 0, "residual norm")
    return residual_w * residual_g


def xi(scale: int, height: int, q0: int, theta: str) -> float:
    value = radius_squared(scale, height, q0, theta)
    return value ** 3 / scale ** 10


def interval_contains(interval: list[str], value: float) -> bool:
    lo, hi = (float(x) for x in interval)
    tolerance = max(1e-10 * max(abs(value), 1.0), 1e-15)
    return lo - tolerance <= value <= hi + tolerance


def semantic(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        payload = data["payload"]
        theorem = payload["finite_theorem"]
        firewall = payload["firewall"]
        if data["claim_status"] != STATUS:
            return False
        if payload["schema"] != "TPC270_CROSS_SCALE_RADIUS_NORMALIZATION_CERTIFICATE_V1":
            return False
        if (theorem["base_rows"], theorem["profile_control_rows"],
                theorem["dyadic_ratio_rows"], theorem["adjacent_ratio_rows"],
                theorem["profile_ratio_rows"]) != (6, 3, 4, 5, 3):
            return False
        if theorem["dyadic_pattern"] != "DROP_RISE_RISE_DROP":
            return False
        if payload["parameters"]["normalization"] != "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6":
            return False
        if firewall["TPC270_ENDPOINT_NORMALIZATION"] != "PROVED_EXACT_FINITE_IDENTITY":
            return False
        if firewall["TPC270_SOURCE_LEVEL_RADIUS"] != "OPEN_ASYMPTOTIC":
            return False
        if firewall["TPC270_FIXED_POWER_CREDIT"] != 0:
            return False
        if len(payload["base_rows"]) != 6 or len(payload["profile_rows"]) != 3:
            return False
        for row in payload["base_rows"] + payload["profile_rows"]:
            if not interval_contains(row["endpoint_normalized_sixth_interval"],
                                     xi(row["scale"], row["H"], row["Q"],
                                        row["profile_theta"])):
                return False
            if float(row["radius_squared_interval"][0]) <= 0:
                return False
        expected = ["DROP_BELOW_ONE_QUARTER", "RISE_ABOVE_SIXTEEN",
                    "RISE_ABOVE_SEVEN", "DROP_BETWEEN_THREE_QUARTERS_AND_ONE"]
        if [row["classification"] for row in payload["dyadic_ratios"]] != expected:
            return False
        for row in payload["dyadic_ratios"]:
            lo, hi = (float(x) for x in row["ratio_interval"])
            if not 0 < lo <= hi:
                return False
        for row in payload["profile_ratios"]:
            lo, hi = (float(x) for x in row["ratio_interval"])
            if not (0.5 < lo <= hi < 0.75):
                return False
        return True
    except (KeyError, TypeError, ValueError, IndexError, RuntimeError):
        return False


def mutation_audit(data: dict[str, object]) -> int:
    mutations = []

    def mutate(path: tuple[object, ...], value: object) -> None:
        candidate = copy.deepcopy(data)
        cursor = candidate
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        mutations.append(candidate)

    mutate(("payload", "schema"), "TPC270_V0")
    mutate(("claim_status",), "PROVED")
    mutate(("payload", "finite_theorem", "dyadic_pattern"), "STABLE")
    mutate(("payload", "dyadic_ratios", 0, "classification"), "RISE_ABOVE_SEVEN")
    mutate(("payload", "firewall", "TPC270_FIXED_POWER_CREDIT"), 1)
    mutate(("payload", "parameters", "normalization"), "R/N^(5/3)")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def run() -> None:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    need(semantic(data), "certificate semantics")
    rejected = mutation_audit(data)
    base = {row["scale"]: xi(row["scale"], row["H"], row["Q"],
                              row["profile_theta"])
            for row in data["payload"]["base_rows"]}
    profile_rows = data["payload"]["profile_rows"]
    profile = {(row["scale"], row["profile_theta"]):
               xi(row["scale"], row["H"], row["Q"], row["profile_theta"])
               for row in profile_rows}
    pairs = ((64, 128), (96, 192), (128, 256), (192, 384))
    ratios = [base[high] / base[low] for low, high in pairs]
    need(ratios[0] < 0.25 and ratios[1] > 16 and ratios[2] > 7 and
         0.75 < ratios[3] < 1.0, "dyadic replay pattern")
    for row in data["payload"]["dyadic_ratios"]:
        low, high = row["low_scale"], row["high_scale"]
        need(interval_contains(row["ratio_interval"], base[high] / base[low]),
             "dyadic interval replay")
    for row in data["payload"]["profile_ratios"]:
        scale = row["scale"]
        value = profile[(scale, row["profile_theta"])] / base[scale]
        need(0.5 < value < 0.75 and interval_contains(row["ratio_interval"], value),
             "profile ratio replay")
    need(rejected == 6, "mutation count")
    print("TPC270_INDEPENDENT_CHECK=PASS "
          f"base_rows={len(base)} dyadic_pattern=DROP_RISE_RISE_DROP "
          f"profile_controls={len(profile_rows)} mutations_rejected={rejected} "
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
        print("TPC270_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
