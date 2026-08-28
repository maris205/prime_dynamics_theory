#!/usr/bin/env python3
"""Exact signed-graph max-cut atlas for the TPC-292 prime shells.

TPC-292 detects triangle parity.  TPC-293 asks the shell-level combinatorial
question: how many Gram edges can one global coefficient-sign assignment make
cancellation-favourable?  The finite result is a sign-only diagnostic; edge
magnitudes and source-image feasibility are deliberately deferred.
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
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT292_CODE = ROOT / (
    "papers/tpc-292-three-prime-sign-frustration-atlas/code/"
    "tpc292_three_prime_sign_frustration_certificate.py")
PARENT292_RESULT = ROOT / (
    "papers/tpc-292-three-prime-sign-frustration-atlas/results/"
    "tpc292_certificate.json")
PARENT291_CODE = ROOT / (
    "papers/tpc-291-signed-schur-cancellation-atlas/code/"
    "tpc291_signed_schur_cancellation_certificate.py")
PARENT291_RESULT = ROOT / (
    "papers/tpc-291-signed-schur-cancellation-atlas/results/"
    "tpc291_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc293_certificate.json"

PARENT292_CODE_SHA256 = (
    "4b4d13bb6ca6c895e1dde64c7010e22516c064915c7bdd0457e1298ab3774115")
PARENT292_RESULT_SHA256 = (
    "47c45d227fc6654a2e8dba9472630f2876ce88b387de79faf487178bf3e82ab8")
PARENT291_CODE_SHA256 = (
    "368202bcf8b39db0429c9ef8b9546f5041eb2a0c749c20fa539d5f3b6a76584d")
PARENT291_RESULT_SHA256 = (
    "b6743bcc574e3fe865832e4867a6d696aa70dd700bceaf1f8b1b7b1f866344b0")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

STATUS = (
    "PROVED_EXACT_ALL_POSITIVE_MAXCUT_PLUS_NUMERICALLY_CERTIFIED_FINITE_"
    "SIGNED_SHELL_FRUSTRATION_ATLAS")
SCHEMA = "TPC293_SIGNED_SHELL_MAXCUT_CERTIFICATE_V1"
ROUND2_CLUE = "TEST_MAGNITUDE_WEIGHTED_SIGNED_RAYLEIGH_AND_SOURCE_IMAGE"

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


def sign(value: Any) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def sign_text(value: int) -> str:
    return "+" if value > 0 else "-" if value < 0 else "0"


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT292_CODE.read_bytes()) == PARENT292_CODE_SHA256,
         "TPC292 code provenance")
    raw292 = PARENT292_RESULT.read_bytes()
    need(digest(raw292) == PARENT292_RESULT_SHA256,
         "TPC292 result provenance")
    parent292 = json.loads(raw292)
    need(raw292 == canonical(parent292), "TPC292 canonicality")
    need(parent292.get("certificate_version") == 1 and
         parent292.get("claim_status", "").startswith(
             "PROVED_EXACT_TRIANGLE_SIGN_PARITY"), "TPC292 status")
    need(parent292.get("payload", {}).get("finite_audit", {}).get(
        "total_triples") == 5727, "TPC292 triple count")

    need(digest(PARENT291_CODE.read_bytes()) == PARENT291_CODE_SHA256,
         "TPC291 code provenance")
    raw291 = PARENT291_RESULT.read_bytes()
    need(digest(raw291) == PARENT291_RESULT_SHA256,
         "TPC291 result provenance")
    parent291 = json.loads(raw291)
    need(raw291 == canonical(parent291), "TPC291 canonicality")
    need(parent291.get("certificate_version") == 1 and
         parent291.get("claim_status", "").startswith(
             "PROVED_EXACT_SIGNED_TWO_PRIME_SCHUR_CANCELLATION"),
         "TPC291 status")
    return {
        "tpc292_code_sha256": PARENT292_CODE_SHA256,
        "tpc292_result_sha256": PARENT292_RESULT_SHA256,
        "tpc291_code_sha256": PARENT291_CODE_SHA256,
        "tpc291_result_sha256": PARENT291_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc292_triples": 5727,
    }


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    # Keep the shell construction explicit.  This also avoids a Python
    # comprehension-cell collision on some 3.12 worker/interpreter layouts.
    primes: list[int] = []
    for prime in ENGINE.PRIMES:
        if q0 < prime <= 2 * q0:
            primes.append(prime)
    need(bool(primes), "empty shell")
    outputs = [PARENT.physical_output(indices, beta, height, q, exponent)
               for q in primes]
    gram = [[sum(x * y for x, y in zip(outputs[i], outputs[j]))
             for j in range(len(primes))] for i in range(len(primes))]
    signs = [[0 if i == j else sign(gram[i][j])
              for j in range(len(primes))] for i in range(len(primes))]
    edge_count = len(primes) * (len(primes) - 1) // 2
    positive_edges = sum(signs[i][j] == 1
                         for i in range(len(primes))
                         for j in range(i + 1, len(primes)))
    negative_edges = sum(signs[i][j] == -1
                         for i in range(len(primes))
                         for j in range(i + 1, len(primes)))
    zero_edges = edge_count - positive_edges - negative_edges
    need(zero_edges == 0, "zero Gram edge")

    best = -1
    optimal: list[tuple[int, ...]] = []
    for tail in itertools.product((-1, 1), repeat=len(primes) - 1):
        labels = (1,) + tail  # remove the global sign symmetry
        favorable = sum(labels[i] * labels[j] * signs[i][j] == -1
                        for i in range(len(primes))
                        for j in range(i + 1, len(primes)))
        if favorable > best:
            best = favorable
            optimal = [labels]
        elif favorable == best:
            optimal.append(labels)
    need(best >= 0 and bool(optimal), "max-cut search")
    all_positive_max = (len(primes) * len(primes)) // 4
    total_triangles = len(primes) * (len(primes) - 1) * (len(primes) - 2) // 6
    frustrated_triangles = 0
    for i, j, k in itertools.combinations(range(len(primes)), 3):
        if signs[i][j] * signs[i][k] * signs[j][k] == 1:
            frustrated_triangles += 1
    # Store the upper-triangular signed graph compactly and deterministically.
    edge_pattern = []
    for i in range(len(primes)):
        for j in range(i + 1, len(primes)):
            edge_pattern.append(sign_text(signs[i][j]))
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": primes, "shell_cardinality": len(primes),
        "edge_count": edge_count, "positive_edges": positive_edges,
        "negative_edges": negative_edges, "zero_edges": zero_edges,
        "max_favorable_edges": best,
        "minimum_unsatisfied_edges": edge_count - best,
        "all_positive_maxcut": all_positive_max,
        "signed_gain_over_all_positive": best - all_positive_max,
        "optimal_labelings_mod_global_sign": len(optimal),
        "one_optimal_labeling": list(optimal[0]),
        "edge_sign_upper_triangle": "".join(edge_pattern),
        "triangle_count": total_triangles,
        "sign_frustrated_triangles": frustrated_triangles,
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
    total_edges = sum(row["edge_count"] for row in rows)
    total_favorable = sum(row["max_favorable_edges"] for row in rows)
    total_unsatisfied = sum(row["minimum_unsatisfied_edges"] for row in rows)
    total_triangles = sum(row["triangle_count"] for row in rows)
    total_frustrated = sum(row["sign_frustrated_triangles"] for row in rows)
    signed_gain = sum(row["signed_gain_over_all_positive"] for row in rows)
    need((len(rows), total_edges, total_favorable, total_unsatisfied,
          signed_gain, total_triangles, total_frustrated) ==
         (18, 1380, 744, 636, 3, 5727, 5718),
         "finite signed-shell census")
    need(rows[8]["max_favorable_edges"] == 15 and
         rows[8]["negative_edges"] == 3 and
         rows[8]["signed_gain_over_all_positive"] == 3,
         "exceptional signed row")
    need(all(row["max_favorable_edges"] == row["all_positive_maxcut"]
             for index, row in enumerate(rows) if index != 8),
         "all-positive max-cut rows")
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "all_positive_complete_graph": (
                "max favorable cancellation edges in K_m is floor(m^2/4), "
                "by the complete-graph max-cut bound"),
            "signed_objective": (
                "maximize #{i<j: a_i*a_j*sign(G_ij)=-1} over a_i in {+-1}"),
            "frustration_index": (
                "minimum unsatisfied signed edges equals total edges minus "
                "the signed max-cut value"),
            "scope": "finite sign graph of frozen physical prime components",
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
            "rows": len(rows), "total_edges": total_edges,
            "total_max_favorable_edges": total_favorable,
            "total_minimum_unsatisfied_edges": total_unsatisfied,
            "total_signed_gain_over_all_positive": signed_gain,
            "total_triangles": total_triangles,
            "total_sign_frustrated_triangles": total_frustrated,
            "all_positive_rows": sum(
                row["max_favorable_edges"] == row["all_positive_maxcut"]
                for row in rows),
            "signed_gain_rows": sum(row["signed_gain_over_all_positive"] > 0
                                     for row in rows),
            "global_maxcut_gain_row": {
                "axis": rows[8]["axis"], "scale": rows[8]["scale"],
                "H": rows[8]["H"], "Q": rows[8]["Q"],
                "comparison_cutoff_z": rows[8]["comparison_cutoff_z"],
                "kernel_exponent": rows[8]["kernel_exponent"],
            },
            "growing_signed_graph_theorem": "OPEN",
            "magnitude_weighted_objective": "OPEN",
            "source_native_L2": "OPEN",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC293_ALL_POSITIVE_MAXCUT": "PROVED_EXACT_CONDITIONAL",
            "TPC293_SIGNED_MAXCUT_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
            "TPC293_FRUSTRATION_INDEX_ATLAS":
                "NUMERICALLY_CERTIFIED_FINITE_18_ROWS",
            "TPC293_EXCEPTIONAL_SIGNED_GAIN":
                "NUMERICALLY_CERTIFIED_FINITE_PLUS_3_EDGES_ONE_ROW",
            "TPC293_GROWING_SIGNED_GRAPH": "OPEN",
            "TPC293_MAGNITUDE_WEIGHTED_RAYLEIGH": "OPEN",
            "TPC293_SOURCE_NATIVE_L2": "OPEN_LITERAL_SOURCE",
            "TPC293_FIXED_POWER_CREDIT": 0,
            "TPC293_FULL_GATE_B": "OPEN",
            "TPC293_TWIN_PRIME_RESULT": "NONE",
            "TPC293_STATUS": STATUS,
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
    print("TPC293_CERTIFICATE=PASS rows={} edges={} max_favorable={} "
          "unsatisfied={} signed_gain={} frustrated_triangles={}".format(
              audit["rows"], audit["total_edges"],
              audit["total_max_favorable_edges"],
              audit["total_minimum_unsatisfied_edges"],
              audit["total_signed_gain_over_all_positive"],
              audit["total_sign_frustrated_triangles"]))


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
        print("TPC293_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
