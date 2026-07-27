"""Verify the rank-one/projective wrap formulas and replay RH-182."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH182 = PAPERS / "RH-182-finite-temporal-clock-physical-audit"
sys.path[:0] = [str(ROOT / "src"), str(RH182 / "src")]

from finite_clock import (  # noqa: E402
    apply_left_operator,
    column_operator_norm,
    normalized_orbit,
    polar_frame,
    temporal_synthesis,
    weighted_cycle,
)
from wrap_obstruction import (  # noqa: E402
    best_scalar_wrap_residual,
    optimal_wrap_phase,
    phase_optimized_chord,
    polar_wrap_bounds,
    projective_return_distance,
)


def formula_cases(smoke: bool) -> tuple[list[dict[str, float | int]], int]:
    rng = np.random.default_rng(183)
    dimensions = (4, 5) if smoke else (4, 5, 8, 11)
    trials = 4 if smoke else 10
    records = []
    failures = 0
    for dimension in dimensions:
        for length in (3, 4):
            for trial in range(trials):
                operator = rng.normal(size=(dimension, dimension)) / (2.0 * np.sqrt(dimension))
                operator += 0.35 * np.eye(dimension)
                seed = rng.normal(size=(dimension, 2))
                _, norms, units = normalized_orbit(operator, seed, length)
                synthesis = temporal_synthesis(units, 0, length)
                frame, gram, square_root, inverse_root = polar_frame(synthesis)
                phase = optimal_wrap_phase(units[0], units[length])
                cycle, weights = weighted_cycle(norms, 0, length, wrap_phase=phase)
                state_shape = units[0].shape
                direct = apply_left_operator(operator, synthesis, state_shape) - synthesis @ cycle
                direct_norm = column_operator_norm(direct)
                chord = phase_optimized_chord(units[0], units[length])
                expected_direct = float(weights[-1]) * chord
                reduced = square_root @ cycle @ inverse_root
                polar_residual = apply_left_operator(operator, frame, state_shape) - frame @ reduced
                actual_polar = column_operator_norm(polar_residual)
                gram_values = np.linalg.eigvalsh(gram)
                bounds = polar_wrap_bounds(weights[-1], chord, gram_values[0], gram_values[-1])
                scalar = best_scalar_wrap_residual(units[0], units[length], weights[-1])
                projective = projective_return_distance(units[0], units[length])
                formula_error = abs(direct_norm - expected_direct)
                scalar_error = abs(float(scalar["minimum_residual"]) - float(weights[-1]) * projective)
                bound_ok = float(bounds["lower_bound"]) <= actual_polar * (1.0 + 1e-10) + 1e-12 <= float(bounds["upper_bound"]) * (1.0 + 1e-10) + 1e-12
                failed = formula_error > 1e-10 or scalar_error > 1e-10 or not bound_ok
                failures += int(failed)
                records.append({
                    "dimension": dimension,
                    "length": length,
                    "trial": trial,
                    "rank_one_formula_error": formula_error,
                    "best_scalar_formula_error": scalar_error,
                    "polar_residual": actual_polar,
                    "polar_lower_bound": bounds["lower_bound"],
                    "polar_upper_bound": bounds["upper_bound"],
                    "bound_satisfied": bound_ok,
                })
    return records, failures


def run(smoke: bool) -> dict[str, object]:
    cases, failures = formula_cases(smoke)
    source_name = "temporal_clock_smoke.json" if smoke else "temporal_clock_audit.json"
    physical = json.loads((RH182 / "results" / source_name).read_text(encoding="utf-8"))
    records = physical["records"]
    gains = [float(item["unmarked_wrap_chord"]) - float(item["marked_wrap_chord"]) for item in records]
    return {
        "status": "rh183_projective_wrap_obstruction_audit",
        "formula_case_count": len(cases),
        "formula_failure_count": failures,
        "maximum_rank_one_formula_error": max(float(item["rank_one_formula_error"]) for item in cases),
        "maximum_best_scalar_formula_error": max(float(item["best_scalar_formula_error"]) for item in cases),
        "physical_window_count": physical["window_count"],
        "negative_orientation_count": physical["negative_orientation_count"],
        "phase_mark_improvement_count": sum(gain > 1e-12 for gain in gains),
        "maximum_phase_mark_chord_improvement": max(gains),
        "projective_wrap_at_most_0_25_count": sum(float(item["projective_wrap_distance"]) <= 0.25 for item in records),
        "orthogonal_three_gate_success_count": physical["three_gate_success_count"],
        "formula_records": cases,
        "theorem_boundary": {
            "exact_rank_one_wrap_identity": True,
            "phase_optimized_chord_formula": True,
            "arbitrary_scalar_projective_lower_bound": True,
            "polar_conditioning_bounds": True,
            "finite_physical_replay": not smoke,
            "all_level_no_go": False,
            "biorthogonal_route_rejected": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "wrap_obstruction_smoke.json" if args.smoke else "wrap_obstruction_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "formula_cases": payload["formula_case_count"],
        "formula_failures": payload["formula_failure_count"],
        "projective_returns": payload["projective_wrap_at_most_0_25_count"],
        "three_gate_successes": payload["orthogonal_three_gate_success_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
