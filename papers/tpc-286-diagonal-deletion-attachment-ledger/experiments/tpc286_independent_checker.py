#!/usr/bin/env python3
"""Independent replay of the TPC-286 diagonal-deletion attachment ledger.

This checker deliberately does not import the TPC-286 producer.  It rebuilds
the three source outputs, their four-block scalar attachment, and all finite
classifications from the frozen TPC-268 engine and the locked TPC-284 parent
certificate.  The exact linear split is checked before the serialized result
is compared with the producer's certificate.
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
PROJECT = ROOT / "papers/tpc-286-diagonal-deletion-attachment-ledger"
PARENT284 = ROOT / (
    "papers/tpc-284-admissible-source-control-atlas/results/"
    "tpc284_certificate.json")
PARENT285 = ROOT / (
    "papers/tpc-285-prime-shell-residue-rank-obstruction/results/"
    "tpc285_certificate.json")
ENGINE_PATH = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc286_certificate.json"

PARENT284_SHA256 = (
    "0ee28073ba7b460d8ec83393738fa3686c6636d817f243705ef8b1c41699abfc")
PARENT285_SHA256 = (
    "8fb2ffdaae2cbb51e3ead736706449d05ae4c895bc4194d9dd8472b76efb51f9")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
RESULT_SHA256 = (
    "d8f707f5a1297e6f286ed9e0c7330a90d99c699ab8c91b98d6c7c22e99078beb")
STATUS = (
    "PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER")
SCHEMA = "TPC286_DIAGONAL_DELETION_ATTACHMENT_CERTIFICATE_V1"

BASE_CASES = (
    (64, 15, 4, 4), (96, 20, 5, 4), (128, 24, 5, 4),
    (192, 32, 6, 5), (256, 38, 6, 5), (384, 50, 7, 5),
)
EXPONENTS = (1, 2)
CONTROLS = (
    ("H_MINUS_2", -2, 0, 0), ("H_PLUS_2", 2, 0, 0),
    ("Z_MINUS_1", 0, 0, -1), ("Z_PLUS_1", 0, 0, 1),
    ("Q_MINUS_1", 0, -1, 0), ("Q_PLUS_1", 0, 1, 0),
)

spec = importlib.util.spec_from_file_location("frozen_tpc268_engine", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("TPC286_INDEPENDENT_CHECK=FAIL engine unavailable")
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


def as_fraction(value: object) -> Fraction:
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int) and not isinstance(value, bool):
        return Fraction(value)
    need(isinstance(value, str), "fraction representation")
    return Fraction(value)


def bounds(value: object) -> tuple[Fraction, Fraction]:
    if hasattr(value, "lo") and hasattr(value, "hi"):
        lo, hi = Fraction(value.lo), Fraction(value.hi)
    else:
        need(isinstance(value, (list, tuple)) and len(value) == 2,
             "interval representation")
        lo, hi = as_fraction(value[0]), as_fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def serialized(value: object) -> tuple[Fraction, Fraction]:
    lo, hi = bounds(value)
    return (Fraction(ENGINE.decimal_text(lo)),
            Fraction(ENGINE.decimal_text(hi)))


def load_json(path: Path, expected_hash: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, "provenance: " + path.name)
    data = json.loads(raw)
    need(raw == canonical(data), "canonical JSON: " + path.name)
    return data


def shell(q0: int) -> list[int]:
    values: list[int] = []
    for candidate in range(q0 + 1, 2 * q0 + 1):
        if candidate < 2:
            continue
        prime = True
        divisor = 2
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:
                prime = False
                break
            divisor += 1
        if prime:
            values.append(candidate)
    return values


def full_output(indices: list[int], beta: list[Fraction], height: int,
                q0: int, exponent: int) -> list[Fraction]:
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            for prime in shell(q0):
                if u % prime == 0 or t % prime == 0:
                    continue
                residue = Fraction(int(u % prime == t % prime), 1)
                residue -= Fraction(1, prime - 1)
                total += (prime * ENGINE.kernel(u - t, height, exponent)
                          * residue * beta_t)
        output.append(total)
    return output


def diagonal_output(indices: list[int], beta: list[Fraction], q0: int
                    ) -> list[Fraction]:
    output: list[Fraction] = []
    for u, beta_u in zip(indices, beta):
        total = Fraction(0)
        for prime in shell(q0):
            if u % prime:
                total += prime * Fraction(prime - 2, prime - 1) * beta_u
        output.append(total)
    return output


def attachment(indices: list[int], weights: list[Any],
               output: list[Fraction]) -> tuple[Fraction, Fraction]:
    n = len(indices)
    block = n // 4
    groups = [range(k * block, (k + 1) * block) for k in range(4)]
    block_w = [sum((weights[j] for j in group),
                   ENGINE.Interval(Fraction(0))) for group in groups]
    block_g = [sum((output[j] for j in group), Fraction(0))
               for group in groups]
    direct = sum((weights[j] * output[j] for j in range(n)),
                 ENGINE.Interval(Fraction(0)))
    projected = ENGINE.Interval(Fraction(0))
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    for coefficients, denominator in zip(contrasts, denominators):
        w_contrast = sum((block_w[k] * coefficients[k]
                          for k in range(4)), ENGINE.Interval(Fraction(0)))
        g_contrast = sum((block_g[k] * coefficients[k]
                          for k in range(4)), Fraction(0))
        projected += w_contrast * g_contrast / Fraction(denominator)
    result = direct - projected
    return Fraction(result.lo), Fraction(result.hi)


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int, str]:
    return (int(row["scale"]), int(row["base_H"]), int(row["base_Q"]),
            int(row["base_z"]), int(row["kernel_exponent"]),
            str(row["control"]))


def sign(value: tuple[Fraction, Fraction]) -> str:
    lo, hi = value
    need(hi < 0 or lo > 0, "component crosses zero")
    return "NEGATIVE" if hi < 0 else "POSITIVE"


def abs_lower(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return -hi if hi < 0 else lo


def abs_upper(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return max(-lo, hi)


def check_row(row: dict[str, Any], parent: dict[str, Any]) -> tuple[str, str, str,
                                                                    bool, bool, bool,
                                                                    bool, bool]:
    scale, base_h, base_q, base_z, exponent, control = row_key(row)
    controls = {item[0]: item[1:] for item in CONTROLS}
    need(control in controls, "control name")
    dh, dq, dz = controls[control]
    height, q0, cutoff = base_h + dh, base_q + dq, base_z + dz
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    full = full_output(indices, beta, height, q0, exponent)
    diagonal = diagonal_output(indices, beta, q0)
    physical = [x - y for x, y in zip(full, diagonal)]
    c_full = attachment(indices, weights, full)
    c_diag = attachment(indices, weights, diagonal)
    c_phys = attachment(indices, weights, physical)
    reconstructed = (c_full[0] - c_diag[1], c_full[1] - c_diag[0])
    need(reconstructed[0] <= c_phys[0] and reconstructed[1] >= c_phys[1],
         "exact reconstruction containment")

    stored_full = bounds(row["source_scalar_full_including_diagonal_interval"])
    stored_diag = bounds(row["source_scalar_diagonal_deleted_correction_interval"])
    stored_phys = bounds(row["source_scalar_physical_interval"])
    need(serialized(c_full) == stored_full, "full interval")
    need(serialized(c_diag) == stored_diag, "diagonal interval")
    need(serialized(c_phys) == stored_phys, "physical interval")
    need(bounds(row["source_scalar_reconstructed_interval"]) == reconstructed,
         "reconstructed interval")

    frozen = ENGINE.audit_case(scale, height, q0, exponent, cutoff,
                               "TPC286_INDEPENDENT_REPLAY")
    frozen_bounds = bounds(frozen["residual_scalar_interval"])
    parent_bounds = bounds(parent["source_scalar_C_interval"])
    need(serialized(c_phys) == frozen_bounds, "frozen physical replay")
    need(parent_bounds == frozen_bounds, "parent physical replay")

    full_sign, diag_sign, phys_sign = sign(c_full), sign(c_diag), sign(c_phys)
    ratio = abs_lower(c_diag) / abs_upper(c_phys)
    need(row["full_including_diagonal_sign"] == full_sign,
         "full sign")
    need(row["diagonal_correction_sign"] == diag_sign, "diagonal sign")
    need(row["physical_deleted_diagonal_sign"] == phys_sign,
         "physical sign")
    need(row["diagonal_to_physical_absolute_ratio_lower"] == str(ratio),
         "ratio")
    flip = full_sign != phys_sign
    oppose = diag_sign != phys_sign
    dominate = abs_lower(c_diag) > abs_upper(c_phys)
    above_two, above_ten = ratio > 2, ratio > 10
    need(row["full_vs_physical_sign_flip"] is flip, "flip flag")
    need(row["diagonal_opposes_physical"] is oppose, "opposition flag")
    need(row["diagonal_magnitude_strictly_exceeds_physical"] is dominate,
         "dominance flag")
    need(row["diagonal_ratio_lower_exceeds_2"] is above_two,
         "ratio-2 flag")
    need(row["diagonal_ratio_lower_exceeds_10"] is above_ten,
         "ratio-10 flag")
    need(row["linearity_reconstruction_certified"] is True and
         row["physical_literal_operator_replayed"] is True,
         "row certification flags")
    return (full_sign, diag_sign, phys_sign, flip, oppose, dominate,
            above_two, above_ten)


def check() -> None:
    need(digest(ENGINE_PATH.read_bytes()) == ENGINE_SHA256, "engine hash")
    p284 = load_json(PARENT284, PARENT284_SHA256)
    p285 = load_json(PARENT285, PARENT285_SHA256)
    need(p284["payload"]["schema"] ==
         "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1",
         "TPC284 schema")
    need(p285["payload"]["schema"] ==
         "TPC285_PRIME_SHELL_RESIDUE_RANK_CERTIFICATE_V1",
         "TPC285 schema")
    need(len(p284["payload"]["rows"]) == 72 and
         p285["payload"]["finite_audit"]["rows"] == 20,
         "parent census")
    parent_map = {row_key(row): row for row in p284["payload"]["rows"]}
    need(len(parent_map) == 72, "parent key uniqueness")

    data = load_json(RESULT, RESULT_SHA256)
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "result header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA and
         data["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(),
         "result payload hash")
    rows = payload["rows"]
    need(len(rows) == 72, "result row count")
    expected = {(scale, h, q, z, exponent, control)
                for scale, h, q, z in BASE_CASES
                for exponent in EXPONENTS
                for control, _, _, _ in CONTROLS}
    actual = {row_key(row) for row in rows}
    need(actual == expected, "result key census")
    need(set(parent_map) == expected, "parent key census")

    totals = [0] * 8
    for row in rows:
        values = check_row(row, parent_map[row_key(row)])
        totals[0] += int(values[0] == "NEGATIVE")
        totals[1] += int(values[1] == "NEGATIVE")
        totals[2] += int(values[2] == "NEGATIVE")
        for index, value in enumerate(values[3:], start=3):
            totals[index] += int(value)
    need(tuple(totals) == (49, 34, 60, 15, 30, 21, 13, 4),
         "independent census")
    need(payload["finite_audit"] == {
        "asymptotic_diagonal_dominance": "OPEN",
        "component_sign_separated_rows": 72,
        "diagonal_correction_negative_rows": 34,
        "diagonal_correction_positive_rows": 38,
        "diagonal_opposes_physical_rows": 30,
        "diagonal_ratio_lower_exceeds_10_rows": 4,
        "diagonal_ratio_lower_exceeds_2_rows": 13,
        "diagonal_strictly_dominates_physical_rows": 21,
        "fixed_power_credit": 0,
        "full_including_diagonal_negative_rows": 49,
        "full_including_diagonal_positive_rows": 23,
        "full_vs_physical_sign_flip_rows": 15,
        "physical_negative_rows": 60,
        "physical_positive_rows": 12,
        "reconstruction_contained_rows": 72,
        "rows": 72,
    }, "finite audit census")
    print("TPC286_INDEPENDENT_CHECK=PASS rows=72 full_negative=49 "
          "diagonal_negative=34 physical_negative=60 full_physical_flips=15 "
          "diagonal_opposes=30 diagonal_dominates=21 fixed_power_credit=0")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC286_INDEPENDENT_CHECK=FAIL: " + str(error))
