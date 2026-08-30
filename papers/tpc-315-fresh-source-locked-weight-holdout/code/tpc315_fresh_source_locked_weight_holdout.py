#!/usr/bin/env python3
"""TPC-315: fresh-source holdout under a locked positive-weight menu.

TPC-314 found finite class robustness but also law-dependent amplitude.  This
release freezes its three-law menu before reading any new target labels, moves
the literal physical engine to the fresh source interval I=(640,1280], and
recomputes the Gram minimum and all-positive control from that new panel.
The logarithmic law is enclosed by a rational atanh series and all weighted
quadratic forms are rounded outward to a 10^-36 decimal grid.

The result is a finite holdout replication, not an external physical data
source, a growing theorem, an arithmetic L2 estimate, or a twin-prime result.
"""

from __future__ import annotations

import argparse
import hashlib
import math
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

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc315_certificate.json"
MENU_CODE = ROOT / (
    "papers/tpc-314-canonical-weight-law-audit/code/"
    "tpc314_canonical_weight_law_audit.py")
MENU_RESULT = ROOT / (
    "papers/tpc-314-canonical-weight-law-audit/results/"
    "tpc314_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

MENU_CODE_SHA256 = (
    "ef1e27bd81691f04109af63455a2f187079c4a721787b93f7fc49e985608a2a0")
MENU_RESULT_SHA256 = (
    "d0b09fe5c3c33eae949b2b67a93302bdc5b557cdda7094df58027c39a6a8389b")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

MENU_STATUS = (
    "PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_"
    "NEW_PANEL_ROBUSTNESS_AUDIT")
MENU_SCHEMA = "TPC314_EXTERNALLY_MOTIVATED_WEIGHT_LAW_AUDIT_V1"
STATUS = (
    "PROVED_EXACT_FINITE_FRESH_SOURCE_LOCKED_WEIGHT_MENU_HOLDOUT_"
    "REPLICATION_AND_LAW_ORDER_SHIFT")
SCHEMA = "TPC315_FRESH_SOURCE_LOCKED_WEIGHT_HOLDOUT_V1"
ROUND2_CLUE = (
    "PROBE_LITERAL_ARITHMETIC_L2_INTERFACE_ON_THE_FRESH_PANEL_BEFORE_"
    "ANY_GROWING_CLAIM")

SCALE = 1280
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("COUNTING", "REDUCED_RESIDUE", "VON_MANGOLDT")
LOG_TERMS = 120
GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS
MODULUS = 1_000_000_007

engine_spec = importlib.util.spec_from_file_location(
    "locked_tpc268_for_tpc315", ENGINE_CODE)
if engine_spec is None or engine_spec.loader is None:
    raise RuntimeError("TPC-268 arithmetic engine unavailable")
ENGINE = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


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
    """Render an endpoint whose denominator divides the declared grid."""
    scaled = value * GRID
    need(scaled.denominator == 1, "non-grid interval endpoint")
    number = scaled.numerator
    sign = "-" if number < 0 else ""
    number = abs(number)
    whole, remainder = divmod(number, GRID)
    if remainder == 0:
        return sign + str(whole)
    tail = f"{remainder:0{GRID_DIGITS}d}".rstrip("0")
    return sign + str(whole) + "." + tail


class DirectedInterval:
    """Closed interval with floor/ceiling rounding after every operation."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction | int,
                 hi: Fraction | int | None = None) -> None:
        raw_lo = Fraction(lo)
        raw_hi = raw_lo if hi is None else Fraction(hi)
        need(raw_lo <= raw_hi, "reversed raw interval")
        self.lo = grid_floor(raw_lo)
        self.hi = grid_ceil(raw_hi)
        need(self.lo <= self.hi, "reversed rounded interval")

    def __add__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        right = as_interval(other)
        return DirectedInterval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> DirectedInterval:
        return DirectedInterval(-self.hi, -self.lo)

    def __sub__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        return self + (-as_interval(other))

    def __rsub__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        return as_interval(other) - self

    def __mul__(self, other: DirectedInterval | Fraction | int
                ) -> DirectedInterval:
        right = as_interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return DirectedInterval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: DirectedInterval | Fraction | int
                    ) -> DirectedInterval:
        right = as_interval(other)
        need(right.lo > 0 or right.hi < 0,
             "interval denominator crosses zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return DirectedInterval(min(values), max(values))


def as_interval(value: DirectedInterval | Fraction | int) -> DirectedInterval:
    return value if isinstance(value, DirectedInterval) else DirectedInterval(value)


def interval_text(value: DirectedInterval) -> list[str]:
    return [fixed_decimal(value.lo), fixed_decimal(value.hi)]


def interval_digest(value: DirectedInterval) -> str:
    return hashlib.sha256(
        f"{value.lo.numerator}/{value.lo.denominator}|"
        f"{value.hi.numerator}/{value.hi.denominator}\n".encode("ascii")
    ).hexdigest()


def load_locked_menu() -> dict[str, Any]:
    """Verify TPC-314's frozen laws before any fresh target is read."""
    need(digest(MENU_CODE.read_bytes()) == MENU_CODE_SHA256,
         "TPC-314 menu-code provenance")
    raw = MENU_RESULT.read_bytes()
    need(digest(raw) == MENU_RESULT_SHA256,
         "TPC-314 menu-certificate provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC-314 menu canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == MENU_STATUS,
         "TPC-314 menu header")
    payload = document["payload"]
    need(payload.get("schema") == MENU_SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "TPC-314 menu payload")
    protocol = payload.get("protocol", {})
    need(protocol.get("laws") == list(LAWS) and
         protocol.get("log_terms") == LOG_TERMS and
         protocol.get("grid_digits") == GRID_DIGITS and
         protocol.get("weights_locked_before_target_readout") is True,
         "TPC-314 frozen menu")
    return payload


def log_from_atanh(z: Fraction, terms: int = LOG_TERMS) -> DirectedInterval:
    """Enclose 2*atanh(z) using a positive rational remainder bound."""
    need(Fraction(0) <= z < 1, "atanh argument")
    partial = sum((z ** (2 * j + 1)) / (2 * j + 1)
                  for j in range(terms)) * 2
    tail = (2 * z ** (2 * terms + 1) /
            ((2 * terms + 1) * (1 - z * z)))
    return DirectedInterval(partial, partial + tail)


def fraction_mod(value: Fraction) -> int:
    denominator = value.denominator % MODULUS
    need(denominator != 0, "non-invertible modular denominator")
    return value.numerator % MODULUS * pow(
        denominator, MODULUS - 2, MODULUS) % MODULUS


def rank_mod(matrix: list[list[int]]) -> int:
    """Gaussian rank over the declared prime field."""
    if not matrix:
        return 0
    rows = len(matrix)
    columns = len(matrix[0])
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, rows)
                      if matrix[i][column] % MODULUS), None)
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_row = matrix[rank]
        inverse = pow(pivot_row[column] % MODULUS, MODULUS - 2, MODULUS)
        for j in range(column, columns):
            pivot_row[j] = pivot_row[j] * inverse % MODULUS
        for i in range(rank + 1, rows):
            factor = matrix[i][column] % MODULUS
            if not factor:
                continue
            row = matrix[i]
            for j in range(column, columns):
                row[j] = (row[j] - factor * pivot_row[j]) % MODULUS
        rank += 1
        if rank == rows:
            break
    return rank


