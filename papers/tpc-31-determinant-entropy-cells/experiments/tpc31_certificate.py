#!/usr/bin/env python3
"""Exact finite certificate for TPC-31.

This standard-library certificate checks the finite algebra behind the
canonical target-content normalization

    c = gcd(m*j+h, n*j+h),    Delta# = (m-n)/c.

It verifies primitive and reduced-target identities, the relation between
arbitrary selected divisors and the canonical normalization, finite graph
degree bounds for determinant cells, an integer-weight Schur inequality,
exact-c orbit occupancy, exact residue-cell reassembly, and the rational
TPC-30/TPC-31 splice ledger.  These are finite regression checks.  They are
not numerical evidence for asymptotic Mobius cancellation, signed
dispersion, a prime-pair asymptotic, or twin primes.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
from typing import Callable, Iterable


RowPair = tuple[int, int]


def require(condition: bool, label: str, *details: object) -> None:
    """Raise in ordinary and optimized Python when a check fails."""
    if not condition:
        raise RuntimeError((label,) + details)


def factor(n: int) -> dict[int, int]:
    require(n >= 1, "factor-positive", n)
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def divisors(n: int) -> list[int]:
    require(n >= 1, "divisors-positive", n)
    out = [1]
    for prime, exponent in factor(n).items():
        powers = [prime**power for power in range(exponent + 1)]
        out = [left * right for left in out for right in powers]
    return sorted(out)


def mobius(n: int) -> int:
    fac = factor(n)
    if any(exponent > 1 for exponent in fac.values()):
        return 0
    return -1 if len(fac) % 2 else 1


def ceil_div(numerator: int, denominator: int) -> int:
    require(numerator >= 0 and denominator >= 1,
            "ceil-div-domain", numerator, denominator)
    return (numerator + denominator - 1) // denominator


def target(row: int, h: int, orbit: int) -> int:
    value = row * orbit + h
    require(value > 0, "positive-target", row, h, orbit, value)
    return value


def target_content(m: int, n: int, h: int, orbit: int) -> int:
    return math.gcd(target(m, h, orbit), target(n, h, orbit))


def primitive_case(m: int, n: int, h: int, orbit: int) -> bool:
    return (
        h != 0
        and math.gcd(m, abs(h)) == 1
        and math.gcd(n, abs(h)) == 1
        and math.gcd(orbit, abs(h)) == 1
        and m * orbit + h > 0
        and n * orbit + h > 0
    )


def check_primitive_reduced_identities() -> tuple[int, dict[str, object]]:
    checks = 0
    primitive_cases = 0
    nontrivial_contents = 0
    largest_content = 1
    negative_shift_cases = 0
    sample: dict[str, int] | None = None

    shifts = (-5, -3, -2, -1, 1, 2, 3, 4, 5, 6, 8, 10)
    for h in shifts:
        orbit_start = abs(h) + 1 if h < 0 else 1
        for m in range(1, 27):
            for n in range(1, 27):
                if m == n:
                    continue
                for orbit in range(orbit_start, orbit_start + 34):
                    if not primitive_case(m, n, h, orbit):
                        continue
                    left = target(m, h, orbit)
                    right = target(n, h, orbit)
                    c = math.gcd(left, right)
                    delta = m - n
                    delta_sharp = delta // c
                    reduced_left = left // c
                    reduced_right = right // c

                    require(c == math.gcd(left, abs(delta)),
                            "primitive-content-identity",
                            m, n, h, orbit, c)
                    checks += 1
                    require(delta % c == 0,
                            "canonical-content-divides-row-difference",
                            m, n, h, orbit, c, delta)
                    checks += 1
                    require(math.gcd(reduced_left, reduced_right) == 1,
                            "reduced-targets-coprime",
                            m, n, h, orbit, c,
                            reduced_left, reduced_right)
                    checks += 1
                    require(
                        m * reduced_right - n * reduced_left
                        == h * delta_sharp,
                        "reduced-determinant-identity",
                        m, n, h, orbit, c, delta_sharp,
                        reduced_left, reduced_right,
                    )
                    checks += 1
                    require(math.gcd(c, abs(h)) == 1,
                            "canonical-content-coprime-shift",
                            m, n, h, orbit, c)
                    checks += 1
                    require(math.gcd(c, abs(m * n * h)) == 1,
                            "canonical-content-coprime-mnh",
                            m, n, h, orbit, c)
                    checks += 1

                    primitive_cases += 1
                    negative_shift_cases += int(h < 0)
                    if c > 1:
                        nontrivial_contents += 1
                        largest_content = max(largest_content, c)
                        if sample is None or c > sample["c"]:
                            sample = {
                                "m": m,
                                "n": n,
                                "h": h,
                                "j": orbit,
                                "N_m": left,
                                "N_n": right,
                                "c": c,
                                "Delta_sharp": delta_sharp,
                                "reduced_left": reduced_left,
                                "reduced_right": reduced_right,
                            }

    boundary = {"m": 1, "n": 3, "h": 2, "j": 2}
    boundary_left = target(boundary["m"], boundary["h"], boundary["j"])
    boundary_right = target(boundary["n"], boundary["h"], boundary["j"])
    boundary_content = math.gcd(boundary_left, boundary_right)
    boundary_euclid = math.gcd(boundary_left,
                               abs(boundary["m"] - boundary["n"]))
    require(boundary_content != boundary_euclid,
            "nonprimitive-boundary-witness",
            boundary, boundary_content, boundary_euclid)
    checks += 1

    require(sample is not None, "nontrivial-content-sample-exists")
    checks += 1
    return checks, {
        "primitive_cases": primitive_cases,
        "negative_shift_cases": negative_shift_cases,
        "nontrivial_contents": nontrivial_contents,
        "largest_content": largest_content,
        "largest_recorded_sample": sample,
        "verified_identities": [
            "c = gcd(N_m,N_n) = gcd(N_m,m-n)",
            "gcd(N_m/c,N_n/c) = 1",
            "m*(N_n/c)-n*(N_m/c) = h*(m-n)/c",
        ],
        "nonprimitive_boundary_witness": {
            **boundary,
            "target_content": boundary_content,
            "euclidean_right_side": boundary_euclid,
        },
    }


def check_selected_divisor_multiplier() -> tuple[int, dict[str, object]]:
    checks = 0
    factorizations = 0
    divisor_pairs = 0
    proper_divisor_multipliers = 0
    maximum_multiplier = 1
    proper_sample: dict[str, int] | None = None

    for h in range(1, 7):
        for m in range(1, 15):
            for n in range(1, 15):
                if m == n:
                    continue
                for orbit in range(1, 15):
                    if not primitive_case(m, n, h, orbit):
                        continue
                    left = target(m, h, orbit)
                    right = target(n, h, orbit)
                    c = math.gcd(left, right)
                    delta_sharp = (m - n) // c
                    factorizations += 1
                    for r in divisors(left):
                        for s in divisors(right):
                            d = math.gcd(r, s)
                            require(c % d == 0,
                                    "selected-content-divides-canonical",
                                    m, n, h, orbit, r, s, d, c)
                            checks += 1
                            multiplier = c // d
                            require((m - n) % d == 0,
                                    "selected-content-divides-determinant",
                                    m, n, h, orbit, r, s, d)
                            checks += 1
                            require(
                                (m - n) // d == multiplier * delta_sharp,
                                "canonical-determinant-multiplier",
                                m, n, h, orbit, r, s, d, c,
                                multiplier, delta_sharp,
                            )
                            checks += 1
                            divisor_pairs += 1
                            maximum_multiplier = max(maximum_multiplier,
                                                     multiplier)
                            if d < c:
                                proper_divisor_multipliers += 1
                                if (proper_sample is None
                                        or multiplier
                                        > proper_sample["multiplier"]):
                                    proper_sample = {
                                        "m": m,
                                        "n": n,
                                        "h": h,
                                        "j": orbit,
                                        "N_m": left,
                                        "N_n": right,
                                        "r": r,
                                        "s": s,
                                        "d": d,
                                        "c": c,
                                        "multiplier": multiplier,
                                        "Delta_sharp": delta_sharp,
                                        "selected_Delta": (m - n) // d,
                                    }

    require(proper_sample is not None,
            "proper-selected-content-sample-exists")
    checks += 1
    return checks, {
        "affine_factorizations": factorizations,
        "selected_divisor_pairs": divisor_pairs,
        "proper_selected_content_pairs": proper_divisor_multipliers,
        "maximum_multiplier": maximum_multiplier,
        "proper_multiplier_sample": proper_sample,
        "verified_identity": "(m-n)/d = (c/d)*Delta_sharp",
    }


def exact_c_edges(
    rows: tuple[int, ...],
    h: int,
    orbit: int,
    c: int,
    predicate: Callable[[int], bool] | None = None,
) -> tuple[RowPair, ...]:
    require(len(rows) == len(set(rows)), "distinct-row-set", rows)
    require(c >= 1, "positive-content-cell", c)
    out: list[RowPair] = []
    for m in rows:
        for n in rows:
            if m == n:
                continue
            if not primitive_case(m, n, h, orbit):
                continue
            if target_content(m, n, h, orbit) != c:
                continue
            require((m - n) % c == 0,
                    "edge-canonical-divisibility", m, n, h, orbit, c)
            delta_sharp = (m - n) // c
            if predicate is None or predicate(delta_sharp):
                out.append((m, n))
    return tuple(out)


def difference_edges(
    rows: tuple[int, ...],
    c: int,
    predicate: Callable[[int], bool] | None = None,
) -> tuple[RowPair, ...]:
    """The full deterministic row graph m-n=c*delta.

    Unlike ``exact_c_edges``, this is the abstract graph used by the Schur
    lemma before the physical exact-content event is imposed.
    """
    require(len(rows) == len(set(rows)), "distinct-difference-row-set", rows)
    require(c >= 1, "positive-difference-content", c)
    out: list[RowPair] = []
    for m in rows:
        for n in rows:
            if m == n or (m - n) % c != 0:
                continue
            delta_sharp = (m - n) // c
            if predicate is None or predicate(delta_sharp):
                out.append((m, n))
    return tuple(out)


def bidirectional_degrees(
    rows: tuple[int, ...], edges: Iterable[RowPair]
) -> tuple[int, int, dict[int, int], dict[int, int]]:
    outgoing = {row: 0 for row in rows}
    incoming = {row: 0 for row in rows}
    for m, n in edges:
        require(m in outgoing and n in incoming,
                "edge-vertices-in-row-set", m, n, rows)
        outgoing[m] += 1
        incoming[n] += 1
    return (max(outgoing.values(), default=0),
            max(incoming.values(), default=0), outgoing, incoming)


def determinant_values(
    rows: tuple[int, ...], h: int, orbit: int, c: int
) -> tuple[int, ...]:
    return tuple((m - n) // c
                 for m, n in exact_c_edges(rows, h, orbit, c))


def check_cell_degree_bounds() -> tuple[int, dict[str, object]]:
    checks = 0
    omega_cells = 0
    window_cells = 0
    residue_cells = 0
    intersection_cells = 0
    nonempty_cells = 0
    maximum_actual_degree = 0
    sharp_records: dict[str, dict[str, object]] = {}

    row_cases = (
        ("dense", tuple(range(5, 17)), 1, 1),
        ("sparse", (5, 7, 11, 16, 23, 31, 38), 1, 2),
        ("factorable", (11, 22, 33, 13, 26, 39, 17, 34, 51), 1, 3),
        ("shift-six", (5, 7, 11, 13, 17, 19, 23), 6, 5),
    )
    omega_sets = (
        (-9, -4, 2, 7),
        (-3, -1, 0, 1, 5),
        (1,),
        (-12, -11, -10, -9, -8, -7),
    )
    window_starts = (-10, -3, 1, 7)
    window_widths = (1, 3, 6)
    moduli = (1, 2, 3, 5, 8)

    for case_name, rows, h, orbit in row_cases:
        require(math.gcd(orbit, abs(h)) == 1,
                "degree-case-primitive-orbit", case_name)
        checks += 1
        all_contents = {
            target_content(m, n, h, orbit)
            for m in rows for n in rows
            if m != n and primitive_case(m, n, h, orbit)
        }
        all_contents.add(max(all_contents, default=1) + 1)
        span = max(rows) - min(rows)

        for c in sorted(all_contents):
            for omega_tuple in omega_sets:
                omega = frozenset(omega_tuple)
                edges = difference_edges(
                    rows, c, lambda delta, o=omega: delta in o)
                kout, kin, _, _ = bidirectional_degrees(rows, edges)
                bound = len(omega)
                require(kout <= bound and kin <= bound,
                        "omega-bidirectional-degree",
                        case_name, c, omega_tuple, kout, kin, bound)
                checks += 1
                for m, n in edges:
                    delta = (m - n) // c
                    require(n == m - c * delta,
                            "fixed-row-delta-injection",
                            case_name, m, n, c, delta)
                    checks += 1
                omega_cells += 1
                nonempty_cells += int(bool(edges))
                maximum_actual_degree = max(maximum_actual_degree,
                                            kout, kin)

            for start in window_starts:
                for width in window_widths:
                    stop = start + width
                    edges = difference_edges(
                        rows, c,
                        lambda delta, lo=start, hi=stop: lo <= delta < hi)
                    kout, kin, _, _ = bidirectional_degrees(rows, edges)
                    require(kout <= width and kin <= width,
                            "window-bidirectional-degree",
                            case_name, c, start, width, kout, kin)
                    checks += 1
                    window_cells += 1
                    nonempty_cells += int(bool(edges))
                    maximum_actual_degree = max(maximum_actual_degree,
                                                kout, kin)
                    if (kout == width or kin == width) and "window" not in sharp_records:
                        sharp_records["window"] = {
                            "case": case_name,
                            "c": c,
                            "start": start,
                            "width": width,
                            "out_degree": kout,
                            "in_degree": kin,
                        }

                    for modulus in moduli:
                        for residue in range(modulus):
                            intersection = difference_edges(
                                rows, c,
                                lambda delta, lo=start, hi=stop,
                                q=modulus, a=residue:
                                lo <= delta < hi and delta % q == a,
                            )
                            ikout, ikin, _, _ = bidirectional_degrees(
                                rows, intersection)
                            intersection_bound = ceil_div(width, modulus)
                            require(
                                ikout <= intersection_bound
                                and ikin <= intersection_bound,
                                "window-residue-bidirectional-degree",
                                case_name, c, start, width,
                                modulus, residue,
                                ikout, ikin, intersection_bound,
                            )
                            checks += 1
                            intersection_cells += 1
                            nonempty_cells += int(bool(intersection))
                            maximum_actual_degree = max(
                                maximum_actual_degree, ikout, ikin)

            for modulus in moduli:
                residue_bound = span // (c * modulus) + 1
                for residue in range(modulus):
                    edges = difference_edges(
                        rows, c,
                        lambda delta, q=modulus, a=residue:
                        delta % q == a,
                    )
                    kout, kin, _, _ = bidirectional_degrees(rows, edges)
                    require(kout <= residue_bound and kin <= residue_bound,
                            "residue-bidirectional-degree",
                            case_name, c, modulus, residue,
                            kout, kin, residue_bound, span)
                    checks += 1
                    residue_cells += 1
                    nonempty_cells += int(bool(edges))
                    maximum_actual_degree = max(maximum_actual_degree,
                                                kout, kin)
                    if ((kout == residue_bound or kin == residue_bound)
                            and "residue" not in sharp_records):
                        sharp_records["residue"] = {
                            "case": case_name,
                            "c": c,
                            "modulus": modulus,
                            "residue": residue,
                            "span": span,
                            "bound": residue_bound,
                            "out_degree": kout,
                            "in_degree": kin,
                        }

    require("window" in sharp_records,
            "sharp-window-degree-record-exists", sharp_records)
    checks += 1
    require("residue" in sharp_records,
            "sharp-residue-degree-record-exists", sharp_records)
    checks += 1
    return checks, {
        "omega_cells": omega_cells,
        "window_cells": window_cells,
        "residue_cells": residue_cells,
        "window_residue_cells": intersection_cells,
        "nonempty_cells": nonempty_cells,
        "maximum_actual_degree": maximum_actual_degree,
        "sharp_records": sharp_records,
        "verified_bounds": {
            "finite_Omega": "K_plus,K_minus <= #Omega",
            "translated_window": "K_plus,K_minus <= window cardinality",
            "residue": "K_plus,K_minus <= floor(span/(c*q))+1",
            "window_residue": "K_plus,K_minus <= ceil(window cardinality/q)",
        },
    }


def adjacency_key(rows: tuple[int, ...], edges: tuple[RowPair, ...]) -> tuple[int, ...]:
    edge_set = set(edges)
    return tuple(int((m, n) in edge_set) for m in rows for n in rows)


def bilinear_sum(
    rows: tuple[int, ...], edges: tuple[RowPair, ...],
    left: tuple[int, ...], right: tuple[int, ...],
) -> int:
    index = {row: position for position, row in enumerate(rows)}
    return sum(left[index[m]] * right[index[n]] for m, n in edges)


def check_integer_weight_schur() -> tuple[int, dict[str, object]]:
    checks = 0
    rows = (5, 7, 11, 13)
    h = 1
    orbit = 1
    contents = (1, 2, 3, 4, 6, 8)
    graphs: list[tuple[str, tuple[RowPair, ...]]] = []
    seen: set[tuple[int, ...]] = set()

    predicates: list[tuple[str, Callable[[int], bool]]] = [
        ("positive-window", lambda delta: 1 <= delta < 7),
        ("negative-window", lambda delta: -7 <= delta < -1),
        ("translated-window", lambda delta: 3 <= delta < 10),
        ("residue-2-0", lambda delta: delta % 2 == 0),
        ("residue-3-1", lambda delta: delta % 3 == 1),
        ("window-residue", lambda delta: -8 <= delta < 8 and delta % 3 == 2),
        ("finite-omega", lambda delta: delta in {-8, -3, 2, 5}),
    ]
    for c in contents:
        for name, predicate in predicates:
            edges = difference_edges(rows, c, predicate)
            key = adjacency_key(rows, edges)
            if edges and key not in seen:
                seen.add(key)
                graphs.append((f"c={c}:{name}", edges))
            if len(graphs) >= 12:
                break
        if len(graphs) >= 12:
            break
    require(len(graphs) >= 6, "enough-distinct-schur-graphs", len(graphs))
    checks += 1

    weight_vectors = tuple(itertools.product((-1, 0, 1), repeat=len(rows)))
    maximum_ratio = Fraction(0)
    sharp_case: dict[str, object] | None = None
    tested_weight_pairs = 0
    for graph_name, edges in graphs:
        kout, kin, _, _ = bidirectional_degrees(rows, edges)
        require(kout > 0 and kin > 0,
                "nonempty-schur-graph-degrees", graph_name, kout, kin)
        checks += 1
        for left in weight_vectors:
            left_energy = sum(value * value for value in left)
            for right in weight_vectors:
                right_energy = sum(value * value for value in right)
                value = bilinear_sum(rows, edges, left, right)
                left_side = value * value
                right_side = kout * kin * left_energy * right_energy
                require(left_side <= right_side,
                        "integer-weight-schur-square",
                        graph_name, left, right, value,
                        kout, kin, left_energy, right_energy)
                checks += 1
                tested_weight_pairs += 1
                if right_side:
                    ratio = Fraction(left_side, right_side)
                    if ratio > maximum_ratio:
                        maximum_ratio = ratio
                        sharp_case = {
                            "graph": graph_name,
                            "left_weights": left,
                            "right_weights": right,
                            "bilinear_sum": value,
                            "out_degree": kout,
                            "in_degree": kin,
                            "left_energy": left_energy,
                            "right_energy": right_energy,
                        }

    require(maximum_ratio == 1,
            "schur-sharp-witness", maximum_ratio, sharp_case)
    checks += 1
    return checks, {
        "row_set": rows,
        "graphs": len(graphs),
        "graph_names": [name for name, _ in graphs],
        "weight_alphabet": [-1, 0, 1],
        "tested_weight_pairs": tested_weight_pairs,
        "maximum_squared_ratio": str(maximum_ratio),
        "sharp_case": sharp_case,
        "verified_inequality": (
            "|sum x_m y_n A(m,n)|^2 <= "
            "K_plus*K_minus*||x||_2^2*||y||_2^2"
        ),
    }


def primitive_congruence_count(
    m: int, h: int, modulus: int, start: int, horizon: int
) -> int:
    require(modulus >= 1 and horizon >= 1,
            "congruence-count-domain", modulus, horizon)
    return sum(
        1
        for orbit in range(start, start + horizon)
        if math.gcd(orbit, abs(h)) == 1
        and target(m, h, orbit) % modulus == 0
    )


def exact_content_orbits(
    m: int, n: int, h: int, c: int, start: int, horizon: int
) -> tuple[int, ...]:
    return tuple(
        orbit
        for orbit in range(start, start + horizon)
        if primitive_case(m, n, h, orbit)
        and target_content(m, n, h, orbit) == c
    )


def check_exact_content_occupancy() -> tuple[int, dict[str, object]]:
    checks = 0
    layers = 0
    nonempty_layers = 0
    strict_mobius_subsets = 0
    maximum_occupancy = 0
    maximum_record: dict[str, object] | None = None

    row_cases = (
        (5, 11, 1),
        (5, 17, 2),
        (7, 19, 6),
        (11, 23, 10),
        (13, 29, 12),
        (29, 13, 12),
    )
    starts = (1, 4, 9)
    horizons = (1, 2, 5, 13, 31)

    for m, n, h in row_cases:
        require(math.gcd(m, h) == math.gcd(n, h) == 1,
                "occupancy-row-primitivity", m, n, h)
        checks += 1
        delta = abs(m - n)
        for c in divisors(delta):
            for start in starts:
                for horizon in horizons:
                    direct_orbits = exact_content_orbits(
                        m, n, h, c, start, horizon)
                    mobius_total = sum(
                        mobius(d) * primitive_congruence_count(
                            m, h, c * d, start, horizon)
                        for d in divisors(delta // c)
                    )
                    require(len(direct_orbits) == mobius_total,
                            "exact-c-mobius-occupancy",
                            m, n, h, c, start, horizon,
                            direct_orbits, mobius_total)
                    checks += 1

                    congruence_count = primitive_congruence_count(
                        m, h, c, start, horizon)
                    require(len(direct_orbits) <= congruence_count,
                            "exact-c-subset-of-c-divisibility",
                            m, n, h, c, start, horizon,
                            len(direct_orbits), congruence_count)
                    checks += 1
                    require(len(direct_orbits) <= ceil_div(horizon, c),
                            "exact-c-window-occupancy-bound",
                            m, n, h, c, start, horizon,
                            len(direct_orbits), ceil_div(horizon, c))
                    checks += 1
                    if direct_orbits:
                        residues = {orbit % c for orbit in direct_orbits}
                        require(len(residues) == 1,
                                "exact-c-single-orbit-class",
                                m, n, h, c, start, horizon, residues)
                        checks += 1
                        nonempty_layers += 1
                    if len(direct_orbits) < congruence_count:
                        strict_mobius_subsets += 1
                    layers += 1
                    if len(direct_orbits) > maximum_occupancy:
                        maximum_occupancy = len(direct_orbits)
                        maximum_record = {
                            "m": m,
                            "n": n,
                            "h": h,
                            "c": c,
                            "start": start,
                            "horizon": horizon,
                            "orbits": direct_orbits,
                        }

        impossible_c = delta + 1
        for start in starts:
            for horizon in horizons:
                direct = exact_content_orbits(
                    m, n, h, impossible_c, start, horizon)
                require(not direct,
                        "nondivisor-content-layer-empty",
                        m, n, h, impossible_c, start, horizon, direct)
                checks += 1

    require(maximum_record is not None,
            "nonempty-exact-content-record-exists")
    checks += 1
    return checks, {
        "exact_layers": layers,
        "nonempty_layers": nonempty_layers,
        "strict_subsets_of_c_divisibility": strict_mobius_subsets,
        "maximum_occupancy": maximum_occupancy,
        "maximum_record": maximum_record,
        "verified_formula": (
            "#exact_c = sum_{d|Delta/c} mu(d) "
            "#primitive{c*d divides N_m(j)}"
        ),
        "verified_bound": "#exact_c in a length-J interval <= ceil(J/c)",
    }


def weighted_cell_sum(
    rows: tuple[int, ...], edges: Iterable[RowPair],
    left: tuple[int, ...], right: tuple[int, ...], absolute: bool,
) -> int:
    index = {row: position for position, row in enumerate(rows)}
    if absolute:
        return sum(abs(left[index[m]] * right[index[n]]) for m, n in edges)
    return sum(left[index[m]] * right[index[n]] for m, n in edges)


def check_cell_partition_no_go() -> tuple[int, dict[str, object]]:
    checks = 0
    partitions = 0
    edges_partitioned = 0
    absolute_reassembly_checks = 0
    cancellation_witness: dict[str, object] | None = None

    row_cases = (
        ("dense", tuple(range(5, 14)), 1, 1),
        ("sparse", (5, 7, 11, 16, 23, 31), 1, 2),
        ("shift-six", (5, 7, 11, 13, 17, 19), 6, 5),
    )
    moduli = (1, 2, 3, 4, 5, 7)

    for case_name, rows, h, orbit in row_cases:
        contents = sorted({
            target_content(m, n, h, orbit)
            for m in rows for n in rows
            if m != n and primitive_case(m, n, h, orbit)
        })
        left = tuple(((-1) ** index) * (index % 3 + 1)
                     for index in range(len(rows)))
        right = tuple(((-1) ** (index // 2)) * (2 - index % 3)
                      for index in range(len(rows)))

        for c in contents:
            total_edges = exact_c_edges(rows, h, orbit, c)
            total_set = set(total_edges)
            for modulus in moduli:
                cells = [
                    exact_c_edges(
                        rows, h, orbit, c,
                        lambda delta, q=modulus, a=residue:
                        delta % q == a,
                    )
                    for residue in range(modulus)
                ]
                union: set[RowPair] = set()
                multiplicity: defaultdict[RowPair, int] = defaultdict(int)
                for cell in cells:
                    for edge in cell:
                        union.add(edge)
                        multiplicity[edge] += 1
                require(union == total_set,
                        "residue-cells-cover-exact-c-graph",
                        case_name, c, modulus, union, total_set)
                checks += 1
                require(all(value == 1 for value in multiplicity.values()),
                        "residue-cells-disjoint",
                        case_name, c, modulus, dict(multiplicity))
                checks += 1
                require(sum(len(cell) for cell in cells) == len(total_edges),
                        "residue-cell-cardinality-reassembly",
                        case_name, c, modulus,
                        [len(cell) for cell in cells], len(total_edges))
                checks += 1

                total_signed = weighted_cell_sum(
                    rows, total_edges, left, right, absolute=False)
                cell_signed = [
                    weighted_cell_sum(rows, cell, left, right, absolute=False)
                    for cell in cells
                ]
                require(sum(cell_signed) == total_signed,
                        "signed-cell-reassembly",
                        case_name, c, modulus,
                        cell_signed, total_signed)
                checks += 1

                total_absolute = weighted_cell_sum(
                    rows, total_edges, left, right, absolute=True)
                cell_absolute = [
                    weighted_cell_sum(rows, cell, left, right, absolute=True)
                    for cell in cells
                ]
                require(sum(cell_absolute) == total_absolute,
                        "absolute-cell-reassembly-no-gain",
                        case_name, c, modulus,
                        cell_absolute, total_absolute)
                checks += 1
                absolute_reassembly_checks += 1
                partitions += 1
                edges_partitioned += len(total_edges)

                if (cancellation_witness is None
                        and sum(abs(value) for value in cell_signed)
                        > abs(total_signed)):
                    cancellation_witness = {
                        "case": case_name,
                        "rows": rows,
                        "h": h,
                        "j": orbit,
                        "c": c,
                        "modulus": modulus,
                        "left_weights": left,
                        "right_weights": right,
                        "cell_signed_sums": cell_signed,
                        "total_signed_sum": total_signed,
                        "sum_absolute_cell_sums": sum(
                            abs(value) for value in cell_signed),
                    }

    require(cancellation_witness is not None,
            "signed-reassembly-cancellation-witness-exists")
    checks += 1
    return checks, {
        "partitions": partitions,
        "edges_partitioned_with_multiplicity": edges_partitioned,
        "absolute_reassembly_checks": absolute_reassembly_checks,
        "verified_partition": (
            "exact-c graph is the disjoint union of Delta_sharp mod q cells"
        ),
        "verified_absolute_no_gain": (
            "sum_a absolute edge mass in cell a equals total absolute edge mass"
        ),
        "signed_cancellation_witness": cancellation_witness,
    }


def positive_part(value: Fraction) -> Fraction:
    return max(Fraction(0), value)


def window_cell_splice_saving(
    beta: Fraction, split_exp: Fraction, capacity_exp: Fraction
) -> Fraction:
    """Saving in the all-content window/residue-cell splice.

    The four ratios are J^{-1}, C^{-1}, X^{capacity} C/X, and
    X^{capacity}/Q.  Here C=X^{split_exp} and
    1+W/q=X^{capacity_exp+o(1)}.
    """
    return positive_part(min(
        1 - beta,
        split_exp,
        1 - split_exp - capacity_exp,
        beta - capacity_exp,
    ))


def optimal_window_cell_splice(
    beta: Fraction, capacity_exp: Fraction
) -> tuple[Fraction, Fraction]:
    optimum = positive_part(min(1 - beta, beta - capacity_exp))
    # This exact candidate is feasible because
    # 2*optimum <= (1-beta)+(beta-capacity) = 1-capacity.
    return optimum, optimum


def residue_cell_splice_saving(
    beta: Fraction, split_exp: Fraction, modulus_exp: Fraction
) -> Fraction:
    """Saving in the full-range single-residue all-content splice."""
    return positive_part(min(
        1 - beta,
        split_exp,
        1 - split_exp,
        beta,
        modulus_exp,
    ))


def optimal_residue_cell_splice(
    beta: Fraction, modulus_exp: Fraction
) -> tuple[Fraction, Fraction]:
    optimum = positive_part(min(1 - beta, beta, modulus_exp))
    # Since optimum <= min(beta,1-beta) <= 1/2, C=X^optimum
    # balances the two threshold terms and respects C <= Q.
    return optimum, optimum


def check_rational_splice_optimization() -> tuple[int, dict[str, object]]:
    checks = 0
    general_window_cases = 0
    general_residue_cases = 0

    denominators = (5, 7, 8, 10, 12, 16)
    for denominator in denominators:
        for beta_num in range(1, denominator):
            beta = Fraction(beta_num, denominator)
            for capacity_num in range(beta_num):
                capacity_exp = Fraction(capacity_num, denominator)
                optimum, split_star = optimal_window_cell_splice(
                    beta, capacity_exp)
                require(window_cell_splice_saving(
                    beta, split_star, capacity_exp) == optimum,
                    "window-optimum-attained",
                    beta, capacity_exp, optimum, split_star)
                checks += 1
                for split_num in range(0, 2 * beta_num + 1):
                    split_exp = Fraction(split_num, 2 * denominator)
                    require(window_cell_splice_saving(
                        beta, split_exp, capacity_exp) <= optimum,
                        "window-optimum-upper-bound",
                        beta, capacity_exp, split_exp, optimum)
                    checks += 1
                general_window_cases += 1

            for modulus_num in range(1, denominator + 1):
                modulus_exp = Fraction(modulus_num, denominator)
                optimum, split_star = optimal_residue_cell_splice(
                    beta, modulus_exp)
                require(residue_cell_splice_saving(
                    beta, split_star, modulus_exp) == optimum,
                    "residue-optimum-attained",
                    beta, modulus_exp, optimum, split_star)
                checks += 1
                for split_num in range(0, 2 * beta_num + 1):
                    split_exp = Fraction(split_num, 2 * denominator)
                    require(residue_cell_splice_saving(
                        beta, split_exp, modulus_exp) <= optimum,
                        "residue-optimum-upper-bound",
                        beta, modulus_exp, split_exp, optimum)
                    checks += 1
                general_residue_cases += 1

    beta = Fraction(267, 400)
    orbit_exp = 1 - beta
    width_equals_orbit = orbit_exp
    width_half = Fraction(1, 2)
    modulus_equals_orbit = orbit_exp

    window_j_opt, window_j_split = optimal_window_cell_splice(
        beta, width_equals_orbit)
    window_half_opt, window_half_split = optimal_window_cell_splice(
        beta, width_half)
    residue_j_opt, residue_j_split = optimal_residue_cell_splice(
        beta, modulus_equals_orbit)

    expected = {
        "window_J": (Fraction(133, 400), Fraction(133, 400)),
        "window_half": (Fraction(67, 400), Fraction(67, 400)),
        "residue_J": (Fraction(133, 400), Fraction(133, 400)),
    }
    actual = {
        "window_J": (window_j_opt, window_j_split),
        "window_half": (window_half_opt, window_half_split),
        "residue_J": (residue_j_opt, residue_j_split),
    }
    require(actual == expected,
            "high-beta-splice-values", actual, expected)
    checks += 1

    additional_cells = {
        "fully_coprime_J_window": positive_part(beta - orbit_exp),
        "macro_centered_all_content_J_window": positive_part(
            beta - orbit_exp),
        "general_window_residue_intersection": (
            optimal_window_cell_splice(beta, Fraction(0, 1))[0]),
        "macro_centered_window_residue_intersection": positive_part(beta),
    }
    additional_expected = {
        "fully_coprime_J_window": Fraction(67, 200),
        "macro_centered_all_content_J_window": Fraction(67, 200),
        "general_window_residue_intersection": Fraction(133, 400),
        "macro_centered_window_residue_intersection": Fraction(267, 400),
    }
    for name, expected_value in additional_expected.items():
        require(additional_cells[name] == expected_value,
                "high-beta-additional-cell-value",
                name, additional_cells[name], expected_value)
        checks += 1

    grid_denominator = 1600
    high_beta_grid: dict[str, dict[str, object]] = {}
    scenarios = (
        ("W_equals_J", "window", width_equals_orbit, window_j_opt),
        ("W_exponent_one_half", "window", width_half, window_half_opt),
        ("q_equals_J", "residue", modulus_equals_orbit, residue_j_opt),
    )
    max_eta_num = int(beta * grid_denominator)
    for name, kind, parameter, expected_optimum in scenarios:
        values: list[tuple[Fraction, Fraction]] = []
        for eta_num in range(max_eta_num + 1):
            split_exp = Fraction(eta_num, grid_denominator)
            if kind == "window":
                saving = window_cell_splice_saving(
                    beta, split_exp, parameter)
            else:
                saving = residue_cell_splice_saving(
                    beta, split_exp, parameter)
            values.append((split_exp, saving))
            require(saving <= expected_optimum,
                    "high-beta-grid-upper-bound",
                    name, split_exp, saving, expected_optimum)
            checks += 1
        grid_maximum = max(saving for _, saving in values)
        maximizers = [eta for eta, saving in values
                      if saving == grid_maximum]
        require(grid_maximum == expected_optimum,
                "high-beta-grid-optimum",
                name, grid_maximum, expected_optimum, maximizers)
        checks += 1
        high_beta_grid[name] = {
            "parameter_exponent": str(parameter),
            "optimum_saving": str(grid_maximum),
            "first_maximizing_split_exponent": str(min(maximizers)),
            "last_maximizing_split_exponent": str(max(maximizers)),
            "grid_denominator": grid_denominator,
            "grid_points": len(values),
        }

    return checks, {
        "formulas": {
            "window_cell_at_split": (
                "min(1-beta,kappa,1-kappa-s,beta-s)_+"
            ),
            "optimized_window_cell_splice": "min(1-beta,beta-s)_+",
            "residue_cell_at_split": (
                "min(1-beta,kappa,1-kappa,beta,rho)_+"
            ),
            "optimized_residue_cell_splice": "min(1-beta,beta,rho)",
        },
        "general_window_cases": general_window_cases,
        "general_residue_cases": general_residue_cases,
        "high_beta": {
            "beta": str(beta),
            "J_exponent": str(orbit_exp),
            "W_equals_J": {
                "W_exponent": str(width_equals_orbit),
                "optimal_split_exponent": str(window_j_split),
                "optimal_saving": str(window_j_opt),
            },
            "W_exponent_one_half": {
                "W_exponent": str(width_half),
                "optimal_split_exponent": str(window_half_split),
                "optimal_saving": str(window_half_opt),
            },
            "q_equals_J": {
                "q_exponent": str(modulus_equals_orbit),
                "optimal_split_exponent": str(residue_j_split),
                "optimal_saving": str(residue_j_opt),
            },
            "additional_cell_margins": {
                name: str(value)
                for name, value in additional_cells.items()
            },
            "grid_regression": high_beta_grid,
        },
    }


def main() -> None:
    checks = 0
    subcounts: dict[str, int] = {}

    count, primitive_summary = check_primitive_reduced_identities()
    checks += count
    subcounts["primitive_and_reduced_target_identities"] = count

    count, divisor_summary = check_selected_divisor_multiplier()
    checks += count
    subcounts["selected_divisor_multiplier"] = count

    count, degree_summary = check_cell_degree_bounds()
    checks += count
    subcounts["determinant_cell_degrees"] = count

    count, schur_summary = check_integer_weight_schur()
    checks += count
    subcounts["integer_weight_schur"] = count

    count, occupancy_summary = check_exact_content_occupancy()
    checks += count
    subcounts["exact_content_occupancy"] = count

    count, partition_summary = check_cell_partition_no_go()
    checks += count
    subcounts["cell_partition_and_absolute_reassembly"] = count

    count, exponent_summary = check_rational_splice_optimization()
    checks += count
    subcounts["rational_splice_optimization"] = count

    claims = {
        "finite_primitive_target_content_identity": True,
        "finite_reduced_targets_coprime": True,
        "finite_reduced_determinant_identity": True,
        "finite_selected_divisor_multiplier": True,
        "finite_Omega_degree_bound": True,
        "finite_window_degree_bound": True,
        "finite_residue_degree_bound": True,
        "finite_window_residue_degree_bound": True,
        "finite_integer_weight_schur_bound": True,
        "finite_exact_content_occupancy": True,
        "finite_residue_cell_partition": True,
        "finite_absolute_reassembly_identity": True,
        "finite_rational_splice_optimization": True,
        "sample_W_equals_J_saving_positive": True,
        "sample_W_half_saving_positive": True,
        "sample_q_equals_J_saving_positive": True,
        "uses_mobius_sign_cancellation": False,
        "uses_chowla_or_elliott_input": False,
        "proves_signed_dispersion": False,
        "closes_small_target_content_core": False,
        "closes_complete_ultra_difference": False,
        "closes_complete_residual": False,
        "proves_positivity": False,
        "proves_hardy_littlewood_asymptotic": False,
        "proves_twin_primes": False,
        "breaks_sieve_parity": False,
    }
    expected_true = {
        name for name in claims
        if name.startswith("finite_") or name.startswith("sample_")
    }
    require(all(claims[name] for name in expected_true),
            "positive-scope-flags", expected_true, claims)
    checks += len(expected_true)
    expected_false = set(claims) - expected_true
    require(all(not claims[name] for name in expected_false),
            "negative-scope-flags", expected_false, claims)
    checks += len(expected_false)
    subcounts["scope_flags"] = len(claims)

    source_path = Path(__file__)
    source_bytes = source_path.read_bytes()
    normalized_source = source_bytes.replace(b"\r\n", b"\n").replace(
        b"\r", b"\n")
    source_hash = hashlib.sha256(normalized_source).hexdigest()
    payload = {
        "paper": "TPC-31",
        "certificate": "canonical determinant support cells",
        "description": (
            "finite exact regression for canonical target content, reduced "
            "determinants, selected-divisor multipliers, determinant-cell "
            "degrees, integer-weight Schur bounds, exact-content occupancy, "
            "cell reassembly, and rational splice optimization; not a "
            "numerical proof of asymptotic Mobius cancellation"
        ),
        "exact_check_count": checks,
        "subcheck_counts": subcounts,
        "primitive_reduced_summary": primitive_summary,
        "selected_divisor_summary": divisor_summary,
        "cell_degree_summary": degree_summary,
        "integer_weight_schur_summary": schur_summary,
        "exact_content_occupancy_summary": occupancy_summary,
        "cell_partition_summary": partition_summary,
        "rational_splice_summary": exponent_summary,
        "claims": claims,
        "source_sha256": source_hash,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_digest"] = hashlib.sha256(
        canonical.encode("utf-8")).hexdigest()
    output_path = source_path.with_suffix(".json")
    output_path.write_bytes(
        (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
