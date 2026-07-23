"""Build the RH-110--RH-119 theorem ledger and proof-frontier audit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from route_review import each_addition_reaches, minimal_missing_sets, proof_closure  # noqa: E402


FULL_OUTPUT = ROOT / "results" / "ten_layer_review_audit.json"
SMOKE_OUTPUT = ROOT / "results" / "ten_layer_review_smoke.json"
PAPER_DIRECTORIES = {
    110: "RH-110-finite-memory-three-mode-capacity",
    111: "RH-111-tail-energy-exterior-concentration",
    112: "RH-112-global-wedge-lipschitz-barrier",
    113: "RH-113-right-frame-directional-wedge",
    114: "RH-114-psd-rayleigh-directional-tail",
    115: "RH-115-composite-directional-support-gate",
    116: "RH-116-monotone-memory-depth-optimization",
    117: "RH-117-finite-anchor-scale-law-barrier",
    118: "RH-118-conditional-composite-exterior-route",
}


def load_summary(number: int) -> dict[str, object]:
    path = PAPERS / PAPER_DIRECTORIES[number] / "results" / "summary.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    summaries = {number: load_summary(number) for number in PAPER_DIRECTORIES}

    layers = [
        {"number": 110, "category": "constructive", "headline": "capacity factorization and finite-memory enclosure", "route_status": "open physical continuation"},
        {"number": 111, "category": "constructive", "headline": "trace--concentration exterior certificate", "route_status": "open physical continuation"},
        {"number": 112, "category": "negative", "headline": "sharp global wedge-Lipschitz barrier", "route_status": "global norm-only improvement closed"},
        {"number": 113, "category": "constructive", "headline": "right-frame directional exterior action", "route_status": "directional route retained"},
        {"number": 114, "category": "constructive", "headline": "PSD Rayleigh tail comparison", "route_status": "directional gamma law open"},
        {"number": 115, "category": "constructive", "headline": "composite gate and outward admission", "route_status": "unguarded cross-assembly fusion closed"},
        {"number": 116, "category": "constructive", "headline": "monotone cost-optimal memory depth", "route_status": "all-level bounded depth open"},
        {"number": 117, "category": "negative", "headline": "finite-anchor asymptotic nonidentifiability", "route_status": "finite-anchor extrapolation closed"},
        {"number": 118, "category": "synthesis", "headline": "conditional composite liminf theorem", "route_status": "three physical packets open"},
        {"number": 119, "category": "synthesis", "headline": "proof-frontier audit and revised roadmap", "route_status": "current review"},
    ]
    reported_layers = layers[:3] if args.smoke else layers

    theorem_checks = {
        "rh110_capacity_factorization": bool(summaries[110]["theorem"]["capacity_aware_volume_recovery"]),
        "rh111_trace_concentration": bool(summaries[111]["theorem"]["refined_trace_exterior_certificate"]),
        "rh112_global_negative": bool(summaries[112]["theorem"]["global_route_declared_negative"]),
        "rh113_directional_frame": bool(summaries[113]["theorem"]["directional_frame_variational_certificate"]),
        "rh114_relative_rayleigh": bool(summaries[114]["theorem"]["relative_psd_rayleigh_volume_bound"]),
        "rh115_composite_gate": bool(summaries[115]["theorem"]["monotone_composite_gate"]),
        "rh116_depth_first_passage": bool(summaries[116]["theorem"]["first_passage_depth_is_cost_minimal"]),
        "rh117_anchor_barrier": bool(summaries[117]["theorem"]["finite_anchor_asymptotic_nonidentifiability"]),
        "rh118_liminf_gate": bool(summaries[118]["theorem"]["conditional_composite_liminf_theorem"]),
    }
    proved_nodes = {
        "factor_identity",
        "capacity_gate",
        "trace_identity",
        "trace_conversion",
        "directional_factor",
        "monotone_maximum",
        "nested_depth_first_passage",
        "conditional_liminf_theorem",
        "outward_degradation_rule",
        "finite_archive_support",
        "finite_anchor_nonidentifiability",
    }
    rules = {
        "eventual_fourth_mode_support": [
            ("conditional_liminf_theorem", "direct_margin_packet"),
            ("conditional_liminf_theorem", "trace_concentration_packet"),
            ("conditional_liminf_theorem", "directional_rayleigh_packet"),
        ],
        "validated_eventual_fourth_mode_support": [
            ("eventual_fourth_mode_support", "all_level_outward_admissibility")
        ],
    }
    physical_packets = (
        "direct_margin_packet",
        "trace_concentration_packet",
        "directional_rayleigh_packet",
    )
    reached = proof_closure(proved_nodes, rules)
    mathematical_frontier = minimal_missing_sets("eventual_fourth_mode_support", proved_nodes, rules)
    validated_frontier = minimal_missing_sets("validated_eventual_fourth_mode_support", proved_nodes, rules)
    addition_audit = each_addition_reaches(
        "eventual_fourth_mode_support", proved_nodes, rules, physical_packets
    )

    closed_routes = [
        {
            "route": "global norm-only wedge perturbation as an improvement",
            "reason": "sharply dominated by product Weyl",
            "source": "RH-112",
        },
        {
            "route": "arbitrary fixed-frame universal positive capture",
            "reason": "exact blindness example",
            "source": "RH-113",
        },
        {
            "route": "unguarded fusion of independently rounded Gram assemblies",
            "reason": "outward-admissibility failure on one weak record",
            "source": "RH-115",
        },
        {
            "route": "finite-anchor fitting as an all-level proof",
            "reason": "bounded smooth continuations have incompatible limits",
            "source": "RH-117",
        },
    ]
    physical_frontier = [
        {
            "packet": "direct_margin_packet",
            "primitive_count": 1,
            "research_priority": 2,
            "comment": "logically shortest, but close to restating the desired support margin",
        },
        {
            "packet": "directional_rayleigh_packet",
            "primitive_count": 3,
            "research_priority": 1,
            "comment": "best structural route; PSD tail geometry and finite directional gains are available",
        },
        {
            "packet": "trace_concentration_packet",
            "primitive_count": 3,
            "research_priority": 3,
            "comment": "rigorous but currently never wins the finite composite maximum",
        },
    ]
    rh118_audit = summaries[118]["audit"]
    summary = {
        "layer_count": len(reported_layers),
        "upstream_archive_count": len(summaries),
        "constructive_layer_count": sum(layer["category"] == "constructive" for layer in reported_layers),
        "negative_layer_count": sum(layer["category"] == "negative" for layer in reported_layers),
        "synthesis_layer_count": sum(layer["category"] == "synthesis" for layer in reported_layers),
        "theorem_check_failure_count": sum(not value for value in theorem_checks.values()),
        "closed_route_count": len(closed_routes),
        "frontier_packet_count": len(physical_packets),
        "proved_frontier_packet_count": 0,
        "mathematical_minimal_frontier_count": len(mathematical_frontier),
        "validated_minimal_frontier_count": len(validated_frontier),
        "eventual_support_reachable": "eventual_fourth_mode_support" in reached,
        "finite_archive_support_reachable": "finite_archive_support" in reached,
        "each_physical_packet_individually_completes_conditional_graph": all(addition_audit.values()),
        "finite_actual_support_count": int(rh118_audit["actual_support_count"]),
        "finite_adaptive_support_count": int(rh118_audit["adaptive_support_count"]),
    }
    payload = {
        "status": "rh119_ten_layer_exterior_route_review_audit",
        "layers": reported_layers,
        "theorem_checks": theorem_checks,
        "factor_ledger": {
            "core_identity": "q4 = nu4 / Lambda23",
            "definitions": ["nu4 = q2*q3*q4", "Lambda23 = q2*q3"],
            "trace_variant": "nu4^2 = Theta4 / kappa4",
            "directional_variant": "nu4 >= (1-gamma_upper)^4 * frame_volume_lower",
            "composite_rule": "maximum of outward-admitted lower bounds",
        },
        "closed_routes": closed_routes,
        "numerical_interface_barriers": [
            {
                "barrier": "cross-assembly near-cancellation",
                "required_rule": "same enclosed operator or explicit outward transport loss",
                "finite_resolution": "RH-116 one-path assembly",
                "all_level_status": "open when independent paths are used",
            }
        ],
        "proof_graph": {
            "proved_nodes": sorted(proved_nodes),
            "rules": {output: [list(inputs) for inputs in alternatives] for output, alternatives in rules.items()},
            "reached_nodes": sorted(reached),
            "mathematical_minimal_missing_sets": [sorted(values) for values in mathematical_frontier],
            "validated_minimal_missing_sets": [sorted(values) for values in validated_frontier],
            "single_packet_addition_audit": addition_audit,
        },
        "physical_frontier": physical_frontier,
        "audit_summary": summary,
        "theorem_boundary": {
            "ten_layer_factor_ledger_verified": all(theorem_checks.values()),
            "proof_frontier_antichain_identified": True,
            "finite_archive_support_complete": int(rh118_audit["actual_support_count"])
            == int(rh118_audit["adaptive_support_count"]),
            "eventual_fourth_mode_support_proved": False,
            "all_level_outward_admissibility_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "zeta_zero_identification": False,
            "riemann_hypothesis": False,
        },
        "revised_roadmap": [
            "First attack a cross-level directional-Rayleigh transfer inequality for frame volume and relative gamma.",
            "Use one assembly path or validated outward transport from the outset.",
            "In parallel, seek a direct-margin recurrence as the logically shortest fallback.",
            "Defer trace-concentration unless an independent physical exterior-trace source law appears.",
            "Do not advance to Hilbert--Polya or zero claims before one all-level support packet is actually proved.",
        ],
        "route_consequence": (
            "The ten-layer route has a verified exact factor ledger, six constructive layers, two rigorous route-closing layers, and two synthesis layers. Four tempting branches are explicitly closed. The current proof graph reaches complete finite support but not eventual all-level support. Its inclusion-minimal mathematical frontier is the three-way antichain consisting of direct margin, trace-concentration, and directional-Rayleigh packets; adding any one packet completes the conditional graph, while validated numerical closure also needs all-level outward admissibility."
        ),
        "limitations": [
            "This is a proof-dependency review, not a proof of any missing physical packet.",
            "Finite audit completeness has no edge to eventual support because RH-117 proves the finite-anchor barrier.",
            "No Hilbert--Polya operator, zeta-zero identification, or Riemann Hypothesis conclusion is claimed.",
        ],
    }
    output = SMOKE_OUTPUT if args.smoke else FULL_OUTPUT
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
