"""Turn the finite RH-245 power data into a 12-block diagnostic."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH245 = PAPERS / "RH-245-orthogonal-quotient-superloop-compression"
sys.path.insert(0, str(ROOT / "src"))

from block_envelope import (  # noqa: E402
    geometric_envelope_constant,
    logarithmic_tail_bound,
)


BLOCK_SIZE = 12
AUDIT_RADIUS = 1.0


def run() -> dict[str, object]:
    source = json.loads((RH245 / "results/orthogonal_quotient_audit.json").read_text(encoding="utf-8"))
    rows = source["endpoint_rows"]
    eta = max(float(row["quotient_power_12_operator_norm"]) for row in rows)
    trace_norm = max(float(row["quotient_power_12_trace_norm"]) for row in rows)
    remainder_norms = [1.0] + [
        max(float(row["quotient_power_operator_norms_orders_1_to_12"][order - 1]) for row in rows)
        for order in range(1, BLOCK_SIZE)
    ]
    envelope = geometric_envelope_constant(
        trace_norm,
        eta,
        remainder_norms,
        BLOCK_SIZE,
    )
    tail = logarithmic_tail_bound(
        trace_norm,
        eta,
        remainder_norms,
        BLOCK_SIZE,
        AUDIT_RADIUS,
    )
    depths = Counter(int(row["first_contractive_power_depth"]) for row in rows)
    return {
        "status": "rh246_block_power_quotient_envelope_criterion",
        "source_endpoint_count": len(rows),
        "source_maximum_dimension": int(source["maximum_dimension"]),
        "block_size": BLOCK_SIZE,
        "finite_sample_operator_norm_block_bound": eta,
        "finite_sample_trace_norm_block_bound": trace_norm,
        "finite_sample_remainder_operator_norm_bounds_orders_0_to_11": remainder_norms,
        "finite_sample_geometric_rate_q12": envelope["q"],
        "finite_sample_geometric_constant_M12": envelope["M"],
        "finite_sample_unit_disk_logarithmic_tail_bound_from_order_12": tail,
        "minimum_first_contractive_power_depth": min(depths),
        "maximum_first_contractive_power_depth": max(depths),
        "first_contractive_power_depth_histogram": {
            str(depth): count for depth, count in sorted(depths.items())
        },
        "one_step_contractive_count": int(source["one_step_contractive_count"]),
        "route_coordinate": "finite_12_block_contraction_open_uniform_noise_certificate_and_anchor",
        "theorem_boundary": {
            "block_power_trace_envelope_criterion": True,
            "explicit_logarithmic_tail_bound": True,
            "finite_17_endpoint_12_block_diagnostic": True,
            "uniform_noise_block_constants": False,
            "all_32_archived_endpoints_covered": False,
            "continuum_small_noise_bridge": False,
            "uniform_all_order_trace_envelope": False,
            "deterministic_numerator_identification": False,
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
    output = ROOT / "results/block_power_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "q12": payload["finite_sample_geometric_rate_q12"],
        "tail_bound": payload["finite_sample_unit_disk_logarithmic_tail_bound_from_order_12"],
        "depth_histogram": payload["first_contractive_power_depth_histogram"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
