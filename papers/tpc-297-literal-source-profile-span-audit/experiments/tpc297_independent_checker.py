#!/usr/bin/env python3
"""Independent source-first replay for TPC-297."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import multiprocessing as mp_pool
import os
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import mpmath as mp

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-297-literal-source-profile-span-audit"
PARENT_RESULT = ROOT / (
    "papers/tpc-295-source-correlation-image-audit/results/"
    "tpc295_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc297_certificate.json"
PARENT_RESULT_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FINITE_RESTRICTED_PROFILE_PROJECTION_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_FOUR_CUTOFF_PROFILE_ATLAS")
SCHEMA = "TPC297_LITERAL_SOURCE_PROFILE_SPAN_CERTIFICATE_V1"
MODULI = (1000000007, 998244353)
PROFILE_CUTOFFS = (3, 5, 7, 11)
MP_DPS = 70
CHECK_RADIUS = mp.mpf("1e-10")

spec = importlib.util.spec_from_file_location("independent_tpc297_engine",
                                              ENGINE_CODE)
if spec is None or spec.loader is None:
    raise RuntimeError("engine unavailable")
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


def as_mp(value: Fraction | int) -> mp.mpf:
    return (mp.mpf(value.numerator) / value.denominator
            if isinstance(value, Fraction) else mp.mpf(value))


def inside(value: mp.mpf, interval: list[str]) -> bool:
    lo, hi = map(mp.mpf, interval)
    tolerance = CHECK_RADIUS * max(mp.mpf(1), abs(value))
    return lo - tolerance <= value <= hi + tolerance


def beta(value: int, cutoff: int) -> Fraction:
    power = ENGINE.prime_power(value)
    lam = Fraction(0) if power is None else Fraction(1, power[1])
    return lam - sum((ENGINE.mobius(d) for d in range(1, cutoff + 1)
                      if value % d == 0), Fraction(0))


def source_first(indices: list[int], values: list[Fraction], height: int,
                 prime: int, exponent: int) -> list[Fraction]:
    output = [Fraction(0) for _ in indices]
    for source, coefficient in zip(indices, values):
        if source % prime == 0:
            continue
        for position, target in enumerate(indices):
            if target == source or target % prime == 0:
                continue
            centered = Fraction(int(target % prime == source % prime), 1)
            centered -= Fraction(1, prime - 1)
            output[position] += (prime * ENGINE.kernel(target - source,
                                                        height, exponent) *
                                 centered * coefficient)
    return output


def modular_rank(matrix: list[list[Fraction]], modulus: int) -> int:
    a = [[(v.numerator % modulus) *
          pow(v.denominator % modulus, modulus - 2, modulus) % modulus
          for v in row] for row in matrix]
    if not a or not a[0]:
        return 0
    rows, columns = len(a), len(a[0])
    rank = 0
    for column in range(columns):
        pivot = next((r for r in range(rank, rows) if a[r][column]), None)
        need(pivot is not None or rank <= min(rows, columns),
             "rank pivot bookkeeping")
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], modulus - 2, modulus)
        a[rank] = [(x * inverse) % modulus for x in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][column]:
                continue
            factor = a[r][column]
            a[r] = [(x - factor * y) % modulus
                    for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def one(item: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    parent_row, actual = item
    mp.mp.dps = MP_DPS
    x, height, q0, cutoff, exponent = (
        int(parent_row["scale"]), int(parent_row["H"]),
        int(parent_row["Q"]), int(parent_row["comparison_cutoff_z"]),
        int(parent_row["kernel_exponent"]))
    indices = list(range(x // 2 + 1, x + 1))
    # The frozen physical source follows the engine's registered critical
    # cutoff rule; the row's comparison cutoff is a separate control.
    _, frozen, _ = ENGINE.source_weights(x, cutoff)
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    columns = [source_first(indices, frozen, height, q, exponent)
               for q in shell]
    profiles = [[beta(t, z) for z in PROFILE_CUTOFFS] for t in indices]
    v_exact = [[sum(columns[j][i] * profiles[i][k]
                    for i in range(len(indices)))
                for k in range(len(PROFILE_CUTOFFS))]
               for j in range(len(shell))]
    ranks = [modular_rank(v_exact, p) for p in MODULI]
    need(ranks == [min(len(shell), 4)] * 2, "independent rank")
    rank = ranks[0]
    A = mp.matrix([[as_mp(columns[j][i]) for j in range(len(shell))]
                   for i in range(len(indices))])
    U = mp.matrix([[as_mp(profiles[i][k]) for k in range(4)]
                   for i in range(len(indices))])
    V = A.T * U
    W = V[:, :rank]
    native = A.T * mp.matrix([as_mp(v) for v in frozen])
    native_norm = (native.T * native)[0]
    labels = {
        "minimum": [int(v) for v in parent_row["minimum_signed_label"]],
        "maxcut": [int(v) for v in parent_row["maxcut_label"]],
        "plus": [1] * len(shell),
    }
    raw: dict[str, mp.mpf] = {}
    for name, label in labels.items():
        b = mp.matrix(label)
        c = mp.qr_solve(W, b)[0]
        residual = W * c - b
        rms = mp.sqrt(mp.fsum(residual[i] ** 2
                              for i in range(len(label))) / len(label))
        raw[name] = rms
        alpha = (native.T * b)[0] / native_norm
        ray = mp.sqrt(mp.fsum((alpha * native[i] - b[i]) ** 2
                              for i in range(len(label))) / len(label))
        need(rms <= ray + mp.mpf("1e-45"), "nested independent residual")
        got = actual["targets"][name]
        need(inside(rms, got["rms_residual"]), "residual interval: " + name)
    need(actual["profile_rank"] == rank, "stored rank")
    need(actual["shell"] == shell, "stored shell")
    return {"minimum": raw["minimum"], "plus": raw["plus"],
            "shell_cardinality": len(shell)}


def main() -> int:
    raw_parent = PARENT_RESULT.read_bytes()
    need(digest(raw_parent) == PARENT_RESULT_SHA256, "parent provenance")
    parent = json.loads(raw_parent)
    need(raw_parent == canonical(parent), "parent canonicality")
    actual_raw = RESULT.read_bytes()
    actual = json.loads(actual_raw)
    need(actual_raw == canonical(actual), "result canonicality")
    need(actual["certificate_version"] == 1 and
         actual["claim_status"] == STATUS, "result header")
    need(actual["payload"]["schema"] == SCHEMA, "result schema")
    mapping = {}
    for row in parent["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))
        mapping[key] = row
    items = []
    for row in actual["payload"]["rows"]:
        key = (int(row["scale"]), int(row["H"]), int(row["Q"]),
               int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))
        items.append((mapping[key], row))
    workers = min(len(items), max(1, os.cpu_count() or 1))
    if workers > 1:
        with mp_pool.get_context("fork").Pool(workers) as pool:
            checks = pool.map(one, items)
    else:
        checks = [one(item) for item in items]
    large = [v for v in checks if v["shell_cardinality"] >= 5]
    need(len(checks) == 18 and len(large) == 17, "check census")
    need(sum(v["minimum"] >= mp.mpf("0.6") for v in large) == 17,
         "weighted separation census")
    need(sum(v["plus"] <= mp.mpf("0.15") for v in checks) == 18,
         "positive capture census")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(actual["payload"])).hexdigest(), "payload hash")
    print("TPC297_INDEPENDENT_CHECK=PASS rows=18 rank3=1 rank4=17 "
          "weighted_large=17 plus=18")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC297_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
