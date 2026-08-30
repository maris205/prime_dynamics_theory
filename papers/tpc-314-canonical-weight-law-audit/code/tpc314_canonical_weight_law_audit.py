#!/usr/bin/env python3
"""TPC-314: externally motivated positive-weight audit on the TPC-312 panel.

The previous release certified a profile-budget interface, but left the
choice of weights open.  This release freezes the TPC-312 physical panel and
audits three deliberately declared positive laws on the same Gram/sign
targets: counting weight 1, reduced-residue weight 1/(p-1), and prime
von-Mangoldt weight log(p).  The first two laws are rational.  The logarithm
is enclosed with a rational atanh series and every subsequent quadratic-form
operation is rounded outward to a 10^-36 decimal grid.

The result is finite and source-first.  It is a robustness audit of a
weighting convention, not an external physical holdout, an arithmetic L2
estimate, a growing theorem, or a twin-prime result.
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

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
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
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

PARENT_STATUS = (
    "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS")
PARENT_SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"
STATUS = (
    "PROVED_EXACT_FINITE_EXTERNALLY_MOTIVATED_WEIGHT_LAW_ENCLOSURE_AND_"
    "NEW_PANEL_ROBUSTNESS_AUDIT")
SCHEMA = "TPC314_EXTERNALLY_MOTIVATED_WEIGHT_LAW_AUDIT_V1"
ROUND2_CLUE = (
    "REPLICATE_THE_LOCKED_WEIGHT_LAW_MENU_ON_A_FRESH_SOURCE_INTERVAL_"
    "WITH_WEIGHTS_FIXED_BEFORE_TARGET_RECOMPUTATION")

SCALE = 640
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
LAWS = ("COUNTING", "REDUCED_RESIDUE", "VON_MANGOLDT")
LOG_TERMS = 120
GRID_DIGITS = 36
GRID = 10 ** GRID_DIGITS

parent_spec = importlib.util.spec_from_file_location(
    "frozen_tpc312_for_tpc314", PARENT_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-312 physical panel unavailable")
PARENT = importlib.util.module_from_spec(parent_spec)
parent_spec.loader.exec_module(PARENT)
ENGINE = PARENT.ENGINE


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


def load_parent() -> dict[tuple[int, int], dict[str, Any]]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "TPC-312 code provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "TPC-312 result provenance")
    document = json.loads(raw)
    need(raw == canonical(document), "TPC-312 canonicality")
    need(document.get("certificate_version") == 1 and
         document.get("claim_status") == PARENT_STATUS,
         "TPC-312 header")
    payload = document["payload"]
    need(payload.get("schema") == PARENT_SCHEMA and
         document.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "TPC-312 payload")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "TPC-268 engine provenance")
    rows = payload.get("rows", [])
    indexed = {(int(row["Q"]), int(row["kernel_exponent"])): row
               for row in rows}
    need(len(indexed) == 8, "TPC-312 row census")
    return indexed


def log_from_atanh(z: Fraction, terms: int = LOG_TERMS) -> DirectedInterval:
    """Enclose 2*atanh(z) using a positive rational remainder bound."""
    need(Fraction(0) <= z < 1, "atanh argument")
    partial = sum((z ** (2 * j + 1)) / (2 * j + 1)
                  for j in range(terms)) * 2
    tail = (2 * z ** (2 * terms + 1) /
            ((2 * terms + 1) * (1 - z * z)))
    return DirectedInterval(partial, partial + tail)


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
        list[int], list[int], list[list[Fraction]]]:
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
    return indices, shell, gram


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


def build_row(parent_row: dict[str, Any]) -> dict[str, Any]:
    q0 = int(parent_row["Q"])
    exponent = int(parent_row["kernel_exponent"])
    indices, shell, gram = exact_row_matrices(q0, exponent)
    need(parent_row["prime_shell"] == shell, "parent shell mismatch")
    minimum = [int(value) for value in parent_row["minimum_label"]]
    plus = [1] * len(shell)
    need(len(minimum) == len(shell), "minimum label length")
    laws: list[dict[str, Any]] = []
    all_cases: dict[str, list[dict[str, Any]]] = {}
    for law in LAWS:
        weights = weight_vector(law, shell)
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
        "source_interval": [321, 640],
        "index_count": len(indices),
        "shell": shell,
        "shell_cardinality": len(shell),
        "gram_trace_rational_sha256": fraction_digest(
            sum((gram[i][i] for i in range(len(shell))), Fraction(0))),
        "inherited_modular_rank": int(parent_row["modular_gram_rank"]),
        "minimum_label": minimum,
        "positive_label": plus,
        "target_label_provenance": (
            "TPC-312 exact physical Gram minimum; all-positive control"),
        "laws": laws,
        "minimum_law_order_ascending": minimum_order,
        "positive_law_order_ascending": positive_order,
    }


def build_payload() -> dict[str, Any]:
    parent_rows = load_parent()
    specifications = [parent_rows[(q0, exponent)]
                      for q0 in Q_ANCHORS for exponent in EXPONENTS]
    workers_text = os.environ.get("TPC314_WORKERS", str(len(specifications)))
    try:
        workers = max(1, min(len(specifications), int(workers_text)))
    except ValueError:
        workers = len(specifications)
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(build_row, specifications)
        except (AttributeError, OSError, RuntimeError):
            rows = [build_row(row) for row in specifications]
    else:
        rows = [build_row(row) for row in specifications]
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
    minimum_exception = ("COUNTING", "VON_MANGOLDT", "REDUCED_RESIDUE")
    need(sum(order == minimum_expected for order in minimum_orders) == 7 and
         sum(order == minimum_exception for order in minimum_orders) == 1,
         "minimum law order census")
    minimum_census = Counter(">".join(order) for order in minimum_orders)
    positive_census = Counter(">".join(order) for order in positive_orders)
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc312_code_sha256": PARENT_CODE_SHA256,
            "tpc312_result_sha256": PARENT_RESULT_SHA256,
            "tpc268_engine_sha256": ENGINE_CODE_SHA256,
            "tpc312_status": PARENT_STATUS,
        },
        "protocol": {
            "physical_engine": "locked TPC-268/TPC-312 literal rational engine",
            "source_interval": [321, 640],
            "source_scale": SCALE,
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "laws": list(LAWS),
            "law_order": "COUNTING, REDUCED_RESIDUE, VON_MANGOLDT",
            "target_rule": "TPC-312 minimum label plus all-positive control",
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
            "scope": "finite TPC-312 source-shell rows and declared laws only",
        },
        "finite_audit": {
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
            "inherited_full_rank_rows": 8,
            "external_physical_holdout": "NONE_SAME_LOCKED_ENGINE",
            "fixed_power_credit": 0,
        },
        "claim_firewall": {
            "TPC314_WEIGHTED_GRAM_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC314_LOG_ATANH_ENCLOSURE": "PROVED_EXACT_FINITE",
            "TPC314_DIRECTED_INTERVAL_PROPAGATION":
                "PROVED_EXACT_FINITE_GRID_1E_MINUS_36",
            "TPC314_MINIMUM_BELOW_ONE":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC314_POSITIVE_ABOVE_ONE":
                "NUMERICALLY_CERTIFIED_FINITE_24_OF_24",
            "TPC314_MINIMUM_LAW_ORDER":
                "NUMERICALLY_CERTIFIED_FINITE_7_OF_8_LOG_LT_COUNT_LT_RECIP_"
                "ONE_COUNT_LT_LOG_CROSSOVER",
            "TPC314_POSITIVE_LAW_ORDER":
                "NUMERICALLY_CERTIFIED_FINITE_8_OF_8_FOUR_ORDER_TYPES",
            "TPC314_EXTERNAL_INDEPENDENCE": "NONE_SAME_LOCKED_ENGINE",
            "TPC314_TARGET_GENERATION_LEAKAGE":
                "INHERITED_TPC312_SOURCE_FIRST_GRAM_LABEL",
            "TPC314_CANONICAL_WEIGHTING_THEOREM": "OPEN",
            "TPC314_FRESH_PHYSICAL_HOLDOUT": "OPEN",
            "TPC314_UNIFORM_GROWING_BUDGET": "OPEN",
            "TPC314_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC314_FIXED_POWER_CREDIT": 0,
            "TPC314_FULL_GATE_B": "OPEN",
            "TPC314_TWIN_PRIME_RESULT": "NONE",
            "TPC314_STATUS": STATUS,
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
    need(audit.get("rows") == 8 and audit.get("laws") == 3 and
         audit.get("weighted_cases") == 48 and
         audit.get("minimum_cases_below_one") == 24 and
         audit.get("positive_cases_above_one") == 24 and
         audit.get("log_enclosed_cases") == 16 and
         audit.get("fixed_power_credit") == 0, "finite audit")
    need(len(payload.get("rows", [])) == 8, "row payload")
    firewall = payload.get("claim_firewall", {})
    need(firewall.get("TPC314_EXTERNAL_INDEPENDENCE") ==
         "NONE_SAME_LOCKED_ENGINE" and
         firewall.get("TPC314_ARITHMETIC_L2") == "OPEN_LITERAL_SOURCE" and
         firewall.get("TPC314_FIXED_POWER_CREDIT") == 0 and
         firewall.get("TPC314_FULL_GATE_B") == "OPEN" and
         firewall.get("TPC314_TWIN_PRIME_RESULT") == "NONE",
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
        print("TPC314_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC314_CERTIFICATE=PASS rows=8 laws=3 cases=48 "
          "minimum_below_one=24 positive_above_one=24 "
          "log_terms=120 grid_digits=36 fixed_power_credit=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
