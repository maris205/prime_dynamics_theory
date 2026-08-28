#!/usr/bin/env python3
"""Exact finite three-prime sign-frustration and Schur atlas for TPC-292.

TPC-291 proved the optimal signed direction for one pair of physical prime
components.  TPC-292 asks the next compatibility question: can all three
edges of a prime triangle be made cancellation-favourable at once?  The
triangle parity rule is exact, while the accompanying three-vector Schur
residual scan is finite evidence only.
"""

from __future__ import annotations

import argparse
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

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
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

SCHEMA = "TPC292_THREE_PRIME_SIGN_FRUSTRATION_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_TRIANGLE_SIGN_PARITY_AND_THREE_VECTOR_SCHUR_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SIGN_FRUSTRATION_ATLAS")
ROUND2_CLUE = (
    "TEST_SIGNED_GRAPH_MAXCUT_AND_MULTI_PRIME_RAYLEIGH_COMPATIBILITY")

# This is deliberately the inherited TPC-291 grid.  Keeping the row list
# explicit makes the finite certificate auditable without trusting a mutable
# parent result for its domain.
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

parent_spec = importlib.util.spec_from_file_location("frozen_tpc291", PARENT291_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-291 parent unavailable")
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


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def sign(value: Fraction) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def sign_text(value: Fraction) -> str:
    return "+" if value > 0 else "-" if value < 0 else "0"


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT291_CODE.read_bytes()) == PARENT291_CODE_SHA256,
         "TPC291 code provenance")
    raw = PARENT291_RESULT.read_bytes()
    need(digest(raw) == PARENT291_RESULT_SHA256,
         "TPC291 result provenance")
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC291 result canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status", "").startswith(
             "PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION"),
         "TPC291 status")
    need(parent.get("payload", {}).get("finite_audit", {}).get("rows") == 18,
         "TPC291 row count")
    return {
        "tpc291_code_sha256": PARENT291_CODE_SHA256,
        "tpc291_result_sha256": PARENT291_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc291_rows": 18,
    }


def determinant3(matrix: list[list[Fraction]]) -> Fraction:
    """Return the determinant of a 3 by 3 exact-rational matrix."""
    need(len(matrix) == 3 and all(len(row) == 3 for row in matrix),
         "three by three matrix")
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def triple_gram(gram: list[list[Fraction]], triple: tuple[int, int, int]
                ) -> list[list[Fraction]]:
    return [[gram[i][j] for j in triple] for i in triple]


def edge_pattern(sub: list[list[Fraction]]) -> tuple[str, int]:
    # Canonical edge order is (0,1), (0,2), (1,2), matching increasing prime
    # order in the enclosing shell.
    edges = (sub[0][1], sub[0][2], sub[1][2])
    pattern = "".join(sign_text(value) for value in edges)
    product = sign(edges[0]) * sign(edges[1]) * sign(edges[2])
    return pattern, product


def projection_data(sub: list[list[Fraction]], target: int
                    ) -> tuple[Fraction, Fraction, Fraction, str]:
    """Project target vector onto the other two, exactly.

    If the other indices are j<k, solve
       [d_j G_jk; G_jk d_k] [alpha; beta] = [G_ij; G_ik].
    The residual of g_i-alpha*g_j-beta*g_k is the three-vector Schur
    residual.  The returned pattern records signs of (alpha,beta), not the
    signs of the subtraction coefficients.
    """
    others = [index for index in range(3) if index != target]
    j, k = others
    d_i = sub[target][target]
    d_j = sub[j][j]
    d_k = sub[k][k]
    cross_jk = sub[j][k]
    minor = d_j * d_k - cross_jk * cross_jk
    need(minor > 0, "positive pair minor")
    alpha = (sub[target][j] * d_k - sub[target][k] * cross_jk) / minor
    beta = (sub[target][k] * d_j - sub[target][j] * cross_jk) / minor
    det = determinant3(sub)
    residual = det / (d_i * minor)
    pattern = sign_text(alpha) + sign_text(beta)
    return residual, alpha, beta, pattern


