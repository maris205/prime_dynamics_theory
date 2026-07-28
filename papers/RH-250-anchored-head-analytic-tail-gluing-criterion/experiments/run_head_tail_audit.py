"""Audit the missing finite-head/analytic-tail gluing certificates."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH246 = PAPERS / "RH-246-block-power-quotient-envelope-criterion"
RH248 = PAPERS / "RH-248-anchored-shell-zonotope-reachability-obstruction"
sys.path.insert(0, str(ROOT / "src"))

from head_tail_gluing import logarithmic_gluing_error  # noqa: E402


def run() -> dict[str, object]:
    head = json.loads((RH248 / "results/zonotope_audit.json").read_text(encoding="utf-8"))
    tail = json.loads((RH246 / "results/block_power_audit.json").read_text(encoding="utf-8"))
    head_min = float(head["minimum_box_distance"])
    head_max = float(head["maximum_box_distance"])
    tail_bound = float(tail["finite_sample_unit_disk_logarithmic_tail_bound_from_order_12"])
    head_tail_ratio = head_min / tail_bound
    return {
        "status": "rh250_anchored_head_analytic_tail_gluing_criterion",
        "head_endpoint_count": int(head["endpoint_count"]),
        "tail_endpoint_count": int(tail["source_endpoint_count"]),
        "head_class": "RH-248 frozen shell box relaxation",
        "head_orders": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        "tail_block_size": int(tail["block_size"]),
        "head_tolerance_rule": "epsilon_sigma=sigma",
        "head_pass_count": int(head["box_zonotope_pass_count"]),
        "head_distance_range": [head_min, head_max],
        "tail_finite_subbatch_bound": tail_bound,
        "head_minimum_to_tail_bound_ratio": head_tail_ratio,
        "tail_coverage_is_uniform_over_head_endpoints": False,
        "target_tail_bound_available": False,
        "complete_gluing_certificate_count": 0,
        "illustrative_log_error_budget_if_target_tail_zero": logarithmic_gluing_error(
            head_min,
            tail_bound,
            0.0,
        ),
        "route_coordinate": "finite_head_anchor_missing_tail_conditional_open_new_anchor_or_route_stop",
        "theorem_boundary": {
            "finite_head_plus_tail_log_gluing_theorem": True,
            "current_relaxed_head_has_no_archived_pass": True,
            "finite_17_endpoint_tail_diagnostic": True,
            "uniform_tail_constants": False,
            "target_numerator_tail_bound": False,
            "continuum_head_tail_bridge": False,
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
    output = ROOT / "results/head_tail_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "head_passes": payload["head_pass_count"],
        "tail_bound": payload["tail_finite_subbatch_bound"],
        "head_to_tail_ratio": payload["head_minimum_to_tail_bound_ratio"],
        "complete_certificates": payload["complete_gluing_certificate_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
