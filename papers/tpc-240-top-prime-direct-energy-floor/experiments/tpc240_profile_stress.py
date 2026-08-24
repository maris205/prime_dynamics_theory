#!/usr/bin/env python3
"""Finite smooth-profile stress tests for TPC-240 row and Riemann identities."""

from __future__ import annotations

import argparse
import json
import math
from math import isqrt
from typing import Any, Callable


class StressFailure(RuntimeError):
    """Fail-closed finite stress error."""


def demand(condition: bool, message: str) -> None:
    if type(condition) is not bool:
        raise StressFailure("stress condition is not a strict bool")
    if not condition:
        raise StressFailure(message)


def strict_integer(value: object, name: str) -> int:
    demand(type(value) is int, f"{name} must be an exact int")
    return value


def prime(value: int) -> bool:
    strict_integer(value, "prime candidate")
    if value < 2:
        return False
    for divisor in range(2, isqrt(value) + 1):
        if value % divisor == 0:
            return False
    return True


def smooth_raw(t: float, shape: str) -> float:
    demand(type(t) is float and math.isfinite(t), "invalid profile coordinate")
    demand(type(shape) is str, "shape type")
    if abs(t) >= 1.0:
        return 0.0
    bump = math.exp(-1.0 / (1.0 - t * t))
    if shape == "STANDARD_BUMP":
        factor = 1.0
    elif shape == "QUADRATIC_TILT_BUMP":
        factor = 1.0 + 0.25 * t * t
    else:
        raise StressFailure("unknown smooth profile shape")
    return bump * factor


def simpson(function: Callable[[float], float], panels: int = 32768) -> float:
    strict_integer(panels, "Simpson panels")
    demand(panels > 0 and panels % 2 == 0, "Simpson panel parity")
    left, right = -1.0, 1.0
    step = (right - left) / panels
    total = function(left) + function(right)
    for index in range(1, panels):
        weight = 4.0 if index % 2 else 2.0
        total += weight * function(left + index * step)
    value = total * step / 3.0
    demand(math.isfinite(value), "nonfinite Simpson value")
    return value


def profile_record(shape: str) -> tuple[Callable[[float], float], dict[str, Any]]:
    normalization = simpson(lambda t: smooth_raw(t, shape))
    demand(normalization > 0.0, "nonpositive profile normalization")

    def psi(t: float) -> float:
        return smooth_raw(t, shape) / normalization

    integral_check = simpson(psi)
    kappa = simpson(lambda t: psi(t) ** 2)
    grid_max = max(psi(-1.0 + 2.0 * index / 20000) for index in range(20001))
    grid_min = min(psi(-1.0 + 2.0 * index / 20000) for index in range(20001))
    demand(abs(integral_check - 1.0) <= 2.0e-12, "profile normalization stress")
    demand(grid_min >= -1.0e-15, "profile nonnegativity stress")
    demand(grid_max <= 1.0 + 1.0e-12, "profile upper-bound stress")
    demand(0.5 - 1.0e-10 <= kappa <= 1.0 + 1.0e-10, "kappa range stress")
    return psi, {
        "exact_definition": "raw(t)/integral_{-1}^1 raw(s) ds",
        "kappa_approx": scientific(kappa),
        "maximum_grid_approx": scientific(grid_max),
        "minimum_grid_approx": scientific(grid_min),
        "normalization_approx": scientific(normalization),
        "normalized_integral_approx": scientific(integral_check),
        "shape": shape,
    }


def scientific(value: float) -> str:
    demand(type(value) is float and math.isfinite(value), "invalid finite real")
    return format(value, ".12e")


def row_stress(
    Q: int,
    H: int,
    U: int,
    p: int,
    q: int,
    psi: Callable[[float], float],
    kappa: float,
) -> dict[str, Any]:
    for value, name in ((Q, "Q"), (H, "H"), (U, "U"), (p, "p"), (q, "q")):
        strict_integer(value, name)
    demand(4 * Q < H, "fixture 4Q<H")
    demand(U < Q, "fixture U<Q")
    demand(prime(p) and U / 2.0 < p <= U, "fixture top prime")
    demand(prime(q) and Q < q <= 2 * Q, "fixture shell prime")
    cutoff = p * q // H
    demand(2 * cutoff < p, "fixture injective cutoff")
    inverse = pow(q, -1, p)
    residue_row: dict[int, float] = {}
    direct_energy = 0.0
    for m in range(-cutoff, cutoff + 1):
        if m == 0:
            continue
        residue = m * inverse % p
        demand(residue != 0, "stress zero residue")
        demand(residue not in residue_row, "stress residue collision")
        weight = psi(H * m / (p * q))
        demand(weight >= -1.0e-15, "stress negative row weight")
        residue_row[residue] = weight
        direct_energy += weight * weight
    row_energy = sum(weight * weight for weight in residue_row.values())
    difference = abs(row_energy - direct_energy)
    tolerance = 5.0e-14 * max(1.0, direct_energy)
    demand(difference <= tolerance, "stress row/direct energy mismatch")
    depth = p * q / H
    ratio = direct_energy / depth
    error = abs(ratio - kappa)
    return {
        "H": H,
        "Q": Q,
        "U": U,
        "atom_count": len(residue_row),
        "cutoff": cutoff,
        "direct_energy_approx": scientific(direct_energy),
        "lattice_depth_approx": scientific(depth),
        "p": p,
        "q": q,
        "riemann_error_approx": scientific(error),
        "row_direct_difference_approx": scientific(difference),
        "row_energy_approx": scientific(row_energy),
        "row_over_depth_approx": scientific(ratio),
    }


def stress() -> dict[str, Any]:
    parameter_grid = [
        (101, 409, 97, 97, 199),
        (211, 853, 199, 199, 421),
        (401, 1613, 397, 397, 797),
    ]
    profile_outputs: list[dict[str, Any]] = []
    total_rows = 0
    maximum_identity_error = 0.0
    for shape in ("STANDARD_BUMP", "QUADRATIC_TILT_BUMP"):
        psi, metadata = profile_record(shape)
        kappa = float(metadata["kappa_approx"])
        rows = [row_stress(*fixture, psi, kappa) for fixture in parameter_grid]
        errors = [float(row["riemann_error_approx"]) for row in rows]
        demand(errors[-1] < errors[0], f"{shape} Riemann error did not improve")
        demand(errors[-1] <= 0.30 * errors[0], f"{shape} Riemann improvement too weak")
        metadata["fixtures"] = rows
        metadata["riemann_error_improved"] = True
        profile_outputs.append(metadata)
        total_rows += len(rows)
        maximum_identity_error = max(
            maximum_identity_error,
            *(float(row["row_direct_difference_approx"]) for row in rows),
        )
    return {
        "TPC240_PROFILE_STRESS": "PASS",
        "classification": "NUMERICAL_FINITE_ILLUSTRATION_ONLY",
        "legitimate_fixed_smooth_profile_shapes": len(profile_outputs),
        "maximum_row_identity_error_approx": scientific(maximum_identity_error),
        "prime_fixtures_per_profile": len(parameter_grid),
        "profiles": profile_outputs,
        "rows_checked": total_rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", required=True)
    parser.parse_args()
    print(
        json.dumps(
            stress(),
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except StressFailure as error:
        raise SystemExit(f"TPC240_PROFILE_STRESS=FAIL: {error}")
