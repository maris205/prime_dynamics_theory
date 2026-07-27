"""Construct exact endpoint shell maps and audit their non-predictive cost."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
sys.path.insert(0, str(ROOT / "src"))

from procrustes_shell import optimal_shell_map, procrustes_residual_from_cosines  # noqa: E402


def random_isometry(rng: np.random.Generator, rows: int, columns: int) -> np.ndarray:
    raw = rng.normal(size=(rows, columns)) + 1j * rng.normal(size=(rows, columns))
    return np.linalg.qr(raw, mode="reduced")[0]


def run() -> dict[str, object]:
    rng = np.random.default_rng(205)
    identity_rows = []
    for case in range(80):
        rank = 2 + case % 4
        coarse_dimension = rank + 3
        fine_dimension = coarse_dimension + 4
        coarse = random_isometry(rng, coarse_dimension, rank)
        fine = random_isometry(rng, fine_dimension, rank)
        embedding = random_isometry(rng, fine_dimension, coarse_dimension)
        result = optimal_shell_map(coarse, fine, embedding)
        transport = np.asarray(result["transport"])
        coarse_projector = coarse @ coarse.conj().T
        fine_projector = fine @ fine.conj().T
        identity_rows.append({
            "case": case,
            "initial_projector_error": float(np.linalg.norm(transport.conj().T @ transport - coarse_projector, 2)),
            "terminal_projector_error": float(np.linalg.norm(transport @ transport.conj().T - fine_projector, 2)),
            "reported_residual_error": float(abs(result["actual_frobenius_residual"] - result["optimal_frobenius_residual"])),
        })

    inherited = json.loads((RH202 / "results/adjacent_transport_audit.json").read_text(encoding="utf-8"))
    physical_rows = []
    for record in inherited["records"]:
        row = {
            "side": record["side"],
            "coarse_sigma": record["coarse_sigma"],
            "fine_sigma": record["fine_sigma"],
            "maximum_eigenvalue_displacement": max(float(mode["eigenvalue_displacement"]) for mode in record["modes"]),
            "natural_oblique_projector_defect": record["relative_oblique_projector_transport_defect"],
        }
        for kind in ("right", "left"):
            cosines = record[f"{kind}_subspace_transport"]["principal_cosines"]
            row[f"{kind}_procrustes"] = procrustes_residual_from_cosines(np.asarray(cosines))
        physical_rows.append(row)
    audit_values = [value for row in identity_rows for key, value in row.items() if key.endswith("error")]
    return {
        "status": "rh205_endpoint_procrustes_shell_map",
        "identity_case_count": len(identity_rows),
        "identity_failure_count": sum(value > 1e-10 for value in audit_values),
        "maximum_identity_error": max(audit_values),
        "physical_case_count": len(physical_rows),
        "maximum_right_rank_normalized_procrustes_residual": max(float(row["right_procrustes"]["rank_normalized_residual"]) for row in physical_rows),
        "maximum_left_rank_normalized_procrustes_residual": max(float(row["left_procrustes"]["rank_normalized_residual"]) for row in physical_rows),
        "minimum_right_rank_normalized_procrustes_residual": min(float(row["right_procrustes"]["rank_normalized_residual"]) for row in physical_rows),
        "minimum_left_rank_normalized_procrustes_residual": min(float(row["left_procrustes"]["rank_normalized_residual"]) for row in physical_rows),
        "maximum_spectral_intertwining_floor": max(float(row["maximum_eigenvalue_displacement"]) for row in physical_rows),
        "identity_rows": identity_rows,
        "physical_rows": physical_rows,
        "theorem_boundary": {
            "optimal_partial_isometry_formula": True,
            "exact_endpoint_packet_map": True,
            "finite_physical_procrustes_cost": True,
            "map_determined_without_fine_endpoint": False,
            "predictive_interlevel_transport": False,
            "all_level_shell_map": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/procrustes_shell_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "identity_failures": payload["identity_failure_count"],
        "right_cost_max": payload["maximum_right_rank_normalized_procrustes_residual"],
        "left_cost_max": payload["maximum_left_rank_normalized_procrustes_residual"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
