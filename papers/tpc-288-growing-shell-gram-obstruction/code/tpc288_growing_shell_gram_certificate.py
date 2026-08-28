#!/usr/bin/env python3
"""Growing-shell Gram and full-rank certificate for TPC-288.

TPC-287 measured cancellation after applying one scalar four-block
attachment.  This release keeps the same literal physical operator, but
records the output vectors before that scalar quotient.  The exact output
Gram matrix is positive semidefinite, its rank is audited modulo a large
prime, and a selected set of active physical matrices is also audited at
full rank.  All source and operator arithmetic is rational; decimal text is
only presentation.

The shell/control grid is deliberately finite.  It is a route obstruction
and stability map, not a growing-shell or arithmetic L2 theorem.
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
PARENT287_PROJECT = ROOT / "papers/tpc-287-prime-shell-cancellation-depth"
PARENT287_CODE = PARENT287_PROJECT / (
    "code/tpc287_prime_shell_cancellation_certificate.py")
PARENT287_RESULT = PARENT287_PROJECT / "results/tpc287_certificate.json"
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

# The first five points grow the source scale and shell together.  The last
# three hold the source scale fixed and probe deeper shells, which separates
# shell growth from the scale effect instead of silently conflating them.
GROWTH_PATH = (
    (128, 24, 9, 5),
    (192, 32, 16, 5),
    (256, 38, 27, 5),
    (384, 50, 40, 5),
    (512, 58, 50, 5),
    (512, 58, 60, 5),
    (512, 58, 70, 5),
    (512, 58, 90, 5),
)

# A two-dimensional source-control grid at a shell where TPC-287 already
# showed strong scalar cancellation.  The controls are finite named probes,
# not an assertion that all admissible sources have been covered.
CONTROL_GRID = tuple(
    (384, height, 70, cutoff, exponent)
    for height in (48, 50, 52)
    for cutoff in (3, 5, 7)
    for exponent in (1, 2)
)

# Full active-matrix rank is more expensive than the scalar/Gram replay.  It
# is therefore audited on a declared six-row spine while the output Gram
# rank is checked on every row.
OPERATOR_RANK_CASES = frozenset({
    (128, 24, 9, 5, 1),
    (192, 32, 16, 5, 1),
    (256, 38, 27, 5, 1),
    (384, 50, 40, 5, 1),
    (384, 50, 70, 5, 1),
    (512, 58, 60, 5, 1),
})

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


def interval(value: object) -> tuple[Fraction, Fraction]:
    if hasattr(value, "lo") and hasattr(value, "hi"):
        lo, hi = Fraction(value.lo), Fraction(value.hi)
    else:
        need(isinstance(value, (list, tuple)) and len(value) == 2,
             "interval shape")
        lo, hi = fraction(value[0]), fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def interval_text(value: object) -> list[str]:
    lo, hi = interval(value)
    return [ENGINE.decimal_text(lo), ENGINE.decimal_text(hi)]


def parent_data() -> dict[str, Any]:
    need(digest(PARENT287_CODE.read_bytes()) == PARENT287_CODE_SHA256,
         "TPC287 code provenance")
    raw = PARENT287_RESULT.read_bytes()
    need(digest(raw) == PARENT287_RESULT_SHA256, "TPC287 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC287 result canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_"
         "NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER",
         "TPC287 status")
    payload = data.get("payload", {})
    need(payload.get("schema") ==
         "TPC287_PRIME_SHELL_CANCELLATION_CERTIFICATE_V1",
         "TPC287 schema")
    need(payload.get("finite_audit", {}).get("rows") == 84,
         "TPC287 row count")
    return data


def physical_prime_output(indices: list[int], beta: list[Fraction],
                          height: int, prime: int,
                          exponent: int) -> list[Fraction]:
    """Build one literal deleted-diagonal prime component exactly."""
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(int(u % prime == t % prime), 1)
            centered -= Fraction(1, prime - 1)
            total += (prime * ENGINE.kernel(u - t, height, exponent) *
                      centered * beta_t)
        output.append(total)
    return output


def attachment(indices: list[int], weights: list[Any],
                output: list[Fraction]) -> Any:
    """The frozen TPC-268 direct-minus-three-Haar scalar functional."""
    n = len(indices)
    need(n % 4 == 0, "four equal blocks")
    block = n // 4
    blocks = [range(k * block, (k + 1) * block) for k in range(4)]
    block_w = [sum((weights[j] for j in group),
                   ENGINE.Interval(Fraction(0))) for group in blocks]
    block_g = [sum((output[j] for j in group), Fraction(0))
               for group in blocks]
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


def abs_lower(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    if lo <= 0 <= hi:
        return Fraction(0)
    return min(abs(lo), abs(hi))


def abs_upper(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return max(abs(lo), abs(hi))


def sign_label(value: tuple[Fraction, Fraction]) -> str:
    lo, hi = value
    if hi < 0:
        return "NEGATIVE"
    if lo > 0:
        return "POSITIVE"
    return "CROSSING"


def fraction_mod(value: Fraction) -> int:
    denominator = value.denominator % MODULUS
    need(denominator != 0, "non-invertible rational denominator")
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


def active_operator_rank(indices: list[int], height: int, shell: list[int],
                         exponent: int) -> tuple[int, int]:
    """Return (active dimension, modular rank) of the aggregate operator."""
    active = [u for u in indices if all(u % prime for prime in shell)]
    matrix: list[list[int]] = []
    h_power = pow(height, 2 * exponent, MODULUS)
    for u in active:
        row: list[int] = []
        for t in active:
            if u == t:
                row.append(0)
                continue
            entry = 0
            difference = u - t
            for prime in shell:
                denominator = (height * height + difference * difference) % MODULUS
                kernel_denominator = pow(denominator, exponent, MODULUS)
                need(kernel_denominator != 0, "operator denominator modulus")
                kernel = h_power * pow(
                    kernel_denominator, MODULUS - 2, MODULUS) % MODULUS
                inverse_q = pow(prime - 1, MODULUS - 2, MODULUS)
                if u % prime == t % prime:
                    centered = (prime - 2) * inverse_q % MODULUS
                else:
                    centered = -inverse_q % MODULUS
                entry = (entry + prime * kernel * centered) % MODULUS
            row.append(entry)
        matrix.append(row)
    return len(active), rank_mod(matrix)


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, axis: str, rank_audit: bool) -> dict[str, Any]:
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    need(shell and all(prime > 2 for prime in shell), "odd prime shell")
    outputs = [physical_prime_output(indices, beta, height, prime, exponent)
               for prime in shell]
    component_intervals = [interval(attachment(indices, weights, output))
                           for output in outputs]
    shell_output = [sum((output[j] for output in outputs), Fraction(0))
                    for j in range(len(indices))]
    shell_interval = interval(attachment(indices, weights, shell_output))

    mass_lower = sum((abs_lower(value) for value in component_intervals),
                     Fraction(0))
    mass_upper = sum((abs_upper(value) for value in component_intervals),
                     Fraction(0))
    need(mass_lower > 0 and mass_upper > 0, "component scalar mass")
    shell_abs_lower = abs_lower(shell_interval)
    shell_abs_upper = abs_upper(shell_interval)
    scalar_retention_lower = shell_abs_lower / mass_upper
    scalar_retention_upper = shell_abs_upper / mass_lower

    component_energy = sum((sum(value * value for value in output)
                            for output in outputs), Fraction(0))
    shell_energy = sum(value * value for value in shell_output)
    need(component_energy > 0, "component output energy")
    energy_ratio = shell_energy / component_energy
    cross_energy = shell_energy - component_energy

    gram_rank = rank_mod(gram_matrix(outputs))
    active_count = sum(all(value % prime for prime in shell)
                       for value in indices)
    operator_active_rank: int | None = None
    operator_rank_mod: int | None = None
    if rank_audit:
        operator_active_rank, operator_rank_mod = active_operator_rank(
            indices, height, shell, exponent)
        need(operator_active_rank == active_count, "active count mismatch")

    component_records = []
    for prime, value in zip(shell, component_intervals):
        component_records.append({
            "prime": prime,
            "attachment_interval": interval_text(value),
            "absolute_lower": str(abs_lower(value)),
            "absolute_upper": str(abs_upper(value)),
            "sign": sign_label(value),
            "zero_separated": value[1] < 0 or value[0] > 0,
        })

    scalar_upper_certified = scalar_retention_upper < Fraction(1, 10)
    energy_amplified = energy_ratio > 1
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
        "active_index_count": active_count,
        "components": component_records,
        "component_sign_crossings": sum(
            record["sign"] == "CROSSING" for record in component_records),
        "component_negative": sum(
            record["sign"] == "NEGATIVE" for record in component_records),
        "shell_attachment_interval": interval_text(shell_interval),
        "shell_sign": sign_label(shell_interval),
        "component_scalar_mass_lower": str(mass_lower),
        "component_scalar_mass_upper": str(mass_upper),
        "shell_scalar_abs_lower": str(shell_abs_lower),
        "shell_scalar_abs_upper": str(shell_abs_upper),
        "scalar_retention_lower": str(scalar_retention_lower),
        "scalar_retention_upper": str(scalar_retention_upper),
        "scalar_retention_upper_decimal": ENGINE.decimal_text(
            scalar_retention_upper),
        "scalar_upper_lt_tenth": scalar_upper_certified,
        "component_energy": str(component_energy),
        "shell_energy": str(shell_energy),
        "cross_energy": str(cross_energy),
        "energy_ratio": str(energy_ratio),
        "energy_ratio_decimal": ENGINE.decimal_text(energy_ratio),
        "energy_amplified": energy_amplified,
        "gram_dimension": len(shell),
        "gram_rank_mod": gram_rank,
        "gram_positive_definite": gram_rank == len(shell),
        "operator_rank_audited": rank_audit,
        "operator_active_dimension": operator_active_rank,
        "operator_rank_mod": operator_rank_mod,
        "scalar_energy_mismatch": scalar_upper_certified and energy_amplified,
    }


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for scale, height, q0, cutoff in GROWTH_PATH:
        for exponent in (1, 2):
            rows.append(build_row(
                scale, height, q0, cutoff, exponent, "GROWTH_PATH",
                (scale, height, q0, cutoff, exponent) in OPERATOR_RANK_CASES))
    for scale, height, q0, cutoff, exponent in CONTROL_GRID:
        rows.append(build_row(
            scale, height, q0, cutoff, exponent, "SOURCE_CONTROL_GRID",
            (scale, height, q0, cutoff, exponent) in OPERATOR_RANK_CASES))

    need(len(rows) == 34, "row census")
    need(all(row["gram_rank_mod"] == row["gram_dimension"] for row in rows),
         "Gram full-rank census")
    rank_rows = [row for row in rows if row["operator_rank_audited"]]
    need(len(rank_rows) == len(OPERATOR_RANK_CASES), "operator audit census")
    need(all(row["operator_rank_mod"] == row["operator_active_dimension"]
             for row in rank_rows), "operator full-rank census")
    mismatches = [row for row in rows if row["scalar_energy_mismatch"]]
    need(len(mismatches) >= 2, "scalar-energy obstruction census")
    amplified = [row for row in rows if row["energy_amplified"]]
    need(len(amplified) >= 20, "energy amplification census")

    growth_rows = [row for row in rows if row["axis"] == "GROWTH_PATH"]
    control_rows = [row for row in rows
                    if row["axis"] == "SOURCE_CONTROL_GRID"]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc287_code_sha256": PARENT287_CODE_SHA256,
            "tpc287_result_sha256": PARENT287_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "tpc287_rows": parent["payload"]["finite_audit"]["rows"],
        },
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
            "control_grid_rows": len(CONTROL_GRID),
            "control_heights": [48, 50, 52],
            "control_cutoffs": [3, 5, 7],
            "control_shell_Q": 70,
            "exponents": [1, 2],
            "operator_rank_cases": [list(item)
                                     for item in sorted(OPERATOR_RANK_CASES)],
            "modulus": MODULUS,
        },
        "finite_audit": {
            "rows": len(rows),
            "growth_rows": len(growth_rows),
            "source_control_rows": len(control_rows),
            "distinct_shell_anchors": len({row["Q"] for row in rows}),
            "max_shell_cardinality": max(row["shell_cardinality"]
                                          for row in rows),
            "gram_full_rank_rows": sum(row["gram_positive_definite"]
                                        for row in rows),
            "operator_rank_audited_rows": len(rank_rows),
            "operator_full_active_rank_rows": sum(
                row["operator_rank_mod"] == row["operator_active_dimension"]
                for row in rank_rows),
            "energy_amplified_rows": len(amplified),
            "scalar_upper_lt_tenth_rows": sum(
                row["scalar_upper_lt_tenth"] for row in rows),
            "scalar_energy_mismatch_rows": len(mismatches),
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
            "TPC288_FULL_GATE_B": "OPEN",
            "TPC288_TWIN_PRIME_RESULT": "NONE",
            "TPC288_STATUS": STATUS,
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
    print("TPC288_CERTIFICATE=PASS rows={} gram_full_rank={} "
          "operator_full_rank={} energy_amplified={} scalar_lt_tenth={} "
          "mismatch={}".format(
              audit["rows"], audit["gram_full_rank_rows"],
              audit["operator_full_active_rank_rows"],
              audit["energy_amplified_rows"],
              audit["scalar_upper_lt_tenth_rows"],
              audit["scalar_energy_mismatch_rows"]))


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
        print("TPC288_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
