#!/usr/bin/env python3
"""Independent replay of the TPC-289 coherence certificate.

The producer is intentionally not imported.  This replay uses the frozen
engine only, constructs the same literal prime outputs with the summation
order reversed, and independently checks every exact sign and threshold.
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
PROJECT = ROOT / "papers/tpc-289-cross-prime-gram-coherence"
PARENT288_CODE = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/code/"
    "tpc288_growing_shell_gram_certificate.py")
PARENT288_RESULT = ROOT / (
    "papers/tpc-288-growing-shell-gram-obstruction/results/"
    "tpc288_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc289_certificate.json"

PARENT288_CODE_SHA256 = (
    "ee88cef250dc37d14b5fa5bbc22cc9cd5d0a44da6a4e4412118895b27e214987")
PARENT288_RESULT_SHA256 = (
    "39ab30b6701015bfaf85ebb670706182ecd7b52120e9963d58d0731a0a8e947d")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
SCHEMA = "TPC289_CROSS_PRIME_GRAM_COHERENCE_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_NORMALIZED_GRAM_COHERENCE_ACCUMULATION_BOUND_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_SIGN_PHASE_DIAGRAM")
ROUND2_CLUE = (
    "TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_"
    "FINITE_BLOCK")
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

spec = importlib.util.spec_from_file_location("independent_engine", ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen engine unavailable")
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


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT288_CODE.read_bytes()) == PARENT288_CODE_SHA256,
         "TPC288 code lock")
    raw = PARENT288_RESULT.read_bytes()
    need(digest(raw) == PARENT288_RESULT_SHA256, "TPC288 result lock")
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC288 canonicality")
    need(parent["payload"]["finite_audit"]["rows"] == 34,
         "TPC288 row census")
    return {
        "tpc288_code_sha256": PARENT288_CODE_SHA256,
        "tpc288_result_sha256": PARENT288_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc288_rows": 34,
    }


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    # Reverse the producer's u-then-t order: accumulate each source column
    # into the output rows.  Exact Fraction addition is associative here.
    output = [Fraction(0) for _ in indices]
    for t, beta_t in zip(indices, beta):
        if t % prime == 0:
            continue
        for position, u in enumerate(indices):
            if u == t or u % prime == 0:
                continue
            residue = 1 if u % prime == t % prime else 0
            centered = Fraction(residue, 1) - Fraction(1, prime - 1)
            output[position] += (prime * ENGINE.kernel(u - t, height, exponent)
                                 * centered * beta_t)
    return output


def gram_matrix(outputs: list[list[Fraction]]) -> list[list[Fraction]]:
    dimension = len(outputs)
    gram = [[Fraction(0) for _ in range(dimension)]
            for _ in range(dimension)]
    for position in range(len(outputs[0])):
        column = [output[position] for output in outputs]
        for i in range(dimension):
            for j in range(dimension):
                gram[i][j] += column[i] * column[j]
    return gram


def sign_label(value: Fraction) -> str:
    return "POSITIVE" if value > 0 else "NEGATIVE" if value < 0 else "ZERO"


def decimal(value: Fraction) -> str:
    return ENGINE.decimal_text(value)


def pair_record(prime_i: int, prime_j: int, cross: Fraction,
                coherence_squared: Fraction) -> dict[str, Any]:
    return {
        "prime_pair": [prime_i, prime_j],
        "gram_cross": str(cross),
        "sign": sign_label(cross),
        "coherence_squared": str(coherence_squared),
        "coherence_squared_decimal": decimal(coherence_squared),
    }


def make_row(scale: int, height: int, q0: int, cutoff: int, exponent: int,
             axis: str) -> dict[str, Any]:
    indices, beta, _weights = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = gram_matrix(outputs)
    diagonal = [gram[i][i] for i in range(len(shell))]
    need(all(value > 0 for value in diagonal), "diagonal positivity")
    dmin, dmax = min(diagonal), max(diagonal)
    pairs: list[tuple[int, int, Fraction, Fraction]] = []
    for i in range(len(shell)):
        for j in range(i):
            cross = gram[i][j]
            coh = cross * cross / (diagonal[i] * diagonal[j])
            need(Fraction(0) <= coh <= Fraction(1), "Cauchy bound")
            pairs.append((shell[j], shell[i], cross, coh))
    positive = sum(item[2] > 0 for item in pairs)
    negative = sum(item[2] < 0 for item in pairs)
    zero = sum(item[2] == 0 for item in pairs)
    minimum = min(pairs, key=lambda item: item[3])
    negative_records = [pair_record(a, b, cross, coh)
                        for a, b, cross, coh in pairs if cross < 0]
    component_energy = sum(
        (sum(value * value for value in output) for output in outputs),
        Fraction(0))
    aggregate = [sum((output[position] for output in outputs), Fraction(0))
                 for position in range(len(indices))]
    aggregate_energy = sum(value * value for value in aggregate)
    ratio = aggregate_energy / component_energy
    floor_ok = positive == len(pairs) and minimum[3] >= COHERENCE_SQUARED_FLOOR
    balance_ok = 5 * dmin >= 4 * dmax
    strong = floor_ok and balance_ok
    lower = Fraction(1) + ETA * DELTA * (len(shell) - 1)
    if strong:
        need(ratio >= lower, "accumulation lower bound")
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": len(indices), "shell": shell,
        "shell_cardinality": len(shell), "pair_count": len(pairs),
        "pair_positive": positive, "pair_negative": negative,
        "pair_zero": zero, "pairwise_positive": positive == len(pairs),
        "minimum_coherence_pair": pair_record(
            minimum[0], minimum[1], minimum[2], minimum[3]),
        "negative_pairs": negative_records,
        "diagonal_min": str(dmin), "diagonal_max": str(dmax),
        "diagonal_balance_4_over_5": balance_ok,
        "coherence_squared_floor_3_over_5": floor_ok,
        "strong_coherence_block": strong,
        "conditional_energy_lower_bound": str(lower),
        "component_energy": str(component_energy),
        "shell_energy": str(aggregate_energy),
        "cross_energy": str(aggregate_energy - component_energy),
        "energy_ratio": str(ratio), "energy_ratio_decimal": decimal(ratio),
        "energy_amplified": ratio > 1,
    }


def control_equivalence(rows: list[dict[str, Any]]) -> int:
    count = 0
    for height in (48, 52):
        members = [row for row in rows
                   if row["axis"] == "SOURCE_CONTROL_S2" and
                   row["H"] == height]
        need(len(members) == 3, "control triplet")
        keys = [(
            row["pair_positive"], row["pair_negative"], row["pair_zero"],
            row["minimum_coherence_pair"]["coherence_squared"],
            row["energy_ratio"],
        ) for row in members]
        count += int(keys[0] == keys[1] == keys[2])
    return count


def expected_document() -> dict[str, Any]:
    rows = [make_row(*args, axis) for args, axis in ROWS]
    need(len(rows) == 18, "row count")
    positive_rows = sum(row["pairwise_positive"] for row in rows)
    negative_pairs = sum(row["pair_negative"] for row in rows)
    strong_rows = sum(row["strong_coherence_block"] for row in rows)
    amplified_rows = sum(row["energy_amplified"] for row in rows)
    need((positive_rows, negative_pairs, strong_rows, amplified_rows) ==
         (17, 3, 8, 18), "audit census")
    payload = {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "gram_definition": "G_{q,r}=<g_q,g_r>",
            "gram_psd": "c^T G c=||sum_q c_q g_q||_2^2>=0",
            "coherence_definition":
                "Gamma_{q,r}=G_{q,r}^2/(G_{q,q}G_{r,r})",
            "cauchy_bound": "0<=Gamma_{q,r}<=1",
            "accumulation_bound":
                "positive Gamma>=eta^2 and d_min/d_max>=delta => "
                "R_E>=1+eta*delta*(k-1)",
            "energy_identity": "R_E=1+sum_{q!=r}G_{q,r}/sum_q G_{q,q}",
            "scope": "finite shell, frozen source, literal deleted-diagonal operator",
        },
        "thresholds": {"eta": str(ETA), "delta": str(DELTA),
                       "coherence_squared_floor": str(COHERENCE_SQUARED_FLOOR)},
        "grid": {
            "growth_s2": [list(item) for item in GROWTH_S2],
            "exponent_crossover": [list(item)
                                   for item in EXPONENT_CROSSOVER],
            "source_control_s2": [list(item) for item in SOURCE_CONTROL_S2],
            "rows": 18,
        },
        "finite_audit": {
            "rows": 18, "growth_s2_rows": 8,
            "exponent_crossover_rows": 4, "source_control_rows": 6,
            "total_pairs": sum(row["pair_count"] for row in rows),
            "pairwise_positive_rows": positive_rows,
            "pairwise_negative_rows": sum(row["pair_negative"] > 0
                                           for row in rows),
            "pairwise_negative_pairs": negative_pairs,
            "pairwise_zero_pairs": sum(row["pair_zero"] for row in rows),
            "energy_amplified_rows": amplified_rows,
            "strong_coherence_block_rows": strong_rows,
            "control_cutoff_equivalence_groups": control_equivalence(rows),
            "uniform_pairwise_positivity": "REFUTED_FINITE",
            "uniform_coherence_floor": "REFUTED_FINITE",
            "growing_coherence_theorem": "OPEN",
            "source_native_L2": "OPEN", "fixed_power_credit": 0,
        },
        "rows": rows,
        "firewall": {
            "TPC289_EXACT_GRAM_COHERENCE": "PROVED_EXACT_FINITE",
            "TPC289_EXACT_ACCUMULATION_BOUND": "PROVED_EXACT_CONDITIONAL",
            "TPC289_PAIRWISE_POSITIVITY":
                "NUMERICALLY_CERTIFIED_FINITE_17_OF_18_ROWS",
            "TPC289_SIGN_FLIP_OBSTRUCTION":
                "NUMERICALLY_CERTIFIED_FINITE_3_PAIRS_ONE_ROW",
            "TPC289_STRONG_COHERENCE_BLOCK":
                "NUMERICALLY_CERTIFIED_FINITE_8_ROWS",
            "TPC289_ENERGY_AMPLIFIED":
                "NUMERICALLY_CERTIFIED_FINITE_18_OF_18_ROWS",
            "TPC289_GROWING_COHERENCE_STABILITY": "OPEN",
            "TPC289_SOURCE_CONTROL_UNIFORMITY": "OPEN",
            "TPC289_SOURCE_NATIVE_L2": "OPEN_LITERAL_SOURCE",
            "TPC289_FIXED_POWER_CREDIT": 0,
            "TPC289_FULL_GATE_B": "OPEN",
            "TPC289_TWIN_PRIME_RESULT": "NONE", "TPC289_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def main() -> int:
    actual_raw = RESULT.read_bytes()
    actual = json.loads(actual_raw)
    need(actual_raw == canonical(actual), "result canonicality")
    need(actual == expected_document(), "independent document mismatch")
    print("TPC289_INDEPENDENT_CHECK=PASS rows=18 positive_rows=17 "
          "negative_pairs=3 strong_block=8 amplified=18")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC289_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
