#!/usr/bin/env python3
"""Independent reverse-order replay for TPC-290.

This checker does not import the TPC-290 producer.  It rebuilds the physical
vectors with the source-column loop reversed, then checks the exact policy,
pair-support, and leave-one-out records in the frozen certificate.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-290-adaptive-shell-weighting-obstruction"
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
STATUS = (
    "PROVED_EXACT_NONNEGATIVE_WEIGHTED_GRAM_NO_DECAY_BOUND_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_ADAPTIVE_WEIGHTING_OBSTRUCTION")
POLICIES = ("uniform", "inverse_diagonal", "linear_taper")
ETA = Fraction(3, 5)
DELTA = Fraction(4, 5)
FLOOR = ETA * ETA
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

spec = importlib.util.spec_from_file_location("independent_engine", ENGINE_CODE)
if spec is None or spec.loader is None:
    raise SystemExit("TPC290_INDEPENDENT_CHECK=FAIL engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


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


def decimal(value: Fraction) -> str:
    return ENGINE.decimal_text(value)


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT289_CODE.read_bytes()) == PARENT289_CODE_SHA256,
         "TPC289 code lock")
    raw = PARENT289_RESULT.read_bytes()
    need(digest(raw) == PARENT289_RESULT_SHA256, "TPC289 result lock")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC289 canonicality")
    need(data.get("claim_status", "").startswith(
        "PROVED_EXACT_NORMALIZED_GRAM_COHERENCE"), "TPC289 status")
    need(data.get("payload", {}).get("finite_audit", {}).get("rows") == 18,
         "TPC289 row count")
    return {"tpc289_code_sha256": PARENT289_CODE_SHA256,
            "tpc289_result_sha256": PARENT289_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256, "tpc289_rows": 18}


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    # Reverse the producer's u-then-t order.  Exact Fraction arithmetic makes
    # the two orders mathematically identical while exercising another path.
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


def weighted_ratio(gram: list[list[Fraction]], diagonal: list[Fraction],
                   weights: list[Fraction]) -> Fraction:
    denominator = sum(weights[i] * weights[i] * diagonal[i]
                      for i in range(len(weights)))
    numerator = sum(weights[i] * gram[i][j] * weights[j]
                    for i in range(len(weights))
                    for j in range(len(weights)))
    need(denominator > 0, "weighted denominator")
    return numerator / denominator


def weights(name: str, shell: list[int], diagonal: list[Fraction],
            q0: int) -> list[Fraction]:
    if name == "uniform":
        return [Fraction(1) for _ in shell]
    if name == "inverse_diagonal":
        return [Fraction(1, value) for value in diagonal]
    if name == "linear_taper":
        return [Fraction(2 * q0 - q) for q in shell]
    raise Failure("policy")


def row_expected(scale: int, height: int, q0: int, cutoff: int,
                 exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _ = ENGINE.source_weights(scale, cutoff)
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    outputs = [physical_output(indices, beta, height, q, exponent)
               for q in shell]
    gram = [[sum(outputs[i][u] * outputs[j][u]
                 for u in range(len(indices)))
             for j in range(len(shell))] for i in range(len(shell))]
    diagonal = [gram[i][i] for i in range(len(shell))]
    pairs = []
    for i in range(len(shell)):
        for j in range(i):
            cross = gram[i][j]
            coh = cross * cross / (diagonal[i] * diagonal[j])
            need(0 <= coh <= 1, "coherence")
            pairs.append((i, j, cross, coh))
    positive = sum(item[2] > 0 for item in pairs)
    negative = sum(item[2] < 0 for item in pairs)
    zero = sum(item[2] == 0 for item in pairs)
    minimum = min(pairs, key=lambda item: item[3])
    dmin, dmax = min(diagonal), max(diagonal)
    strong = (positive == len(pairs) and minimum[3] >= FLOOR and
              5 * dmin >= 4 * dmax)
    policy_data: dict[str, Any] = {}
    for name in POLICIES:
        ww = weights(name, shell, diagonal, q0)
        rr = weighted_ratio(gram, diagonal, ww)
        effective = sum(ww) ** 2 / sum(value * value for value in ww)
        lower = Fraction(1) + ETA * DELTA * (effective - 1) if strong else None
        if lower is not None:
            need(rr >= lower, "strong weighted bound")
        policy_data[name] = {
            "weights_nonnegative": all(value >= 0 for value in ww),
            "full_support": all(value > 0 for value in ww),
            "ratio": str(rr), "ratio_decimal": decimal(rr),
            "effective_support": str(effective),
            "effective_support_decimal": decimal(effective),
            "conditional_lower_bound": None if lower is None else str(lower),
            "conditional_lower_bound_pass":
                None if lower is None else rr >= lower,
            "amplified": rr > 1,
        }
    pair_records = []
    for i, j, cross, _coh in pairs:
        diagonal_sum = diagonal[i] + diagonal[j]
        rr = (diagonal_sum + 2 * cross) / diagonal_sum
        pair_records.append({
            "prime_pair": [shell[j], shell[i]], "gram_cross": str(cross),
            "equal_pair_ratio": str(rr),
            "equal_pair_ratio_decimal": decimal(rr), "subunit": rr < 1,
        })
    drop = []
    for omitted in range(len(shell)):
        ww = [Fraction(1) for _ in shell]
        ww[omitted] = Fraction(0)
        drop.append((weighted_ratio(gram, diagonal, ww), shell[omitted]))
    drop_min = min(drop)
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "shell": shell, "shell_cardinality": len(shell),
        "pair_count": len(pairs), "pair_positive": positive,
        "pair_negative": negative, "pair_zero": zero,
        "pairwise_positive": positive == len(pairs),
        "minimum_coherence_pair": {
            "prime_pair": [shell[minimum[1]], shell[minimum[0]]],
            "coherence_squared": str(minimum[3]),
            "coherence_squared_decimal": decimal(minimum[3]),
        },
        "equal_pair_subunit_count": sum(item["subunit"] for item in pair_records),
        "equal_pair_subunit_witnesses": [
            item for item in pair_records if item["subunit"]],
        "diagonal_min": str(dmin), "diagonal_max": str(dmax),
        "diagonal_balance_4_over_5": 5 * dmin >= 4 * dmax,
        "strong_coherence_block": strong, "policies": policy_data,
        "drop_one_min_ratio": str(drop_min[0]),
        "drop_one_min_ratio_decimal": decimal(drop_min[0]),
        "drop_one_omitted_prime": drop_min[1],
        "drop_one_all_amplified": all(value[0] > 1 for value in drop),
    }


def main() -> int:
    raw = RESULT.read_bytes()
    actual = json.loads(raw)
    need(raw == canonical(actual), "certificate canonicality")
    need(actual.get("certificate_version") == 1 and
         actual.get("claim_status") == STATUS, "certificate header")
    payload = actual["payload"]
    need(payload["parent_lock"] == parent_lock(), "parent lock")
    expected_rows = [row_expected(*args, axis) for args, axis in ROWS]
    got_rows = payload["rows"]
    need(len(got_rows) == len(expected_rows), "row count")
    for index, (got, expected) in enumerate(zip(got_rows, expected_rows)):
        for key, value in expected.items():
            need(got.get(key) == value, "row {} field {}".format(index, key))
    audit = payload["finite_audit"]
    need(audit["rows"] == 18 and audit["policy_rows"] == 54,
         "audit dimensions")
    need(audit["all_full_support_policies_amplified_rows"] == 18 and
         audit["equal_pair_subunit_rows"] == 1 and
         audit["equal_pair_subunit_witnesses"] == 3 and
         audit["drop_one_all_amplified_rows"] == 18,
         "audit census")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(payload)).hexdigest(), "payload hash")
    print("TPC290_INDEPENDENT_CHECK=PASS rows=18 policy_rows=54 "
          "full_amplified=18 pair_subunit=3 drop_amplified=18")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC290_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
