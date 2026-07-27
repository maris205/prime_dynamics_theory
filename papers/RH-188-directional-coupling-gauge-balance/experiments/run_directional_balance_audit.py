"""Balance the two physical RH-185 coupling residuals without changing their product."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
sys.path.insert(0, str(ROOT / "src"))

from directional_balance import scalar_gauge_balance  # noqa: E402


def summarize(records: list[dict[str, object]], key: str) -> dict[str, float]:
    values = np.asarray([float(item[key]) for item in records])
    return {"minimum": float(values.min()), "median": float(np.median(values)), "maximum": float(values.max())}


def run(smoke: bool) -> dict[str, object]:
    source_name = "bi_krylov_smoke.json" if smoke else "bi_krylov_audit.json"
    source = json.loads((RH185 / "results" / source_name).read_text(encoding="utf-8"))
    records = []
    for item in source["records"]:
        balance = scalar_gauge_balance(item["left_residual_norm"], item["right_residual_norm"])
        records.append({
            "sigma": item["sigma"],
            "side": item["side"],
            "candidate_length": item["candidate_length"],
            "start": item["start"],
            "left_residual_norm": item["left_residual_norm"],
            "right_residual_norm": item["right_residual_norm"],
            "relative_coupling_product": float(item["left_relative_residual"]) * float(item["right_relative_residual"]),
            **balance,
        })
    local = [item for item in records if float(item["sigma"]) == 0.01 and int(item["candidate_length"]) == 4]
    return {
        "status": "rh188_directional_coupling_gauge_balance_audit",
        "window_count": len(records),
        "local_l4_window_count": len(local),
        "absolute_coupling_product_below_1_count": sum(float(item["directed_coupling_product"]) < 1.0 for item in records),
        "local_l4_absolute_product_below_1_count": sum(float(item["directed_coupling_product"]) < 1.0 for item in local),
        "relative_coupling_product_below_0_01_count": sum(float(item["relative_coupling_product"]) < 0.01 for item in records),
        "local_l4_relative_product_below_0_01_count": sum(float(item["relative_coupling_product"]) < 0.01 for item in local),
        "directed_coupling_product": summarize(records, "directed_coupling_product"),
        "balanced_maximum_coupling": summarize(records, "balanced_maximum_coupling"),
        "relative_coupling_product": summarize(records, "relative_coupling_product"),
        "records": records,
        "theorem_boundary": {
            "scalar_gauge_product_invariance": True,
            "optimal_scalar_balance": True,
            "finite_physical_coupling_audit": not smoke,
            "complement_resolvent_bound": False,
            "continuous_contour_schur_certificate": False,
            "physical_riesz_shell": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "directional_balance_smoke.json" if args.smoke else "directional_balance_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "absolute_products_below_one": payload["absolute_coupling_product_below_1_count"],
        "local_l4_products_below_one": payload["local_l4_absolute_product_below_1_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