def gram_matrix(outputs: list[list[Fraction]]) -> list[list[int]]:
    vectors = [[fraction_mod(value) for value in output]
               for output in outputs]
    return [[sum(vectors[i][k] * vectors[j][k]
                 for k in range(len(vectors[i]))) % MODULUS
             for j in range(len(vectors))]
            for i in range(len(vectors))]


def exhaustive_signed_extrema(matrix: list[list[Fraction]]) -> dict[str, Any]:
    """Enumerate all sign classes after fixing the first sign to +1."""
    denominator = 1
    for row in matrix:
        for value in row:
            denominator = math.lcm(denominator, value.denominator)
    scaled = [[value.numerator * (denominator // value.denominator)
               for value in row] for row in matrix]
    size = len(scaled)
    need(size > 0 and all(len(row) == size for row in scaled),
         "square Gram matrix")
    labels = [1] * size
    fields = [sum(scaled[i][j] for j in range(size) if j != i)
              for i in range(size)]
    value = sum(scaled[i][j] for i in range(size) for j in range(size))
    minimum = maximum = value
    minimum_label = maximum_label = tuple(labels)
    minimum_count = maximum_count = 1
    previous_gray = 0
    for code in range(1, 1 << (size - 1)):
        gray = code ^ (code >> 1)
        changed = gray ^ previous_gray
        vertex = changed.bit_length()
        old = labels[vertex]
        value -= 4 * old * fields[vertex]
        labels[vertex] = -old
        for other in range(size):
            if other != vertex:
                fields[other] -= 2 * old * scaled[other][vertex]
        previous_gray = gray
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
    need(trace > 0, "positive Gram trace")
    return {
        "common_denominator": denominator,
        "trace_integer": trace,
        "minimum_integer": minimum,
        "maximum_integer": maximum,
        "minimum_label": minimum_label,
        "maximum_label": maximum_label,
        "minimum_count": minimum_count,
        "maximum_count": maximum_count,
        "enumerated_labelings": 1 << (size - 1),
    }


def ratio(extrema: dict[str, Any], which: str) -> Fraction:
    return Fraction(extrema[which + "_integer"], extrema["trace_integer"])


LOG2_INTERVAL = log_from_atanh(Fraction(1, 3))
LOG_CACHE: dict[int, DirectedInterval] = {}


def log_prime_interval(prime: int) -> DirectedInterval:
    """Return a rational outward enclosure of log(prime)."""
    if prime not in LOG_CACHE:
        power = 2 ** (prime.bit_length() - 1)
        y = Fraction(prime, power)
        z = (y - 1) / (y + 1)
        LOG_CACHE[prime] = (DirectedInterval(prime.bit_length() - 1) *
                            LOG2_INTERVAL + log_from_atanh(z))
    return LOG_CACHE[prime]


def weight_vector(law: str, shell: list[int]
                  ) -> list[Fraction] | list[DirectedInterval]:
    need(law in LAWS, "unknown weighting law")
    if law == "COUNTING":
        return [Fraction(1) for _ in shell]
    if law == "REDUCED_RESIDUE":
        return [Fraction(1, prime - 1) for prime in shell]
    return [log_prime_interval(prime) for prime in shell]


def weight_definition(law: str) -> str:
    return {
        "COUNTING": "w_p=1",
        "REDUCED_RESIDUE": "w_p=1/(p-1)=1/phi(p)",
        "VON_MANGOLDT": "w_p=log(p)=Lambda(p) on prime support",
    }[law]


def weights_digest(weights: list[Fraction] | list[DirectedInterval]) -> str:
    pieces: list[str] = []
    for value in weights:
        interval = as_interval(value)
        pieces.append(
            f"{interval.lo.numerator}/{interval.lo.denominator}|"
            f"{interval.hi.numerator}/{interval.hi.denominator}\n")
    return hashlib.sha256("".join(pieces).encode("ascii")).hexdigest()


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


def exact_row_matrices(q0: int, exponent: int) -> tuple[
        list[int], list[int], list[list[Fraction]], int]:
    indices = list(range(SCALE // 2 + 1, SCALE + 1))
    beta = [ENGINE.beta_value(value, SCALE) for value in indices]
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [physical_prime_output(indices, beta, prime, exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    need(all(gram[i][i] > 0 for i in range(len(shell))),
         "positive Gram diagonal")
    modular_rank = rank_mod(gram_matrix(outputs))
    return indices, shell, gram, modular_rank


def exact_weighted_ratio(gram: list[list[Fraction]], labels: list[int],
                         weights: list[Fraction]) -> Fraction:
    numerator = sum((Fraction(labels[i] * labels[j]) * weights[i] *
                     gram[i][j] * weights[j]
                     for i in range(len(labels))
                     for j in range(len(labels))), Fraction(0))
    denominator = sum((weights[i] * gram[i][i] * weights[i]
                       for i in range(len(labels))), Fraction(0))
    need(denominator > 0, "nonpositive weighted diagonal")
    return numerator / denominator


def interval_weighted_ratio(gram: list[list[Fraction]], labels: list[int],
                            weights: list[Fraction] | list[DirectedInterval]
                            ) -> tuple[DirectedInterval, DirectedInterval,
                                       DirectedInterval]:
    numerator = DirectedInterval(0)
    denominator = DirectedInterval(0)
    for i in range(len(labels)):
        wi = as_interval(weights[i])
        denominator += wi * gram[i][i] * wi
        for j in range(len(labels)):
            wj = as_interval(weights[j])
            numerator += wi * gram[i][j] * wj * (labels[i] * labels[j])
    need(denominator.lo > 0, "weighted interval denominator")
    return numerator / denominator, numerator, denominator


def case_record(gram: list[list[Fraction]], shell: list[int], law: str,
                target_name: str, labels: list[int],
                weights: list[Fraction] | list[DirectedInterval]
                ) -> dict[str, Any]:
    ratio_i, numerator_i, denominator_i = interval_weighted_ratio(
        gram, labels, weights)
    exact_hash: str | None = None
    if law != "VON_MANGOLDT":
        exact = exact_weighted_ratio(
            gram, labels, [Fraction(value) for value in weights])
        need(ratio_i.lo <= exact <= ratio_i.hi,
             "exact ratio outside directed interval")
        exact_hash = fraction_digest(exact)
        display = decimal(exact)
    else:
        display = decimal(Fraction(ratio_i.lo + ratio_i.hi, 2))
    below = ratio_i.hi < 1
    above = ratio_i.lo > 1
    need(below != above, "ratio must lie on one side of one")
    return {
        "target": target_name,
        "label_vector": labels,
        "shell": shell,
        "numerator_interval": interval_text(numerator_i),
        "denominator_interval": interval_text(denominator_i),
        "ratio_interval": interval_text(ratio_i),
        "ratio_interval_sha256": interval_digest(ratio_i),
        "ratio_display_decimal": display,
        "exact_ratio_sha256": exact_hash,
        "strict_below_one": below,
        "strict_above_one": above,
        "classification": "BELOW_ONE" if below else "ABOVE_ONE",
    }


def order_laws(cases: list[dict[str, Any]]) -> list[str]:
    indexed = {case["law"]: case for case in cases}
    need(set(indexed) == set(LAWS), "law order census")
    # Every adjacent pair must be disjoint, so the order is an interval fact.
    ordered = sorted(
        LAWS, key=lambda law: Fraction(indexed[law]["ratio_interval"][0]))
    for left, right in zip(ordered, ordered[1:]):
        need(Fraction(indexed[left]["ratio_interval"][1]) <
             Fraction(indexed[right]["ratio_interval"][0]),
             "law order intervals overlap")
    return ordered


def build_row(specification: tuple[int, int]) -> dict[str, Any]:
    q0, exponent = specification
    declared_shell = [prime for prime in ENGINE.PRIMES
                      if q0 < prime <= 2 * q0]
    # The complete law menu is materialized before the fresh Gram target is
    # computed.  This prevents post-target law selection within this audit.
    frozen_weights = {law: weight_vector(law, declared_shell) for law in LAWS}
    indices, shell, gram, modular_rank = exact_row_matrices(q0, exponent)
    need(shell == declared_shell, "declared shell changed during target readout")
    extrema = exhaustive_signed_extrema(gram)
    minimum = list(extrema["minimum_label"])
    plus = list(extrema["maximum_label"])
    need(plus == [1] * len(shell), "all-positive vector is not the maximum")
    need(extrema["minimum_count"] == 1 and extrema["maximum_count"] == 1,
         "nonunique fresh extrema modulo global sign")
    trace = Fraction(extrema["trace_integer"], extrema["common_denominator"])
    minimum_ratio = ratio(extrema, "minimum")
    maximum_ratio = ratio(extrema, "maximum")
    need(minimum_ratio < 1 < maximum_ratio, "unweighted fresh separation")
    laws: list[dict[str, Any]] = []
    all_cases: dict[str, list[dict[str, Any]]] = {}
    for law in LAWS:
        weights = frozen_weights[law]
        cases = [case_record(gram, shell, law, "minimum", minimum, weights),
                 case_record(gram, shell, law, "plus", plus, weights)]
        for case in cases:
            case["law"] = law
        all_cases[law] = cases
        saved_weights: list[Any] = []
        for value in weights:
            interval = as_interval(value)
            saved_weights.append(interval_text(interval))
        laws.append({
            "law": law,
            "definition": weight_definition(law),
            "weight_vector_intervals": saved_weights,
            "weight_vector_sha256": weights_digest(weights),
            "log_enclosure_terms": LOG_TERMS if law == "VON_MANGOLDT" else None,
            "cases": cases,
        })

    minimum_cases = [all_cases[law][0] for law in LAWS]
    positive_cases = [all_cases[law][1] for law in LAWS]
    minimum_order = order_laws(minimum_cases)
    positive_order = order_laws(positive_cases)
    need(all(case["strict_below_one"] for case in minimum_cases),
         "minimum separation")
    need(all(case["strict_above_one"] for case in positive_cases),
         "positive separation")
    return {
        "Q": q0,
        "kernel_exponent": exponent,
        "source_interval": [SCALE // 2 + 1, SCALE],
        "index_count": len(indices),
        "shell": shell,
        "shell_cardinality": len(shell),
        "modular_rank_prime": MODULUS,
        "modular_gram_rank": modular_rank,
        "enumerated_labelings_mod_global_sign":
            extrema["enumerated_labelings"],
        "minimum_count_mod_global_sign": extrema["minimum_count"],
        "maximum_count_mod_global_sign": extrema["maximum_count"],
        "gram_trace_rational_sha256": fraction_digest(trace),
        "minimum_ratio_decimal": decimal(minimum_ratio),
        "maximum_ratio_decimal": decimal(maximum_ratio),
        "minimum_ratio_rational_sha256": fraction_digest(minimum_ratio),
        "maximum_ratio_rational_sha256": fraction_digest(maximum_ratio),
        "minimum_below_one": True,
        "positive_maximum_above_one": True,
        "minimum_label": minimum,
        "positive_label": plus,
        "target_label_provenance": (
            "fresh exact physical Gram minimum recomputed after locking the "
            "menu; fresh all-positive exact Gram maximum control"),
        "weights_locked_before_target_recomputation": True,
        "laws": laws,
        "minimum_law_order_ascending": minimum_order,
        "positive_law_order_ascending": positive_order,
    }


def build_payload() -> dict[str, Any]:
    # Verify and lock the TPC-314 menu before any fresh physical target work.
    load_locked_menu()
    specifications = [(q0, exponent)
                      for q0 in Q_ANCHORS for exponent in EXPONENTS]
    workers_text = os.environ.get("TPC315_WORKERS", str(len(specifications)))
    try:
        workers = max(1, min(len(specifications), int(workers_text)))
    except ValueError:
        workers = len(specifications)
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(build_row, specifications)
        except (AttributeError, OSError, RuntimeError):
            rows = [build_row(specification)
                    for specification in specifications]
    else:
        rows = [build_row(specification) for specification in specifications]
    need(len(rows) == 8, "row census")
    cases = [case for row in rows for law in row["laws"]
             for case in law["cases"]]
    minimum = [case for case in cases if case["target"] == "minimum"]
    positive = [case for case in cases if case["target"] == "plus"]
    need(len(cases) == 48 and len(minimum) == 24 and len(positive) == 24,
         "case census")
    need(all(case["strict_below_one"] for case in minimum),
         "minimum census")
    need(all(case["strict_above_one"] for case in positive),
         "positive census")
    minimum_orders = [tuple(row["minimum_law_order_ascending"]) for row in rows]
    positive_orders = [tuple(row["positive_law_order_ascending"]) for row in rows]
    minimum_expected = ("VON_MANGOLDT", "COUNTING", "REDUCED_RESIDUE")
    minimum_exception_a = ("REDUCED_RESIDUE", "COUNTING", "VON_MANGOLDT")
    minimum_exception_b = ("COUNTING", "VON_MANGOLDT", "REDUCED_RESIDUE")
    positive_expected = ("REDUCED_RESIDUE", "COUNTING", "VON_MANGOLDT")
    positive_exception = ("VON_MANGOLDT", "REDUCED_RESIDUE", "COUNTING")
    need(sum(order == minimum_expected for order in minimum_orders) == 6 and
         sum(order == minimum_exception_a for order in minimum_orders) == 1 and
         sum(order == minimum_exception_b for order in minimum_orders) == 1,
         "minimum law order census")
    need(sum(order == positive_expected for order in positive_orders) == 6 and
         sum(order == positive_exception for order in positive_orders) == 2,
         "positive law order census")
    minimum_census = Counter("<".join(order) for order in minimum_orders)
    positive_census = Counter("<".join(order) for order in positive_orders)
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc314_menu_code_sha256": MENU_CODE_SHA256,
            "tpc314_menu_result_sha256": MENU_RESULT_SHA256,
            "tpc268_engine_sha256": ENGINE_CODE_SHA256,
            "tpc314_menu_status": MENU_STATUS,
        },
        "protocol": {
            "physical_engine": "locked TPC-268 literal rational engine",
            "source_interval": [SCALE // 2 + 1, SCALE],
            "source_scale": SCALE,
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS),
            "law_order": "COUNTING, REDUCED_RESIDUE, VON_MANGOLDT",
            "target_rule": (
                "fresh exact Gram minimum plus fresh all-positive maximum control"),
            "target_generation_order": (
                "lock laws and weights before recomputing fresh physical Gram labels"),
            "normalizer": "weighted diagonal D_w=sum_p w_p^2 G_pp",
            "log_range_reduction": (
                "p=2^k y, 1<=y<2, z=(y-1)/(y+1), log(y)=2 atanh(z)"),
            "log_tail_bound": (
                "2 z^(2N+1)/((2N+1)(1-z^2)) after N positive terms"),
            "log_terms": LOG_TERMS,
            "grid_digits": GRID_DIGITS,
            "grid": str(GRID),
            "weights_locked_before_target_readout": True,
        },
        "exact_theorem": {
            "weighted_gram_identity": (
                "E_w(c)=sum_{p,q} c_p c_q w_p G_(p,q) w_q"),
            "weighted_diagonal_normalizer": (
                "D_w=sum_p w_p^2 G_(p,p)>0 for nonzero positive weights"),
            "scale_invariance": "R_(a w)(c)=R_w(c) for a>0",
            "log_enclosure": (
                "the atanh partial sum is below log(y), and the stated "
                "positive tail bound is above the remainder"),
            "directed_interval_soundness": (
                "floor lower endpoints and ceiling upper endpoints preserve "
                "containment under rational +,-,*,/ operations"),
            "scope": (
                "finite fresh source interval I=(640,1280], eight source-shell "
                "rows, and the predeclared TPC-314 menu only"),
        },
        "finite_audit": {
            "fresh_source_rows": 8,
            "recomputed_target_rows": 8,
            "rows": 8,
            "laws": 3,
            "targets_per_law": 16,
            "weighted_cases": 48,
            "minimum_cases_below_one": 24,
            "positive_cases_above_one": 24,
            "log_enclosed_cases": 16,
            "minimum_order_rows": 8,
            "minimum_order_census": {
                key: minimum_census[key]
                for key in sorted(minimum_census)
            },
            "minimum_order_types": len(minimum_census),
            "positive_order_census": {
                key: positive_census[key]
                for key in sorted(positive_census)
            },
            "positive_order_types": len(positive_census),
            "fresh_replication_rows": 8,
            "fresh_full_rank_rows": sum(
                row["modular_gram_rank"] == row["shell_cardinality"]
                for row in rows),
            "tpc314_parent_minimum_order_types": 2,
            "tpc314_parent_positive_order_types": 4,
            "external_physical_holdout": "NONE_SAME_LOCKED_ENGINE",
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC315_FRESH_SOURCE_TARGET_RECOMPUTATION":
                "PROVED_EXACT_FINITE_8_ROWS",
            "TPC315_LOCKED_WEIGHT_MENU":
                "PROVED_EXACT_FINITE_PRE_TARGET",
            "TPC315_LOG_ATANH_ENCLOSURE":
                "PROVED_EXACT_FINITE_120_TERMS",
            "TPC315_DIRECTED_INTERVAL_PROPAGATION":
                "PROVED_EXACT_FINITE_GRID_1E_MINUS_36",
            "TPC315_MINIMUM_BELOW_ONE":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC315_POSITIVE_ABOVE_ONE":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC315_HOLDOUT_REPLICATION":
                "NUMERICALLY_CERTIFIED_FINITE_8_OF_8",
            "TPC315_MINIMUM_LAW_ORDER_SHIFT":
                "NUMERICALLY_CERTIFIED_FINITE_3_TYPES",
            "TPC315_POSITIVE_LAW_ORDER_SHIFT":
                "NUMERICALLY_CERTIFIED_FINITE_2_TYPES",
            "TPC315_EXTERNAL_INDEPENDENCE": "NONE_SAME_LOCKED_ENGINE",
            "TPC315_TARGET_GENERATION_LEAKAGE":
                "FRESH_SOURCE_GRAM_DEPENDENT_LABELS",
            "TPC315_CANONICAL_WEIGHTING": "OPEN",
            "TPC315_FRESH_PHYSICAL_HOLDOUT": "NONE_SAME_LOCKED_ENGINE",
            "TPC315_UNIFORM_GROWING_WEIGHTED_THEOREM": "OPEN",
            "TPC315_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC315_FIXED_POWER_CREDIT": 0,
            "TPC315_FULL_GATE_B": "OPEN",
            "TPC315_TWIN_PRIME_RESULT": "NONE",
            "TPC315_STATUS": STATUS,
        },
        "rows": rows,
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def check_document(data: dict[str, Any]) -> None:
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA and
         data.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload")
    audit = payload.get("finite_audit", {})
    need(audit.get("fresh_source_rows") == 8 and
         audit.get("recomputed_target_rows") == 8 and
         audit.get("rows") == 8 and audit.get("laws") == 3 and
         audit.get("weighted_cases") == 48 and
         audit.get("minimum_cases_below_one") == 24 and
         audit.get("positive_cases_above_one") == 24 and
         audit.get("log_enclosed_cases") == 16 and
         audit.get("minimum_order_types") == 3 and
         audit.get("positive_order_types") == 2 and
         audit.get("fresh_replication_rows") == 8 and
         audit.get("fresh_full_rank_rows") == 8 and
         audit.get("fixed_power_credit") == 0, "finite audit")
    protocol = payload.get("protocol", {})
    need(protocol.get("source_interval") == [641, 1280] and
         protocol.get("source_scale") == 1280 and
         protocol.get("laws") == list(LAWS) and
         protocol.get("weights_locked_before_target_readout") is True,
         "fresh protocol")
    rows = payload.get("rows", [])
    need(len(rows) == 8 and
         all(row.get("source_interval") == [641, 1280] and
             row.get("weights_locked_before_target_recomputation") is True and
             row.get("minimum_below_one") is True and
             row.get("positive_maximum_above_one") is True
             for row in rows), "row payload")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC315_HOLDOUT_REPLICATION") ==
         "NUMERICALLY_CERTIFIED_FINITE_8_OF_8" and
         firewall.get("TPC315_EXTERNAL_INDEPENDENCE") ==
         "NONE_SAME_LOCKED_ENGINE" and
         firewall.get("TPC315_CANONICAL_WEIGHTING") == "OPEN" and
         firewall.get("TPC315_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC315_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC315_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC315_TWIN_PRIME_RESULT") == "NONE" and
         firewall.get("TPC315_STATUS") == STATUS,
         "claim firewall")


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        built = document()
        check_document(built)
        raw = canonical(built)
        if args.write:
            RESULT.parent.mkdir(parents=True, exist_ok=True)
            RESULT.write_bytes(raw)
        else:
            need(RESULT.is_file(), "missing certificate")
            need(RESULT.read_bytes() == raw, "certificate is not reproducible")
    except (CheckFailure, OSError, ValueError, KeyError,
            json.JSONDecodeError) as error:
        print("TPC315_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC315_CERTIFICATE=PASS rows=8 laws=3 cases=48 "
          "minimum_below_one=24 positive_above_one=24 "
          "fresh_target_rows=8 log_terms=120 grid_digits=36 "
          "fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
