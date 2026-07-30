from __future__ import annotations

import csv
from collections import defaultdict
import math
from pathlib import Path

LAMBDA = 1.678573510428322
R_H = 0.85
BETA = 1.0 / (R_H * math.sqrt(LAMBDA))


def audit_csv(path: Path) -> list[dict[str, float | int]]:
    groups: dict[float, list[dict[str, str]]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["positive_order"].isdigit():
                groups[float(row["sigma"])].append(row)
    output = []
    for sigma in sorted(groups, reverse=True):
        rows = sorted(groups[sigma], key=lambda item: int(item["positive_order"]))
        N = int(rows[0]["effective_cloud_degree"])
        actual: list[complex] = []
        ideal: list[complex] = []
        phase_l1 = 0.0
        radial_l1 = 0.0
        for row in rows:
            order = int(row["positive_order"])
            value = complex(float(row["real"]), float(row["imag"])) / R_H
            target = BETA * complex(math.cos(order * math.pi / (N + 1)), math.sin(order * math.pi / (N + 1)))
            actual.extend((value, value.conjugate()))
            ideal.extend((target, target.conjugate()))
            phase_l1 += abs(float(row["phase_error"]))
            radial_l1 += abs(abs(value) - BETA)
        total_error = sum(abs(a - b) for a, b in zip(actual, ideal))
        moment_errors = []
        for n in range(2, min(12, 2 * N + 1) + 1):
            target = -2 * BETA**n if n % 2 == 0 else 0.0
            moment_errors.append(abs(sum(z**n for z in actual) - target))
        output.append({
            "sigma": sigma, "N": N, "rank": 2 * N,
            "total_root_error": total_error,
            "mean_root_error": total_error / (2 * N),
            "N_times_mean_root_error": total_error / 2,
            "positive_phase_l1": phase_l1,
            "positive_radial_l1": radial_l1,
            "maximum_pre_alias_moment_error": max(moment_errors),
        })
    return output
