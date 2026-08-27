#!/usr/bin/env python3
"""Independent exact/modular replay for the TPC-285 residue-rank audit."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
PROJECT = ROOT / "papers/tpc-285-prime-shell-residue-rank-obstruction"
PARENT = ROOT / (
    "papers/tpc-284-admissible-source-control-atlas/results/"
    "tpc284_certificate.json")
ENGINE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc285_certificate.json"
PARENT_SHA256 = (
    "0ee28073ba7b460d8ec83393738fa3686c6636d817f243705ef8b1c41699abfc")
ENGINE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
MODULUS = 1_000_000_007
STATUS = (
    "PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_"
    "FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK")
SCHEMA = "TPC285_PRIME_SHELL_RESIDUE_RANK_CERTIFICATE_V1"
BASE_CASES = (
    (64, 15, 4, 4), (96, 20, 5, 4), (128, 24, 5, 4),
    (192, 32, 6, 5), (256, 38, 6, 5), (384, 50, 7, 5),
)


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


def shell(q0: int) -> list[int]:
    values = []
    for q in range(q0 + 1, 2 * q0 + 1):
        if q >= 2 and all(q % d for d in range(2, math.isqrt(q) + 1)):
            values.append(q)
    return values


def entry(u: int, t: int, q: int, deleted: bool) -> int:
    if u % q == 0 or t % q == 0 or (deleted and u == t):
        return 0
    return q - 2 if u % q == t % q else -1


def rank_mod(matrix: list[list[int]]) -> int:
    a = [[value % MODULUS for value in row] for row in matrix]
    m = len(a)
    n = len(a[0]) if m else 0
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inv = pow(a[rank][col], MODULUS - 2, MODULUS)
        a[rank] = [(x * inv) % MODULUS for x in a[rank]]
        for i in range(rank + 1, m):
            factor = a[i][col]
            if factor:
                a[i] = [(x - factor * y) % MODULUS
                        for x, y in zip(a[i], a[rank])]
        rank += 1
        if rank == m:
            break
    return rank


def replay(row: dict[str, Any]) -> tuple[int, int, int, int, bool]:
    scale, height, q, exponent = (int(row["scale"]), int(row["H"]),
                                  int(row["prime"]),
                                  int(row["kernel_exponent"]))
    indices = list(range(scale // 2 + 1, scale + 1))
    active = [u for u in indices if u % q]
    need(sorted({u % q for u in active}) == list(range(1, q)),
         "residue classes")
    # Verify the scaled factorization independently for every full-index entry.
    for u in indices:
        for t in indices:
            expected = 0 if (u % q == 0 or t % q == 0) else (
                (q - 1 if u % q == t % q else 0) - 1)
            need(entry(u, t, q, False) == expected, "factorization entry")
    centered = [[entry(u, t, q, False) for t in active] for u in active]
    deleted = [[entry(u, t, q, True) for t in active] for u in active]
    kernel = []
    invertible = True
    for u in active:
        out = []
        for t in active:
            denominator = height * height + (u - t) * (u - t)
            if denominator % MODULUS == 0:
                invertible = False
                out.append(0)
            else:
                kval = (pow(height, 2 * exponent, MODULUS) *
                         pow(denominator % MODULUS,
                             MODULUS - 1 - exponent, MODULUS)) % MODULUS
                out.append(entry(u, t, q, True) * kval % MODULUS)
        kernel.append(out)
    return (len(active), rank_mod(centered), rank_mod(deleted),
            rank_mod(kernel), invertible)


def check() -> None:
    need(digest(PARENT.read_bytes()) == PARENT_SHA256, "parent hash")
    need(digest(ENGINE.read_bytes()) == ENGINE_SHA256, "engine hash")
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "result canonicality")
    need(data["certificate_version"] == 1 and data["claim_status"] == STATUS,
         "result header")
    payload = data["payload"]
    need(payload["schema"] == SCHEMA and
         data["payload_sha256"] == digest(canonical(payload)), "result hash")
    rows = payload["rows"]
    need(len(rows) == 20, "row count")
    expected_keys = {(x, h, q0, z, s, q)
                     for x, h, q0, z in BASE_CASES
                     for s in (1, 2) for q in shell(q0)}
    actual_keys = {(int(r["scale"]), int(r["H"]), int(r["Q"]),
                    int(r["comparison_cutoff_z"]),
                    int(r["kernel_exponent"]), int(r["prime"])) for r in rows}
    need(actual_keys == expected_keys, "row keys")
    for row in rows:
        active, centered, deleted, kernel, invertible = replay(row)
        q = int(row["prime"])
        need(active == row["active_count"], "active count")
        need(centered == row["centered_scaled_rank_mod_p"] == q - 2,
             "centered rank")
        need(deleted == row["deleted_diagonal_scaled_rank_mod_p"] == active,
             "deleted rank")
        need(kernel == row["kernel_schur_scaled_rank_mod_p"] == active,
             "kernel rank")
        need(row["deleted_diagonal_full_rank_proved_exact"] is True and
             row["block_constant_determinant_factor_negative"] is True,
             "exact deleted-rank marker")
        need(invertible is row["all_modular_denominators_invertible"],
             "denominator audit")
        need(row["factorization_checked_entries"] == row["index_count"] ** 2,
             "entry census")
    need(payload["finite_audit"] == {
        "centered_rank_rows": 20,
        "deleted_diagonal_exact_full_rank_rows": 20,
        "deleted_diagonal_full_active_rank_rows": 20,
        "factorization_rows": 20,
        "fixed_power_credit": 0,
        "kernel_schur_full_active_rank_rows": 20,
        "literal_arithmetic_L2": "OPEN",
        "rows": 20,
    }, "finite census")
    print("TPC285_INDEPENDENT_CHECK=PASS rows=20 factorization=20 "
          "centered_rank=20 deleted_full_rank=20 kernel_full_rank=20")


if __name__ == "__main__":
    try:
        check()
    except (Failure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC285_INDEPENDENT_CHECK=FAIL: " + str(error))
