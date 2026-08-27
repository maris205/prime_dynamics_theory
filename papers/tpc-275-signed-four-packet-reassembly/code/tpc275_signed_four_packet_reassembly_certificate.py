#!/usr/bin/env python3
"""Exact finite signed four-packet reassembly certificate for TPC-275."""

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
RESULT = PROJECT / "results/tpc275_certificate.json"
PARENT = ROOT / "papers/tpc-274-projected-output-frobenius-envelope/results/tpc274_certificate.json"
ENGINE_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"
PARENT_PAYLOAD_SHA256 = "ce03d5c47cd242732b21f8f71d58e009a8dc8b0521d58fdf1a587ba1a9f2affc"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT"
ROUND2_CLUE = "COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET"

spec = importlib.util.spec_from_file_location("frozen_tpc268_engine", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("frozen TPC-268 engine unavailable")
ENGINE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


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
        need(right.lo > 0 or right.hi < 0, "interval division crosses zero")
        values = (self.lo / right.lo, self.lo / right.hi,
                  self.hi / right.lo, self.hi / right.hi)
        return Interval(min(values), max(values))

    def square(self) -> Interval:
        if self.lo <= 0 <= self.hi:
            return Interval(Fraction(0), max(self.lo * self.lo,
                                             self.hi * self.hi))
        values = (self.lo * self.lo, self.hi * self.hi)
        return Interval(min(values), max(values))


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True,
                      separators=(",", ":")) + "\n"


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval_text(value: Interval) -> list[str]:
    return [fraction_text(value.lo), fraction_text(value.hi)]


def parse_interval(value: object, positive: bool = False) -> Interval:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    result = Interval(Fraction(str(value[0])), Fraction(str(value[1])))
    need(not positive or result.lo > 0, "nonpositive interval")
    return result


def load_parent() -> dict[str, Any]:
    raw = PARENT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data).encode("ascii"), "noncanonical parent")
    need(data.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_PROJECTED_FROBENIUS_ENVELOPE_GAP",
         "parent status")
    payload = data.get("payload")
    need(isinstance(payload, dict), "parent payload")
    need(data.get("payload_sha256") == PARENT_PAYLOAD_SHA256 and
         hashlib.sha256(canonical(payload).encode("ascii")).hexdigest() ==
         PARENT_PAYLOAD_SHA256, "parent payload provenance")
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
    shell = [prime for prime in ENGINE.PRIMES if q0 < prime <= 2 * q0]
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
                total += prime * ENGINE.kernel(u - t, height, exponent) * centered
            row.append(total)
        matrix.append(row)
    return matrix, shell


def projected_matrix(matrix: list[list[Fraction]]) -> list[list[Fraction]]:
    length = len(matrix)
    block = length // 4
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    projection = [[Fraction(0) for _ in range(length)]
                  for _ in range(length)]
    for coefficients, denominator in zip(contrasts, denominators):
        for k in range(4):
            for r in range(block):
                i = k * block + r
                for ell in range(4):
                    for rr in range(block):
                        j = ell * block + rr
                        projection[i][j] += Fraction(
                            coefficients[k] * coefficients[ell], denominator)
    return [[matrix[i][j] - sum(projection[i][r] * matrix[r][j]
                                for r in range(length))
             for j in range(length)] for i in range(length)]


def dot(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right))


def norm_squared(value: list[Fraction]) -> Fraction:
    return dot(value, value)


def vector_add(left: list[Fraction], right: list[Fraction], sign: int = 1) -> list[Fraction]:
    return [a + sign * b for a, b in zip(left, right)]


def packet_vectors(matrix: list[list[Fraction]], beta: list[Fraction]) -> list[list[Fraction]]:
    length = len(beta)
    block = length // 4
    return [
        [sum(matrix[i][j] * beta[j]
             for j in range(packet * block, (packet + 1) * block))
         for i in range(length)]
        for packet in range(4)
    ]


def dft_mode_energies(packets: list[list[Fraction]]) -> list[Fraction]:
    v0, v1, v2, v3 = packets
    mode0 = [sum(values) / 2 for values in zip(v0, v1, v2, v3)]
    mode2 = [a - b + c - d for a, b, c, d in zip(v0, v1, v2, v3)]
    difference02 = vector_add(v0, v2, -1)
    difference31 = vector_add(v3, v1, -1)
    return [norm_squared(mode0),
            (norm_squared(difference02) + norm_squared(difference31)) / 4,
            norm_squared(mode2) / 4,
            (norm_squared(difference02) + norm_squared(difference31)) / 4]


