"""Aggregate RH-212--RH-220 into one strict frontier ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from shape_review import review_coordinate, strict_gate_vector  # noqa: E402


PATHS = {
    212: ("RH-212-intrinsic-quartic-normalization-audit", "intrinsic_normalization_audit.json"),
    213: ("RH-213-centered-conjugate-quartet-shape-manifold", "shape_manifold_audit.json"),
    214: ("RH-214-monotone-axial-shape-clock", "shape_clock_audit.json"),
    215: ("RH-215-out-of-sample-shape-clock-prediction", "prediction_audit.json"),
    216: ("RH-216-degenerate-quartet-boundary-stratification", "boundary_audit.json"),
    217: ("RH-217-transverse-shape-quenching", "transverse_quenching_audit.json"),
    218: ("RH-218-autonomous-shape-recurrence-obstruction", "recurrence_audit.json"),
    219: ("RH-219-fixed-quartic-counting-obstruction", "counting_obstruction_audit.json"),
    220: ("RH-220-gauge-complete-divisor-reconstruction", "gauge_reconstruction_audit.json"),
}


def load() -> dict[int, dict[str, object]]:
    return {
        number: json.loads((PAPERS / directory / "results" / filename).read_text(encoding="utf-8"))
        for number, (directory, filename) in PATHS.items()
    }


def run() -> dict[str, object]:
    papers = load()
    p212, p213, p214, p215, p216, p217, p218, p219, p220 = (papers[number] for number in range(212, 221))
    statuses = {
        "normalization_negative": not p212["theorem_boundary"]["natural_normalization_contraction"],
        "shape_manifold_exact": p213["theorem_boundary"]["shape_parameterization_exact"],
        "finite_clock_positive": p214["all_u_transitions_strictly_positive"],
        "prediction_law_open": not p215["theorem_boundary"]["asymptotic_law_identified"],
        "boundary_theorem_exact": p216["theorem_boundary"]["discriminant_factorization_exact"],
        "transverse_quenching_exact": p217["theorem_boundary"]["transverse_lipschitz_quenching_exact"],
        "recurrence_identification_negative": not p218["theorem_boundary"]["scale_independent_semigroup_identified"],
        "fixed_degree_counting_negative": p219["theorem_boundary"]["growing_divisor_required_for_spectral_count"],
        "gauge_completion_exact": p220["theorem_boundary"]["affine_gauge_reconstruction_exact"],
        "rank_growing_divisor_constructed": False,
    }
    counts = {
        212: len(p212["endpoint_rows"]) + len(p212["adjacent_rows"]) + len(p212["channel_rows"]),
        213: len(p213["shape_rows"]) + len(p213["identity_rows"]),
        214: len(p214["transition_rows"]),
        215: len(p215["channel_rows"]) + sum(len(row["model_rows"]) for row in p215["channel_rows"]),
        216: len(p216["endpoint_rows"]) + len(p216["identity_rows"]),
        217: len(p217["sensitivity_rows"]) + len(p217["channel_decomposition_rows"]) + p217["random_bound_case_count"],
        218: len(p218["channel_rows"]) + sum(len(row["scalar_rows"]) for row in p218["channel_rows"]),
        219: len(p219["repeated_divisor_rows"]) + len(p219["normalized_power_rows"]) + len(p219["growing_cloud_contrast_rows"]),
        220: len(p220["endpoint_rows"]) + len(p220["transition_rows"]) + len(p220["channel_rows"]),
    }
    paper_rows = [
        {"paper": "RH-212", "result": "two natural normalizations do not contract", "status": "finite negative"},
        {"paper": "RH-213", "result": "exact two-coordinate conjugate-quartet manifold", "status": "exact theorem"},
        {"paper": "RH-214", "result": "sixteen-level monotone axial clock and narrow mature corridor", "status": "finite positive"},
        {"paper": "RH-215", "result": "power-gap wins two holdouts but no asymptotic law", "status": "finite mixed"},
        {"paper": "RH-216", "result": "discriminant stratification and uniform boundary collapse", "status": "exact theorem"},
        {"paper": "RH-217", "result": "transverse coefficient sensitivity quenches as u approaches one", "status": "exact theorem"},
        {"paper": "RH-218", "result": "simple autonomous maps fail holdout; finite interpolation is non-identifying", "status": "exact + finite negative"},
        {"paper": "RH-219", "result": "fixed or repeated quartic cannot supply a locally finite growing spectrum", "status": "exact obstruction"},
        {"paper": "RH-220", "result": "center-radius-shape data reconstruct every raw divisor", "status": "exact + route decision"},
    ]
    gates = strict_gate_vector()
    return {
        "status": "rh221_ten_layer_quartet_shape_frontier_review",
        "route_coordinate": review_coordinate(statuses),
        "statuses": statuses,
        "strict_gate_vector": gates,
        "paper_rows": paper_rows,
        "paper_ledger_counts": {str(key): value for key, value in counts.items()},
        "aggregate_finite_ledger_item_count": sum(counts.values()),
        "aggregate_identity_failure_count": int(
            p213["maximum_random_coefficient_error"] > 1.0e-10
            or p216["maximum_random_discriminant_relative_error"] > 1.0e-10
            or p217["maximum_random_bound_violation"] > 1.0e-12
            or p220["maximum_coefficient_reconstruction_error"] > 1.0e-10
        ),
        "headline_metrics": {
            "raw_normalization_adjacent_mean": p212["normalization_summary"]["raw"]["adjacent_fine_relative_error_mean"],
            "centered_normalization_adjacent_mean": p212["normalization_summary"]["centered_rms"]["adjacent_fine_relative_error_mean"],
            "shape_manifold_residual": p213["maximum_endpoint_manifold_residual"],
            "all_u_transitions_positive": p214["all_u_transitions_strictly_positive"],
            "mature_left_eta_width": p214["channel_summaries"]["left"]["mature_eta_corridor_sigma_at_most_0_02"]["width"],
            "power_gap_two_holdout_winner_both_channels": p215["same_winner_both_channels"],
            "boundary_bound_violation": p216["maximum_uniform_bound_violation"],
            "finest_transverse_to_axial_ratio": p217["finest_maximum_transverse_ratio"],
            "pooled_affine_holdout_error": p218["pooled_affine_holdout_metrics"]["maximum_error"],
            "maximum_repeated_degree": p219["maximum_repeated_degree"],
            "maximum_repeated_support": p219["maximum_repeated_distinct_support"],
            "gauge_reconstruction_error": p220["maximum_coefficient_reconstruction_error"],
        },
        "theorem_boundary": {
            "finite_quartet_shape_atlas": True,
            "gauge_complete_reconstruction": True,
            "rank_growing_divisor": False,
            "locally_uniform_determinant": False,
            **gates,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/shape_frontier_review.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "ledger_items": payload["aggregate_finite_ledger_item_count"],
        "identity_failures": payload["aggregate_identity_failure_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
