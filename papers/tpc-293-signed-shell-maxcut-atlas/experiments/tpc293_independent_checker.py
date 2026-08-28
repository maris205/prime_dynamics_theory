#!/usr/bin/env python3
"""Independent exact replay of the TPC-293 signed-shell atlas.

The producer imports the TPC-291 physical-output helper and accumulates each
output by target coordinate.  This checker imports only the frozen TPC-268
engine, accumulates by source coordinate first, and reconstructs the signed
complete-graph objective from scratch.  It deliberately does not import the
TPC-293 producer or trust its result while constructing the expected rows.
"""

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
PROJECT = ROOT / "papers/tpc-293-signed-shell-maxcut-atlas"
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
    "tpc293_independent_frozen_engine", ENGINE_CODE)
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


def sign(value: Fraction) -> int:
    return 1 if value > 0 else -1 if value < 0 else 0


def sign_text(value: int) -> str:
    return "+" if value > 0 else "-" if value < 0 else "0"


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    """Accumulate by source t, then target position u (independent order)."""
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


def shell_between(q0: int) -> list[int]:
    shell: list[int] = []
    for prime in ENGINE.PRIMES:
        if q0 < prime <= 2 * q0:
            shell.append(prime)
    return shell


def expected_row(scale: int, height: int, q0: int, cutoff: int,
                 exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = shell_between(q0)
    need(len(shell) >= 3, "small shell")
    outputs = [physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    need(all(gram[i][i] > 0 for i in range(len(shell))), "diagonal")

    edge_signs = [[0 if i == j else sign(gram[i][j])
                   for j in range(len(shell))] for i in range(len(shell))]
    edge_count = len(shell) * (len(shell) - 1) // 2
    positive = sum(edge_signs[i][j] == 1
                   for i in range(len(shell))
                   for j in range(i + 1, len(shell)))
    negative = sum(edge_signs[i][j] == -1
                   for i in range(len(shell))
                   for j in range(i + 1, len(shell)))
    need(positive + negative == edge_count, "zero edge")

    best = -1
    optimal: list[tuple[int, ...]] = []
    for tail in itertools.product((-1, 1), repeat=len(shell) - 1):
        labels = (1,) + tail
        favorable = sum(
            labels[i] * labels[j] * edge_signs[i][j] == -1
            for i in range(len(shell)) for j in range(i + 1, len(shell)))
        if favorable > best:
            best = favorable
            optimal = [labels]
        elif favorable == best:
            optimal.append(labels)
    need(bool(optimal), "max-cut witness")

    triangles = len(shell) * (len(shell) - 1) * (len(shell) - 2) // 6
    frustrated = 0
    for i, j, k in itertools.combinations(range(len(shell)), 3):
        if edge_signs[i][j] * edge_signs[i][k] * edge_signs[j][k] == 1:
            frustrated += 1
    pattern: list[str] = []
    for i in range(len(shell)):
        for j in range(i + 1, len(shell)):
            pattern.append(sign_text(edge_signs[i][j]))
    all_positive = (len(shell) * len(shell)) // 4
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "edge_count": edge_count, "positive_edges": positive,
        "negative_edges": negative, "zero_edges": 0,
        "max_favorable_edges": best,
        "minimum_unsatisfied_edges": edge_count - best,
        "all_positive_maxcut": all_positive,
        "signed_gain_over_all_positive": best - all_positive,
        "optimal_labelings_mod_global_sign": len(optimal),
        "one_optimal_labeling": list(optimal[0]),
        "edge_sign_upper_triangle": "".join(pattern),
        "triangle_count": triangles,
        "sign_frustrated_triangles": frustrated,
    }


def expected_rows() -> list[dict[str, Any]]:
    workers = min(len(ROWS), max(1, os.cpu_count() or 1))
    if workers == 1:
        return [expected_row(*args, axis) for args, axis in ROWS]
    try:
        context = mp.get_context("fork")
        with context.Pool(processes=workers) as pool:
            return pool.starmap(expected_row,
                                [(*args, axis) for args, axis in ROWS])
    except (AttributeError, OSError, RuntimeError):
        return [expected_row(*args, axis) for args, axis in ROWS]


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT292_CODE.read_bytes()) == PARENT292_CODE_SHA256,
         "TPC292 code provenance")
    raw292 = PARENT292_RESULT.read_bytes()
    need(digest(raw292) == PARENT292_RESULT_SHA256, "TPC292 result provenance")
    data292 = json.loads(raw292)
    need(raw292 == canonical(data292), "TPC292 canonicality")
    need(data292.get("certificate_version") == 1 and
         data292.get("claim_status", "").startswith(
             "PROVED_EXACT_TRIANGLE_SIGN_PARITY"), "TPC292 status")

    need(digest(PARENT291_CODE.read_bytes()) == PARENT291_CODE_SHA256,
         "TPC291 code provenance")
    raw291 = PARENT291_RESULT.read_bytes()
    need(digest(raw291) == PARENT291_RESULT_SHA256, "TPC291 result provenance")
    data291 = json.loads(raw291)
    need(raw291 == canonical(data291), "TPC291 canonicality")
    need(data291.get("certificate_version") == 1 and
         data291.get("claim_status", "").startswith(
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
    audit = payload["finite_audit"]
    need(audit == {
        "all_positive_rows": 17,
        "fixed_power_credit": 0,
        "global_maxcut_gain_row": {
            "H": 38, "Q": 27, "axis": "EXPONENT_CROSSOVER",
            "comparison_cutoff_z": 5, "kernel_exponent": 1,
            "scale": 256,
        },
        "growing_signed_graph_theorem": "OPEN",
        "magnitude_weighted_objective": "OPEN",
        "rows": 18,
        "signed_gain_rows": 1,
        "source_native_L2": "OPEN",
        "total_edges": 1380,
        "total_max_favorable_edges": 744,
        "total_minimum_unsatisfied_edges": 636,
        "total_sign_frustrated_triangles": 5718,
        "total_signed_gain_over_all_positive": 3,
        "total_triangles": 5727,
    }, "finite audit")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC293_INDEPENDENT_CHECK=PASS rows=18 edges=1380 "
          "max_favorable=744 unsatisfied=636 signed_gain=3 "
          "frustrated_triangles=5718")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC293_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
