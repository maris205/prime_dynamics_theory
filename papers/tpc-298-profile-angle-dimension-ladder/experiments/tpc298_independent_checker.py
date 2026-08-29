#!/usr/bin/env python3
"""Independent source-first replay for TPC-298."""

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
PROJECT = ROOT / "papers/tpc-298-profile-angle-dimension-ladder"
PARENT_RESULT = ROOT / (
    "papers/tpc-297-literal-source-profile-span-audit/results/"
    "tpc297_certificate.json")
LABEL_RESULT = ROOT / (
    "papers/tpc-295-source-correlation-image-audit/results/"
    "tpc295_certificate.json")
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc298_certificate.json"

PARENT_RESULT_SHA256 = (
    "2ffe4cfd0f564fb2cd63669dccbd8dc99f5911123b3b4a3f8b766262f88d97b6")
LABEL_RESULT_SHA256 = (
    "5e0e723aa93f221f77d5ee84cf20b0ed968adae67669d04e9d70032128212aff")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
STATUS = (
    "PROVED_EXACT_FINITE_PRINCIPAL_ANGLE_IDENTITY_PLUS_"
    "NUMERICALLY_CERTIFIED_FINITE_PROFILE_DIMENSION_LADDER")
SCHEMA = "TPC298_PROFILE_ANGLE_DIMENSION_CERTIFICATE_V1"
PROFILE_CUTOFFS = (
    3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61)
MODULI = (1000000007, 998244353)
MP_DPS = 70
CHECK_RADIUS = mp.mpf("1e-10")

engine_spec = importlib.util.spec_from_file_location(
    "independent_tpc298_engine", ENGINE_CODE)
if engine_spec is None or engine_spec.loader is None:
    raise RuntimeError("engine unavailable")
ENGINE = importlib.util.module_from_spec(engine_spec)
engine_spec.loader.exec_module(ENGINE)


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
    if isinstance(value, Fraction):
        return mp.mpf(value.numerator) / value.denominator
    return mp.mpf(value)


def inside(value: mp.mpf, interval: list[str]) -> bool:
    lo, hi = map(mp.mpf, interval)
    tolerance = CHECK_RADIUS * max(mp.mpf(1), abs(value))
    return lo - tolerance <= value <= hi + tolerance


def row_key(row: dict[str, Any]) -> tuple[int, int, int, int, int]:
    return (int(row["scale"]), int(row["H"]), int(row["Q"]),
            int(row["comparison_cutoff_z"]), int(row["kernel_exponent"]))


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


def mod_fraction(value: Fraction, modulus: int) -> int:
    denominator = value.denominator % modulus
    need(denominator != 0, "noninvertible profile denominator")
    return (value.numerator % modulus) * pow(denominator, modulus - 2,
                                             modulus) % modulus


def modular_rank(matrix: list[list[Fraction]], modulus: int) -> int:
    if not matrix or not matrix[0]:
        return 0
    a = [[mod_fraction(value, modulus) for value in row] for row in matrix]
    rows, columns = len(a), len(a[0])
    rank = 0
    for column in range(columns):
        pivot = next((r for r in range(rank, rows) if a[r][column]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][column], modulus - 2, modulus)
        a[rank] = [(v * inverse) % modulus for v in a[rank]]
        for r in range(rows):
            if r == rank or not a[r][column]:
                continue
            factor = a[r][column]
            a[r] = [(x - factor * y) % modulus
                    for x, y in zip(a[r], a[rank])]
        rank += 1
    return rank


