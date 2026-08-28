#!/usr/bin/env python3
"""Exact finite signed-Schur cancellation atlas for TPC-291.

TPC-290 separated diffuse nonnegative weights from sparse sign-flip escape.
This release quantifies the signed two-prime direction behind both branches.
For each Gram pair it records the exact orthogonal-projection residual
`1-Gamma` and the sign of the optimal coefficient.  The scan is finite and
does not claim a multi-prime or asymptotic cancellation theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT290_CODE = ROOT / (
    "papers/tpc-290-adaptive-shell-weighting-obstruction/code/"
    "tpc290_adaptive_shell_weighting_certificate.py")
PARENT290_RESULT = ROOT / (
    "papers/tpc-290-adaptive-shell-weighting-obstruction/results/"
    "tpc290_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc291_certificate.json"

PARENT290_CODE_SHA256 = (
    "819577011d9dbcae4137b30d823ae342f7a44f6ac9f3d54fa0716393032ac810")
PARENT290_RESULT_SHA256 = (
    "4e3bb7b23247b0f7e2272063a56e5527365136c1bd748e985d0c4d43d69905fc")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

SCHEMA = "TPC291_SIGNED_SCHUR_CANCELLATION_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_COHERENCE_TO_CANCELLATION_ATLAS")
ROUND2_CLUE = (
    "TEST_SOURCE_RESTRICTED_DIFFUSE_WEIGHTS_OR_MULTI_PRIME_SIGNED_NULL_"
    "DIRECTIONS")

GROWTH_S2 = (
    (128, 24, 9, 5, 2), (192, 32, 16, 5, 2),
    (256, 38, 27, 5, 2), (384, 50, 40, 5, 2),
    (512, 58, 50, 5, 2), (512, 58, 60, 5, 2),
    (512, 58, 70, 5, 2), (512, 58, 90, 5, 2),
)
EXPONENT_CROSSOVER = (
    (256, 38, 27, 5, 1), (384, 50, 40, 5, 1),
    (512, 58, 70, 5, 1), (512, 58, 90, 5, 1),
)
SOURCE_CONTROL_S2 = tuple(
    (384, height, 70, cutoff, 2)
    for height in (48, 52) for cutoff in (3, 5, 7))
ROWS = tuple((args, "GROWTH_S2") for args in GROWTH_S2) + tuple(
    (args, "EXPONENT_CROSSOVER") for args in EXPONENT_CROSSOVER) + tuple(
    (args, "SOURCE_CONTROL_S2") for args in SOURCE_CONTROL_S2)

RESIDUAL_THRESHOLDS = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 10))
COHERENCE_THRESHOLDS = (Fraction(9, 25), Fraction(3, 4))

parent_spec = importlib.util.spec_from_file_location("frozen_tpc290", PARENT290_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-290 parent unavailable")
PARENT = importlib.util.module_from_spec(parent_spec)
parent_spec.loader.exec_module(PARENT)
ENGINE = PARENT.ENGINE


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def decimal(value: Fraction) -> str:
    return ENGINE.decimal_text(value)


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT290_CODE.read_bytes()) == PARENT290_CODE_SHA256,
         "TPC290 code provenance")
    raw = PARENT290_RESULT.read_bytes()
    need(digest(raw) == PARENT290_RESULT_SHA256, "TPC290 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC290 result canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM"), "TPC290 status")
    need(data.get("payload", {}).get("finite_audit", {}).get("rows") == 18,
         "TPC290 row count")
    return {
        "tpc290_code_sha256": PARENT290_CODE_SHA256,
        "tpc290_result_sha256": PARENT290_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc290_rows": 18,
    }


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1)
            centered -= Fraction(1, prime - 1)
            total += (prime * ENGINE.kernel(u - t, height, exponent)
                      * centered * beta_t)
        output.append(total)
    return output


def pair_record(low: int, high: int, cross: Fraction,
                diagonal_low: Fraction, diagonal_high: Fraction,
                gamma: Fraction) -> dict[str, Any]:
    residual = 1 - gamma
    coefficient = cross / diagonal_low
    return {
        "prime_pair": [low, high],
        "gram_cross": str(cross),
        "sign": "POSITIVE" if cross > 0 else "NEGATIVE" if cross < 0 else "ZERO",
        "coherence_squared": str(gamma),
        "schur_residual": str(residual),
        "schur_residual_decimal": decimal(residual),
        "projection_target_prime": high,
        "projection_reference_prime": low,
        "projection_coefficient": str(coefficient),
        "projection_coefficient_decimal": decimal(coefficient),
        "optimal_coefficient_sign": (
            "POSITIVE" if coefficient > 0 else
            "NEGATIVE" if coefficient < 0 else "ZERO"),
        "same_sign_cancellation": coefficient < 0,
        "opposite_sign_cancellation": coefficient > 0,
    }


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    outputs = [physical_output(indices, beta, height, q, exponent)
               for q in shell]
    gram = [[sum(x * y for x, y in zip(outputs[i], outputs[j]))
             for j in range(len(shell))] for i in range(len(shell))]
    diagonal = [gram[i][i] for i in range(len(shell))]
    need(all(value > 0 for value in diagonal), "positive diagonal")
    pairs: list[dict[str, Any]] = []
    for i in range(len(shell)):
        for j in range(i):
            cross = gram[i][j]
            gamma = cross * cross / (diagonal[i] * diagonal[j])
            need(0 <= gamma <= 1, "Cauchy coherence")
            pairs.append(pair_record(shell[j], shell[i], cross,
                                     diagonal[j], diagonal[i], gamma))
    need(bool(pairs), "nonempty pair atlas")
    best = max(pairs, key=lambda item: fraction(item["coherence_squared"]))
    negative = [item for item in pairs if item["sign"] == "NEGATIVE"]
    residual_counts = {
        str(bound): sum(fraction(item["schur_residual"]) <= bound
                        for item in pairs)
        for bound in RESIDUAL_THRESHOLDS
    }
    coherence_counts = {
        str(bound): sum(fraction(item["coherence_squared"]) >= bound
                        for item in pairs)
        for bound in COHERENCE_THRESHOLDS
    }
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "pair_count": len(pairs),
        "pair_positive": sum(item["sign"] == "POSITIVE" for item in pairs),
        "pair_negative": len(negative),
        "pair_zero": sum(item["sign"] == "ZERO" for item in pairs),
        "best_coherence_pair": best,
        "residual_counts": residual_counts,
        "coherence_counts": coherence_counts,
        "negative_pair_records": negative,
        "schur_residuals_nonnegative": all(
            fraction(item["schur_residual"]) >= 0 for item in pairs),
        "opposite_sign_cancellation_pairs": sum(
            item["opposite_sign_cancellation"] for item in pairs),
        "same_sign_cancellation_pairs": sum(
            item["same_sign_cancellation"] for item in pairs),
    }


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def build_payload() -> dict[str, Any]:
    rows = [build_row(*args, axis) for args, axis in ROWS]
    total_pairs = sum(row["pair_count"] for row in rows)
    positive = sum(row["pair_positive"] for row in rows)
    negative = sum(row["pair_negative"] for row in rows)
    zero = sum(row["pair_zero"] for row in rows)
    residual_totals = {
        str(bound): sum(row["residual_counts"][str(bound)] for row in rows)
        for bound in RESIDUAL_THRESHOLDS
    }
    coherence_totals = {
        str(bound): sum(row["coherence_counts"][str(bound)] for row in rows)
        for bound in COHERENCE_THRESHOLDS
    }
    need((len(rows), total_pairs, positive, negative, zero,
          residual_totals, coherence_totals) ==
         (18, 1380, 1377, 3, 0,
          {"1/2": 1074, "1/4": 852, "1/10": 477},
          {"9/25": 1189, "3/4": 852}), "finite census")
    global_best = max(
        ((row["best_coherence_pair"], row) for row in rows),
        key=lambda item: fraction(item[0]["coherence_squared"]))
    best_pair, best_row = global_best
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "gram_pair": "G_{i,j}=<g_i,g_j>",
            "coherence": "Gamma_{i,j}=G_{i,j}^2/(d_i d_j)",
            "projection_coefficient": "rho*=G_{i,j}/d_j",
            "schur_identity":
                "min_rho ||g_i-rho g_j||_2^2/d_i=1-Gamma_{i,j}",
            "normalized_signed_rayleigh":
                "inf_{a,b} ||a g_i+b g_j||^2/(a^2d_i+b^2d_j)"
                "=1-sqrt(Gamma_{i,j})",
            "coefficient_sign_rule":
                "sign(rho*)=sign(G_{i,j}); positive cross needs opposite"
                " signs in subtraction, negative cross needs same signs",
            "scope": "finite two-component probe, frozen source, literal operator",
        },
        "thresholds": {
            "residual": [str(value) for value in RESIDUAL_THRESHOLDS],
            "coherence": [str(value) for value in COHERENCE_THRESHOLDS],
        },
        "grid": {
            "growth_s2": [list(item) for item in GROWTH_S2],
            "exponent_crossover": [list(item)
                                   for item in EXPONENT_CROSSOVER],
            "source_control_s2": [list(item) for item in SOURCE_CONTROL_S2],
            "rows": len(ROWS),
        },
        "finite_audit": {
            "rows": len(rows), "total_pairs": total_pairs,
            "positive_pairs": positive, "negative_pairs": negative,
            "zero_pairs": zero, "residual_totals": residual_totals,
            "coherence_totals": coherence_totals,
            "same_sign_cancellation_pairs": negative,
            "opposite_sign_cancellation_pairs": positive,
            "all_schur_residuals_nonnegative": all(
                row["schur_residuals_nonnegative"] for row in rows),
            "global_best_row": {
                "axis": best_row["axis"], "scale": best_row["scale"],
                "H": best_row["H"], "Q": best_row["Q"],
                "comparison_cutoff_z": best_row["comparison_cutoff_z"],
                "kernel_exponent": best_row["kernel_exponent"],
            },
            "global_best_pair": best_pair,
            "growing_signed_cancellation_theorem": "OPEN",
            "source_native_L2": "OPEN",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC291_SCHUR_PROJECTION_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC291_SIGNED_TWO_PRIME_CANCELLATION": "PROVED_EXACT_CONDITIONAL",
            "TPC291_RESIDUAL_NONNEGATIVITY": "PROVED_EXACT_FROM_CAUCHY",
            "TPC291_COHERENCE_TO_CANCELLATION_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_1380_PAIRS",
            "TPC291_LOW_RESIDUAL_COUNTS":
                "NUMERICALLY_CERTIFIED_FINITE_1074_852_477",
            "TPC291_SIGN_COST_CENSUS":
                "NUMERICALLY_CERTIFIED_FINITE_1377_OPPOSITE_3_SAME",
            "TPC291_GROWING_SIGNED_THEOREM": "OPEN",
            "TPC291_SOURCE_NATIVE_L2": "OPEN_LITERAL_SOURCE",
            "TPC291_FIXED_POWER_CREDIT": 0,
            "TPC291_FULL_GATE_B": "OPEN",
            "TPC291_TWIN_PRIME_RESULT": "NONE",
            "TPC291_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def frozen_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(frozen_document()))


def check_data(data: dict[str, Any]) -> None:
    expected = frozen_document()
    need(data == expected, "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    check_data(data)
    audit = data["payload"]["finite_audit"]
    print("TPC291_CERTIFICATE=PASS rows={} pairs={} residual_le_half={} "
          "residual_le_quarter={} residual_le_tenth={} negative={}".format(
              audit["rows"], audit["total_pairs"],
              audit["residual_totals"]["1/2"],
              audit["residual_totals"]["1/4"],
              audit["residual_totals"]["1/10"], audit["negative_pairs"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    if args.write:
        write()
    else:
        check()
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC291_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
