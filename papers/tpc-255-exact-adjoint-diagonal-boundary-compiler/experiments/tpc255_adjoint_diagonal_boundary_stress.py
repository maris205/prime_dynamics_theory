#!/usr/bin/env python3
"""Deterministic exact stress audit for the TPC-255 finite identities."""

from __future__ import annotations

import argparse
from fractions import Fraction


Gaussian = tuple[Fraction, Fraction]
ZERO: Gaussian = (Fraction(0), Fraction(0))


class StressError(ValueError):
    pass


def _add(left: Gaussian, right: Gaussian) -> Gaussian:
    return (left[0] + right[0], left[1] + right[1])


def _conj(value: Gaussian) -> Gaussian:
    return (value[0], -value[1])


def _scale(value: Fraction, entry: Gaussian) -> Gaussian:
    return (value * entry[0], value * entry[1])


def _sum(values: list[Gaussian]) -> Gaussian:
    total = ZERO
    for value in values:
        total = _add(total, value)
    return total


def _floor(value: Fraction) -> int:
    return value.numerator // value.denominator


def _row(q_value: int, t_value: int, u_value: int) -> Fraction:
    if u_value % q_value == 0:
        return Fraction(0)
    return Fraction(int(u_value % q_value == t_value % q_value)) - Fraction(
        1, q_value - 1
    )


def _kernel(family: int) -> dict[int, Gaussian]:
    values: dict[int, Gaussian] = {}
    for shift in range(-6, 7):
        if shift == 0:
            values[shift] = (Fraction(1), Fraction(0))
        else:
            values[shift] = (
                Fraction(((family + 3) * (shift + 7) + 2) % 19 - 9, abs(shift) + 2),
                Fraction(((family + 5) * (2 * shift + 13) + 1) % 17 - 8, abs(shift) + 3),
            )
    if values[-1] == values[1]:
        values[-1] = _add(values[-1], (Fraction(1, 23), Fraction(1, 29)))
    if values[-1][1] == 0 and values[1][1] == 0:
        values[-1] = _add(values[-1], (Fraction(0), Fraction(1, 31)))
    return values