def one(item: tuple[dict[str, Any], dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
    parent_row, actual, label_row = item
    mp.mp.dps = MP_DPS
    x = int(parent_row["scale"])
    height = int(parent_row["H"])
    q0 = int(parent_row["Q"])
    cutoff = int(parent_row["comparison_cutoff_z"])
    exponent = int(parent_row["kernel_exponent"])
    indices = list(range(x // 2 + 1, x + 1))
    # The physical source uses the engine's critical cutoff rule.  The row's
    # comparison cutoff remains a declared control, exactly as in TPC-297.
    _, frozen, _ = ENGINE.source_weights(x, cutoff)
    shell = [q for q in ENGINE.PRIMES if q0 < q <= 2 * q0]
    columns = [source_first(indices, frozen, height, q, exponent)
               for q in shell]
    profiles = [[beta(t, z) for z in PROFILE_CUTOFFS] for t in indices]
    v_exact = [[sum(columns[j][i] * profiles[i][k]
                    for i in range(len(indices)))
                for k in range(len(PROFILE_CUTOFFS))]
               for j in range(len(shell))]
    for k in range(1, len(PROFILE_CUTOFFS) + 1):
        expected = min(k, len(shell))
        ranks = [modular_rank([row[:k] for row in v_exact], modulus)
                 for modulus in MODULI]
        need(ranks == [expected, expected], "independent prefix rank")
        stored_rank = actual["profile_rank_ladder_modular"][k - 1]
        need(stored_rank["expected_rank"] == expected and
             [item["rank"] for item in stored_rank["ranks"]] == ranks,
             "stored rank ladder")
    A = mp.matrix([[as_mp(columns[j][i]) for j in range(len(shell))]
                   for i in range(len(indices))])
    U = mp.matrix([[as_mp(profiles[i][k]) for k in range(len(PROFILE_CUTOFFS))]
                   for i in range(len(indices))])
    V = A.T * U
    labels = {
        "minimum": [int(v) for v in label_row["minimum_signed_label"]],
        "maxcut": [int(v) for v in label_row["maxcut_label"]],
        "plus": [1] * len(shell),
    }
    prefix_count = min(len(shell), len(PROFILE_CUTOFFS))
    raw_by_name: dict[str, list[mp.mpf]] = {name: [] for name in labels}
    for position, k in enumerate(range(1, prefix_count + 1)):
        W = mp.matrix([[V[i, j] for j in range(k)]
                       for i in range(len(shell))])
        singular = mp.svd(W, compute_uv=False)
        need(singular[k - 1] > 0, "independent singular value")
        stored = actual["prefixes"][position]
        need(stored["k"] == k and stored["cutoff"] == PROFILE_CUTOFFS[k - 1],
             "prefix ordering")
        for name, label in labels.items():
            b = mp.matrix(label)
            coefficients = mp.qr_solve(W, b)[0]
            residual = W * coefficients - b
            rms = mp.sqrt(mp.fsum(residual[i] ** 2
                                  for i in range(len(shell))) / len(shell))
            captured = 1 - rms ** 2
            angle = mp.asin(max(mp.mpf(0), min(mp.mpf(1), rms)))
            raw_by_name[name].append(rms)
            saved = stored["targets"][name]
            need(inside(rms, saved["rms_residual"]),
                 "residual interval: " + name)
            need(inside(captured, saved["captured_fraction"]),
                 "capture interval: " + name)
            need(inside(angle, saved["principal_angle_radians"]),
                 "angle interval: " + name)
            need(abs(rms ** 2 + captured - 1) < mp.mpf("1e-55"),
                 "angle Pythagoras")
        if position:
            for name in labels:
                need(raw_by_name[name][-1] <=
                     raw_by_name[name][-2] + mp.mpf("1e-45"),
                     "nested residual monotonicity")
    half = {
        name: next((i + 1 for i, value in enumerate(raw_by_name[name])
                    if value <= mp.mpf("0.5")), None)
        for name in labels
    }
    need(all(value is not None for value in half.values()),
         "independent half threshold")
    need(3 * int(half["minimum"]) >= 2 * len(shell),
         "independent weighted dimension")
    need(int(half["plus"]) <= 6, "independent positive dimension")
    need(all(value <= mp.mpf("1e-8") for value in
             (raw_by_name[name][-1] for name in labels)),
         "independent full capture")
    need(actual["half_rms_dimensions"] == {name: int(value)
                                             for name, value in half.items()},
         "stored half dimensions")
    need(actual["shell"] == shell, "stored shell")
    return {"shell_cardinality": len(shell), "half": half}


def main() -> int:
    raw_parent = PARENT_RESULT.read_bytes()
    need(digest(raw_parent) == PARENT_RESULT_SHA256, "parent provenance")
    parent = json.loads(raw_parent)
    need(raw_parent == canonical(parent), "parent canonicality")
    raw_labels = LABEL_RESULT.read_bytes()
    need(digest(raw_labels) == LABEL_RESULT_SHA256, "label provenance")
    labels = json.loads(raw_labels)
    need(raw_labels == canonical(labels), "label canonicality")
    raw_engine = ENGINE_CODE.read_bytes()
    need(digest(raw_engine) == ENGINE_CODE_SHA256, "engine provenance")
    actual_raw = RESULT.read_bytes()
    actual = json.loads(actual_raw)
    need(actual_raw == canonical(actual), "result canonicality")
    need(actual["certificate_version"] == 1 and
         actual["claim_status"] == STATUS, "result header")
    need(actual["payload"]["schema"] == SCHEMA, "result schema")
    parent_map = {row_key(row): row for row in parent["payload"]["rows"]}
    label_map = {row_key(row): row for row in labels["payload"]["rows"]}
    items = []
    for row in actual["payload"]["rows"]:
        key = row_key(row)
        need(key in parent_map and key in label_map, "row alignment")
        items.append((parent_map[key], row, label_map[key]))
    need(len(items) == 18, "check census")
    workers = min(len(items), max(1, os.cpu_count() or 1))
    if workers > 1:
        with mp_pool.get_context("fork").Pool(workers) as pool:
            checks = pool.map(one, items)
    else:
        checks = [one(item) for item in items]
    need(sum(3 * int(v["half"]["minimum"]) >=
             2 * v["shell_cardinality"] for v in checks) == 18,
         "weighted census")
    need(sum(int(v["half"]["plus"]) <= 6 for v in checks) == 18,
         "positive census")
    need(actual["payload_sha256"] == hashlib.sha256(
        canonical(actual["payload"])).hexdigest(), "payload hash")
    print("TPC298_INDEPENDENT_CHECK=PASS rows=18 prefixes=306 "
          "weighted_ratio_floor=2/3 plus_dim_max=6 full_capture=18")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        print("TPC298_INDEPENDENT_CHECK=FAIL " + str(error), file=sys.stderr)
        raise SystemExit(1)
