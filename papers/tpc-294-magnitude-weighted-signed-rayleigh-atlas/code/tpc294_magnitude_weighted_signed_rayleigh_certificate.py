#!/usr/bin/env python3
"""Exact trace-normalized signed Rayleigh atlas for the TPC-293 shells.

TPC-293 optimized only the signs of Gram edges.  TPC-294 restores the Gram
magnitudes and asks for the minimum physical quadratic form among equal
coefficient-sign vectors.  The finite optimization is exact: a common
positive denominator turns each Gram matrix into an integer matrix and a Gray
code traversal evaluates every sign vector with integer updates.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import math
import multiprocessing as mp
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any
import json

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT293_CODE = ROOT / (
    "papers/tpc-293-signed-shell-maxcut-atlas/code/"
    "tpc293_signed_shell_maxcut_certificate.py")
PARENT293_RESULT = ROOT / (
    "papers/tpc-293-signed-shell-maxcut-atlas/results/"
    "tpc293_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc294_certificate.json"

PARENT293_CODE_SHA256 = (
    "2fdaa5e1bce7a70e520ab4fe89b93b3e43383423a0277d82bc5a8689f2764d71")
PARENT293_RESULT_SHA256 = (
    "14dae97ac94398612af49860b364e2fac8d112ea288fb95114d974eacd2d07b2")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

STATUS = (
    "PROVED_EXACT_TRACE_NORMALIZED_SIGNED_QUADRATIC_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_GLOBAL_SIGN_ATLAS")
SCHEMA = "TPC294_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_CERTIFICATE_V1"
ROUND2_CLUE = "TEST_SOURCE_IMAGE_OF_WEIGHTED_OPTIMAL_SIGN_PATTERNS_AND_DIFFUSE_SIGNED_WEIGHTS"

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

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc293_for_tpc294", PARENT293_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-293 parent unavailable")
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


def shell_between(q0: int) -> list[int]:
    shell: list[int] = []
    for prime in ENGINE.PRIMES:
        if q0 < prime <= 2 * q0:
            shell.append(prime)
    return shell


def physical_output(indices: list[int], beta: list[Any], height: int,
                    prime: int, exponent: int) -> list[Any]:
    """Use a target-first order distinct from the TPC-293 producer wrapper."""
    output = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(1 if u % prime == t % prime else 0)
            centered -= Fraction(1, prime - 1)
            total += (prime * ENGINE.kernel(u - t, height, exponent)
                      * centered * beta_t)
        output.append(total)
    return output


def integer_matrix(gram: list[list[Fraction]]) -> tuple[list[list[int]], int]:
    denominator = 1
    for row in gram:
        for value in row:
            denominator = math.lcm(denominator, value.denominator)
    scaled = [[value.numerator * (denominator // value.denominator)
               for value in row] for row in gram]
    return scaled, denominator


def gray_extrema(matrix: list[list[int]]) -> dict[str, Any]:
    """Enumerate labels[0]=+1 with exact integer Gray-code updates."""
    m = len(matrix)
    labels = [1] * m
    diagonal_sum = sum(matrix[i][i] for i in range(m))
    fields = [sum(matrix[i][j] for j in range(m) if j != i)
              for i in range(m)]
    value = sum(matrix[i][j] for i in range(m) for j in range(m))
    minimum = value
    maximum = value
    minimum_label = tuple(labels)
    maximum_label = tuple(labels)
    minimum_count = 1
    maximum_count = 1
    previous_gray = 0
    for code in range(1, 1 << (m - 1)):
        gray = code ^ (code >> 1)
        changed = gray ^ previous_gray
        vertex = changed.bit_length()
        old = labels[vertex]
        value -= 4 * old * fields[vertex]
        labels[vertex] = -old
        for other in range(m):
            if other != vertex:
                fields[other] -= 2 * old * matrix[other][vertex]
        previous_gray = gray
        candidate = tuple(labels)
        if value < minimum:
            minimum = value
            minimum_label = candidate
            minimum_count = 1
        elif value == minimum:
            minimum_count += 1
            if candidate < minimum_label:
                minimum_label = candidate
        if value > maximum:
            maximum = value
            maximum_label = candidate
            maximum_count = 1
        elif value == maximum:
            maximum_count += 1
            if candidate > maximum_label:
                maximum_label = candidate
    return {
        "trace_integer": diagonal_sum,
        "plus_integer": sum(matrix[i][j]
                             for i in range(m) for j in range(m)),
        "minimum_integer": minimum,
        "maximum_integer": maximum,
        "minimum_label": minimum_label,
        "maximum_label": maximum_label,
        "minimum_count": minimum_count,
        "maximum_count": maximum_count,
    }


def ratio(matrix: list[list[int]], labels: tuple[int, ...],
          trace: int) -> Fraction:
    numerator = sum(labels[i] * labels[j] * matrix[i][j]
                    for i in range(len(labels)) for j in range(len(labels)))
    return Fraction(numerator, trace)


def signed_maxcut(matrix: list[list[int]]) -> dict[str, Any]:
    signs = [[0 if i == j else (1 if matrix[i][j] > 0 else -1)
              for j in range(len(matrix))] for i in range(len(matrix))]
    best = -1
    best_label: tuple[int, ...] | None = None
    count = 0
    for tail in itertools.product((-1, 1), repeat=len(matrix) - 1):
        labels = (1,) + tail
        favorable = sum(labels[i] * labels[j] * signs[i][j] == -1
                        for i in range(len(matrix))
                        for j in range(i + 1, len(matrix)))
        if favorable > best:
            best = favorable
            best_label = labels
            count = 1
        elif favorable == best:
            count += 1
            if labels < best_label:
                best_label = labels
    need(best_label is not None, "signed max-cut witness")
    return {"favorable_edges": best, "label": best_label, "count": count}


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT293_CODE.read_bytes()) == PARENT293_CODE_SHA256,
         "TPC293 code provenance")
    raw = PARENT293_RESULT.read_bytes()
    need(digest(raw) == PARENT293_RESULT_SHA256, "TPC293 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC293 canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status", "").startswith(
             "PROVED_EXACT_ALL_POSITIVE_MAXCUT"), "TPC293 status")
    audit = data.get("payload", {}).get("finite_audit", {})
    need(audit.get("rows") == 18 and audit.get("total_edges") == 1380,
         "TPC293 finite audit")
    return {
        "tpc293_code_sha256": PARENT293_CODE_SHA256,
        "tpc293_result_sha256": PARENT293_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc293_rows": 18,
        "tpc293_edges": 1380,
    }


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = shell_between(q0)
    need(len(shell) >= 3, "small shell")
    outputs = [physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    need(all(gram[i][i] > 0 for i in range(len(shell))), "positive diagonal")
    scaled, common_denominator = integer_matrix(gram)
    trace = sum(scaled[i][i] for i in range(len(shell)))
    need(trace > 0, "positive trace")
    extrema = gray_extrema(scaled)
    need(extrema["trace_integer"] == trace, "trace update")
    all_positive = (1,) * len(shell)
    plus_ratio = ratio(scaled, all_positive, trace)
    minimum_ratio = Fraction(extrema["minimum_integer"], trace)
    maximum_ratio = Fraction(extrema["maximum_integer"], trace)
    cut = signed_maxcut(scaled)
    cut_label = cut["label"]
    need(cut_label is not None, "cut label")
    cut_ratio = ratio(scaled, cut_label, trace)
    positive_edges = 0
    negative_edges = 0
    edge_pattern: list[str] = []
    for i in range(len(shell)):
        for j in range(i + 1, len(shell)):
            if scaled[i][j] > 0:
                positive_edges += 1
                edge_pattern.append("+")
            elif scaled[i][j] < 0:
                negative_edges += 1
                edge_pattern.append("-")
            else:
                edge_pattern.append("0")
    edge_count = len(shell) * (len(shell) - 1) // 2
    need(positive_edges + negative_edges == edge_count,
         "zero Gram edge")
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "edge_count": edge_count, "positive_edges": positive_edges,
        "negative_edges": negative_edges, "zero_edges": 0,
        "edge_sign_upper_triangle": "".join(edge_pattern),
        "all_positive_ratio": str(plus_ratio),
        "all_positive_ratio_decimal": ENGINE.decimal_text(plus_ratio),
        "minimum_signed_ratio": str(minimum_ratio),
        "minimum_signed_ratio_decimal": ENGINE.decimal_text(minimum_ratio),
        "maximum_signed_ratio": str(maximum_ratio),
        "maximum_signed_ratio_decimal": ENGINE.decimal_text(maximum_ratio),
        "minimum_signed_label": list(extrema["minimum_label"]),
        "maximum_signed_label": list(extrema["maximum_label"]),
        "minimum_label_count_mod_global_sign": extrema["minimum_count"],
        "maximum_label_count_mod_global_sign": extrema["maximum_count"],
        "maxcut_favorable_edges": cut["favorable_edges"],
        "maxcut_label": list(cut_label),
        "maxcut_label_count_mod_global_sign": cut["count"],
        "maxcut_ratio": str(cut_ratio),
        "maxcut_ratio_decimal": ENGINE.decimal_text(cut_ratio),
        "weighted_saving_from_all_positive": str(plus_ratio - minimum_ratio),
        "weighted_saving_from_all_positive_decimal": ENGINE.decimal_text(
            plus_ratio - minimum_ratio),
        "maxcut_weighted_gap": str(cut_ratio - minimum_ratio),
        "maxcut_weighted_gap_decimal": ENGINE.decimal_text(
            cut_ratio - minimum_ratio),
        "minimum_is_below_one": minimum_ratio < 1,
        "all_positive_is_above_one": plus_ratio > 1,
        "maxcut_is_below_one": cut_ratio < 1,
        "common_denominator_bits": common_denominator.bit_length(),
        "common_denominator_digits": len(str(common_denominator)),
        "trace_integer_digits": len(str(abs(trace))),
    }


def row_from_spec(spec: tuple[tuple[int, int, int, int, int], str]
                  ) -> dict[str, Any]:
    args, axis = spec
    return build_row(*args, axis)


def build_rows() -> list[dict[str, Any]]:
    workers = min(len(ROWS), max(1, os.cpu_count() or 1))
    if workers == 1:
        return [row_from_spec(spec) for spec in ROWS]
    try:
        context = mp.get_context("fork")
        with context.Pool(processes=workers) as pool:
            return pool.map(row_from_spec, ROWS)
    except (AttributeError, OSError, RuntimeError):
        return [row_from_spec(spec) for spec in ROWS]


def build_payload() -> dict[str, Any]:
    rows = build_rows()
    need(len(rows) == 18, "row count")
    need(all(row["minimum_is_below_one"] for row in rows),
         "finite weighted contraction census")
    need(all(row["all_positive_is_above_one"] for row in rows),
         "all-positive amplification census")
    need(all(row["maxcut_is_below_one"] for row in rows),
         "max-cut candidate census")
    minimum_row = min(rows, key=lambda row: (
        Fraction(row["minimum_signed_ratio"]),
        tuple(row["shell"])))
    maximum_plus_row = max(rows, key=lambda row: (
        Fraction(row["all_positive_ratio"]),
        tuple(row["shell"])))
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "trace_normalized_identity": (
                "R(a)=a^T G a/trace(G)=1+2 sum_{i<j} a_i a_j G_ij/trace(G)"),
            "sign_restricted_domain": "a_i in {+-1} with global sign fixed by a_0=+1",
            "finite_global_optimization": (
                "common positive denominator and Gray-code integer traversal "
                "visit every 2^(m-1) labeling exactly once"),
            "psd_nonnegativity": "R(a)>=0 because G is a Gram matrix",
            "scope": "equal-coefficient signs on frozen finite physical shells",
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
            "total_edges": sum(row["edge_count"] for row in rows),
            "minimum_below_one_rows": sum(
                row["minimum_is_below_one"] for row in rows),
            "all_positive_above_one_rows": sum(
                row["all_positive_is_above_one"] for row in rows),
            "maxcut_below_one_rows": sum(
                row["maxcut_is_below_one"] for row in rows),
            "weighted_optimum_le_one_quarter_rows": sum(
                Fraction(row["minimum_signed_ratio"]) <= Fraction(1, 4)
                for row in rows),
            "weighted_optimum_le_one_tenth_rows": sum(
                Fraction(row["minimum_signed_ratio"]) <= Fraction(1, 10)
                for row in rows),
            "maxcut_is_weighted_optimum_rows": sum(
                row["maxcut_ratio"] == row["minimum_signed_ratio"]
                for row in rows),
            "weighted_optimum_differs_from_maxcut_rows": sum(
                row["maxcut_ratio"] != row["minimum_signed_ratio"]
                for row in rows),
            "minimum_global_witness": {
                "axis": minimum_row["axis"], "scale": minimum_row["scale"],
                "H": minimum_row["H"], "Q": minimum_row["Q"],
                "comparison_cutoff_z": minimum_row["comparison_cutoff_z"],
                "kernel_exponent": minimum_row["kernel_exponent"],
                "shell": minimum_row["shell"],
                "ratio": minimum_row["minimum_signed_ratio"],
                "ratio_decimal": minimum_row[
                    "minimum_signed_ratio_decimal"],
            },
            "largest_all_positive_witness": {
                "axis": maximum_plus_row["axis"],
                "scale": maximum_plus_row["scale"],
                "H": maximum_plus_row["H"], "Q": maximum_plus_row["Q"],
                "comparison_cutoff_z": maximum_plus_row[
                    "comparison_cutoff_z"],
                "kernel_exponent": maximum_plus_row["kernel_exponent"],
                "shell": maximum_plus_row["shell"],
                "ratio": maximum_plus_row["all_positive_ratio"],
                "ratio_decimal": maximum_plus_row[
                    "all_positive_ratio_decimal"],
            },
            "growing_weighted_theorem": "OPEN",
            "source_native_coefficient_image": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC294_TRACE_NORMALIZED_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC294_GLOBAL_SIGN_ENUMERATION": "PROVED_EXACT_FINITE",
            "TPC294_WEIGHTED_RAYLEIGH_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
            "TPC294_EQUAL_SIGNED_CONTRACTION":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE",
            "TPC294_ALL_POSITIVE_AMPLIFICATION":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ABOVE_ONE",
            "TPC294_MAXCUT_CANDIDATE_CONTRACTION":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_BELOW_ONE",
            "TPC294_GROWING_WEIGHTED_THEOREM": "OPEN",
            "TPC294_SOURCE_NATIVE_COEFFICIENT_IMAGE": "OPEN_LITERAL_SOURCE",
            "TPC294_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC294_FIXED_POWER_CREDIT": 0,
            "TPC294_FULL_GATE_B": "OPEN",
            "TPC294_TWIN_PRIME_RESULT": "NONE",
            "TPC294_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def frozen_document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(frozen_document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data == frozen_document(), "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")
    audit = data["payload"]["finite_audit"]
    print("TPC294_CERTIFICATE=PASS rows={} edges={} min_below_one={} "
          "plus_above_one={} maxcut_below_one={} le_quarter={} le_tenth={}"
          .format(audit["rows"], audit["total_edges"],
                 audit["minimum_below_one_rows"],
                 audit["all_positive_above_one_rows"],
                 audit["maxcut_below_one_rows"],
                 audit["weighted_optimum_le_one_quarter_rows"],
                 audit["weighted_optimum_le_one_tenth_rows"]))


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
        print("TPC294_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
