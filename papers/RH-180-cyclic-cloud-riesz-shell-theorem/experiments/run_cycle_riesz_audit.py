"""Finite matrix audit of the explicit double-cycle Riesz-shell theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cycle_riesz import cycle_roots, cycle_shell_budget, double_cycle_seed, root_half_spacing  # noqa: E402


POLE = 1.6785735104283224


def scaled_random(rng: np.random.Generator, shape: tuple[int, int], target_norm: float) -> np.ndarray:
    raw = rng.normal(size=shape) + 1j * rng.normal(size=shape)
    norm = float(np.linalg.norm(raw, 2))
    return raw * (float(target_norm) / norm)


def run(smoke: bool) -> dict[str, object]:
    rng = np.random.default_rng(180)
    lengths = (4, 6) if smoke else (4, 5, 6, 8, 10, 12)
    trials = 3 if smoke else 32
    radius = 1.0 / POLE
    records = []
    for length in lengths:
        seed = double_cycle_seed(length, radius)
        roots = cycle_roots(length, radius)
        packet_dimension = seed.shape[0]
        complement_dimension = 3
        contour_radius = 0.35 * root_half_spacing(length, radius)
        packet_perturbation = 0.15 * contour_radius
        complement_phases = np.exp(2j * np.pi * np.arange(complement_dimension) / complement_dimension)
        complement_eigenvalues = 2.5 * radius * complement_phases
        complement = np.diag(complement_eigenvalues)
        minimum_complement_boundary_distance = min(abs(root - value) - contour_radius for root in roots for value in complement_eigenvalues)
        complement_resolvent = 1.0 / minimum_complement_boundary_distance
        packet_resolvent = 1.0 / (contour_radius - packet_perturbation)
        target_product = 0.20
        coupling_norm = np.sqrt(target_product / (packet_resolvent * complement_resolvent))
        budget = cycle_shell_budget(
            length,
            radius,
            contour_radius,
            packet_perturbation,
            complement_resolvent,
            coupling_norm,
            coupling_norm,
        )
        for trial in range(trials):
            perturbation = scaled_random(rng, (packet_dimension, packet_dimension), packet_perturbation)
            left = scaled_random(rng, (packet_dimension, complement_dimension), coupling_norm)
            right = scaled_random(rng, (complement_dimension, packet_dimension), coupling_norm)
            full = np.block([[seed + perturbation, left], [right, complement]])
            eigenvalues = np.linalg.eigvals(full)
            counts = [int(np.sum(np.abs(eigenvalues - root) < contour_radius)) for root in roots]
            records.append({
                "length": length,
                "trial": trial,
                "shell_count": len(roots),
                "minimum_enclosed_rank": min(counts),
                "maximum_enclosed_rank": max(counts),
                "all_shell_ranks_two": all(count == 2 for count in counts),
                "directed_schur_product": budget["directed_schur_product"],
                "certificate_admissible": budget["certificate_admissible"],
            })
    return {
        "status": "rh180_cyclic_cloud_riesz_shell_audit",
        "matrix_case_count": len(records),
        "shell_case_count": sum(record["shell_count"] for record in records),
        "rank_failure_count": sum(not record["all_shell_ranks_two"] for record in records),
        "certificate_failure_count": sum(not record["certificate_admissible"] for record in records),
        "maximum_directed_schur_product": max(record["directed_schur_product"] for record in records),
        "records": records,
        "theorem_boundary": {
            "explicit_normal_cycle_contour_geometry": True,
            "conditional_same_rank_riesz_shell_theorem": True,
            "finite_random_formula_audit": True,
            "physical_transfer_operator_budget": False,
            "all_level_shell_transport": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "cycle_riesz_smoke.json" if args.smoke else "cycle_riesz_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "matrix_cases": payload["matrix_case_count"], "shell_cases": payload["shell_case_count"], "rank_failures": payload["rank_failure_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
