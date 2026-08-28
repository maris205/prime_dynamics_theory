#!/usr/bin/env python3
"""Finite signed prime-shell cancellation certificate for TPC-287.

The preceding TPC-286 ledger split the literal physical operator into a
diagonal correction and a physical remainder.  This certificate keeps the
physical remainder fixed and expands the *outer prime shell* into individually
audited components.  It is deliberately a finite route-exploration artifact:
the shell ladder is declared in the payload and is not promoted to an
asymptotic family.

All arithmetic in the source profile, kernel, and operator is exact rational
arithmetic.  The comparison weights use the frozen interval implementation
from TPC-268.  The only numerical objects written to the certificate are
outward-rounded decimal strings and exact rational strings where a later
checker needs the latter.
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
PARENT286_PROJECT = ROOT / "papers/tpc-286-diagonal-deletion-attachment-ledger"
PARENT286_CODE = PARENT286_PROJECT / (
    "code/tpc286_diagonal_deletion_attachment_certificate.py")
PARENT286_RESULT = PARENT286_PROJECT / "results/tpc286_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc287_certificate.json"

PARENT286_CODE_SHA256 = (
    "7e0bfead06d37941ee972e42782e5917237aa7083eae37ed891bd775cc240022")
PARENT286_RESULT_SHA256 = (
    "d8f707f5a1297e6f286ed9e0c7330a90d99c699ab8c91b98d6c7c22e99078beb")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

SCHEMA = "TPC287_PRIME_SHELL_CANCELLATION_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER")
ROUND2_CLUE = "TEST_CANCELLATION_STABILITY_UNDER_GROWING_SHELL_AND_SOURCE_CONTROLS"

BASE_CASES = (
    (64, 15, 4, 4), (96, 20, 5, 4), (128, 24, 5, 4),
    (192, 32, 6, 5), (256, 38, 6, 5), (384, 50, 7, 5),
)
EXPONENTS = (1, 2)
SHELL_LADDER = (
    (3, (5,)),
    (4, (5, 7)),
    (9, (11, 13, 17)),
    (10, (11, 13, 17, 19)),
    (16, (17, 19, 23, 29, 31)),
    (22, (23, 29, 31, 37, 41, 43)),
    (27, (29, 31, 37, 41, 43, 47, 53)),
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


def shell_for(q0: int) -> list[int]:
    return [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]


def parent_data() -> dict[str, Any]:
    need(digest(PARENT286_CODE.read_bytes()) == PARENT286_CODE_SHA256,
         "TPC286 code provenance")
    raw = PARENT286_RESULT.read_bytes()
    need(digest(raw) == PARENT286_RESULT_SHA256, "TPC286 result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "TPC286 result canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "PROVED_EXACT_LINEAR_DIAGONAL_DELETION_ATTACHMENT_SPLIT_PLUS_"
         "NUMERICALLY_CERTIFIED_FINITE_DIAGONAL_SENSITIVITY_LEDGER",
         "TPC286 status")
    need(data.get("payload", {}).get("schema") ==
         "TPC286_DIAGONAL_DELETION_ATTACHMENT_CERTIFICATE_V1",
         "TPC286 schema")
    need(data["payload"]["finite_audit"]["rows"] == 72,
         "TPC286 row count")
    return data


def physical_prime_output(indices: list[int], beta: list[Fraction],
                          height: int, prime: int, exponent: int) -> list[Fraction]:
    """Return the literal off-diagonal component for one prime."""
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
    """TPC-268's direct-minus-three-Haar-contrasts scalar attachment."""
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


def sign(value: tuple[Fraction, Fraction]) -> str:
    lo, hi = value
    need(hi < 0 or lo > 0, "interval crosses zero")
    return "NEGATIVE" if hi < 0 else "POSITIVE"