def witness(primes: list[int], sub: list[list[Fraction]],
            triple: tuple[int, int, int], residual: Fraction,
            target: int, volume: Fraction, pattern: str,
            projection_pattern: str) -> dict[str, Any]:
    return {
        "prime_triple": [primes[index] for index in triple],
        "target_prime": primes[triple[target]],
        "edge_sign_pattern": pattern,
        "edge_sign_product": (
            1 if pattern.count("-") % 2 == 0 else -1),
        "projection_coefficient_signs": projection_pattern,
        "schur_residual": str(residual),
        "schur_residual_decimal": decimal(residual),
        "normalized_volume_squared": str(volume),
        "normalized_volume_squared_decimal": decimal(volume),
    }


def volume_witness(primes: list[int], triple: tuple[int, int, int],
                   volume: Fraction, pattern: str) -> dict[str, Any]:
    return {
        "prime_triple": [primes[index] for index in triple],
        "edge_sign_pattern": pattern,
        "edge_sign_product": (
            1 if pattern.count("-") % 2 == 0 else -1),
        "normalized_volume_squared": str(volume),
        "normalized_volume_squared_decimal": decimal(volume),
    }


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    primes = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    need(len(primes) >= 3, "three-prime shell")
    outputs = [PARENT.physical_output(indices, beta, height, q, exponent)
               for q in primes]
    gram = [[sum(x * y for x, y in zip(outputs[i], outputs[j]))
             for j in range(len(primes))] for i in range(len(primes))]
    diagonal = [gram[i][i] for i in range(len(primes))]
    need(all(value > 0 for value in diagonal), "positive diagonal")

    triple_count = 0
    positive_volume = 0
    zero_volume = 0
    negative_volume = 0
    zero_edge = 0
    anti_alignable = 0
    frustrated = 0
    edge_patterns: dict[str, int] = {}
    projection_patterns: dict[str, int] = {}
    residual_counts = {str(bound): 0 for bound in RESIDUAL_THRESHOLDS}
    min_volume: tuple[Fraction, tuple[int, int, int], str] | None = None
    min_residual: tuple[Fraction, tuple[int, int, int], int, str, str,
                         Fraction] | None = None

    for triple in itertools.combinations(range(len(primes)), 3):
        sub = triple_gram(gram, triple)
        determinant = determinant3(sub)
        d0, d1, d2 = (sub[index][index] for index in range(3))
        volume = determinant / (d0 * d1 * d2)
        pattern, product = edge_pattern(sub)
        triple_count += 1
        edge_patterns[pattern] = edge_patterns.get(pattern, 0) + 1
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

        row_min_residual: tuple[Fraction, int, str] | None = None
        for target in range(3):
            residual, alpha, beta_coefficient, projection_pattern = \
                projection_data(sub, target)
            projection_patterns[projection_pattern] = (
                projection_patterns.get(projection_pattern, 0) + 1)
            if row_min_residual is None or residual < row_min_residual[0]:
                row_min_residual = (residual, target, projection_pattern)
        need(row_min_residual is not None, "three target projections")
        residual, target, projection_pattern = row_min_residual
        for bound in RESIDUAL_THRESHOLDS:
            residual_counts[str(bound)] += int(residual <= bound)
        if min_volume is None or (volume, tuple(primes[index]
                                                for index in triple)) < \
                (min_volume[0], tuple(primes[index] for index in min_volume[1])):
            min_volume = (volume, triple, pattern)
        if min_residual is None or (residual, tuple(primes[index]
                                                   for index in triple), target) < \
                (min_residual[0], tuple(primes[index] for index in min_residual[1]),
                 min_residual[2]):
            min_residual = (residual, triple, target, pattern,
                            projection_pattern, volume)

    need(min_volume is not None and min_residual is not None,
         "nonempty triple audit")
    min_volume_value, min_volume_triple, min_volume_pattern = min_volume
    min_residual_value, min_residual_triple, min_residual_target, \
        min_residual_pattern, min_residual_projection, min_residual_volume = \
        min_residual
    for bound in RESIDUAL_THRESHOLDS:
        need(residual_counts[str(bound)] >= 0, "residual count")

    return {
        "axis": axis,
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "shell": primes,
        "shell_cardinality": len(primes),
        "triple_count": triple_count,
        "positive_volume_triples": positive_volume,
        "zero_volume_triples": zero_volume,
        "negative_volume_triples": negative_volume,
        "zero_edge_triples": zero_edge,
        "anti_alignable_triples": anti_alignable,
        "sign_frustrated_triples": frustrated,
        "edge_sign_pattern_counts": edge_patterns,
        "projection_coefficient_sign_pattern_counts": projection_patterns,
        "residual_counts": residual_counts,
        "minimum_volume_witness": volume_witness(
            primes, min_volume_triple, min_volume_value, min_volume_pattern),
        "minimum_residual_witness": witness(
            primes, triple_gram(gram, min_residual_triple),
            min_residual_triple, min_residual_value, min_residual_target,
            min_residual_volume, min_residual_pattern,
            min_residual_projection),
    }


