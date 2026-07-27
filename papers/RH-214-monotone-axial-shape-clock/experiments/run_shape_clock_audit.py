"""Measure the finite axial clock and asymmetry corridor."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from shape_clock import corridor_summary, monotone_clock_summary, paired_channel_summary  # noqa: E402


def run() -> dict[str, object]:
    source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    rows = source["shape_rows"]
    sigmas = sorted({float(row["sigma"]) for row in rows}, reverse=True)
    endpoint = {(float(row["sigma"]), str(row["side"])): row for row in rows}
    channel_summaries = {}
    for side in ("left", "right"):
        u = np.asarray([endpoint[(sigma, side)]["u"] for sigma in sigmas])
        eta = np.asarray([endpoint[(sigma, side)]["eta"] for sigma in sigmas])
        mature = np.asarray([endpoint[(sigma, side)]["eta"] for sigma in sigmas if sigma <= 0.02])
        channel_summaries[side] = {
            "u_clock": monotone_clock_summary(np.asarray(sigmas), u),
            "full_eta_corridor": corridor_summary(eta),
            "mature_eta_corridor_sigma_at_most_0_02": corridor_summary(mature),
            "spearman_clock_correlation": float(np.corrcoef(
                np.argsort(np.argsort(np.log(1.0 / np.asarray(sigmas)))),
                np.argsort(np.argsort(u)),
            )[0, 1]),
        }
    left_u = np.asarray([endpoint[(sigma, "left")]["u"] for sigma in sigmas])
    right_u = np.asarray([endpoint[(sigma, "right")]["u"] for sigma in sigmas])
    left_eta = np.asarray([endpoint[(sigma, "left")]["eta"] for sigma in sigmas])
    right_eta = np.asarray([endpoint[(sigma, "right")]["eta"] for sigma in sigmas])
    mature_mask = np.asarray(sigmas) <= 0.02
    transition_rows = []
    for coarse, fine in zip(sigmas[:-1], sigmas[1:]):
        transition_rows.append({
            "coarse_sigma": coarse,
            "fine_sigma": fine,
            "left_u_increment": float(endpoint[(fine, "left")]["u"] - endpoint[(coarse, "left")]["u"]),
            "right_u_increment": float(endpoint[(fine, "right")]["u"] - endpoint[(coarse, "right")]["u"]),
            "left_eta_increment": float(endpoint[(fine, "left")]["eta"] - endpoint[(coarse, "left")]["eta"]),
            "right_eta_increment": float(endpoint[(fine, "right")]["eta"] - endpoint[(coarse, "right")]["eta"]),
        })
    return {
        "status": "rh214_monotone_axial_shape_clock",
        "scale_count": len(sigmas),
        "transition_count": len(transition_rows),
        "sigmas_coarse_to_fine": sigmas,
        "channel_summaries": channel_summaries,
        "dual_channel_u": paired_channel_summary(left_u, right_u),
        "dual_channel_eta": paired_channel_summary(left_eta, right_eta),
        "mature_dual_channel_u": paired_channel_summary(left_u[mature_mask], right_u[mature_mask]),
        "mature_dual_channel_eta": paired_channel_summary(left_eta[mature_mask], right_eta[mature_mask]),
        "transition_rows": transition_rows,
        "all_u_transitions_strictly_positive": all(
            row["left_u_increment"] > 0.0 and row["right_u_increment"] > 0.0 for row in transition_rows
        ),
        "theorem_boundary": {
            "finite_piecewise_linear_clock_exists": True,
            "sixteen_scale_monotonicity_observed": True,
            "finite_asymmetry_corridor_observed": True,
            "all_scale_monotonicity": False,
            "small_noise_limit": False,
            "autonomous_flow_law": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/shape_clock_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "all_u_positive": payload["all_u_transitions_strictly_positive"],
        "left_eta_width": payload["channel_summaries"]["left"]["mature_eta_corridor_sigma_at_most_0_02"]["width"],
        "u_channel_max": payload["dual_channel_u"]["maximum_absolute_discrepancy"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