def abs_lower(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return -hi if hi < 0 else lo


def abs_upper(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    return max(-lo, hi)


def distance_zero(value: tuple[Fraction, Fraction]) -> Fraction:
    lo, hi = value
    if hi < 0:
        return -hi
    if lo > 0:
        return lo
    return Fraction(0)


def add_intervals(values: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    return (sum((value[0] for value in values), Fraction(0)),
            sum((value[1] for value in values), Fraction(0)))


def component_record(prime: int, value: Any) -> dict[str, Any]:
    ivalue = interval(value)
    return {
        "prime": prime,
        "attachment_interval": interval_text(ivalue),
        "sign": sign(ivalue),
        "absolute_lower": str(abs_lower(ivalue)),
        "absolute_upper": str(abs_upper(ivalue)),
        "zero_separated": True,
    }


def leave_one_out_record(prime: int, value: Any,
                        shell_sign: str) -> dict[str, Any]:
    ivalue = interval(value)
    zero = ivalue == (Fraction(0), Fraction(0))
    return {
        "omitted_prime": prime,
        "attachment_interval": interval_text(ivalue),
        "zero_remainder": zero,
        "sign": "ZERO" if zero else sign(ivalue),
        "nonzero_sign_flip": (not zero and sign(ivalue) != shell_sign),
    }


def build_row(scale: int, height: int, q0: int, cutoff: int,
              exponent: int, expected_shell: tuple[int, ...]) -> dict[str, Any]:
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    shell = shell_for(q0)
    need(tuple(shell) == expected_shell, "shell ladder mismatch")
    components: list[dict[str, Any]] = []
    component_intervals: list[tuple[Fraction, Fraction]] = []
    component_outputs: list[list[Fraction]] = []
    for prime in shell:
        output = physical_prime_output(indices, beta, height, prime, exponent)
        value = interval(attachment(indices, weights, output))
        components.append(component_record(prime, value))
        component_intervals.append(value)
        component_outputs.append(output)

    shell_output = [sum((output[j] for output in component_outputs),
                         Fraction(0)) for j in range(len(indices))]
    shell_value = interval(attachment(indices, weights, shell_output))
    component_sum = add_intervals(component_intervals)
    # The direct shell interval and the sum of component intervals are two
    # outward-rounded enclosures of the same exact scalar.  They need not have
    # identical endpoints, but the direct interval must be contained in the
    # looser sum interval (up to the engine's outward rounding).
    need(component_sum[0] <= shell_value[0] and
         component_sum[1] >= shell_value[1],
         "shell interval not contained by component sum")
    shell_sign = sign(shell_value)
    mass_lower = sum((abs_lower(value) for value in component_intervals),
                     Fraction(0))
    mass_upper = sum((abs_upper(value) for value in component_intervals),
                     Fraction(0))
    need(mass_lower > 0, "zero component mass")
    retention_lower = distance_zero(shell_value) / mass_upper
    retention_upper = abs_upper(shell_value) / mass_lower

    leave_one_out: list[dict[str, Any]] = []
    for omitted, omitted_prime in enumerate(shell):
        remainder_output = [
            sum((component_outputs[k][j] for k in range(len(shell))
                 if k != omitted), Fraction(0))
            for j in range(len(indices))
        ]
        remainder = attachment(indices, weights, remainder_output)
        leave_one_out.append(leave_one_out_record(
            omitted_prime, remainder, shell_sign))

    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": len(indices),
        "shell": shell,
        "shell_cardinality": len(shell),
        "components": components,
        "component_sum_interval": interval_text(component_sum),
        "shell_attachment_interval": interval_text(shell_value),
        "shell_sign": shell_sign,
        "all_components_zero_separated": True,
        "mixed_component_signs": len({row["sign"] for row in components}) == 2,
        "unsigned_component_mass_lower": str(mass_lower),
        "unsigned_component_mass_upper": str(mass_upper),
        "shell_absolute_lower": str(distance_zero(shell_value)),
        "shell_absolute_upper": str(abs_upper(shell_value)),
        "retention_lower": str(retention_lower),
        "retention_upper": str(retention_upper),
        "leave_one_out": leave_one_out,
        "exact_shell_component_additivity": True,
        "finite_interval_enclosure": True,
    }


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for q0, shell in SHELL_LADDER:
        for scale, height, _unused_q, cutoff in BASE_CASES:
            for exponent in EXPONENTS:
                rows.append(build_row(scale, height, q0, cutoff, exponent,
                                      shell))
    need(len(rows) == 84, "row census")
    components = [component for row in rows for component in row["components"]]
    need(len(components) == 336, "component census")
    component_negative = sum(item["sign"] == "NEGATIVE" for item in components)
    shell_negative = sum(row["shell_sign"] == "NEGATIVE" for row in rows)
    mixed = sum(row["mixed_component_signs"] for row in rows)
    by_size: dict[str, dict[str, int]] = {}
    for size in range(1, 8):
        group = [row for row in rows if row["shell_cardinality"] == size]
        by_size[str(size)] = {
            "rows": len(group),
            "mixed_sign_rows": sum(row["mixed_component_signs"] for row in group),
            "retention_upper_lt_half": sum(
                fraction(row["retention_upper"]) < Fraction(1, 2)
                for row in group),
            "retention_upper_lt_quarter": sum(
                fraction(row["retention_upper"]) < Fraction(1, 4)
                for row in group),
            "retention_upper_lt_tenth": sum(
                fraction(row["retention_upper"]) < Fraction(1, 10)
                for row in group),
        }
        need(len(group) == 12, "per-cardinality row census")
    flip_events = sum(item["nonzero_sign_flip"]
                      for row in rows for item in row["leave_one_out"])
    zero_events = sum(item["zero_remainder"]
                      for row in rows for item in row["leave_one_out"])
    same_events = 336 - flip_events - zero_events
    need((component_negative, len(components) - component_negative,
          shell_negative, len(rows) - shell_negative, mixed,
          flip_events, zero_events, same_events) ==
         (175, 161, 52, 32, 57, 48, 12, 276),
         "aggregate census")
    retention_half = sum(fraction(row["retention_upper"]) < Fraction(1, 2)
                         for row in rows)
    retention_quarter = sum(fraction(row["retention_upper"]) < Fraction(1, 4)
                            for row in rows)
    retention_tenth = sum(fraction(row["retention_upper"]) < Fraction(1, 10)
                          for row in rows)
    retention_twentieth = sum(
        fraction(row["retention_upper"]) < Fraction(1, 20) for row in rows)
    need((retention_half, retention_quarter, retention_tenth,
          retention_twentieth) == (31, 22, 8, 5), "retention census")
    weakest = min(rows, key=lambda row: fraction(row["retention_upper"]))
    strongest = max(rows, key=lambda row: fraction(row["retention_lower"]))
    parent_payload = parent["payload"]
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "tpc286_code_sha256": PARENT286_CODE_SHA256,
            "tpc286_result_sha256": PARENT286_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "tpc286_rows": parent_payload["finite_audit"]["rows"],
        },
        "finite_theorem": {
            "shell_identity": "g_shell=sum_{q in S} g_q",
            "attachment_identity": "C_shell=sum_{q in S} C_q",
            "retention_envelope":
                "dist(0,J_shell)/m_plus <= |C_shell|/sum|C_q| "
                "<= max_abs(J_shell)/m_minus",
            "scope": "finite shell, common source, and linear attachment",
            "component_sign_assumption_for_ratio": True,
        },
        "shell_ladder": [
            {"Q": q0, "primes": list(shell), "cardinality": len(shell)}
            for q0, shell in SHELL_LADDER
        ],
        "finite_audit": {
            "rows": len(rows),
            "component_intervals": len(components),
            "component_sign_separated": len(components),
            "component_negative": component_negative,
            "component_positive": len(components) - component_negative,
            "shell_negative": shell_negative,
            "shell_positive": len(rows) - shell_negative,
            "mixed_component_sign_rows": mixed,
            "same_sign_component_rows": len(rows) - mixed,
            "retention_upper_lt_half_rows": retention_half,
            "retention_upper_lt_quarter_rows": retention_quarter,
            "retention_upper_lt_tenth_rows": retention_tenth,
            "retention_upper_lt_twentieth_rows": retention_twentieth,
            "leave_one_out_same_sign_events": same_events,
            "leave_one_out_sign_flip_events": flip_events,
            "leave_one_out_zero_events": zero_events,
            "fixed_power_credit": 0,
            "growing_shell_stability": "OPEN",
            "literal_arithmetic_L2": "OPEN",
        },
        "by_shell_cardinality": by_size,
        "extremal_retention": {
            "smallest_upper": {
                "scale": weakest["scale"], "H": weakest["H"],
                "Q": weakest["Q"], "kernel_exponent": weakest["kernel_exponent"],
                "retention_upper": weakest["retention_upper"],
            },
            "largest_lower": {
                "scale": strongest["scale"], "H": strongest["H"],
                "Q": strongest["Q"], "kernel_exponent": strongest["kernel_exponent"],
                "retention_lower": strongest["retention_lower"],
            },
        },
        "rows": rows,
        "firewall": {
            "TPC287_EXACT_SHELL_ADDITIVITY": "PROVED_EXACT_FINITE",
            "TPC287_EXACT_LINEAR_ATTACHMENT_ADDITIVITY": "PROVED_EXACT_FINITE",
            "TPC287_RETENTION_ENVELOPE": "PROVED_CONDITIONAL_INTERVAL",
            "TPC287_FINITE_CANCELLATION_LEDGER": "NUMERICALLY_CERTIFIED",
            "TPC287_GROWING_SHELL_CANCELLATION": "OPEN",
            "TPC287_SOURCE_CONTROL_UNIFORMITY": "OPEN",
            "TPC287_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC287_FIXED_POWER_CREDIT": 0,
            "TPC287_FULL_GATE_B": "OPEN",
            "TPC287_TWIN_PRIME_RESULT": "NONE",
            "TPC287_STATUS": STATUS,
        },
        "upstream_structure": {
            "tpc286_schema": parent_payload["schema"],
            "tpc286_diagonal_split": "PROVED_EXACT",
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    parent = parent_data()
    payload = build_payload(parent)
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
    print("TPC287_CERTIFICATE=PASS rows={} components={} mixed={} "
          "retention_lt_half={} retention_lt_quarter={} "
          "retention_lt_tenth={} leave_flips={} leave_zero={}".format(
              audit["rows"], audit["component_intervals"],
              audit["mixed_component_sign_rows"],
              audit["retention_upper_lt_half_rows"],
              audit["retention_upper_lt_quarter_rows"],
              audit["retention_upper_lt_tenth_rows"],
              audit["leave_one_out_sign_flip_events"],
              audit["leave_one_out_zero_events"]))


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
        raise SystemExit("TPC287_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
