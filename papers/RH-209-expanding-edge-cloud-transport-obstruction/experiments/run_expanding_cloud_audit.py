"""Test whether a larger modulus-selected cloud repairs Haar transport."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH58 = PAPERS / "RH-58-time-ordered-schur-cross-gramian"
RH77 = PAPERS / "RH-77-postblock-effective-rank-compression"
sys.path[:0] = [str(ROOT / "src"), str(RH58 / "experiments"), str(RH77 / "experiments")]

from edge_cloud_transport import cloud_transport_data, ordered_edge_indices  # noqa: E402
from run_effective_rank_audit import build_models  # noqa: E402
from run_schur_fusion_pilot import coarse_embedding  # noqa: E402


SIGMAS = (0.04, 0.02, 0.01)
RANKS = (2, 4, 6, 8, 12, 16, 24, 32)
ANGLE_GATE = 0.5


def run() -> dict[str, object]:
    spectra = {}
    for sigma in SIGMAS:
        _, models = build_models(sigma)
        for model in models:
            values, left, right = eig(np.asarray(model["operator"]), left=True, right=True, check_finite=False)
            spectra[(sigma, str(model["side"]))] = {"values": values, "left": left, "right": right}

    case_rows = []
    for coarse_sigma, fine_sigma in zip(SIGMAS[:-1], SIGMAS[1:]):
        for side in ("left", "right"):
            coarse = spectra[(coarse_sigma, side)]
            fine = spectra[(fine_sigma, side)]
            embedding = coarse_embedding(fine["right"].shape[0])
            rank_rows = []
            for rank in RANKS:
                coarse_indices = ordered_edge_indices(coarse["values"], rank)
                fine_indices = ordered_edge_indices(fine["values"], rank)
                right_data = cloud_transport_data(coarse["right"][:, coarse_indices], fine["right"][:, fine_indices], embedding)
                left_data = cloud_transport_data(coarse["left"][:, coarse_indices], fine["left"][:, fine_indices], embedding)
                joint = max(float(right_data["maximum_principal_sine"]), float(left_data["maximum_principal_sine"]))
                rank_rows.append({
                    "rank": rank,
                    "right_transport": right_data,
                    "left_transport": left_data,
                    "joint_maximum_principal_sine": joint,
                    "two_sided_angle_gate": joint < ANGLE_GATE,
                })
            best = min(rank_rows, key=lambda row: row["joint_maximum_principal_sine"])
            quartet = next(row for row in rank_rows if row["rank"] == 4)
            case_rows.append({
                "coarse_sigma": coarse_sigma,
                "fine_sigma": fine_sigma,
                "side": side,
                "best_rank": best["rank"],
                "best_joint_maximum_principal_sine": best["joint_maximum_principal_sine"],
                "quartet_joint_maximum_principal_sine": quartet["joint_maximum_principal_sine"],
                "green_rank_count": sum(bool(row["two_sided_angle_gate"]) for row in rank_rows),
                "rank_rows": rank_rows,
            })
    all_rank_rows = [row for case in case_rows for row in case["rank_rows"]]
    expanded_rows = [row for row in all_rank_rows if int(row["rank"]) > 4]
    return {
        "status": "rh209_expanding_edge_cloud_transport_obstruction",
        "angle_gate": ANGLE_GATE,
        "rank_grid": list(RANKS),
        "adjacent_case_count": len(case_rows),
        "rank_case_count": len(all_rank_rows),
        "two_sided_green_rank_case_count": sum(bool(row["two_sided_angle_gate"]) for row in all_rank_rows),
        "expanded_two_sided_green_count": sum(bool(row["two_sided_angle_gate"]) for row in expanded_rows),
        "minimum_joint_maximum_principal_sine": min(float(row["joint_maximum_principal_sine"]) for row in all_rank_rows),
        "maximum_expanded_joint_maximum_principal_sine": max(float(row["joint_maximum_principal_sine"]) for row in expanded_rows),
        "best_rank_distribution": {str(rank): sum(int(case["best_rank"]) == rank for case in case_rows) for rank in RANKS},
        "case_rows": case_rows,
        "theorem_boundary": {
            "finite_rank_grid_audit": True,
            "modulus_selected_cloud_growth_tested": True,
            "principal_angle_nonmonotonicity_observed": True,
            "simple_cloud_enlargement_repairs_transport": False,
            "adaptive_nonmodulus_cloud_ruled_out": False,
            "all_level_cloud_obstruction": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/expanding_cloud_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "rank_cases": payload["rank_case_count"],
        "green": payload["two_sided_green_rank_case_count"],
        "expanded_green": payload["expanded_two_sided_green_count"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
