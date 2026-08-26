#!/usr/bin/env python3
"""Standalone floating-point replay for the TPC-271 lane audit."""

from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc271_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT"
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


def replay(scale: int, height: int, q0: int, theta_text: str) -> dict[str, float | str]:
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
    projected = projected_w = projected_g = 0.0
    for contrast, denominator in zip(contrasts, denominators):
        wc = sum(contrast[j] * wb[j] for j in range(4))
        gc = sum(contrast[j] * gb[j] for j in range(4))
        projected += wc * gc / denominator
        projected_w += wc * wc / denominator
        projected_g += gc * gc / denominator
    residual = direct - projected
    w_perp = sum(w * w for w in weights) - projected_w
    g_perp = sum(g * g for g in output) - projected_g
    need(w_perp > 0 and g_perp > 0, "residual lanes")
    radius_squared = w_perp * g_perp
    abs_residual = abs(residual)
    xi = radius_squared ** 3 / scale ** 10
    xi_w = w_perp ** 3 / scale ** 5
    xi_g = g_perp ** 3 / scale ** 5
    xi_c = abs_residual ** 6 / scale ** 10
    need(xi > 0 and xi_c > 0, "normalized lanes")
    phase = ("NEGATIVE_REAL_AXIS" if residual < 0 else
             "POSITIVE_REAL_AXIS" if residual > 0 else "CROSSES_ZERO")
    return {
        "residual": residual,
        "w_perp": w_perp,
        "g_perp": g_perp,
        "radius_squared": radius_squared,
        "rho_squared": residual * residual / radius_squared,
        "xi": xi,
        "xi_w": xi_w,
        "xi_g": xi_g,
        "xi_c": xi_c,
        "amplification": xi / xi_c,
        "phase": phase,
    }


def contains(values: object, value: float) -> bool:
    need(isinstance(values, list) and len(values) == 2, "interval shape")
    lo, hi = float(values[0]), float(values[1])
    tolerance = max(2e-10 * max(abs(value), 1.0), 1e-14)
    return lo - tolerance <= value <= hi + tolerance


