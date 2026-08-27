#!/usr/bin/env python3
"""Independent replay of the TPC-282 literal source attachment rows.

This file does not import the TPC-282 producer.  It reconstructs the frozen
source model, the three block-Haar projection, the scalar attachment, and the
normalized cosine interval directly from the TPC-268 engine.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-282-literal-source-attachment-audit"
ENGINE_PATH = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
PARENT_RESULT = ROOT / "papers/tpc-275-signed-four-packet-reassembly/results/tpc275_certificate.json"
RESULT = PROJECT / "results/tpc282_certificate.json"
ENGINE_SHA256 = "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3"
PARENT_SHA256 = "8ab8856cd000ef172cec4fabf15e65772984452bfb547672ffa136704d48c0fd"
SCHEMA = "TPC282_LITERAL_SOURCE_ATTACHMENT_CERTIFICATE_V1"
STATUS = (
    "NUMERICALLY_CERTIFIED_FINITE_LITERAL_SOURCE_ATTACHMENT_LOCK_PLUS_"
    "ASYMPTOTIC_NONDEGENERACY_OPEN")

spec = importlib.util.spec_from_file_location("frozen_source_engine", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise SystemExit("TPC282_INDEPENDENT_CHECK=FAIL engine unavailable")
E = importlib.util.module_from_spec(spec)
spec.loader.exec_module(E)


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


def ftext(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction")
    return Fraction(value)


def parse_interval(value: object) -> tuple[Fraction, Fraction]:
    need(isinstance(value, list) and len(value) == 2, "interval")
    lo, hi = parse_fraction(value[0]), parse_fraction(value[1])
    need(lo <= hi, "interval order")
    return lo, hi


def interval_fraction(value: Any) -> tuple[Fraction, Fraction]:
    # The frozen engine emits outward decimal strings.  Convert those strings
    # to exact rationals before comparing the release certificate.
    text = E.interval_text(value)
    return parse_fraction(text[0]), parse_fraction(text[1])


def projection_data(values: list[Any], block: int, interval_mode: bool) -> tuple[Any, Any]:
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    zero = E.Interval(Fraction(0)) if interval_mode else Fraction(0)
    block_sum = [sum(values[k * block:(k + 1) * block], zero)
                 for k in range(4)]
    projected = E.Interval(Fraction(0)) if interval_mode else Fraction(0)
    for coefficients, denominator in zip(contrasts, denominators):
        contrast = sum((block_sum[k] * coefficients[k]
                        for k in range(4)), zero)
        projected += contrast * contrast / Fraction(denominator) \
            if interval_mode else contrast * contrast / Fraction(denominator)
    return block_sum, projected


def row_replay(scale: int, height: int, q0: int, exponent: int,
               cutoff: int) -> tuple[tuple[Fraction, Fraction],
                                      tuple[Fraction, Fraction], Fraction,
                                      tuple[Fraction, Fraction]]:
    indices, beta, weights = E.source_weights(scale, cutoff)
    output, _ = E.operator_output(indices, beta, height, q0, exponent)
    n = len(indices)
    block = n // 4
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    block_g = [sum(output[k * block:(k + 1) * block], Fraction(0))
               for k in range(4)]
    block_w = [sum(weights[k * block:(k + 1) * block],
                   E.Interval(Fraction(0))) for k in range(4)]
    projected_output = [Fraction(0) for _ in range(n)]
    projected_weight_energy = E.Interval(Fraction(0))
    projected_source_signal = E.Interval(Fraction(0))
    for coefficients, denominator in zip(contrasts, denominators):
        gc = sum(block_g[k] * coefficients[k] for k in range(4))
        wc = sum((block_w[k] * coefficients[k] for k in range(4)),
                 E.Interval(Fraction(0)))
        projected_source_signal += wc * gc / Fraction(denominator)
        projected_weight_energy += wc.square() / Fraction(denominator)
        for k in range(4):
            for r in range(block):
                i = k * block + r
                projected_output[i] += Fraction(coefficients[k] * gc,
                                                denominator)
                # The energy and scalar are accumulated below in the same
                # outward-interval order as the frozen source audit.
    signal = [output[i] - projected_output[i] for i in range(n)]
    direct = sum((weights[i] * output[i] for i in range(n)),
            E.Interval(Fraction(0)))
    C = direct - projected_source_signal
    W = sum((value.square() for value in weights),
            E.Interval(Fraction(0))) - projected_weight_energy
    Y = sum(value * value for value in signal)
    rho = C.square() / (W * E.Interval(Y))
    return interval_fraction(C), interval_fraction(W), Y, interval_fraction(rho)


def load() -> dict[str, Any]:
    need(digest(ENGINE_PATH.read_bytes()) == ENGINE_SHA256,
         "engine provenance")
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "certificate header")
    need(data["payload"]["schema"] == SCHEMA, "schema")
    need(data["payload_sha256"] == digest(canonical(data["payload"])),
         "payload hash")
    parent = json.loads(PARENT_RESULT.read_text(encoding="utf-8"))
    need(digest(PARENT_RESULT.read_bytes()) == PARENT_SHA256,
         "parent provenance")
    need(parent["payload"]["schema"] ==
         "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1",
         "parent schema")
    return data


def check() -> None:
    data = load()
    payload = data["payload"]
    rows = payload["rows"]
    need(len(rows) == 12, "row census")
    for row in rows:
        c, w, y, rho = row_replay(
            int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["kernel_exponent"]), int(row["comparison_cutoff_z"]))
        need([ftext(x) for x in c] == row["source_scalar_C_interval"],
             "source scalar mismatch")
        need([ftext(x) for x in w] ==
             row["projected_source_norm_squared_interval"],
             "source norm mismatch")
        need(ftext(y) == row["projected_output_norm_squared"],
             "output norm mismatch")
        need([ftext(x) for x in rho] ==
             row["attachment_cosine_squared_interval"],
             "attachment mismatch")
        need(c[1] < 0 or c[0] > 0, "unseparated attachment")
        need(rho[0] > 0 and rho[1] < 1, "invalid cosine interval")
    need(payload["finite_theorem"] == {
        "asymptotic_nonvanishing": "OPEN",
        "fixed_power_credit": 0,
        "negative_rows": 11,
        "positive_rows": 1,
        "statement": "all registered literal rows have a sign-separated nonzero source attachment",
        "zero_crossing_rows": 0,
    }, "finite theorem census")
    print("TPC282_INDEPENDENT_CHECK=PASS rows=12 exact_projection=12 "
          "attachment_signs=11_negative_1_positive")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC282_INDEPENDENT_CHECK=FAIL: " + str(error))
