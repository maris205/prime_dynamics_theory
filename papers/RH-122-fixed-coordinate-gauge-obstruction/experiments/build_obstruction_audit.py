from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from fixed_coordinate_obstruction import swap_obstruction_family  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    count = 64 if args.smoke else 512
    epsilons = np.geomspace(1e-1, 1e-14, count)
    records = []
    for epsilon in epsilons:
        row = swap_obstruction_family(float(epsilon), 0.2)
        records.append({
            "epsilon": row["epsilon"],
            "gram_lower_factor": row["gram_lower_factor"],
            "tail_upper_factor": row["tail_upper_factor"],
            "fixed_transfer_factor": row["fixed_transfer_factor"],
            "source_gamma": row["source_gamma"],
            "target_gamma": row["target_gamma"],
            "fixed_gamma_upper": row["fixed_gamma_upper"],
            "gauged_transfer_factor": row["gauged_transfer_factor"],
        })
    slope = float(np.polyfit(np.log10(epsilons), np.log10([r["fixed_transfer_factor"] for r in records]), 1)[0])
    summary = {
        "sample_count": count,
        "formula_failure_count": sum(abs(r["fixed_transfer_factor"] * r["epsilon"] - 1.0) > 2e-12 for r in records),
        "gamma_invariance_failure_count": sum(abs(r["source_gamma"] - r["target_gamma"]) > 2e-12 for r in records),
        "gauged_recovery_failure_count": sum(abs(r["gauged_transfer_factor"] - 1.0) > 2e-12 for r in records),
        "minimum_fixed_transfer_factor": min(r["fixed_transfer_factor"] for r in records),
        "maximum_fixed_transfer_factor": max(r["fixed_transfer_factor"] for r in records),
        "log_log_slope": slope,
    }
    payload = {
        "status": "rh122_fixed_coordinate_gauge_obstruction_audit", "records": records, "audit_summary": summary,
        "theorem_boundary": {
            "sharp_identity_gauge_constants": True, "fixed_coordinate_unboundedness": True,
            "exact_gauge_removes_obstruction": True, "uniform_physical_gauge_proved": False,
            "uniform_stage_A_closed": False, "hilbert_polya_operator": False, "riemann_hypothesis": False,
        },
        "route_consequence": "Fixed-coordinate Loewner comparison can lose an arbitrarily large factor even when source and target relative tail constants are identical. A frame gauge is therefore logically necessary unless a separate common-coordinate condition is proved.",
    }
    output = ROOT / "results" / ("fixed_coordinate_smoke.json" if args.smoke else "fixed_coordinate_audit.json")
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

