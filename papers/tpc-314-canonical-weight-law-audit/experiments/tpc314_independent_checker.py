#!/usr/bin/env python3
"""Independent exact replay for TPC-314.

This checker intentionally loads only the frozen TPC-268 arithmetic engine.
It copies the deleted-diagonal physical operator, rebuilds every Gram matrix,
reconstructs the three weight laws, and verifies the rational/outward
interval certificate without importing the TPC-314 producer or TPC-312's
producer.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import multiprocessing as mp_pool
import os
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-314-canonical-weight-law-audit"
RESULT = PROJECT / "results/tpc314_certificate.json"
PARENT_CODE = ROOT / (
    "papers/tpc-312-new-source-shell-separation-atlas/code/"
    "tpc312_new_source_shell_separation.py")
PARENT_RESULT = ROOT / (
    "papers/tpc-312-new-source-shell-separation-atlas/results/"
    "tpc312_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

PARENT_CODE_SHA256 = (
    "dc0d371c71069e97cf685f46163efc285ba8a38801f3732b9283ec990426ddb9")
PARENT_RESULT_SHA256 = (
    "04528d9b7381d2f1b3e1e8ff7854114752816fca49ff8779de5a07714b95224d")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_"
    "NEW_PANEL_ROBUSTNESS_AUDIT")
SCHEMA = "TPC314_EXTERNALLY_MOTIVATED_WEIGHT_LAW_AUDIT_V1"
PARENT_STATUS = (
    "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS")
PARENT_SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"

SCALE = 640
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("COUNTING", "REDUCED_RESIDUE", "VON_MANGOLDT")
LOG_TERMS = 120
GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS

engine_spec = importlib.util.spec_from_file_location(
    "locked_tpc268_for_tpc314_checker", ENGINE_CODE)
if engine_spec is None or engine_spec.loader is None:
    raise RuntimeError("locked arithmetic engine unavailable")
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


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def decimal(value: Fraction, digits: int = 18) -> str:
    return ENGINE.decimal_text(value, digits=digits)


def grid_floor(value: Fraction) -> Fraction:
    quotient, _ = divmod(value.numerator * GRID, value.denominator)
    return Fraction(quotient, GRID)


def grid_ceil(value: Fraction) -> Fraction:
    quotient, remainder = divmod(value.numerator * GRID,
                                  value.denominator)
    return Fraction(quotient + int(remainder != 0), GRID)


def fixed_decimal(value: Fraction) -> str:
    scaled = value * GRID
    need(scaled.denominator == 1, "non-grid endpoint")
    number = scaled.numerator
    sign = "-" if number < 0 else ""
    number = abs(number)
    whole, remainder = divmod(number, GRID)
    if remainder == 0:
        return sign + str(whole)
    tail = f"{remainder:0{GRID_DIGITS}d}".rstrip("0")
    return sign + str(whole) + "." + tail


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int,
                 hi: Fraction | int | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
        need(raw_lo <= raw_hi, "reversed raw interval")
        self.lo = grid_floor(raw_lo)
        self.hi = grid_ceil(raw_hi)
        need(self.lo <= self.hi, "reversed rounded interval")

    def __add__(self, other: Interval | Fraction | int) -> Interval:
        right = as_interval(other)
        return Interval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval | Fraction | int) -> Interval:
        return self + (-as_interval(other))

    def __rsub__(self, other: Interval | Fraction | int) -> Interval:
        return as_interval(other) - self

    def __mul__(self, other: Interval | Fraction | int) -> Interval:
        right = as_interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction | int) -> Interval:
        right = as_interval(other)
        need(right.lo > 0 or right.hi < 0, "zero-crossing denominator")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))


def as_interval(value: Interval | Fraction | int) -> Interval:
    return value if isinstance(value, Interval) else Interval(value)


def interval_text(value: Interval) -> list[str]:
    return [fixed_decimal(value.lo), fixed_decimal(value.hi)]


def interval_digest(value: Interval) -> str:
    return hashlib.sha256(
        f"{value.lo.numerator}/{value.lo.denominator}|"
        f"{value.hi.numerator}/{value.hi.denominator}\n".encode("ascii")
    ).hexdigest()


def parse_interval(raw: Any) -> Interval:
    need(isinstance(raw, list) and len(raw) == 2, "stored interval")
    return Interval(Fraction(raw[0]), Fraction(raw[1]))


def load_documents() -> tuple[dict[str, Any],
                                dict[tuple[int, int], dict[str, Any]],
                                dict[tuple[int, int], dict[str, Any]]]:
    raw = RESULT.read_bytes()
    document = json.loads(raw)
    need(raw == canonical(document), "certificate canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == STATUS, "certificate header")
    payload = document["payload"]
    need(payload.get("schema") == SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")

    parent_raw = PARENT_RESULT.read_bytes()
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    need(digest(parent_raw) == PARENT_RESULT_SHA256,
         "parent result provenance")
    parent = json.loads(parent_raw)
    need(parent_raw == canonical(parent), "parent canonicality")
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") == PARENT_STATUS and
         parent.get("payload", {}).get("schema") == PARENT_SCHEMA,
         "parent header")
    parent_rows = {(int(row["Q"]), int(row["kernel_exponent"])): row
                   for row in parent["payload"]["rows"]}
    need(len(parent_rows) == 8, "parent row census")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_SHA256,
         "engine provenance")
    rows = {(int(row["Q"]), int(row["kernel_exponent"])): row
            for row in payload.get("rows", [])}
    need(len(rows) == 8, "certificate row census")
    return payload, rows, parent_rows


def log_from_atanh(z: Fraction, terms: int = LOG_TERMS) -> Interval:
    need(Fraction(0) <= z < 1, "atanh argument")
    partial = sum((z ** (2 * j + 1)) / (2 * j + 1)
                  for j in range(terms)) * 2
    tail = (2 * z ** (2 * terms + 1) /
            ((2 * terms + 1) * (1 - z * z)))
    return Interval(partial, partial + tail)


LOG2_INTERVAL = log_from_atanh(Fraction(1, 3))
LOG_CACHE: dict[int, Interval] = {}


def log_prime_interval(prime: int) -> Interval:
    if prime not in LOG_CACHE:
        k = prime.bit_length() - 1
        power = 2 ** k
        y = Fraction(prime, power)
        z = (y - 1) / (y + 1)
        LOG_CACHE[prime] = Interval(k) * LOG2_INTERVAL + log_from_atanh(z)
    return LOG_CACHE[prime]


def make_weights(law: str, shell: list[int]
                 ) -> list[Fraction] | list[Interval]:
    need(law in LAWS, "law name")
    if law == "COUNTING":
        return [Fraction(1) for _ in shell]
    if law == "REDUCED_RESIDUE":
        return [Fraction(1, prime - 1) for prime in shell]
    return [log_prime_interval(prime) for prime in shell]


def weights_digest(weights: list[Fraction] | list[Interval]) -> str:
    text = ""
    for value in weights:
        interval = as_interval(value)
        text += (f"{interval.lo.numerator}/{interval.lo.denominator}|"
                 f"{interval.hi.numerator}/{interval.hi.denominator}\n")
    return hashlib.sha256(text.encode("ascii")).hexdigest()


def physical_prime_output(indices: list[int], beta: list[Fraction],
                          prime: int, exponent: int) -> list[Fraction]:
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


def row_matrices(q0: int, exponent: int) -> tuple[
        list[int], list[int], list[list[Fraction]]]:
    indices = list(range(SCALE // 2 + 1, SCALE + 1))
    beta = [ENGINE.beta_value(value, SCALE) for value in indices]
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [physical_prime_output(indices, beta, prime, exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    return indices, shell, gram


def exact_ratio(gram: list[list[Fraction]], labels: list[int],
                weights: list[Fraction]) -> Fraction:
    numerator = sum((labels[i] * labels[j] * weights[i] * gram[i][j] *
                     weights[j]
                     for i in range(len(labels))
                     for j in range(len(labels))), Fraction(0))
    denominator = sum((weights[i] * gram[i][i] * weights[i]
                       for i in range(len(labels))), Fraction(0))
    need(denominator > 0, "exact denominator")
    return numerator / denominator


def interval_ratio(gram: list[list[Fraction]], labels: list[int],
                   weights: list[Fraction] | list[Interval]
                   ) -> tuple[Interval, Interval, Interval]:
    numerator = Interval(0)
    denominator = Interval(0)
    for i in range(len(labels)):
        wi = as_interval(weights[i])
        denominator += wi * gram[i][i] * wi
        for j in range(len(labels)):
            numerator += wi * gram[i][j] * as_interval(weights[j]) * (
                labels[i] * labels[j])
    need(denominator.lo > 0, "interval denominator")
    return numerator / denominator, numerator, denominator


def order_laws(cases: list[dict[str, Any]]) -> list[str]:
    indexed = {case["law"]: case for case in cases}
    need(set(indexed) == set(LAWS), "order law census")
    ordered = sorted(
        LAWS, key=lambda law: Fraction(indexed[law]["ratio_interval"][0]))
    for left, right in zip(ordered, ordered[1:]):
        need(Fraction(indexed[left]["ratio_interval"][1]) <
             Fraction(indexed[right]["ratio_interval"][0]),
             "overlapping law intervals")
    return ordered


def check_case(case: dict[str, Any], law: str, target_name: str,
               labels: list[int], shell: list[int],
               gram: list[list[Fraction]],
               weights: list[Fraction] | list[Interval]) -> None:
    need(case.get("law") == law and case.get("target") == target_name,
         "case identity")
    need(case.get("label_vector") == labels and case.get("shell") == shell,
         "case labels")
    ratio_i, numerator_i, denominator_i = interval_ratio(gram, labels, weights)
    need(case.get("numerator_interval") == interval_text(numerator_i),
         "numerator interval")
    need(case.get("denominator_interval") == interval_text(denominator_i),
         "denominator interval")
    need(case.get("ratio_interval") == interval_text(ratio_i),
         "ratio interval")
    need(case.get("ratio_interval_sha256") == interval_digest(ratio_i),
         "ratio interval digest")
    if law == "VON_MANGOLDT":
        display = decimal(Fraction(ratio_i.lo + ratio_i.hi, 2))
        need(case.get("exact_ratio_sha256") is None, "log exact digest")
    else:
        exact = exact_ratio(gram, labels,
                            [Fraction(value) for value in weights])
        need(ratio_i.lo <= exact <= ratio_i.hi, "exact ratio enclosure")
        display = decimal(exact)
        need(case.get("exact_ratio_sha256") == fraction_digest(exact),
             "exact ratio digest")
    need(case.get("ratio_display_decimal") == display, "display ratio")
    below = ratio_i.hi < 1
    above = ratio_i.lo > 1
    need(below != above, "ratio straddles one")
    need(case.get("strict_below_one") is below and
         case.get("strict_above_one") is above, "classification flags")
    need(case.get("classification") ==
         ("BELOW_ONE" if below else "ABOVE_ONE"), "classification")


def check_row(row: dict[str, Any], parent: dict[str, Any]) -> tuple[int, int]:
    q0 = int(row["Q"])
    exponent = int(row["kernel_exponent"])
    need((q0, exponent) in {(q, e) for q in Q_ANCHORS for e in EXPONENTS},
         "row key")
    indices, shell, gram = row_matrices(q0, exponent)
    need(row.get("source_interval") == [321, 640] and
         row.get("index_count") == len(indices) and
         row.get("shell") == shell and
         row.get("shell_cardinality") == len(shell), "row geometry")
    need(parent["prime_shell"] == shell, "parent shell")
    minimum = [int(value) for value in parent["minimum_label"]]
    plus = [1] * len(shell)
    need(row.get("minimum_label") == minimum and
         row.get("positive_label") == plus, "target labels")
    trace = sum((gram[i][i] for i in range(len(shell))), Fraction(0))
    need(row.get("gram_trace_rational_sha256") == fraction_digest(trace),
         "trace digest")
    need(row.get("inherited_modular_rank") == parent["modular_gram_rank"],
         "rank inheritance")
    need(len(row.get("laws", [])) == 3, "law count")
    saved_cases: dict[str, list[dict[str, Any]]] = {}
    for law_record, law in zip(row["laws"], LAWS):
        need(law_record.get("law") == law, "law order")
        weights = make_weights(law, shell)
        expected_intervals = [interval_text(as_interval(value))
                              for value in weights]
        need(law_record.get("weight_vector_intervals") == expected_intervals,
             "weight vector intervals")
        need(law_record.get("weight_vector_sha256") == weights_digest(weights),
             "weight vector digest")
        need(law_record.get("log_enclosure_terms") ==
             (LOG_TERMS if law == "VON_MANGOLDT" else None),
             "log term field")
        cases = law_record.get("cases", [])
        need(len(cases) == 2, "target case count")
        check_case(cases[0], law, "minimum", minimum, shell, gram, weights)
        check_case(cases[1], law, "plus", plus, shell, gram, weights)
        saved_cases[law] = cases
    minimum_cases = [saved_cases[law][0] for law in LAWS]
    positive_cases = [saved_cases[law][1] for law in LAWS]
    need(row.get("minimum_law_order_ascending") == order_laws(minimum_cases),
         "minimum law order")
    need(row.get("positive_law_order_ascending") == order_laws(positive_cases),
         "positive law order")
    need(all(case["strict_below_one"] for case in minimum_cases),
         "minimum separation")
    need(all(case["strict_above_one"] for case in positive_cases),
         "positive separation")
    return q0, exponent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        parser.error("explicit --check is required")
    try:
        payload, rows, parent_rows = load_documents()
        protocol = payload.get("protocol", {})
        need(protocol.get("source_interval") == [321, 640] and
             protocol.get("source_scale") == SCALE and
             protocol.get("height") == HEIGHT and
             protocol.get("Q_anchors") == list(Q_ANCHORS) and
             protocol.get("kernel_exponents") == list(EXPONENTS) and
             protocol.get("laws") == list(LAWS) and
             protocol.get("log_terms") == LOG_TERMS and
             protocol.get("grid_digits") == GRID_DIGITS and
             protocol.get("weights_locked_before_target_readout") is True,
             "protocol")
        arguments = [(rows[(q, e)], parent_rows[(q, e)])
                     for q in Q_ANCHORS for e in EXPONENTS]
        workers_text = os.environ.get("TPC314_CHECK_WORKERS", str(len(arguments)))
        try:
            workers = max(1, min(len(arguments), int(workers_text)))
        except ValueError:
            workers = len(arguments)
        if workers > 1:
            try:
                with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                    completed = pool.starmap(check_row, arguments)
            except (AttributeError, OSError, RuntimeError):
                completed = [check_row(*argument) for argument in arguments]
        else:
            completed = [check_row(*argument) for argument in arguments]
        need(len(completed) == 8, "checked row census")
        audit = payload.get("finite_audit", {})
        need(audit.get("rows") == 8 and audit.get("laws") == 3 and
             audit.get("weighted_cases") == 48 and
             audit.get("minimum_cases_below_one") == 24 and
             audit.get("positive_cases_above_one") == 24 and
             audit.get("log_enclosed_cases") == 16 and
             audit.get("positive_order_types") == 4 and
             audit.get("fixed_power_credit") == 0,
             "audit counters")
        firewall = payload.get("claim_firewall", {})
        need(firewall.get("TPC314_EXTERNAL_INDEPENDENCE") ==
             "NONE_SAME_LOCKED_ENGINE" and
             firewall.get("TPC314_CANONICAL_WEIGHTING_THEOREM") == "OPEN" and
             firewall.get("TPC314_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
             firewall.get("TPC314_FULL_GATE_B") == "OPEN" and
             firewall.get("TPC314_TWIN_PRIME_RESULT") == "NONE",
             "claim firewall")
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC314_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC314_INDEPENDENT_CHECK=PASS rows=8 laws=3 cases=48 "
          "minimum_below_one=24 positive_above_one=24 "
          "log_enclosures=16 grid_digits=36")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