def build_row_from_spec(spec: tuple[tuple[int, int, int, int, int], str]
                        ) -> dict[str, Any]:
    args, axis = spec
    return build_row(*args, axis)


def build_rows() -> list[dict[str, Any]]:
    """Evaluate independent rows in parallel while preserving row order."""
    workers = min(len(ROWS), max(1, os.cpu_count() or 1))
    if workers == 1:
        return [build_row_from_spec(spec) for spec in ROWS]
    try:
        context = mp.get_context("fork")
        with context.Pool(processes=workers) as pool:
            return pool.map(build_row_from_spec, ROWS)
    except (AttributeError, OSError, RuntimeError):
        # Portability fallback; the mathematical payload is unchanged.
        return [build_row_from_spec(spec) for spec in ROWS]


def build_payload() -> dict[str, Any]:
    rows = build_rows()
    total_triples = sum(row["triple_count"] for row in rows)
    positive_volume = sum(row["positive_volume_triples"] for row in rows)
    zero_volume = sum(row["zero_volume_triples"] for row in rows)
    negative_volume = sum(row["negative_volume_triples"] for row in rows)
    zero_edge = sum(row["zero_edge_triples"] for row in rows)
    anti_alignable = sum(row["anti_alignable_triples"] for row in rows)
    frustrated = sum(row["sign_frustrated_triples"] for row in rows)
    edge_patterns: dict[str, int] = {}
    projection_patterns: dict[str, int] = {}
    residual_totals = {str(bound): 0 for bound in RESIDUAL_THRESHOLDS}
    for row in rows:
        for pattern, count in row["edge_sign_pattern_counts"].items():
            edge_patterns[pattern] = edge_patterns.get(pattern, 0) + count
        for pattern, count in row[
                "projection_coefficient_sign_pattern_counts"].items():
            projection_patterns[pattern] = (
                projection_patterns.get(pattern, 0) + count)
        for bound in RESIDUAL_THRESHOLDS:
            residual_totals[str(bound)] += row["residual_counts"][str(bound)]

    actual_census = (len(rows), total_triples, positive_volume, zero_volume,
                     negative_volume, zero_edge, anti_alignable, frustrated,
                     edge_patterns, residual_totals)
    need(actual_census ==
         (18, 5727, 5727, 0, 0, 0, 9, 5718,
          {"+++": 5715, "+--": 3, "+-+": 8, "++-": 1},
          {"1/2": 5313, "1/4": 4413, "1/10": 3620}),
         "finite triangle census")

    min_row = min(rows, key=lambda row: (
        fraction(row["minimum_residual_witness"]["schur_residual"]),
        tuple(row["minimum_residual_witness"]["prime_triple"]),
        row["minimum_residual_witness"]["target_prime"]))
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "triangle_parity": (
                "There exists signs a_i with a_i*a_j*sign(G_ij)=-1 for "
                "all three edges iff sign(G_12 G_13 G_23)=-1"),
            "three_vector_schur": (
                "min_{alpha,beta} ||g_i-alpha*g_j-beta*g_k||^2/d_i "
                "= det(G_ijk)/(d_i det(G_jk))"),
            "normalized_volume": (
                "det(G_ijk)/(d_i d_j d_k) is the squared normalized "
                "three-volume"),
            "scope": "finite three-component probe, frozen source, literal operator",
        },
        "thresholds": {
            "minimum_target_residual": [str(value)
                                         for value in RESIDUAL_THRESHOLDS],
        },
        "grid": {
            "growth_s2": [list(item) for item in GROWTH_S2],
            "exponent_crossover": [list(item)
                                   for item in EXPONENT_CROSSOVER],
            "source_control_s2": [list(item)
                                   for item in SOURCE_CONTROL_S2],
            "rows": len(ROWS),
        },
        "finite_audit": {
            "rows": len(rows),
            "total_triples": total_triples,
            "positive_volume_triples": positive_volume,
            "zero_volume_triples": zero_volume,
            "negative_volume_triples": negative_volume,
            "zero_edge_triples": zero_edge,
            "anti_alignable_triples": anti_alignable,
            "sign_frustrated_triples": frustrated,
            "edge_sign_pattern_totals": edge_patterns,
            "projection_coefficient_sign_pattern_totals": projection_patterns,
            "minimum_target_residual_totals": residual_totals,
            "global_minimum_residual_row": {
                "axis": min_row["axis"], "scale": min_row["scale"],
                "H": min_row["H"], "Q": min_row["Q"],
                "comparison_cutoff_z": min_row["comparison_cutoff_z"],
                "kernel_exponent": min_row["kernel_exponent"],
            },
            "global_minimum_residual_witness":
                min_row["minimum_residual_witness"],
            "growing_triangle_compatibility_theorem": "OPEN",
            "source_native_L2": "OPEN",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC292_TRIANGLE_SIGN_PARITY": "PROVED_EXACT_CONDITIONAL",
            "TPC292_THREE_VECTOR_SCHUR_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC292_NORMALIZED_VOLUME_NONNEGATIVITY":
                "PROVED_EXACT_FROM_GRAM_PSD",
            "TPC292_TRIANGLE_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_5727_TRIPLES",
            "TPC292_SIGN_FRUSTRATION":
                "NUMERICALLY_CERTIFIED_FINITE_5718_OF_5727",
            "TPC292_ANTI_ALIGNABLE":
                "NUMERICALLY_CERTIFIED_FINITE_9_OF_5727",
            "TPC292_GROWING_TRIANGLE_COMPATIBILITY": "OPEN",
            "TPC292_SOURCE_NATIVE_L2": "OPEN_LITERAL_SOURCE",
            "TPC292_FIXED_POWER_CREDIT": 0,
            "TPC292_FULL_GATE_B": "OPEN",
            "TPC292_TWIN_PRIME_RESULT": "NONE",
            "TPC292_STATUS": STATUS,
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
    print("TPC292_CERTIFICATE=PASS rows={} triples={} frustrated={} "
          "anti_alignable={} residual_le_half={} residual_le_quarter={} "
          "residual_le_tenth={}".format(
              audit["rows"], audit["total_triples"],
              audit["sign_frustrated_triples"],
              audit["anti_alignable_triples"],
              audit["minimum_target_residual_totals"]["1/2"],
              audit["minimum_target_residual_totals"]["1/4"],
              audit["minimum_target_residual_totals"]["1/10"]))


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
        print("TPC292_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
