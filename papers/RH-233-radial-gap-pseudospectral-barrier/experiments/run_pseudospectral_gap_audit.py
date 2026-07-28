"""Compare radial shell gaps with the RH-232 projector norms."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH232 = PAPERS / "RH-232-biorthogonal-riesz-cloud-projection"
sys.path.insert(0, str(ROOT / "src"))

from pseudospectral_gap import power_growth_fit, triangular_projector_norm  # noqa: E402


def run() -> dict[str, object]:
    source = json.loads(
        (RH232 / "results/riesz_projection_audit.json").read_text(encoding="utf-8")
    )
    rows = source["endpoint_rows"]
    fits = {}
    correlations = {}
    for side in ("left", "right"):
        channel = [row for row in rows if row["side"] == side]
        fits[side] = power_growth_fit(
            np.asarray([row["sigma"] for row in channel]),
            np.asarray([row["projector_operator_norm"] for row in channel]),
        )
        correlations[side] = float(np.corrcoef(
            np.log([row["radial_gap_after_cloud"] for row in channel]),
            np.log([row["projector_operator_norm"] for row in channel]),
        )[0, 1])
    model_rows = []
    for coupling in (1.0, 1.0e3, 1.0e6, 1.0e9):
        model_rows.append({
            "first_eigenvalue": 0.8,
            "second_eigenvalue": 0.5,
            "eigenvalue_gap": 0.3,
            "coupling": coupling,
            "projector_operator_norm": triangular_projector_norm(0.8, 0.5, coupling),
        })
    return {
        "status": "rh233_radial_gap_pseudospectral_barrier",
        "endpoint_count": len(rows),
        "minimum_radial_gap": min(row["radial_gap_after_cloud"] for row in rows),
        "maximum_projector_operator_norm": max(row["projector_operator_norm"] for row in rows),
        "minimum_gap_to_projector_norm_ratio": min(
            row["gap_to_projector_norm_ratio"] for row in rows
        ),
        "projector_growth_fits": fits,
        "log_gap_log_projector_correlations": correlations,
        "fixed_gap_model_rows": model_rows,
        "fixed_gap_model_growth_factor": (
            model_rows[-1]["projector_operator_norm"]
            / model_rows[0]["projector_operator_norm"]
        ),
        "theorem_boundary": {
            "fixed_eigenvalue_gap_does_not_bound_projector_norm": True,
            "positive_radial_shell_gap_is_not_a_pseudospectral_certificate": True,
            "rh222_radial_gaps_invalidated": False,
            "uniform_riesz_contour_bound": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/pseudospectral_gap_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "maximum_projector_norm": payload["maximum_projector_operator_norm"],
        "minimum_gap_ratio": payload["minimum_gap_to_projector_norm_ratio"],
        "growth_exponents": {
            side: fit["growth_exponent"]
            for side, fit in payload["projector_growth_fits"].items()
        },
    }, sort_keys=True))


if __name__ == "__main__":
    main()
