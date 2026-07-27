"""Audit exact transverse bounds and finite dual-channel decomposition."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from transverse_quenching import (  # noqa: E402
    axial_transverse_path_decomposition,
    coefficient_jacobian,
    transverse_difference,
    transverse_lipschitz_bound,
)


def run() -> dict[str, object]:
    source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    endpoint = {(float(row["sigma"]), str(row["side"])): row for row in source["shape_rows"]}
    sigmas = sorted({key[0] for key in endpoint}, reverse=True)
    sensitivity_rows = []
    for sigma in sigmas:
        for side in ("left", "right"):
            row = endpoint[(sigma, side)]
            jacobian = coefficient_jacobian(float(row["u"]), float(row["eta"]))
            axial_norm = float(np.linalg.norm(jacobian[:, 0]))
            transverse_norm = float(np.linalg.norm(jacobian[:, 1]))
            sensitivity_rows.append({
                "sigma": sigma,
                "side": side,
                "u": float(row["u"]),
                "eta": float(row["eta"]),
                "axial_jacobian_norm": axial_norm,
                "transverse_jacobian_norm": transverse_norm,
                "transverse_to_axial_ratio": transverse_norm / axial_norm,
                "uniform_transverse_lipschitz_bound": transverse_lipschitz_bound(float(row["u"])),
            })
    channel_rows = []
    for sigma in sigmas:
        left = endpoint[(sigma, "left")]
        right = endpoint[(sigma, "right")]
        decomposition = axial_transverse_path_decomposition(
            float(left["u"]), float(left["eta"]), float(right["u"]), float(right["eta"])
        )
        bound = transverse_lipschitz_bound(float(right["u"])) * abs(float(left["eta"]) - float(right["eta"]))
        channel_rows.append({
            "sigma": sigma,
            "u_discrepancy": float(abs(float(left["u"]) - float(right["u"]))),
            "eta_discrepancy": float(abs(float(left["eta"]) - float(right["eta"]))),
            "transverse_bound": bound,
            "transverse_bound_slack": bound - decomposition["transverse_leg_norm"],
            **decomposition,
        })
    rng = np.random.default_rng(217)
    bound_rows = []
    for case in range(800):
        u = float(rng.uniform(0.0, 1.0))
        first = float(rng.uniform(-1.0, 1.0))
        second = float(rng.uniform(-1.0, 1.0))
        actual = transverse_difference(max(u, 1.0e-12), first, second)
        bound = transverse_lipschitz_bound(u) * abs(first - second)
        bound_rows.append({"case": case, "bound_violation": max(0.0, actual - bound)})
    mature = [row for row in sensitivity_rows if row["sigma"] <= 0.02]
    coarsest_mature = [row for row in mature if row["sigma"] == 0.02]
    finest = [row for row in mature if row["sigma"] == min(sigmas)]
    return {
        "status": "rh217_transverse_shape_quenching",
        "sensitivity_rows": sensitivity_rows,
        "channel_decomposition_rows": channel_rows,
        "random_bound_case_count": len(bound_rows),
        "maximum_random_bound_violation": max(row["bound_violation"] for row in bound_rows),
        "maximum_telescoping_residual": max(row["telescoping_residual"] for row in channel_rows),
        "coarsest_mature_maximum_transverse_ratio": max(row["transverse_to_axial_ratio"] for row in coarsest_mature),
        "finest_maximum_transverse_ratio": max(row["transverse_to_axial_ratio"] for row in finest),
        "finest_maximum_channel_transverse_leg": max(
            row["transverse_leg_norm"] for row in channel_rows if row["sigma"] == min(sigmas)
        ),
        "theorem_boundary": {
            "transverse_lipschitz_quenching_exact": True,
            "axial_sensitivity_remains_nonzero": True,
            "finite_channel_decomposition": True,
            "eta_has_a_limit": False,
            "u_tends_to_one": False,
            "one_dimensional_flow_theorem": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/transverse_quenching_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "bound_violation": payload["maximum_random_bound_violation"],
        "mature_ratio": payload["coarsest_mature_maximum_transverse_ratio"],
        "finest_ratio": payload["finest_maximum_transverse_ratio"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
