#!/usr/bin/env python3
"""Exact finite certificate for the TPC-290 adaptive-weighting obstruction.

TPC-289 found a positive-coherence late-shell block, but also found three
early sign-flip pairs.  This release asks whether a nonnegative, adaptive
weight vector can turn the physical shell energy into decay.  Everything in
the finite certificate is rational; the weighted theorem is an exact
Hilbert-space statement and the shell scan is finite evidence only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT289_CODE = ROOT / (
    "papers/tpc-289-cross-prime-gram-coherence/code/"
    "tpc289_cross_prime_gram_coherence_certificate.py")
PARENT289_RESULT = ROOT / (
    "papers/tpc-289-cross-prime-gram-coherence/results/"
    "tpc289_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc290_certificate.json"

PARENT289_CODE_SHA256 = (
    "9baa58dc05b5707931d623a72198bc1ee6aecdd61bbe63aaf06784f9cc7268f4")
PARENT289_RESULT_SHA256 = (
    "9f0a2db34195fe93c8acb461bb7e0caa615a4a781f948732ad9572344c6efb1e")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

SCHEMA = "TPC290_ADAPTIVE_SHELL_WEIGHTING_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION")
ROUND2_CLUE = (
    "TEST_SIGNED_TWO_PRIME_SCHUR_CANCELLATION_OR_SOURCE_RESTRICTED_"
    "DIFFUSE_WEIGHTS")

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

ETA = Fraction(3, 5)
DELTA = Fraction(4, 5)
COHERENCE_SQUARED_FLOOR = ETA * ETA
POLICIES = ("uniform", "inverse_diagonal", "linear_taper")

parent_spec = importlib.util.spec_from_file_location("frozen_tpc289", PARENT289_CODE)
if parent_spec is None or parent_spec.loader is None:
    raise RuntimeError("TPC-289 parent unavailable")
PARENT = importlib.util.module_from_spec(parent_spec)
parent_spec.loader.exec_module(PARENT)

engine_spec = importlib.util.spec_from_file_location("frozen_tpc268", ENGINE_CODE)
if engine_spec is None or engine_spec.loader is None:
    raise RuntimeError("frozen TPC-268 engine unavailable")
ENGINE = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    """Raised when the frozen finite contract is not reproduced."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT289_CODE.read_bytes()) == PARENT289_CODE_SHA256,
         "TPC289 code provenance")
    raw = PARENT289_RESULT.read_bytes()
    need(digest(raw) == PARENT289_RESULT_SHA256, "TPC289 result provenance")
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC289 result canonicality")
    payload = parent.get("payload", {})
    need(parent.get("certificate_version") == 1 and
         parent.get("claim_status") == PARENT.STATUS,
         "TPC289 status")
    need(payload.get("schema") == "TPC289_CROSS_PRIME_GRAM_COHERENCE_CERTIFICATE_V1",
         "TPC289 schema")
    need(payload.get("finite_audit", {}).get("rows") == 18,
         "TPC289 row count")
    return {
        "tpc289_code_sha256": PARENT289_CODE_SHA256,
        "tpc289_result_sha256": PARENT289_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc289_rows": 18,
    }


def ratio(outputs: list[list[Fraction]], gram: list[list[Fraction]],
          diagonal: list[Fraction], weights: list[Fraction]) -> Fraction:
    denominator = sum(weights[i] * weights[i] * diagonal[i]
                      for i in range(len(weights)))
    need(denominator > 0, "weighted denominator")
    numerator = sum(weights[i] * gram[i][j] * weights[j]
                    for i in range(len(weights))
                    for j in range(len(weights)))
    return numerator / denominator


def policy_weights(name: str, shell: list[int],
                   diagonal: list[Fraction], q0: int) -> list[Fraction]:
    if name == "uniform":
        return [Fraction(1) for _ in shell]
    if name == "inverse_diagonal":
        return [Fraction(1, value) for value in diagonal]
    if name == "linear_taper":
        return [Fraction(2 * q0 - prime) for prime in shell]
    raise CheckFailure("unknown policy")


def decimal(value: Fraction) -> str:
    return ENGINE.decimal_text(value)


