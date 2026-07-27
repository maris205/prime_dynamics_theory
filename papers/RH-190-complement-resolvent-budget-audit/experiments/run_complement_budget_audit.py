"""Apply the sharp elementary orthonormal-coordinate complement bound to RH-185."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
sys.path.insert(0, str(ROOT / "src"))

from complement_budget import norm_only_complement_budget, root_half_spacing  # noqa: E402


CONTOUR_FRACTION = 0.4


def summarize(records: list[dict[str, object]], key: str) -> dict[str, float]:
    values = np.asarray([float(item[key]) for item in records])
    return {"minimum": float(values.min()), "median": float(np.median(values)), "maximum": float(values.max())}


def run(smoke: bool) -> dict[str, object]:
    source_name = "bi_krylov_smoke.json" if smoke else "bi_krylov_audit.json"
    source = json.loads((RH185 / "results" / source_name).read_text(encoding="utf-8"))
    records = []
    for item in source["records"]:
        length = int(item["candidate_length"])
        radius = float(item["source_cycle_radius"])
        spacing = root_half_spacing(length, radius)
        contour = CONTOUR_FRACTION * spacing
        packet_resolvent = 1.0 / contour
        budget = norm_only_complement_budget(
            item["operator_norm"],
            item["oblique_condition_number"],
            radius,
            contour,
            packet_resolvent,
            item["left_residual_norm"],
            item["right_residual_norm"],
        )
        optimistic_schur = packet_resolvent * float(item["left_residual_norm"]) * float(item["right_residual_norm"])
        records.append({
            "sigma": item["sigma"],
            "side": item["side"],
            "candidate_length": length,
            "start": item["start"],
            "root_radius": radius,
            "root_half_spacing": spacing,
            "contour_radius": contour,
            "packet_resolvent_bound": packet_resolvent,
            "optimistic_unit_complement_schur_product": optimistic_schur,
            "optimistic_unit_complement_schur_success": optimistic_schur < 1.0,
            **budget,
        })
    local = [item for item in records if float(item["sigma"]) == 0.01 and int(item["candidate_length"]) == 4]
    return {
        "status": "rh190_complement_resolvent_budget_audit",
        "complement_operator_bound_model": "orthonormal_D_le_chi_times_A",
        "contour_fraction_of_half_spacing": CONTOUR_FRACTION,
        "window_count": len(records),
        "norm_only_resolvent_success_count": sum(bool(item["norm_only_resolvent_available"]) for item in records),
        "full_norm_only_certificate_count": sum(bool(item["full_norm_only_certificate"]) for item in records),
        "local_l4_norm_only_resolvent_success_count": sum(bool(item["norm_only_resolvent_available"]) for item in local),
        "optimistic_unit_complement_schur_success_count": sum(bool(item["optimistic_unit_complement_schur_success"]) for item in records),
        "local_l4_optimistic_unit_complement_schur_success_count": sum(bool(item["optimistic_unit_complement_schur_success"]) for item in local),
        "complement_operator_norm_bound": summarize(records, "complement_operator_norm_bound"),
        "minimum_contour_modulus": summarize(records, "minimum_contour_modulus"),
        "norm_only_clearance": summarize(records, "norm_only_clearance"),
        "optimistic_unit_complement_schur_product": summarize(records, "optimistic_unit_complement_schur_product"),
        "records": records,
        "theorem_boundary": {
            "orthonormal_coordinate_one_factor_bound": True,
            "neumann_resolvent_sufficient_condition": True,
            "finite_physical_norm_audit": not smoke,
            "norm_only_route_survives": any(bool(item["norm_only_resolvent_available"]) for item in records),
            "validated_contour_inverse": False,
            "physical_D_leaf": False,
            "physical_riesz_shell": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "complement_budget_smoke.json" if args.smoke else "complement_budget_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "norm_only_resolvent_successes": payload["norm_only_resolvent_success_count"],
        "optimistic_schur_successes": payload["optimistic_unit_complement_schur_success_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
