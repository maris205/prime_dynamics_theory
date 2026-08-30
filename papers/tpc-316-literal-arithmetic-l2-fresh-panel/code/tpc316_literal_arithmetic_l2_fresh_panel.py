#!/usr/bin/env python3
"""TPC-316: an exact finite literal arithmetic L2 envelope.

TPC-315 left the source-level arithmetic L2 interface open.  This release
instantiates the literal deleted-diagonal prime-shell operator as a map from
the full source space ell^2(I_X) to ell^2(S_Q x I_X).  The Hilbert--Schmidt
mass is reduced to exact difference/residue counts, and a small deterministic
set of coordinate vectors supplies exact lower witnesses.  Two disjoint
source panels are compared only as a finite diagnostic; no growing estimate
or power saving is inferred.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import multiprocessing as mp_pool
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
RESULT = PROJECT / "results/tpc316_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")

ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")

SCHEMA = "TPC316_LITERAL_ARITHMETIC_L2_FRESH_PANEL_V1"
STATUS = (
    "PROVED_EXACT_FINITE_LITERAL_ARITHMETIC_L2_ENVELOPE_PLUS_"
    "TWO_SCALE_OBSTRUCTION")
ROUND2_CLUE = (
    "REPLACE_THE_FROBENIUS_ENVELOPE_BY_A_GROWING_OPERATOR_OR_"
    "ARITHMETIC_CANCELLATION_ESTIMATE_WITHOUT_IMPORTING_A_POWER_CLAIM")

SCALES = (640, 1280)
FRESH_SCALE = 1280
HEIGHT = 66
Q_ANCHORS = (24, 36, 54, 80)
EXPONENTS = (1, 2)
PROBE_DIVISIONS = 4
MODULUS = 1_000_000_007

ENGINE_SPEC = importlib.util.spec_from_file_location(
    "locked_tpc268_for_tpc316", ENGINE_CODE)
if ENGINE_SPEC is None or ENGINE_SPEC.loader is None:
    raise RuntimeError("TPC-268 arithmetic engine unavailable")
ENGINE = importlib.util.module_from_spec(ENGINE_SPEC)
ENGINE_SPEC.loader.exec_module(ENGINE)


class CheckFailure(RuntimeError):
    """A fail-closed certificate error."""


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


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


def decimal_text(value: Fraction, digits: int = 18) -> str:
    return ENGINE.decimal_text(value, digits=digits)


def metric(value: Fraction) -> dict[str, str]:
    """Store a reproducible decimal view and an exact rational digest."""
    return {
        "decimal": decimal_text(value),
        "rational_sha256": fraction_digest(value),
    }


def primes_up_to(limit: int) -> list[int]:
    # This local sieve is deliberately independent of the engine's list when
    # validating the finite shell geometry.
    sieve = bytearray(b"\x01") * (limit + 1)
    if limit >= 0:
        sieve[0] = 0
    if limit >= 1:
        sieve[1] = 0
    for prime in range(2, math.isqrt(limit) + 1):
        if sieve[prime]:
            start = prime * prime
            sieve[start:limit + 1:prime] = b"\x00" * (
                (limit - start) // prime + 1)
    return [value for value in range(2, limit + 1) if sieve[value]]


def shell_for(q0: int) -> list[int]:
    return [prime for prime in primes_up_to(2 * max(Q_ANCHORS))
            if q0 < prime <= 2 * q0]


def source_interval(scale: int) -> tuple[int, int, int]:
    lo = scale // 2 + 1
    hi = scale
    count = hi - lo + 1
    need(scale % 2 == 0 and count == scale // 2,
         "dyadic source panel")
    return lo, hi, count


def kernel(shift: int, height: int, exponent: int) -> Fraction:
    """The exact TPC-268 kernel, with the sign removed by abs(shift)."""
    shift = abs(shift)
    return Fraction(height ** (2 * exponent),
                    (height * height + shift * shift) ** exponent)


def matrix_entry(prime: int, u: int, t: int, height: int,
                 exponent: int) -> Fraction:
    """Return one literal deleted-diagonal matrix entry."""
    if u == t or u % prime == 0 or t % prime == 0:
        return Fraction(0)
    centered = (Fraction(1) if u % prime == t % prime else Fraction(0))
    centered -= Fraction(1, prime - 1)
    return prime * kernel(u - t, height, exponent) * centered


def residue_count(lo: int, hi: int, residue: int, modulus: int) -> int:
    """Count integers in [lo,hi] in one residue class."""
    need(lo <= hi and modulus > 0, "residue-count domain")
    residue %= modulus
    first = lo + (residue - lo) % modulus
    return 0 if first > hi else 1 + (hi - first) // modulus


def pair_slice(lo: int, hi: int, delta: int) -> tuple[int, int, int]:
    """Return the t-range and pair count for u=t+delta."""
    tlo = max(lo, lo - delta)
    thi = min(hi, hi - delta)
    count = max(0, thi - tlo + 1)
    need(count == (hi - lo + 1) - abs(delta),
         "difference-pair count")
    return tlo, thi, count


def valid_pair_count(tlo: int, thi: int, pair_count: int,
                     delta: int, prime: int) -> tuple[int, Fraction]:
    """Count nonzero endpoint pairs and return the squared centered weight."""
    if delta % prime == 0:
        # The two endpoints have the same nonzero residue.
        valid = pair_count - residue_count(tlo, thi, 0, prime)
        centered_squared = Fraction((prime - 2) ** 2,
                                    (prime - 1) ** 2)
    else:
        # The two excluded endpoint residues are distinct.
        valid = (pair_count - residue_count(tlo, thi, 0, prime)
                 - residue_count(tlo, thi, -delta, prime))
        centered_squared = Fraction(1, (prime - 1) ** 2)
    need(valid >= 0, "negative valid-pair count")
    return valid, centered_squared


def hilbert_schmidt_squared(scale: int, height: int, q0: int,
                            exponent: int) -> Fraction:
    """Compute sum_(p,u,t) K_(p,u,t)^2 by exact counting.

    For a fixed difference delta=u-t, the only dependence on (u,t) left
    after squaring is the count of admissible endpoint residues.  This is an
    exact regrouping, not a numerical approximation.
    """
    lo, hi, count = source_interval(scale)
    shell = shell_for(q0)
    kernels = {delta: kernel(delta, height, exponent)
               for delta in range(1, count)}
    total = Fraction(0)
    for prime in shell:
        prime_squared = prime * prime
        for magnitude in range(1, count):
            for delta in (magnitude, -magnitude):
                tlo, thi, pair_count = pair_slice(lo, hi, delta)
                valid, centered_squared = valid_pair_count(
                    tlo, thi, pair_count, delta, prime)
                total += (prime_squared * kernels[magnitude] ** 2
                          * centered_squared * valid)
    need(total > 0, "positive Hilbert-Schmidt mass")
    return total


def probe_offsets(count: int) -> tuple[int, ...]:
    offsets = {0, count - 1}
    for divisor in range(PROBE_DIVISIONS + 1):
        offsets.add((divisor * (count - 1)) // PROBE_DIVISIONS)
    return tuple(sorted(offsets))


def column_energy(scale: int, height: int, q0: int, exponent: int,
                  column: int) -> Fraction:
    """Exact squared output of A on one coordinate basis vector."""
    lo, hi, count = source_interval(scale)
    need(lo <= column <= hi, "probe column outside source")
    total = Fraction(0)
    for prime in shell_for(q0):
        if column % prime == 0:
            continue
        for u in range(lo, hi + 1):
            if u == column or u % prime == 0:
                continue
            coefficient = matrix_entry(prime, u, column, height, exponent)
            total += coefficient * coefficient
    need(total >= 0 and count > 0, "column energy")
    return total


def build_row(specification: tuple[int, int, int]) -> dict[str, Any]:
    scale, q0, exponent = specification
    lo, hi, count = source_interval(scale)
    shell = shell_for(q0)
    hs2 = hilbert_schmidt_squared(scale, HEIGHT, q0, exponent)
    probes: list[dict[str, Any]] = []
    exact_probe_energies: dict[int, Fraction] = {}
    for offset in probe_offsets(count):
        column = lo + offset
        energy = column_energy(scale, HEIGHT, q0, exponent, column)
        exact_probe_energies[column] = energy
        probes.append({
            "column": column,
            "offset": offset,
            "energy": metric(energy),
            "normalized_energy": metric(energy / count),
        })
    best_column = min(
        (column for column, value in exact_probe_energies.items()
         if value == max(exact_probe_energies.values())))
    best_energy = exact_probe_energies[best_column]
    upper_normalized = hs2 / count
    lower_normalized = best_energy / count
    need(lower_normalized <= upper_normalized and lower_normalized > 0,
         "finite L2 sandwich")
    return {
        "scale": scale,
        "source_interval": [lo, hi],
        "source_count": count,
        "Q": q0,
        "kernel_exponent": exponent,
        "height": HEIGHT,
        "shell": shell,
        "shell_cardinality": len(shell),
        "operator_rows": count * len(shell),
        "operator_columns": count,
        "probe_offsets": list(probe_offsets(count)),
        "probe_columns": probes,
        "best_probe_column": best_column,
        "best_probe_energy": metric(best_energy),
        "best_probe_normalized_energy": metric(lower_normalized),
        "hilbert_schmidt_squared": metric(hs2),
        "normalized_hilbert_schmidt_squared": metric(upper_normalized),
        "frobenius_over_probe": metric(hs2 / best_energy),
        "finite_sandwich": True,
    }


def build_comparison(low: dict[str, Any], high: dict[str, Any]
                     ) -> dict[str, Any]:
    need(low["scale"] < high["scale"] and low["Q"] == high["Q"] and
         low["kernel_exponent"] == high["kernel_exponent"],
         "comparison pairing")
    # Reconstruct the exact fractions from the calculations rather than from
    # display strings.  The comparison is recomputed by build_payload.
    low_hs = hilbert_schmidt_squared(low["scale"], HEIGHT, low["Q"],
                                     low["kernel_exponent"])
    high_hs = hilbert_schmidt_squared(high["scale"], HEIGHT, high["Q"],
                                      high["kernel_exponent"])
    low_n = low_hs / low["source_count"]
    high_n = high_hs / high["source_count"]
    ratio = high_n / low_n
    return {
        "Q": low["Q"],
        "kernel_exponent": low["kernel_exponent"],
        "lower_scale": low["scale"],
        "upper_scale": high["scale"],
        "lower_normalized_hs": metric(low_n),
        "upper_normalized_hs": metric(high_n),
        "upper_over_lower": metric(ratio),
        "strictly_increased": ratio > 1,
        "comparison_scope": "finite_two_panel_observation_only",
    }


def build_payload() -> dict[str, Any]:
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "TPC-268 engine provenance")
    specifications = [(scale, q0, exponent)
                      for scale in SCALES for q0 in Q_ANCHORS
                      for exponent in EXPONENTS]
    workers_text = os.environ.get("TPC316_WORKERS", "1")
    try:
        workers = max(1, min(len(specifications), int(workers_text)))
    except ValueError:
        workers = 1
    if workers > 1:
        try:
            with mp_pool.get_context("fork").Pool(processes=workers) as pool:
                rows = pool.map(build_row, specifications)
        except (AttributeError, OSError, RuntimeError):
            rows = [build_row(specification) for specification in specifications]
    else:
        rows = [build_row(specification) for specification in specifications]
    need(len(rows) == 16, "row census")
    indexed = {(row["scale"], row["Q"], row["kernel_exponent"]): row
               for row in rows}
    need(len(indexed) == 16, "unique row census")
    comparisons = []
    for q0 in Q_ANCHORS:
        for exponent in EXPONENTS:
            comparisons.append(build_comparison(
                indexed[(SCALES[0], q0, exponent)],
                indexed[(SCALES[1], q0, exponent)]))
    need(len(comparisons) == 8, "comparison census")
    increased = sum(item["strictly_increased"] for item in comparisons)
    need(increased == 8, "normalized Hilbert-Schmidt growth observation")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "physical_engine": "TPC-268 literal rational deleted-diagonal engine",
            "engine_path": str(ENGINE_CODE.relative_to(ROOT)),
            "engine_sha256": ENGINE_CODE_SHA256,
            "parent_route_context": "TPC-315 fresh source interval [641,1280]",
        },
        "protocol": {
            "source_scales": list(SCALES),
            "fresh_scale": FRESH_SCALE,
            "source_intervals": {
                str(scale): [scale // 2 + 1, scale] for scale in SCALES
            },
            "height": HEIGHT,
            "Q_anchors": list(Q_ANCHORS),
            "kernel_exponents": list(EXPONENTS),
            "shell_rule": "S_Q={p prime: Q<p<=2Q}",
            "domain": "ell^2(I_X)",
            "codomain": "ell^2(S_Q x I_X)",
            "matrix_entry": (
                "1_{t!=u,p not_divides ut} p H^(2s)/(H^2+(u-t)^2)^s "
                "(1_{u==t mod p}-1/(p-1))"),
            "deleted_diagonal": True,
            "probe_rule": "five equally spaced endpoint-inclusive coordinate columns",
            "normalization": "divide output energy and Hilbert-Schmidt mass by source count N",
            "arithmetic": "exact Fraction; no floating-point matrix entries",
        },
        "exact_theorem": {
            "entry_rationality": (
                "every matrix entry is rational under the displayed finite formula"),
            "finite_frobenius_interface": (
                "||A beta||_2^2 <= ||A||_HS^2 ||beta||_2^2 "
                "for every beta in ell^2(I_X)"),
            "mean_square_interface": (
                "N^(-1)||A beta||_2^2 <= (HS^2/N)||beta||_2^2"),
            "coordinate_lower_witness": (
                "||A||_(2->2)^2 >= ||A e_t||_2^2 for each declared probe column"),
            "count_reduction": (
                "HS^2 is exactly the sum over differences and admissible residue counts"),
            "scope": "finite scales 640 and 1280 only",
        },
        "finite_audit": {
            "scales": 2,
            "rows": 16,
            "comparison_rows": 8,
            "probe_columns_per_row": 5,
            "finite_sandwich_rows": 16,
            "normalized_hs_increased_rows": increased,
            "normalized_hs_increased_all_rows": increased == 8,
            "exact_hilbert_schmidt_rows": 16,
            "fixed_power_credit": 0,
            "growing_theorem": "OPEN",
        },
        "claim_firewall": {
            "TPC316_FINITE_LITERAL_OPERATOR": "PROVED_EXACT_FINITE",
            "TPC316_FROBENIUS_L2_ENVELOPE": "PROVED_EXACT_FINITE",
            "TPC316_COORDINATE_LOWER_WITNESSES": "PROVED_EXACT_FINITE",
            "TPC316_NORMALIZED_HS_TWO_SCALE_RISE":
                "NUMERICALLY_CERTIFIED_FINITE_8_OF_8",
            "TPC316_ENVELOPE_GAP": "NUMERICALLY_CERTIFIED_FINITE",
            "TPC316_GROWING_ARITHMETIC_L2": "OPEN",
            "TPC316_OPERATOR_NORM_DECAY": "OPEN",
            "TPC316_ARITHMETIC_ADVANCE": "NO",
            "TPC316_FIXED_POWER_CREDIT": 0,
            "TPC316_FULL_GATE_B": "OPEN",
            "TPC316_TWIN_PRIME_RESULT": "NONE",
        },
        "round2_clue": ROUND2_CLUE,
        "rows": rows,
        "comparisons": comparisons,
    }


def build_document() -> dict[str, Any]:
    payload = build_payload()
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def write_certificate() -> None:
    RESULT.write_bytes(canonical(build_document()))


def check_certificate() -> None:
    raw = RESULT.read_bytes()
    stored = json.loads(raw)
    need(raw == canonical(stored), "certificate canonicality")
    need(stored.get("certificate_version") == 1 and
         stored.get("claim_status") == STATUS, "certificate header")
    payload = stored.get("payload")
    need(isinstance(payload, dict) and
         stored.get("payload_sha256") == hashlib.sha256(
             canonical(payload)).hexdigest(), "certificate payload hash")
    expected = build_payload()
    need(payload == expected, "certificate does not replay")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("exactly one of --write or --check is required")
    try:
        if args.write:
            write_certificate()
            print("TPC316_CERTIFICATE=WRITTEN")
        else:
            check_certificate()
            print("TPC316_CERTIFICATE=PASS scales=2 rows=16 comparisons=8 "
                  "probe_columns=80 normalized_hs_rise=8 fixed_power_credit=0")
    except (CheckFailure, OSError, json.JSONDecodeError) as error:
        print("TPC316_CERTIFICATE=FAIL " + str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
