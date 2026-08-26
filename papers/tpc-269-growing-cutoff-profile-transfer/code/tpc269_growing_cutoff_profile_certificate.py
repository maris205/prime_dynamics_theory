#!/usr/bin/env python3
"""Finite growing-cutoff and convex-profile transfer certificate for TPC-269."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-269-growing-cutoff-profile-transfer"
RESULT = PROJECT / "results/tpc269_certificate.json"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_GROWING_CUTOFF_PROFILE_TRANSFER"
ROUND2_CLUE = "TEST_CROSS_SCALE_RADIUS_NORMALIZATION_AFTER_SOURCE_COMPATIBLE_PROFILE"
THRESHOLD = Fraction(1, 16)
UPSTREAM_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"

spec = importlib.util.spec_from_file_location("tpc268_engine", UPSTREAM_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("upstream engine unavailable")
UPSTREAM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(UPSTREAM)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def growing_cutoff(scale: int) -> int:
    schedule = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    need(scale in schedule, "unregistered scale")
    return schedule[scale]


def mixture_output(indices: list[int], beta: list[Fraction], height: int,
                   q0: int, theta: Fraction) -> tuple[list[Fraction], list[int]]:
    first, shell = UPSTREAM.operator_output(indices, beta, height, q0, 1)
    second, shell_again = UPSTREAM.operator_output(indices, beta, height, q0, 2)
    need(shell == shell_again, "profile shell mismatch")
    return [(1 - theta) * a + theta * b for a, b in zip(first, second)], shell


def theta_text(theta: Fraction) -> str:
    return str(theta.numerator) + "/" + str(theta.denominator)


def audit_case(scale: int, height: int, q0: int, theta: Fraction,
               role: str) -> dict[str, Any]:
    z = growing_cutoff(scale)
    indices, beta, weights = UPSTREAM.source_weights(scale, z)
    output, shell = mixture_output(indices, beta, height, q0, theta)
    length = len(indices)
    block_size = length // 4
    blocks = [range(k * block_size, (k + 1) * block_size)
              for k in range(4)]
    block_w = [UPSTREAM.sum_interval(weights[j] for j in block)
               for block in blocks]
    block_g = [sum(output[j] for j in block) for block in blocks]
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block_size, 2 * block_size, 2 * block_size)
    direct = UPSTREAM.sum_interval(weights[j] * output[j]
                                   for j in range(length))
    projected = UPSTREAM.Interval(Fraction(0))
    projected_w_norm = UPSTREAM.Interval(Fraction(0))
    projected_g_norm = Fraction(0)
    for coefficients, denominator in zip(contrasts, denominators):
        w_contrast = sum((block_w[k] * coefficients[k]
                          for k in range(4)),
                         UPSTREAM.Interval(Fraction(0)))
        g_contrast = sum(block_g[k] * coefficients[k] for k in range(4))
        projected += w_contrast * g_contrast / Fraction(denominator)
        projected_w_norm += w_contrast.square() / Fraction(denominator)
        projected_g_norm += g_contrast * g_contrast / denominator
    w_norm = UPSTREAM.sum_interval(value.square() for value in weights)
    g_norm = sum(value * value for value in output)
    residual = direct - projected
    residual_w_norm = w_norm - projected_w_norm
    residual_g_norm = UPSTREAM.Interval(g_norm) - projected_g_norm
    radius_squared = residual_w_norm * residual_g_norm
    need(residual_w_norm.lo > 0 and residual_g_norm.lo > 0,
         "nonpositive residual norm")
    rho_squared = residual.square() / radius_squared
    if rho_squared.hi < THRESHOLD:
        classification = "CONTRACTION"
    elif rho_squared.lo > THRESHOLD:
        classification = "OBSTRUCTION"
    else:
        raise CheckFailure("threshold unresolved")
    phase = ("NEGATIVE_REAL_AXIS" if residual.hi < 0 else
             "POSITIVE_REAL_AXIS" if residual.lo > 0 else "CROSSES_ZERO")
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": z,
        "profile_theta": theta_text(theta),
        "profile_theta_numerator": theta.numerator,
        "profile_theta_denominator": theta.denominator,
        "role": role,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": length,
        "block_size": block_size,
        "prime_shell": shell,
        "beta_exact_rational": True,
        "finite_profile_status": "CONVEX_MIXTURE_OF_TWO_NORMALIZED_NONNEGATIVE_PROFILES",
        "kernel_family": "(1-theta)K_(H,1)+theta K_(H,2)",
        "residual_scalar_interval": UPSTREAM.interval_text(residual),
        "radius_squared_interval": UPSTREAM.interval_text(radius_squared),
        "rho_squared_interval": UPSTREAM.interval_text(rho_squared),
        "rho_upper": UPSTREAM.square_root_text(rho_squared.hi, 10),
        "rho_upper_squared": UPSTREAM.decimal_text(rho_squared.hi),
        "phase": phase,
        "classification": classification,
        "quarter_contraction": classification == "CONTRACTION",
        "certified_obstruction": classification == "OBSTRUCTION",
        "exact_projection_identity": True,
    }


CASES = (
    (64, 15, 4, Fraction(0), "GROWING_CUTOFF_BASE"),
    (96, 20, 5, Fraction(0), "GROWING_CUTOFF_BASE"),
    (128, 24, 5, Fraction(0), "GROWING_CUTOFF_BASE"),
    (192, 32, 6, Fraction(0), "GROWING_CUTOFF_BASE"),
    (256, 38, 6, Fraction(0), "GROWING_CUTOFF_BASE"),
    (384, 50, 7, Fraction(0), "GROWING_CUTOFF_BASE"),
    (64, 15, 4, Fraction(9, 10), "PROFILE_OBSTRUCTION"),
    (64, 15, 4, Fraction(24, 25), "PROFILE_CONTRACTION"),
    (64, 15, 4, Fraction(1), "PROFILE_ENDPOINT"),
    (96, 20, 5, Fraction(1, 2), "PROFILE_OBSTRUCTION"),
    (128, 24, 5, Fraction(1, 2), "PROFILE_CONTROL"),
    (256, 38, 6, Fraction(1, 2), "PROFILE_CONTROL"),
)


def build_payload() -> dict[str, Any]:
    cases = [audit_case(*case) for case in CASES]
    contractions = [case for case in cases
                    if case["classification"] == "CONTRACTION"]
    obstructions = [case for case in cases
                    if case["classification"] == "OBSTRUCTION"]
    need(len(cases) == 12 and len(contractions) == 8 and
         len(obstructions) == 4, "classification counts")
    central_obstruction = next(case for case in cases
                               if case["profile_theta"] == "9/10")
    central_contraction = next(case for case in cases
                               if case["profile_theta"] == "24/25")
    need(central_obstruction["classification"] == "OBSTRUCTION" and
         central_contraction["classification"] == "CONTRACTION",
         "profile path flip")
    return {
        "schema": "TPC269_GROWING_CUTOFF_PROFILE_TRANSFER_CERTIFICATE_V1",
        "parameters": {
            "cutoff_rule": "z_N=floor(log(N)) on registered rows",
            "profile_rule": "psi_theta=(1-theta)psi_1+theta psi_2",
            "kernel_rule": "K_theta=(1-theta)K_1+theta K_2",
            "tail_cutoff": 50000,
            "threshold_squared": "1/16",
            "registered_scales": [64, 96, 128, 192, 256, 384],
        },
        "finite_theorem": {
            "total_cases": 12,
            "certified_contractions": 8,
            "certified_obstructions": 4,
            "growing_cutoff_rows": 6,
            "profile_path_rows": 6,
            "universal_quarter_claim": "REFUTED_SCOPED_GROWING_PROXY_FAMILY",
            "matched_profile_flip": "9/10_OBSTRUCTION_TO_24/25_CONTRACTION",
        },
        "cases": cases,
        "firewall": {
            "TPC269_GROWING_CUTOFF_PROXY": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC269_PROFILE_MIXTURE_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC269_PROFILE_PATH_FLIP": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC269_GROWING_UNIFORMITY": "OPEN_ASYMPTOTIC",
            "TPC269_ACTUAL_V59_RADIUS": "OPEN_ASYMPTOTIC",
            "TPC269_ACTUAL_V59_PHASE": "OPEN_ASYMPTOTIC",
            "TPC269_FIXED_POWER_CREDIT": 0,
            "TPC269_ARITHMETIC_ADVANCE": "NO",
            "TPC269_L2": "NONE",
            "TPC269_FULL_GATE_B": "OPEN",
            "TPC269_TWIN_PRIME_RESULT": "NONE",
            "TPC269_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    canonical = json.dumps(payload, ensure_ascii=True, sort_keys=True,
                            separators=(",", ":")) + "\n"
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(document(), ensure_ascii=True,
                                  sort_keys=True, separators=(",", ":")) + "\n",
                       encoding="utf-8")


def check() -> None:
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    expected = document()
    need(stored == expected, "certificate mismatch")
    canonical = json.dumps(stored, ensure_ascii=True, sort_keys=True,
                           separators=(",", ":")) + "\n"
    need(raw == canonical, "certificate not canonical")
    cases = stored["payload"]["cases"]
    print("TPC269_CERTIFICATE=PASS "
          f"cases={len(cases)} contractions=8 obstructions=4 "
          "growing_cutoff=FINITE_PROXY profile_flip=YES "
          "actual_asymptotic_radius=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC269_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
