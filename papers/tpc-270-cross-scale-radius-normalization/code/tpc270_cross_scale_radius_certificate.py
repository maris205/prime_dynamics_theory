#!/usr/bin/env python3
"""Finite cross-scale endpoint-normalized radius certificate for TPC-270."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-270-cross-scale-radius-normalization"
RESULT = PROJECT / "results/tpc270_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT"
ROUND2_CLUE = "TEST_SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_NORMALIZATION"
THRESHOLD_DROP = Fraction(1, 4)
THRESHOLD_RISE = Fraction(16)
UPSTREAM_PATH = ROOT / "papers/tpc-269-growing-cutoff-profile-transfer/code/tpc269_growing_cutoff_profile_certificate.py"

spec = importlib.util.spec_from_file_location("tpc269_engine", UPSTREAM_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("upstream engine unavailable")
UPSTREAM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(UPSTREAM)
ENGINE = UPSTREAM.UPSTREAM


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def theta_text(theta: Fraction) -> str:
    return f"{theta.numerator}/{theta.denominator}"


def mixture_output(indices: list[int], beta: list[Fraction], height: int,
                   q0: int, theta: Fraction) -> tuple[list[Fraction], list[int]]:
    first, shell = ENGINE.operator_output(indices, beta, height, q0, 1)
    second, shell_again = ENGINE.operator_output(indices, beta, height, q0, 2)
    need(shell == shell_again, "profile shell mismatch")
    output = [(1 - theta) * left + theta * right
              for left, right in zip(first, second)]
    return output, shell


def radius_row(scale: int, height: int, q0: int, theta: Fraction,
               role: str) -> dict[str, Any]:
    cutoff = UPSTREAM.growing_cutoff(scale)
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    output, shell = mixture_output(indices, beta, height, q0, theta)
    length = len(indices)
    block_size = length // 4
    blocks = [range(k * block_size, (k + 1) * block_size)
              for k in range(4)]
    block_w = [ENGINE.sum_interval(weights[j] for j in block)
               for block in blocks]
    block_g = [sum(output[j] for j in block) for block in blocks]
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block_size, 2 * block_size, 2 * block_size)
    direct = ENGINE.sum_interval(weights[j] * output[j]
                                 for j in range(length))
    projected = ENGINE.Interval(Fraction(0))
    projected_w_norm = ENGINE.Interval(Fraction(0))
    projected_g_norm = Fraction(0)
    for coefficients, denominator in zip(contrasts, denominators):
        w_contrast = sum((block_w[k] * coefficients[k]
                          for k in range(4)), ENGINE.Interval(Fraction(0)))
        g_contrast = sum(block_g[k] * coefficients[k] for k in range(4))
        projected += w_contrast * g_contrast / Fraction(denominator)
        projected_w_norm += w_contrast.square() / Fraction(denominator)
        projected_g_norm += g_contrast * g_contrast / denominator
    w_norm = ENGINE.sum_interval(value.square() for value in weights)
    g_norm = sum(value * value for value in output)
    residual_w_norm = w_norm - projected_w_norm
    residual_g_norm = ENGINE.Interval(g_norm) - projected_g_norm
    radius_squared = residual_w_norm * residual_g_norm
    need(residual_w_norm.lo > 0 and residual_g_norm.lo > 0 and
         radius_squared.lo > 0, "positive residual radius")
    xi = ENGINE.Interval(
        radius_squared.lo ** 3 / Fraction(scale ** 10),
        radius_squared.hi ** 3 / Fraction(scale ** 10),
    )
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "profile_theta": theta_text(theta),
        "profile_theta_numerator": theta.numerator,
        "profile_theta_denominator": theta.denominator,
        "role": role,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": length,
        "block_size": block_size,
        "prime_shell": shell,
        "radius_squared_interval": ENGINE.interval_text(radius_squared),
        "endpoint_normalized_sixth_interval": ENGINE.interval_text(xi),
        "normalization_identity": "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6",
        "exact_projection_identity": True,
        "positive_radius_certified": True,
    }


BASE_CASES = (
    (64, 15, 4, Fraction(0), "GROWING_CUTOFF_BASE"),
    (96, 20, 5, Fraction(0), "GROWING_CUTOFF_BASE"),
    (128, 24, 5, Fraction(0), "GROWING_CUTOFF_BASE"),
    (192, 32, 6, Fraction(0), "GROWING_CUTOFF_BASE"),
    (256, 38, 6, Fraction(0), "GROWING_CUTOFF_BASE"),
    (384, 50, 7, Fraction(0), "GROWING_CUTOFF_BASE"),
)

PROFILE_CASES = (
    (96, 20, 5, Fraction(1, 2), "PROFILE_CONTROL"),
    (128, 24, 5, Fraction(1, 2), "PROFILE_CONTROL"),
    (256, 38, 6, Fraction(1, 2), "PROFILE_CONTROL"),
)


def index_rows(rows: list[dict[str, Any]]) -> dict[tuple[int, str], dict[str, Any]]:
    return {(row["scale"], row["profile_theta"]): row for row in rows}


def xi_interval(row: dict[str, Any]) -> Any:
    values = row["endpoint_normalized_sixth_interval"]
    return ENGINE.Interval(Fraction(values[0]), Fraction(values[1]))


def ratio_record(low: dict[str, Any], high: dict[str, Any],
                 role: str, label: str) -> dict[str, Any]:
    ratio = xi_interval(high) / xi_interval(low)
    return {
        "low_scale": low["scale"],
        "high_scale": high["scale"],
        "label": label,
        "role": role,
        "ratio_interval": ENGINE.interval_text(ratio),
        "positive_denominator_certified": True,
    }


def profile_ratio_record(base: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    ratio = xi_interval(profile) / xi_interval(base)
    return {
        "scale": base["scale"],
        "base_theta": base["profile_theta"],
        "profile_theta": profile["profile_theta"],
        "ratio_interval": ENGINE.interval_text(ratio),
        "role": "PROFILE_TO_BASE_RATIO",
    }


def classify_dyadic(ratio: Any) -> str:
    if ratio.hi < THRESHOLD_DROP:
        return "DROP_BELOW_ONE_QUARTER"
    if ratio.lo > THRESHOLD_RISE:
        return "RISE_ABOVE_SIXTEEN"
    if ratio.lo > 7:
        return "RISE_ABOVE_SEVEN"
    if ratio.lo > Fraction(3, 4) and ratio.hi < 1:
        return "DROP_BETWEEN_THREE_QUARTERS_AND_ONE"
    raise CheckFailure("dyadic ratio unresolved")


def classify_adjacent(ratio: Any) -> str:
    if ratio.hi < Fraction(1, 2):
        return "DROP_BELOW_ONE_HALF"
    if ratio.lo > 16:
        return "RISE_ABOVE_SIXTEEN"
    if ratio.lo > 4:
        return "RISE_ABOVE_FOUR"
    if ratio.hi < Fraction(1, 4):
        return "DROP_BELOW_ONE_QUARTER"
    if ratio.hi < Fraction(3, 4):
        return "DROP_BELOW_THREE_QUARTERS"
    raise CheckFailure("adjacent ratio unresolved")


def build_payload() -> dict[str, Any]:
    base = [radius_row(*case) for case in BASE_CASES]
    profile = [radius_row(*case) for case in PROFILE_CASES]
    base_by_scale = {row["scale"]: row for row in base}
    profile_by_key = index_rows(profile)
    dyadic_pairs = ((64, 128), (96, 192), (128, 256), (192, 384))
    dyadic = []
    for low, high in dyadic_pairs:
        record = ratio_record(base_by_scale[low], base_by_scale[high],
                              "DYADIC_SCALE_RATIO", f"{low}->{high}")
        ratio = ENGINE.Interval(Fraction(record["ratio_interval"][0]),
                                Fraction(record["ratio_interval"][1]))
        record["classification"] = classify_dyadic(ratio)
        dyadic.append(record)
    adjacent_pairs = ((64, 96), (96, 128), (128, 192), (192, 256), (256, 384))
    adjacent = []
    for low, high in adjacent_pairs:
        record = ratio_record(base_by_scale[low], base_by_scale[high],
                              "ADJACENT_SCALE_RATIO", f"{low}->{high}")
        ratio = ENGINE.Interval(Fraction(record["ratio_interval"][0]),
                                Fraction(record["ratio_interval"][1]))
        record["classification"] = classify_adjacent(ratio)
        adjacent.append(record)
    profile_ratios = []
    for scale in (96, 128, 256):
        profile_ratios.append(profile_ratio_record(
            base_by_scale[scale], profile_by_key[(scale, "1/2")]))
    need([row["classification"] for row in dyadic] == [
        "DROP_BELOW_ONE_QUARTER", "RISE_ABOVE_SIXTEEN",
        "RISE_ABOVE_SEVEN", "DROP_BETWEEN_THREE_QUARTERS_AND_ONE"],
         "dyadic pattern")
    for record in profile_ratios:
        ratio = ENGINE.Interval(Fraction(record["ratio_interval"][0]),
                                Fraction(record["ratio_interval"][1]))
        need(ratio.lo > Fraction(1, 2) and ratio.hi < Fraction(3, 4),
             "profile control band")
    return {
        "schema": "TPC270_CROSS_SCALE_RADIUS_NORMALIZATION_CERTIFICATE_V1",
        "parameters": {
            "cutoff_rule": "z_N=floor(log(N)) on registered rows",
            "profile_rule": "theta=0 base; theta=1/2 profile controls",
            "endpoint_baseline_exponent": "5/3",
            "normalization": "Xi=(R_squared)^3/N^10=(R/N^(5/3))^6",
            "tail_cutoff": 50000,
            "registered_scales": [64, 96, 128, 192, 256, 384],
        },
        "finite_theorem": {
            "base_rows": len(base),
            "profile_control_rows": len(profile),
            "dyadic_ratio_rows": len(dyadic),
            "adjacent_ratio_rows": len(adjacent),
            "profile_ratio_rows": len(profile_ratios),
            "dyadic_pattern": "DROP_RISE_RISE_DROP",
            "normalized_radius_variation": "NUMERICALLY_CERTIFIED_FINITE",
            "profile_control_band": "1/2<Xi_profile/Xi_base<3/4",
            "asymptotic_radius_claim": "OPEN",
        },
        "base_rows": base,
        "profile_rows": profile,
        "dyadic_ratios": dyadic,
        "adjacent_ratios": adjacent,
        "profile_ratios": profile_ratios,
        "firewall": {
            "TPC270_ENDPOINT_NORMALIZATION": "PROVED_EXACT_FINITE_IDENTITY",
            "TPC270_CROSS_SCALE_VARIATION": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC270_PROFILE_CONTROL": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC270_SOURCE_LEVEL_RADIUS": "OPEN_ASYMPTOTIC",
            "TPC270_SOURCE_LEVEL_PHASE": "OPEN_ASYMPTOTIC",
            "TPC270_FIXED_POWER_CREDIT": 0,
            "TPC270_ARITHMETIC_ADVANCE": "NO",
            "TPC270_L2": "NONE",
            "TPC270_FULL_GATE_B": "OPEN",
            "TPC270_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC270_TWIN_PRIME_RESULT": "NONE",
            "TPC270_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    canonical = json.dumps(payload, ensure_ascii=True, sort_keys=True,
                            separators=(",", ":")) + "\n"
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(document(), ensure_ascii=True, sort_keys=True,
                                 separators=(",", ":")) + "\n", encoding="utf-8")


def check() -> None:
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    expected = document()
    need(stored == expected, "certificate mismatch")
    canonical = json.dumps(stored, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")) + "\n"
    need(raw == canonical, "certificate not canonical")
    theorem = stored["payload"]["finite_theorem"]
    print("TPC270_CERTIFICATE=PASS "
          f"base_rows={theorem['base_rows']} profile_rows={theorem['profile_control_rows']} "
          f"dyadic_ratios={theorem['dyadic_ratio_rows']} pattern={theorem['dyadic_pattern']} "
          "source_level_radius=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC270_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
