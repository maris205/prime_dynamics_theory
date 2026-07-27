#!/usr/bin/env python3
"""Finite audit for the TPC-130 Fejer/four-sign certificate."""

from __future__ import annotations

import argparse
import cmath
import difflib
from fractions import Fraction
import json
from pathlib import Path
import sys


TOL = 1.0e-10


def exp_turns(t: float) -> complex:
    return cmath.exp(2j * cmath.pi * t)


def liouville(n: int) -> int:
    value = 1
    p = 2
    while p * p <= n:
        while n % p == 0:
            n //= p
            value = -value
        p += 1
    if n > 1:
        value = -value
    return value


def audit() -> dict:
    values = [
        complex((7 * k) % 11 - 5, ((3 * k) % 7 - 3) / 5)
        for k in range(1, 24)
    ]
    n_len = len(values)
    alpha = 0.173
    h_len = 7

    def value(index: int) -> complex:
        return values[index] if 0 <= index < n_len else 0j

    correlations: dict[int, complex] = {}
    for h in range(-(h_len - 1), h_len):
        correlations[h] = sum(
            value(z + h) * value(z).conjugate()
            for z in range(n_len)
        )

    kernel = sum(
        (1 - abs(h) / h_len)
        * exp_turns(-alpha * h)
        * correlations[h]
        for h in range(-(h_len - 1), h_len)
    )

    window_energy = 0.0
    for t in range(1 - h_len, n_len):
        window = sum(
            value(t + j) * exp_turns(-alpha * (t + j))
            for j in range(h_len)
        )
        window_energy += abs(window) ** 2
    window_identity_ok = abs(h_len * kernel - window_energy) <= TOL * max(
        1.0, abs(window_energy)
    )
    kernel_real_nonnegative = (
        abs(kernel.imag) <= TOL * max(1.0, abs(kernel.real))
        and kernel.real >= -TOL
    )

    total = sum(
        values[z] * exp_turns(-alpha * (z + 1))
        for z in range(n_len)
    )
    fejer_upper = (n_len + h_len - 1) / h_len * kernel.real
    fejer_inequality_ok = abs(total) ** 2 <= fejer_upper + TOL

    mass = sum(abs(v) for v in values)
    energy = sum(abs(v) ** 2 for v in values)
    participation = mass**2 / (n_len * energy)
    offdiag = kernel.real - energy
    normalized_rhs = 2 * (
        1 / (h_len * participation)
        + n_len * max(offdiag, 0) / (h_len * mass**2)
    )
    normalized_ok = abs(total) ** 2 / mass**2 <= normalized_rhs + TOL

    # Independently audit the window count and H-fold participation
    # with exact integer/Fraction arithmetic at phase zero.
    exact_values = [3, -1, 4, 0, -2, 5]
    exact_n = len(exact_values)
    exact_h = 4

    def exact_value(index: int) -> int:
        return (
            exact_values[index]
            if 0 <= index < exact_n
            else 0
        )

    exact_correlations = {
        h: sum(
            exact_value(z + h) * exact_value(z)
            for z in range(exact_n)
        )
        for h in range(-(exact_h - 1), exact_h)
    }
    exact_kernel = sum(
        Fraction(exact_h - abs(h), exact_h)
        * exact_correlations[h]
        for h in range(-(exact_h - 1), exact_h)
    )
    exact_windows = [
        sum(exact_value(t + j) for j in range(exact_h))
        for t in range(1 - exact_h, exact_n)
    ]
    exact_window_energy = sum(
        window * window for window in exact_windows
    )
    exact_window_identity_ok = (
        exact_h * exact_kernel == exact_window_energy
        and len(exact_windows) == exact_n + exact_h - 1
    )
    participation_counts = [
        sum(
            1
            for t in range(1 - exact_h, exact_n)
            if t <= z <= t + exact_h - 1
        )
        for z in range(exact_n)
    ]
    exact_h_participation_ok = participation_counts == [
        exact_h
    ] * exact_n

    # Verify the shift-two four-sign identity on a determinant-two frame.
    a, s, d, u = 3, 5, 1, 1
    q = a * s
    shift = 4
    four_sign_ok = True
    for z in range(0, 20 - shift):
        n = s * (u + a * z)
        direct = (
            liouville(d + s * (z + shift))
            * liouville(u + a * (z + shift))
            * liouville(d + s * z)
            * liouville(u + a * z)
        )
        pulled = (
            liouville(n + q * shift - 2)
            * liouville(n + q * shift)
            * liouville(n - 2)
            * liouville(n)
        )
        four_sign_ok &= direct == pulled

    # Sparse support: short off-diagonals vanish and H*p is O(1).
    sparse_h = 9
    sparse_n = 10 * sparse_h
    sparse = [0j] * sparse_n
    for index in range(0, sparse_n, sparse_h):
        sparse[index] = 1 + 0j
    sparse_mass = sum(abs(v) for v in sparse)
    sparse_energy = sum(abs(v) ** 2 for v in sparse)
    sparse_p = sparse_mass**2 / (sparse_n * sparse_energy)
    sparse_offdiag_zero = all(
        abs(
            sum(
                sparse[z + h] * sparse[z].conjugate()
                for z in range(sparse_n - h)
            )
        )
        <= TOL
        for h in range(1, sparse_h)
    )
    sparse_saturates = (
        abs(sum(sparse)) == sparse_mass
        and sparse_h * sparse_p <= 1.0 + TOL
    )

    # Zero-mass prefixes have S=E=V=0.  They pass trivially and must
    # be excluded from any formula dividing by V or defining p.
    zero_prefix = [0j] * 8
    zero_sum = sum(zero_prefix)
    zero_mass = sum(abs(value) for value in zero_prefix)
    zero_energy = sum(abs(value) ** 2 for value in zero_prefix)
    zero_mass_prefix_ok = (
        zero_sum == 0j and zero_mass == 0 and zero_energy == 0
    )

    # Keep the local square-root budget distinct from the older,
    # stronger termwise screen.
    quadratic_squared_target = Fraction(1, 200)
    local_amplitude_target = quadratic_squared_target / 2
    conservative_termwise_target = Fraction(1, 200)
    endpoint_budget_distinction_ok = (
        local_amplitude_target == Fraction(1, 400)
        and conservative_termwise_target == Fraction(1, 200)
        and conservative_termwise_target > local_amplitude_target
    )

    result = {
        "sliding_window_identity": window_identity_ok,
        "exact_integer_window_identity": exact_window_identity_ok,
        "exact_H_fold_participation": exact_h_participation_ok,
        "fejer_kernel_real_nonnegative": kernel_real_nonnegative,
        "fejer_inequality": fejer_inequality_ok,
        "normalized_certificate": normalized_ok,
        "shift_two_four_sign_crosswalk": four_sign_ok,
        "sparse_short_correlations_zero": sparse_offdiag_zero,
        "sparse_diagonal_stop": sparse_saturates,
        "zero_mass_prefix_trivial": zero_mass_prefix_ok,
        "endpoint_budget_distinction": endpoint_budget_distinction_ok,
        "sample": {
            "kernel": [kernel.real, kernel.imag],
            "window_energy": window_energy,
            "fejer_upper": fejer_upper,
            "sum_square": abs(total) ** 2,
            "participation": participation,
            "sparse_H_times_participation": sparse_h * sparse_p,
            "exact_window_audit": {
                "N": exact_n,
                "H": exact_h,
                "window_count": len(exact_windows),
                "expected_window_count": exact_n + exact_h - 1,
                "participation_counts": participation_counts,
                "kernel": str(exact_kernel),
                "window_energy": exact_window_energy,
            },
            "zero_mass_prefix": {
                "mass": 0,
                "energy": 0,
                "sum": [0, 0],
                "participation": None,
                "status": "trivial_zero_excluded_from_normalized_maximum",
            },
            "endpoint_budget": {
                "quadratic_squared_saving": str(
                    quadratic_squared_target
                ),
                "local_square_root_amplitude": str(
                    local_amplitude_target
                ),
                "conservative_termwise_amplitude": str(
                    conservative_termwise_target
                ),
                "interpretation": (
                    "1/400 is the local square-root target; "
                    "1/200 is a stronger sufficient screen"
                ),
            },
        },
        "level": {
            "finite_certificate": "L0",
            "actual_four_sign_crosswalk": "L1",
            "growing_four_sign_bound": "not proved",
        },
    }
    result["all_checks_passed"] = all(
        result[key]
        for key in (
            "sliding_window_identity",
            "exact_integer_window_identity",
            "exact_H_fold_participation",
            "fejer_kernel_real_nonnegative",
            "fejer_inequality",
            "normalized_certificate",
            "shift_two_four_sign_crosswalk",
            "sparse_short_correlations_zero",
            "sparse_diagonal_stop",
            "zero_mass_prefix_trivial",
            "endpoint_budget_distinction",
        )
    )
    return result


def serialized(output: dict) -> str:
    return json.dumps(output, indent=2, sort_keys=True) + "\n"


def check_or_write(path: Path, rendered: str, check: bool) -> bool:
    if not check:
        path.write_text(rendered, encoding="utf-8")
        return True
    if not path.exists():
        print(f"{path}: missing audit artifact", file=sys.stderr)
        return False
    current = path.read_text(encoding="utf-8")
    if current == rendered:
        return True
    print(f"{path}: stale audit artifact", file=sys.stderr)
    sys.stderr.writelines(
        difflib.unified_diff(
            current.splitlines(keepends=True),
            rendered.splitlines(keepends=True),
            fromfile=str(path),
            tofile="generated",
        )
    )
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare with the committed JSON without rewriting it",
    )
    args = parser.parse_args()
    output = audit()
    path = Path(__file__).with_suffix(".json")
    rendered = serialized(output)
    artifact_ok = check_or_write(path, rendered, args.check)
    print(rendered, end="")
    if not output["all_checks_passed"] or not artifact_ok:
        raise SystemExit(1)
