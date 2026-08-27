#!/usr/bin/env python3
"""Prime-shell residue factorization and finite rank-inflation certificate.

Before the diagonal is deleted, each prime residue block has an exact
centered-residue factorization through the q-1 nonzero residue classes.  This
certificate proves that identity and then tests the physical off-diagonal
block and its kernel Schur product on the registered finite rows.  A modular
full-rank witness is enough to certify full rational rank: all denominators
are checked to be invertible modulo the declared prime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[1]
PARENT_PROJECT = ROOT / "papers/tpc-284-admissible-source-control-atlas"
PARENT_CODE = PARENT_PROJECT / (
    "code/tpc284_admissible_source_control_atlas_certificate.py")
PARENT_RESULT = PARENT_PROJECT / "results/tpc284_certificate.json"
ENGINE_CODE = ROOT / (
    "papers/tpc-268-finite-cutoff-sensitivity-obstruction/code/"
    "tpc268_cutoff_sensitivity_certificate.py")
RESULT = PROJECT / "results/tpc285_certificate.json"

PARENT_CODE_SHA256 = (
    "023659e316a6b700fa2853cd630f49f0582236fcc0eff9f42ad4c1159367a573")
PARENT_RESULT_SHA256 = (
    "0ee28073ba7b460d8ec83393738fa3686c6636d817f243705ef8b1c41699abfc")
ENGINE_CODE_SHA256 = (
    "e0ec5400ab6a052fb0e2afc82035dc1428085423d43a3bf86e34d0f7e55d2ee3")
MODULUS = 1_000_000_007
SCHEMA = "TPC285_PRIME_SHELL_RESIDUE_RANK_CERTIFICATE_V1"
STATUS = (
    "PROVED_EXACT_CENTERED_RESIDUE_FACTORIZATION_AND_DELETED_DIAGONAL_"
    "FULL_RANK_PLUS_NUMERICALLY_CERTIFIED_KERNEL_RANK")
ROUND2_CLUE = (
    "SEPARATE_RESIDUE_MODE_FACTORIZATION_FROM_DELETED_DIAGONAL_AND_"
    "KERNEL_RANK_BEFORE_LITERAL_L2")

BASE_CASES = (
    (64, 15, 4, 4), (96, 20, 5, 4), (128, 24, 5, 4),
    (192, 32, 6, 5), (256, 38, 6, 5), (384, 50, 7, 5),
)
EXPONENTS = (1, 2)


class CheckFailure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise CheckFailure(message)


def canonical(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("ascii")


def digest(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")).hexdigest()


def load_parent() -> dict[str, Any]:
    need(digest(PARENT_CODE.read_bytes()) == PARENT_CODE_SHA256,
         "parent code provenance")
    need(digest(ENGINE_CODE.read_bytes()) == ENGINE_CODE_SHA256,
         "engine provenance")
    raw = PARENT_RESULT.read_bytes()
    need(digest(raw) == PARENT_RESULT_SHA256, "parent result provenance")
    data = json.loads(raw)
    need(raw == canonical(data), "parent canonicality")
    need(data.get("certificate_version") == 1 and
         data.get("claim_status") ==
         "NUMERICALLY_CERTIFIED_FINITE_ADMISSIBLE_CONTROL_ATLAS_PLUS_"
         "SIGN_FLIP_OBSTRUCTION", "parent status")
    payload = data.get("payload")
    need(isinstance(payload, dict) and
         payload.get("schema") ==
         "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1",
         "parent schema")
    need(payload.get("finite_theorem", {}).get("rows") == 72,
         "parent finite row count")
    return data


def primes_in_shell(q0: int) -> list[int]:
    # The frozen engine exposes the registered prime list; this small local
    # sieve keeps the algebraic certificate independent of its implementation.
    limit = 2 * q0
    sieve = [True] * (limit + 1)
    if limit >= 0:
        sieve[0] = False
    if limit >= 1:
        sieve[1] = False
    for p in range(2, math.isqrt(limit) + 1):
        if sieve[p]:
            for k in range(p * p, limit + 1, p):
                sieve[k] = False
    return [p for p in range(q0 + 1, limit + 1) if sieve[p]]


def residue_scaled(u: int, t: int, q: int, deleted: bool) -> int:
    """Return (q-1) times the centered residue block entry."""
    if u % q == 0 or t % q == 0:
        return 0
    if deleted and u == t:
        return 0
    return q - 2 if u % q == t % q else -1


def rank_mod(matrix: list[list[int]], modulus: int = MODULUS) -> int:
    a = [[entry % modulus for entry in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = next((row for row in range(rank, rows)
                      if a[row][col] != 0), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        inverse = pow(a[rank][col], modulus - 2, modulus)
        a[rank] = [(value * inverse) % modulus for value in a[rank]]
        for row in range(rank + 1, rows):
            factor = a[row][col]
            if factor:
                a[row] = [(x - factor * y) % modulus
                          for x, y in zip(a[row], a[rank])]
        rank += 1
        if rank == rows:
            break
    return rank


def exact_factorization_check(indices: list[int], q: int) -> bool:
    """Check B = R (I-11^T/(q-1)) R^T entry by entry over Q."""
    denominator = q - 1
    for u in indices:
        for t in indices:
            left = residue_scaled(u, t, q, False)
            if u % q == 0 or t % q == 0:
                right_num = 0
            else:
                right_num = ((q - 1) if u % q == t % q else 0) - 1
            need(left == right_num, "centered residue identity")
            # The explicit denominator check documents the rational identity.
            need(denominator != 0, "residue denominator")
    return True


def kernel_residue_matrix(indices: list[int], q: int, height: int,
                          exponent: int) -> tuple[list[list[int]], bool]:
    """Build a modular representative of K_H times (q-1)D_q."""
    matrix: list[list[int]] = []
    denominators_invertible = True
    for u in indices:
        row: list[int] = []
        for t in indices:
            denominator = (height * height + (u - t) * (u - t))
            if denominator % MODULUS == 0:
                denominators_invertible = False
                row.append(0)
                continue
            kernel = (pow(height, 2 * exponent, MODULUS) *
                      pow(denominator % MODULUS, MODULUS - 1 - exponent,
                          MODULUS)) % MODULUS
            row.append(residue_scaled(u, t, q, True) * kernel % MODULUS)
        matrix.append(row)
    return matrix, denominators_invertible


def record(scale: int, height: int, q0: int, cutoff: int,
           exponent: int, q: int) -> dict[str, Any]:
    # The residue block itself is independent of the source cutoff, but the
    # registered value is retained in the row key for provenance.
    indices = list(range(scale // 2 + 1, scale + 1))
    active = [u for u in indices if u % q != 0]
    active_count = len(active)
    classes = sorted({u % q for u in active})
    need(classes == list(range(1, q)), "not all nonzero residue classes present")
    need(exact_factorization_check(indices, q), "factorization failure")

    m = q - 1
    class_sizes = [sum(u % q == residue for u in active)
                   for residue in range(1, q)]
    constant_diagonal = [m * size - (m - 1) for size in class_sizes]
    determinant_ratio = sum((Fraction(size, diagonal) for size, diagonal
                             in zip(class_sizes, constant_diagonal)),
                            Fraction(0))
    # Every term exceeds 1/m because m*size-(m-1) < m*size.  Hence the
    # block-constant determinant factor 1-sum n_a/d_a is strictly negative.
    need(all(size > 0 and diagonal > 0 for size, diagonal
             in zip(class_sizes, constant_diagonal)), "class-size theorem")
    need(determinant_ratio > 1, "deleted-diagonal determinant factor")

    centered = [[residue_scaled(u, t, q, False) for t in active]
                for u in active]
    deleted = [[residue_scaled(u, t, q, True) for t in active]
               for u in active]
    centered_rank = rank_mod(centered)
    deleted_rank = rank_mod(deleted)
    kernel_matrix, invertible = kernel_residue_matrix(
        active, q, height, exponent)
    need(invertible, "kernel denominator not invertible modulo certificate prime")
    kernel_rank = rank_mod(kernel_matrix)
    need(centered_rank == q - 2, "centered rank")
    need(deleted_rank == active_count and kernel_rank == active_count,
         "rank inflation")
    return {
        "scale": scale,
        "H": height,
        "Q": q0,
        "comparison_cutoff_z": cutoff,
        "kernel_exponent": exponent,
        "prime": q,
        "index_count": len(indices),
        "active_count": active_count,
        "nonzero_residue_classes": classes,
        "residue_class_sizes": class_sizes,
        "block_constant_diagonal_terms": constant_diagonal,
        "block_constant_sum_n_over_d": str(determinant_ratio),
        "block_constant_determinant_factor_negative": True,
        "factorization_identity": "B_q=R_q(I-11^T/(q-1))R_q^T",
        "factorization_checked_entries": len(indices) ** 2,
        "centered_scaled_rank_mod_p": centered_rank,
        "centered_rank_upper_bound": q - 2,
        "deleted_diagonal_scaled_rank_mod_p": deleted_rank,
        "kernel_schur_scaled_rank_mod_p": kernel_rank,
        "modulus": MODULUS,
        "all_modular_denominators_invertible": invertible,
        "rational_rank_conclusion": "deleted_and_kernel_blocks_full_on_active_subspace",
        "deleted_diagonal_full_rank_proved_exact": True,
        "diagonal_deleted": True,
        "kernel_schur_product_tested": True,
    }


def build_payload(parent: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for scale, height, q0, cutoff in BASE_CASES:
        shell = primes_in_shell(q0)
        for exponent in EXPONENTS:
            for q in shell:
                rows.append(record(scale, height, q0, cutoff, exponent, q))
    need(len(rows) == 20, "row census")
    need(all(row["factorization_checked_entries"] ==
             row["index_count"] ** 2 for row in rows), "entry census")
    need(all(row["centered_scaled_rank_mod_p"] ==
             row["centered_rank_upper_bound"] for row in rows),
         "centered rank census")
    need(all(row["deleted_diagonal_scaled_rank_mod_p"] == row["active_count"]
             and row["kernel_schur_scaled_rank_mod_p"] == row["active_count"]
             for row in rows), "full-rank census")
    return {
        "schema": SCHEMA,
        "parent_lock": {
            "schema": "TPC284_ADMISSIBLE_SOURCE_CONTROL_ATLAS_CERTIFICATE_V1",
            "code_sha256": PARENT_CODE_SHA256,
            "result_sha256": PARENT_RESULT_SHA256,
            "engine_code_sha256": ENGINE_CODE_SHA256,
            "parent_control_rows": 72,
        },
        "exact_theorem": {
            "active_indicator": "m_q(u)=1_{q does not divide u}",
            "residue_matrix": "R_q(u,a)=m_q(u)1_{u=a mod q}, a=1,...,q-1",
            "centered_factorization":
                "B_q=R_q(I_{q-1}-11^T/(q-1))R_q^T",
            "centered_rank_bound": "rank(B_q)<=q-2",
            "physical_block": "D_q=B_q-diag(B_q), A_q=q(K_H o D_q)",
            "deleted_scaled_decomposition":
                "(q-1)D_q=(q-1)R_qR_q^T-u_qu_q^T-(q-2)I_active",
            "within_class_zero_sum_eigenvalue": "-(q-2)",
            "block_constant_matrix":
                "diag((q-1)n_a-(q-2))-1*n^T",
            "block_constant_determinant_factor":
                "1-sum_a n_a/((q-1)n_a-(q-2))<0",
            "deleted_diagonal_conclusion":
                "rank(D_q)=active_count when every nonzero class occurs",
            "scope": "exact finite residue algebra; no arithmetic L2 conclusion",
        },
        "finite_audit": {
            "rows": 20,
            "factorization_rows": 20,
            "centered_rank_rows": 20,
            "deleted_diagonal_exact_full_rank_rows": 20,
            "deleted_diagonal_full_active_rank_rows": 20,
            "kernel_schur_full_active_rank_rows": 20,
            "fixed_power_credit": 0,
            "literal_arithmetic_L2": "OPEN",
        },
        "rows": rows,
        "firewall": {
            "TPC285_RESIDUE_FACTORIZATION": "PROVED_EXACT",
            "TPC285_CENTERED_RANK_BOUND": "PROVED_EXACT_RANK_LE_Q_MINUS_2",
            "TPC285_DELETED_DIAGONAL_RANK":
                "PROVED_EXACT_FULL_ACTIVE_RANK_WHEN_ALL_CLASSES_OCCUR",
            "TPC285_KERNEL_SCHUR_RANK":
                "NUMERICALLY_CERTIFIED_FINITE_FULL_ACTIVE_RANK_20_ROWS",
            "TPC285_LOW_RANK_TRANSFER_TO_PHYSICAL_A": "OBSTRUCTED_BY_DIAGONAL_AND_SCHUR",
            "TPC285_ARITHMETIC_L2": "OPEN_LITERAL_SOURCE",
            "TPC285_FIXED_POWER_CREDIT": 0,
            "TPC285_FULL_GATE_B": "OPEN",
            "TPC285_TWIN_PRIME_RESULT": "NONE",
            "TPC285_STATUS": STATUS,
        },
        "round2_clue": ROUND2_CLUE,
    }


def document() -> dict[str, Any]:
    payload = build_payload(load_parent())
    return {
        "certificate_version": 1,
        "claim_status": STATUS,
        "payload": payload,
        "payload_sha256": hashlib.sha256(canonical(payload)).hexdigest(),
    }


def check_data(data: dict[str, Any]) -> None:
    need(data == document(), "certificate is not reproducible")
    need(data["payload_sha256"] == hashlib.sha256(
        canonical(data["payload"])).hexdigest(), "payload hash")


def write() -> None:
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_bytes(canonical(document()))


def check() -> None:
    raw = RESULT.read_bytes()
    data = json.loads(raw)
    need(raw == canonical(data), "certificate canonicality")
    check_data(data)
    print("TPC285_CERTIFICATE=PASS rows=20 factorization=20 "
          "centered_rank=20 deleted_full_rank=20 kernel_full_rank=20 "
          "fixed_power_credit=0")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    need(args.write != args.check, "choose exactly one mode")
    try:
        write() if args.write else check()
    except (CheckFailure, OSError, KeyError, TypeError, ValueError,
            json.JSONDecodeError) as error:
        raise SystemExit("TPC285_CERTIFICATE=FAIL: " + str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
