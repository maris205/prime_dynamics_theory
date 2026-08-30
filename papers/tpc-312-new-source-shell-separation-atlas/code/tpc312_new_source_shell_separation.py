#!/usr/bin/env python3
"""TPC-312: exact new-source-shell Gram and sign-separation atlas.

TPC-311 ended with a request for physical rows that were not recycled from
the TPC-309 parent atlas.  This release constructs eight new rows from the
literal TPC-268/TPC-288 physical engine on I=(320,640], H=66, prime-shell
anchors Q in {24,36,54,80}, and kernel exponents 1 and 2.  Every Gram entry
and every sign energy is rational.  The finite sign extrema are obtained by
an exhaustive Gray traversal modulo the global sign symmetry.

"New" here means new source indices and parameter rows inside the same locked
physical engine.  It does not mean an external data source, an independent
arithmetic sample, an asymptotic theorem, or a twin-prime result.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import multiprocessing as mp_pool
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc312_certificate.json"

TPC311_CODE = ROOT / (
    "papers/tpc-311-stratified-tau-holdout-replication/code/"
    "tpc311_stratified_tau_holdout_replication.py")
TPC311_RESULT = ROOT / (
    "papers/tpc-311-stratified-tau-holdout-replication/results/"
    "tpc311_certificate.json")
TPC288_CODE = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/code/"
    "tpc288_growing_shell_gram_certificate.py")
TPC288_RESULT = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/results/"
    "tpc288_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

TPC311_CODE_SHA256 = (
    "9d10375def6b3b136c16fabbce806a854699c4b5d494a77aab07fab20aa7ece2")
TPC311_RESULT_SHA256 = (
    "0e7ac4ef8d7f62d152ce364a46e5c6f09cabd8e38af3448f65b7249bdda95acd")
TPC288_CODE_SHA256 = (
    "ee88cef250dc37d14b5fa5bbc22cc9cd5d0a44da6a4e4412118895b27e214987")
TPC288_RESULT_SHA256 = (
    "39ab30b6701015bfaf85ebb670706182ecd7b52120e9963d58d0731a0a8e947d")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

TPC311_STATUS = (
    "PROVED_EXACT_FINITE_STRATIFIED_HOLDOUT_PROTOCOL_PLUS_"
    "NUMERICALLY_REPRODUCED_TAU_SLICE_NONREPLICATION_ATLAS")
TPC288_STATUS = (
    "PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION")
STATUS = (
    "PROVED_EXACT_FINITE_NEW_SOURCE_SHELL_GRAM_AND_SIGN_SEPARATION_ATLAS")
SCHEMA = "TPC312_NEW_SOURCE_SHELL_SIGN_SEPARATION_V1"
ROUND2_CLUE = (
    "CERTIFY_NEW_PANEL_PROFILE_BUDGETS_WITH_OUTWARD_ROUNDING_BEFORE_"
    "ANY_HOLDOUT_PREFERENCE_CLAIM")

SOURCE_SCALE = 640
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
MODULUS = 1_000_000_007

spec = importlib.util.spec_from_file_location("frozen_tpc288_for_tpc312",
                                               TPC288_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("TPC-288 physical engine unavailable")
PARENT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PARENT)
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


def rational_digest(value: Fraction) -> str:
    return hashlib.sha256(str(value).encode("ascii")).hexdigest()


def decimal(value: Fraction, digits: int = 24) -> str:
    return ENGINE.decimal_text(value, digits=digits)


def load_canonical(path: Path, expected_hash: str,
                   expected_status: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, path.name + " provenance")
    data = json.loads(raw)
    need(raw == canonical(data), path.name + " canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == expected_status,
         path.name + " header")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), path.name + " payload hash")
    return data


def parent_lock() -> dict[str, Any]:
    need(digest(TPC311_CODE.read_bytes()) == TPC311_CODE_SHA256,
         "TPC-311 code provenance")
    tpc311 = load_canonical(TPC311_RESULT, TPC311_RESULT_SHA256,
                            TPC311_STATUS)
    need(tpc311["payload"].get("schema") ==
         "TPC311_STRATIFIED_TAU_SLICE_HOLDOUT_REPLICATION_V1",
         "TPC-311 schema")
    need(tpc311["payload"].get("round2_clue") ==
         "REQUIRE_FRESH_SOURCE_HOLDOUT_AND_EXTERNALLY_JUSTIFIED_WEIGHT_"
         "LAW_BEFORE_ANY_GLOBAL_PREFERENCE_CLAIM", "TPC-311 route clue")

    need(digest(TPC288_CODE.read_bytes()) == TPC288_CODE_SHA256,
         "TPC-288 code provenance")
    tpc288 = load_canonical(TPC288_RESULT, TPC288_RESULT_SHA256,
                            TPC288_STATUS)
    need(tpc288["payload"].get("schema") ==
         "TPC288_GROWING_SHELL_GRAM_OBSTRUCTION_CERTIFICATE_V1",
         "TPC-288 schema")
    need(tpc288["payload"]["finite_audit"].get("rows") == 34,
         "TPC-288 census")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "TPC-268 engine provenance")
    return {
        "tpc311_code_sha256": TPC311_CODE_SHA256,
        "tpc311_result_sha256": TPC311_RESULT_SHA256,
        "tpc288_code_sha256": TPC288_CODE_SHA256,
        "tpc288_result_sha256": TPC288_RESULT_SHA256,
        "tpc268_engine_sha256": ENGINE_CODE_SHA256,
        "tpc311_parent_observations": 162,
        "tpc288_parent_rows": 34,
    }


def integer_matrix(matrix: list[list[Fraction]]) -> tuple[list[list[int]], int]:
    denominator = 1
    for row in matrix:
        for value in row:
            denominator = math.lcm(denominator, value.denominator)
    scaled = [[value.numerator * (denominator // value.denominator)
               for value in row] for row in matrix]
    return scaled, denominator


def exhaustive_signed_extrema(matrix: list[list[Fraction]]) -> dict[str, Any]:
    """Enumerate all sign classes after fixing the first sign to +1."""
    scaled, denominator = integer_matrix(matrix)
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


def divisor_cutoff(scale: int) -> int:
    return max(k for k in range(scale + 1)
               if (k + 1) ** 400 <= scale ** 133)


def build_row(specification: tuple[int, int]) -> tuple[dict[str, Any],
                                                       Fraction, Fraction]:
    q0, exponent = specification
    indices = list(range(SOURCE_SCALE // 2 + 1, SOURCE_SCALE + 1))
    beta = [ENGINE.beta_value(value, SOURCE_SCALE) for value in indices]
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    need(len(shell) >= 3, "prime shell too small")
    outputs = [PARENT.physical_prime_output(indices, beta, HEIGHT, prime,
                                             exponent)
               for prime in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    need(all(gram[i][j] == gram[j][i]
             for i in range(len(shell)) for j in range(len(shell))),
         "Gram symmetry")
    need(all(gram[i][i] > 0 for i in range(len(shell))),
         "positive Gram diagonal")
    modular_rank = PARENT.rank_mod(PARENT.gram_matrix(outputs))
    need(modular_rank == len(shell), "modular full rank")

    extrema = exhaustive_signed_extrema(gram)
    minimum_ratio = ratio(extrema, "minimum")
    maximum_ratio = ratio(extrema, "maximum")
    positive = (1,) * len(shell)
    need(extrema["maximum_label"] == positive and
         extrema["maximum_count"] == 1, "positive target is unique maximum")
    need(extrema["minimum_count"] == 1, "unique minimum modulo global sign")
    need(0 < minimum_ratio < 1 < maximum_ratio,
         "strict sign separation")

    saved = {
        "scale": SOURCE_SCALE,
        "H": HEIGHT,
        "Q": q0,
        "kernel_exponent": exponent,
        "index_interval": [SOURCE_SCALE // 2 + 1, SOURCE_SCALE],
        "index_count": len(indices),
        "divisor_cutoff_U": divisor_cutoff(SOURCE_SCALE),
        "prime_shell": shell,
        "shell_cardinality": len(shell),
        "modular_rank_prime": MODULUS,
        "modular_gram_rank": modular_rank,
        "enumerated_labelings_mod_global_sign":
            extrema["enumerated_labelings"],
        "minimum_label": list(extrema["minimum_label"]),
        "maximum_label": list(extrema["maximum_label"]),
        "minimum_count_mod_global_sign": extrema["minimum_count"],
        "maximum_count_mod_global_sign": extrema["maximum_count"],
        "minimum_ratio_decimal": decimal(minimum_ratio),
        "maximum_ratio_decimal": decimal(maximum_ratio),
        "minimum_ratio_rational_sha256": rational_digest(minimum_ratio),
        "maximum_ratio_rational_sha256": rational_digest(maximum_ratio),
        "gram_trace_rational_sha256": rational_digest(
            Fraction(extrema["trace_integer"],
                     extrema["common_denominator"])),
        "common_denominator_bits":
            extrema["common_denominator"].bit_length(),
        "minimum_below_one": minimum_ratio < 1,
        "positive_maximum_above_one": maximum_ratio > 1,
        "target_label_provenance": (
            "exact literal physical Gram; exhaustive equal-sign enumeration "
            "with the first shell sign fixed to +1"),
    }
    return saved, minimum_ratio, maximum_ratio


def build_rows() -> list[tuple[dict[str, Any], Fraction, Fraction]]:
    specs = tuple((q0, exponent) for q0 in Q_ANCHORS
                  for exponent in EXPONENTS)
    requested = os.environ.get("TPC312_WORKERS", "8")
    try:
        workers = max(1, min(len(specs), int(requested)))
    except ValueError:
        workers = 8
    if workers == 1:
        return [build_row(item) for item in specs]
    try:
        with mp_pool.get_context("fork").Pool(processes=workers) as pool:
            return pool.map(build_row, specs)
    except (AttributeError, OSError, RuntimeError):
        return [build_row(item) for item in specs]


def build_payload() -> dict[str, Any]:
    built = build_rows()
    rows = [item[0] for item in built]
    minima = {(row["Q"], row["kernel_exponent"]): item[1]
              for row, item in zip(rows, built)}
    maxima = {(row["Q"], row["kernel_exponent"]): item[2]
              for row, item in zip(rows, built)}
    need(len(rows) == 8 and len(minima) == 8 and len(maxima) == 8,
         "row census")

    for exponent in EXPONENTS:
        need(all(minima[(Q_ANCHORS[i], exponent)] >
                 minima[(Q_ANCHORS[i + 1], exponent)]
                 for i in range(len(Q_ANCHORS) - 1)),
             "minimum-ratio Q descent")
        need(all(maxima[(Q_ANCHORS[i], exponent)] <
                 maxima[(Q_ANCHORS[i + 1], exponent)]
                 for i in range(len(Q_ANCHORS) - 1)),
             "positive-ratio Q ascent")
    need(all(minima[(q0, 2)] < minima[(q0, 1)] for q0 in Q_ANCHORS),
         "exponent-two minimum strengthening")
    need(all(maxima[(q0, 2)] > maxima[(q0, 1)] for q0 in Q_ANCHORS),
         "exponent-two positive strengthening")

    minimum_witness = min(rows, key=lambda row: Fraction(
        row["minimum_ratio_decimal"]))
    maximum_witness = max(rows, key=lambda row: Fraction(
        row["maximum_ratio_decimal"]))
    total_targets = sum(row["shell_cardinality"] for row in rows)
    total_labelings = sum(row["enumerated_labelings_mod_global_sign"]
                         for row in rows)
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "protocol": {
            "physical_engine": "locked TPC-268/TPC-288 literal rational engine",
            "source_scale": SOURCE_SCALE,
            "index_interval": [SOURCE_SCALE // 2 + 1, SOURCE_SCALE],
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "row_order": "Q outer, exponent inner",
            "global_sign_gauge": "first shell sign fixed to +1",
            "freshness_scope": (
                "new source indices and new parameter rows inside the same "
                "locked physical engine; not external independent data"),
        },
        "exact_theorem": {
            "gram_identity": "G_(p,q)=<g_p,g_q>",
            "psd_identity":
                "c^T G c=||sum_p c_p g_p||_2^2>=0",
            "modular_rank_implication": (
                "full rank modulo 1000000007, with invertible rational "
                "denominators, certifies full rank over Q"),
            "global_sign_reduction":
                "E(c)=E(-c), so c_1=+1 represents every sign class",
            "gray_enumeration": (
                "one-bit Gray updates visit all 2^(|S|-1) classes exactly once"),
            "finite_ordering": (
                "on the declared four-Q spine, the exact minimum ratio "
                "strictly decreases and the positive ratio strictly increases "
                "for both exponents; exponent two strengthens both inequalities"),
            "scope": "eight finite rational physical rows only",
        },
        "finite_audit": {
            "rows": len(rows),
            "source_index_count_per_row": SOURCE_SCALE // 2,
            "explicit_shell_targets": total_targets,
            "enumerated_labelings_mod_global_sign": total_labelings,
            "full_rank_rows": sum(row["modular_gram_rank"] ==
                                  row["shell_cardinality"] for row in rows),
            "unique_minimum_rows": sum(
                row["minimum_count_mod_global_sign"] == 1 for row in rows),
            "positive_unique_maximum_rows": sum(
                row["maximum_count_mod_global_sign"] == 1 and
                set(row["maximum_label"]) == {1} for row in rows),
            "strict_separation_rows": sum(
                row["minimum_below_one"] and
                row["positive_maximum_above_one"] for row in rows),
            "minimum_ratio_Q_descent_series": 2,
            "positive_ratio_Q_ascent_series": 2,
            "exponent_two_strengthening_Q_cases": 4,
            "smallest_minimum_witness": {
                key: minimum_witness[key] for key in
                ("Q", "kernel_exponent", "minimum_ratio_decimal",
                 "minimum_label")},
            "largest_positive_witness": {
                key: maximum_witness[key] for key in
                ("Q", "kernel_exponent", "maximum_ratio_decimal")},
            "external_physical_holdout": "NONE_SAME_LOCKED_ENGINE",
            "uniform_growing_shell_theorem": "OPEN",
            "arithmetic_l2": "OPEN_LITERAL_SOURCE",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC312_NEW_SOURCE_SHELL_ROWS": "PROVED_EXACT_FINITE_8_ROWS",
            "TPC312_PHYSICAL_GRAM_PSD": "PROVED_EXACT_FINITE",
            "TPC312_RATIONAL_FULL_RANK": "PROVED_EXACT_FINITE_8_OF_8",
            "TPC312_SIGN_EXTREMA": "PROVED_EXACT_FINITE_37440_CLASSES",
            "TPC312_STRICT_SIGN_SEPARATION": "PROVED_EXACT_FINITE_8_OF_8",
            "TPC312_Q_SPINE_ORDERING": "PROVED_EXACT_FINITE_4_Q_BY_2_EXPONENTS",
            "TPC312_FRESHNESS":
                "NEW_SOURCE_SHELL_ROWS_WITHIN_SAME_LOCKED_ENGINE",
            "TPC312_EXTERNAL_INDEPENDENCE": "NONE",
            "TPC312_PROFILE_BUDGET_INTERVAL_CERTIFICATE": "OPEN",
            "TPC312_UNIFORM_ASYMPTOTIC_BUDGET": "OPEN",
            "TPC312_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC312_FIXED_POWER_CREDIT": 0,
            "TPC312_FULL_GATE_B": "OPEN",
            "TPC312_TWIN_PRIME_RESULT": "NONE",
            "TPC312_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == STATUS, "certificate header")
    payload = data.get("payload", {})
    need(payload.get("schema") == SCHEMA, "certificate schema")
    need(data.get("payload_sha256") == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    audit = payload.get("finite_audit", {})
    need(audit.get("rows") == 8 and
         audit.get("explicit_shell_targets") == 84 and
         audit.get("enumerated_labelings_mod_global_sign") == 37440 and
         audit.get("full_rank_rows") == 8 and
         audit.get("unique_minimum_rows") == 8 and
         audit.get("positive_unique_maximum_rows") == 8 and
         audit.get("strict_separation_rows") == 8,
         "finite audit census")
    need(len(payload.get("rows", [])) == 8, "row payload")
    print("TPC312_CERTIFICATE=PASS rows=8 shell_targets=84 "
          "sign_classes=37440 full_rank=8 strict_separation=8")


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
        print("TPC312_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