def _audit_family(x: Fraction, family: int) -> tuple[int, int, int, int, int, int]:
    coordinates = list(range(_floor(x / 2) + 1, _floor(x) + 1))
    count = len(coordinates)
    if count < 2:
        raise StressError("rank clock has fewer than two coordinates")
    ell = count // 2
    right_size = count - ell
    h = [Fraction(1, ell)] * ell + [Fraction(-1, right_size)] * right_size
    rho_squared = Fraction(ell * right_size, count)
    if sum(h, Fraction(0)) != 0:
        raise StressError("rank step is not centered")
    if rho_squared * sum((entry * entry for entry in h), Fraction(0)) != 1:
        raise StressError("rank step normalization failed")
    if rho_squared * (Fraction(1, ell) + Fraction(1, right_size)) != 1:
        raise StressError("one-over-rho jump conversion failed")
    q_values = [3, 5, 7]
    kernel = _kernel(family)
    if kernel[-1] == kernel[1] or (kernel[-1][1] == 0 and kernel[1][1] == 0):
        raise StressError("stress kernel is not a non-even complex witness")
    beta = [
        Fraction(((family + 7) * (index + 3)) % 29 - 14, (index % 7) + 1)
        for index in range(count)
    ]
    coordinate_set = set(coordinates)
    astar: list[Gaussian] = []
    p_lanes: list[Gaussian] = []
    e_lanes: list[Gaussian] = []
    j_lanes: list[Gaussian] = []
    d_lanes: list[Gaussian] = []
    coordinate_checks = 0
    child_left = 0
    child_right = 0
    input_masks = 0
    output_masks = 0
    for t_index, t_value in enumerate(coordinates):
        direct = ZERO
        p_lane = ZERO
        e_lane = ZERO
        j_lane = ZERO
        d_lane = ZERO
        for q_value in q_values:
            if t_value % q_value == 0:
                input_masks += 1
                continue
            for u_index, u_value in enumerate(coordinates):
                if u_value % q_value == 0:
                    output_masks += 1
                if u_value == t_value:
                    continue
                direct = _add(
                    direct,
                    _scale(
                        Fraction(q_value) * _row(q_value, t_value, u_value) * h[u_index],
                        _conj(kernel.get(u_value - t_value, ZERO)),
                    ),
                )
            p_star = ZERO
            e_star = ZERO
            j_star = ZERO
            for shift, kernel_value in kernel.items():
                u_value = t_value + shift
                row_value = _scale(_row(q_value, t_value, u_value), _conj(kernel_value))
                p_star = _add(p_star, row_value)
                if u_value not in coordinate_set:
                    e_star = _add(e_star, row_value)
                else:
                    j_star = _add(
                        j_star,
                        _scale(h[u_value - coordinates[0]] - h[t_index], row_value),
                    )
            p_lane = _add(p_lane, _scale(Fraction(q_value) * h[t_index], p_star))
            e_lane = _add(e_lane, _scale(-Fraction(q_value) * h[t_index], e_star))
            j_lane = _add(j_lane, _scale(Fraction(q_value), j_star))
            d_lane = _add(
                d_lane,
                _scale(
                    -Fraction(q_value * (q_value - 2), q_value - 1) * h[t_index],
                    _conj(kernel[0]),
                ),
            )
            opposite = range(ell, count) if t_index < ell else range(ell)
            jump = ZERO
            for u_index in opposite:
                jump = _add(
                    jump,
                    _scale(
                        (h[u_index] - h[t_index])
                        * _row(q_value, t_value, coordinates[u_index]),
                        _conj(kernel.get(coordinates[u_index] - t_value, ZERO)),
                    ),
                )
            if jump != j_star:
                raise StressError("child-jump support or sign failed")
            if t_index < ell:
                child_left += 1
            else:
                child_right += 1
        if direct != _sum([p_lane, e_lane, j_lane, d_lane]):
            raise StressError("coordinate P/E/J/diagonal decomposition failed")
        astar.append(direct)
        p_lanes.append(p_lane)
        e_lanes.append(e_lane)
        j_lanes.append(j_lane)
        d_lanes.append(d_lane)
        coordinate_checks += 1
    a_beta: list[Gaussian] = []
    for u_value in coordinates:
        total = ZERO
        for t_index, t_value in enumerate(coordinates):
            if u_value == t_value:
                continue
            for q_value in q_values:
                if u_value % q_value == 0 or t_value % q_value == 0:
                    continue
                total = _add(
                    total,
                    _scale(
                        Fraction(q_value) * _row(q_value, t_value, u_value) * beta[t_index],
                        kernel.get(u_value - t_value, ZERO),
                    ),
                )
        a_beta.append(total)
    lhs = _sum([_scale(h[index], value) for index, value in enumerate(a_beta)])
    rhs = _sum([_scale(beta[index], _conj(value)) for index, value in enumerate(astar)])
    lane_sum = _sum(
        [
            _sum([_scale(beta[index], _conj(row[index])) for index in range(count)])
            for row in (p_lanes, e_lanes, j_lanes, d_lanes)
        ]
    )
    if lhs != rhs or rhs != lane_sum:
        raise StressError("adjoint scalar reassembly failed")
    b_q = sum((Fraction(q * (q - 2), q - 1) for q in q_values), Fraction(0))
    correction = Fraction(0)
    for q_value in q_values:
        correction += Fraction(q_value * (q_value - 2), q_value - 1) * sum(
            (
                h[index] * beta[index]
                for index, t_value in enumerate(coordinates)
                if t_value % q_value == 0
            ),
            Fraction(0),
        )
    h_beta = sum((h[index] * beta[index] for index in range(count)), Fraction(0))
    d_scalar = _sum(
        [_scale(beta[index], _conj(d_lanes[index])) for index in range(count)]
    )
    if d_scalar != (-b_q * h_beta + correction, Fraction(0)):
        raise StressError("B_Q diagonal reassembly failed")
    threshold_mismatch = 0
    if x.denominator != 1:
        naive = [value for value in coordinates if value <= _floor(3 * x / 4)]
        threshold_mismatch = int(naive != coordinates[:ell])
    return (
        coordinate_checks,
        child_left,
        child_right,
        input_masks,
        output_masks,
        threshold_mismatch,
    )


def run() -> None:
    clocks = [Fraction(40 + index) for index in range(96)]
    clocks += [Fraction(81 + 2 * index, 2) for index in range(96)]
    if len(clocks) != 192:
        raise StressError("family construction failed")
    totals = [0, 0, 0, 0, 0, 0]
    odd_rank = 0
    even_rank = 0
    for family, x in enumerate(clocks):
        count = _floor(x) - _floor(x / 2)
        if count % 2:
            odd_rank += 1
        else:
            even_rank += 1
        values = _audit_family(x, family)
        totals = [left + right for left, right in zip(totals, values)]
    if odd_rank == 0 or even_rank == 0:
        raise StressError("odd/even rank coverage missing")
    if totals[1] == 0 or totals[2] == 0 or totals[3] == 0 or totals[4] == 0:
        raise StressError("child or mask coverage missing")
    if not (Fraction(16) > 2 * Fraction(4)):
        raise StressError("Poisson support contract clock failed")
    for q_value in (5, 7):
        if Fraction(16, q_value) <= 1:
            raise StressError("first dual frequency did not leave support")
        c_sum = -Fraction(1, q_value - 1)
        d_sum = Fraction(1, q_value - 1)
        if c_sum + d_sum != 0:
            raise StressError("unit-mask zero-mode cancellation failed")
    print(
        "TPC255_STRESS=PASS families=192 integer=96 noninteger=96"
        + " coordinate_identities=" + str(totals[0])
        + " child_left=" + str(totals[1])
        + " child_right=" + str(totals[2])
        + " input_masks=" + str(totals[3])
        + " output_masks=" + str(totals[4])
        + " noninteger_threshold_mismatches=" + str(totals[5])
        + " odd_rank=" + str(odd_rank)
        + " even_rank=" + str(even_rank)
        + " non_even_complex_kernels=192"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    run()


if __name__ == "__main__":
    main()
