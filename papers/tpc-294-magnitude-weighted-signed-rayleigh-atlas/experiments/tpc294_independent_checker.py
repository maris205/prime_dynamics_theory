#!/usr/bin/env python3
"""Independent exact replay for TPC-294.

The producer accumulates each physical output by target first and uses its
own Gray-code routine.  This checker imports only the frozen TPC-268 engine,
accumulates by source first, and reconstructs the weighted Rayleigh atlas
from scratch.  It does not import the TPC-294 producer or trust its JSON
while constructing the expected rows.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import math
import multiprocessing as mp
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-294-magnitude-weighted-signed-rayleigh-atlas"
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

engine_spec = importlib.util.spec_from_file_location(
    "tpc294_independent_frozen_engine", ENGINE_CODE)
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


def shell_between(q0: int) -> list[int]:
    return [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]


def source_first_output(indices: list[int], beta: list[Fraction], height: int,
                        prime: int, exponent: int) -> list[Fraction]:
    """Accumulate in source-coordinate order, unlike the producer."""
    output = [Fraction(0) for _ in indices]
    for source, coefficient in zip(indices, beta):
        if source % prime == 0:
            continue
        for target_position, target in enumerate(indices):
            if target == source or target % prime == 0:
                continue
            centered = Fraction(int(target % prime == source % prime), 1)
            centered -= Fraction(1, prime - 1)
            output[target_position] += (
                prime * ENGINE.kernel(target - source, height, exponent)
                * centered * coefficient)
    return output


def integer_matrix(gram: list[list[Fraction]]) -> tuple[list[list[int]], int]:
    denominator = 1
    for row in gram:
        for entry in row:
            denominator = math.lcm(denominator, entry.denominator)
    return ([[entry.numerator * (denominator // entry.denominator)
              for entry in row] for row in gram], denominator)


def enumerate_extrema(matrix: list[list[int]]) -> dict[str, Any]:
    """Independent direct enumeration with a reflected binary state."""
    m = len(matrix)
    best_min: int | None = None
    best_max: int | None = None
    min_label: tuple[int, ...] | None = None
    max_label: tuple[int, ...] | None = None
    min_count = 0
    max_count = 0
    for code in range(1 << (m - 1)):
        labels = (1,) + tuple(
            1 if ((code >> (vertex - 1)) & 1) == 0 else -1
            for vertex in range(1, m))
        value = sum(labels[i] * labels[j] * matrix[i][j]
                    for i in range(m) for j in range(m))
        if best_min is None or value < best_min:
            best_min, min_label, min_count = value, labels, 1
        elif value == best_min:
            min_count += 1
            if labels < min_label:
                min_label = labels
        if best_max is None or value > best_max:
            best_max, max_label, max_count = value, labels, 1
        elif value == best_max:
            max_count += 1
            if labels > max_label:
                max_label = labels
    need(best_min is not None and best_max is not None,
         "empty sign domain")
    need(min_label is not None and max_label is not None, "extremal label")
    return {"minimum_integer": best_min, "maximum_integer": best_max,
            "minimum_label": min_label, "maximum_label": max_label,
            "minimum_count": min_count, "maximum_count": max_count,
            "trace_integer": sum(matrix[i][i] for i in range(m)),
            "plus_integer": sum(matrix[i][j]
                                 for i in range(m) for j in range(m))}


def quotient(matrix: list[list[int]], labels: tuple[int, ...],
             trace: int) -> Fraction:
    return Fraction(sum(labels[i] * labels[j] * matrix[i][j]
                        for i in range(len(labels))
                        for j in range(len(labels))), trace)


def maxcut(matrix: list[list[int]]) -> dict[str, Any]:
    signs = [[0 if i == j else (1 if matrix[i][j] > 0 else -1)
              for j in range(len(matrix))] for i in range(len(matrix))]
    best = -1
    witness: tuple[int, ...] | None = None
    count = 0
    for tail in itertools.product((-1, 1), repeat=len(matrix) - 1):
        labels = (1,) + tail
        favorable = sum(labels[i] * labels[j] * signs[i][j] == -1
                        for i in range(len(matrix))
                        for j in range(i + 1, len(matrix)))
        if favorable > best:
            best, witness, count = favorable, labels, 1
        elif favorable == best:
            count += 1
            if labels < witness:
                witness = labels
    need(witness is not None, "max-cut witness")
    return {"favorable_edges": best, "label": witness, "count": count}


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
         "TPC293 audit")
    return {"tpc293_code_sha256": PARENT293_CODE_SHA256,
            "tpc293_result_sha256": PARENT293_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "tpc293_rows": 18, "tpc293_edges": 1380}


def expected_row(scale: int, height: int, q0: int, cutoff: int,
                 exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = shell_between(q0)
    need(len(shell) >= 3, "small shell")
    outputs = [source_first_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices))) for j in range(len(shell))]
            for i in range(len(shell))]
    need(all(gram[i][i] > 0 for i in range(len(shell))), "diagonal")
    scaled, denominator = integer_matrix(gram)
    trace = sum(scaled[i][i] for i in range(len(shell)))
    extrema = enumerate_extrema(scaled)
    need(extrema["trace_integer"] == trace, "trace")
    plus = quotient(scaled, (1,) * len(shell), trace)
    minimum = Fraction(extrema["minimum_integer"], trace)
    maximum = Fraction(extrema["maximum_integer"], trace)
    cut = maxcut(scaled)
    cut_label = cut["label"]
    need(cut_label is not None, "cut label")
    cut_ratio = quotient(scaled, cut_label, trace)
    positive = sum(scaled[i][j] > 0 for i in range(len(shell))
                   for j in range(i + 1, len(shell)))
    negative = sum(scaled[i][j] < 0 for i in range(len(shell))
                   for j in range(i + 1, len(shell)))
    edges = len(shell) * (len(shell) - 1) // 2
    need(positive + negative == edges, "zero edge")
    pattern = "".join(
        "+" if scaled[i][j] > 0 else "-"
        for i in range(len(shell)) for j in range(i + 1, len(shell)))
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "edge_count": edges, "positive_edges": positive,
        "negative_edges": negative, "zero_edges": 0,
        "edge_sign_upper_triangle": pattern,
        "all_positive_ratio": str(plus),
        "all_positive_ratio_decimal": ENGINE.decimal_text(plus),
        "minimum_signed_ratio": str(minimum),
        "minimum_signed_ratio_decimal": ENGINE.decimal_text(minimum),
        "maximum_signed_ratio": str(maximum),
        "maximum_signed_ratio_decimal": ENGINE.decimal_text(maximum),
        "minimum_signed_label": list(extrema["minimum_label"]),
        "maximum_signed_label": list(extrema["maximum_label"]),
        "minimum_label_count_mod_global_sign": extrema["minimum_count"],
        "maximum_label_count_mod_global_sign": extrema["maximum_count"],
        "maxcut_favorable_edges": cut["favorable_edges"],
        "maxcut_label": list(cut_label),
        "maxcut_label_count_mod_global_sign": cut["count"],
        "maxcut_ratio": str(cut_ratio),
        "maxcut_ratio_decimal": ENGINE.decimal_text(cut_ratio),
        "weighted_saving_from_all_positive": str(plus - minimum),
        "weighted_saving_from_all_positive_decimal": ENGINE.decimal_text(
            plus - minimum),
        "maxcut_weighted_gap": str(cut_ratio - minimum),
        "maxcut_weighted_gap_decimal": ENGINE.decimal_text(cut_ratio - minimum),
        "minimum_is_below_one": minimum < 1,
        "all_positive_is_above_one": plus > 1,
        "maxcut_is_below_one": cut_ratio < 1,
        "common_denominator_bits": denominator.bit_length(),
        "common_denominator_digits": len(str(denominator)),
        "trace_integer_digits": len(str(abs(trace))),
    }


def expected_rows() -> list[dict[str, Any]]:
    workers = min(len(ROWS), max(1, os.cpu_count() or 1))
    if workers == 1:
        return [expected_row(*args, axis) for args, axis in ROWS]
    try:
        with mp.get_context("fork").Pool(processes=workers) as pool:
            return pool.starmap(expected_row,
                                [(*args, axis) for args, axis in ROWS])
    except (AttributeError, OSError, RuntimeError):
        return [expected_row(*args, axis) for args, axis in ROWS]


def finite_audit(rows: list[dict[str, Any]]) -> dict[str, Any]:
    minimum_row = min(rows, key=lambda row: (
        Fraction(row["minimum_signed_ratio"]), tuple(row["shell"])))
    maximum_row = max(rows, key=lambda row: (
        Fraction(row["all_positive_ratio"]), tuple(row["shell"])))
    return {
        "rows": len(rows),
        "total_edges": sum(row["edge_count"] for row in rows),
        "minimum_below_one_rows": sum(row["minimum_is_below_one"]
                                       for row in rows),
        "all_positive_above_one_rows": sum(row["all_positive_is_above_one"]
                                           for row in rows),
        "maxcut_below_one_rows": sum(row["maxcut_is_below_one"]
                                      for row in rows),
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
            "ratio_decimal": minimum_row["minimum_signed_ratio_decimal"],
        },
        "largest_all_positive_witness": {
            "axis": maximum_row["axis"], "scale": maximum_row["scale"],
            "H": maximum_row["H"], "Q": maximum_row["Q"],
            "comparison_cutoff_z": maximum_row["comparison_cutoff_z"],
            "kernel_exponent": maximum_row["kernel_exponent"],
            "shell": maximum_row["shell"],
            "ratio": maximum_row["all_positive_ratio"],
            "ratio_decimal": maximum_row["all_positive_ratio_decimal"],
        },
        "growing_weighted_theorem": "OPEN",
        "source_native_coefficient_image": "OPEN",
        "arithmetic_l2": "OPEN_LITERAL_SOURCE",
        "fixed_power_credit": 0,
    }


def main() -> int:
    raw = RESULT.read_bytes()
    actual = json.loads(raw)
    need(raw == canonical(actual), "certificate canonicality")
    need(actual.get("certificate_version") == 1 and
         actual.get("claim_status") == STATUS, "header")
    payload = actual["payload"]
    need(payload.get("schema") == SCHEMA, "schema")
    need(payload.get("parent_lock") == parent_lock(), "parent lock")
    rows = expected_rows()
    need(payload.get("rows") == rows, "independent row replay")
    need(payload.get("finite_audit") == finite_audit(rows), "finite audit")
    firewall = payload.get("firewall", {})
    need(firewall.get("TPC294_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC294_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC294_FIXED_POWER_CREDIT") == 0,
         "claim firewall")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    audit = payload["finite_audit"]
    print("TPC294_INDEPENDENT_CHECK=PASS rows={} edges={} min_below_one={} "
          "plus_above_one={} maxcut_below_one={} differing={}"
          .format(audit["rows"], audit["total_edges"],
                 audit["minimum_below_one_rows"],
                 audit["all_positive_above_one_rows"],
                 audit["maxcut_below_one_rows"],
                 audit["weighted_optimum_differs_from_maxcut_rows"]))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC294_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
