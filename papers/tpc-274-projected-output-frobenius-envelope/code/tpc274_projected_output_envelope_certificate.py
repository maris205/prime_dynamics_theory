#!/usr/bin/env python3
"""TPC-274: exact projected Frobenius envelopes for the V59 output lane."""

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

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-274-projected-output-frobenius-envelope"
RESULT = PROJECT / "results/tpc274_certificate.json"
UPSTREAM_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"
UPSTREAM_RESULT = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/results/tpc268_certificate.json"
UPSTREAM_PAYLOAD_SHA256 = "890167856037b7c1c0356ffa40bfe5f98e3f6974ff14ca3ef7e248682d220f4a"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP"
ROUND2_CLUE = "TEST_SIGNED_OUTPUT_REASSEMBLY_BEYOND_CANCELLATION_FREE_ENVELOPES"

spec = importlib.util.spec_from_file_location("tpc268_engine", UPSTREAM_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("upstream engine unavailable")
UPSTREAM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(UPSTREAM)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


class Interval:
    """A small exact rational interval used only for certificate transfer."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: Fraction, hi: Fraction | None = None) -> None:
        self.lo = Fraction(lo)
        self.hi = self.lo if hi is None else Fraction(hi)
        need(self.lo <= self.hi, "reversed interval")

    def __add__(self, other: Interval | Fraction) -> Interval:
        right = as_interval(other)
        return Interval(self.lo + right.lo, self.hi + right.hi)

    __radd__ = __add__

    def __neg__(self) -> Interval:
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other: Interval | Fraction) -> Interval:
        return self + (-as_interval(other))

    def __rsub__(self, other: Interval | Fraction) -> Interval:
        return as_interval(other) - self

    def __mul__(self, other: Interval | Fraction) -> Interval:
        right = as_interval(other)
        values = (self.lo * right.lo, self.lo * right.hi,
                  self.hi * right.lo, self.hi * right.hi)
        return Interval(min(values), max(values))

    __rmul__ = __mul__

    def __truediv__(self, other: Interval | Fraction) -> Interval:
        right = as_interval(other)
        need(right.lo > 0 or right.hi < 0, "division interval crosses zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))

    def square(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(self.lo * self.lo,
                                             self.hi * self.hi))
        values = (self.lo * self.lo, self.hi * self.hi)
        return Interval(min(values), max(values))


def as_interval(value: Interval | Fraction | int) -> Interval:
    return value if isinstance(value, Interval) else Interval(Fraction(value))


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval_text(value: Interval) -> list[str]:
    return [fraction_text(value.lo), fraction_text(value.hi)]


def parse_interval(value: object, positive: bool = False) -> Interval:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    result = Interval(Fraction(str(value[0])), Fraction(str(value[1])))
    if positive:
        need(result.lo > 0, "nonpositive interval")
    return result


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def load_parent() -> dict[str, Any]:
    raw = UPSTREAM_RESULT.read_bytes()
    data = json.loads(raw)
    payload = data.get("payload")
    need(isinstance(payload, dict), "parent payload")
    need(data.get("payload_sha256") == UPSTREAM_PAYLOAD_SHA256,
         "parent payload provenance")
    need(hashlib.sha256(canonical(payload).encode("ascii")).hexdigest() ==
         UPSTREAM_PAYLOAD_SHA256, "parent payload digest")
    return data


def growing_cutoff(scale: int) -> int:
    schedule = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}
    need(scale in schedule, "unregistered scale")
    return schedule[scale]


BASE_CASES = (
    (64, 15, 4), (96, 20, 5), (128, 24, 5),
    (192, 32, 6), (256, 38, 6), (384, 50, 7),
)
EXPONENTS = (1, 2)


def operator_matrix(indices: list[int], height: int, q0: int,
                    exponent: int) -> tuple[list[list[Fraction]], list[int]]:
    shell = [prime for prime in UPSTREAM.PRIMES if q0 < prime <= 2 * q0]
    matrix: list[list[Fraction]] = []
    for u in indices:
        row: list[Fraction] = []
        for t in indices:
            if u == t:
                row.append(Fraction(0))
                continue
            total = Fraction(0)
            for prime in shell:
                if u % prime == 0 or t % prime == 0:
                    continue
                centered = Fraction(int(u % prime == t % prime), 1)
                centered -= Fraction(1, prime - 1)
                total += prime * UPSTREAM.kernel(u - t, height, exponent) * centered
            row.append(total)
        matrix.append(row)
    return matrix, shell


def projected_residual_matrix(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    length = len(matrix)
    block_size = length // 4
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block_size, 2 * block_size, 2 * block_size)
    result: list[list[Fraction]] = []
    for column in range(length):
        values = [matrix[row][column] for row in range(length)]
        projected = [Fraction(0) for _ in range(length)]
        for coefficients, denominator in zip(contrasts, denominators):
            contrast = sum(values[k * block_size + r] * coefficients[k]
                           for k in range(4) for r in range(block_size))
            for k in range(4):
                for r in range(block_size):
                    projected[k * block_size + r] += (
                        contrast * coefficients[k] / denominator)
        result.append([values[row] - projected[row] for row in range(length)])
    # Transpose the column-oriented construction back to row-oriented form.
    return [[result[column][row] for column in range(length)]
            for row in range(length)]


def row_record(scale: int, height: int, q0: int, exponent: int) -> dict[str, Any]:
    cutoff = growing_cutoff(scale)
    indices, beta, _weights = UPSTREAM.source_weights(scale, cutoff)
    matrix, shell = operator_matrix(indices, height, q0, exponent)
    output, output_shell = UPSTREAM.operator_output(indices, beta, height, q0,
                                                    exponent)
    need(shell == output_shell, "shell mismatch")
    matrix_output = [sum(matrix[row][column] * beta[column]
                          for column in range(len(indices)))
                     for row in range(len(indices))]
    need(matrix_output == output, "matrix replay mismatch")
    residual_matrix = projected_residual_matrix(matrix)
    frobenius_squared = sum(value * value
                            for row in residual_matrix for value in row)
    beta_norm_squared = sum(value * value for value in beta)
    envelope = frobenius_squared * beta_norm_squared
    audit = UPSTREAM.audit_case(scale, height, q0, exponent, cutoff,
                                "TPC274_GROWING_CUTOFF_KERNEL_GRID")
    actual_g = parse_interval(audit["residual_g_norm_squared_interval"], True)
    actual_w = parse_interval(audit["residual_w_norm_squared_interval"], True)
    actual_c = parse_interval(audit["residual_scalar_interval"])
    actual_margin = parse_interval(audit["rho_squared_interval"], True)
    envelope_interval = Interval(envelope)
    gap = envelope_interval / actual_g
    envelope_margin = actual_c.square() / (actual_w * envelope_interval)
    normalized_envelope = Interval(envelope ** 3 / Fraction(scale ** 5))
    normalized_actual = Interval(actual_g.lo ** 3 / Fraction(scale ** 5),
                                 actual_g.hi ** 3 / Fraction(scale ** 5))
    need(gap.lo > 50, "finite envelope gap below threshold")
    need(envelope_margin.hi < Fraction(1, 64),
         "envelope margin not below one eighth")
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "role": "GROWING_CUTOFF_KERNEL_GRID",
        "index_count": len(indices),
        "prime_shell": shell,
        "projected_operator": "A_perp=(I-P_3)A",
        "matrix_entry_arithmetic": "EXACT_RATIONAL",
        "projected_frobenius_squared": fraction_text(frobenius_squared),
        "beta_norm_squared": fraction_text(beta_norm_squared),
        "output_envelope_squared": fraction_text(envelope),
        "actual_output_residual_norm_squared_interval": interval_text(actual_g),
        "envelope_to_actual_ratio_interval": interval_text(gap),
        "envelope_margin_squared_interval": interval_text(envelope_margin),
        "actual_margin_squared_interval": interval_text(actual_margin),
        "normalized_envelope_sixth_interval": interval_text(normalized_envelope),
        "normalized_actual_output_sixth_interval": interval_text(normalized_actual),
        "phase": audit["phase"],
        "frobenius_envelope_valid": True,
        "envelope_gap_classification": "GAP_ABOVE_FIFTY",
        "envelope_margin_classification": "ENVELOPE_MARGIN_BELOW_ONE_EIGHTH",
        "exact_projection_identity": True,
    }


def kernel_pair_record(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    a = Interval(Fraction(first["output_envelope_squared"]),
                 Fraction(first["output_envelope_squared"]))
    b = Interval(Fraction(second["output_envelope_squared"]),
                 Fraction(second["output_envelope_squared"]))
    actual_a = parse_interval(first["actual_output_residual_norm_squared_interval"])
    actual_b = parse_interval(second["actual_output_residual_norm_squared_interval"])
    return {
        "scale": first["scale"],
        "exponent_transition": "1->2",
        "envelope_ratio_interval": interval_text(b / a),
        "actual_output_ratio_interval": interval_text(actual_b / actual_a),
        "both_envelope_margins_below_one_eighth": True,
    }


def build_payload() -> dict[str, Any]:
    load_parent()
    rows = [row_record(n, h, q, exponent)
            for n, h, q in BASE_CASES for exponent in EXPONENTS]
    pairs = [kernel_pair_record(rows[2 * index], rows[2 * index + 1])
             for index in range(len(BASE_CASES))]
    need(len(rows) == 12 and len(pairs) == 6, "row/pair count")
    need(all(row["phase"] in ("NEGATIVE_REAL_AXIS", "POSITIVE_REAL_AXIS",
                               "CROSSES_ZERO") for row in rows), "phase labels")
    need(all(row["envelope_gap_classification"] == "GAP_ABOVE_FIFTY"
             for row in rows), "gap classes")
    need(all(row["envelope_margin_classification"] ==
             "ENVELOPE_MARGIN_BELOW_ONE_EIGHTH" for row in rows),
         "margin classes")
    return {
        "schema": "TPC274_PROJECTED_OUTPUT_FROBENIUS_ENVELOPE_CERTIFICATE_V1",
        "parameters": {
            "upstream_schema": "TPC268_FINITE_CUTOFF_SENSITIVITY_CERTIFICATE_V1",
            "upstream_payload_sha256": UPSTREAM_PAYLOAD_SHA256,
            "growing_cutoff_schedule": {"64": 4, "96": 4, "128": 4,
                                         "192": 5, "256": 5, "384": 5},
            "kernel_exponents": [1, 2],
            "projection": "three declared four-block Haar contrasts",
            "envelope": "G_F=||A_perp||_F^2 ||beta||_2^2",
            "gap_threshold": "G_F/G_perp > 50",
            "margin_threshold": "m_F^2<1/64",
        },
        "finite_theorem": {
            "total_rows": len(rows),
            "scale_rows": len(BASE_CASES),
            "kernel_pair_rows": len(pairs),
            "gap_above_fifty_rows": len(rows),
            "envelope_margin_below_one_eighth_rows": len(rows),
            "phase_negative_rows": sum(row["phase"] == "NEGATIVE_REAL_AXIS"
                                        for row in rows),
            "phase_positive_rows": sum(row["phase"] == "POSITIVE_REAL_AXIS"
                                        for row in rows),
            "phase_crossing_rows": sum(row["phase"] == "CROSSES_ZERO"
                                        for row in rows),
            "operator_envelope": "PROVED_EXACT_FINITE_INEQUALITY",
            "cancellation_free_route": "INSUFFICIENT_SCOPED",
            "status": "NUMERICALLY_CERTIFIED_FINITE",
            "claim": "projected Frobenius envelope is valid but too loose on registered rows",
        },
        "rows": rows,
        "kernel_pairs": pairs,
        "firewall": {
            "TPC274_PROJECTED_FROBENIUS_ENVELOPE": "PROVED_EXACT_FINITE_INEQUALITY",
            "TPC274_FINITE_GAP": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC274_CANCELLATION_FREE_ROUTE": "INSUFFICIENT_SCOPED",
            "TPC274_SOURCE_LEVEL_OUTPUT_BOUND": "OPEN_ASYMPTOTIC",
            "TPC274_SIGNED_OUTPUT_REASSEMBLY": "OPEN",
            "TPC274_FIXED_POWER_CREDIT": 0,
            "TPC274_ARITHMETIC_ADVANCE": "NO",
            "TPC274_L2": "NONE",
            "TPC274_FULL_GATE_B": "OPEN",
            "TPC274_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC274_TWIN_PRIME_RESULT": "NONE",
            "TPC274_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {"certificate_version": 1, "claim_status": STATUS,
            "payload": payload,
            "payload_sha256": hashlib.sha256(canonical(payload).encode("ascii")).hexdigest()}


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(canonical(document()), encoding="utf-8")


def check() -> None:
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    need(stored == document(), "certificate mismatch")
    need(raw == canonical(stored), "certificate canonicality")
    theorem = stored["payload"]["finite_theorem"]
    print("TPC274_CERTIFICATE=PASS "
          f"rows={theorem['total_rows']} pairs={theorem['kernel_pair_rows']} "
          f"gap_above_fifty={theorem['gap_above_fifty_rows']} "
          f"envelope_margin_low={theorem['envelope_margin_below_one_eighth_rows']} "
          "source_output_reassembly=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError) as error:
        raise SystemExit("TPC274_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
