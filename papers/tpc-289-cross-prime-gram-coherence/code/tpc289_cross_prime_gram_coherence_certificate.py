#!/usr/bin/env python3
"""TPC-289 exact cross-prime Gram-coherence certificate.

TPC-288 established the physical output Gram and found that a scalar
attachment can be small while vector energy is amplified.  This release
keeps the same frozen operator and asks a narrower question: how much of the
energy surplus is explained by signed cross-prime coherence, and does a
uniform positive-coherence rule survive the declared growth path?

All output and Gram arithmetic is rational.  The certificate is finite; its
conditional accumulation lemma is exact, while the sign/coherence phase
diagram is a numerically certified finite observation rather than an
asymptotic theorem.
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
PARENT288_PROJECT = ROOT / "papers/tpc-288-growing-shell-gram-obstruction"
PARENT288_CODE = PARENT288_PROJECT / (
    "code/tpc288_growing_shell_gram_certificate.py")
PARENT288_RESULT = PARENT288_PROJECT / "results/tpc288_certificate.json"
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

# Eight common-scale anchors retain only the s=2 branch.  Four s=1 rows at
# selected anchors expose the exponent crossover, and six controls probe the
# late Q=70 shell without conflating height and cutoff.
GROWTH_S2 = (
    (128, 24, 9, 5, 2),
    (192, 32, 16, 5, 2),
    (256, 38, 27, 5, 2),
    (384, 50, 40, 5, 2),
    (512, 58, 50, 5, 2),
    (512, 58, 60, 5, 2),
    (512, 58, 70, 5, 2),
    (512, 58, 90, 5, 2),
)
EXPONENT_CROSSOVER = (
    (256, 38, 27, 5, 1),
    (384, 50, 40, 5, 1),
    (512, 58, 70, 5, 1),
    (512, 58, 90, 5, 1),
)
SOURCE_CONTROL_S2 = tuple(
    (384, height, 70, cutoff, 2)
    for height in (48, 52)
    for cutoff in (3, 5, 7)
)

ROWS = tuple(
    (args, "GROWTH_S2") for args in GROWTH_S2
) + tuple(
    (args, "EXPONENT_CROSSOVER") for args in EXPONENT_CROSSOVER
) + tuple(
    (args, "SOURCE_CONTROL_S2") for args in SOURCE_CONTROL_S2
)

ETA = Fraction(3, 5)
DELTA = Fraction(4, 5)
COHERENCE_SQUARED_FLOOR = ETA * ETA

spec = importlib.util.spec_from_file_location("frozen_tpc268_engine", ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen TPC-268 engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    """A fail-closed certificate validation error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return Fraction(value)
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def parent_data() -> dict[str, Any]:
    need(digest(PARENT288_CODE.read_bytes()) == PARENT288_CODE_SHA256,
         "TPC288 code provenance")
    raw = PARENT288_RESULT.read_bytes()
    need(digest(raw) == PARENT288_RESULT_SHA256, "TPC288 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC288 result canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_"
         "NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION",
         "TPC288 status")
    need(data.get("payload", {}).get("finite_audit", {}).get("rows") == 34,
         "TPC288 row census")
    return data


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
    """Build one literal deleted-diagonal prime component exactly."""
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1)
            centered -= Fraction(1, prime - 1)
            total += prime * ENGINE.kernel(u - t, height, exponent) * centered * beta_t
        output.append(total)
    return output


def gram_matrix(outputs: list[list[Fraction]]) -> list[list[Fraction]]:
    return [[sum(x * y for x, y in zip(outputs[i], outputs[j]))
             for j in range(len(outputs))]
            for i in range(len(outputs))]


