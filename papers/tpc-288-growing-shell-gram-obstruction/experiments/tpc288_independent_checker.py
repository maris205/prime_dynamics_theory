#!/usr/bin/env python3
"""Independent replay for the TPC-288 growing-shell certificate.

This file intentionally does not import the TPC-288 producer.  It rebuilds
the literal outputs, scalar intervals, exact energies, modular Gram ranks,
and the selected active-operator ranks from the frozen TPC-268 engine, then
compares a freshly constructed canonical document with the committed result.
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
PROJECT = ROOT / "papers/tpc-288-growing-shell-gram-obstruction"
PARENT287_CODE = ROOT / (
    "papers/tpc-287-prime-shell-cancellation-depth/code/"
    "tpc287_prime_shell_cancellation_certificate.py")
PARENT287_RESULT = ROOT / (
    "papers/tpc-287-prime-shell-cancellation-depth/results/"
    "tpc287_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc288_certificate.json"

PARENT287_CODE_SHA256 = (
    "944f276ac661cc115bca8fe29aa214be981b65692348f737b94c9429260aeb2f")
PARENT287_RESULT_SHA256 = (
    "a72dd15e4b2977c04d3cba81b4f02d5736d9d8dcab6fcf7c8661d45ddc1fee30")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
MODULUS = 1_000_000_007
SCHEMA = "TPC288_GROWING_SHELL_GRAM_OBSTRUCTION_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_PHYSICAL_OUTPUT_GRAM_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_GROWING_SHELL_FULL_RANK_OBSTRUCTION")
ROUND2_CLUE = (
    "TEST_SOURCE_NATIVE_CROSS_PRIME_GRAM_BOUNDS_BEYOND_FINITE_"
    "FULL_RANK_OBSTRUCTION")
GROWTH_PATH = (
    (128, 24, 9, 5), (192, 32, 16, 5), (256, 38, 27, 5),
    (384, 50, 40, 5), (512, 58, 50, 5), (512, 58, 60, 5),
    (512, 58, 70, 5), (512, 58, 90, 5),
)
CONTROL_GRID = tuple(
    (384, height, 70, cutoff, exponent)
    for height in (48, 50, 52)
    for cutoff in (3, 5, 7)
    for exponent in (1, 2)
)
OPERATOR_RANK_CASES = frozenset({
    (128, 24, 9, 5, 1), (192, 32, 16, 5, 1),
    (256, 38, 27, 5, 1), (384, 50, 40, 5, 1),
    (384, 50, 70, 5, 1), (512, 58, 60, 5, 1),
})

spec = importlib.util.spec_from_file_location("independent_tpc268", ENGINE_CODE)
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


def interval(value: object) -> tuple[Fraction, Fraction]:
    if hasattr(value, "lo") and hasattr(value, "hi"):
        lo, hi = Fraction(value.lo), Fraction(value.hi)
    else:
        need(isinstance(value, (list, tuple)) and len(value) == 2,
             "interval shape")
        lo, hi = Fraction(value[0]), Fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def interval_text(value: object) -> list[str]:
    lo, hi = interval(value)
    return [ENGINE.decimal_text(lo), ENGINE.decimal_text(hi)]


def parent_lock() -> dict[str, Any]:
    need(digest(PARENT287_CODE.read_bytes()) == PARENT287_CODE_SHA256,
         "TPC287 code lock")
    raw = PARENT287_RESULT.read_bytes()
    need(digest(raw) == PARENT287_RESULT_SHA256, "TPC287 result lock")
    parent = json.loads(raw)
    need(raw == canonical(parent), "TPC287 canonicality")
    need(parent["payload"]["finite_audit"]["rows"] == 84,
         "TPC287 row census")
    return {
        "tpc287_code_sha256": PARENT287_CODE_SHA256,
        "tpc287_result_sha256": PARENT287_RESULT_SHA256,
        "engine_code_sha256": ENGINE_CODE_SHA256,
        "tpc287_rows": 84,
    }


def physical_output(indices: list[int], beta: list[Fraction], height: int,
                    prime: int, exponent: int) -> list[Fraction]:
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


def attachment(indices: list[int], weights: list[Any],
                output: list[Fraction]) -> Any:
    n = len(indices)
    need(n % 4 == 0, "four blocks")
    block = n // 4
    block_w = [sum((weights[j] for j in range(k * block, (k + 1) * block)),
                   ENGINE.Interval(Fraction(0))) for k in range(4)]
    block_g = [sum((output[j] for j in range(k * block, (k + 1) * block)),
                   Fraction(0)) for k in range(4)]
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    direct = sum((weights[j] * output[j] for j in range(n)),
                 ENGINE.Interval(Fraction(0)))
    projected = ENGINE.Interval(Fraction(0))
    for coefficients, denominator in zip(contrasts, denominators):
        wc = sum((block_w[k] * coefficients[k] for k in range(4)),
                 ENGINE.Interval(Fraction(0)))
        gc = sum((block_g[k] * coefficients[k] for k in range(4)),
                 Fraction(0))
        projected += wc * gc / Fraction(denominator)
    return direct - projected


def absolute_lower(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return Fraction(0) if lo <= 0 <= hi else min(abs(lo), abs(hi))


def absolute_upper(value: tuple[Fraction, Fraction]) -> Fraction:
    return max(abs(value[0]), abs(value[1]))


def fraction_mod(value: Fraction) -> int:
    denominator = value.denominator % MODULUS
    need(denominator != 0, "modular denominator")
    return value.numerator % MODULUS * pow(
        denominator, MODULUS - 2, MODULUS) % MODULUS


def rank_mod(matrix: list[list[int]]) -> int:
    if not matrix:
        return 0
    rows, columns, rank = len(matrix), len(matrix[0]), 0
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
                target = matrix[i]
                for j in range(column, columns):
                    target[j] = (target[j] - factor * row[j]) % MODULUS
        rank += 1
        if rank == rows:
            break
    return rank


def gram_rank(outputs: list[list[Fraction]]) -> int:
    vectors = [[fraction_mod(value) for value in output]
               for output in outputs]
    matrix = [[sum(vectors[i][k] * vectors[j][k]
                   for k in range(len(vectors[i]))) % MODULUS
               for j in range(len(vectors))]
              for i in range(len(vectors))]
    return rank_mod(matrix)


def operator_rank(indices: list[int], height: int, shell: list[int],
                  exponent: int) -> tuple[int, int]:
    active = [u for u in indices if all(u % prime for prime in shell)]
    h_power = pow(height, 2 * exponent, MODULUS)
    matrix: list[list[int]] = []
    for u in active:
        row: list[int] = []
        for t in active:
            if u == t:
                row.append(0)
                continue
            entry = 0
            difference = u - t
            denominator = (height * height + difference * difference) % MODULUS
            kernel_denominator = pow(denominator, exponent, MODULUS)
            need(kernel_denominator != 0, "operator denominator")
            kernel = h_power * pow(kernel_denominator,
                                   MODULUS - 2, MODULUS) % MODULUS
            for prime in shell:
                inverse_q = pow(prime - 1, MODULUS - 2, MODULUS)
                centered = ((prime - 2) * inverse_q % MODULUS
                            if u % prime == t % prime
                            else -inverse_q % MODULUS)
                entry = (entry + prime * kernel * centered) % MODULUS
            row.append(entry)
        matrix.append(row)
    return len(active), rank_mod(matrix)


def sign(value: tuple[Fraction, Fraction]) -> str:
    if value[1] < 0:
        return "NEGATIVE"
    if value[0] > 0:
        return "POSITIVE"
    return "CROSSING"


def make_row(scale: int, height: int, q0: int, cutoff: int, exponent: int,
             axis: str) -> dict[str, Any]:
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    outputs = [physical_output(indices, beta, height, prime, exponent)
               for prime in shell]
    intervals = [interval(attachment(indices, weights, output))
                 for output in outputs]
    shell_output = [sum((output[j] for output in outputs), Fraction(0))
                    for j in range(len(indices))]
    shell_iv = interval(attachment(indices, weights, shell_output))
    mass_lo = sum((absolute_lower(v) for v in intervals), Fraction(0))
    mass_hi = sum((absolute_upper(v) for v in intervals), Fraction(0))
    need(mass_lo > 0 and mass_hi > 0, "scalar mass")
    shell_lo, shell_hi = absolute_lower(shell_iv), absolute_upper(shell_iv)
    retention_lo, retention_hi = shell_lo / mass_hi, shell_hi / mass_lo
    component_energy = sum((sum(value * value for value in output)
                            for output in outputs), Fraction(0))
    shell_energy = sum(value * value for value in shell_output)
    energy_ratio = shell_energy / component_energy
    output_gram_rank = gram_rank(outputs)
    records = [{
        "prime": prime,
        "attachment_interval": interval_text(value),
        "absolute_lower": str(absolute_lower(value)),
        "absolute_upper": str(absolute_upper(value)),
        "sign": sign(value),
        "zero_separated": value[1] < 0 or value[0] > 0,
    } for prime, value in zip(shell, intervals)]
    rank_audit = (scale, height, q0, cutoff, exponent) in OPERATOR_RANK_CASES
    active_rank = operator_active = None
    if rank_audit:
        operator_active, active_rank = operator_rank(
            indices, height, shell, exponent)
    return {
        "axis": axis, "scale": scale, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": len(indices), "shell": shell,
        "shell_cardinality": len(shell), "active_index_count": sum(
            all(value % prime for prime in shell) for value in indices),
        "components": records,
        "component_sign_crossings": sum(r["sign"] == "CROSSING" for r in records),
        "component_negative": sum(r["sign"] == "NEGATIVE" for r in records),
        "shell_attachment_interval": interval_text(shell_iv),
        "shell_sign": sign(shell_iv),
        "component_scalar_mass_lower": str(mass_lo),
        "component_scalar_mass_upper": str(mass_hi),
        "shell_scalar_abs_lower": str(shell_lo),
        "shell_scalar_abs_upper": str(shell_hi),
        "scalar_retention_lower": str(retention_lo),
        "scalar_retention_upper": str(retention_hi),
        "scalar_retention_upper_decimal": ENGINE.decimal_text(retention_hi),
        "scalar_upper_lt_tenth": retention_hi < Fraction(1, 10),
        "component_energy": str(component_energy),
        "shell_energy": str(shell_energy),
        "cross_energy": str(shell_energy - component_energy),
        "energy_ratio": str(energy_ratio),
        "energy_ratio_decimal": ENGINE.decimal_text(energy_ratio),
        "energy_amplified": energy_ratio > 1,
        "gram_dimension": len(shell), "gram_rank_mod": output_gram_rank,
        "gram_positive_definite": output_gram_rank == len(shell),
        "operator_rank_audited": rank_audit,
        "operator_active_dimension": operator_active,
        "operator_rank_mod": active_rank,
        "scalar_energy_mismatch": retention_hi < Fraction(1, 10) and
        energy_ratio > 1,
    }


def expected_document() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for scale, height, q0, cutoff in GROWTH_PATH:
        for exponent in (1, 2):
            rows.append(make_row(
                scale, height, q0, cutoff, exponent, "GROWTH_PATH"))
    for scale, height, q0, cutoff, exponent in CONTROL_GRID:
        rows.append(make_row(
            scale, height, q0, cutoff, exponent, "SOURCE_CONTROL_GRID"))
    need(len(rows) == 34, "row count")
    rank_rows = [row for row in rows if row["operator_rank_audited"]]
    payload = {
        "schema": SCHEMA,
        "parent_lock": parent_lock(),
        "exact_theorem": {
            "operator_identity": "A_S=sum_{q in S} A_q",
            "output_identity": "g_S=sum_{q in S} g_q",
            "gram_definition": "G_{q,r}=<g_q,g_r>",
            "energy_identity": "||g_S||_2^2=1^T G 1",
            "psd_identity": "c^T G c=||sum_q c_q g_q||_2^2>=0",
            "scalar_functional_identity": "C_S=sum_q C_q",
            "active_domain": "I_active={u in I: q does not divide u for every q in S}",
            "scope": "finite shell, frozen source, and literal deleted-diagonal operator",
        },
        "grid": {
            "growth_path": [list(item) for item in GROWTH_PATH],
            "control_grid_rows": 18, "control_heights": [48, 50, 52],
            "control_cutoffs": [3, 5, 7], "control_shell_Q": 70,
            "exponents": [1, 2],
            "operator_rank_cases": [list(item)
                                     for item in sorted(OPERATOR_RANK_CASES)],
            "modulus": MODULUS,
        },
        "finite_audit": {
            "rows": 34, "growth_rows": 16, "source_control_rows": 18,
            "distinct_shell_anchors": len({row["Q"] for row in rows}),
            "max_shell_cardinality": max(row["shell_cardinality"] for row in rows),
            "gram_full_rank_rows": sum(row["gram_positive_definite"] for row in rows),
            "operator_rank_audited_rows": len(rank_rows),
            "operator_full_active_rank_rows": sum(
                row["operator_rank_mod"] == row["operator_active_dimension"]
                for row in rank_rows),
            "energy_amplified_rows": sum(row["energy_amplified"] for row in rows),
            "scalar_upper_lt_tenth_rows": sum(
                row["scalar_upper_lt_tenth"] for row in rows),
            "scalar_energy_mismatch_rows": sum(
                row["scalar_energy_mismatch"] for row in rows),
            "component_scalar_crossings": sum(
                row["component_sign_crossings"] for row in rows),
            "fixed_power_credit": 0,
            "growing_shell_theorem": "OPEN",
            "literal_arithmetic_L2": "OPEN",
        },
        "rows": rows,
        "firewall": {
            "TPC288_EXACT_OPERATOR_ADDITIVITY": "PROVED_EXACT_FINITE",
            "TPC288_EXACT_OUTPUT_GRAM_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC288_GRAM_PSD": "PROVED_EXACT_FINITE",
            "TPC288_GRAM_FULL_RANK": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC288_OPERATOR_FULL_ACTIVE_RANK":
                "NUMERICALLY_CERTIFIED_FINITE_SELECTED_ROWS",
            "TPC288_SCALAR_ENERGY_MISMATCH":
                "NUMERICALLY_CERTIFIED_FINITE_OBSTRUCTION",
            "TPC288_GROWING_SHELL_STABILITY": "OPEN",
            "TPC288_SOURCE_CONTROL_UNIFORMITY": "OPEN",
            "TPC288_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC288_FIXED_POWER_CREDIT": 0,
            "TPC288_FULL_GATE_B": "OPEN", "TPC288_TWIN_PRIME_RESULT": "NONE",
            "TPC288_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest()}


def main() -> int:
    raw = RESULT.read_bytes()
    actual = json.loads(raw)
    need(raw == canonical(actual), "result canonicality")
    expected = expected_document()
    need(actual == expected, "independent document mismatch")
    print("TPC288_INDEPENDENT_CHECK=PASS rows=34 gram_full_rank=34 "
          "operator_full_rank=6 energy_amplified=34 scalar_lt_tenth=13 "
          "mismatch=13")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC288_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
