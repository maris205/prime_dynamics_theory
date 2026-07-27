"""Verify the discriminant formula and measure finite boundary approach."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH213 = PAPERS / "RH-213-centered-conjugate-quartet-shape-manifold"
sys.path.insert(0, str(ROOT / "src"))

from shape_boundary import (  # noqa: E402
    boundary_root_distance,
    canonical_roots,
    coefficient_boundary_distance,
    discriminant_formula,
    root_discriminant,
    uniform_boundary_root_bound,
)


def run() -> dict[str, object]:
    source = json.loads((RH213 / "results/shape_manifold_audit.json").read_text(encoding="utf-8"))
    endpoint_rows = []
    for row in source["shape_rows"]:
        u = float(row["u"])
        eta = float(row["eta"])
        distance = boundary_root_distance(u, eta)
        bound = uniform_boundary_root_bound(u)
        endpoint_rows.append({
            "sigma": float(row["sigma"]),
            "side": str(row["side"]),
            "u": u,
            "eta": eta,
            "discriminant": discriminant_formula(u, eta),
            "root_distance_to_double_pm_one": distance,
            "uniform_root_bound": bound,
            "bound_slack": bound - distance,
            "coefficient_distance_to_z2_minus_1_squared": coefficient_boundary_distance(u, eta),
        })
    rng = np.random.default_rng(216)
    identity_rows = []
    for case in range(600):
        u = float(rng.uniform(0.0, 1.0))
        eta = float(rng.uniform(-1.0, 1.0))
        direct = root_discriminant(canonical_roots(u, eta))
        formula = discriminant_formula(u, eta)
        distance = boundary_root_distance(u, eta)
        bound = uniform_boundary_root_bound(u)
        identity_rows.append({
            "case": case,
            "discriminant_absolute_error": float(abs(direct - formula)),
            "discriminant_relative_error": float(abs(direct - formula) / max(1.0, abs(formula))),
            "bound_violation": float(max(0.0, distance - bound)),
        })
    finest = [row for row in endpoint_rows if row["sigma"] == min(item["sigma"] for item in endpoint_rows)]
    return {
        "status": "rh216_degenerate_quartet_boundary_stratification",
        "endpoint_count": len(endpoint_rows),
        "random_identity_case_count": len(identity_rows),
        "maximum_random_discriminant_absolute_error": max(row["discriminant_absolute_error"] for row in identity_rows),
        "maximum_random_discriminant_relative_error": max(row["discriminant_relative_error"] for row in identity_rows),
        "maximum_uniform_bound_violation": max(row["bound_violation"] for row in identity_rows),
        "finest_maximum_root_distance": max(row["root_distance_to_double_pm_one"] for row in finest),
        "finest_maximum_coefficient_distance": max(row["coefficient_distance_to_z2_minus_1_squared"] for row in finest),
        "endpoint_rows": endpoint_rows,
        "identity_rows": identity_rows,
        "theorem_boundary": {
            "discriminant_factorization_exact": True,
            "degeneracy_strata_exact": True,
            "uniform_u_to_one_collapse_exact": True,
            "finite_data_move_toward_axial_boundary": True,
            "u_converges_to_one": False,
            "quartet_limit_exists": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/boundary_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "discriminant_relative_error": payload["maximum_random_discriminant_relative_error"],
        "bound_violation": payload["maximum_uniform_bound_violation"],
        "finest_root_distance": payload["finest_maximum_root_distance"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
