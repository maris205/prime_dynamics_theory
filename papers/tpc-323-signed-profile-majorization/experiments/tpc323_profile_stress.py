#!/usr/bin/env python3
"""Deterministic algebraic stress tests for TPC-323."""

from __future__ import annotations

import argparse
import math
import sys

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC323 stress suite requires numpy: " + str(error))

PROFILE_TOL = 1.0e-10


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def profile(values: list[float]) -> np.ndarray:
    values_array = np.asarray(values, dtype=np.float64)
    values_array = np.maximum(values_array, 0.0)
    total = float(values_array.sum(dtype=np.float64))
    need(total > 0, "profile domain")
    result = values_array / total
    need(math.isclose(float(result.sum(dtype=np.float64)), 1.0,
                      rel_tol=1e-14, abs_tol=1e-14),
         "profile normalisation")
    return result


def metrics(signed: np.ndarray, direct: np.ndarray) -> tuple[float, float,
                                                               float, float, str]:
    delta = np.cumsum(signed - direct, dtype=np.float64)[:-1]
    minimum, maximum = float(delta.min()), float(delta.max())
    if minimum >= -PROFILE_TOL and maximum > PROFILE_TOL:
        label = "SIGNED_MAJORISES_DIRECT"
    elif maximum <= PROFILE_TOL and minimum < -PROFILE_TOL:
        label = "DIRECT_MAJORISES_SIGNED"
    elif minimum < -PROFILE_TOL and maximum > PROFILE_TOL:
        label = "MIXED"
    else:
        label = "UNRESOLVED"
    return (0.5 * float(np.abs(signed - direct).sum(dtype=np.float64)),
            float(np.max(np.abs(delta))), minimum, maximum, label)


def test_positive_scalar_invariance() -> None:
    base = profile([19.0, 7.0, 3.0, 1.0, 0.25])
    for scalar in (1.0e-9, 0.125, 1.0, 17.0, 1.0e9):
        scaled = profile((base * scalar).tolist())
        need(float(np.max(np.abs(base - scaled))) < 3.0e-15,
             "positive-scalar profile invariance")


def test_factorisation_and_projector_contraction() -> None:
    # A simple two-block family with a cancelling coordinate.  The coherent
    # energy is below the direct energy, yet its normalised profile is more
    # concentrated.  This is the exact amplitude/shape separation used by
    # the paper.
    b1 = np.diag(np.asarray([1.0, 1.0]))
    b2 = np.diag(np.asarray([0.0, 1.0]))
    direct = b1.T @ b1 + b2.T @ b2
    coherent = b1 - b2
    direct_energy = float(np.trace(direct))
    signed_gram = coherent.T @ coherent
    signed_energy = float(np.trace(signed_gram))
    need(math.isclose(direct_energy, 3.0, rel_tol=1e-14) and
         math.isclose(signed_energy, 1.0, rel_tol=1e-14),
         "energy expansion")
    rho = signed_energy / direct_energy
    signed_profile = profile(np.linalg.eigvalsh(signed_gram)[::-1].tolist())
    direct_profile = profile(np.linalg.eigvalsh(direct)[::-1].tolist())
    result = metrics(signed_profile, direct_profile)
    need(rho < 1.0 and result[-1] == "SIGNED_MAJORISES_DIRECT" and
         result[2] >= -PROFILE_TOL, "amplitude/shape separation")
    # The diagonal embedding E(v)=(v,-v)/sqrt(2) is an isometry, so the
    # projector fraction is rho/m and is contractive.
    need(0.0 <= rho / 2.0 <= 1.0, "projector fraction")


def test_majorization_geometry() -> None:
    concentrated = profile([8.0, 3.0, 1.0, 0.5])
    diffuse = profile([5.0, 4.0, 2.5, 1.0])
    mixed_left = profile([7.0, 2.0, 2.0, 1.0])
    mixed_right = profile([5.5, 3.5, 2.5, 1.0])
    need(metrics(concentrated, diffuse)[-1] ==
         "SIGNED_MAJORISES_DIRECT" and
         metrics(diffuse, concentrated)[-1] == "DIRECT_MAJORISES_SIGNED" and
         metrics(mixed_left, mixed_right)[-1] == "MIXED",
         "majorization labels")
    near = profile([1.0 + 2.0e-11, 1.0 - 2.0e-11, 1.0])
    flat = profile([1.0, 1.0, 1.0])
    need(metrics(near, flat)[-1] == "UNRESOLVED" or
         metrics(flat, near)[-1] == "UNRESOLVED", "near-tie guard")


def test_metric_bounds_and_symmetry() -> None:
    left = profile([12.0, 6.0, 2.0, 1.0])
    right = profile([8.0, 7.0, 4.0, 2.0])
    lr = metrics(left, right)
    rl = metrics(right, left)
    need(math.isclose(lr[0], rl[0], rel_tol=1e-14, abs_tol=1e-14) and
         math.isclose(lr[1], rl[1], rel_tol=1e-14, abs_tol=1e-14) and
         0.0 <= lr[0] <= 1.0 and 0.0 <= lr[1] <= 1.0,
         "metric symmetry/bounds")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        raise SystemExit("--check is required")
    try:
        test_positive_scalar_invariance()
        test_factorisation_and_projector_contraction()
        test_majorization_geometry()
        test_metric_bounds_and_symmetry()
    except (Failure, ValueError, np.linalg.LinAlgError) as error:
        print("TPC323_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC323_STRESS=PASS scalar_invariance=1 factorisation=1 "
          "majorization_geometry=1 metric_bounds=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
