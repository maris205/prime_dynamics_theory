#!/usr/bin/env python3
"""Independent replay for the TPC-274 projected-output envelope certificate."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
RESULT = ROOT / "papers/tpc-274-projected-output-frobenius-envelope/results/tpc274_certificate.json"
PARENT = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json"
ENGINE_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"
PARENT_SHA = "890167856037b7c1c0356ffa40bfe5f98e3f6974ff14ca3ef7e248682d220f4a"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP"

spec = importlib.util.spec_from_file_location("frozen_output_engine", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise RuntimeError(message)


class Interval:
    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction, hi: Fraction | None = None) -> None:
        self.lo = Fraction(lo)
        self.hi = self.lo if hi is None else Fraction(hi)
        need(self.lo <= self.hi, "reversed interval")

    def __add__(self, other: Interval | Fraction) -> Interval:
        right = other if isinstance(other, Interval) else Interval(other)
        return Interval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval | Fraction) -> Interval:
        return self + (-other if isinstance(other, Interval) else -Interval(other))

    def __mul__(self, other: Interval | Fraction) -> Interval:
        right = other if isinstance(other, Interval) else Interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction) -> Interval:
        right = other if isinstance(other, Interval) else Interval(other)
        need(right.lo > 0 or right.hi < 0, "division through zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))

    def square(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(self.lo * self.lo,
                                             self.hi * self.hi))
        return Interval(min(self.lo * self.lo, self.hi * self.hi),
                        max(self.lo * self.lo, self.hi * self.hi))


def text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval(value: object, positive: bool = False) -> Interval:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    result = Interval(Fraction(str(value[0])), Fraction(str(value[1])))
    if positive:
        need(result.lo > 0, "nonpositive interval")
    return result


def interval_text(value: Interval) -> list[str]:
    return [text(value.lo), text(value.hi)]


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def load(path: Path) -> dict:
    raw = path.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "noncanonical JSON: " + path.name)
    return data


def matrix(indices: list[int], height: int, q0: int,
           exponent: int) -> tuple[list[list[Fraction]], list[int]]:
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    result: list[list[Fraction]] = []
    for u in indices:
        row: list[Fraction] = []
        for t in indices:
            total = Fraction(0)
            if u != t:
                for q in shell:
                    if u % q == 0 or t % q == 0:
                        continue
                    centered = Fraction(int(u % q == t % q), 1)
                    centered -= Fraction(1, q - 1)
                    total += q * ENGINE.kernel(u - t, height, exponent) * centered
            row.append(total)
        result.append(row)
    return result, shell


def residual_matrix(matrix_value: list[list[Fraction]]) -> list[list[Fraction]]:
    length = len(matrix_value)
    block = length // 4
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    columns: list[list[Fraction]] = []
    for j in range(length):
        col = [matrix_value[i][j] for i in range(length)]
        projected = [Fraction(0) for _ in range(length)]
        for coefficients, denominator in zip(contrasts, denominators):
            c = sum(col[k * block + r] * coefficients[k]
                    for k in range(4) for r in range(block))
            for k in range(4):
                for r in range(block):
                    projected[k * block + r] += c * coefficients[k] / denominator
        columns.append([col[i] - projected[i] for i in range(length)])
    return [[columns[j][i] for j in range(length)] for i in range(length)]


def growing(scale: int) -> int:
    schedule = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    need(scale in schedule, "scale schedule")
    return schedule[scale]


CASES = ((64, 15, 4), (96, 20, 5), (128, 24, 5),
         (192, 32, 6), (256, 38, 6), (384, 50, 7))


def check() -> None:
    parent = load(PARENT)
    payload_parent = parent["payload"]
    need(hashlib.sha256(canonical(payload_parent)).hexdigest() == PARENT_SHA,
         "parent provenance")
    data = load(RESULT)
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "header")
    payload = data["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() == data["payload_sha256"],
         "payload digest")
    need(payload["schema"] ==
         "TPC274_PROJECTED_OUTPUT_FROBENIUS_ENVELOPE_CERTIFICATE_V1",
         "schema")
    rows = payload["rows"]
    need(len(rows) == 12, "row count")
    keys = set()
    for row in rows:
        key = (row["scale"], row["kernel_exponent"])
        need(key not in keys, "duplicate row")
        keys.add(key)
        n, h, q, exponent = row["scale"], row["H"], row["Q"], row["kernel_exponent"]
        need(row["comparison_cutoff_z"] == growing(n), "cutoff registry")
        indices, beta, _ = ENGINE.source_weights(n, row["comparison_cutoff_z"])
        mat, shell = matrix(indices, h, q, exponent)
        output, shell_again = ENGINE.operator_output(indices, beta, h, q, exponent)
        need(shell == shell_again, "shell replay")
        need([sum(mat[i][j] * beta[j] for j in range(len(indices)))
              for i in range(len(indices))] == output, "matrix multiplication")
        projected = residual_matrix(mat)
        f2 = sum(value * value for line in projected for value in line)
        b2 = sum(value * value for value in beta)
        envelope = f2 * b2
        need(row["projected_frobenius_squared"] == text(f2) and
             row["beta_norm_squared"] == text(b2) and
             row["output_envelope_squared"] == text(envelope), "exact envelope")
        audit = ENGINE.audit_case(n, h, q, exponent,
                                  row["comparison_cutoff_z"],
                                  "TPC274_INDEPENDENT_REPLAY")
        actual_g = interval(audit["residual_g_norm_squared_interval"], True)
        actual_w = interval(audit["residual_w_norm_squared_interval"], True)
        actual_c = interval(audit["residual_scalar_interval"])
        need(row["actual_output_residual_norm_squared_interval"] ==
             interval_text(actual_g), "actual output replay")
        gap = Interval(envelope) / actual_g
        margin = actual_c.square() / (actual_w * Interval(envelope))
        need(row["envelope_to_actual_ratio_interval"] == interval_text(gap) and
             row["envelope_margin_squared_interval"] == interval_text(margin),
             "transferred intervals")
        need(gap.lo > 50 and margin.hi < Fraction(1, 64) and
             row["envelope_gap_classification"] == "GAP_ABOVE_FIFTY" and
             row["envelope_margin_classification"] ==
             "ENVELOPE_MARGIN_BELOW_ONE_EIGHTH", "threshold semantics")
    theorem = payload["finite_theorem"]
    need(theorem["total_rows"] == 12 and theorem["kernel_pair_rows"] == 6 and
         theorem["gap_above_fifty_rows"] == 12 and
         theorem["envelope_margin_below_one_eighth_rows"] == 12 and
         theorem["status"] == "NUMERICALLY_CERTIFIED_FINITE", "theorem counts")
    need(payload["firewall"]["TPC274_FIXED_POWER_CREDIT"] == 0 and
         payload["firewall"]["TPC274_CANCELLATION_FREE_ROUTE"] ==
         "INSUFFICIENT_SCOPED" and
         payload["firewall"]["TPC274_SOURCE_LEVEL_OUTPUT_BOUND"] ==
         "OPEN_ASYMPTOTIC", "firewall")
    print("TPC274_INDEPENDENT_CHECK=PASS rows=12 pairs=6 gap_above_fifty=12 "
          "envelope_margin_low=12 matrix_replay=EXACT source_output_reassembly=OPEN")


if __name__ == "__main__":
    try:
        check()
    except Exception as error:
        print("TPC274_INDEPENDENT_CHECK=FAIL " + str(error))
        raise SystemExit(1)
