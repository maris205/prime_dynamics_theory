#!/usr/bin/env python3
"""Independent replay of the TPC-287 finite shell ledger.

This file intentionally does not import the producer.  It rebuilds the prime
list by trial division, forms one deleted-diagonal component at a time, and
recomputes the four-block attachment and all census fields.  The frozen
TPC-268 engine is used only as the locked source-profile/kernel provider; the
shell enumeration, component regrouping, and certificate comparison are
implemented independently here.
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
PROJECT = ROOT / "papers/tpc-287-prime-shell-cancellation-depth"
ENGINE_PATH = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
PARENT286 = ROOT / (
    "papers/tpc-286-diagonal-deletion-attachment-ledger/results/"
    "tpc286_certificate.json")
RESULT = PROJECT / "results/tpc287_certificate.json"

ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
PARENT286_SHA256 = (
    "d8f707f5a1297e6f286ed9e0c7330a90d99c699ab8c91b98d6c7c22e99078beb")
RESULT_SHA256 = (
    "a72dd15e4b2977c04d3cba81b4f02d5736d9d8dcab6fcf7c8661d45ddc1fee30")
SCHEMA = "TPC287_PRIME_SHELL_CANCELLATION_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_FINITE_SHELL_ADDITIVE_ATTACHMENT_DECOMPOSITION_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_CANCELLATION_DEPTH_LEDGER")

BASE_CASES = (
    (64, 15, 4), (96, 20, 4), (128, 24, 4),
    (192, 32, 5), (256, 38, 5), (384, 50, 5),
)
EXPONENTS = (1, 2)
LADDER = (
    (3, (5,)), (4, (5, 7)), (9, (11, 13, 17)),
    (10, (11, 13, 17, 19)), (16, (17, 19, 23, 29, 31)),
    (22, (23, 29, 31, 37, 41, 43)),
    (27, (29, 31, 37, 41, 43, 47, 53)),
)

spec = importlib.util.spec_from_file_location("locked_tpc268_engine", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("TPC287_INDEPENDENT_CHECK=FAIL engine unavailable")
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
    need(isinstance(value, (list, tuple)) and len(value) == 2,
         "interval representation")
    result = (as_fraction(value[0]), as_fraction(value[1]))
    need(result[0] <= result[1], "interval order")
    return result


def serialized(value: object) -> tuple[Fraction, Fraction]:
    lo, hi = bounds(value)
    return Fraction(ENGINE.decimal_text(lo)), Fraction(ENGINE.decimal_text(hi))


def load_json(path: Path, expected: str) -> dict[str, Any]:
    raw = path.read_bytes()
    need(digest(raw) == expected, "provenance: " + path.name)
    data = json.loads(raw)
    need(raw == canonical(data), "canonical JSON: " + path.name)
    return data


def primes_in_shell(lower: int) -> list[int]:
    values: list[int] = []
    for candidate in range(lower + 1, 2 * lower + 1):
        if candidate < 2:
            continue
        divisor = 2
        prime = True
        while divisor * divisor <= candidate:
            if candidate % divisor == 0:
                prime = False
                break
            divisor += 1
        if prime:
            values.append(candidate)
    return values


def physical_component(indices: list[int], beta: list[Fraction], height: int,
                       prime: int, exponent: int) -> list[Fraction]:
    output: list[Fraction] = []
    for u in indices:
        total = Fraction(0)
        for t, beta_t in zip(indices, beta):
            if u == t or u % prime == 0 or t % prime == 0:
                continue
            centered = Fraction(1 if u % prime == t % prime else 0)
            centered -= Fraction(1, prime - 1)
            total += prime * ENGINE.kernel(u - t, height, exponent) \
                * centered * beta_t
        output.append(total)
    return output


def attach(indices: list[int], weights: list[Any], output: list[Fraction]
           ) -> tuple[Fraction, Fraction]:
    n = len(indices)
    need(n % 4 == 0, "balanced blocks")
    size = n // 4
    groups = [range(k * size, (k + 1) * size) for k in range(4)]
    w_blocks = [sum((weights[j] for j in group),
                    ENGINE.Interval(Fraction(0))) for group in groups]
    g_blocks = [sum((output[j] for j in group), Fraction(0))
                for group in groups]
    direct = sum((weights[j] * output[j] for j in range(n)),
                 ENGINE.Interval(Fraction(0)))
    projected = ENGINE.Interval(Fraction(0))
    for coefficients, denominator in zip(
            ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1)),
            (4 * size, 2 * size, 2 * size)):
        w_contrast = sum((w_blocks[k] * coefficients[k]
                          for k in range(4)),
                         ENGINE.Interval(Fraction(0)))
        g_contrast = sum((g_blocks[k] * coefficients[k]
                          for k in range(4)), Fraction(0))
        projected += w_contrast * g_contrast / Fraction(denominator)
    answer = direct - projected
    return Fraction(answer.lo), Fraction(answer.hi)


def interval_sum(values: list[tuple[Fraction, Fraction]]) -> tuple[Fraction, Fraction]:
    return (sum((value[0] for value in values), Fraction(0)),
            sum((value[1] for value in values), Fraction(0)))


def sign(value: tuple[Fraction, Fraction]) -> str:
    lo, hi = value
    need(hi < 0 or lo > 0, "unexpected zero crossing")
    return "NEGATIVE" if hi < 0 else "POSITIVE"


def abs_lo(value: tuple[Fraction, Fraction]) -> Fraction:
    return -value[1] if value[1] < 0 else value[0]


def abs_hi(value: tuple[Fraction, Fraction]) -> Fraction:
    return max(-value[0], value[1])


def dist_zero(value: tuple[Fraction, Fraction]) -> Fraction:
    if value[1] < 0:
        return -value[1]
    if value[0] > 0:
        return value[0]
    return Fraction(0)


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


def replay_row(row: dict[str, Any], shell: tuple[int, ...]) -> tuple[int, int, int, int]:
    scale, height, q0, cutoff, exponent = row_key(row)
    need(tuple(row["shell"]) == shell and tuple(primes_in_shell(q0)) == shell,
         "shell row")
    need(row["shell_cardinality"] == len(shell), "shell cardinality")
    indices, beta, weights = ENGINE.source_weights(scale, cutoff)
    values: list[tuple[Fraction, Fraction]] = []
    outputs: list[list[Fraction]] = []
    for stored, prime in zip(row["components"], shell):
        need(stored["prime"] == prime and stored["zero_separated"] is True,
             "component header")
        output = physical_component(indices, beta, height, prime, exponent)
        value = attach(indices, weights, output)
        values.append(value)
        outputs.append(output)
        need(serialized(value) == bounds(stored["attachment_interval"]),
             "component interval")
        need(stored["sign"] == sign(value), "component sign")
        need(stored["absolute_lower"] == str(abs_lo(value)),
             "component lower mass")
        need(stored["absolute_upper"] == str(abs_hi(value)),
             "component upper mass")

    shell_output = [sum((output[j] for output in outputs), Fraction(0))
                    for j in range(len(indices))]
    shell_value = attach(indices, weights, shell_output)
    sum_value = interval_sum(values)
    need(serialized(sum_value) == bounds(row["component_sum_interval"]),
         "component sum interval")
    need(serialized(shell_value) == bounds(row["shell_attachment_interval"]),
         "shell interval")
    need(sum_value[0] <= shell_value[0] and sum_value[1] >= shell_value[1],
         "shell containment")
    shell_sign = sign(shell_value)
    need(row["shell_sign"] == shell_sign and
         row["all_components_zero_separated"] is True,
         "shell flags")
    mixed = len({sign(value) for value in values}) == 2
    need(row["mixed_component_signs"] is mixed, "mixed flag")
    lower_mass = sum((abs_lo(value) for value in values), Fraction(0))
    upper_mass = sum((abs_hi(value) for value in values), Fraction(0))
    lower_retention = dist_zero(shell_value) / upper_mass
    upper_retention = abs_hi(shell_value) / lower_mass
    need(row["unsigned_component_mass_lower"] == str(lower_mass) and
         row["unsigned_component_mass_upper"] == str(upper_mass),
         "unsigned mass")
    need(row["shell_absolute_lower"] == str(dist_zero(shell_value)) and
         row["shell_absolute_upper"] == str(abs_hi(shell_value)),
         "shell mass")
    need(row["retention_lower"] == str(lower_retention) and
         row["retention_upper"] == str(upper_retention),
         "retention")

    expected_leave = row["leave_one_out"]
    need(len(expected_leave) == len(shell), "leave-out length")
    for omit, prime in enumerate(shell):
        remainder = [
            sum((outputs[k][j] for k in range(len(shell)) if k != omit),
                Fraction(0)) for j in range(len(indices))
        ]
        remainder_value = attach(indices, weights, remainder)
        stored = expected_leave[omit]
        zero = remainder_value == (Fraction(0), Fraction(0))
        need(stored["omitted_prime"] == prime and
             serialized(remainder_value) ==
             bounds(stored["attachment_interval"]) and
             stored["zero_remainder"] is zero,
             "leave-out value")
        stored_sign = "ZERO" if zero else sign(remainder_value)
        flip = not zero and stored_sign != shell_sign
        need(stored["sign"] == stored_sign and
             stored["nonzero_sign_flip"] is flip,
             "leave-out sign")
    return (int(mixed), int(shell_sign == "NEGATIVE"),
            sum(item["nonzero_sign_flip"] for item in expected_leave),
            sum(item["zero_remainder"] for item in expected_leave))


def check() -> None:
    need(digest(ENGINE_PATH.read_bytes()) == ENGINE_SHA256, "engine hash")
    parent = load_json(PARENT286, PARENT286_SHA256)
    need(parent["payload"]["schema"] ==
         "TPC286_DIAGONAL_DELETION_ATTACHMENT_CERTIFICATE_V1",
         "parent schema")
    data = load_json(RESULT, RESULT_SHA256)
    need(data["certificate_version"] == 1 and
         data["claim_status"] == STATUS,
         "result header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA and
         data["payload_sha256"] == hashlib.sha256(canonical(payload)).hexdigest(),
         "result schema/hash")
    expected_keys = {
        (scale, height, q0, cutoff, exponent)
        for scale, height, cutoff in BASE_CASES
        for q0, _shell in LADDER for exponent in EXPONENTS
    }
    rows = payload["rows"]
    need(len(rows) == 84 and {row_key(row) for row in rows} == expected_keys,
         "row key census")
    ladder = {int(item["Q"]): tuple(item["primes"])
              for item in payload["shell_ladder"]}
    need(ladder == {q0: shell for q0, shell in LADDER}, "ladder payload")
    mixed = negative_shell = flips = zeros = 0
    components = 0
    component_negative = 0
    for row in rows:
        values = replay_row(row, ladder[int(row["Q"])])
        mixed += values[0]
        negative_shell += values[1]
        flips += values[2]
        zeros += values[3]
        components += len(row["components"])
        component_negative += sum(item["sign"] == "NEGATIVE"
                                  for item in row["components"])
    need((components, component_negative, negative_shell, mixed, flips, zeros)
         == (336, 175, 52, 57, 48, 12), "replayed aggregate")
    audit = payload["finite_audit"]
    need(audit["rows"] == 84 and audit["component_intervals"] == 336 and
         audit["component_sign_separated"] == 336 and
         audit["component_negative"] == 175 and
         audit["component_positive"] == 161 and
         audit["shell_negative"] == 52 and audit["shell_positive"] == 32 and
         audit["mixed_component_sign_rows"] == 57 and
         audit["same_sign_component_rows"] == 27 and
         audit["leave_one_out_same_sign_events"] == 276 and
         audit["leave_one_out_sign_flip_events"] == 48 and
         audit["leave_one_out_zero_events"] == 12,
         "finite audit")
    thresholds = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 10),
                  Fraction(1, 20))
    observed = [sum(as_fraction(row["retention_upper"]) < threshold
                    for row in rows) for threshold in thresholds]
    need(observed == [31, 22, 8, 5], "retention threshold census")
    print("TPC287_INDEPENDENT_CHECK=PASS rows=84 components=336 "
          "mixed=57 component_negative=175 shell_negative=52 "
          "retention_lt_half=31 retention_lt_quarter=22 "
          "retention_lt_tenth=8 leave_flips=48 leave_zero=12")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC287_INDEPENDENT_CHECK=FAIL: " + str(error))
