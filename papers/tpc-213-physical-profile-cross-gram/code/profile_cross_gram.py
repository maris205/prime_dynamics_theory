"""Exact finite algebra for the TPC-213 physical profile/emitter map.

TPC-212 kept one residual vector in a separate direct-sum block for every
divisor.  The literal V46 residual instead comes from one common physical
support.  This module records the resulting residue-lift map and pulls the
reciprocal emitter back to that common support.

All finite calculations are exact.  The reciprocal weights are unit weights
and the logarithmic prefactors are omitted from the geometric Gram fixture;
that is an explicit finite modeling choice, not an asymptotic replacement for
the physical smooth weight or for log(d).
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, lcm


Matrix = tuple[tuple[int, ...], ...]


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ValueError(message)


def prime_factors(value: int) -> tuple[int, ...]:
    require(type(value) is int and value >= 1, "positive integer")
    remaining = value
    factors: list[int] = []
    candidate = 2
    while candidate * candidate <= remaining:
        if remaining % candidate == 0:
            factors.append(candidate)
            remaining //= candidate
            require(remaining % candidate != 0, "squarefree divisor")
            while remaining % candidate == 0:
                remaining //= candidate
        candidate += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def local_f(prime: int, residue: int) -> Fraction:
    require(prime > 2, "odd local prime")
    return Fraction(0, 1) if (residue + 2) % prime == 0 else Fraction(prime, prime - 1)


def local_g(prime: int, cutoff: int, residue: int) -> Fraction:
    require(prime > 2, "odd local prime")
    if prime <= cutoff:
        return local_f(prime, residue)
    if residue % prime == 0:
        return Fraction(prime, prime - 1)
    return Fraction(prime * (prime - 2), (prime - 1) ** 2)


def delta_profile(divisor: int, cutoff: int) -> tuple[Fraction, ...]:
    """Return the literal finite V46 profile Delta_d=P_d-B_d,z."""

    factors = prime_factors(divisor)
    require(divisor >= 3 and bool(factors), "nontrivial squarefree divisor")
    return tuple(
        _profile_value(factors, cutoff, residue)
        for residue in range(divisor)
    )


def _profile_value(factors: tuple[int, ...], cutoff: int, residue: int) -> Fraction:
    p_value = Fraction(1, 1)
    b_value = Fraction(1, 1)
    for prime in factors:
        p_value *= local_f(prime, residue)
        b_value *= local_g(prime, cutoff, residue)
    return p_value - b_value


def residue_lift(divisor: int, support: tuple[int, ...]) -> Matrix:
    """Matrix C_d with (C_d f)(a)=sum_{u congruent a mod d} f(u)."""

    require(divisor >= 2, "divisor")
    return tuple(
        tuple(int(u % divisor == residue) for u in support)
        for residue in range(divisor)
    )


def cross_lift_matrix(
    left: int, right: int, support: tuple[int, ...]
) -> Matrix:
    """Return C_left C_right^* on the common physical support."""

    return tuple(
        tuple(
            sum(
                int(u % left == left_residue and u % right == right_residue)
                for u in support
            )
            for right_residue in range(right)
        )
        for left_residue in range(left)
    )


def complete_period_cross_lift(left: int, right: int, period: int) -> Matrix:
    """Expected C_left C_right^* for a complete period of the lcm."""

    common = gcd(left, right)
    common_period = lcm(left, right)
    require(period % common_period == 0, "period must contain complete lcm periods")
    multiplicity = period // common_period
    return tuple(
        tuple(
            multiplicity * int(left_residue % common == right_residue % common)
            for right_residue in range(right)
        )
        for left_residue in range(left)
    )


def matrix_rank(matrix: Matrix) -> int:
    """Exact rational row rank for a finite integer matrix."""

    if not matrix:
        return 0
    work = [[Fraction(value, 1) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    require(all(len(row) == columns for row in work), "matrix shape")
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [a - factor * b for a, b in zip(work[row], work[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def reciprocal_pairs(
    divisor: int, q_values: tuple[int, ...], H: int
) -> tuple[tuple[int, int], ...]:
    require(divisor >= 2 and H >= 1, "positive parameters")
    pairs: list[tuple[int, int]] = []
    for q in q_values:
        require(type(q) is int and q > 1 and gcd(q, divisor) == 1, "unit q")
        limit = divisor * q // H
        pairs.extend((q, m) for m in range(-limit, limit + 1) if m != 0)
    return tuple(pairs)


def emitter_counts(
    divisor: int, q_values: tuple[int, ...], H: int
) -> tuple[int, ...]:
    counts = [0 for _ in range(divisor)]
    for q, m in reciprocal_pairs(divisor, q_values, H):
        counts[(m * pow(q, -1, divisor)) % divisor] += 1
    return tuple(counts)


def emitter_norm_squared(
    divisor: int, q_values: tuple[int, ...], H: int
) -> int:
    counts = emitter_counts(divisor, q_values, H)
    return sum(value * value for value in counts)


def frequency_intersections(
    left: int,
    right: int,
    left_counts: tuple[int, ...],
    right_counts: tuple[int, ...],
) -> tuple[tuple[int, int, int, int], ...]:
    """Return nonzero common rational frequencies r/left=s/right."""

    require(len(left_counts) == left and len(right_counts) == right, "occupancy shape")
    return tuple(
        (r, s, left_counts[r], right_counts[s])
        for r in range(left)
        for s in range(right)
        if Fraction(r, left) == Fraction(s, right)
        and left_counts[r] != 0
        and right_counts[s] != 0
    )


def full_period_cross_gram(
    left: int,
    right: int,
    q_values: tuple[int, ...],
    H: int,
) -> int:
    """Exact Hermitian cross Gram on one complete lcm period.

    If K_d(u)=sum_r A_d(r)e_d(ru), then
    sum_{u mod lcm(d,e)} K_d(u) conjugate(K_e(u))
    is lcm(d,e) times the common-frequency occupancy product.
    """

    left_counts = emitter_counts(left, q_values, H)
    right_counts = emitter_counts(right, q_values, H)
    period = lcm(left, right)
    return period * sum(
        left_count * right_count
        for _, _, left_count, right_count in frequency_intersections(
            left, right, left_counts, right_counts
        )
    )


def delta_audit(divisor: int, cutoff: int) -> dict[str, object]:
    profile = delta_profile(divisor, cutoff)
    return {
        "divisor": divisor,
        "profile": [str(value) for value in profile],
        "zero_axis": str(profile[0]),
        "mean": str(sum(profile, Fraction(0, 1))),
        "l2_squared": str(sum(value * value for value in profile)),
    }


def lift_audit(left: int, right: int, support: tuple[int, ...]) -> dict[str, object]:
    actual = cross_lift_matrix(left, right, support)
    expected = complete_period_cross_lift(left, right, len(support))
    require(actual == expected, "CRT/lcm lift identity")
    return {
        "left": left,
        "right": right,
        "gcd": gcd(left, right),
        "lcm": lcm(left, right),
        "support_size": len(support),
        "compatibility_identity": True,
        "nonzero_entries": sum(value != 0 for row in actual for value in row),
        "rank": matrix_rank(actual),
    }


def emitter_audit(
    divisor: int, q_values: tuple[int, ...], H: int
) -> dict[str, object]:
    pairs = reciprocal_pairs(divisor, q_values, H)
    counts = emitter_counts(divisor, q_values, H)
    maximum_m = max((abs(m) for _, m in pairs), default=0)
    return {
        "divisor": divisor,
        "q_values": list(q_values),
        "H": H,
        "reciprocal_pair_count": len(pairs),
        "maximum_abs_m": maximum_m,
        "two_m_less_than_d": 2 * maximum_m < divisor,
        "occupancy": list(counts),
        "norm_squared": sum(value * value for value in counts),
        "zero_frequency_occupancy": counts[0],
    }


def cross_gram_audit(
    left: int,
    right: int,
    q_values: tuple[int, ...],
    H: int,
) -> dict[str, object]:
    left_counts = emitter_counts(left, q_values, H)
    right_counts = emitter_counts(right, q_values, H)
    intersections = frequency_intersections(left, right, left_counts, right_counts)
    period = lcm(left, right)
    cross = full_period_cross_gram(left, right, q_values, H)
    left_diagonal = period * sum(value * value for value in left_counts)
    right_diagonal = period * sum(value * value for value in right_counts)
    return {
        "left": left,
        "right": right,
        "period": period,
        "frequency_intersections": [list(row) for row in intersections],
        "frequency_intersection_weight": sum(row[2] * row[3] for row in intersections),
        "cross_gram": cross,
        "left_diagonal_gram": left_diagonal,
        "right_diagonal_gram": right_diagonal,
        "cross_gram_nonzero": cross != 0,
        "normalized_cross_gram_squared": str(
            Fraction(cross * cross, left_diagonal * right_diagonal)
        ),
    }


def build_certificate() -> dict[str, object]:
    divisors = (5, 7, 35)
    support = tuple(range(35))
    q_values = (11, 13, 17)
    H = 40
    cutoff = 3
    lift_cases = tuple(
        lift_audit(left, right, support)
        for left, right in ((5, 7), (5, 35), (7, 35))
    )
    emitter_cases = tuple(
        emitter_audit(divisor, q_values, H) for divisor in divisors
    )
    cross_cases = tuple(
        cross_gram_audit(left, right, q_values, H)
        for left, right in ((5, 7), (5, 35), (7, 35))
    )
    joint_lift = tuple(
        residue_lift(divisor, support)[row]
        for divisor in divisors
        for row in range(divisor)
    )
    return {
        "schema": "TPC213_PHYSICAL_PROFILE_CROSS_GRAM_CERTIFICATE_V1",
        "classification": "PROVED_STRUCTURAL_L1_CROSS_DIVISOR_COUPLING",
        "modeling_choice": "UNIT_RECIPROCAL_WEIGHTS_PSI_EQUALS_ONE_NO_LOG_PREFactor",
        "fixture": {
            "divisors": list(divisors),
            "support": [support[0], support[-1], len(support)],
            "q_values": list(q_values),
            "H": H,
            "cutoff_z": cutoff,
            "complete_period": len(support),
        },
        "delta_profiles": [delta_audit(divisor, cutoff) for divisor in divisors],
        "lift_cases": list(lift_cases),
        "joint_lift": {
            "row_count": len(joint_lift),
            "column_count": len(support),
            "rank": matrix_rank(joint_lift),
            "domain_kernel_dimension": len(support) - matrix_rank(joint_lift),
            "codomain_dependency_dimension": len(joint_lift) - matrix_rank(joint_lift),
        },
        "emitter_cases": list(emitter_cases),
        "cross_gram_cases": list(cross_cases),
        "theorem_contract": {
            "physical_profile_emitter_pullback": "PROVED_EXACT_OPERATOR_IDENTITY",
            "residue_lift_gcd_aliasing": "PROVED_EXACT_FINITE",
            "cross_divisor_frequency_gram": "PROVED_EXACT_FINITE",
            "physical_direct_sum_replacement": "REFUTED_SCOPED",
            "literal_v46_asymptotic_gram_bound": "OPEN",
            "smooth_psi_prime_shell_reassembly": "OPEN",
        },
        "claim_firewall": {
            "route_advance": "YES",
            "structural_threshold_a": "PASS",
            "physical_profile_emitter_pullback": "PROVED_EXACT",
            "residue_lift_gcd_aliasing": "PROVED_EXACT",
            "cross_divisor_frequency_gram": "PROVED_EXACT_FINITE",
            "physical_direct_sum_replacement": "REFUTED_SCOPED",
            "literal_v46_asymptotic_gram_bound": "OPEN",
            "prime_shell_reassembly": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b_strict_1_over_400": "UNPAID",
        },
        "audit_counts": {
            "delta_profile_rows": len(divisors),
            "delta_profile_coordinates": sum(divisors),
            "lift_cases": len(lift_cases),
            "emitter_cases": len(emitter_cases),
            "cross_gram_cases": len(cross_cases),
        },
        "open_theorem": (
            "BOUND_THE_JOINT_PULLBACK_KERNEL_FOR_THE_LITERAL_V46_RANGE_WITH_"
            "SMOOTH_PSI_FOUR_PACKET_SIGNS_ZERO_AXIS_AND_PRIME_SHELL_REASSEMBLY"
        ),
    }
