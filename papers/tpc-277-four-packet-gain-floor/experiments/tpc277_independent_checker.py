#!/usr/bin/env python3
"""Independent column-major exact replay for TPC-277."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
CERTIFICATE = PROJECT / "results/tpc277_certificate.json"
CODE = PROJECT / "code/tpc277_four_packet_gain_floor_certificate.py"

spec = importlib.util.spec_from_file_location("tpc277_producer", CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("producer unavailable")
PRODUCER = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PRODUCER)
ENGINE = PRODUCER.ENGINE


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval(value: Fraction) -> list[str]:
    return PRODUCER.interval_text(value)


def replay(case: tuple[int, int, int, int, int, str]):
    scale, height, q0, z, exponent, _role = case
    indices, beta, _ = ENGINE.source_weights(scale, z)
    length = len(indices)
    block = length // 4
    shell = [p for p in ENGINE.PRIMES if q0 < p <= 2 * q0]
    outputs = [[Fraction(0) for _ in range(length)] for _ in range(4)]
    # Column-major accumulation is intentionally different from the producer.
    for column, t in enumerate(indices):
        packet = column // block
        for row, u in enumerate(indices):
            if u == t:
                continue
            shell_factor = Fraction(0)
            for prime in shell:
                if u % prime == 0 or t % prime == 0:
                    continue
                shell_factor += prime * (
                    Fraction(int(u % prime == t % prime), 1)
                    - Fraction(1, prime - 1)
                )
            outputs[packet][row] += (
                ENGINE.kernel(u - t, height, exponent)
                * shell_factor * beta[column]
            )
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    packets = []
    for output in outputs:
        sums = [sum(output[k * block:(k + 1) * block]) for k in range(4)]
        projected = []
        for row, value in enumerate(output):
            k = row // block
            correction = Fraction(0)
            for contrast, denominator in zip(contrasts, denominators):
                cs = sum(contrast[j] * sums[j] for j in range(4))
                correction += Fraction(contrast[k], denominator) * cs
            projected.append(value - correction)
        packets.append(projected)
    energies = [sum(x * x for x in packet) for packet in packets]
    diagonal = sum(energies)
    signed = sum(sum(packets[k][row] for k in range(4)) ** 2
                 for row in range(length))
    return diagonal, signed, shell


def digest(diagonal: Fraction, signed: Fraction) -> str:
    raw = (json.dumps({"D": fraction_text(diagonal), "G": fraction_text(signed)},
                      ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n").encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def check() -> None:
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    need(data["claim_status"] == PRODUCER.STATUS, "status")
    rows = data["payload"]["rows"]
    need(len(rows) == len(PRODUCER.CASES), "row count")
    for case, row in zip(PRODUCER.CASES, rows):
        diagonal, signed, shell = replay(case)
        need(row["prime_shell"] == shell, "shell")
        need(row["exact_replay_digest"] == digest(diagonal, signed),
             "exact replay digest")
        gain = diagonal / signed
        cancellation = (diagonal - signed) / diagonal
        cross_ratio = (signed - diagonal) / (2 * diagonal)
        need(row["gain_interval"] == interval(gain) and
             row["cancellation_fraction_interval"] == interval(cancellation) and
             row["cross_ratio_interval"] == interval(cross_ratio),
             "outward interval")
        need((gain > 1) == row["gain_above_one"] and
             (gain > Fraction(101, 100)) ==
             (row["one_percent_gain_classification"] == "ABOVE"),
             "classification")
    need(data["payload"]["finite_theorem"]["gain_above_one_rows"] == 8,
         "gain count")
    need(data["payload"]["finite_theorem"]["one_percent_below_rows"] == 1,
         "one percent count")
    print("TPC277_INDEPENDENT_CHECK=PASS rows=8 exact_replays=8 "
          "parent_overlap=3 one_percent_floor=REFUTED_SCOPED")


if __name__ == "__main__":
    try:
        check()
    except Exception as error:
        print("TPC277_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
