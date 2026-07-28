"""Assemble the RH-222--RH-230 theorem and reproducibility ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from determinant_review import macro_gates, route_coordinate  # noqa: E402


SOURCES = {
    222: ("RH-222-rank-growing-conjugate-cloud-atlas", "cloud_atlas.json"),
    223: ("RH-223-shell-complete-edge-selection-stability", "shell_stability_audit.json"),
    224: ("RH-224-global-cloud-gauge-tightness", "tightness_audit.json"),
    225: ("RH-225-tight-cloud-local-finiteness-obstruction", "divisor_obstruction_audit.json"),
    226: ("RH-226-reciprocal-resonance-fredholm-dictionary", "fredholm_dictionary_audit.json"),
    227: ("RH-227-reciprocal-local-count-small-noise-gate", "local_count_gate.json"),
    228: ("RH-228-resolved-det2-omitted-shell-control", "resolved_tail_audit.json"),
    229: ("RH-229-nonnormal-frobenius-tail-budget-barrier", "frobenius_tail_audit.json"),
    230: ("RH-230-dual-channel-det2-coherence-noncontraction", "det2_coherence_audit.json"),
}


def load_sources() -> dict[int, dict[str, object]]:
    return {
        number: json.loads((PAPERS / directory / "results" / filename).read_text(encoding="utf-8"))
        for number, (directory, filename) in SOURCES.items()
    }


def run() -> dict[str, object]:
    source = load_sources()
    statuses = {
        "rank_growing_cloud": source[222]["maximum_actual_rank"] >= 34,
        "shell_complete_selection": source[223]["all_margin_prefixes_recover_reference"],
        "empirical_tightness": source[224]["theorem_boundary"]["uniform_empirical_tightness"],
        "direct_divisor_rejected": source[225]["theorem_boundary"]["direct_normalized_cloud_route_rejected"],
        "reciprocal_dictionary": source[226]["theorem_boundary"]["finite_reciprocal_polynomial_identity"],
        "local_count_stability": source[227]["all_channel_radius_counts_stable_in_frozen_tail"],
        "resolved_tail_control": source[228]["minimum_bound_slack"] >= 0.0,
        "uniform_complement_ideal_control": source[229]["small_tail_gate_pass_count"] == source[229]["endpoint_count"],
        "dual_channel_coherence": source[230]["all_channels_pass"],
        "cross_scale_contraction": source[230]["both_channels_strictly_contract_on_last_four_transitions"],
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
    }
    finite_ledger_items = (
        source[222]["endpoint_count"]
        + source[223]["endpoint_count"] * (1 + len(source[223]["prefix_margins"]))
        + source[224]["endpoint_count"] * (1 + len(source[224]["tail_radii"]))
        + source[225]["endpoint_count"]
        + source[226]["endpoint_count"] * source[226]["grid_point_count"]
        + source[227]["endpoint_count"] * len(source[227]["radii"])
        + source[228]["endpoint_count"] * source[228]["grid_point_count"]
        + source[229]["endpoint_count"]
        + source[230]["channel_case_count"]
        + source[230]["adjacent_case_count"]
    )
    identity_failures = sum((
        source[222]["maximum_conjugacy_error"] >= 1.0e-7,
        source[223]["maximum_margin_matching_error"] >= 1.0e-12,
        source[224]["maximum_second_moment_error"] >= 1.0e-12,
        source[224]["minimum_tail_bound_slack"] < -1.0e-12,
        source[226]["maximum_reciprocal_polynomial_identity_error"] >= 1.0e-10,
        source[228]["minimum_bound_slack"] < -1.0e-12,
    ))
    return {
        "status": "rh231_ten_layer_rank_growing_determinant_frontier_review",
        "paper_numbers": list(SOURCES),
        "route_coordinate": route_coordinate(statuses),
        "statuses": statuses,
        "macro_gates": macro_gates(statuses),
        "finite_ledger_items": int(finite_ledger_items),
        "identity_failure_count": int(identity_failures),
        "headline_metrics": {
            "rank_range": [source[222]["minimum_actual_rank"], source[222]["maximum_actual_rank"]],
            "naive_split_pair_count": source[223]["naive_split_pair_count"],
            "maximum_normalized_modulus": source[224]["maximum_normalized_modulus"],
            "direct_compact_mass_growth": [row["normalized_compact_mass_growth"] for row in source[225]["channel_rows"]],
            "reciprocal_modulus_range": [source[226]["minimum_reciprocal_modulus"], source[226]["maximum_reciprocal_modulus"]],
            "maximum_reciprocal_count_growth": source[227]["maximum_first_to_last_count_growth"],
            "maximum_resolved_log_tail_upper": source[228]["maximum_log_tail_upper"],
            "full_frobenius_log_tail_range": [source[229]["minimum_full_frobenius_log_tail_upper"], source[229]["maximum_full_frobenius_log_tail_upper"]],
            "maximum_channel_det2_log_difference": source[230]["maximum_channel_log_difference"],
            "adjacent_det2_log_difference_range": [source[230]["minimum_adjacent_log_difference"], source[230]["maximum_adjacent_log_difference"]],
        },
        "next_target": "moving_cloud_relative_det2_with_uniform_complement_ideal_control",
        "theorem_boundary": {
            "rank_growing_finite_atlas_complete": True,
            "fixed_noise_det2_reconnected": True,
            "direct_tight_divisor_route_rejected": True,
            "uniform_small_noise_relative_det2": False,
            "dynamical_limit": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/determinant_frontier_review.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "ledger_items": payload["finite_ledger_items"],
        "identity_failures": payload["identity_failure_count"],
        "next_target": payload["next_target"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
