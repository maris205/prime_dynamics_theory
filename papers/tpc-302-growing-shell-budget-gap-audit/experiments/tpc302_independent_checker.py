#!/usr/bin/env python3
"""Independent source-first replay for the TPC-302 growing grid.

This checker deliberately does not import the TPC-302 producer.  It loads the
frozen TPC-288 physical engine, rebuilds every shell Gram matrix, and repeats
the exact global-sign enumeration.  It then checks the published weighted and
positive ratios and the structural budget census.  The expensive mpmath
frontier is produced by the producer; the independent replay attacks the new
source-first target compiler and its exact rational inputs.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_CODE = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/code/"
    "tpc288_growing_shell_gram_certificate.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/results/"
    "tpc288_certificate.json")
CERTIFICATE = PROJECT / "results/tpc302_certificate.json"
PARENT_CODE_SHA256 = (
    "ee88cef250dc37d14b5fa5bbc22cc9cd5d0a44da6a4e4412118895b27e214987")
PARENT_RESULT_SHA256 = (
    "39ab30b6701015bfaf85ebb670706182ecd7b52120e9963d58d0731a0a8e947d")
SCHEMA = "TPC302_GROWING_SHELL_BUDGET_GAP_AUDIT_V1"
PROFILE_CUTOFFS = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)

spec = importlib.util.spec_from_file_location("frozen_tpc288_replay", PARENT_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("parent loader")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)
ENGINE = PARENT.ENGINE


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


def literal_beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    lam = Fraction(0) if power is None else Fraction(1, power[1])
    return lam - sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                      if value % d == 0), 0)


def integer_matrix(matrix: list[list[Fraction]]) -> tuple[list[list[int]], int]:
    denominator = 1
    for row in matrix:
        for value in row:
            denominator = math.lcm(denominator, value.denominator)
    return ([[value.numerator * (denominator // value.denominator)
              for value in row] for row in matrix], denominator)


def minimum_label(matrix: list[list[Fraction]]) -> tuple[tuple[int, ...], Fraction, int]:
    scaled, _ = integer_matrix(matrix)
    m = len(scaled)
    labels = [1] * m
    fields = [sum(scaled[i][j] for j in range(m) if j != i)
              for i in range(m)]
    value = sum(scaled[i][j] for i in range(m) for j in range(m))
    minimum = value
    witness = tuple(labels)
    count = 1
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
                fields[other] -= 2 * old * scaled[other][vertex]
        previous_gray = gray
        candidate = tuple(labels)
        if value < minimum:
            minimum, witness, count = value, candidate, 1
        elif value == minimum:
            count += 1
            if candidate < witness:
                witness = candidate
    trace = sum(scaled[i][i] for i in range(m))
    ratio = Fraction(minimum, trace)
    return witness, ratio, count


def physical_gram(scale: int, height: int, q0: int, cutoff: int,
                  exponent: int) -> tuple[list[int], list[list[Fraction]]]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [PARENT.physical_prime_output(indices, beta, height, prime,
                                             exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices))) for j in range(len(shell))]
            for i in range(len(shell))]
    return shell, gram


def row_specs() -> list[tuple[int, int, int, int, int, str]]:
    answer = []
    for scale, height, q0, cutoff in PARENT.GROWTH_PATH:
        for exponent in (1, 2):
            answer.append((scale, height, q0, cutoff, exponent, "GROWTH_PATH"))
    for scale, height, q0, cutoff, exponent in PARENT.CONTROL_GRID:
        answer.append((scale, height, q0, cutoff, exponent,
                       "SOURCE_CONTROL_GRID"))
    return answer


def check() -> None:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    raw_parent = PARENT_RESULT.read_bytes()
    need(digest(raw_parent) == PARENT_RESULT_SHA256,
         "parent result provenance")
    parent = json.loads(raw_parent)
    need(raw_parent == canonical(parent), "parent canonicality")

    raw = CERTIFICATE.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    payload = data["payload"]
    need(data["certificate_version"] == 1 and
         payload["schema"] == SCHEMA and len(payload["rows"]) == 34,
         "certificate header")
    published = {(
        int(row["scale"]), int(row["H"]), int(row["Q"]),
        int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]),
        row["axis"]): row for row in payload["rows"]}
    need(len(published) == 34, "unique row keys")
    exact_weighted = 0
    exact_positive = 0
    exact_targets = 0
    shell_targets = 0
    for scale, height, q0, cutoff, exponent, axis in row_specs():
        key = (scale, height, q0, cutoff, exponent, axis)
        need(key in published, "missing row")
        row = published[key]
        shell, gram = physical_gram(scale, height, q0, cutoff, exponent)
        witness, weighted_ratio, count = minimum_label(gram)
        scaled, _ = integer_matrix(gram)
        trace = sum(scaled[i][i] for i in range(len(shell)))
        positive_ratio = Fraction(sum(scaled[i][j]
                                     for i in range(len(shell))
                                     for j in range(len(shell))), trace)
        need(row["shell"] == shell, "shell replay")
        need(row["weighted_target_label"] == list(witness),
             "source-first sign witness")
        need(row["weighted_minimum_ratio"] == str(weighted_ratio),
             "weighted ratio replay")
        need(row["positive_ratio"] == str(positive_ratio),
             "positive ratio replay")
        need(row["enumerated_labelings"] == 1 << (len(shell) - 1),
             "enumeration count")
        need(row["minimum_count_mod_global_sign"] == count,
             "minimum multiplicity")
        need(row["weighted_below_one"] == (weighted_ratio < 1),
             "weighted status")
        need(row["positive_above_one"] == (positive_ratio > 1),
             "positive status")
        exact_weighted += weighted_ratio < 1
        exact_positive += positive_ratio > 1
        exact_targets += len(shell)
        shell_targets += len(shell)
    audit = payload["finite_audit"]
    need(exact_weighted == audit["weighted_below_one_rows"] == 34,
         "weighted census")
    need(exact_positive == audit["positive_above_one_rows"] == 34,
         "positive census")
    need(exact_targets == shell_targets == 430 ==
         audit["explicit_shell_target_count"], "shell census")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC302_INDEPENDENT_CHECK=PASS rows=34 source_first_labels=34 "
          "shell_targets=430 weighted_below_one=34 positive_above_one=34")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC302_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
