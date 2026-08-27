#!/usr/bin/env python3
"""Attachment ledger for the physical diagonal-deletion convention.

TPC-285 proves that the centered residue block is low rank before its diagonal
is deleted.  TPC-286 uses linearity to split the literal source attachment into
the attachment of a diagonal-including shell and the attachment of the
deleted diagonal.  The split is exact; the 72-row ledger measures how often
the diagonal term controls the finite sign and magnitude.
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
PARENT284_PROJECT = ROOT / "papers/tpc-284-admissible-source-control-atlas"
PARENT284_CODE = PARENT284_PROJECT / (
    "code/tpc284_admissible_source_control_atlas_certificate.py")
PARENT284_RESULT = PARENT284_PROJECT / "results/tpc284_certificate.json"
PARENT285_PROJECT = ROOT / "papers/tpc-285-prime-shell-residue-rank-obstruction"
PARENT285_CODE = PARENT285_PROJECT / (
    "code/tpc285_prime_shell_residue_rank_certificate.py")
PARENT285_RESULT = PARENT285_PROJECT / "results/tpc285_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc286_certificate.json"

PARENT284_CODE_SHA256 = (
    "023659e316a6b700fa2853cd630f49f0582236fcc0eff9f42ad4c1159367a573")
PARENT284_RESULT_SHA256 = (
    "0ee28073ba7b460d8ec83393738fa3686c6636d817f243705ef8b1c41699abfc")
PARENT285_CODE_SHA256 = (
    "d8934fbea2c1ff074774718f081c4c6477aa817a5c4838e029bef999315fbc6d")
PARENT285_RESULT_SHA256 = (
    "8fb2ffdaae2cbb51e3ead736706449d05ae4c895bc4194d9dd8472b76efb51f9")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
SCHEMA = "TPC286_DIAGONAL_DELETION_ATTACHMENT_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER")
ROUND2_CLUE = (
    "SEEK_SIGNED_FULL_SHELL_CANCELLATION_AFTER_DIAGONAL_ATTACHMENT_LEDGER")

BASE_CASES = (
    (64, 15, 4, 4), (96, 20, 5, 4), (128, 24, 5, 4),
    (192, 32, 6, 5), (256, 38, 6, 5), (384, 50, 7, 5),
)
EXPONENTS = (1, 2)
CONTROL_SPECS = (
    ("H_MINUS_2", -2, 0, 0), ("H_PLUS_2", 2, 0, 0),
    ("Z_MINUS_1", 0, 0, -1), ("Z_PLUS_1", 0, 0, 1),
    ("Q_MINUS_1", 0, -1, 0), ("Q_PLUS_1", 0, 1, 0),
)

spec = importlib.util.spec_from_file_location("frozen_tpc268_engine", ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen TPC-268 engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    pass


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


def interval_text(value: Any) -> list[str]:
    lo, hi = interval(value)
    return [ENGINE.decimal_text(lo), ENGINE.decimal_text(hi)]


def parent_data(path: Path, expected_hash: str, schema: str,
                status: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected_hash, "parent provenance: " + path.name)
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality: " + path.name)
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") == status, "parent status: " + path.name)
    need(data.get("payload", {}).get("schema") == schema,
         "parent schema: " + path.name)
    return data


def load_parents() -> tuple[dict[str, Any], dict[str, Any]]:
    need(digest(PARENT284_CODE.read_bytes()) == PARENT284_CODE_SHA256,
         "TPC284 code provenance")
    need(digest(PARENT285_CODE.read_bytes()) == PARENT285_CODE_SHA256,
         "TPC285 code provenance")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "engine provenance")
    atlas = parent_data(
        PARENT284_RESULT, PARENT284_RESULT_SHA256,
        "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1",
        "NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_"
        "SIGN_FLIP_OBSTRUCTION")
    rank = parent_data(
        PARENT285_RESULT, PARENT285_RESULT_SHA256,
        "TPC285_PRIME_SHELL_RESIDUE_RANK_CERTIFICATE_V1",
        "PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_"
        "FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK")
    need(atlas["payload"]["finite_theorem"]["rows"] == 72,
         "TPC284 row count")
    need(rank["payload"]["finite_audit"]["rows"] == 20,
         "TPC285 row count")
    return atlas, rank


def parent_row_map(atlas: dict[str, Any]) -> dict[tuple[int, int, int, int, int, str], dict[str, Any]]:
    result: dict[tuple[int, int, int, int, int, str], dict[str, Any]] = {}
    for row in atlas["payload"]["rows"]:
        key = (int(row["scale"]), int(row["base_H"]), int(row["base_Q"]),
               int(row["base_z"]), int(row["kernel_exponent"]),
               str(row["control"]))
        need(key not in result, "duplicate TPC284 control row")
        result[key] = row
    need(len(result) == 72, "TPC284 control map")
    return result


def full_output(indices: list[int], beta: list[Fraction], height: int,
                q0: int, exponent: int) -> list[Fraction]:
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            for prime in shell:
                if u % prime == 0 or t % prime == 0:
                    continue
                centered = Fraction(int(u % prime == t % prime), 1)
                centered -= Fraction(1, prime - 1)
                total += (prime * ENGINE.kernel(u - t, height, exponent) *
                          centered * beta_t)
        output.append(total)
    return output


def attachment(indices: list[int], weights: list[Any],
               output: list[Fraction]) -> Any:
    n = len(indices)
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


def sign(value: tuple[Fraction, Fraction]) -> str:
    lo, hi = value
    need(hi < 0 or lo > 0, "component interval crosses zero")
    return "NEGATIVE" if hi < 0 else "POSITIVE"


def abs_lower(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return -hi if hi < 0 else lo


def abs_upper(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return max(-lo, hi)


def controlled_row(parent_row: dict[str, Any], dh: int, dq: int,
                   dz: int, description: str) -> dict[str, Any]:
    scale, base_h, base_q, base_z, exponent = (
        int(parent_row["scale"]), int(parent_row["base_H"]),
        int(parent_row["base_Q"]), int(parent_row["base_z"]),
        int(parent_row["kernel_exponent"]))
    height, q0, cutoff = base_h + dh, base_q + dq, base_z + dz
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    full = full_output(indices, beta, height, q0, exponent)
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    diagonal = []
    for u, beta_u in zip(indices, beta):
        value = Fraction(0)
        for prime in shell:
            if u % prime:
                value += (prime * Fraction(prime - 2, prime - 1) * beta_u)
        diagonal.append(value)
    physical = [x - y for x, y in zip(full, diagonal)]
    c_full = interval(attachment(indices, weights, full))
    c_diag = interval(attachment(indices, weights, diagonal))
    c_phys = interval(attachment(indices, weights, physical))
    # Re-run the frozen physical audit and bind its interval to the immediate
    # control-atlas parent.  The parent interval is the canonical source row.
    frozen = ENGINE.audit_case(scale, height, q0, exponent, cutoff,
                               "TPC286_PHYSICAL_REPLAY")
    frozen_c = interval(frozen["residual_scalar_interval"])
    parent_c = interval(parent_row["source_scalar_C_interval"])
    frozen_c = interval(frozen["residual_scalar_interval"])
    need(interval(interval_text(c_phys)) == frozen_c,
         "physical replay serialization mismatch")
    need(parent_c == frozen_c,
         "TPC284 source interval mismatch")
    reconstructed = (c_full[0] - c_diag[1], c_full[1] - c_diag[0])
    need(reconstructed[0] <= c_phys[0] and reconstructed[1] >= c_phys[1],
         "component reconstruction does not contain physical interval")
    full_sign, diag_sign, phys_sign = sign(c_full), sign(c_diag), sign(c_phys)
    ratio_lower = abs_lower(c_diag) / abs_upper(c_phys)
    return {
        "scale": scale, "base_H": base_h, "base_Q": base_q,
        "base_z": base_z, "H": height, "Q": q0,
        "comparison_cutoff_z": cutoff, "kernel_exponent": exponent,
        "control": str(parent_row["control"]),
        "control_description": description,
        "source_scalar_full_including_diagonal_interval": interval_text(c_full),
        "source_scalar_diagonal_deleted_correction_interval": interval_text(c_diag),
        "source_scalar_physical_interval": interval_text(c_phys),
        "source_scalar_reconstructed_interval": [str(reconstructed[0]),
                                                   str(reconstructed[1])],
        "full_including_diagonal_sign": full_sign,
        "diagonal_correction_sign": diag_sign,
        "physical_deleted_diagonal_sign": phys_sign,
        "diagonal_opposes_physical": diag_sign != phys_sign,
        "full_vs_physical_sign_flip": full_sign != phys_sign,
        "diagonal_magnitude_strictly_exceeds_physical":
            abs_lower(c_diag) > abs_upper(c_phys),
        "diagonal_to_physical_absolute_ratio_lower": str(ratio_lower),
        "diagonal_ratio_lower_exceeds_2": ratio_lower > 2,
        "diagonal_ratio_lower_exceeds_10": ratio_lower > 10,
        "linearity_reconstruction_certified": True,
        "physical_literal_operator_replayed": True,
    }


def build_payload(atlas: dict[str, Any], rank: dict[str, Any]) -> dict[str, Any]:
    mapping = parent_row_map(atlas)
    descriptions = {name: description for name, _, _, _, description in (
        (name, dh, dq, dz, "") for name, dh, dq, dz in CONTROL_SPECS)}
    # Keep descriptions deterministic even though they do not affect arithmetic.
    descriptions.update({
        "H_MINUS_2": "clock height H decreased by 2",
        "H_PLUS_2": "clock height H increased by 2",
        "Z_MINUS_1": "comparison cutoff z decreased by 1",
        "Z_PLUS_1": "comparison cutoff z increased by 1",
        "Q_MINUS_1": "prime-shell lower endpoint Q decreased by 1",
        "Q_PLUS_1": "prime-shell lower endpoint Q increased by 1",
    })
    rows: list[dict[str, Any]] = []
    for scale, height, q0, cutoff in BASE_CASES:
        for exponent in EXPONENTS:
            for name, dh, dq, dz in CONTROL_SPECS:
                key = (scale, height, q0, cutoff, exponent, name)
                need(key in mapping, "missing TPC284 row")
                rows.append(controlled_row(
                    mapping[key], dh, dq, dz, descriptions[name]))
    need(len(rows) == 72, "row census")
    full_negative = sum(row["full_including_diagonal_sign"] == "NEGATIVE"
                        for row in rows)
    diag_negative = sum(row["diagonal_correction_sign"] == "NEGATIVE"
                        for row in rows)
    physical_negative = sum(row["physical_deleted_diagonal_sign"] == "NEGATIVE"
                            for row in rows)
    full_flip = sum(row["full_vs_physical_sign_flip"] for row in rows)
    opposing = sum(row["diagonal_opposes_physical"] for row in rows)
    dominates = sum(row["diagonal_magnitude_strictly_exceeds_physical"]
                    for row in rows)
    above_two = sum(row["diagonal_ratio_lower_exceeds_2"] for row in rows)
    above_ten = sum(row["diagonal_ratio_lower_exceeds_10"] for row in rows)
    need((full_negative, diag_negative, physical_negative) == (49, 34, 60),
         "component sign census")
    need((full_flip, opposing, dominates, above_two, above_ten) ==
         (15, 30, 21, 13, 4), "component sensitivity census")
    weakest = min(rows, key=lambda row: fraction(
        row["diagonal_to_physical_absolute_ratio_lower"]))
    strongest = max(rows, key=lambda row: fraction(
        row["diagonal_to_physical_absolute_ratio_lower"]))
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc284_code_sha256": PARENT284_CODE_SHA256,
            "tpc284_result_sha256": PARENT284_RESULT_SHA256,
            "tpc285_code_sha256": PARENT285_CODE_SHA256,
            "tpc285_result_sha256": PARENT285_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "tpc284_control_rows": 72,
            "tpc285_rank_rows": 20,
        },
        "exact_theorem": {
            "full_operator": "A_full=sum_q q(K_H o B_q)",
            "physical_operator": "A_phys=A_full-Delta_diag",
            "diagonal_output":
                "Delta_diag(u)=sum_{q in shell} q K_H(0)(q-2)/(q-1) m_q(u) beta(u)",
            "attachment_split": "C_phys=C_full-C_diag",
            "scope": "exact linear decomposition for the declared finite source model",
        },
        "finite_audit": {
            "rows": 72,
            "full_including_diagonal_negative_rows": full_negative,
            "full_including_diagonal_positive_rows": len(rows) - full_negative,
            "diagonal_correction_negative_rows": diag_negative,
            "diagonal_correction_positive_rows": len(rows) - diag_negative,
            "physical_negative_rows": physical_negative,
            "physical_positive_rows": len(rows) - physical_negative,
            "component_sign_separated_rows": 72,
            "reconstruction_contained_rows": 72,
            "full_vs_physical_sign_flip_rows": full_flip,
            "diagonal_opposes_physical_rows": opposing,
            "diagonal_strictly_dominates_physical_rows": dominates,
            "diagonal_ratio_lower_exceeds_2_rows": above_two,
            "diagonal_ratio_lower_exceeds_10_rows": above_ten,
            "fixed_power_credit": 0,
            "asymptotic_diagonal_dominance": "OPEN",
        },
        "extremal_ratios": {
            "smallest_lower_ratio": {
                "scale": weakest["scale"], "kernel_exponent": weakest["kernel_exponent"],
                "control": weakest["control"],
                "interval_lower": weakest["diagonal_to_physical_absolute_ratio_lower"],
            },
            "largest_lower_ratio": {
                "scale": strongest["scale"], "kernel_exponent": strongest["kernel_exponent"],
                "control": strongest["control"],
                "interval_lower": strongest["diagonal_to_physical_absolute_ratio_lower"],
            },
        },
        "rows": rows,
        "firewall": {
            "TPC286_ATTACHMENT_SPLIT": "PROVED_EXACT_LINEARITY",
            "TPC286_COMPONENT_SIGN_LEDGER": "NUMERICALLY_CERTIFIED_FINITE_72_ROWS",
            "TPC286_FULL_VS_PHYSICAL_FLIPS": "NUMERICALLY_CERTIFIED_FINITE_15_ROWS",
            "TPC286_DIAGONAL_OPPOSITION": "NUMERICALLY_CERTIFIED_FINITE_30_ROWS",
            "TPC286_DIAGONAL_DOMINANCE": "NUMERICALLY_CERTIFIED_FINITE_21_ROWS",
            "TPC286_ASYMPTOTIC_DIAGONAL_DOMINANCE": "OPEN",
            "TPC286_SIGNED_FULL_SHELL_CANCELLATION": "OPEN",
            "TPC286_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC286_FIXED_POWER_CREDIT": 0,
            "TPC286_FULL_GATE_B": "OPEN",
            "TPC286_TWIN_PRIME_RESULT": "NONE",
            "TPC286_STATUS": STATUS,
        },
        "upstream_rank_structure": {
            "schema": rank["payload"]["schema"],
            "finite_rows": rank["payload"]["finite_audit"]["rows"],
            "deleted_diagonal_theorem": "PROVED_EXACT",
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    atlas, rank = load_parents()
    payload = build_payload(atlas, rank)
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
    print("TPC286_CERTIFICATE=PASS rows=72 full_negative=49 "
          "diagonal_negative=34 physical_negative=60 full_physical_flips=15 "
          "diagonal_opposes=30 diagonal_dominates=21 fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC286_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