def sign_label(value: Fraction) -> str:
    if value > 0:
        return "POSITIVE"
    if value < 0:
        return "NEGATIVE"
    return "ZERO"


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


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str) -> dict[str, Any]:
    indices, beta, _weights = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    need(shell and all(prime > 2 for prime in shell), "odd prime shell")
    outputs = [physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    gram = gram_matrix(outputs)
    diagonal = [gram[i][i] for i in range(len(shell))]
    need(all(value > 0 for value in diagonal), "positive component energy")
    diagonal_min, diagonal_max = min(diagonal), max(diagonal)
    pair_values: list[tuple[int, int, Fraction, Fraction]] = []
    for i in range(len(shell)):
        for j in range(i):
            cross = gram[i][j]
            coherence_squared = cross * cross / (diagonal[i] * diagonal[j])
            # This is an exact Cauchy--Schwarz sanity check for the Gram
            # construction.  It also catches accidental non-vector data.
            need(Fraction(0) <= coherence_squared <= Fraction(1),
                 "Cauchy coherence bound")
            pair_values.append((shell[j], shell[i], cross,
                                coherence_squared))

    positive = sum(value[2] > 0 for value in pair_values)
    negative = sum(value[2] < 0 for value in pair_values)
    zero = sum(value[2] == 0 for value in pair_values)
    need(positive + negative + zero == len(pair_values), "pair census")
    minimum = min(pair_values, key=lambda value: value[3])
    negatives = [pair_record(a, b, cross, coh)
                 for a, b, cross, coh in pair_values if cross < 0]
    shell_output = [sum((output[j] for output in outputs), Fraction(0))
                    for j in range(len(indices))]
    shell_energy = sum(value * value for value in shell_output)
    component_energy = sum(
        (sum(value * value for value in output) for output in outputs),
        Fraction(0))
    need(component_energy > 0, "component energy")
    energy_ratio = shell_energy / component_energy
    coherence_floor = positive == len(pair_values) and minimum[3] >= COHERENCE_SQUARED_FLOOR
    diagonal_balance = 5 * diagonal_min >= 4 * diagonal_max
    strong_block = coherence_floor and diagonal_balance
    conditional_lower = Fraction(1) + ETA * DELTA * (len(shell) - 1)
    if strong_block:
        need(energy_ratio >= conditional_lower,
             "conditional accumulation lower bound")

    minimum_record = pair_record(minimum[0], minimum[1], minimum[2], minimum[3])
    return {
        "axis": axis,
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": len(indices),
        "shell": shell,
        "shell_cardinality": len(shell),
        "pair_count": len(pair_values),
        "pair_positive": positive,
        "pair_negative": negative,
        "pair_zero": zero,
        "pairwise_positive": positive == len(pair_values),
        "minimum_coherence_pair": minimum_record,
        "negative_pairs": negatives,
        "diagonal_min": str(diagonal_min),
        "diagonal_max": str(diagonal_max),
        "diagonal_balance_4_over_5": diagonal_balance,
        "coherence_squared_floor_3_over_5": coherence_floor,
        "strong_coherence_block": strong_block,
        "conditional_energy_lower_bound": str(conditional_lower),
        "component_energy": str(component_energy),
        "shell_energy": str(shell_energy),
        "cross_energy": str(shell_energy - component_energy),
        "energy_ratio": str(energy_ratio),
        "energy_ratio_decimal": decimal(energy_ratio),
        "energy_amplified": energy_ratio > 1,
    }


def control_equivalence(rows: list[dict[str, Any]]) -> int:
    """Count exact z-triplets that leave the finite source unchanged."""
    controls = [row for row in rows if row["axis"] == "SOURCE_CONTROL_S2"]
    groups = 0
    for height in (48, 52):
        members = [row for row in controls if row["H"] == height]
        need(len(members) == 3, "control triplet")
        signatures = [(
            row["pair_positive"], row["pair_negative"], row["pair_zero"],
            row["minimum_coherence_pair"]["coherence_squared"],
            row["energy_ratio"],
        ) for row in members]
        if signatures[0] == signatures[1] == signatures[2]:
            groups += 1
    return groups


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    rows = [build_row(*args, axis) for args, axis in ROWS]
    need(len(rows) == 18, "row census")
    pairwise_positive_rows = sum(row["pairwise_positive"] for row in rows)
    negative_pairs = sum(row["pair_negative"] for row in rows)
    amplified_rows = sum(row["energy_amplified"] for row in rows)
    strong_rows = sum(row["strong_coherence_block"] for row in rows)
    need(pairwise_positive_rows == 17, "positive-row census")
    need(negative_pairs == 3, "negative-pair census")
    need(amplified_rows == 18, "energy census")
    need(strong_rows == 8, "strong-block census")
    exceptional = next(row for row in rows
                       if (row["scale"], row["H"], row["Q"],
                           row["comparison_cutoff_z"], row["kernel_exponent"])
                       == (256, 38, 27, 5, 1))
    need(exceptional["pair_negative"] == 3, "exceptional sign row")
    need(any(item["prime_pair"] == [29, 53]
             for item in exceptional["negative_pairs"]),
         "exceptional pair")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc288_code_sha256": PARENT288_CODE_SHA256,
            "tpc288_result_sha256": PARENT288_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "tpc288_rows": parent["payload"]["finite_audit"]["rows"],
        },
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
            "rows": len(ROWS),
        },
        "finite_audit": {
            "rows": len(rows),
            "growth_s2_rows": len(GROWTH_S2),
            "exponent_crossover_rows": len(EXPONENT_CROSSOVER),
            "source_control_rows": len(SOURCE_CONTROL_S2),
            "total_pairs": sum(row["pair_count"] for row in rows),
            "pairwise_positive_rows": pairwise_positive_rows,
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
            "source_native_L2": "OPEN",
            "fixed_power_credit": 0,
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
            "TPC289_TWIN_PRIME_RESULT": "NONE",
            "TPC289_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload(parent_data())
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def check_data(data: dict[str, Any]) -> None:
    need(data == document(), "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    check_data(data)
    audit = data["payload"]["finite_audit"]
    print("TPC289_CERTIFICATE=PASS rows={} positive_rows={} negative_pairs={} "
          "strong_block={} amplified={}".format(
              audit["rows"], audit["pairwise_positive_rows"],
              audit["pairwise_negative_pairs"],
              audit["strong_coherence_block_rows"],
              audit["energy_amplified_rows"]))


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
        print("TPC289_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
