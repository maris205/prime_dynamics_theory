#!/usr/bin/env python3
"""Exact ledgers and finite reproduction for TPC-237."""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from math import gcd


class ReassemblyFailure(RuntimeError):
    """Raised when a source lock or exact certificate condition fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ReassemblyFailure(message)


def fraction_text(value: Fraction) -> str:
    require(type(value) is Fraction, "fraction-text input")
    return str(value)


def is_prime(n: int) -> bool:
    require(type(n) is int, "prime input type")
    if n < 2:
        return False
    return all(n % p for p in range(2, int(n**0.5) + 1))


def primes_in_shell(Q: int) -> tuple[int, ...]:
    require(type(Q) is int and Q >= 2, "shell scale")
    return tuple(q for q in range(Q + 1, 2 * Q + 1) if is_prime(q))


def mobius(n: int) -> int:
    require(type(n) is int and n >= 1, "Mobius input")
    remaining = n
    sign = 1
    p = 2
    while p * p <= remaining:
        if remaining % p == 0:
            remaining //= p
            sign = -sign
            if remaining % p == 0:
                return 0
            while remaining % p == 0:
                remaining //= p
        p += 1
    if remaining > 1:
        sign = -sign
    return sign


def validate_reduced_frequency_pairs(pairs: tuple[tuple[int, int], ...], U: int) -> None:
    require(type(pairs) is tuple and type(U) is int and U >= 1, "frequency input types")
    reduced: list[Fraction] = []
    for pair in pairs:
        require(type(pair) is tuple and len(pair) == 2, "frequency pair shape")
        h, a = pair
        require(type(h) is int and type(a) is int and 1 <= h <= U and 0 <= a < h,
                "frequency pair range")
        require(gcd(a, h) == 1, "nonprimitive frequency forbidden")
        reduced.append(Fraction(a, h))
    require(len(reduced) == len(set(reduced)), "duplicate reduced frequency forbidden")


def row_values(Q: int, H: int, h: int, q: int, packet: str) -> dict[int, int]:
    require(all(type(v) is int and v > 0 for v in (Q, H, h, q)), "positive row scales")
    require(type(packet) is str and packet in ("constant", "signed_multiplier"), "packet label")
    require(h <= Q < q <= 2 * Q and is_prime(q) and gcd(q, h) == 1, "physical shell row")
    cutoff = h * q // H
    inverse = pow(q, -1, h)
    row: dict[int, int] = {}
    for m in range(-cutoff, cutoff + 1):
        if m == 0:
            continue
        a = m * inverse % h
        require(a not in row, "internal row collision")
        row[a] = 1 if packet == "constant" else (1 if m > 0 else -1)
    return row


def rational_cluster_weight(Q: int, H: int, U: int, h: int) -> tuple[Fraction, tuple[tuple[int, int], ...]]:
    require(all(type(v) is int and v > 0 for v in (Q, H, U, h)), "cluster scales")
    require(h <= U, "cluster denominator")
    total = Fraction(0, 1)
    terms: list[tuple[int, int]] = []
    for d in range(1, U + 1):
        mu = mobius(d)
        if 4 * Q * d > H and mu != 0 and d % h == 0:
            total += Fraction(mu, d)
            terms.append((d, mu))
    return total, tuple(terms)


def exponent_ledger() -> dict[str, str]:
    q = Fraction(1, 3)
    height = Fraction(21, 32)
    upper_h = Fraction(133, 400)
    entries = {
        "Q": q,
        "H": height,
        "U": upper_h,
        "Q2_over_H": 2 * q - height,
        "UQ_over_H": upper_h + q - height,
        "main_product": 2 * (2 * q - height),
        "secondary_product": (2 * q - height) + (upper_h + q - height),
        "window_U2_over_x": 2 * upper_h - 1,
        "unnormalized_main": 1 + 2 * (2 * q - height),
    }
    require(entries["Q2_over_H"] == Fraction(1, 96), "Q2/H exponent")
    require(entries["UQ_over_H"] == Fraction(23, 2400), "UQ/H exponent")
    require(entries["main_product"] == Fraction(1, 48), "main product exponent")
    require(entries["secondary_product"] == Fraction(1, 50), "secondary exponent")
    require(entries["window_U2_over_x"] == Fraction(-67, 200), "window exponent")
    require(entries["unnormalized_main"] == Fraction(49, 48), "unnormalized exponent")
    return {key: fraction_text(value) for key, value in entries.items()}


def physical_window_fixture() -> dict[str, object]:
    Q, H, U, h = 101, 8830, 99, 82
    selected_q = (109, 137, 191)
    packets = ("constant", "signed_multiplier")
    require(H**32 <= Q**63 < (H + 1) ** 32, "V59-shaped H floor")
    require(U**400 <= Q**399 < (U + 1) ** 400, "V59-shaped U floor")
    require(mobius(h) != 0 and h <= U < Q and 4 * Q < H, "physical scale ordering")
    require(all(q in primes_in_shell(Q) for q in selected_q), "selected prime shell")

    C_h, divisor_terms = rational_cluster_weight(Q, H, U, h)
    require(C_h == Fraction(1, 82) and divisor_terms == ((82, 1),), "source-active rational weight")

    rows: dict[str, dict[int, dict[int, int]]] = {}
    direct_energy = Fraction(0, 1)
    collapsed: dict[str, dict[int, Fraction]] = {}
    for packet in packets:
        rows[packet] = {}
        collapsed[packet] = {}
        for q in selected_q:
            row = row_values(Q, H, h, q, packet)
            require(set(row) == {3, 79}, "aligned primitive support")
            rows[packet][q] = row
            for a, amplitude in row.items():
                require(gcd(a, h) == 1, "fixture frequency primitive")
                value = C_h * amplitude
                direct_energy += value * value
                collapsed[packet][a] = collapsed[packet].get(a, Fraction(0, 1)) + value

    frequency_pairs = tuple((h, a) for a in sorted(collapsed["constant"]))
    validate_reduced_frequency_pairs(frequency_pairs, U)
    collapsed_by_packet = {
        packet: sum((value * value for value in coefficients.values()), Fraction(0, 1))
        for packet, coefficients in collapsed.items()
    }
    collapsed_energy = sum(collapsed_by_packet.values(), Fraction(0, 1))
    require(direct_energy == Fraction(3, 1681), "direct packet energy")
    require(collapsed_by_packet["constant"] == Fraction(9, 3362), "constant packet energy")
    require(collapsed_by_packet["signed_multiplier"] == Fraction(1, 3362), "signed packet energy")
    require(collapsed_energy == Fraction(5, 1681), "collapsed packet trace")
    require(collapsed_by_packet["constant"] / (direct_energy / 2) == 3, "constant collision ratio")
    require(collapsed_energy / direct_energy == Fraction(5, 3), "packet trace collision ratio")

    N = h
    for first_index, left in enumerate(frequency_pairs):
        for right in frequency_pairs[first_index + 1 :]:
            require((left[1] - right[1]) % h != 0, "complete-period frequency collision")
    window_energy = N * collapsed_energy
    require(window_energy == Fraction(10, 41), "exact complete-period energy")

    R_star = Fraction(4 * Q * Q, H) + Fraction(4 * U * Q, H)
    maximum_bucket_multiplicity = max(
        sum(1 for q in selected_q if a in rows["constant"][q]) for a in (3, 79)
    )
    require(maximum_bucket_multiplicity == 3 and Fraction(3, 1) <= R_star, "collision factor")
    large_sieve_factor = N - 1 + U * U
    large_sieve_rhs = large_sieve_factor * collapsed_energy
    composed_rhs = large_sieve_factor * R_star * direct_energy
    require(window_energy <= large_sieve_rhs <= composed_rhs, "finite-window composition")

    nonprimitive_rejected = False
    try:
        validate_reduced_frequency_pairs(((82, 6),), U)
    except ReassemblyFailure:
        nonprimitive_rejected = True
    require(nonprimitive_rejected, "nonprimitive mutation control")

    serial_rows = {
        packet: {
            str(q): {str(a): amplitude for a, amplitude in sorted(row.items())}
            for q, row in sorted(packet_rows.items())
        }
        for packet, packet_rows in rows.items()
    }
    return {
        "Q": Q,
        "H": H,
        "U": U,
        "h": h,
        "selected_q": list(selected_q),
        "shell_prime_count": len(primes_in_shell(Q)),
        "divisor_terms": [[d, mu] for d, mu in divisor_terms],
        "rational_C_h": fraction_text(C_h),
        "rows": serial_rows,
        "primitive_frequencies": [[h_value, a] for h_value, a in frequency_pairs],
        "direct_packet_energy": fraction_text(direct_energy),
        "constant_packet_collapsed_energy": fraction_text(collapsed_by_packet["constant"]),
        "signed_packet_collapsed_energy": fraction_text(collapsed_by_packet["signed_multiplier"]),
        "collapsed_packet_trace": fraction_text(collapsed_energy),
        "constant_packet_collision_ratio": "3",
        "packet_trace_collision_ratio": "5/3",
        "maximum_bucket_multiplicity": maximum_bucket_multiplicity,
        "R_star": fraction_text(R_star),
        "window_start": 0,
        "window_length": N,
        "exact_window_energy": fraction_text(window_energy),
        "normalized_window_energy": fraction_text(window_energy / N),
        "large_sieve_factor": large_sieve_factor,
        "large_sieve_rhs": fraction_text(large_sieve_rhs),
        "collision_composed_rhs": fraction_text(composed_rhs),
        "nonprimitive_frequency_mutation": "REJECTED",
    }


def build_certificate() -> dict[str, object]:
    records = {
        "exponents": exponent_ledger(),
        "physical_window_fixture": physical_window_fixture(),
    }
    digest = hashlib.sha256(
        json.dumps(records, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return {
        "schema": "tpc237-collision-compressed-finite-window-reassembly-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1_COMMON_SOURCE_COLLISION_COMPRESSED_FINITE_WINDOW_PACKET_TRACE",
        "theorem": {
            "primitive_bucket_factor": "R_*<=4Q^2/H+4UQ/H",
            "finite_window_factor": "N-1+U^2",
            "direct_coefficient_energy": "O(JM^2(Q^2/H)(log x)^5)",
            "normalized_envelope": "O(JM^2(x^(1/48)+x^(1/50))(log x)^5)",
            "unnormalized_main_exponent": "49/48",
        },
        "normalization_loss_ledger": {
            "q_weight": 1,
            "packet_dependent_transform": "NONE",
            "row_dependent_normalization": "NONE",
            "outer_coefficient": "LITERAL_SIGNED_C_h_IN_THEOREM",
            "frequency_representatives": "PRIMITIVE_ONLY",
            "output_normalization": "N^(-1)",
            "hidden_P_factor": "NONE",
        },
        "finite_reproduction": {"records": records, "digest": digest},
        "firewall": {
            "unsigned_packet_trace": "PROVED_STRUCTURAL",
            "signed_four_packet_gate_b_scalar": "OPEN",
            "C_h_signed_cancellation": "NONE",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "L2": "NONE",
            "strict_1_over_400": "UNPAID_GLOBAL",
            "full_gate_b": "OPEN",
            "sharpness": "NOT_CLAIMED",
        },
    }