def pair_record(a: int, b: int, cross: Fraction,
                diagonal_sum: Fraction) -> dict[str, Any]:
    pair_ratio = (diagonal_sum + 2 * cross) / diagonal_sum
    return {
        "prime_pair": [a, b],
        "gram_cross": str(cross),
        "equal_pair_ratio": str(pair_ratio),
        "equal_pair_ratio_decimal": decimal(pair_ratio),
        "subunit": pair_ratio < 1,
    }


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    need(shell and all(prime > 2 for prime in shell), "odd prime shell")
    outputs = [PARENT.physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = [[sum(x * y for x, y in zip(outputs[i], outputs[j]))
             for j in range(len(shell))] for i in range(len(shell))]
    diagonal = [gram[i][i] for i in range(len(shell))]
    need(all(value > 0 for value in diagonal), "positive diagonal")
    pairs: list[tuple[int, int, Fraction, Fraction]] = []
    for i in range(len(shell)):
        for j in range(i):
            cross = gram[i][j]
            coherence = cross * cross / (diagonal[i] * diagonal[j])
            need(Fraction(0) <= coherence <= Fraction(1), "Cauchy bound")
            pairs.append((shell[j], shell[i], cross, coherence))
    positive = sum(item[2] > 0 for item in pairs)
    negative = sum(item[2] < 0 for item in pairs)
    zero = sum(item[2] == 0 for item in pairs)
    minimum = min(pairs, key=lambda item: item[3])
    dmin, dmax = min(diagonal), max(diagonal)
    strong = (positive == len(pairs) and
              minimum[3] >= COHERENCE_SQUARED_FLOOR and
              5 * dmin >= 4 * dmax)

    policy_records: dict[str, Any] = {}
    for name in POLICIES:
        weights = policy_weights(name, shell, diagonal, q0)
        weighted_ratio = ratio(outputs, gram, diagonal, weights)
        effective = sum(weights) ** 2 / sum(value * value for value in weights)
        lower = (Fraction(1) + ETA * DELTA * (effective - 1)
                 if strong else None)
        if lower is not None:
            need(weighted_ratio >= lower, "weighted strong-block bound")
        policy_records[name] = {
            "weights_nonnegative": all(value >= 0 for value in weights),
            "full_support": all(value > 0 for value in weights),
            "ratio": str(weighted_ratio),
            "ratio_decimal": decimal(weighted_ratio),
            "effective_support": str(effective),
            "effective_support_decimal": decimal(effective),
            "conditional_lower_bound": None if lower is None else str(lower),
            "conditional_lower_bound_pass":
                None if lower is None else weighted_ratio >= lower,
            "amplified": weighted_ratio > 1,
        }

    pair_records = []
    for i in range(len(shell)):
        for j in range(i):
            pair_records.append(pair_record(
                shell[j], shell[i], gram[i][j], diagonal[i] + diagonal[j]))
    subunit_pairs = [item for item in pair_records if item["subunit"]]

    drop_one: list[tuple[Fraction, int]] = []
    for omitted in range(len(shell)):
        weights = [Fraction(1) for _ in shell]
        weights[omitted] = Fraction(0)
        drop_one.append((ratio(outputs, gram, diagonal, weights),
                         shell[omitted]))
    drop_min = min(drop_one)

    return {
        "axis": axis,
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "shell": shell,
        "shell_cardinality": len(shell),
        "pair_count": len(pairs),
        "pair_positive": positive,
        "pair_negative": negative,
        "pair_zero": zero,
        "pairwise_positive": positive == len(pairs),
        "minimum_coherence_pair": {
            "prime_pair": [minimum[0], minimum[1]],
            "coherence_squared": str(minimum[3]),
            "coherence_squared_decimal": decimal(minimum[3]),
        },
        "equal_pair_subunit_count": len(subunit_pairs),
        "equal_pair_subunit_witnesses": subunit_pairs,
        "diagonal_min": str(dmin),
        "diagonal_max": str(dmax),
        "diagonal_balance_4_over_5": 5 * dmin >= 4 * dmax,
        "strong_coherence_block": strong,
        "policies": policy_records,
        "drop_one_min_ratio": str(drop_min[0]),
        "drop_one_min_ratio_decimal": decimal(drop_min[0]),
        "drop_one_omitted_prime": drop_min[1],
        "drop_one_all_amplified": all(value[0] > 1 for value in drop_one),
    }


def control_groups(rows: list[dict[str, Any]]) -> int:
    groups = 0
    for height in (48, 52):
        members = [row for row in rows
                   if row["axis"] == "SOURCE_CONTROL_S2" and
                   row["H"] == height]
        need(len(members) == 3, "control triplet")
        signatures = [(
            row["pair_positive"], row["pair_negative"],
            row["minimum_coherence_pair"]["coherence_squared"],
            row["policies"]["uniform"]["ratio"],
        ) for row in members]
        groups += int(signatures[0] == signatures[1] == signatures[2])
    return groups


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    rows = [build_row(*args, axis) for args, axis in ROWS]
    need(len(rows) == 18, "row count")
    policy_rows = len(rows) * len(POLICIES)
    subunit_rows = sum(row["equal_pair_subunit_count"] > 0 for row in rows)
    subunit_pairs = sum(row["equal_pair_subunit_count"] for row in rows)
    strong_rows = sum(row["strong_coherence_block"] for row in rows)
    amplified = sum(all(row["policies"][name]["amplified"] for name in POLICIES)
                    for row in rows)
    drop_amplified = sum(row["drop_one_all_amplified"] for row in rows)
    need((policy_rows, subunit_rows, subunit_pairs, strong_rows,
          amplified, drop_amplified) == (54, 1, 3, 8, 18, 18),
         "finite census")
    exceptional = next(row for row in rows
                       if (row["scale"], row["H"], row["Q"],
                           row["comparison_cutoff_z"],
                           row["kernel_exponent"]) == (256, 38, 27, 5, 1))
    need(exceptional["equal_pair_subunit_count"] == 3,
         "exceptional pair support census")
    return {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "weighted_ratio":
                "R(w)=||sum_q w_q g_q||_2^2/sum_q w_q^2 d_q",
            "weighted_energy_identity":
                "R(w)=1+2 sum_{q<r} w_q w_r G_{q,r}/sum_q w_q^2 d_q",
            "nonnegative_no_decay":
                "w_q>=0 and G_{q,r}>=0 => R(w)>=1",
            "effective_support":
                "kappa(w)=(sum_q w_q)^2/sum_q w_q^2",
            "diffuse_accumulation_bound":
                "G_{q,r}>=eta sqrt(d_q d_r), d_min/d_max>=delta, w>=0 "
                "=> R(w)>=1+eta delta (kappa(w)-1)",
            "equal_pair_witness":
                "w_i=w_j=1, others=0 => R=1+2G_{i,j}/(d_i+d_j)",
            "scope": "finite shell, frozen source, literal deleted-diagonal operator",
        },
        "thresholds": {
            "eta": str(ETA),
            "delta": str(DELTA),
            "coherence_squared_floor": str(COHERENCE_SQUARED_FLOOR),
        },
        "grid": {
            "growth_s2": [list(item) for item in GROWTH_S2],
            "exponent_crossover": [list(item)
                                   for item in EXPONENT_CROSSOVER],
            "source_control_s2": [list(item) for item in SOURCE_CONTROL_S2],
            "policies": list(POLICIES),
            "rows": len(ROWS),
        },
        "finite_audit": {
            "rows": len(rows),
            "policy_rows": policy_rows,
            "full_support_policy_rows": policy_rows,
            "all_full_support_policies_amplified_rows": amplified,
            "equal_pair_subunit_rows": subunit_rows,
            "equal_pair_subunit_witnesses": subunit_pairs,
            "drop_one_all_amplified_rows": drop_amplified,
            "strong_coherence_block_rows": strong_rows,
            "control_signature_groups": control_groups(rows),
            "uniform_nonnegative_no_decay": "REFUTED_FINITE_BY_SPARSE_SIGN_FLIP",
            "diffuse_positive_block_obstruction": "CERTIFIED_FINITE",
            "growing_weighted_theorem": "OPEN",
            "source_native_L2": "OPEN",
            "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC290_WEIGHTED_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC290_NONNEGATIVE_NO_DECAY": "PROVED_EXACT_CONDITIONAL",
            "TPC290_DIFFUSE_ACCUMULATION_BOUND": "PROVED_EXACT_CONDITIONAL",
            "TPC290_FULL_SUPPORT_POLICY_SCAN":
                "NUMERICALLY_CERTIFIED_FINITE_54_OF_54_AMPLIFIED",
            "TPC290_SPARSE_SIGN_FLIP_ESCAPE":
                "NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW",
            "TPC290_DROP_ONE_SCAN": "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_AMPLIFIED",
            "TPC290_GROWING_WEIGHTED_THEOREM": "OPEN",
            "TPC290_SOURCE_NATIVE_L2": "OPEN_LITERAL_SOURCE",
            "TPC290_FIXED_POWER_CREDIT": 0,
            "TPC290_FULL_GATE_B": "OPEN",
            "TPC290_TWIN_PRIME_RESULT": "NONE",
            "TPC290_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def frozen_document() -> dict[str, Any]:
    payload = build_payload({})
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(frozen_document()))


def check_data(data: dict[str, Any]) -> None:
    expected = frozen_document()
    need(data == expected, "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    check_data(data)
    audit = data["payload"]["finite_audit"]
    print("TPC290_CERTIFICATE=PASS rows={} policy_rows={} full_amplified={} "
          "pair_subunit={} drop_amplified={}".format(
              audit["rows"], audit["policy_rows"],
              audit["all_full_support_policies_amplified_rows"],
              audit["equal_pair_subunit_witnesses"],
              audit["drop_one_all_amplified_rows"]))


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
        print("TPC290_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
