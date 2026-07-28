"""Assemble the RH-242--RH-251 ten-layer frontier review."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from superloop_review import macro_gates, route_coordinate  # noqa: E402


SOURCES = {
    242: ("RH-242-cloud-extracted-periodic-superloop-representation", "periodic_superloop_audit.json"),
    243: ("RH-243-deterministic-numerator-coefficient-anchor-dictionary", "coefficient_anchor_audit.json"),
    244: ("RH-244-anchored-shell-prefix-availability-obstruction", "anchored_prefix_audit.json"),
    245: ("RH-245-orthogonal-quotient-superloop-compression", "orthogonal_quotient_audit.json"),
    246: ("RH-246-block-power-quotient-envelope-criterion", "block_power_audit.json"),
    247: ("RH-247-separate-absolute-majorant-barrier", "absolute_majorant_audit.json"),
    248: ("RH-248-anchored-shell-zonotope-reachability-obstruction", "zonotope_audit.json"),
    249: ("RH-249-unbounded-shell-multiplicity-pathology", "cone_reachability_audit.json"),
    250: ("RH-250-anchored-head-analytic-tail-gluing-criterion", "head_tail_audit.json"),
}


def load_sources() -> dict[int, dict[str, object]]:
    return {
        number: json.loads((PAPERS / directory / "results" / filename).read_text(encoding="utf-8"))
        for number, (directory, filename) in SOURCES.items()
    }


def run() -> dict[str, object]:
    source = load_sources()
    statuses = {
        "exact_periodic_superloop_identity": source[242]["maximum_supertrace_identity_error"] < 1.0e-10,
        "deterministic_anchor_dictionary_defined": source[243]["theorem_boundary"][
            "deterministic_one_step_trace_style_anchor_target_defined"
        ],
        "frozen_prefix_anchor_available": source[244]["anchored_selection_pass_count"] > 0,
        "orthogonal_quotient_identity": source[245]["rank_mismatch_count"] == 0
        and source[245]["maximum_archived_residual_error_orders_2_to_12"] < 1.0e-9,
        "block_power_criterion": source[246]["theorem_boundary"]["block_power_trace_envelope_criterion"],
        "uniform_block_constants": source[246]["theorem_boundary"]["uniform_noise_block_constants"],
        "separate_absolute_route_survives": source[247]["theorem_boundary"][
            "absolute_majorant_can_prove_subunit_envelope"
        ],
        "frozen_shell_zonotope_anchor_available": source[248]["box_zonotope_pass_count"] > 0,
        "unbounded_cone_is_legal_cloud": source[249]["theorem_boundary"][
            "unbounded_real_weights_are_legal_spectral_multiplicities"
        ],
        "complete_gluing_certificate": source[250]["complete_gluing_certificate_count"] > 0,
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
    }
    paper_rows = [
        {"number": 242, "layer": "periodic-loop realization", "claim_level": "exact fixed-noise identity", "blocker": "uniform all-order envelope and anchor"},
        {"number": 243, "layer": "deterministic numerator anchor", "claim_level": "exact finite coefficient dictionary", "blocker": "current cloud coefficient bridge"},
        {"number": 244, "layer": "anchored prefix availability", "claim_level": "scoped finite obstruction", "blocker": "prefix class misses anchor"},
        {"number": 245, "layer": "orthogonal quotient grouping", "claim_level": "exact fixed-operator quotient identity", "blocker": "uniform selected-space stability"},
        {"number": 246, "layer": "block-power envelope", "claim_level": "exact conditional criterion plus finite diagnostic", "blocker": "uniform block constants"},
        {"number": 247, "layer": "separate absolute majorant", "claim_level": "exact scoped barrier", "blocker": "must preserve cancellation"},
        {"number": 248, "layer": "single-use shell zonotope", "claim_level": "dual-certified finite obstruction", "blocker": "expanded or signed selector"},
        {"number": 249, "layer": "unbounded shell weights", "claim_level": "cone obstruction and multiplicity pathology", "blocker": "legal spectral multiplicity"},
        {"number": 250, "layer": "head/tail gluing", "claim_level": "exact determinant interface and route stop", "blocker": "anchored head and target tail"},
        {"number": 251, "layer": "frontier review", "claim_level": "ten-layer synthesis", "blocker": "Gate-A closure remains open"},
    ]
    finite_ledger_items = (
        source[242]["enumerated_closed_loop_count"]
        + source[242]["archived_determinant_relevant_trace_case_count"]
        + len(source[243]["coefficient_rows"])
        + source[243]["endpoint_count"]
        + source[244]["total_evaluated_prefix_count"]
        + source[245]["eligible_endpoint_count"] * source[245]["maximum_order"]
        + source[246]["source_endpoint_count"]
        + source[247]["case_count"]
        + source[248]["endpoint_count"]
        + source[249]["endpoint_count"]
        + source[250]["head_endpoint_count"]
    )
    audit_failures = sum((
        not statuses["exact_periodic_superloop_identity"],
        not statuses["deterministic_anchor_dictionary_defined"],
        source[245]["rank_mismatch_count"] != 0,
        source[248]["maximum_box_primal_dual_gap"] >= 1.0e-9,
        source[249]["maximum_cone_primal_dual_gap"] >= 1.0e-4,
        source[250]["complete_gluing_certificate_count"] != 0,
    ))
    return {
        "status": "rh251_ten_layer_superloop_anchor_frontier_review",
        "paper_numbers": list(range(242, 252)),
        "route_coordinate": route_coordinate(statuses),
        "statuses": statuses,
        "macro_gates": macro_gates(statuses),
        "paper_rows": paper_rows,
        "finite_ledger_items": int(finite_ledger_items),
        "audit_failure_count": int(audit_failures),
        "headline_metrics": {
            "rh242_loop_count": source[242]["enumerated_closed_loop_count"],
            "rh242_trace_residual_count": source[242]["archived_determinant_relevant_trace_case_count"],
            "rh243_anchor_norm": source[243]["one_step_target_unit_disk_log_jet_norm_orders_2_to_12"],
            "rh244_prefix_passes": source[244]["anchored_selection_pass_count"],
            "rh245_quotient_endpoints": source[245]["eligible_endpoint_count"],
            "rh246_q12": source[246]["finite_sample_geometric_rate_q12"],
            "rh247_absolute_root_rate_range": [source[247]["minimum_case_root_rate"], source[247]["maximum_case_root_rate"]],
            "rh248_box_distance_range": [source[248]["minimum_box_distance"], source[248]["maximum_box_distance"]],
            "rh249_cone_passes_failures": [source[249]["cone_pass_count"], source[249]["cone_failure_count"]],
            "rh250_complete_gluing_certificates": source[250]["complete_gluing_certificate_count"],
        },
        "next_target": "new_anchored_selector_outside_frozen_resolved_window_with_uniform_quotient_block_certificate_and_target_tail",
        "theorem_boundary": {
            "exact_superloop_and_orthogonal_quotient_progress": True,
            "finite_anchor_target_defined": True,
            "frozen_single_use_anchor_class_obstructed": True,
            "uniform_all_order_trace_envelope": False,
            "coefficient_anchor_to_current_cloud": False,
            "locally_uniform_relative_det2_family": False,
            "gate_A": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/frontier_review.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "ledger_items": payload["finite_ledger_items"],
        "audit_failures": payload["audit_failure_count"],
        "next_target": payload["next_target"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
