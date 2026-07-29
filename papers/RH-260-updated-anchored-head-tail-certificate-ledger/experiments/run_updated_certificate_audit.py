"""Assemble the updated RH-250 head--tail certificate ledger."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH252 = PAPERS / "RH-252-deterministic-numerator-analytic-tail-certificate"
RH255 = PAPERS / "RH-255-expanded-window-anchored-zonotope-obstruction"
RH258 = PAPERS / "RH-258-unit-cap-signed-integer-selector-obstruction"
RH259 = PAPERS / "RH-259-extended-quotient-block-power-diagnostic"
sys.path.insert(0, str(ROOT / "src"))

from certificate_ledger import complete_certificate_status  # noqa: E402


def read_json(directory: Path, filename: str) -> dict[str, object]:
    return json.loads((directory / "results" / filename).read_text(encoding="utf-8"))


def run() -> dict[str, object]:
    target = read_json(RH252, "analytic_tail_audit.json")
    box = read_json(RH255, "expanded_reachability_audit.json")
    signed = read_json(RH258, "unit_cap_integer_audit.json")
    quotient = read_json(RH259, "extended_quotient_audit.json")

    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool) -> None:
        checks.append({"name": name, "passed": bool(condition)})

    target_boundary = target["theorem_boundary"]
    box_boundary = box["theorem_boundary"]
    signed_boundary = signed["theorem_boundary"]
    quotient_boundary = quotient["theorem_boundary"]

    check(
        "rh252_status",
        target["status"] == "rh252_deterministic_numerator_analytic_tail_certificate",
    )
    check("rh252_analytic_tail_exists", target["unit_disk_all_order_target_tail_exists"] is True)
    check("rh252_analytic_boundary", target_boundary["analytic_all_order_target_tail"] is True)
    check("rh252_Ms_not_certified", target["finite_boundary_supremum_available"] is False)
    check("rh255_status", box["status"] == "rh255_expanded_window_anchored_zonotope_obstruction")
    check("rh255_32_endpoints", box["endpoint_count"] == 32)
    check("rh255_zero_box_passes", box["box_zonotope_pass_count"] == 0)
    check("rh255_zero_prefix_passes", box["prefix_pass_count"] == 0)
    check("rh258_status", signed["status"] == "rh258_unit_cap_signed_integer_selector_obstruction")
    check("rh258_32_endpoints", signed["endpoint_count"] == 32)
    check("rh258_zero_integer_passes", signed["integer_selector_pass_count"] == 0)
    check("rh259_status", quotient["status"] == "rh259_extended_quotient_block_power_diagnostic")
    check("rh259_23_endpoints", quotient["eligible_endpoint_count"] == 23)
    check(
        "rh259_all_audited_power12_contractive",
        quotient["power_12_contractive_count"] == quotient["eligible_endpoint_count"],
    )
    check("rh259_uniform_small_noise_open", quotient_boundary["uniform_small_noise_block_power"] is False)
    check("rh259_all_archived_endpoints_not_audited", quotient_boundary["all_archived_endpoints_audited"] is False)
    check("rh259_finite_dimension_diagnostic", quotient_boundary["finite_dimension_1024_diagnostic"] is True)
    check("rh255_signed_complex_not_excluded", box_boundary["signed_or_complex_selector_excluded"] is False)
    check("rh258_larger_caps_open", signed_boundary["larger_integer_caps_excluded"] is False)
    check("rh258_operator_realization_open", signed_boundary["integer_mask_has_operator_realization"] is False)

    endpoint_count = int(box["endpoint_count"])
    class_endpoint_cases = endpoint_count + int(signed["endpoint_count"])
    total_head_passes = int(box["box_zonotope_pass_count"]) + int(
        signed["integer_selector_pass_count"]
    )
    remaining_archived = endpoint_count - int(quotient["eligible_endpoint_count"])
    check("same_32_endpoint_universe", signed["endpoint_count"] == endpoint_count)
    check("nine_quotient_endpoints_uncontrolled", remaining_archived == 9)
    check("union_of_audited_head_classes_has_no_pass", total_head_passes == 0)

    component_status = complete_certificate_status(
        legal_anchored_head=total_head_passes > 0,
        coefficient_bridge=bool(target_boundary["current_cloud_coefficient_bridge"]),
        uniform_quotient_tail=bool(quotient_boundary["uniform_small_noise_block_power"]),
        analytic_target_tail=bool(target_boundary["analytic_all_order_target_tail"]),
        certified_target_boundary_constant=bool(
            target["finite_boundary_supremum_available"]
        ),
    )
    complete_count = endpoint_count if component_status["complete"] else 0
    check("complete_certificate_count_zero", complete_count == 0)

    for source_name, boundary in (
        ("rh252", target_boundary),
        ("rh255", box_boundary),
        ("rh258", signed_boundary),
        ("rh259", quotient_boundary),
    ):
        for letter in "ABCDE":
            check(f"{source_name}_gate_{letter}_open", boundary[f"gate_{letter}"] is False)

    failures = [row["name"] for row in checks if not row["passed"]]
    if failures:
        raise RuntimeError(f"source consistency checks failed: {failures}")

    return {
        "status": "rh260_updated_anchored_head_tail_certificate_ledger",
        "route_coordinate": (
            "legal_heads_obstructed_target_tail_exists_Ms_uncertified_"
            "quotient_finite_nonuniform_complete_certificate_zero"
        ),
        "gluing_interface": {
            "logarithmic_bound": "H_N + Q_N + A_N",
            "target_tail_bound": "M_S * (R/S)^N / (1-R/S)",
            "determinant_bound": "exp(B_*) * (exp(H_N+Q_N+A_N)-1)",
            "first_omitted_order_convention": "N",
            "uniform_convergence_requires_all_three_budgets_to_vanish": True,
        },
        "target_tail": {
            "analytic_interface_exists": bool(
                target["unit_disk_all_order_target_tail_exists"]
            ),
            "scaled_zero_free_radius": target["scaled_zero_free_radius"],
            "hardy_radius": target["hardy_radius"],
            "first_omitted_order_diagnostic": 13,
            "unit_disk_tail_factor_per_M": target[
                "best_unit_disk_order_13_tail_factor_per_M"
            ],
            "certified_boundary_supremum_available": bool(
                target["finite_boundary_supremum_available"]
            ),
            "numerical_tail_bound_available": False,
            "finite_scan_is_proof": False,
        },
        "anchored_head": {
            "audited_endpoint_count": endpoint_count,
            "audited_class_endpoint_case_count": class_endpoint_cases,
            "classes": {
                "rh255_expanded_single_use_box": {
                    "pass_count": box["box_zonotope_pass_count"],
                    "prefix_pass_count": box["prefix_pass_count"],
                    "minimum_distance": box["minimum_box_distance"],
                    "maximum_distance": box["maximum_box_distance"],
                    "eligible_binary_subset_count": box[
                        "total_eligible_binary_subset_count"
                    ],
                    "primal_dual_gap_max": box["maximum_box_primal_dual_gap"],
                    "operator_realization_claimed": False,
                },
                "rh258_unit_cap_signed_integer": {
                    "pass_count": signed["integer_selector_pass_count"],
                    "minimum_distance": signed["minimum_integer_distance"],
                    "maximum_distance": signed["maximum_integer_distance"],
                    "total_signed_lattice_point_count": signed[
                        "total_signed_lattice_point_count"
                    ],
                    "maximum_mip_gap": signed["maximum_mip_gap"],
                    "operator_realization_claimed": False,
                },
            },
            "total_pass_count": total_head_passes,
            "any_legal_head_pass_count": 0 if total_head_passes == 0 else None,
            "head_obstruction_scope": "the two archived expanded head classes only",
        },
        "quotient_tail": {
            "finite_endpoint_count": quotient["eligible_endpoint_count"],
            "remaining_archived_endpoint_count": remaining_archived,
            "power_12_contractive_count": quotient["power_12_contractive_count"],
            "minimum_q12": quotient["minimum_q12"],
            "maximum_q12": quotient["maximum_q12"],
            "maximum_q12_endpoint": quotient["maximum_q12_endpoint"],
            "finite_unit_disk_logarithmic_tail_diagnostic": quotient[
                "finite_sample_unit_disk_logarithmic_tail_bound_from_order_12"
            ],
            "uniform_small_noise_certificate": bool(
                quotient_boundary["uniform_small_noise_block_power"]
            ),
            "all_archived_endpoints_audited": bool(
                quotient_boundary["all_archived_endpoints_audited"]
            ),
            "floating_diagnostic_not_interval_enclosure": True,
        },
        "component_status": component_status,
        "complete_certificate_count": complete_count,
        "source_consistency_audit": {
            "check_count": len(checks),
            "failure_count": len(failures),
            "failures": failures,
        },
        "theorem_boundary": {
            "updated_head_tail_gluing_theorem": True,
            "analytic_all_order_target_tail": True,
            "certified_target_boundary_constant": False,
            "expanded_single_use_head_class_obstructed": True,
            "unit_cap_signed_integer_head_class_obstructed": True,
            "finite_23_endpoint_quotient_diagnostic": True,
            "uniform_quotient_tail": False,
            "current_cloud_coefficient_bridge": False,
            "complete_head_tail_certificate": False,
            "locally_uniform_relative_determinant_family": False,
            "uniform_all_order_trace_envelope": False,
            "gate_A": False,
            "gate_B": False,
            "gate_C": False,
            "gate_D": False,
            "gate_E": False,
            "hilbert_polya_operator": False,
            "zeta_divisor_identification": False,
            "riemann_hypothesis_implication": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/updated_certificate_ledger.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "head_cases": payload["anchored_head"]["audited_class_endpoint_case_count"],
        "head_passes": payload["anchored_head"]["total_pass_count"],
        "quotient_endpoints": payload["quotient_tail"]["finite_endpoint_count"],
        "complete_certificates": payload["complete_certificate_count"],
        "consistency_failures": payload["source_consistency_audit"]["failure_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
