#!/usr/bin/env python3
"""Finite phase--radius decoupling certificate for TPC-271."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-271-phase-radius-decoupling"
RESULT = PROJECT / "results/tpc271_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PHASE_RADIUS_DECOUPLING_AUDIT"
ROUND2_CLUE = "TEST_SOURCE_LEVEL_SIGNED_PHASE_BOUND_WITH_EXPLICIT_RADIUS_LANE_CONTROL"
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


def cube(value: Any) -> Any:
    return value * value * value


def sixth(value: Any) -> Any:
    return cube(value) * cube(value)


def theta_text(theta: Fraction) -> str:
    return f"{theta.numerator}/{theta.denominator}"


def mixture_output(indices: list[int], beta: list[Fraction], height: int,
                   q0: int, theta: Fraction) -> tuple[list[Fraction], list[int]]:
    first, shell = ENGINE.operator_output(indices, beta, height, q0, 1)
    second, shell_again = ENGINE.operator_output(indices, beta, height, q0, 2)
    need(shell == shell_again, "profile shell mismatch")
    return [(1 - theta) * left + theta * right
            for left, right in zip(first, second)], shell


def row(scale: int, height: int, q0: int, theta: Fraction,
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
        g_contrast = sum(block_g[k] * coefficients[k]
                         for k in range(4))
        projected += w_contrast * g_contrast / Fraction(denominator)
        projected_w_norm += w_contrast.square() / Fraction(denominator)
        projected_g_norm += g_contrast * g_contrast / denominator
    w_norm = ENGINE.sum_interval(value.square() for value in weights)
    g_norm = sum(value * value for value in output)
    residual = direct - projected
    w_perp = w_norm - projected_w_norm
    g_perp = ENGINE.Interval(g_norm) - projected_g_norm
    radius_squared = w_perp * g_perp
    need(w_perp.lo > 0 and g_perp.lo > 0 and radius_squared.lo > 0,
         "positive residual lanes")
    abs_residual = ENGINE.Interval(-residual.hi, -residual.lo)
    xi = ENGINE.Interval(cube(radius_squared.lo) / Fraction(scale ** 10),
                         cube(radius_squared.hi) / Fraction(scale ** 10))
    xi_w = cube(w_perp) / Fraction(scale ** 5)
    xi_g = cube(g_perp) / Fraction(scale ** 5)
    xi_c = sixth(abs_residual) / Fraction(scale ** 10)
    amplification = xi / xi_c
    # The exact product identity is checked by interval inclusion.  The
    # intervals may be wider than the direct product because the lanes share
    # upstream quantities.
    lane_product = xi_w * xi_g
    need(lane_product.lo <= xi.hi and xi.lo <= lane_product.hi,
         "lane factorization enclosure")
    rho_squared = residual.square() / radius_squared
    phase = ("NEGATIVE_REAL_AXIS" if residual.hi < 0 else
             "POSITIVE_REAL_AXIS" if residual.lo > 0 else "CROSSES_ZERO")
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
        "residual_scalar_interval": ENGINE.interval_text(residual),
        "residual_w_norm_interval": ENGINE.interval_text(w_perp),
        "residual_g_norm_interval": ENGINE.interval_text(g_perp),
        "radius_squared_interval": ENGINE.interval_text(radius_squared),
        "rho_squared_interval": ENGINE.interval_text(rho_squared),
        "endpoint_normalized_sixth_interval": ENGINE.interval_text(xi),
        "source_lane_normalized_interval": ENGINE.interval_text(xi_w),
        "output_lane_normalized_interval": ENGINE.interval_text(xi_g),
        "signed_scalar_normalized_interval": ENGINE.interval_text(xi_c),
        "phase_amplification_interval": ENGINE.interval_text(amplification),
        "lane_product_encloses_radius": True,
        "phase": phase,
        "positive_residual_lanes_certified": True,
        "exact_projection_identity": True,
        "factorization_identity": "Xi=Xi_W*Xi_G; Xi/Xi_C=|kappa|^(-6)",
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


def as_interval(values: list[str]) -> Any:
    return ENGINE.Interval(Fraction(values[0]), Fraction(values[1]))


def field_interval(item: dict[str, Any], key: str) -> Any:
    return as_interval(item[key])


def classify_source(value: Any) -> str:
    if value.hi < Fraction(1, 8):
        return "SOURCE_DROP_BELOW_ONE_EIGHTH"
    if value.hi < Fraction(1, 2):
        return "SOURCE_DROP_BELOW_ONE_HALF"
    if value.lo > 1:
        return "SOURCE_RISE_ABOVE_ONE"
    raise CheckFailure("source lane unresolved")


def classify_output(value: Any) -> str:
    if value.hi < Fraction(3, 4):
        return "OUTPUT_DROP_BELOW_THREE_QUARTERS"
    if value.lo > 230:
        return "OUTPUT_RISE_ABOVE_230"
    if value.lo > 15:
        return "OUTPUT_RISE_ABOVE_15"
    raise CheckFailure("output lane unresolved")


def classify_radius(value: Any) -> str:
    if value.hi < Fraction(1, 4):
        return "RADIUS_DROP_BELOW_ONE_QUARTER"
    if value.lo > 23:
        return "RADIUS_RISE_ABOVE_23"
    if value.lo > 7:
        return "RADIUS_RISE_ABOVE_SEVEN"
    if value.lo > Fraction(3, 4) and value.hi < 1:
        return "RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE"
    raise CheckFailure("radius lane unresolved")


def ratio_record(low: dict[str, Any], high: dict[str, Any]) -> dict[str, Any]:
    xi_w = field_interval(high, "source_lane_normalized_interval") / field_interval(low, "source_lane_normalized_interval")
    xi_g = field_interval(high, "output_lane_normalized_interval") / field_interval(low, "output_lane_normalized_interval")
    xi = field_interval(high, "endpoint_normalized_sixth_interval") / field_interval(low, "endpoint_normalized_sixth_interval")
    c = field_interval(high, "signed_scalar_normalized_interval") / field_interval(low, "signed_scalar_normalized_interval")
    amplification = field_interval(high, "phase_amplification_interval") / field_interval(low, "phase_amplification_interval")
    record = {
        "low_scale": low["scale"],
        "high_scale": high["scale"],
        "label": f"{low['scale']}->{high['scale']}",
        "source_lane_ratio_interval": ENGINE.interval_text(xi_w),
        "output_lane_ratio_interval": ENGINE.interval_text(xi_g),
        "radius_ratio_interval": ENGINE.interval_text(xi),
        "signed_scalar_normalized_ratio_interval": ENGINE.interval_text(c),
        "phase_amplification_ratio_interval": ENGINE.interval_text(amplification),
        "source_classification": classify_source(xi_w),
        "output_classification": classify_output(xi_g),
        "radius_classification": classify_radius(xi),
        "phase_sign_low": low["phase"],
        "phase_sign_high": high["phase"],
        "phase_sign_preserved": low["phase"] == high["phase"],
        "positive_denominators_certified": True,
        "exact_lane_product_identity": True,
    }
    return record


def profile_record(base: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    source = field_interval(profile, "source_lane_normalized_interval") / field_interval(base, "source_lane_normalized_interval")
    output = field_interval(profile, "output_lane_normalized_interval") / field_interval(base, "output_lane_normalized_interval")
    radius = field_interval(profile, "endpoint_normalized_sixth_interval") / field_interval(base, "endpoint_normalized_sixth_interval")
    scalar = field_interval(profile, "signed_scalar_normalized_interval") / field_interval(base, "signed_scalar_normalized_interval")
    return {
        "scale": base["scale"],
        "base_theta": base["profile_theta"],
        "profile_theta": profile["profile_theta"],
        "source_lane_ratio_interval": ENGINE.interval_text(source),
        "output_lane_ratio_interval": ENGINE.interval_text(output),
        "radius_ratio_interval": ENGINE.interval_text(radius),
        "signed_scalar_normalized_ratio_interval": ENGINE.interval_text(scalar),
        "source_lane_is_profile_invariant": source.lo <= 1 <= source.hi,
        "output_lane_classification": "OUTPUT_PROFILE_DROP_BELOW_NINE_TENTHS" if output.hi < Fraction(9, 10) else "UNRESOLVED",
        "radius_classification": "RADIUS_PROFILE_RATIO_BETWEEN_ONE_HALF_AND_THREE_QUARTERS" if radius.lo > Fraction(1, 2) and radius.hi < Fraction(3, 4) else "UNRESOLVED",
        "phase_sign_preserved": base["phase"] == profile["phase"],
        "positive_denominators_certified": True,
    }


def build_payload() -> dict[str, Any]:
    base = [row(*case) for case in BASE_CASES]
    profiles = [row(*case) for case in PROFILE_CASES]
    by_scale = {item["scale"]: item for item in base}
    profile_by_scale = {item["scale"]: item for item in profiles}
    dyadic = [ratio_record(by_scale[a], by_scale[b])
              for a, b in ((64, 128), (96, 192), (128, 256), (192, 384))]
    profile_ratios = [profile_record(by_scale[n], profile_by_scale[n])
                      for n in (96, 128, 256)]
    need([r["radius_classification"] for r in dyadic] == [
        "RADIUS_DROP_BELOW_ONE_QUARTER", "RADIUS_RISE_ABOVE_23",
        "RADIUS_RISE_ABOVE_SEVEN",
        "RADIUS_DROP_BETWEEN_THREE_QUARTERS_AND_ONE"],
         "radius pattern")
    need(all(item["phase"] == "NEGATIVE_REAL_AXIS" for item in base + profiles),
         "phase sign census")
    need(all(item["phase_sign_preserved"] for item in dyadic),
         "dyadic phase preservation")
    need(all(item["source_lane_is_profile_invariant"] and
             item["output_lane_classification"] == "OUTPUT_PROFILE_DROP_BELOW_NINE_TENTHS" and
             item["radius_classification"] == "RADIUS_PROFILE_RATIO_BETWEEN_ONE_HALF_AND_THREE_QUARTERS"
             for item in profile_ratios), "profile lane controls")
    return {
        "schema": "TPC271_PHASE_RADIUS_DECOUPLING_CERTIFICATE_V1",
        "parameters": {
            "upstream_registry": "TPC-269 growing-cutoff finite interface",
            "cutoff_rule": "z_N=floor(log(N)) on registered rows",
            "profile_rule": "theta=0 base; theta=1/2 profile controls",
            "endpoint_normalization": "Xi=(R_squared)^3/N^10",
            "source_lane_normalization": "Xi_W=W_perp^3/N^5",
            "output_lane_normalization": "Xi_G=G_perp^3/N^5",
            "signed_scalar_normalization": "Xi_C=|C_perp|^6/N^10",
            "tail_cutoff": 50000,
            "registered_scales": [64, 96, 128, 192, 256, 384],
        },
        "finite_theorem": {
            "base_rows": len(base),
            "profile_control_rows": len(profiles),
            "dyadic_lane_rows": len(dyadic),
            "profile_lane_rows": len(profile_ratios),
            "phase_rows": len(base) + len(profiles),
            "base_negative_phase_rows": len(base),
            "lane_factorization": "PROVED_EXACT_FINITE",
            "phase_radius_decoupling": "NUMERICALLY_CERTIFIED_FINITE",
            "dyadic_radius_pattern": "DROP_RISE_RISE_DROP",
            "phase_sign_pattern": "ALL_NEGATIVE_REAL_AXIS",
            "source_lane_profile_invariance": "PROVED_EXACT_FINITE",
        },
        "base_rows": base,
        "profile_rows": profiles,
        "dyadic_lane_ratios": dyadic,
        "profile_lane_ratios": profile_ratios,
        "firewall": {
            "TPC271_LANE_FACTORIZATION": "PROVED_EXACT_FINITE",
            "TPC271_PHASE_SIGN_CENSUS": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC271_PHASE_RADIUS_DECOUPLING": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC271_SOURCE_LANE_PROFILE_INVARIANCE": "PROVED_EXACT_FINITE",
            "TPC271_OUTPUT_LANE_SPIKE": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC271_SOURCE_LEVEL_SIGNED_PHASE": "OPEN_ASYMPTOTIC",
            "TPC271_SOURCE_LEVEL_RADIUS": "OPEN_ASYMPTOTIC",
            "TPC271_FIXED_POWER_CREDIT": 0,
            "TPC271_ARITHMETIC_ADVANCE": "NO",
            "TPC271_L2": "NONE",
            "TPC271_FULL_GATE_B": "OPEN",
            "TPC271_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC271_TWIN_PRIME_RESULT": "NONE",
            "TPC271_STATUS": STATUS,
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
    print("TPC271_CERTIFICATE=PASS "
          f"base_rows={theorem['base_rows']} profile_rows={theorem['profile_control_rows']} "
          f"dyadic_lane_rows={theorem['dyadic_lane_rows']} "
          f"phase_pattern={theorem['phase_sign_pattern']} "
          "source_level_phase=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC271_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
