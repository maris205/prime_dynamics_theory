#!/usr/bin/env python3
"""Exact four-packet gain-floor and source-scan certificate for TPC-277.

The source calculation is deliberately matrix-free after the prime shell has
been fixed.  It computes the four actual packet outputs, applies the declared
rank-three Haar projection to each output vector, and then forms D and G with
Fraction arithmetic.  The JSON stores outward intervals and a digest of the
exact D/G replay; the independent checker performs the expensive replay.
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
ENGINE_PATH = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py"
)
PARENT = ROOT / (
    "papers/tpc-275-signed-four-packet-reassembly/results/"
    "tpc275_certificate.json"
)
RESULT = PROJECT / "results/tpc277_certificate.json"
PARENT_FILE_SHA256 = (
    "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
)
PARENT_PAYLOAD_SHA256 = (
    "6f72d561af7f6aec1626843cc0574afc74a1de5a10f57867b202a585a1cfc429"
)
PARENT_SCHEMA = "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1"
SCHEMA = "TPC277_FOUR_PACKET_GAIN_FLOOR_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_UNIVERSAL_FOUR_PACKET_GAIN_FLOOR_PLUS_"
    "NUMERICALLY_CERTIFIED_SOURCE_SCAN"
)
ROUND2_CLUE = "TEST_CROSS_SCALE_SIGNED_GAIN_STABILITY_AND_SHELL_SENSITIVITY"
GRID = 10**15
UNITY_GAIN_THRESHOLD = Fraction(1)
ONE_PERCENT_GAIN_THRESHOLD = Fraction(101, 100)

spec = importlib.util.spec_from_file_location("tpc277_frozen_engine", ENGINE_PATH)
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


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval_text(value: Fraction) -> list[str]:
    scaled = value * GRID
    lower = scaled.numerator // scaled.denominator
    upper = lower + int(scaled.numerator % scaled.denominator != 0)
    return [fraction_text(Fraction(lower, GRID)),
            fraction_text(Fraction(upper, GRID))]


def parse_interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    left, right = parse_fraction(value[0]), parse_fraction(value[1])
    need(left <= right, "interval order")
    return left, right


def load_parent() -> dict[str, Any]:
    raw = PARENT.read_bytes()
    need(digest_bytes(raw) == PARENT_FILE_SHA256, "parent file provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    payload = data.get("payload")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT",
         "parent header")
    need(isinstance(payload, dict) and payload.get("schema") == PARENT_SCHEMA,
         "parent schema")
    need(data.get("payload_sha256") == PARENT_PAYLOAD_SHA256 and
         hashlib.sha256(canonical(payload)).hexdigest() ==
         PARENT_PAYLOAD_SHA256, "parent payload provenance")
    need(isinstance(payload.get("rows"), list) and
         len(payload["rows"]) == 12, "parent rows")
    return data


def exact_packet_energies(scale: int, height: int, q0: int, z: int,
                          exponent: int) -> tuple[Fraction, Fraction,
                                                  list[int]]:
    """Return exact (D,G,shell) for the four actual source packets."""
    indices, beta, _weights = ENGINE.source_weights(scale, z)
    length = len(indices)
    block = length // 4
    need(length % 4 == 0, "four equal source blocks")
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
    # y[j] is the unprojected output from the columns in packet j.
    outputs = [[Fraction(0) for _ in range(length)] for _ in range(4)]
    for row, u in enumerate(indices):
        for column, t in enumerate(indices):
            if u == t:
                continue
            shell_factor = Fraction(0)
            for prime in shell:
                if u % prime == 0 or t % prime == 0:
                    continue
                centered = Fraction(int(u % prime == t % prime), 1)
                centered -= Fraction(1, prime - 1)
                shell_factor += prime * centered
            if shell_factor:
                outputs[column // block][row] += (
                    ENGINE.kernel(u - t, height, exponent)
                    * shell_factor * beta[column]
                )

    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    packets: list[list[Fraction]] = []
    for output in outputs:
        block_sums = [sum(output[k * block:(k + 1) * block])
                      for k in range(4)]
        projected: list[Fraction] = []
        for row, value in enumerate(output):
            packet_index = row // block
            correction = Fraction(0)
            for contrast, denominator in zip(contrasts, denominators):
                contrast_sum = sum(contrast[k] * block_sums[k]
                                   for k in range(4))
                correction += Fraction(contrast[packet_index], denominator) \
                    * contrast_sum
            projected.append(value - correction)
        packets.append(projected)

    energies = [sum(value * value for value in packet)
                for packet in packets]
    diagonal = sum(energies)
    signed = sum(sum(packets[k][row] for k in range(4)) ** 2
                 for row in range(length))
    need(diagonal > 0 and signed > 0, "positive packet energies")
    return diagonal, signed, shell


CASES = (
    (192, 32, 6, 5, 2, "REGISTERED_NEAR_ONE"),
    (256, 38, 6, 6, 2, "REGISTERED_CONTROL"),
    (384, 50, 7, 7, 2, "REGISTERED_CONTROL"),
    (512, 64, 8, 7, 2, "EXTENDED_SCALE"),
    (768, 86, 9, 9, 2, "EXTENDED_SCALE"),
    (1024, 108, 10, 10, 2, "EXTENDED_SCALE"),
    (1536, 150, 12, 12, 2, "EXTENDED_SCALE"),
    (2048, 170, 12, 12, 2, "EXTENDED_SCALE"),
)


def exact_digest(diagonal: Fraction, signed: Fraction) -> str:
    return hashlib.sha256(canonical({
        "D": fraction_text(diagonal),
        "G": fraction_text(signed),
    })).hexdigest()


def parent_rows_by_key(parent: dict[str, Any]) -> dict[tuple[int, int], dict[str, Any]]:
    return {(int(row["scale"]), int(row["kernel_exponent"])): row
            for row in parent["payload"]["rows"]}


def row_record(case: tuple[int, int, int, int, int, str],
               parent: dict[str, Any]) -> dict[str, Any]:
    scale, height, q0, z, exponent, role = case
    diagonal, signed, shell = exact_packet_energies(
        scale, height, q0, z, exponent)
    gain = diagonal / signed
    cancellation = (diagonal - signed) / diagonal
    cross_ratio = (signed - diagonal) / (2 * diagonal)
    need(gain > 0, "gain sign")
    record: dict[str, Any] = {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": z,
        "kernel_exponent": exponent,
        "role": role,
        "index_interval": [scale // 2 + 1, scale],
        "index_count": scale // 2,
        "block_size": scale // 8,
        "prime_shell": shell,
        "matrix_entry_arithmetic": "EXACT_RATIONAL",
        "packet_definition": "V_j=(I-P_3)A beta^(j)",
        "gain_interval": interval_text(gain),
        "cancellation_fraction_interval": interval_text(cancellation),
        "cross_ratio_interval": interval_text(cross_ratio),
        "gain_above_one": gain > UNITY_GAIN_THRESHOLD,
        "one_percent_gain_classification": (
            "ABOVE" if gain > ONE_PERCENT_GAIN_THRESHOLD else "BELOW"
        ),
        "net_cross_term_classification": (
            "NEGATIVE" if signed < diagonal else
            "POSITIVE" if signed > diagonal else "ZERO"
        ),
        "exact_replay_digest": exact_digest(diagonal, signed),
        "source_replay_status": "EXACT_FRACTION_REPLAY",
    }
    parent_row = parent_rows_by_key(parent).get((scale, exponent))
    if parent_row is not None:
        parent_gain = parse_fraction(parent_row["diagonal_to_signed_ratio"])
        need(parent_gain == gain, "registered parent gain mismatch")
        record["parent_gain_match"] = True
        record["parent_gain_interval"] = interval_text(parent_gain)
    else:
        record["parent_gain_match"] = False
        record["parent_gain_interval"] = None
    return record


def build_payload() -> dict[str, Any]:
    parent = load_parent()
    rows = [row_record(case, parent) for case in CASES]
    need(len(rows) == 8, "row count")
    need(all(row["gain_above_one"] for row in rows), "natural gain sign")
    need(any(row["one_percent_gain_classification"] == "BELOW"
             for row in rows), "one percent obstruction")
    return {
        "schema": SCHEMA,
        "parameters": {
            "upstream_schema": PARENT_SCHEMA,
            "upstream_payload_sha256": PARENT_PAYLOAD_SHA256,
            "upstream_file_sha256": PARENT_FILE_SHA256,
            "projection": "three four-block Haar contrasts",
            "packet_count": 4,
            "gain_definition": "r=D/G",
            "cancellation_definition": "kappa=(D-G)/D=1-1/r",
            "exact_replay": "matrix-free Fraction source replay",
            "interval_grid": str(GRID),
            "registered_and_extended_clock": (
                "(192,32,6,5),(256,38,6,6),(384,50,7,7),"
                "(512,64,8,7),(768,86,9,9),(1024,108,10,10),"
                "(1536,150,12,12),(2048,170,12,12)"
            ),
        },
        "universal_theorem": {
            "statement": "G<=4D and therefore r>=1/4 for four packets",
            "signed_statement": "G<=D when the net cross term is nonpositive",
            "sharp_general_floor": "1/4",
            "sharp_signed_floor": "1",
            "proof_status": "PROVED_EXACT",
        },
        "finite_theorem": {
            "total_rows": len(rows),
            "gain_above_one_rows": sum(row["gain_above_one"] for row in rows),
            "negative_cross_rows": sum(
                row["net_cross_term_classification"] == "NEGATIVE"
                for row in rows),
            "one_percent_below_rows": sum(
                row["one_percent_gain_classification"] == "BELOW"
                for row in rows),
            "minimum_gain_target": "r>=101/100",
            "minimum_gain_target_status": "REFUTED_SCOPED_FINITE",
            "claim": (
                "natural source rows have r>1, but the one-percent floor "
                "already fails on the registered/extended finite scan"
            ),
        },
        "rows": rows,
        "firewall": {
            "TPC277_UNIVERSAL_FOUR_PACKET_FLOOR": "PROVED_EXACT_R>=1_OVER_4",
            "TPC277_NONPOSITIVE_CROSS_FLOOR": "PROVED_CONDITIONAL_R>=1",
            "TPC277_SOURCE_SCAN": "NUMERICALLY_CERTIFIED_FINITE_ALL_8_ROWS",
            "TPC277_NATURAL_GAIN_SIGN": "NUMERICALLY_CERTIFIED_FINITE_ALL_8_ROWS",
            "TPC277_ONE_PERCENT_FLOOR": "REFUTED_SCOPED_FINITE",
            "TPC277_SOURCE_LEVEL_POWER_GAIN": "OPEN_ASYMPTOTIC",
            "TPC277_FIXED_POWER_CREDIT": 0,
            "TPC277_ARITHMETIC_ADVANCE": "NO",
            "TPC277_L2": "NONE",
            "TPC277_FULL_GATE_B": "OPEN",
            "TPC277_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC277_TWIN_PRIME_RESULT": "NONE",
            "TPC277_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored.get("certificate_version") == 1 and
         stored.get("claim_status") == STATUS and
         isinstance(stored.get("payload"), dict), "certificate header")
    payload = stored["payload"]
    need(payload.get("schema") == SCHEMA and
         stored.get("payload_sha256") ==
         hashlib.sha256(canonical(payload)).hexdigest(),
         "certificate digest/schema")
    payload = stored["payload"]
    theorem = payload["finite_theorem"]
    need(theorem["total_rows"] == 8 and
         theorem["gain_above_one_rows"] == 8 and
         theorem["negative_cross_rows"] == 8 and
         theorem["one_percent_below_rows"] >= 1,
         "finite theorem counts")
    print("TPC277_CERTIFICATE=PASS rows=8 gain_above_one=8 "
          f"one_percent_below={theorem['one_percent_below_rows']} "
          "universal_floor=1/4 fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            ZeroDivisionError, json.JSONDecodeError) as error:
        raise SystemExit("TPC277_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
