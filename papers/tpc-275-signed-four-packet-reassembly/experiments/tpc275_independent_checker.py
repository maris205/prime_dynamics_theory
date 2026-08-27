#!/usr/bin/env python3
"""Independent exact replay for the TPC-275 packet certificate."""

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
PROJECT = ROOT / "papers/tpc-275-signed-four-packet-reassembly"
RESULT = PROJECT / "results/tpc275_certificate.json"
PARENT = ROOT / "papers/tpc-274-projected-output-frobenius-envelope/results/tpc274_certificate.json"
ENGINE_PATH = ROOT / "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/tpc268_cutoff_sensitivity_certificate.py"
PARENT_SHA = "ce03d5c47cd242732b21f8f71d58e009a8dc8b0521d58fdf1a587ba1a9f2affc"
STATUS = "NUMERICALLY_CERTIFIED_FINITE_SIGNED_FOUR_PACKET_REASSEMBLY_AUDIT"

spec = importlib.util.spec_from_file_location("independent_frozen_engine", ENGINE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("engine unavailable")
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
        need(self.lo <= self.hi, "interval order")

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
        values = (self.lo * self.lo, self.hi * self.hi)
        return Interval(min(values), max(values))


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def fraction(value: object) -> Fraction:
    need(isinstance(value, str), "fraction text")
    return Fraction(value)


def interval(value: object, positive: bool = False) -> Interval:
    need(isinstance(value, list) and len(value) == 2, "interval shape")
    result = Interval(Fraction(str(value[0])), Fraction(str(value[1])))
    need(not positive or result.lo > 0, "interval sign")
    return result


def interval_text(value: Interval) -> list[str]:
    return [f"{value.lo.numerator}/{value.lo.denominator}",
            f"{value.hi.numerator}/{value.hi.denominator}"]


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
                    total += q * ENGINE.kernel(u - t, height, exponent) * (
                        Fraction(int(u % q == t % q)) - Fraction(1, q - 1))
            row.append(total)
        result.append(row)
    return result, shell


def project(matrix_value: list[list[Fraction]]) -> list[list[Fraction]]:
    length = len(matrix_value)
    block = length // 4
    contrasts = ((1, 1, -1, -1), (1, -1, 0, 0), (0, 0, 1, -1))
    denominators = (4 * block, 2 * block, 2 * block)
    p = [[Fraction(0) for _ in range(length)] for _ in range(length)]
    for coefficients, denominator in zip(contrasts, denominators):
        for k in range(4):
            for r in range(block):
                i = k * block + r
                for ell in range(4):
                    for rr in range(block):
                        j = ell * block + rr
                        p[i][j] += Fraction(coefficients[k] * coefficients[ell],
                                             denominator)
    return [[matrix_value[i][j] - sum(p[i][r] * matrix_value[r][j]
                                     for r in range(length))
             for j in range(length)] for i in range(length)]


def inner(left: list[Fraction], right: list[Fraction]) -> Fraction:
    return sum(a * b for a, b in zip(left, right))


def packet_list(matrix_value: list[list[Fraction]],
                beta: list[Fraction]) -> list[list[Fraction]]:
    block = len(beta) // 4
    return [[sum(matrix_value[i][j] * beta[j]
                 for j in range(k * block, (k + 1) * block))
             for i in range(len(beta))] for k in range(4)]


def add(left: list[Fraction], right: list[Fraction], sign: int) -> list[Fraction]:
    return [a + sign * b for a, b in zip(left, right)]


def energy(value: list[Fraction]) -> Fraction:
    return inner(value, value)


def mode_energies(v: list[list[Fraction]]) -> list[Fraction]:
    v0, v1, v2, v3 = v
    zero = [sum(values) / 2 for values in zip(v0, v1, v2, v3)]
    two = [a - b + c - d for a, b, c, d in zip(v0, v1, v2, v3)]
    d02 = add(v0, v2, -1)
    d31 = add(v3, v1, -1)
    side = (energy(d02) + energy(d31)) / 4
    return [energy(zero), side, energy(two) / 4, side]


def replay_row(row: dict) -> None:
    n, h, q, s = (row["scale"], row["H"], row["Q"],
                   row["kernel_exponent"])
    schedule = {64: (15, 4), 96: (20, 5), 128: (24, 5),
                192: (32, 6), 256: (38, 6), 384: (50, 7)}
    need(n in schedule and (h, q) == schedule[n], "scale tuple")
    cutoff = {64: 4, 96: 4, 128: 4, 192: 5, 256: 5, 384: 5}[n]
    need(row["comparison_cutoff_z"] == cutoff and s in (1, 2),
         "cutoff/exponent")
    indices, beta, _ = ENGINE.source_weights(n, cutoff)
    raw, shell = matrix(indices, h, q, s)
    output, output_shell = ENGINE.operator_output(indices, beta, h, q, s)
    need(shell == output_shell, "shell")
    need([sum(raw[i][j] * beta[j] for j in range(len(beta)))
          for i in range(len(beta))] == output, "raw output")
    projected = project(raw)
    packets = packet_list(projected, beta)
    total = [sum(v[i] for v in packets) for i in range(len(beta))]
    signed = energy(total)
    packet_norms = [energy(v) for v in packets]
    diagonal = sum(packet_norms)
    gram = [[inner(packets[j], packets[k]) for k in range(4)]
            for j in range(4)]
    modes = mode_energies(packets)
    frob = sum(value * value for line in projected for value in line)
    beta_norm = energy(beta)
    f_env = frob * beta_norm
    need(row["packet_norm_squared"] == [f"{x.numerator}/{x.denominator}"
                                         for x in packet_norms], "packet norms")
    need(row["gram"] == [[f"{x.numerator}/{x.denominator}" for x in line]
                          for line in gram], "Gram")
    need(fraction(row["diagonal_packet_energy"]) == diagonal and
         fraction(row["signed_output_energy"]) == signed and
         fraction(row["signed_cross_sum"]) == signed - diagonal and
         fraction(row["projected_frobenius_squared"]) == frob and
         fraction(row["beta_norm_squared"]) == beta_norm and
         fraction(row["frobenius_envelope_energy"]) == f_env,
         "exact energies")
    need(fraction(row["diagonal_to_signed_ratio"]) == diagonal / signed and
         fraction(row["frobenius_to_signed_ratio"]) == f_env / signed,
         "ratios")
    need(row["dft_mode_energy"] ==
         {str(k): f"{x.numerator}/{x.denominator}"
          for k, x in enumerate(modes)} and
         sum(modes) == diagonal and modes[0] * 4 == signed,
         "DFT ledger")
    probes = row["polarization"]
    need(len(probes) == 6, "probe count")
    cursor = 0
    for j in range(4):
        for k in range(j + 1, 4):
            plus = energy(add(packets[j], packets[k], 1))
            minus = energy(add(packets[j], packets[k], -1))
            recovered = (plus - minus) / 4
            item = probes[cursor]
            cursor += 1
            need((item["left"], item["right"]) == (j, k) and
                 fraction(item["plus_energy"]) == plus and
                 fraction(item["minus_energy"]) == minus and
                 fraction(item["recovered_cross_term"]) == recovered and
                 fraction(item["gram_cross_term"]) == gram[j][k] and
                 item["identity_holds"] is True and recovered == gram[j][k],
                 "polarization probe")
    actual = ENGINE.audit_case(n, h, q, s, cutoff,
                               "TPC275_INDEPENDENT_REPLAY")
    actual_output = interval(actual["residual_g_norm_squared_interval"], True)
    actual_weight = interval(actual["residual_w_norm_squared_interval"], True)
    actual_scalar = interval(actual["residual_scalar_interval"])
    diagonal_margin = actual_scalar.square() / (actual_weight * Interval(diagonal))
    need(row["actual_output_residual_norm_squared_interval"] ==
         interval_text(actual_output),
         "parent output reference")
    need(row["diagonal_margin_squared_interval"] == interval_text(diagonal_margin),
         "diagonal margin")
    need(row["exact_signed_output_replay"] is True and
         row["net_cross_term_classification"] == "NEGATIVE_NET_CROSS_TERM" and
         row["diagonal_gain_classification"] == "BETWEEN_1_AND_12_OVER_5" and
         row["frobenius_comparison_classification"] == "ABOVE_FIFTY" and
         row["diagonal_margin_classification"] == "BELOW_QUARTER_MARGIN",
         "row firewall")
    need((signed - diagonal) < 0 and Fraction(1) < diagonal / signed < Fraction(12, 5)
         and f_env / signed > 50 and diagonal_margin.hi < Fraction(1, 16),
         "row thresholds")


def check() -> None:
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    need(parent["payload_sha256"] == PARENT_SHA and
         hashlib.sha256(canonical(parent["payload"])) .hexdigest() == PARENT_SHA,
         "parent provenance")
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "header")
    payload = data["payload"]
    need(hashlib.sha256(canonical(payload)).hexdigest() == data["payload_sha256"],
         "payload digest")
    need(payload["schema"] ==
         "TPC275_SIGNED_FOUR_PACKET_REASSEMBLY_CERTIFICATE_V1", "schema")
    rows = payload["rows"]
    need(len(rows) == 12, "row count")
    seen = set()
    for row in rows:
        key = (row["scale"], row["kernel_exponent"])
        need(key not in seen, "duplicate key")
        seen.add(key)
        replay_row(row)
    theorem = payload["finite_theorem"]
    need(theorem == {
        "claim": "literal signed packet cross terms sharpen but do not close the margin route",
        "diagonal_margin_below_quarter_rows": 12,
        "diagonal_ratio_between_rows": 12,
        "dft_parseval_rows": 12,
        "frobenius_above_fifty_rows": 12,
        "kernel_pair_rows": 6,
        "net_cross_negative_rows": 12,
        "polarization_probe_rows": 72,
        "scale_rows": 6,
        "status": "NUMERICALLY_CERTIFIED_FINITE",
        "total_rows": 12,
    }, "theorem ledger")
    firewall = payload["firewall"]
    need(firewall["TPC275_SIGNED_GRAM_IDENTITY"] == "PROVED_EXACT_FINITE" and
         firewall["TPC275_DFT_LEDGER"] == "PROVED_EXACT_FINITE" and
         firewall["TPC275_POLARIZATION"] == "PROVED_EXACT_FINITE" and
         firewall["TPC275_NET_CROSS_TERM"] ==
         "NUMERICALLY_CERTIFIED_FINITE_NEGATIVE_ALL_12_ROWS" and
         firewall["TPC275_DIAGONAL_ROUTE"] == "INSUFFICIENT_SCOPED" and
         firewall["TPC275_FIXED_POWER_CREDIT"] == 0 and
         firewall["TPC275_SOURCE_LEVEL_SIGNED_CROSS_GRAM"] == "OPEN_ASYMPTOTIC" and
         firewall["TPC275_L2"] == "NONE" and
         firewall["TPC275_FULL_GATE_B"] == "OPEN" and
         firewall["TPC275_TWIN_PRIME_RESULT"] == "NONE",
         "firewall")
    need(payload["round2_clue"] ==
         "COMPILE_SIGNED_CROSS_GRAM_WITH_MARGIN_AND_ENDPOINT_BUDGET",
         "round2 clue")
    print("TPC275_INDEPENDENT_CHECK=PASS rows=12 cross_negative=12 "
          "diagonal_gain=12 diagonal_margin_low=12 "
          "dft_parseval=12 source_signed_cross_gram=OPEN")


if __name__ == "__main__":
    try:
        check()
    except Exception as error:
        print("TPC275_INDEPENDENT_CHECK=FAIL " + str(error))
        raise SystemExit(1)
