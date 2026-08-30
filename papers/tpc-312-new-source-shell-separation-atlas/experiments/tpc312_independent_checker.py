#!/usr/bin/env python3
"""Independent exact replay for TPC-312.

The checker intentionally does not import the TPC-312 producer or TPC-288's
output routine.  It imports only the locked finite arithmetic engine and
rebuilds the deleted-diagonal prime outputs, Gram matrices, modular ranks, and
Gray-code sign extrema from scratch.
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

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-312-new-source-shell-separation-atlas"
RESULT = PROJECT / "results/tpc312_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
TPC311_RESULT = ROOT / (
    "papers/tpc-311-stratified-tau-holdout-replication/results/"
    "tpc311_certificate.json")

ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
TPC311_RESULT_SHA256 = (
    "0e7ac4ef8d7f62d152ce364a46e5c6f09cabd8e38af3448f65b7249bdda95acd")
STATUS = (
    "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS")
SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"
MODULUS = 1_000_000_007
SCALE = 640
HEIGHT = 66
QS = (24, 36, 54, 80)
EXPONENTS = (1, 2)

spec = importlib.util.spec_from_file_location("locked_engine_for_tpc312_check",
                                               ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("locked arithmetic engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class Failure(RuntimeError):
    pass


def need(ok: bool, message: str) -> None:
    if type(ok) is not bool or not ok:
        raise Failure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load_certificate() -> dict[str, Any]:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "certificate payload hash")
    payload = data["payload"]
    need(payload.get("schema") == SCHEMA, "schema")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_SHA256,
         "engine provenance")
    parent = TPC311_RESULT.read_bytes()
    need(digest(parent) == TPC311_RESULT_SHA256, "TPC-311 provenance")
    return payload


def physical_prime_output(indices: list[int], beta: list[Fraction],
                          prime: int, exponent: int) -> list[Fraction]:
    """Independent copy of the literal deleted-diagonal prime component."""
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1)
            centered -= Fraction(1, prime - 1)
            total += (prime * ENGINE.kernel(u - t, HEIGHT, exponent) *
                      centered * beta_t)
        output.append(total)
    return output


def fraction_mod(value: Fraction) -> int:
    denominator = value.denominator % MODULUS
    need(denominator != 0, "non-invertible denominator")
    return value.numerator % MODULUS * pow(
        denominator, MODULUS - 2, MODULUS) % MODULUS


def rank_mod(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    matrix = [row[:] for row in matrix]
    rows, columns = len(matrix), len(matrix[0])
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, rows)
                      if matrix[i][column] % MODULUS), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        row = matrix[rank]
        inverse = pow(row[column] % MODULUS, MODULUS - 2, MODULUS)
        for j in range(column, columns):
            row[j] = row[j] * inverse % MODULUS
        for i in range(rank + 1, rows):
            factor = matrix[i][column] % MODULUS
            if factor:
                for j in range(column, columns):
                    matrix[i][j] = (matrix[i][j] - factor * row[j]) % MODULUS
        rank += 1
        if rank == rows:
            break
    return rank


def extrema(gram: list[list[Fraction]]) -> tuple[dict[str, Any], Fraction,
                                                   Fraction]:
    denominator = 1
    for row in gram:
        for value in row:
            denominator = math.lcm(denominator, value.denominator)
    scaled = [[value.numerator * (denominator // value.denominator)
               for value in row] for row in gram]
    size = len(scaled)
    labels = [1] * size
    fields = [sum(scaled[i][j] for j in range(size) if j != i)
              for i in range(size)]
    value = sum(scaled[i][j] for i in range(size) for j in range(size))
    minimum = maximum = value
    minimum_label = maximum_label = tuple(labels)
    minimum_count = maximum_count = 1
    previous = 0
    for code in range(1, 1 << (size - 1)):
        gray = code ^ (code >> 1)
        changed = gray ^ previous
        vertex = changed.bit_length()
        old = labels[vertex]
        value -= 4 * old * fields[vertex]
        labels[vertex] = -old
        for other in range(size):
            if other != vertex:
                fields[other] -= 2 * old * scaled[other][vertex]
        previous = gray
        candidate = tuple(labels)
        if value < minimum:
            minimum, minimum_label, minimum_count = value, candidate, 1
        elif value == minimum:
            minimum_count += 1
            minimum_label = min(minimum_label, candidate)
        if value > maximum:
            maximum, maximum_label, maximum_count = value, candidate, 1
        elif value == maximum:
            maximum_count += 1
            maximum_label = max(maximum_label, candidate)
    trace = sum(scaled[i][i] for i in range(size))
    return ({"minimum_label": minimum_label, "maximum_label": maximum_label,
             "minimum_count": minimum_count, "maximum_count": maximum_count,
             "enumerated": 1 << (size - 1),
             "trace": trace, "minimum": minimum, "maximum": maximum},
            Fraction(minimum, trace), Fraction(maximum, trace))


def check_row(stored: dict[str, Any], q0: int, exponent: int,
              indices: list[int], beta: list[Fraction]) -> tuple[Fraction,
                                                                      Fraction]:
    shell = [p for p in ENGINE.PRIMES if q0 < p <= 2 * q0]
    outputs = [physical_prime_output(indices, beta, p, exponent)
               for p in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u] for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    need(stored["Q"] == q0 and stored["kernel_exponent"] == exponent,
         "row key")
    need(stored["prime_shell"] == shell and
         stored["shell_cardinality"] == len(shell), "shell")
    need(all(gram[i][j] == gram[j][i]
             for i in range(len(shell)) for j in range(len(shell))),
         "Gram symmetry")
    modular = [[sum(fraction_mod(outputs[i][u]) *
                    fraction_mod(outputs[j][u]) for u in range(len(indices)))
                % MODULUS for j in range(len(shell))]
               for i in range(len(shell))]
    need(rank_mod(modular) == len(shell), "full modular rank")
    ext, minimum, maximum = extrema(gram)
    need(ext["enumerated"] == stored["enumerated_labelings_mod_global_sign"],
         "enumeration count")
    need(list(ext["minimum_label"]) == stored["minimum_label"] and
         list(ext["maximum_label"]) == stored["maximum_label"], "labels")
    need(ext["minimum_count"] == stored["minimum_count_mod_global_sign"] and
         ext["maximum_count"] == stored["maximum_count_mod_global_sign"],
         "extremum multiplicity")
    need(hashlib.sha256(str(Fraction(ext["minimum"], ext["trace"])).encode(
        "ascii")).hexdigest() == stored["minimum_ratio_rational_sha256"],
         "minimum ratio digest")
    need(hashlib.sha256(str(Fraction(ext["maximum"], ext["trace"])).encode(
        "ascii")).hexdigest() == stored["maximum_ratio_rational_sha256"],
         "maximum ratio digest")
    need(ENGINE.decimal_text(minimum, digits=24) ==
         stored["minimum_ratio_decimal"] and
         ENGINE.decimal_text(maximum, digits=24) ==
         stored["maximum_ratio_decimal"], "decimal replay")
    need(minimum < 1 < maximum and stored["minimum_below_one"] and
         stored["positive_maximum_above_one"], "strict separation")
    return minimum, maximum


def main() -> int:
    try:
        payload = load_certificate()
        protocol = payload["protocol"]
        need(protocol["source_scale"] == SCALE and
             protocol["index_interval"] == [321, 640] and
             protocol["height"] == HEIGHT and
             protocol["Q_anchors"] == list(QS) and
             protocol["kernel_exponents"] == list(EXPONENTS), "protocol")
        rows = payload["rows"]
        need(len(rows) == 8, "row count")
        indices = list(range(321, 641))
        beta = [ENGINE.beta_value(value, SCALE) for value in indices]
        values: dict[tuple[int, int], tuple[Fraction, Fraction]] = {}
        for stored, (q0, exponent) in zip(
                rows, ((q, e) for q in QS for e in EXPONENTS)):
            values[(q0, exponent)] = check_row(stored, q0, exponent,
                                                indices, beta)
        for exponent in EXPONENTS:
            for left, right in zip(QS, QS[1:]):
                need(values[(left, exponent)][0] >
                     values[(right, exponent)][0], "minimum Q ordering")
                need(values[(left, exponent)][1] <
                     values[(right, exponent)][1], "maximum Q ordering")
        for q0 in QS:
            need(values[(q0, 2)][0] < values[(q0, 1)][0] and
                 values[(q0, 2)][1] > values[(q0, 1)][1],
                 "exponent ordering")
        print("TPC312_INDEPENDENT_CHECK=PASS rows=8 exact_gram=8 "
              "full_rank=8 sign_extrema=8 ordering=8")
        return 0
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC312_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
