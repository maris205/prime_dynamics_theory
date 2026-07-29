"""Assemble the RH-252--RH-261 analytic-tail/selector frontier review."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from frontier_review import macro_gates, obligation_summary, route_coordinate  # noqa: E402


SOURCES = {
    252: (
        "RH-252-deterministic-numerator-analytic-tail-certificate",
        "analytic_tail_audit.json",
    ),
    253: (
        "RH-253-extended-deterministic-anchor-atlas",
        "extended_anchor_atlas.json",
    ),
    254: (
        "RH-254-expanded-resolved-candidate-window-atlas",
        "expanded_window_atlas.json",
    ),
    255: (
        "RH-255-expanded-window-anchored-zonotope-obstruction",
        "expanded_reachability_audit.json",
    ),
    256: (
        "RH-256-invariant-polynomial-selector-binary-collapse",
        "polynomial_selector_audit.json",
    ),
    257: (
        "RH-257-monodromy-integrality-barrier-for-signed-moment-fits",
        "signed_moment_audit.json",
    ),
    258: (
        "RH-258-unit-cap-signed-integer-selector-obstruction",
        "unit_cap_integer_audit.json",
    ),
    259: (
        "RH-259-extended-quotient-block-power-diagnostic",
        "extended_quotient_audit.json",
    ),
    260: (
        "RH-260-updated-anchored-head-tail-certificate-ledger",
        "updated_certificate_ledger.json",
    ),
}


def load_sources() -> dict[int, dict[str, object]]:
    return {
        number: json.loads(
            (PAPERS / directory / "results" / filename).read_text(encoding="utf-8")
        )
        for number, (directory, filename) in SOURCES.items()
    }


def _check(checks: list[dict[str, object]], name: str, condition: bool) -> None:
    checks.append({"name": name, "passed": bool(condition)})


def run() -> dict[str, object]:
    source = load_sources()
    target = source[252]
    atlas = source[253]
    window = source[254]
    box = source[255]
    polynomial = source[256]
    monodromy = source[257]
    unit_cap = source[258]
    quotient = source[259]
    ledger = source[260]

    checks: list[dict[str, object]] = []
    _check(checks, "rh252_target_tail_exists", target["unit_disk_all_order_target_tail_exists"] is True)
    _check(checks, "rh252_boundary_constant_open", target["finite_boundary_supremum_available"] is False)
    _check(checks, "rh253_order_28_atlas", atlas["maximum_order"] == 28)
    _check(checks, "rh254_32_endpoints", window["endpoint_count"] == 32)
    _check(checks, "rh254_21_complete_11_incomplete", (
        window["expanded_shell_complete_endpoint_count"] == 21
        and window["expanded_shell_incomplete_endpoint_count"] == 11
    ))
    _check(checks, "rh255_box_zero_passes", box["box_zonotope_pass_count"] == 0)
    _check(checks, "rh255_lp_gap_small", box["maximum_box_primal_dual_gap"] < 1.0e-9)
    _check(checks, "rh256_scoped_idempotent_firewall", polynomial[
        "real_conjugate_closed_idempotent_selector_pass_count"
    ] == 0)
    _check(checks, "rh257_fractional_fit_count", monodromy["signed_fit_pass_count"] == 32)
    _check(checks, "rh257_integer_necessity", monodromy["theorem_boundary"][
        "integer_weights_are_necessary_for_single_valued_meromorphic_product"
    ] is True)
    _check(checks, "rh258_unit_cap_zero_passes", unit_cap["integer_selector_pass_count"] == 0)
    _check(checks, "rh258_mip_gap_zero", unit_cap["maximum_mip_gap"] == 0.0)
    _check(checks, "rh259_23_power12_blocks", (
        quotient["eligible_endpoint_count"] == 23
        and quotient["power_12_contractive_count"] == 23
    ))
    _check(checks, "rh259_uniform_theorem_open", quotient["theorem_boundary"][
        "uniform_small_noise_block_power"
    ] is False)
    _check(checks, "rh260_source_consistency", ledger["source_consistency_audit"]["failure_count"] == 0)
    _check(checks, "rh260_zero_complete_certificates", ledger["complete_certificate_count"] == 0)
    _check(checks, "rh260_one_satisfied_component", ledger["component_status"]["satisfied_component_count"] == 1)

    statuses = {
        "analytic_target_tail_interface": target["theorem_boundary"]["analytic_all_order_target_tail"],
        "certified_target_boundary_constant": target["finite_boundary_supremum_available"],
        "extended_anchor_atlas": atlas["maximum_order"] == 28,
        "expanded_window": window["theorem_boundary"]["expanded_window_finite"],
        "expanded_box_anchor": box["box_zonotope_pass_count"] > 0,
        "real_conjugate_closed_idempotent_head": polynomial[
            "real_conjugate_closed_idempotent_selector_pass_count"
        ] > 0,
        "fractional_signed_fit_legal": monodromy["theorem_boundary"][
            "fractional_signed_fit_is_legal_determinant_quotient"
        ],
        "unit_cap_signed_head": unit_cap["integer_selector_pass_count"] > 0,
        "finite_quotient_diagnostic": quotient["power_12_contractive_count"] == quotient["eligible_endpoint_count"],
        "uniform_quotient_tail": quotient["theorem_boundary"]["uniform_small_noise_block_power"],
        "complete_certificate": ledger["complete_certificate_count"] > 0,
        "coefficient_bridge": False,
        "gate_A": False,
        "gate_B": False,
        "gate_C": False,
        "gate_D": False,
        "gate_E": False,
    }
    components = obligation_summary(
        legal_anchored_head=ledger["component_status"]["components"]["legal_anchored_head"],
        coefficient_bridge=ledger["component_status"]["components"]["coefficient_bridge"],
        uniform_quotient_tail=ledger["component_status"]["components"]["uniform_quotient_tail"],
        analytic_target_tail=ledger["component_status"]["components"]["analytic_target_tail"],
        certified_target_boundary_constant=ledger["component_status"]["components"][
            "certified_target_boundary_constant"
        ],
    )

    coefficient_rows = len(atlas["coefficient_rows"])
    target_radius_rows = sum(len(row["inner_radius_rows"]) for row in target["rows"])
    new_root_count = sum(row["new_candidate_rank"] for row in window["endpoint_rows"])
    endpoint_audit_rows = sum(
        len(source[number].get("endpoint_rows", []))
        for number in (254, 255, 256, 257, 258, 259)
    )
    finite_review_records = (
        coefficient_rows
        + target_radius_rows
        + new_root_count
        + endpoint_audit_rows
        + ledger["anchored_head"]["audited_class_endpoint_case_count"]
        + ledger["source_consistency_audit"]["check_count"]
    )

    paper_rows = [
        {
            "number": 252,
            "layer": "deterministic target tail",
            "claim_level": "exact analytic interface, numerical constant open",
            "blocker": "certified M_S and cloud coefficient bridge",
        },
        {
            "number": 253,
            "layer": "extended deterministic anchor",
            "claim_level": "exact finite dictionary through order 28",
            "blocker": "finite fit is not an all-order cloud envelope",
        },
        {
            "number": 254,
            "layer": "expanded resolved window",
            "claim_level": "finite spectral atlas",
            "blocker": "11 boundary-split windows and no legal anchor yet",
        },
        {
            "number": 255,
            "layer": "expanded anchored box",
            "claim_level": "dual-certified scoped obstruction",
            "blocker": "signed/complex or larger legal selector",
        },
        {
            "number": 256,
            "layer": "polynomial idempotent selector",
            "claim_level": "exact binary-collapse theorem",
            "blocker": "non-idempotent grouping, non-conjugate complex mask, or outside algebra",
        },
        {
            "number": 257,
            "layer": "signed moment fits",
            "claim_level": "exact monodromy-integrality barrier",
            "blocker": "bounded integer selector with operator meaning",
        },
        {
            "number": 258,
            "layer": "unit-cap signed lattice",
            "claim_level": "zero-pass MILP obstruction",
            "blocker": "larger cap and invariant realization",
        },
        {
            "number": 259,
            "layer": "quotient block power",
            "claim_level": "23-endpoint finite diagnostic",
            "blocker": "uniform small-noise theorem and continuum bridge",
        },
        {
            "number": 260,
            "layer": "updated head/tail ledger",
            "claim_level": "exact gluing interface and zero current certificates",
            "blocker": "four missing obligations, including certified M_S",
        },
        {
            "number": 261,
            "layer": "frontier review",
            "claim_level": "ten-layer synthesis with scoped route stop",
            "blocker": "a genuinely new legal head and uniform tails",
        },
    ]

    return {
        "status": "rh261_ten_layer_analytic_tail_selector_frontier_review",
        "paper_numbers": list(range(252, 262)),
        "route_coordinate": route_coordinate(ledger),
        "statuses": statuses,
        "macro_gates": macro_gates(statuses),
        "paper_rows": paper_rows,
        "finite_review_records": int(finite_review_records),
        "audit_failure_count": sum(not row["passed"] for row in checks),
        "source_consistency_checks": checks,
        "headline_metrics": {
            "rh252_scaled_zero_free_radius": target["scaled_zero_free_radius"],
            "rh252_target_tail_factor_per_M_order_13": target["best_unit_disk_order_13_tail_factor_per_M"],
            "rh253_maximum_order": atlas["maximum_order"],
            "rh253_order_13_to_28_unit_disk_log_norm": atlas["order_13_to_28_unit_disk_log_norm"],
            "rh253_finite_root_rate": atlas["new_all_log_linear_root_rate"],
            "rh254_endpoint_count": window["endpoint_count"],
            "rh254_new_root_count": int(new_root_count),
            "rh254_complete_incomplete": [
                window["expanded_shell_complete_endpoint_count"],
                window["expanded_shell_incomplete_endpoint_count"],
            ],
            "rh254_maximum_matching_error": window["maximum_matching_error"],
            "rh255_box_passes": box["box_zonotope_pass_count"],
            "rh255_box_distance_range": [box["minimum_box_distance"], box["maximum_box_distance"]],
            "rh255_binary_subset_count": box["total_eligible_binary_subset_count"],
            "rh256_real_conjugate_closed_idempotent_passes": polynomial[
                "real_conjugate_closed_idempotent_selector_pass_count"
            ],
            "rh256_maximum_interpolation_residual": polynomial["maximum_interpolation_residual"],
            "rh257_signed_fit_passes": monodromy["signed_fit_pass_count"],
            "rh257_integer_fit_passes": monodromy["integer_weight_fit_count"],
            "rh257_maximum_weight_range": [
                monodromy["minimum_maximum_absolute_weight"],
                monodromy["maximum_maximum_absolute_weight"],
            ],
            "rh257_maximum_monodromy_defect": monodromy["maximum_monodromy_defect"],
            "rh258_unit_cap_passes": unit_cap["integer_selector_pass_count"],
            "rh258_integer_distance_range": [
                unit_cap["minimum_integer_distance"],
                unit_cap["maximum_integer_distance"],
            ],
            "rh258_signed_lattice_point_count": unit_cap["total_signed_lattice_point_count"],
            "rh259_endpoint_count": quotient["eligible_endpoint_count"],
            "rh259_q12_range": [quotient["minimum_q12"], quotient["maximum_q12"]],
            "rh259_q12_deterioration_factor": quotient["q12_deterioration_factor"],
            "rh259_finite_tail_diagnostic": quotient["finite_sample_unit_disk_logarithmic_tail_bound_from_order_12"],
            "rh260_head_cases": ledger["anchored_head"]["audited_class_endpoint_case_count"],
            "rh260_head_passes": ledger["anchored_head"]["total_pass_count"],
            "rh260_remaining_quotient_endpoints": ledger["quotient_tail"]["remaining_archived_endpoint_count"],
            "rh260_complete_certificates": ledger["complete_certificate_count"],
            "rh260_satisfied_components": ledger["component_status"]["satisfied_component_count"],
        },
        "next_target": (
            "certified_target_Ms_legal_selector_outside_audited_classes_"
            "uniform_quotient_tail_coefficient_bridge"
        ),
        "theorem_boundary": {
            "analytic_target_tail_interface": True,
            "finite_order_atlas_only": True,
            "expanded_head_classes_scoped_obstruction": True,
            "fractional_signed_fits_not_legal_determinant": True,
            "unit_cap_signed_integer_class_obstructed": True,
            "uniform_quotient_tail": False,
            "certified_target_boundary_constant": False,
            "coefficient_bridge": False,
            "complete_head_tail_certificate": False,
            "locally_uniform_relative_determinant_family": False,
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
    output = ROOT / "results/frontier_review.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "route": payload["route_coordinate"],
        "finite_review_records": payload["finite_review_records"],
        "audit_failures": payload["audit_failure_count"],
        "next_target": payload["next_target"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
