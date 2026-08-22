#!/usr/bin/env python3
"""Exact cutoff-one source-clock obstruction for TPC-225.

The source-surrogate clock inherited from TPC-224 is

    x=Q^3, H=4 Q^2, h=4 Q,  Q<q<=2Q prime.

Its literal cutoff is one.  This module rebuilds the resulting two-point
rows with exact ``Fraction`` arithmetic and records the identities
E_AP=E_diag and E_all=E_pol.  It is intentionally self-contained: the
independent checker does not import this producer.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from typing import Iterable


J = 4
AFFINE_SLOPES = (Fraction(0), Fraction(1, 10), Fraction(-1, 10), Fraction(1, 5))
Vector = dict[tuple[int, int], Fraction]


class ObstructionFailure(RuntimeError):
    """Raised when a declared finite audit invariant fails."""


def require(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise ObstructionFailure(message)


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return value == divisor
        divisor += 1
    return True


def prime_shell(Q: int) -> tuple[int, ...]:
    require(type(Q) is int and Q >= 3, "Q must be an integer at least three")
    return tuple(q for q in range(Q + 1, 2 * Q + 1) if is_prime(q))


def source_parameters(Q: int) -> tuple[int, int, int]:
    return Q**3, 4 * Q**2, 4 * Q


def profile_values(
    Q: int, q: int, packet: int, *, mode: str
) -> tuple[Fraction, Fraction]:
    require(0 <= packet < J, "packet label outside J=4")
    if mode == "affine":
        t = Fraction(Q, q)
        slope = AFFINE_SLOPES[packet]
        return Fraction(1) + slope * t, Fraction(1) - slope * t
    if mode == "aligned":
        return Fraction(1), Fraction(1)
    if mode == "balanced":
        plus = (Fraction(1), Fraction(-1), Fraction(0), Fraction(0))[packet]
        minus = (Fraction(0), Fraction(0), Fraction(1), Fraction(-1))[packet]
        return plus, minus
    raise ObstructionFailure(f"unknown profile mode: {mode}")


def add_to(vector: Vector, coordinate: tuple[int, int], value: Fraction) -> None:
    vector[coordinate] = vector.get(coordinate, Fraction(0)) + value
    if vector[coordinate] == 0:
        del vector[coordinate]


def literal_rows(Q: int, *, mode: str) -> dict[tuple[int, int], Vector]:
    """Build the literal cutoff-one rows for one named profile mode."""

    _, H, h = source_parameters(Q)
    qs = prime_shell(Q)
    require(bool(qs), f"empty prime shell at Q={Q}")
    rows: dict[tuple[int, int], Vector] = {}
    for q in qs:
        require(gcd(q, h) == 1, f"q={q} is not a unit modulo h={h}")
        inverse = pow(q, -1, h)
        cutoff = h * q // H
        require(cutoff == 1, f"cutoff is not one at Q={Q}, q={q}")
        for packet in range(J):
            plus, minus = profile_values(Q, q, packet, mode=mode)
            vector: Vector = {}
            # C_h=1/h is the common normalization inherited from TPC-224.
            add_to(vector, (h, inverse), plus / h)
            add_to(vector, (h, (-inverse) % h), minus / h)
            rows[(q, packet)] = vector
    return rows


def vector_sum(vectors: Iterable[Vector]) -> Vector:
    result: Vector = {}
    for vector in vectors:
        for coordinate, value in vector.items():
            add_to(result, coordinate, value)
    return result


def squared_norm(vector: Vector) -> Fraction:
    return sum((value * value for value in vector.values()), Fraction(0))


def energies(Q: int, *, mode: str) -> dict[str, object]:
    rows = literal_rows(Q, mode=mode)
    qs = prime_shell(Q)
    by_packet = [
        vector_sum(rows[(q, packet)] for q in qs) for packet in range(J)
    ]
    by_prime = [
        vector_sum(rows[(q, packet)] for packet in range(J)) for q in qs
    ]
    diagonal = sum((squared_norm(row) for row in rows.values()), Fraction(0))
    ap = sum((squared_norm(row) for row in by_packet), Fraction(0))
    polarized = sum((squared_norm(row) for row in by_prime), Fraction(0))
    full = squared_norm(vector_sum(rows.values()))
    supports = {
        q: frozenset(
            coordinate
            for packet in range(J)
            for coordinate in rows[(q, packet)]
        )
        for q in qs
    }
    disjoint = all(
        supports[q1].isdisjoint(supports[q2])
        for index, q1 in enumerate(qs)
        for q2 in qs[index + 1 :]
    )
    require(disjoint, f"support collision at Q={Q}")
    require(ap == diagonal, f"AP identity failed at Q={Q}, mode={mode}")
    require(full == polarized, f"full/polarized identity failed at Q={Q}, mode={mode}")
    _, H, h = source_parameters(Q)
    t_values = [Fraction(Q, q) for q in qs]
    return {
        "Q": Q,
        "x": Q**3,
        "H": H,
        "h": h,
        "mode": mode,
        "prime_count": len(qs),
        "prime_values": list(qs),
        "packet_count": J,
        "cutoffs": sorted({h * q // H for q in qs}),
        "coordinate_count": len({c for row in rows.values() for c in row}),
        "shared_normalization": "C_h=1/h",
        "E_diag": str(diagonal),
        "E_AP": str(ap),
        "E_pol": str(polarized),
        "E_all": str(full),
        "AP_over_diag": str(ap / diagonal) if diagonal else "UNDEFINED",
        "all_over_pol": str(full / polarized) if polarized else "UNDEFINED",
        "pol_over_diag": str(polarized / diagonal) if diagonal else "UNDEFINED",
        "support_disjoint": disjoint,
        "cutoff_one": True,
        "t_min": str(min(t_values)),
        "t_max": str(max(t_values)),
    }


def affine_formula_record(Q: int) -> dict[str, object]:
    record = energies(Q, mode="affine")
    qs = prime_shell(Q)
    C = Fraction(1, 4 * Q)
    s1 = sum(AFFINE_SLOPES, Fraction(0))
    s2 = sum((slope * slope for slope in AFFINE_SLOPES), Fraction(0))
    diagonal_formula = sum(
        (2 * C * C * (J + s2 * Fraction(Q, q) ** 2) for q in qs),
        Fraction(0),
    )
    polarized_formula = sum(
        (2 * C * C * (J * J + s1 * s1 * Fraction(Q, q) ** 2) for q in qs),
        Fraction(0),
    )
    require(str(diagonal_formula) == record["E_diag"], "affine diagonal formula")
    require(str(polarized_formula) == record["E_pol"], "affine polarized formula")
    record["affine_s1"] = str(s1)
    record["affine_s2"] = str(s2)
    record["formula_E_diag"] = str(diagonal_formula)
    record["formula_E_pol"] = str(polarized_formula)
    return record


def build_certificate() -> dict[str, object]:
    affine_Q = (11, 17, 29, 43, 61, 89, 127, 181, 257)
    boundary_Q = (3, 5, 7, 13, 31, 47, 73)
    affine_records = [affine_formula_record(Q) for Q in affine_Q]
    aligned_records = [energies(Q, mode="aligned") for Q in boundary_Q]
    balanced_records = [energies(Q, mode="balanced") for Q in boundary_Q]
    all_records = affine_records + aligned_records + balanced_records
    require(all(record["cutoff_one"] is True for record in all_records), "cutoff records")
    require(all(record["support_disjoint"] is True for record in all_records), "support records")
    require(all(record["AP_over_diag"] == "1" for record in all_records), "AP identity records")
    require(
        all(record["all_over_pol"] in {"1", "UNDEFINED"} for record in all_records),
        "full identity records",
    )
    require(all(record["formula_E_diag"] for record in affine_records), "affine formulas")
    require(all(record["formula_E_pol"] for record in affine_records), "affine formulas")
    require(all(record["E_pol"] == "0" for record in balanced_records), "balanced cancellation")
    require(all(record["E_diag"] != "0" for record in balanced_records), "balanced nonzero diagonal")
    require(all(record["E_pol"] != "0" for record in aligned_records), "aligned nonzero packet")
    return {
        "schema": "tpc225-cutoff-one-shared-clock-obstruction-v1",
        "status": "PASS",
        "claim_level": "PROVED_STRUCTURAL_L1",
        "author": "Liang Wang",
        "affiliation": "Huazhong University of Science and Technology",
        "theorem": {
            "clock": "x=Q^3, H=4Q^2, h=4Q",
            "cutoff": "floor(hq/H)=1",
            "support_disjointness": "PROVED_EXACT",
            "ap_equals_diagonal": "PROVED_EXACT",
            "all_equals_polarized": "PROVED_EXACT",
            "positive_ap_saving_on_clock": "REFUTED_SCOPED",
            "complex_profile_extension": "ALGEBRAIC",
        },
        "affine_clock": {
            "classification": "MODELING_CHOICE / FINITE_GROWING_AUDIT",
            "profile": "psi_j(t)=1+s_j t",
            "slopes": [str(value) for value in AFFINE_SLOPES],
            "records": affine_records,
        },
        "boundary_profiles": {
            "classification": "EXACT_PROFILE_FIXTURES / NOT_ASYMPTOTIC",
            "aligned_records": aligned_records,
            "balanced_records": balanced_records,
        },
        "checks": {
            "cutoff_one_all_scales": True,
            "support_disjoint_all_scales": True,
            "ap_identity_all_scales": True,
            "full_polarized_identity_all_scales": True,
            "affine_closed_form_replayed": True,
            "balanced_packet_cancellation_replayed": True,
            "all_arithmetic_exact_rational": True,
            "source_clock_not_promoted_to_v46": True,
        },
        "firewall": {
            "route_a": "NOT_APPLICABLE",
            "route_b_structural_threshold_a": "PASS",
            "cutoff_one_obstruction": "PROVED_STRUCTURAL_L1",
            "ap_dispersion_on_named_clock": "REFUTED_SCOPED",
            "polarized_saving": "PROFILE_DEPENDENT_OPEN",
            "v46_clock_transfer": "OPEN",
            "arithmetic_advance": "NO",
            "fixed_atom_credit": 0,
            "l2": "NONE",
            "full_gate_b": "OPEN",
            "strict_1_over_400": "UNPAID",
        },
        "route": {
            "strongest_positive": "CUTOFF_ONE_SUPPORT_ORTHOGONALITY_IDENTITY",
            "strongest_obstruction": "AP_MARGINAL_EQUALS_DIAGONAL_NO_SAVING",
            "open_theorem": "FIND_A_SOURCE_LOCKED_CLOCK_WITH_NONTRIVIAL_M_SUPPORT_OR_PROVE_ITS_ABSENCE",
            "reusable_structure": "E_AP=E_DIAG_AND_E_ALL=E_POL_IN_CUTOFF_ONE_REGIME",
            "round2_clue": "MOVE_TO_NONTRIVIAL_CUTOFF_CLOCK_BEFORE_CLAIMING_AP_DISPERSION",
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_certificate(), indent=2, sort_keys=True))
