#!/usr/bin/env python3
"""Reverse-order independent replay for the TPC-291 Schur atlas."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-291-signed-schur-cancellation-atlas"
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
STATUS = (
    "PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_COHERENCE_TO_CANCELLATION_ATLAS")
RESIDUAL_THRESHOLDS = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 10))
COHERENCE_THRESHOLDS = (Fraction(9, 25), Fraction(3, 4))
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

spec = importlib.util.spec_from_file_location("independent_engine", ENGINE_CODE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC291_INDEPENDENT_CHECK=FAIL engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


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
         "TPC290 code lock")
    raw = PARENT290_RESULT.read_bytes()
    need(digest(raw) == PARENT290_RESULT_SHA256, "TPC290 result lock")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC290 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM"), "TPC290 status")
    need(data["payload"]["finite_audit"]["rows"] == 18,
         "TPC290 row count")
    return {"tpc290_code_sha256": PARENT290_CODE_SHA256,
            "tpc290_result_sha256": PARENT290_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256, "tpc290_rows": 18}


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    # Column-first accumulation is intentionally different from the producer.
    output = [Fraction(0) for _ in indices]
    for t, beta_t in zip(indices, beta):
        if t % prime == 0:
            continue
        for position, u in enumerate(indices):
            if u == t or u % prime == 0:
                continue
            centered = Fraction(1 if u % prime == t % prime else 0)
            centered -= Fraction(1, prime - 1)
            output[position] += (prime * ENGINE.kernel(u - t, height, exponent)
                                 * centered * beta_t)
    return output


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def pair_record(low: int, high: int, cross: Fraction,
                diagonal_low: Fraction, gamma: Fraction) -> dict[str, Any]:
    residual = 1 - gamma
    coefficient = cross / diagonal_low
    return {
        "prime_pair": [low, high], "gram_cross": str(cross),
        "sign": "POSITIVE" if cross > 0 else "NEGATIVE" if cross < 0 else "ZERO",
        "coherence_squared": str(gamma), "schur_residual": str(residual),
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


def row_expected(scale: int, height: int, q0: int, cutoff: int,
                 exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    outputs = [physical_output(indices, beta, height, q, exponent)
               for q in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices))) for j in range(len(shell))]
            for i in range(len(shell))]
    diagonal = [gram[i][i] for i in range(len(shell))]
    pairs = []
    for i in range(len(shell)):
        for j in range(i):
            cross = gram[i][j]
            gamma = cross * cross / (diagonal[i] * diagonal[j])
            need(0 <= gamma <= 1, "Cauchy")
            pairs.append(pair_record(shell[j], shell[i], cross,
                                     diagonal[j], gamma))
    best = max(pairs, key=lambda item: fraction(item["coherence_squared"]))
    negative = [item for item in pairs if item["sign"] == "NEGATIVE"]
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "pair_count": len(pairs),
        "pair_positive": sum(item["sign"] == "POSITIVE" for item in pairs),
        "pair_negative": len(negative),
        "pair_zero": sum(item["sign"] == "ZERO" for item in pairs),
        "best_coherence_pair": best,
        "residual_counts": {
            str(bound): sum(fraction(item["schur_residual"]) <= bound
                            for item in pairs)
            for bound in RESIDUAL_THRESHOLDS
        },
        "coherence_counts": {
            str(bound): sum(fraction(item["coherence_squared"]) >= bound
                            for item in pairs)
            for bound in COHERENCE_THRESHOLDS
        },
        "negative_pair_records": negative,
        "schur_residuals_nonnegative": all(
            fraction(item["schur_residual"]) >= 0 for item in pairs),
        "opposite_sign_cancellation_pairs": sum(
            item["opposite_sign_cancellation"] for item in pairs),
        "same_sign_cancellation_pairs": sum(
            item["same_sign_cancellation"] for item in pairs),
    }


def main() -> int:
    raw = RESULT.read_bytes()
    actual = json.loads(raw)
    need(raw == canonical(actual), "certificate canonicality")
    need(actual.get("certificate_version") == 1 and
         actual.get("claim_status") == STATUS, "header")
    payload = actual["payload"]
    need(payload["parent_lock"] == parent_lock(), "parent lock")
    expected_rows = [row_expected(*args, axis) for args, axis in ROWS]
    need(len(payload["rows"]) == len(expected_rows), "row count")
    for index, (got, expected) in enumerate(zip(payload["rows"], expected_rows)):
        for key, value in expected.items():
            need(got.get(key) == value, "row {} field {}".format(index, key))
    audit = payload["finite_audit"]
    need(audit["total_pairs"] == 1380 and
         audit["positive_pairs"] == 1377 and
         audit["negative_pairs"] == 3 and audit["zero_pairs"] == 0,
         "sign census")
    need(audit["residual_totals"] ==
         {"1/2": 1074, "1/4": 852, "1/10": 477}, "residual census")
    need(audit["coherence_totals"] == {"9/25": 1189, "3/4": 852},
         "coherence census")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC291_INDEPENDENT_CHECK=PASS rows=18 pairs=1380 "
          "residual_le_half=1074 residual_le_quarter=852 "
          "residual_le_tenth=477 negative=3")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC291_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
