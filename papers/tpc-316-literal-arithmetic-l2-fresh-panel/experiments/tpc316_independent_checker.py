#!/usr/bin/env python3
"""Independent replay for TPC-316.

The checker does not import the producer.  It rebuilds the prime shells,
the difference/residue count for the Frobenius mass, and the coordinate-column
energies from the literal matrix formula.  A small direct enumeration is also
used to audit the counting reduction before the two-panel certificate is
accepted.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)
getcontext().prec = 120

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-316-literal-arithmetic-l2-fresh-panel"
RESULT = PROJECT / "results/tpc316_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_"
    "TWO_SCALE_OBSTRUCTION")
SCHEMA = "TPC316_LITERAL_ARITHMETIC_L2_FRESH_PANEL_V1"
SCALES = (640, 1280)
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PROBE_DIVISIONS = 4


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


def fraction_digest(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}\n".encode("ascii")
    ).hexdigest()


def decimal_text(value: Fraction) -> str:
    return format(Decimal(value.numerator) / Decimal(value.denominator),
                  ".18g")


def primes_up_to(limit: int) -> list[int]:
    sieve = [True] * (limit + 1)
    if limit >= 0:
        sieve[0] = False
    if limit >= 1:
        sieve[1] = False
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for multiple in range(p * p, limit + 1, p):
                sieve[multiple] = False
    return [p for p, flag in enumerate(sieve) if flag]


PRIMES = primes_up_to(160)


def shell(q0: int) -> list[int]:
    return [p for p in PRIMES if q0 < p <= 2 * q0]


def interval(scale: int) -> tuple[int, int, int]:
    lo, hi = scale // 2 + 1, scale
    return lo, hi, hi - lo + 1


def kernel(delta: int, exponent: int) -> Fraction:
    delta = abs(delta)
    return Fraction(HEIGHT ** (2 * exponent),
                    (HEIGHT * HEIGHT + delta * delta) ** exponent)


def count_residue(lo: int, hi: int, residue: int, p: int) -> int:
    first = lo + (residue - lo) % p
    return 0 if first > hi else (hi - first) // p + 1


def direct_valid_pairs(lo: int, hi: int, delta: int, p: int) -> int:
    total = 0
    for t in range(lo, hi + 1):
        u = t + delta
        if lo <= u <= hi and u != t and u % p != 0 and t % p != 0:
            total += 1
    return total


def counted_valid_pairs(lo: int, hi: int, delta: int, p: int) -> int:
    pair_count = (hi - lo + 1) - abs(delta)
    tlo = max(lo, lo - delta)
    thi = min(hi, hi - delta)
    need(thi - tlo + 1 == pair_count, "pair slice")
    if delta % p == 0:
        return pair_count - count_residue(tlo, thi, 0, p)
    return (pair_count - count_residue(tlo, thi, 0, p)
            - count_residue(tlo, thi, -delta, p))


def mass_by_count(scale: int, q0: int, exponent: int) -> Fraction:
    lo, hi, count = interval(scale)
    total = Fraction(0)
    for p in shell(q0):
        p2 = p * p
        for delta in range(-(count - 1), count):
            if delta == 0:
                continue
            valid = counted_valid_pairs(lo, hi, delta, p)
            if delta % p == 0:
                c2 = Fraction((p - 2) ** 2, (p - 1) ** 2)
            else:
                c2 = Fraction(1, (p - 1) ** 2)
            total += p2 * kernel(delta, exponent) ** 2 * c2 * valid
    return total


def direct_entry(delta: int, p: int, exponent: int) -> Fraction:
    centered = (Fraction(1) if delta % p == 0 else Fraction(0))
    centered -= Fraction(1, p - 1)
    return p * kernel(delta, exponent) * centered


def direct_mass_small(lo: int, hi: int, p_values: list[int],
                      exponent: int) -> Fraction:
    total = Fraction(0)
    for p in p_values:
        for u in range(lo, hi + 1):
            for t in range(lo, hi + 1):
                if u == t or u % p == 0 or t % p == 0:
                    continue
                total += direct_entry(u - t, p, exponent) ** 2
    return total


def column_energy(scale: int, q0: int, exponent: int, column: int
                  ) -> Fraction:
    lo, hi, count = interval(scale)
    need(lo <= column <= hi, "column domain")
    total = Fraction(0)
    for p in shell(q0):
        for u in range(lo, hi + 1):
            if u == column or u % p == 0 or column % p == 0:
                continue
            total += direct_entry(u - column, p, exponent) ** 2
    return total


def probes(count: int) -> tuple[int, ...]:
    return tuple(sorted({0, count - 1,
                         (count - 1) // 4,
                         2 * (count - 1) // 4,
                         3 * (count - 1) // 4}))


def check_metric(raw: Any, value: Fraction, label: str) -> None:
    need(isinstance(raw, dict), label + " metric type")
    need(raw.get("rational_sha256") == fraction_digest(value),
         label + " rational digest")
    need(raw.get("decimal") == decimal_text(value), label + " decimal")


def main() -> int:
    try:
        need(digest(ENGINE_CODE.read_bytes()) == ENGINE_SHA256,
             "engine provenance")
        raw = RESULT.read_bytes()
        document = json.loads(raw)
        need(raw == canonical(document), "certificate canonicality")
        need(document.get("certificate_version") == 1 and
             document.get("claim_status") == STATUS, "certificate header")
        payload = document.get("payload")
        need(isinstance(payload, dict) and
             payload.get("schema") == SCHEMA and
             document.get("payload_sha256") == hashlib.sha256(
                 canonical(payload)).hexdigest(), "payload")

        parent = payload["parent_lock"]
        need(parent["engine_sha256"] == ENGINE_SHA256 and
             parent["engine_path"] == str(ENGINE_CODE.relative_to(ROOT)),
             "parent lock")
        protocol = payload["protocol"]
        need(protocol["source_scales"] == list(SCALES) and
             protocol["fresh_scale"] == 1280 and
             protocol["height"] == HEIGHT and
             protocol["Q_anchors"] == list(Q_ANCHORS) and
             protocol["kernel_exponents"] == list(EXPONENTS) and
             protocol["deleted_diagonal"] is True and
             protocol["domain"] == "ell^2(I_X)" and
             protocol["codomain"] == "ell^2(S_Q x I_X)", "protocol")

        # First audit the count formula against literal pair enumeration on a
        # separate small interval, including both signs of every difference.
        small_lo, small_hi = 11, 26
        for p in (3, 5, 7, 11):
            for delta in range(-(small_hi - small_lo),
                               small_hi - small_lo + 1):
                if delta == 0:
                    continue
                need(counted_valid_pairs(small_lo, small_hi, delta, p) ==
                     direct_valid_pairs(small_lo, small_hi, delta, p),
                     "residue-count replay")
        need(mass_by_count(32, 3, 1) ==
             direct_mass_small(17, 32, [5], 1),
             "small direct mass replay")

        rows = payload.get("rows", [])
        need(isinstance(rows, list) and len(rows) == 16, "row census")
        row_values: dict[tuple[int, int, int], Fraction] = {}
        for row in rows:
            scale = int(row["scale"])
            q0 = int(row["Q"])
            exponent = int(row["kernel_exponent"])
            lo, hi, count = interval(scale)
            sh = shell(q0)
            need(row["source_interval"] == [lo, hi] and
                 row["source_count"] == count and row["height"] == HEIGHT and
                 row["shell"] == sh and
                 row["shell_cardinality"] == len(sh) and
                 row["operator_rows"] == count * len(sh) and
                 row["operator_columns"] == count, "row geometry")
            need(row["probe_offsets"] == list(probes(count)),
                 "probe offsets")
            hs = mass_by_count(scale, q0, exponent)
            row_values[(scale, q0, exponent)] = hs
            check_metric(row["hilbert_schmidt_squared"], hs,
                         "Hilbert-Schmidt mass")
            check_metric(row["normalized_hilbert_schmidt_squared"],
                         hs / count, "normalized Hilbert-Schmidt mass")
            stored_probes = row["probe_columns"]
            need(len(stored_probes) == len(probes(count)), "probe census")
            exact_probe: dict[int, Fraction] = {}
            for stored, offset in zip(stored_probes, probes(count)):
                column = lo + offset
                value = column_energy(scale, q0, exponent, column)
                exact_probe[column] = value
                need(stored["column"] == column and
                     stored["offset"] == offset, "probe geometry")
                check_metric(stored["energy"], value, "probe energy")
                check_metric(stored["normalized_energy"], value / count,
                             "normalized probe energy")
            best_value = max(exact_probe.values())
            best_column = min(c for c, value in exact_probe.items()
                              if value == best_value)
            need(row["best_probe_column"] == best_column, "best probe")
            check_metric(row["best_probe_energy"], best_value,
                         "best probe energy")
            check_metric(row["best_probe_normalized_energy"],
                         best_value / count, "best normalized probe")
            check_metric(row["frobenius_over_probe"], hs / best_value,
                         "Frobenius gap")
            need(best_value > 0 and best_value <= hs,
                 "finite sandwich")

        comparisons = payload.get("comparisons", [])
        need(len(comparisons) == 8, "comparison census")
        for comparison in comparisons:
            q0 = int(comparison["Q"])
            exponent = int(comparison["kernel_exponent"])
            low = row_values[(640, q0, exponent)] / 320
            high = row_values[(1280, q0, exponent)] / 640
            need(comparison["lower_scale"] == 640 and
                 comparison["upper_scale"] == 1280 and
                 comparison["strictly_increased"] is True and high > low,
                 "two-scale ordering")
            check_metric(comparison["lower_normalized_hs"], low,
                         "lower comparison")
            check_metric(comparison["upper_normalized_hs"], high,
                         "upper comparison")
            check_metric(comparison["upper_over_lower"], high / low,
                         "comparison ratio")
            need(comparison["comparison_scope"] ==
                 "finite_two_panel_observation_only", "comparison scope")

        audit = payload["finite_audit"]
        need(audit["scales"] == 2 and audit["rows"] == 16 and
             audit["comparison_rows"] == 8 and
             audit["probe_columns_per_row"] == 5 and
             audit["normalized_hs_increased_rows"] == 8 and
             audit["normalized_hs_increased_all_rows"] is True and
             audit["fixed_power_credit"] == 0 and
             audit["growing_theorem"] == "OPEN", "audit summary")
        firewall = payload["claim_firewall"]
        need(firewall["TPC316_FINITE_LITERAL_OPERATOR"] ==
             "PROVED_EXACT_FINITE" and
             firewall["TPC316_FROBENIUS_L2_ENVELOPE"] ==
             "PROVED_EXACT_FINITE" and
             firewall["TPC316_NORMALIZED_HS_TWO_SCALE_RISE"] ==
             "NUMERICALLY_CERTIFIED_FINITE_8_OF_8" and
             firewall["TPC316_ARITHMETIC_ADVANCE"] == "NO" and
             firewall["TPC316_FIXED_POWER_CREDIT"] == 0 and
             firewall["TPC316_GROWING_ARITHMETIC_L2"] == "OPEN" and
             firewall["TPC316_OPERATOR_NORM_DECAY"] == "OPEN" and
             firewall["TPC316_FULL_GATE_B"] == "OPEN" and
             firewall["TPC316_TWIN_PRIME_RESULT"] == "NONE", "firewall")
    except (Failure, OSError, json.JSONDecodeError, KeyError, ValueError) as error:
        print("TPC316_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC316_INDEPENDENT_CHECK=PASS scales=2 rows=16 comparisons=8 "
          "direct_small_panel=1 normalized_hs_rise=8")
    return 0


if __name__ == "__main__":
    if "--check" not in sys.argv[1:]:
        raise SystemExit("explicit --check is required")
    raise SystemExit(main())
