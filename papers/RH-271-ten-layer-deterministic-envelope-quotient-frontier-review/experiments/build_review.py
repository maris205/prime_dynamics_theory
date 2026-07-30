"""Assemble the RH-262--RH-271 deterministic-envelope frontier review."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from frontier_review import (  # noqa: E402
    macro_gates,
    obligation_summary,
    root_of_unity_shell_trace,
    route_coordinate,
)


SOURCES = {
    262: ("RH-262-certified-deterministic-numerator-boundary-budget", "certified_boundary_budget.json"),
    263: ("RH-263-parity-resolved-deterministic-numerator-tail", "parity_anchor_audit.json"),
    264: ("RH-264-direct-factorwise-deterministic-tail-certificate", "direct_tail_audit.json"),
    265: ("RH-265-certified-deterministic-tail-ladder", "tail_ladder.json"),
    266: ("RH-266-finite-sample-quotient-uniformity-obstruction", "uniformity_obstruction.json"),
    267: ("RH-267-certified-unified-deterministic-trace-envelope", "coefficient_envelope.json"),
    268: ("RH-268-sharp-deterministic-coefficient-radius-law", "sharp_coefficient_law.json"),
    269: ("RH-269-contour-stable-uniform-quotient-criterion", "criterion_audit.json"),
    270: ("RH-270-updated-deterministic-envelope-quotient-certificate-ledger", "updated_certificate_ledger.json"),
}


EXPECTED_STATUS = {
    262: "rh262_certified_deterministic_numerator_boundary_budget",
    263: "rh263_parity_resolved_deterministic_numerator_tail",
    264: "rh264_direct_factorwise_deterministic_tail_certificate",
    265: "rh265_certified_deterministic_tail_ladder",
    266: "rh266_finite_sample_quotient_uniformity_obstruction",
    267: "rh267_certified_unified_deterministic_trace_envelope",
    268: "rh268_sharp_deterministic_coefficient_radius_law",
    269: "rh269_contour_stable_uniform_quotient_criterion",
    270: "rh270_updated_deterministic_envelope_quotient_certificate_ledger",
}


def load_sources() -> dict[int, dict[str, object]]:
    return {
        number: json.loads(
            (PAPERS / directory / "results" / filename).read_text(encoding="utf-8")
        )
        for number, (directory, filename) in SOURCES.items()
    }


def run() -> dict[str, object]:
    source = load_sources()
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})

    for number, payload in source.items():
        check(f"rh{number}_status", payload["status"] == EXPECTED_STATUS[number])
        boundary = payload["theorem_boundary"]
        for letter in "ABCDE":
            check(f"rh{number}_gate_{letter}_open", boundary[f"gate_{letter}"] is False)
        check(
            f"rh{number}_hilbert_polya_not_claimed",
            boundary["hilbert_polya_operator"] is False,
        )
        check(
            f"rh{number}_rh_not_claimed",
            boundary["riemann_hypothesis_implication"] is False,
        )

    rh262, rh263, rh264 = source[262], source[263], source[264]
    rh265, rh266, rh267 = source[265], source[266], source[267]
    rh268, rh269, rh270 = source[268], source[269], source[270]

    check("rh262_boundary_constant", rh262["certified_conclusions"]["M_7_over_5_lt_108"] is True)
    check("rh263_exact_parity_anchor", rh263["theorem_boundary"]["all_order_deterministic_parity_dictionary"] is True)
    check("rh263_27_cross_checks", rh263["orders_cross_checked"] == 27)
    check("rh264_direct_tail", rh264["theorem_boundary"]["direct_factorwise_all_order_target_tail"] is True)
    check("rh264_clean_order29", rh264["claims"]["total_lt"] == "0.000026624745")
    check("rh265_seven_ladder_orders", rh265["orders"] == [13, 21, 29, 37, 45, 53, 61])
    check("rh265_higher_heads_conditional", rh265["higher_orders_are_conditional_interfaces"] is True)
    check("rh266_finite_uniformity_obstruction", rh266["theorem_boundary"]["finite_data_insufficient_for_uniformity"] is True)
    check("rh266_actual_nonuniformity_not_proved", rh266["theorem_boundary"]["underlying_family_proved_nonuniform"] is False)
    check("rh266_23_of_32", rh266["coverage"]["finite_sample_count"] == 23 and rh266["coverage"]["missing_archived_count"] == 9)
    check("rh267_all_order_envelope", rh267["theorem_boundary"]["deterministic_target_all_order_envelope"] is True)
    check("rh267_constant_48", rh267["clean_envelope_constant"] == 48)
    check("rh267_moving_cloud_open", rh267["theorem_boundary"]["moving_cloud_uniform_trace_envelope"] is False)
    check("rh268_sharp_rate", rh268["theorem_boundary"]["deterministic_sharp_rate"] is True)
    check("rh268_all_exact_conclusions", all(rh268["exact_conclusions"].values()))
    check("rh268_moving_cloud_sharp_open", rh268["theorem_boundary"]["moving_cloud_sharp_rate"] is False)
    check("rh269_sufficient_criterion", rh269["theorem_boundary"]["sufficient_uniform_quotient_criterion"] is True)
    check("rh269_zero_of_four", rh269["criterion_hypotheses"]["satisfied_hypothesis_count"] == 0 and rh269["criterion_hypotheses"]["required_hypothesis_count"] == 4)
    check("rh269_uniform_tail_open", rh269["theorem_boundary"]["uniform_quotient_tail"] is False)
    check("rh270_consistent", rh270["source_consistency_audit"]["failure_count"] == 0)
    check("rh270_two_of_five", rh270["certificate_status"]["satisfied_component_count"] == 2)
    check("rh270_complete_zero", rh270["complete_certificate_count"] == 0)

    components = obligation_summary(
        legal_anchored_head=rh270["certificate_status"]["components"]["legal_anchored_head"],
        coefficient_bridge=rh270["certificate_status"]["components"]["coefficient_bridge"],
        uniform_quotient_tail=rh270["certificate_status"]["components"]["uniform_quotient_tail"],
        analytic_target_tail=rh270["certificate_status"]["components"]["analytic_target_tail"],
        certified_target_boundary_constant=rh270["certificate_status"]["components"]["certified_target_boundary_constant"],
    )
    check("review_vector_00011", components["obligation_vector"] == [False, False, False, True, True])
    check("review_complete_false", components["complete"] is False)

    hidden_head = [root_of_unity_shell_trace(29, order) for order in range(1, 29)]
    first_visible = root_of_unity_shell_trace(29, 29)
    check("shell_orders_1_to_28_vanish", all(value == 0 for value in hidden_head))
    check("shell_order_29_visible", first_visible == 29)

    statuses = {
        "deterministic_boundary_constant": True,
        "deterministic_all_order_parity_anchor": True,
        "deterministic_direct_tail": True,
        "deterministic_tail_ladder": True,
        "deterministic_all_order_envelope": True,
        "deterministic_sharp_base": True,
        "finite_sample_implies_uniform_quotient": False,
        "uniform_quotient_criterion_available": True,
        "uniform_quotient_criterion_activated": False,
        "legal_anchored_head": False,
        "coefficient_bridge": False,
        "uniform_quotient_tail": False,
        "complete_certificate": False,
        **{f"gate_{letter}": False for letter in "ABCDE"},
    }

    finite_review_records = (
        len(rh262["replays"])
        + len(rh263["rows"])
        + len(rh264["replays"])
        + len(rh265["orders"])
        + rh266["coverage"]["finite_sample_count"]
        + len(rh267["replays"])
        + len(rh268["finite_order_2_to_28_diagnostic"]["last_six"])
        + rh269["criterion_hypotheses"]["required_hypothesis_count"]
        + rh270["source_consistency_audit"]["check_count"]
    )

    paper_rows = [
        {"number": 262, "layer": "certified boundary budget", "result": "M_(7/5)<108 and a rigorous order-29 Cauchy tail", "boundary": "deterministic target only"},
        {"number": 263, "layer": "parity anchor", "result": "exact all-order odd/even coefficient dictionary", "boundary": "27-row check is not a cloud bridge"},
        {"number": 264, "layer": "direct tail", "result": "factorwise order-29 logarithmic tail <2.6624745e-5", "boundary": "no selected cloud"},
        {"number": 265, "layer": "tail ladder", "result": "seven certified omitted-order interfaces", "boundary": "only N=29 has the archived head"},
        {"number": 266, "layer": "finite uniformity obstruction", "result": "finite contractions do not imply continuum uniformity", "boundary": "actual family nonuniformity not proved"},
        {"number": 267, "layer": "unified trace envelope", "result": "|a_n|<48 q_*^n for every n>=2", "boundary": "not a moving-cloud envelope"},
        {"number": 268, "layer": "sharp radius law", "result": "a_n/q_*^n tends to 1 and rho_*=q_*^-1", "boundary": "deterministic sharpness only"},
        {"number": 269, "layer": "contour-stable quotient criterion", "result": "four hypotheses imply local uniform RH-246 constants", "boundary": "archive verifies 0/4"},
        {"number": 270, "layer": "updated certificate ledger", "result": "two of five obligations and zero complete certificates", "boundary": "scoped route ledger"},
        {"number": 271, "layer": "frontier review", "result": "exact target/cloud separation and ten-layer synthesis", "boundary": "Gates A--E remain open"},
    ]

    failures = [row["name"] for row in checks if not row["passed"]]
    if failures:
        raise RuntimeError(f"frontier review checks failed: {failures}")

    return {
        "status": "rh271_ten_layer_deterministic_envelope_quotient_frontier_review",
        "paper_numbers": list(range(262, 272)),
        "route_coordinate": route_coordinate(rh270),
        "statuses": statuses,
        "macro_gates": macro_gates(statuses),
        "certificate_status": components,
        "complete_certificate_count": 0,
        "paper_rows": paper_rows,
        "finite_review_records": int(finite_review_records),
        "source_consistency_checks": checks,
        "audit_failure_count": len(failures),
        "headline_metrics": {
            "boundary_supremum_lt": "107.906078",
            "parity_cross_check_orders": rh263["orders_cross_checked"],
            "parity_maximum_residual": rh263["maximum_absolute_cross_check_residual"],
            "direct_order_29_log_tail_lt": rh264["claims"]["total_lt"],
            "tail_ladder_orders": rh265["orders"],
            "finite_quotient_samples": rh266["coverage"]["finite_sample_count"],
            "missing_quotient_endpoints": rh266["coverage"]["missing_archived_count"],
            "envelope_constant": rh267["clean_envelope_constant"],
            "q_star": rh268["q_star"]["float_midpoint"],
            "rho_star": rh268["rho_star"]["float_midpoint"],
            "quotient_criterion_satisfied_required": [
                rh269["criterion_hypotheses"]["satisfied_hypothesis_count"],
                rh269["criterion_hypotheses"]["required_hypothesis_count"],
            ],
            "ledger_satisfied_required": [
                components["satisfied_component_count"],
                components["required_component_count"],
            ],
        },
        "finite_head_separation_witness": {
            "matched_orders": [1, 28],
            "shell_size": 29,
            "vanishing_moment_count": 28,
            "first_visible_order": 29,
            "unit_amplitude_first_visible_trace": first_visible,
            "conclusion": "A complete root-of-unity shell can preserve any fixed 28-order trace head while changing order 29; finite matching alone cannot establish a uniform cloud bridge.",
        },
        "next_target": (
            "legal_anchored_head_cloud_coefficient_bridge_common_finite_rank_"
            "contour_uniform_resolvent_S2_limit_quotient_contraction"
        ),
        "theorem_boundary": {
            "deterministic_target_package_complete_in_stated_scope": True,
            "root_of_unity_finite_head_separation_theorem": True,
            "finite_fit_promoted_to_cloud_theorem": False,
            "moving_cloud_uniform_trace_envelope": False,
            "legal_anchored_head": False,
            "cloud_coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "complete_certificate": False,
            "underlying_quotient_family_nonuniform": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "hilbert_polya_operator": False,
            "riemann_zero_identification": False,
            "zeta_divisor_equality": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/frontier_review.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "checks": len(payload["source_consistency_checks"]),
                "failures": payload["audit_failure_count"],
                "records": payload["finite_review_records"],
                "satisfied_obligations": payload["certificate_status"]["satisfied_component_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
