"""Assemble the RH-232--RH-240 theorem and reproducibility ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from trace_review import macro_gates, route_coordinate  # noqa: E402


SOURCES = {
    232: ("RH-232-biorthogonal-riesz-cloud-projection", "riesz_projection_audit.json"),
    233: ("RH-233-radial-gap-pseudospectral-barrier", "pseudospectral_gap_audit.json"),
    234: ("RH-234-projection-free-det2-spectral-factor", "spectral_factor_audit.json"),
    235: ("RH-235-trace-vs-hilbert-schmidt-separation", "trace_hs_separation_audit.json"),
    236: ("RH-236-cloud-extracted-trace-moment-atlas", "trace_moment_atlas.json"),
    237: ("RH-237-dual-channel-trace-jet-coherence", "trace_jet_coherence.json"),
    238: ("RH-238-trace-adaptive-shell-selection", "adaptive_shell_selection.json"),
    239: ("RH-239-adaptive-jet-contraction-obstruction", "adaptive_jet_contraction.json"),
    240: ("RH-240-uniform-trace-envelope-criterion", "trace_envelope_audit.json"),
}


def load_sources() -> dict[int, dict[str, object]]:
    return {
        number: json.loads((PAPERS / directory / "results" / filename).read_text(encoding="utf-8"))
        for number, (directory, filename) in SOURCES.items()
    }


def run() -> dict[str, object]:
    source = load_sources()
    statuses = {
        "riesz_wall_identified": source[232]["maximum_projector_operator_norm"] > 1.0e8,
        "radial_gap_insufficient": source[233]["theorem_boundary"][
            "fixed_eigenvalue_gap_does_not_bound_projector_norm"
        ],
        "projection_free_factor": source[234]["maximum_grid_factorization_error"] < 1.0e-10,
        "trace_hs_separation": source[235]["theorem_boundary"][
            "divergent_hilbert_schmidt_norm_can_coexist_with_trivial_det2"
        ],
        "trace_moment_atlas": source[236]["trace_case_count"] == 384,
        "dual_channel_jet_coherence": source[237]["unit_disk_gate_pass_count"] == 16,
        "adaptive_selector": source[238]["all_endpoints_pass"],
        "finite_jet_contraction_bound": source[239]["minimum_adjacent_bound_slack"] >= 0.0,
        "trace_envelope_criterion": source[240]["theorem_boundary"][
            "all_order_geometric_trace_envelope_implies_normal_relative_det2"
        ],
        "all_order_trace_envelope": source[240]["theorem_boundary"][
            "order_thirteen_and_above_controlled"
        ],
        "coefficient_anchor": False,
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
    }
    finite_ledger_items = (
        source[232]["endpoint_count"]
        + source[233]["endpoint_count"] + len(source[233]["fixed_gap_model_rows"])
        + source[234]["factorization_case_count"]
        + source[235]["endpoint_count"] + len(source[235]["nilpotent_model_rows"])
        + source[236]["trace_case_count"]
        + source[237]["channel_radius_case_count"]
        + source[238]["total_evaluated_prefix_count"]
        + source[239]["adjacent_case_count"] + source[239]["channel_case_count"]
        + source[240]["observed_order_count"]
    )
    identity_failures = sum((
        source[234]["maximum_grid_factorization_error"] >= 1.0e-10,
        source[237]["unit_disk_gate_pass_count"] != source[237]["channel_case_count"],
        not source[238]["all_endpoints_pass"],
        source[239]["minimum_adjacent_bound_slack"] < -1.0e-12,
        source[239]["minimum_channel_bound_slack"] < -1.0e-12,
        source[240]["global_observed_unit_amplitude_rate"] >= 1.0,
    ))
    return {
        "status": "rh241_ten_layer_trace_envelope_frontier_review",
        "paper_numbers": list(SOURCES),
        "route_coordinate": route_coordinate(statuses),
        "statuses": statuses,
        "macro_gates": macro_gates(statuses),
        "finite_ledger_items": int(finite_ledger_items),
        "identity_failure_count": int(identity_failures),
        "headline_metrics": {
            "projector_norm_range": [
                source[232]["minimum_projector_operator_norm"],
                source[232]["maximum_projector_operator_norm"],
            ],
            "minimum_gap_to_projector_norm_ratio": source[233][
                "minimum_gap_to_projector_norm_ratio"
            ],
            "maximum_projection_free_factorization_error": source[234][
                "maximum_grid_factorization_error"
            ],
            "maximum_trace_square_modulus": source[235][
                "maximum_complement_trace_square_modulus"
            ],
            "maximum_hs_squared_upper": source[235][
                "maximum_complement_hilbert_schmidt_squared_upper"
            ],
            "trace_order_range": [2, source[236]["maximum_order"]],
            "maximum_fine_trace_jet_norm": source[236][
                "maximum_fine_unit_disk_log_jet_norm"
            ],
            "maximum_channel_trace_jet_distance": source[237][
                "maximum_unit_disk_trace_jet_distance"
            ],
            "adaptive_rank_range": [
                source[238]["minimum_adaptive_rank"], source[238]["maximum_adaptive_rank"]
            ],
            "observed_envelope_rates": [
                source[240]["global_observed_unit_amplitude_rate"],
                source[240]["fine_observed_unit_amplitude_rate"],
            ],
        },
        "next_target": "all_order_cloud_extracted_periodic_trace_envelope_with_coefficient_anchor",
        "theorem_boundary": {
            "direct_uniform_riesz_projector_route_supported": False,
            "projection_free_finite_spectral_factor_complete": True,
            "finite_order_trace_route_supported": True,
            "uniform_all_order_trace_envelope": False,
            "coefficient_anchor_to_deterministic_numerator": False,
            "gate_A": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/trace_envelope_frontier_review.json"
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
