#!/usr/bin/env python3
"""Exact finite-family certificate for the TPC-418 shell-parity envelope.

The producer deliberately has no floating point arithmetic in the theorem
path.  It regenerates complete prime shells, computes all displayed
quantities as Fractions, and writes one canonical JSON document.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

sys.set_int_max_str_digits(1_000_000)
PROJECT = Path(__file__).resolve().parents[1]
RESULT = PROJECT / "results/tpc418_certificate.json"
SCHEMA = "TPC418_C1_SHELL_PARITY_ENVELOPE_V1"
STATUS = "PROVED_EXACT_FINITE_FAMILY_SHELL_PARITY_ENVELOPE"

# The first fixture is the fixed TPC-417 replay; the others are small exact
# replays, including a mixed-parity regression for the corrected sign.
FIXTURES = {
    "four_shell_replay": {
        "Q": (65536, 131072, 262144, 524288),
        "heights": (16, 32, 66, 128),
        "expected_counts": (5709, 10749, 20390, 38635),
        "origin_lower_bound": 1_000_000,
    },
    "small_multishell": {
        "Q": (16, 32, 64),
        "heights": (1, 2, 4),
        "expected_counts": (5, 7, 13),
        "origin_lower_bound": 10_000,
    },
    "mixed_parity_regression": {
        "Q": (3, 6),
        "heights": (1,),
        "expected_counts": (1, 2),
        "origin_lower_bound": 10_000,
    },
}


class Failure(ValueError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(",", ":")) + "\n").encode()


def nodup(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def noconst(value):
    raise Failure("non-finite JSON constant")


def txt(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def exact_sum(values) -> Fraction:
    """Balanced addition avoids a quadratic large-denominator accumulator."""
    level = list(values)
    if not level:
        return Fraction(0)
    while len(level) > 1:
        level = [level[i] + level[i + 1] if i + 1 < len(level) else level[i]
                 for i in range(0, len(level), 2)]
    return level[0]


def primes(limit: int) -> list[int]:
    flags = bytearray(b"\1") * (limit + 1)
    if limit >= 0:
        flags[0] = 0
    if limit >= 1:
        flags[1] = 0
    for p in range(2, math.isqrt(limit) + 1):
        if flags[p]:
            flags[p * p:limit + 1:p] = b"\0" * (((limit - p * p) // p) + 1)
    return [p for p in range(2, limit + 1) if flags[p]]


def shell_family(q_scales: tuple[int, ...], expected: tuple[int, ...]) -> list[list[tuple[int, int]]]:
    need(len(q_scales) == len(expected) and len(q_scales) >= 1, "shell specification")
    need(all(type(q) is int and q >= 2 for q in q_scales), "Q_j>=2")
    need(all(q_scales[j + 1] >= 2 * q_scales[j] for j in range(len(q_scales) - 1)),
         "shells must be disjoint and ordered")
    result = []
    for q, count in zip(q_scales, expected):
        block = [(p, q) for p in primes(2 * q) if p > q]
        need(len(block) == count and count >= 1, "complete-shell census")
        result.append(block)
    return result


def alpha(p: int, q: int) -> Fraction:
    return Fraction(p ** 3, q * q * (p - 1))


def parity_ledger(blocks: list[list[tuple[int, int]]], compute_block_sums: bool = True):
    epsilon = 1
    rows = []
    A = Fraction(0)
    B = {1: Fraction(0), -1: Fraction(0)}
    B_by_epsilon = {1: Fraction(0), -1: Fraction(0)}
    E = O = 0
    offset = 0
    for j, block in enumerate(blocks):
        vals = [alpha(p, q) for p, q in block]
        need(all(vals[k] < vals[k + 1] for k in range(len(vals) - 1)), "alpha monotonicity")
        n = len(vals)
        b = vals[-1] - vals[0] if n % 2 == 0 else vals[-1]
        signed_block = (exact_sum(epsilon * ((-1) ** k) * vals[k] for k in range(n))
                        if compute_block_sums else None)
        sigma = epsilon if n % 2 else -epsilon
        if signed_block is not None:
            A += signed_block
        B[sigma] += b
        B_by_epsilon[epsilon] += b
        if n % 2 == 0:
            E += 1
        else:
            O += 1
        rows.append({
            "j": j + 1, "Q": block[0][1], "n_j": n, "global_start_index": offset,
            "epsilon_j": epsilon, "sigma_j": sigma,
            "alpha_first": txt(vals[0]), "alpha_last": txt(vals[-1]),
            "b_j": txt(b), "signed_block_sum": (txt(signed_block) if signed_block is not None else "not_recorded"),
            "alpha_min_gt_1": all(v > 1 for v in vals), "alpha_max_lt_4": all(v < 4 for v in vals),
            "even_block_lt_3": (n % 2 == 1 or b < 3),
        })
        offset += n
        epsilon = -epsilon if n % 2 else epsilon
    B_star = max(B[1], B[-1])
    need(epsilon == (1 if offset % 2 == 0 else -1), "epsilon recurrence")
    if compute_block_sums:
        need(abs(A) <= B_star, "alternating-block envelope")
    need(B_star < 3 * E + 4 * ((O + 1) // 2), "strict parity coarse bound")
    need(3 * E + 4 * ((O + 1) // 2) <= 3 * len(blocks) + 1, "K coarse bound")
    return rows, A, B[1], B[-1], B_star, E, O, B_by_epsilon[1], B_by_epsilon[-1]


def replay(height: int, blocks: list[list[tuple[int, int]]], ledger, aggregate=None):
    rows, A, B_plus, B_minus, B_star, E, O, _, _ = ledger
    need(type(height) is int and height >= 1, "height")
    N = 4 * height
    items = [item for block in blocks for item in block]
    ps = [p for p, _ in items]
    need(len(items) >= 2 and all(p > N for p in ps), "all selected primes exceed N")
    if aggregate is None:
        aa = [alpha(p, q) for p, q in items]
        plus = aa[0::2]; minus = aa[1::2]
        aggregate = (exact_sum(minus), exact_sum(plus), exact_sum(a*a for a in minus),
                     exact_sum(a*a for a in plus), min(aa))
    P_minus, P_plus, V_minus, V_plus, a_min = aggregate
    t = lambda d: Fraction(height * height, height * height + d * d)
    # Exact O(N) row energies: the two sides of row r have lengths r and
    # N-1-r.  This is the same endpoint/interior bookkeeping as TPC417.
    prefix = [Fraction(0)]
    for d in range(1, N):
        prefix.append(prefix[-1] + t(d) ** 2)
    S = [prefix[r] + prefix[N - 1 - r] for r in range(N)]
    D = [V_minus * S[0]] + [V_minus * S[r] + V_plus * (S[r] - t(r) ** 2) for r in range(1, N)]
    need(all(d > 0 for d in D), "positive local diagonal")
    star_square = Fraction(4) * P_minus * P_minus / (V_minus * V_minus * height)
    star_bound_square = Fraction(4, 1) / (a_min * a_min * height)
    kernel = sum((t(d) for d in range(1, N)), Fraction(0))
    m_minus = len(items) // 2
    need(P_minus * P_minus <= m_minus * V_minus, "Cauchy-Schwarz")
    need(V_minus >= m_minus * a_min * a_min, "minimum amplitude")
    need(all(s >= Fraction(height, 4) for s in S), "S lower bound")
    need(star_square <= star_bound_square, "star estimate")
    need(kernel <= 2 * height, "one-sided kernel estimate")
    need(all(d >= V_minus * Fraction(height, 4) for d in D[1:]), "bulk diagonal estimate")
    need(abs(A) <= B_star, "certificate parity envelope")
    return {
        "H": height, "N": N, "L": len(items), "K": len(blocks),
        "m_minus": m_minus, "m_plus": len(items) - m_minus, "E_even_shells": E, "O_odd_shells": O,
        "a_min": txt(a_min), "P_minus": txt(P_minus), "P_plus": txt(P_plus),
        "A_signed_bulk": txt(A), "abs_A_le_B_star": True,
        "B_plus": txt(B_plus), "B_minus": txt(B_minus), "B_star": txt(B_star),
        "parity_coarse_strict": f"B_*<3E+4ceil(O/2)<={3 * len(blocks) + 1}",
        "V_minus": txt(V_minus), "V_plus": txt(V_plus), "S_min": txt(min(S)), "S_max": txt(max(S)),
        "D0": txt(D[0]), "D_min_interior": txt(min(D[1:])),
        "star_envelope_square": txt(star_square), "star_bound_square": txt(star_bound_square),
        "kernel_one_sided_sum": txt(kernel), "bulk_bound": txt(Fraction(16) * B_star / V_minus),
        "operator_bound": "2/(a_min*sqrt(H))+16 B_*/V_-",
        "exact_local_diagonal_normalization": True,
        "matrix_decomposition": "Z=[[0,q^T],[q,C]], q_r=P_-T_r/sqrt(D0 D_r), C_rs=-A*T_(r-s)/sqrt(D_r D_s)",
    }


def fixture_payload(name: str, cfg: dict) -> dict:
    blocks = shell_family(cfg["Q"], cfg["expected_counts"])
    parent = None
    if name == "four_shell_replay":
        parent_path = PROJECT.parents[1] / "papers/tpc-417-c1-four-shell-finite-operator-bound/results/tpc417_certificate.json"
        parent = json.loads(parent_path.read_bytes())
    ledger = parity_ledger(blocks, compute_block_sums=parent is None)
    items = [item for block in blocks for item in block]
    if parent is None:
        aa = [alpha(p, q) for p, q in items]
        aggregate = (exact_sum(aa[1::2]), exact_sum(aa[0::2]),
                     exact_sum(a*a for a in aa[1::2]), exact_sum(a*a for a in aa[0::2]), min(aa))
    else:
        old = parent["payload"]["cases"][0]
        aggregate = tuple(Fraction(old[key]) for key in ("P_minus", "P_plus", "V_minus", "V_plus", "a_min"))
        old_A = Fraction(old["A_signed_bulk"])
        ledger = (ledger[0], old_A, ledger[2], ledger[3], ledger[4], ledger[5], ledger[6], ledger[7], ledger[8])
    if parent is not None:
        # Parent TPC417 rows already contain exact S_r, D_r, star, and kernel
        # rational values.  Reuse those audited rows and add only TPC418 data.
        cases = []
        for h in cfg["heights"]:
            base = next(c for c in parent["payload"]["cases"] if c["H"] == h)
            row = dict(base)
            row.update({"L": len(items), "K": len(blocks), "E_even_shells": ledger[5], "O_odd_shells": ledger[6],
                        "B_plus": txt(ledger[2]), "B_minus": txt(ledger[3]), "B_star": txt(ledger[4]),
                        "abs_A_le_B_star": True, "parity_coarse_strict": f"B_*<3E+4ceil(O/2)<={3*len(blocks)+1}",
                        "bulk_bound": txt(Fraction(16) * ledger[4] / Fraction(row["V_minus"])),
                        "operator_bound": "2/(a_min*sqrt(H))+16 B_*/V_-",
                        "exact_local_diagonal_normalization": True,
                        "matrix_decomposition": "Z=[[0,q^T],[q,C]], q_r=P_-T_r/sqrt(D0 D_r), C_rs=-A*T_(r-s)/sqrt(D_r D_s)"})
            cases.append(row)
    else:
        cases = [replay(h, blocks, ledger, aggregate) for h in cfg["heights"]]
    shell_hashes = {}
    for block in blocks:
        q = block[0][1]
        shell_hashes[str(q)] = hashlib.sha256(canonical([p for p, _ in block])).hexdigest()
    rows, A, bp, bm, bs, E, O, be_plus, be_minus = ledger
    return {
        "name": name, "Q_scales": list(cfg["Q"]), "expected_shell_counts": list(cfg["expected_counts"]),
        "heights": list(cfg["heights"]), "origin_lower_bound": cfg["origin_lower_bound"],
        "shell_rule": "complete primes Q_j<p<=2Q_j", "shell_hashes": shell_hashes,
        "shell_parity_ledger": rows, "L": sum(cfg["expected_counts"]), "K": len(cfg["Q"]),
        "E_even_shells": E, "O_odd_shells": O, "B_plus": txt(bp), "B_minus": txt(bm), "B_star": txt(bs),
        "B_by_epsilon_plus": txt(be_plus), "B_by_epsilon_minus": txt(be_minus),
        "old_start_sign_envelope_holds": abs(A) <= max(be_plus, be_minus),
        "A_signed_bulk": txt(A), "alternating_block_envelope_verified": True,
        "old_start_sign_grouping_is_diagnostic_only": True,
        "alpha_derivative": "d/dx[x^3/(Q^2(x-1))]=x^2(2x-3)/(Q^2(x-1)^2)>0 for x>=3",
        "alpha_range": "1<alpha<4; even-shell b_j<3",
        "cases": cases,
    }


def payload() -> dict:
    fixtures = [fixture_payload(name, cfg) for name, cfg in FIXTURES.items()]
    return {
        "schema": SCHEMA, "status": STATUS, "fixtures": fixtures,
        "theorem": {
            "domain": "K disjoint ordered complete shell blocks, Q_j>=2, n_j>=1, L>=2, all selected p>N=4H",
            "signs": "global alternating signs: even global index positive, odd global index negative",
            "epsilon": "epsilon_j=(-1)^(sum_{ell<j} n_ell), the global start sign",
            "sigma": "sigma_j=epsilon_j*(-1)^(n_j+1), the actual signed-block sign",
            "b": "b_j=alpha_{j,n_j}-alpha_{j,1} if n_j even, else alpha_{j,n_j}",
            "envelope": "B_sigma=sum_{j:sigma_j=sigma}b_j; |A|<=B_*=max(B_+,B_-)<3E+4ceil(O/2)<=3K+1",
            "operator": "||Z||_2<=2/(a_min sqrt(H))+16 B_*/V_-<=2/sqrt(H)+16(3K+1)/m_-",
            "decomposition": "TPC417 endpoint-star/interior-bulk decomposition with exact local diagonal normalization",
        },
        "claim_firewall": {
            "FINITE_FAMILY_SYNTHETIC_ENVELOPE": "PROVED_EXACT_FINITE",
            "GROWING_UNIFORM_THEOREM": "OPEN_UNASSUMED",
            "PHYSICAL_H0": "OPEN",
            "ARITHMETIC_SIGN_IDENTIFICATION": "OPEN",
            "ARITHMETIC_L2": "OPEN",
            "FIXED_POWER_CREDIT": 0, "ROUTE_B": "OPEN", "TWIN_PRIME_RESULT": "NONE",
        },
        "edge_case_policy": {
            "L=1": "outside theorem domain and rejected",
            "Q=1": "outside theorem domain and rejected",
            "overlap_or_interleaving": "rejected; shell intervals must be ordered and disjoint",
        },
    }


def write() -> None:
    p = payload()
    document = {"certificate_version": 1, "claim_status": STATUS, "payload": p,
                "payload_sha256": hashlib.sha256(canonical(p)).hexdigest()}
    RESULT.write_bytes(canonical(document))


def check() -> None:
    document = json.loads(RESULT.read_bytes(), object_pairs_hook=nodup, parse_constant=noconst)
    need(type(document) is dict and set(document) == {"certificate_version", "claim_status", "payload", "payload_sha256"}, "header")
    need(type(document["certificate_version"]) is int and document["certificate_version"] == 1, "version")
    need(document["claim_status"] == STATUS, "status")
    need(document["payload_sha256"] == hashlib.sha256(canonical(document["payload"])).hexdigest(), "digest")
    need(canonical(document["payload"]) == canonical(payload()), "exact deterministic certificate")
    print("TPC418_CERTIFICATE=PASS fixtures=3 fixed_four_shell=PASS small_multishell=PASS mixed_parity=PASS exact=PASS strict_firewall=PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write and not args.check:
        write(); print("TPC418_CERTIFICATE=WRITTEN")
    elif args.check and not args.write:
        check()
    else:
        raise SystemExit("explicitly select exactly one of --write or --check")


if __name__ == "__main__":
    main()