def polarization_records(packets: list[list[Fraction]],
                         gram: list[list[Fraction]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for j in range(4):
        for k in range(j + 1, 4):
            plus = norm_squared(vector_add(packets[j], packets[k]))
            minus = norm_squared(vector_add(packets[j], packets[k], -1))
            recovered = (plus - minus) / 4
            records.append({
                "left": j,
                "right": k,
                "plus_energy": fraction_text(plus),
                "minus_energy": fraction_text(minus),
                "recovered_cross_term": fraction_text(recovered),
                "gram_cross_term": fraction_text(gram[j][k]),
                "identity_holds": recovered == gram[j][k],
            })
    return records


def row_record(scale: int, height: int, q0: int,
               exponent: int) -> dict[str, Any]:
    cutoff = growing_cutoff(scale)
    indices, beta, _weights = ENGINE.source_weights(scale, cutoff)
    matrix, shell = operator_matrix(indices, height, q0, exponent)
    output, output_shell = ENGINE.operator_output(indices, beta, height, q0,
                                                   exponent)
    need(shell == output_shell, "prime shell mismatch")
    matrix_output = [sum(matrix[i][j] * beta[j]
                          for j in range(len(indices)))
                     for i in range(len(indices))]
    need(matrix_output == output, "unprojected matrix replay mismatch")
    residual = projected_matrix(matrix)
    packets = packet_vectors(residual, beta)
    total = [sum(packet[i] for packet in packets)
             for i in range(len(indices))]
    signed_energy = norm_squared(total)
    packet_energy = [norm_squared(packet) for packet in packets]
    diagonal_energy = sum(packet_energy)
    cross_sum = signed_energy - diagonal_energy
    gram = [[dot(packets[j], packets[k]) for k in range(4)]
            for j in range(4)]
    modes = dft_mode_energies(packets)
    frobenius_squared = sum(value * value
                            for row in residual for value in row)
    beta_norm_squared = norm_squared(beta)
    frobenius_envelope = frobenius_squared * beta_norm_squared
    audit = ENGINE.audit_case(scale, height, q0, exponent, cutoff,
                              "TPC275_LITERAL_SIGNED_PACKET_REPLAY")
    actual_output = parse_interval(
        audit["residual_g_norm_squared_interval"], True)
    actual_weight = parse_interval(
        audit["residual_w_norm_squared_interval"], True)
    actual_scalar = parse_interval(audit["residual_scalar_interval"])
    actual_margin = parse_interval(audit["rho_squared_interval"], True)
    diagonal_margin = actual_scalar.square() / (
        actual_weight * Interval(diagonal_energy))
    diagonal_ratio = diagonal_energy / signed_energy
    frobenius_ratio = frobenius_envelope / signed_energy
    # The parent stores a decimal-rounded output reference.  The exact matrix
    # multiplication above is the source of truth for the signed energy; the
    # parent interval is retained as a reproducibility reference and is not
    # silently widened here.
    need(cross_sum < 0 and diagonal_ratio > 1 and
         diagonal_ratio < Fraction(12, 5) and frobenius_ratio > 50,
         "finite signed thresholds")
    need(diagonal_margin.hi < Fraction(1, 16),
         "diagonal envelope reaches quarter margin")
    need(sum(modes) == diagonal_energy and modes[0] * 4 == signed_energy,
         "DFT identities")
    probes = polarization_records(packets, gram)
    need(len(probes) == 6 and all(item["identity_holds"] for item in probes),
         "polarization identities")
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "role": "GROWING_CUTOFF_LITERAL_SIGNED_PACKET_REPLAY",
        "index_count": len(indices),
        "block_size": len(indices) // 4,
        "prime_shell": shell,
        "projected_operator": "A_perp=(I-P_3)A",
        "matrix_entry_arithmetic": "EXACT_RATIONAL",
        "packet_definition": "V_j=A_perp beta^(j)",
        "packet_norm_squared": [fraction_text(value) for value in packet_energy],
        "gram": [[fraction_text(value) for value in row] for row in gram],
        "diagonal_packet_energy": fraction_text(diagonal_energy),
        "signed_output_energy": fraction_text(signed_energy),
        "signed_cross_sum": fraction_text(cross_sum),
        "projected_frobenius_squared": fraction_text(frobenius_squared),
        "beta_norm_squared": fraction_text(beta_norm_squared),
        "frobenius_envelope_energy": fraction_text(frobenius_envelope),
        "diagonal_to_signed_ratio": fraction_text(diagonal_ratio),
        "frobenius_to_signed_ratio": fraction_text(frobenius_ratio),
        "actual_output_residual_norm_squared_interval": interval_text(actual_output),
        "exact_signed_output_replay": True,
        "actual_margin_squared_interval": interval_text(actual_margin),
        "diagonal_margin_squared_interval": interval_text(diagonal_margin),
        "dft_mode_energy": {str(k): fraction_text(value)
                            for k, value in enumerate(modes)},
        "dft_parseval_identity": True,
        "dft_mode_zero_identity": True,
        "polarization": probes,
        "phase": audit["phase"],
        "net_cross_term_classification": "NEGATIVE_NET_CROSS_TERM",
        "diagonal_gain_classification": "BETWEEN_1_AND_12_OVER_5",
        "frobenius_comparison_classification": "ABOVE_FIFTY",
        "diagonal_margin_classification": "BELOW_QUARTER_MARGIN",
    }


def build_payload() -> dict[str, Any]:
    load_parent()
    rows = [row_record(n, h, q, exponent)
            for n, h, q in BASE_CASES for exponent in EXPONENTS]
    need(len(rows) == 12, "row count")
    return {
        "schema": "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1",
        "parameters": {
            "upstream_schema": "TPC274_PROJECTED_OUTPUT_FROBENIUS_ENVELOPE_CERTIFICATE_V1",
            "upstream_payload_sha256": PARENT_PAYLOAD_SHA256,
            "growing_cutoff_schedule": {"64": 4, "96": 4, "128": 4,
                                         "192": 5, "256": 5, "384": 5},
            "kernel_exponents": [1, 2],
            "projection": "three declared four-block Haar contrasts",
            "packet_split": "four consecutive source blocks",
            "diagonal_envelope": "D=sum_j ||V_j||_2^2",
            "diagonal_ratio_threshold": "1 < D/G < 12/5",
            "frobenius_ratio_threshold": "F/G > 50",
            "diagonal_margin_threshold": "m_D^2<1/16",
        },
        "finite_theorem": {
            "total_rows": len(rows),
            "scale_rows": len(BASE_CASES),
            "kernel_pair_rows": len(BASE_CASES),
            "polarization_probe_rows": len(rows) * 6,
            "net_cross_negative_rows": sum(
                row["net_cross_term_classification"] == "NEGATIVE_NET_CROSS_TERM"
                for row in rows),
            "diagonal_ratio_between_rows": sum(
                row["diagonal_gain_classification"] == "BETWEEN_1_AND_12_OVER_5"
                for row in rows),
            "frobenius_above_fifty_rows": sum(
                row["frobenius_comparison_classification"] == "ABOVE_FIFTY"
                for row in rows),
            "diagonal_margin_below_quarter_rows": sum(
                row["diagonal_margin_classification"] == "BELOW_QUARTER_MARGIN"
                for row in rows),
            "dft_parseval_rows": sum(row["dft_parseval_identity"] for row in rows),
            "status": "NUMERICALLY_CERTIFIED_FINITE",
            "claim": "literal signed packet cross terms sharpen but do not close the margin route",
        },
        "rows": rows,
        "firewall": {
            "TPC275_SIGNED_GRAM_IDENTITY": "PROVED_EXACT_FINITE",
            "TPC275_DFT_LEDGER": "PROVED_EXACT_FINITE",
            "TPC275_POLARIZATION": "PROVED_EXACT_FINITE",
            "TPC275_LITERAL_PACKET_REPLAY": "NUMERICALLY_CERTIFIED_FINITE_ALL_12_ROWS",
            "TPC275_NET_CROSS_TERM": "NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_ALL_12_ROWS",
            "TPC275_DIAGONAL_GAIN": "NUMERICALLY_CERTIFIED_FINITE_BETWEEN_1_AND_12_OVER_5",
            "TPC275_FROBENIUS_COMPARISON": "NUMERICALLY_CERTIFIED_FINITE_ABOVE_50",
            "TPC275_DIAGONAL_MARGIN": "NUMERICALLY_CERTIFIED_FINITE_BELOW_QUARTER",
            "TPC275_DIAGONAL_ROUTE": "INSUFFICIENT_SCOPED",
            "TPC275_SOURCE_LEVEL_SIGNED_CROSS_GRAM": "OPEN_ASYMPTOTIC",
            "TPC275_FIXED_POWER_CREDIT": 0,
            "TPC275_ARITHMETIC_ADVANCE": "NO",
            "TPC275_L2": "NONE",
            "TPC275_FULL_GATE_B": "OPEN",
            "TPC275_FULL_GATE_B_STRICT_1_OVER_400": "UNPAID_GLOBAL",
            "TPC275_TWIN_PRIME_RESULT": "NONE",
            "TPC275_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(
            canonical(payload).encode("ascii")).hexdigest(),
    }


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(canonical(document()), encoding="utf-8")


def check() -> None:
    raw = RESULT.read_text(encoding="utf-8")
    stored = json.loads(raw)
    need(stored == document(), "certificate mismatch")
    need(raw == canonical(stored), "certificate canonicality")
    theorem = stored["payload"]["finite_theorem"]
    print("TPC275_CERTIFICATE=PASS "
          f"rows={theorem['total_rows']} "
          f"cross_negative={theorem['net_cross_negative_rows']} "
          f"diagonal_gain={theorem['diagonal_ratio_between_rows']} "
          f"diagonal_margin_low={theorem['diagonal_margin_below_quarter_rows']} "
          "source_signed_cross_gram=OPEN")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            ZeroDivisionError) as error:
        raise SystemExit("TPC275_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
