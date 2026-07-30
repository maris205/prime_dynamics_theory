"""Assemble the RH-270 deterministic-envelope/quotient certificate ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
SOURCES = {
    262: (
        PAPERS / "RH-262-certified-deterministic-numerator-boundary-budget",
        "certified_boundary_budget.json",
    ),
    263: (
        PAPERS / "RH-263-parity-resolved-deterministic-numerator-tail",
        "parity_anchor_audit.json",
    ),
    264: (
        PAPERS / "RH-264-direct-factorwise-deterministic-tail-certificate",
        "direct_tail_audit.json",
    ),
    265: (
        PAPERS / "RH-265-certified-deterministic-tail-ladder",
        "tail_ladder.json",
    ),
    266: (
        PAPERS / "RH-266-finite-sample-quotient-uniformity-obstruction",
        "uniformity_obstruction.json",
    ),
    267: (
        PAPERS / "RH-267-certified-unified-deterministic-trace-envelope",
        "coefficient_envelope.json",
    ),
    268: (
        PAPERS / "RH-268-sharp-deterministic-coefficient-radius-law",
        "sharp_coefficient_law.json",
    ),
    269: (
        PAPERS / "RH-269-contour-stable-uniform-quotient-criterion",
        "criterion_audit.json",
    ),
}
sys.path.insert(0, str(ROOT / "src"))

from certificate_ledger import (  # noqa: E402
    geometric_log_tail_bound,
    obligation_status,
    safe_ratio,
)


def read_source(number: int) -> dict[str, object]:
    directory, filename = SOURCES[number]
    return json.loads((directory / "results" / filename).read_text(encoding="utf-8"))


def run() -> dict[str, object]:
    source = {number: read_source(number) for number in SOURCES}
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})

    expected_status = {
        262: "rh262_certified_deterministic_numerator_boundary_budget",
        263: "rh263_parity_resolved_deterministic_numerator_tail",
        264: "rh264_direct_factorwise_deterministic_tail_certificate",
        265: "rh265_certified_deterministic_tail_ladder",
        266: "rh266_finite_sample_quotient_uniformity_obstruction",
        267: "rh267_certified_unified_deterministic_trace_envelope",
        268: "rh268_sharp_deterministic_coefficient_radius_law",
        269: "rh269_contour_stable_uniform_quotient_criterion",
    }
    for number, payload in source.items():
        check(f"rh{number}_status", payload["status"] == expected_status[number])
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

    rh262 = source[262]
    check("rh262_boundary_certified", rh262["certified_conclusions"]["M_7_over_5_lt_108"] is True)
    check("rh262_target_tail_true", rh262["obligation_vector"]["analytic_target_tail"] is True)
    check("rh262_boundary_component_true", rh262["obligation_vector"]["certified_target_boundary_constant"] is True)
    check("rh262_satisfied_two", rh262["obligation_vector"]["satisfied_count"] == 2)
    check("rh262_complete_false", rh262["obligation_vector"]["complete"] is False)

    rh263 = source[263]
    check("rh263_exact_dictionary", rh263["theorem_boundary"]["all_order_deterministic_parity_dictionary"] is True)
    check("rh263_27_cross_checks", rh263["orders_cross_checked"] == 27)
    check("rh263_residual_below_6_5e_14", rh263["maximum_absolute_cross_check_residual"] < 6.5e-14)
    check("rh263_cloud_bridge_false", rh263["theorem_boundary"]["cloud_coefficient_bridge"] is False)

    rh264 = source[264]
    check("rh264_direct_tail_theorem", rh264["theorem_boundary"]["direct_factorwise_all_order_target_tail"] is True)
    check("rh264_order29_total", rh264["claims"]["total_lt"] == "0.000026624745")
    check("rh264_order29_multiplicative", rh264["claims"]["multiplicative_lt"] == "0.000026625100")
    check("rh264_complete_false", rh264["obligation_vector"]["complete"] is False)

    rh265 = source[265]
    check("rh265_all_rows_certified", rh265["theorem_boundary"]["all_listed_tail_budgets_certified"] is True)
    check("rh265_order29_aligned", rh265["order_29_is_current_anchor_aligned"] is True)
    check("rh265_higher_rows_conditional", rh265["higher_orders_are_conditional_interfaces"] is True)
    check("rh265_higher_heads_not_constructed", rh265["theorem_boundary"]["higher_order_heads_constructed"] is False)

    rh266 = source[266]
    check("rh266_finite_insufficiency", rh266["theorem_boundary"]["finite_data_insufficient_for_uniformity"] is True)
    check("rh266_actual_nonuniformity_not_proved", rh266["theorem_boundary"]["underlying_family_proved_nonuniform"] is False)
    check("rh266_23_samples", rh266["coverage"]["finite_sample_count"] == 23)
    check("rh266_nine_missing", rh266["coverage"]["missing_archived_count"] == 9)
    check("rh266_uniform_false", rh266["coverage"]["uniform_conclusion_available"] is False)

    rh267 = source[267]
    check("rh267_constant_48", rh267["clean_envelope_constant"] == 48)
    check("rh267_all_order_envelope", rh267["theorem_boundary"]["deterministic_target_all_order_envelope"] is True)
    check("rh267_not_cloud_envelope", rh267["theorem_boundary"]["moving_cloud_uniform_trace_envelope"] is False)
    check("rh267_not_finite_fit", rh267["theorem_boundary"]["finite_fit_used_as_proof"] is False)
    check("rh267_qstar_safe", all(row["comparisons"]["q_star_lt_0_700876"] for row in rh267["replays"]))

    rh268 = source[268]
    for name, value in rh268["exact_conclusions"].items():
        check(f"rh268_{name}", value is True)
    check("rh268_deterministic_sharp", rh268["theorem_boundary"]["deterministic_sharp_rate"] is True)
    check("rh268_cloud_sharp_false", rh268["theorem_boundary"]["moving_cloud_sharp_rate"] is False)

    rh269 = source[269]
    criterion = rh269["criterion_hypotheses"]
    check("rh269_four_required", criterion["required_hypothesis_count"] == 4)
    check("rh269_zero_satisfied", criterion["satisfied_hypothesis_count"] == 0)
    check("rh269_criterion_inactive", criterion["criterion_complete"] is False)
    check("rh269_sufficient_theorem", rh269["theorem_boundary"]["sufficient_uniform_quotient_criterion"] is True)
    check("rh269_uniform_tail_false", rh269["theorem_boundary"]["uniform_quotient_tail"] is False)
    check("rh269_actual_nonuniformity_not_proved", rh269["theorem_boundary"]["underlying_family_proved_nonuniform"] is False)

    component_status = obligation_status(
        legal_anchored_head=bool(rh262["obligation_vector"]["legal_anchored_head"]),
        coefficient_bridge=bool(rh262["obligation_vector"]["coefficient_bridge"]),
        uniform_quotient_tail=bool(rh269["theorem_boundary"]["uniform_quotient_tail"]),
        analytic_target_tail=bool(rh262["obligation_vector"]["analytic_target_tail"]),
        certified_target_boundary_constant=bool(
            rh262["obligation_vector"]["certified_target_boundary_constant"]
        ),
    )
    check("ledger_vector_00011", component_status["obligation_vector"] == [False, False, False, True, True])
    check("ledger_satisfied_two", component_status["satisfied_component_count"] == 2)
    check("ledger_complete_false", component_status["complete"] is False)

    q_star = float(rh268["q_star"]["float_midpoint"])
    rho_star = float(rh268["rho_star"]["float_midpoint"])
    q_safe = 0.700876
    envelope_order_29 = geometric_log_tail_bound(48.0, q_safe, 1.0, 29)
    direct_order_29 = float(rh264["claims"]["total_lt"])
    endpoint_improvement = safe_ratio(envelope_order_29, direct_order_29)
    check("coarse_envelope_tail_below_0_000184751", envelope_order_29 < 0.000184751)
    check("direct_endpoint_improvement_above_6_93", endpoint_improvement > 6.93)
    check("qstar_rhostar_reciprocal", abs(q_star * rho_star - 1.0) < 2e-15)

    complete_count = 1 if component_status["complete"] else 0
    check("complete_certificate_count_zero", complete_count == 0)

    failures = [row["name"] for row in checks if not row["passed"]]
    if failures:
        raise RuntimeError(f"source consistency checks failed: {failures}")

    return {
        "status": "rh270_updated_deterministic_envelope_quotient_certificate_ledger",
        "route_coordinate": (
            "deterministic_target_envelope_sharp_legal_head_bridge_"
            "uniform_quotient_open_complete_zero"
        ),
        "source_range": [262, 269],
        "deterministic_target": {
            "boundary_budget": {
                "circle": "7/5",
                "certified_supremum_lt": "107.906078",
                "clean_supremum_lt": "108",
            },
            "parity_anchor": {
                "all_order_exact": True,
                "finite_cross_check_orders": rh263["orders_cross_checked"],
                "maximum_cross_check_residual": rh263[
                    "maximum_absolute_cross_check_residual"
                ],
                "finite_cross_check_is_cloud_bridge": False,
            },
            "direct_order_29_tail": {
                "logarithmic_lt": rh264["claims"]["total_lt"],
                "multiplicative_lt": rh264["claims"]["multiplicative_lt"],
                "all_order_factorwise_certificate": True,
            },
            "tail_ladder": {
                "orders": rh265["orders"],
                "order_29_current_head_aligned": True,
                "higher_orders_conditional_interfaces": True,
            },
            "unified_envelope": {
                "statement": "For every n>=2, |a_n| < 48 q_star^n.",
                "constant": rh267["clean_envelope_constant"],
                "q_star": q_star,
                "q_star_safe_upper": q_safe,
                "moving_cloud_envelope": False,
            },
            "sharp_law": {
                "statement": "a_n/q_star^n tends to 1",
                "rho_star": rho_star,
                "smaller_geometric_base_possible": False,
                "critical_absolute_log_series_diverges": True,
            },
            "cross_source_comparison": {
                "envelope_only_order_29_log_tail_bound": envelope_order_29,
                "envelope_only_clean_lt": "0.000184751",
                "direct_factorwise_clean_lt": rh264["claims"]["total_lt"],
                "upper_endpoint_improvement_factor": endpoint_improvement,
                "improvement_factor_gt": "6.93",
            },
        },
        "quotient_and_cloud": {
            "finite_power_12_contractions": rh266["finite_metrics"][
                "power_12_contractive_count"
            ],
            "finite_sample_count": rh266["coverage"]["finite_sample_count"],
            "missing_archived_endpoint_count": rh266["coverage"][
                "missing_archived_count"
            ],
            "finite_samples_imply_uniformity": False,
            "underlying_family_proved_nonuniform": False,
            "criterion": criterion,
            "missing_criterion_hypotheses": rh269["missing_hypotheses"],
            "uniform_quotient_tail": False,
            "cloud_coefficient_bridge": False,
            "legal_anchored_head": False,
        },
        "certificate_status": component_status,
        "complete_certificate_count": complete_count,
        "source_consistency_audit": {
            "check_count": len(checks),
            "failure_count": len(failures),
            "failures": failures,
        },
        "theorem_boundary": {
            "deterministic_boundary_constant": True,
            "all_order_deterministic_parity_anchor": True,
            "direct_all_order_deterministic_tail": True,
            "deterministic_all_order_envelope": True,
            "deterministic_sharp_base": True,
            "legal_anchored_head": False,
            "cloud_coefficient_bridge": False,
            "uniform_quotient_tail": False,
            "criterion_hypotheses_verified": False,
            "complete_certificate": False,
            "global_selector_nonexistence": False,
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
    output = ROOT / "results/updated_certificate_ledger.json"
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "output": str(output.relative_to(ROOT)),
                "checks": payload["source_consistency_audit"]["check_count"],
                "failures": payload["source_consistency_audit"]["failure_count"],
                "satisfied_obligations": payload["certificate_status"][
                    "satisfied_component_count"
                ],
                "complete_certificates": payload["complete_certificate_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
