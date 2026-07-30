"""Audit exactly what the RH-259 finite quotient sample can imply."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
RH259 = PAPERS / "RH-259-extended-quotient-block-power-diagnostic"
sys.path.insert(0, str(ROOT / "src"))

from uniformity_obstruction import finite_sample_uniformity_status  # noqa: E402


def run() -> dict[str, object]:
    atlas = json.loads((RH222 / "results/cloud_atlas.json").read_text())
    quotient = json.loads((RH259 / "results/extended_quotient_audit.json").read_text())
    total = len(atlas["endpoint_rows"])
    finite = len(quotient["endpoint_rows"])
    missing = total - finite
    status = finite_sample_uniformity_status(
        sample_count=finite,
        missing_archived_count=missing,
        continuum_modulus_available=False,
    )
    checks = {
        "total_archived_endpoints_32": total == 32,
        "finite_quotient_endpoints_23": finite == 23,
        "missing_archived_endpoints_9": missing == 9,
        "all_finite_power_12_blocks_contractive": sum(
            row["quotient_power_12_operator_norm"] < 1.0
            for row in quotient["endpoint_rows"]
        ) == finite,
        "no_one_step_blocks_contractive": quotient["one_step_contractive_count"] == 0,
        "uniform_status_false": status["uniform_conclusion_available"] is False,
    }
    if not all(checks.values()):
        raise RuntimeError("finite-uniformity source audit failed")
    return {
        "status": "rh266_finite_sample_quotient_uniformity_obstruction",
        "coverage": status,
        "finite_metrics": {
            "archived_endpoint_count": total,
            "audited_endpoint_count": finite,
            "missing_endpoint_count": missing,
            "distinct_sigma_count": len({row["sigma"] for row in quotient["endpoint_rows"]}),
            "left_right_counts": {
                "left": sum(row["side"] == "left" for row in quotient["endpoint_rows"]),
                "right": sum(row["side"] == "right" for row in quotient["endpoint_rows"]),
            },
            "power_12_contractive_count": quotient["power_12_contractive_count"],
            "one_step_contractive_count": quotient["one_step_contractive_count"],
            "first_contractive_depth_range": [
                quotient["minimum_first_contractive_power_depth"],
                quotient["maximum_first_contractive_power_depth"],
            ],
            "q12_range": [quotient["minimum_q12"], quotient["maximum_q12"]],
            "finite_unit_disk_tail_diagnostic": quotient[
                "finite_sample_unit_disk_logarithmic_tail_bound_from_order_12"
            ],
        },
        "source_checks": checks,
        "scoped_negative_result": (
            "Finite pointwise contractions, without complete archived coverage and a "
            "parameter modulus or interval family enclosure, do not imply a uniform "
            "small-noise block-power theorem."
        ),
        "theorem_boundary": {
            "finite_data_insufficient_for_uniformity": True,
            "underlying_family_proved_nonuniform": False,
            "all_archived_endpoints_audited": False,
            "continuum_modulus_available": False,
            "uniform_quotient_tail": False,
            "cloud_coefficient_bridge": False,
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
        "route_coordinate": "finite_quotient_sample_logically_nonuniform_missing_nine_and_continuum",
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/uniformity_obstruction.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "audited": payload["finite_metrics"]["audited_endpoint_count"],
        "missing": payload["finite_metrics"]["missing_endpoint_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
