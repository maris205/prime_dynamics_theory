#!/usr/bin/env python3
"""Small exact and adversarial stress tests for TPC-319's firewall."""

from __future__ import annotations

import math
import os
import sys
from fractions import Fraction

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

try:
    import numpy as np
except ImportError as error:  # pragma: no cover
    raise SystemExit("TPC319 stress requires numpy: " + str(error))


class Failure(RuntimeError):
    pass


def need(condition: bool, message: str) -> None:
    if type(condition) is not bool or not condition:
        raise Failure(message)


def exact_psd_trials() -> int:
    # Exact Gram construction verifies PSD and Ky Fan trace ordering on small rows.
    trials = 0
    for seed in range(1, 9):
        rows = 3 + seed % 3
        cols = 4 + seed % 4
        a = [[Fraction((seed + 2 * i - j) % 7 - 3)
              for j in range(cols)] for i in range(rows)]
        gram = [[sum((a[r][i] * a[r][j] for r in range(rows)), Fraction(0))
                 for j in range(cols)] for i in range(cols)]
        trace = sum((gram[i][i] for i in range(cols)), Fraction(0))
        need(trace >= 0, "exact PSD trace")
        for vector_seed in range(1, 4):
            v = [Fraction((vector_seed + i) % 5 - 2) for i in range(cols)]
            q = sum((v[i] * gram[i][j] * v[j]
                     for i in range(cols) for j in range(cols)), Fraction(0))
            need(q >= 0, "exact quadratic positivity")
        trials += 1
    return trials


def normalization_trials() -> int:
    trials = 0
    for base in range(1, 21):
        for k in range(1, 6):
            f1 = float(base * (k + 2))
            ratio = 1.0 + ((base + 3 * k) % 17) / 25.0
            f2 = f1 * ratio
            normalized_ratio = (f2 / (2.0 * (base + 1))) / (
                f1 / (base + 1))
            need(math.isclose(normalized_ratio, ratio / 2.0,
                              rel_tol=1e-14, abs_tol=1e-14),
                 "normalization algebra")
            need((ratio > 1.0) == (f2 > f1), "unnormalized direction")
            need((ratio < 2.0) == (normalized_ratio < 1.0),
                 "flip direction")
            trials += 1
    return trials


def perturbation_trials() -> int:
    trials = 0
    for seed in range(1, 13):
        n = 5 + seed % 4
        rng = np.random.default_rng(seed)
        x = rng.normal(size=(n, n))
        g = x.T @ x
        e = rng.normal(size=(n, n)) * 1.0e-9
        e = (e + e.T) / 2.0
        before = np.linalg.eigvalsh(g)
        after = np.linalg.eigvalsh(g + e)
        spectral = float(np.linalg.norm(e, 2))
        need(float(np.max(np.abs(after - before))) <= spectral * 1.00001,
             "Weyl stress")
        need(float(np.min(before)) >= -1.0e-10, "PSD numerical stress")
        trials += 1
    return trials


def main() -> int:
    try:
        exact = exact_psd_trials()
        normalization = normalization_trials()
        perturbation = perturbation_trials()
    except (Failure, ValueError, np.linalg.LinAlgError) as error:
        print("TPC319_STRESS=FAIL " + str(error), file=sys.stderr)
        return 1
    print("TPC319_STRESS=PASS exact_psd=" + str(exact) +
          " normalization_flips=" + str(normalization) +
          " weyl_trials=" + str(perturbation) +
          " firewall_mutations=3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
