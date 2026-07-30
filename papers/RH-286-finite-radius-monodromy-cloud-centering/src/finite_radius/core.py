from __future__ import annotations

import csv
from collections import defaultdict
import math
from pathlib import Path


LAMBDA = 1.678573510428322
R_H = 0.85
BETA = 1.0 / (R_H * math.sqrt(LAMBDA))


def root_l1_bias_limit(beta: float, multiplier_constant: float) -> float:
    if beta <= 0.0 or multiplier_constant <= 0.0:
        raise ValueError("positive constants required")
    return beta * abs(math.log(multiplier_constant))


def moment_bias_constant(order: int, beta: float, multiplier_constant: float) -> float:
    if order < 1:
        raise ValueError("order must be positive")
    return order * beta**order * abs(math.log(multiplier_constant))


def _finite_radii(path: Path) -> dict[int, float]:
    radii: dict[int, float] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            radii[int(row["component_period"])] = (
                float(row["one_step_cycle_radius"]) / R_H
            )
    return radii


def audit_cloud(cloud_path: Path, radius_path: Path) -> list[dict[str, float | int]]:
    groups: dict[float, list[dict[str, str]]] = defaultdict(list)
    with cloud_path.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if row["positive_order"].isdigit():
                groups[float(row["sigma"])].append(row)
    radii = _finite_radii(radius_path)
    output = []
    for sigma in sorted(groups, reverse=True):
        rows = sorted(groups[sigma], key=lambda item: int(item["positive_order"]))
        degree = int(rows[0]["effective_cloud_degree"])
        finite_beta = radii[degree + 1]
        actual: list[complex] = []
        limiting: list[complex] = []
        finite: list[complex] = []
        for row in rows:
            order = int(row["positive_order"])
            value = complex(float(row["real"]), float(row["imag"])) / R_H
            angle = order * math.pi / (degree + 1)
            phase = complex(math.cos(angle), math.sin(angle))
            for item, target_limit, target_finite in (
                (value, BETA * phase, finite_beta * phase),
                (value.conjugate(), (BETA * phase).conjugate(), (finite_beta * phase).conjugate()),
            ):
                actual.append(item)
                limiting.append(target_limit)
                finite.append(target_finite)
        limit_total = sum(abs(a - b) for a, b in zip(actual, limiting))
        finite_total = sum(abs(a - b) for a, b in zip(actual, finite))
        limit_moments = []
        finite_moments = []
        for order in range(2, min(12, 2 * degree + 1) + 1):
            actual_moment = sum(value**order for value in actual)
            limit_target = -2 * BETA**order if order % 2 == 0 else 0.0
            finite_target = -2 * finite_beta**order if order % 2 == 0 else 0.0
            limit_moments.append(abs(actual_moment - limit_target))
            finite_moments.append(abs(actual_moment - finite_target))
        output.append(
            {
                "sigma": sigma,
                "degree": degree,
                "finite_beta": finite_beta,
                "limiting_total_root_error": limit_total,
                "finite_total_root_error": finite_total,
                "limiting_maximum_moment_error": max(limit_moments),
                "finite_maximum_moment_error": max(finite_moments),
            }
        )
    return output