def semantic(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    try:
        payload = data["payload"]
        theorem = payload["finite_theorem"]
        firewall = payload["firewall"]
        parameters = payload["parameters"]
        dyadic = payload["dyadic_lane_ratios"]
        profiles = payload["profile_lane_ratios"]
        rows = payload["base_rows"] + payload["profile_rows"]
        expected_radius = [
            "RADIUS_DROP_BELOW_ONE_QUARTER", "RADIUS_RISE_ABOVE_23",
            "RADIUS_RISE_ABOVE_SEVEN",
            "RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE",
        ]
        expected_source = [
            "SOURCE_DROP_BELOW_ONE_HALF", "SOURCE_DROP_BELOW_ONE_EIGHTH",
            "SOURCE_DROP_BELOW_ONE_HALF", "SOURCE_RISE_ABOVE_ONE",
        ]
        expected_output = [
            "OUTPUT_DROP_BELOW_THREE_QUARTERS", "OUTPUT_RISE_ABOVE_230",
            "OUTPUT_RISE_ABOVE_15", "OUTPUT_DROP_BELOW_THREE_QUARTERS",
        ]
        row_shape = all(
            item["phase"] == "NEGATIVE_REAL_AXIS" and
            item["exact_projection_identity"] is True and
            item["positive_residual_lanes_certified"] is True and
            item["lane_product_encloses_radius"] is True and
            item["factorization_identity"] ==
            "Xi=Xi_W*Xi_G; Xi/Xi_C=|kappa|^(-6)"
            for item in rows)
        firewall_shape = (
            firewall["TPC271_LANE_FACTORIZATION"] == "PROVED_EXACT_FINITE" and
            firewall["TPC271_PHASE_SIGN_CENSUS"] == "NUMERICALLY_CERTIFIED_FINITE" and
            firewall["TPC271_PHASE_RADIUS_DECOUPLING"] == "NUMERICALLY_CERTIFIED_FINITE" and
            firewall["TPC271_SOURCE_LANE_PROFILE_INVARIANCE"] == "PROVED_EXACT_FINITE" and
            firewall["TPC271_OUTPUT_LANE_SPIKE"] == "NUMERICALLY_CERTIFIED_FINITE" and
            firewall["TPC271_SOURCE_LEVEL_SIGNED_PHASE"] == "OPEN_ASYMPTOTIC" and
            firewall["TPC271_SOURCE_LEVEL_RADIUS"] == "OPEN_ASYMPTOTIC" and
            firewall["TPC271_FIXED_POWER_CREDIT"] == 0 and
            firewall["TPC271_ARITHMETIC_ADVANCE"] == "NO" and
            firewall["TPC271_L2"] == "NONE" and
            firewall["TPC271_FULL_GATE_B"] == "OPEN" and
            firewall["TPC271_TWIN_PRIME_RESULT"] == "NONE" and
            firewall["TPC271_STATUS"] == STATUS
        )
        profile_shape = all(
            item["source_lane_is_profile_invariant"] is True and
            item["output_lane_classification"] ==
            "OUTPUT_PROFILE_DROP_BELOW_NINE_TENTHS" and
            item["radius_classification"] ==
            "RADIUS_PROFILE_RATIO_BETWEEN_ONE_HALF_AND_THREE_QUARTERS" and
            item["phase_sign_preserved"] is True
            for item in profiles)
        return (
            data["claim_status"] == STATUS and
            payload["schema"] == "TPC271_PHASE_RADIUS_DECOUPLING_CERTIFICATE_V1" and
            (theorem["base_rows"], theorem["profile_control_rows"],
             theorem["dyadic_lane_rows"], theorem["profile_lane_rows"],
             theorem["phase_rows"]) == (6, 3, 4, 3, 9) and
            theorem["dyadic_radius_pattern"] == "DROP_RISE_RISE_DROP" and
            theorem["phase_sign_pattern"] == "ALL_NEGATIVE_REAL_AXIS" and
            parameters["endpoint_normalization"] == "Xi=(R_squared)^3/N^10" and
            parameters["source_lane_normalization"] == "Xi_W=W_perp^3/N^5" and
            parameters["output_lane_normalization"] == "Xi_G=G_perp^3/N^5" and
            parameters["signed_scalar_normalization"] == "Xi_C=|C_perp|^6/N^10" and
            len(payload["base_rows"]) == 6 and len(payload["profile_rows"]) == 3 and
            len(payload["dyadic_lane_ratios"]) == 4 and
            len(payload["profile_lane_ratios"]) == 3 and
            tuple(item["radius_classification"] for item in dyadic) == tuple(expected_radius) and
            tuple(item["source_classification"] for item in dyadic) == tuple(expected_source) and
            tuple(item["output_classification"] for item in dyadic) == tuple(expected_output) and
            row_shape and profile_shape and firewall_shape
        )
    except (KeyError, TypeError, ValueError, IndexError):
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

    mutate(("payload", "schema"), "TPC271_V0")
    mutate(("claim_status",), "PROVED")
    mutate(("payload", "finite_theorem", "phase_sign_pattern"), "MIXED")
    mutate(("payload", "dyadic_lane_ratios", 1, "output_classification"), "DROP")
    mutate(("payload", "firewall", "TPC271_FIXED_POWER_CREDIT"), 1)
    mutate(("payload", "parameters", "endpoint_normalization"), "R/N")
    need(all(not semantic(item) for item in mutations), "mutation accepted")
    return len(mutations)


def run() -> None:
    data = json.loads(RESULT.read_text(encoding="utf-8"))
    need(semantic(data), "certificate semantics")
    payload = data["payload"]
    base = payload["base_rows"]
    profiles = payload["profile_rows"]
    for item in base + profiles:
        actual = replay(item["scale"], item["H"], item["Q"], item["profile_theta"])
        need(contains(item["residual_scalar_interval"], actual["residual"]),
             "scalar interval")
        need(contains(item["residual_w_norm_interval"], actual["w_perp"]),
             "source lane interval")
        need(contains(item["residual_g_norm_interval"], actual["g_perp"]),
             "output lane interval")
        need(contains(item["radius_squared_interval"], actual["radius_squared"]),
             "radius interval")
        need(contains(item["rho_squared_interval"], actual["rho_squared"]),
             "rho interval")
        need(contains(item["endpoint_normalized_sixth_interval"], actual["xi"]),
             "Xi interval")
        need(contains(item["source_lane_normalized_interval"], actual["xi_w"]),
             "Xi_W interval")
        need(contains(item["output_lane_normalized_interval"], actual["xi_g"]),
             "Xi_G interval")
        need(contains(item["signed_scalar_normalized_interval"], actual["xi_c"]),
             "Xi_C interval")
        need(contains(item["phase_amplification_interval"], actual["amplification"]),
             "amplification interval")
        need(item["phase"] == actual["phase"] == "NEGATIVE_REAL_AXIS",
             "phase sign")
        need(abs(actual["xi"] - actual["xi_w"] * actual["xi_g"])
             <= 1e-8 * max(actual["xi"], 1e-30), "lane identity")
    by_scale = {item["scale"]: item for item in base}
    pairs = ((64, 128), (96, 192), (128, 256), (192, 384))
    expected_radius = ("RADIUS_DROP_BELOW_ONE_QUARTER", "RADIUS_RISE_ABOVE_23",
                       "RADIUS_RISE_ABOVE_SEVEN",
                       "RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE")
    for item, (low, high), expected in zip(payload["dyadic_lane_ratios"], pairs,
                                           expected_radius):
        lo = replay(low, by_scale[low]["H"], by_scale[low]["Q"], "0/1")
        hi = replay(high, by_scale[high]["H"], by_scale[high]["Q"], "0/1")
        need(item["radius_classification"] == expected and
             item["phase_sign_preserved"] is True and
             item["phase_sign_low"] == item["phase_sign_high"] == "NEGATIVE_REAL_AXIS",
             "dyadic metadata")
        need(contains(item["radius_ratio_interval"], hi["xi"] / lo["xi"]),
             "dyadic radius ratio")
        need(contains(item["source_lane_ratio_interval"], hi["xi_w"] / lo["xi_w"]),
             "dyadic source ratio")
        need(contains(item["output_lane_ratio_interval"], hi["xi_g"] / lo["xi_g"]),
             "dyadic output ratio")
    need(mutation_audit(data) == 6, "mutation count")
    print("TPC271_INDEPENDENT_CHECK=PASS "
          f"base_rows={len(base)} dyadic_pattern=DROP_RISE_RISE_DROP "
          f"phase_rows={len(base) + len(profiles)} mutations_rejected=6 "
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
        print("TPC271_INDEPENDENT_CHECK=FAIL " + str(exc))
        raise SystemExit(1)
