#!/usr/bin/env python3
"""Independent column-first replay for the TPC-292 triangle atlas."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import multiprocessing as mp
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-292-three-prime-sign-frustration-atlas"
PARENT291_CODE = ROOT / (
    "papers/tpc-291-signed-schur-cancellation-atlas/code/"
    "tpc291_signed_schur_cancellation_certificate.py")
PARENT291_RESULT = ROOT / (
    "papers/tpc-291-signed-schur-cancellation-atlas/results/"
    "tpc291_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc292_certificate.json"
PARENT291_CODE_SHA256 = (
    "368202bcf8b39db0429c9ef8b9546f5041eb2a0c749c20fa539d5f3b6a76584d")
PARENT291_RESULT_SHA256 = (
    "b6743bcc574e3fe865832e4867a6d696aa70dd700bceaf1f8b1b7b1f866344b0")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS")
SCHEMA = "TPC292_THREE_PRIME_SIGN_FRUSTRATION_CERTIFICATE_V1"

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
THRESHOLDS = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 10))

engine_spec = importlib.util.spec_from_file_location("independent_engine", ENGINE_CODE)
if engine_spec is None or engine_spec.loader is None:
    raise RuntimeError("frozen engine unavailable")
ENGINE = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(ENGINE)


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


def sign(value: Fraction) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def sign_text(value: Fraction) -> str:
    return "+" if value > 0 else "-" if value < 0 else "0"


def determinant3(matrix: list[list[Fraction]]) -> Fraction:
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    # The producer accumulates row-first.  This replay accumulates column-first
    # and therefore checks the physical matrix through a different operation
    # order.
    output = [Fraction(0) for _ in indices]
    for t, beta_t in zip(indices, beta):
        if t % prime == 0:
            continue
        for position, u in enumerate(indices):
            if u == t or u % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1)
            centered -= Fraction(1, prime - 1)
            output[position] += (prime * ENGINE.kernel(u - t, height, exponent)
                                 * centered * beta_t)
    return output


def volume_witness(primes: list[int], triple: tuple[int, int, int],
                   volume: Fraction, pattern: str) -> dict[str, Any]:
    return {
        "prime_triple": [primes[index] for index in triple],
        "edge_sign_pattern": pattern,
        "edge_sign_product": 1 if pattern.count("-") % 2 == 0 else -1,
        "normalized_volume_squared": str(volume),
        "normalized_volume_squared_decimal": decimal(volume),
    }


def projection(sub: list[list[Fraction]], target: int
               ) -> tuple[Fraction, Fraction, Fraction, str]:
    others = [index for index in range(3) if index != target]
    j, k = others
    d_i = sub[target][target]
    d_j = sub[j][j]
    d_k = sub[k][k]
    cross = sub[j][k]
    minor = d_j * d_k - cross * cross
    need(minor > 0, "pair minor")
    alpha = (sub[target][j] * d_k - sub[target][k] * cross) / minor
    beta = (sub[target][k] * d_j - sub[target][j] * cross) / minor
    residual = determinant3(sub) / (d_i * minor)
    return residual, alpha, beta, sign_text(alpha) + sign_text(beta)


def row_expected(scale: int, height: int, q0: int, cutoff: int,
                 exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    primes = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    outputs = [physical_output(indices, beta, height, q, exponent)
               for q in primes]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(primes))] for i in range(len(primes))]
    diagonal = [gram[i][i] for i in range(len(primes))]
    need(all(value > 0 for value in diagonal), "diagonal")
    edge_counts: dict[str, int] = {}
    projection_counts: dict[str, int] = {}
    residual_counts = {str(bound): 0 for bound in THRESHOLDS}
    positive_volume = zero_volume = negative_volume = 0
    zero_edge = anti_alignable = frustrated = 0
    minimum_volume: tuple[Fraction, tuple[int, int, int], str] | None = None
    minimum_residual: tuple[Fraction, tuple[int, int, int], int, str, str,
                            Fraction] | None = None
    triples = list(itertools.combinations(range(len(primes)), 3))
    for triple in triples:
        sub = [[gram[i][j] for j in triple] for i in triple]
        determinant = determinant3(sub)
        volume = determinant / (sub[0][0] * sub[1][1] * sub[2][2])
        edge_values = (sub[0][1], sub[0][2], sub[1][2])
        pattern = "".join(sign_text(value) for value in edge_values)
        product = sign(edge_values[0]) * sign(edge_values[1]) * sign(edge_values[2])
        edge_counts[pattern] = edge_counts.get(pattern, 0) + 1
        if product == 1:
            frustrated += 1
        elif product == -1:
            anti_alignable += 1
        else:
            zero_edge += 1
        if volume > 0:
            positive_volume += 1
        elif volume < 0:
            negative_volume += 1
        else:
            zero_volume += 1
        row_min: tuple[Fraction, int, str] | None = None
        for target in range(3):
            residual, alpha, beta_coefficient, projection_pattern = \
                projection(sub, target)
            projection_counts[projection_pattern] = (
                projection_counts.get(projection_pattern, 0) + 1)
            if row_min is None or residual < row_min[0]:
                row_min = (residual, target, projection_pattern)
        need(row_min is not None, "target projection")
        residual, target, projection_pattern = row_min
        for bound in THRESHOLDS:
            residual_counts[str(bound)] += int(residual <= bound)
        prime_tuple = tuple(primes[index] for index in triple)
        if minimum_volume is None or (volume, prime_tuple) < (
                minimum_volume[0],
                tuple(primes[index] for index in minimum_volume[1])):
            minimum_volume = (volume, triple, pattern)
        if minimum_residual is None or (residual, prime_tuple, target) < (
                minimum_residual[0],
                tuple(primes[index] for index in minimum_residual[1]),
                minimum_residual[2]):
            minimum_residual = (residual, triple, target, pattern,
                                projection_pattern, volume)
    need(minimum_volume is not None and minimum_residual is not None,
         "triple witnesses")
    volume_value, volume_triple, volume_pattern = minimum_volume
    residual_value, residual_triple, residual_target, residual_pattern, \
        residual_projection, residual_volume = minimum_residual
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": primes, "shell_cardinality": len(primes),
        "triple_count": len(triples),
        "positive_volume_triples": positive_volume,
        "zero_volume_triples": zero_volume,
        "negative_volume_triples": negative_volume,
        "zero_edge_triples": zero_edge,
        "anti_alignable_triples": anti_alignable,
        "sign_frustrated_triples": frustrated,
        "edge_sign_pattern_counts": edge_counts,
        "projection_coefficient_sign_pattern_counts": projection_counts,
        "residual_counts": residual_counts,
        "minimum_volume_witness": volume_witness(
            primes, volume_triple, volume_value, volume_pattern),
        "minimum_residual_witness": {
            "prime_triple": [primes[index] for index in residual_triple],
            "target_prime": primes[residual_triple[residual_target]],
            "edge_sign_pattern": residual_pattern,
            "edge_sign_product": 1 if residual_pattern.count("-") % 2 == 0 else -1,
            "projection_coefficient_signs": residual_projection,
            "schur_residual": str(residual_value),
            "schur_residual_decimal": decimal(residual_value),
            "normalized_volume_squared": str(residual_volume),
            "normalized_volume_squared_decimal": decimal(residual_volume),
        },
    }


def row_from_spec(spec: tuple[tuple[int, int, int, int, int], str]
                  ) -> dict[str, Any]:
    args, axis = spec
    return row_expected(*args, axis)


def expected_rows() -> list[dict[str, Any]]:
    workers = min(len(ROWS), max(1, os.cpu_count() or 1))
    if workers == 1:
        return [row_from_spec(spec) for spec in ROWS]
    try:
        context = mp.get_context("fork")
        with context.Pool(processes=workers) as pool:
            return pool.map(row_from_spec, ROWS)
    except (AttributeError, OSError, RuntimeError):
        return [row_from_spec(spec) for spec in ROWS]


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT291_CODE.read_bytes()) == PARENT291_CODE_SHA256,
         "parent code lock")
    raw = PARENT291_RESULT.read_bytes()
    need(digest(raw) == PARENT291_RESULT_SHA256, "parent result lock")
    parent = json.loads(raw)
    need(raw == canonical(parent), "parent canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status", "").startswith(
             "PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION"),
         "parent status")
    return {"tpc291_code_sha256": PARENT291_CODE_SHA256,
            "tpc291_result_sha256": PARENT291_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256, "tpc291_rows": 18}


def main() -> int:
    raw = RESULT.read_bytes()
    actual = json.loads(raw)
    need(raw == canonical(actual), "certificate canonicality")
    need(actual.get("certificate_version") == 1 and
         actual.get("claim_status") == STATUS, "header")
    payload = actual["payload"]
    need(payload.get("schema") == SCHEMA, "schema")
    need(payload.get("parent_lock") == parent_lock(), "parent lock")
    expected = expected_rows()
    need(payload.get("rows") == expected, "independent row replay")
    audit = payload["finite_audit"]
    need(audit["total_triples"] == 5727 and
         audit["positive_volume_triples"] == 5727 and
         audit["zero_volume_triples"] == 0 and
         audit["negative_volume_triples"] == 0 and
         audit["zero_edge_triples"] == 0 and
         audit["anti_alignable_triples"] == 9 and
         audit["sign_frustrated_triples"] == 5718,
         "finite audit")
    need(audit["edge_sign_pattern_totals"] ==
         {"+++": 5715, "++-": 1, "+-+": 8, "+--": 3},
         "edge census")
    need(audit["minimum_target_residual_totals"] ==
         {"1/2": 5313, "1/4": 4413, "1/10": 3620},
         "residual census")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC292_INDEPENDENT_CHECK=PASS rows=18 triples=5727 "
          "frustrated=5718 anti_alignable=9 residual_le_half=5313 "
          "residual_le_quarter=4413 residual_le_tenth=3620")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC292_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
