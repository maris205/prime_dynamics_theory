"""Audit exact resolvent and source-channel transport identities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH202 = PAPERS / "RH-202-adjacent-edge-quartet-transport"
sys.path.insert(0, str(ROOT / "src"))

from riesz_transport import channel_transport_decomposition, resolvent_intertwining  # noqa: E402


def random_isometry(rng: np.random.Generator, rows: int, columns: int) -> np.ndarray:
    raw = rng.normal(size=(rows, columns)) + 1j * rng.normal(size=(rows, columns))
    return np.linalg.qr(raw, mode="reduced")[0]


def run() -> dict[str, object]:
    rng = np.random.default_rng(203)
    resolvent_rows = []
    channel_rows = []
    for case in range(120):
        coarse_dimension = 2 + case % 4
        fine_dimension = coarse_dimension + 2
        columns_coarse = 2 + case % 3
        columns_fine = columns_coarse + 2
        coarse = 0.12 * (rng.normal(size=(coarse_dimension, coarse_dimension)) + 1j * rng.normal(size=(coarse_dimension, coarse_dimension)))
        fine = 0.12 * (rng.normal(size=(fine_dimension, fine_dimension)) + 1j * rng.normal(size=(fine_dimension, fine_dimension)))
        row = random_isometry(rng, fine_dimension, coarse_dimension)
        column = random_isometry(rng, columns_fine, columns_coarse)
        z = 2.5 + 0.03j * (case + 1)
        identity = resolvent_intertwining(fine, coarse, row, z)
        resolvent_rows.append({
            "case": case,
            "absolute_identity_residual": identity["absolute_identity_residual"],
        })

        fine_projector = rng.normal(size=(fine_dimension, fine_dimension)) + 1j * rng.normal(size=(fine_dimension, fine_dimension))
        coarse_projector = rng.normal(size=(coarse_dimension, coarse_dimension)) + 1j * rng.normal(size=(coarse_dimension, coarse_dimension))
        fine_source = rng.normal(size=(fine_dimension, columns_fine)) + 1j * rng.normal(size=(fine_dimension, columns_fine))
        coarse_source = rng.normal(size=(coarse_dimension, columns_coarse)) + 1j * rng.normal(size=(coarse_dimension, columns_coarse))
        decomposition = channel_transport_decomposition(
            fine_projector, coarse_projector, fine_source, coarse_source, row, column
        )
        channel_rows.append({
            "case": case,
            "absolute_identity_residual": decomposition["absolute_identity_residual"],
            "actual_transport_norm": float(np.linalg.norm(decomposition["left"], "fro")),
            "triangle_upper_bound": decomposition["triangle_upper_bound"],
        })

    inherited = json.loads((RH202 / "results/adjacent_transport_audit.json").read_text(encoding="utf-8"))
    inherited_rows = [{
        "side": record["side"],
        "coarse_sigma": record["coarse_sigma"],
        "fine_sigma": record["fine_sigma"],
        "full_intertwining_defect": record["full_operator_intertwining_relative_frobenius_defect"],
        "quartet_intertwining_defect": record["quartet_restricted_intertwining_relative_defect"],
        "source_transport_defect": record["source_relative_transport_defect"],
        "projector_transport_defect": record["relative_oblique_projector_transport_defect"],
    } for record in inherited["records"]]
    maximum_resolvent = max(float(row["absolute_identity_residual"]) for row in resolvent_rows)
    maximum_channel = max(float(row["absolute_identity_residual"]) for row in channel_rows)
    return {
        "status": "rh203_riesz_intertwining_transport_budget",
        "resolvent_identity_case_count": len(resolvent_rows),
        "channel_decomposition_case_count": len(channel_rows),
        "maximum_resolvent_identity_residual": maximum_resolvent,
        "maximum_channel_identity_residual": maximum_channel,
        "identity_failure_count": sum(row["absolute_identity_residual"] > 1e-10 for row in resolvent_rows + channel_rows),
        "inherited_transport_rows": inherited_rows,
        "minimum_inherited_quartet_intertwining_defect": min(float(row["quartet_intertwining_defect"]) for row in inherited_rows),
        "maximum_inherited_quartet_intertwining_defect": max(float(row["quartet_intertwining_defect"]) for row in inherited_rows),
        "minimum_inherited_source_transport_defect": min(float(row["source_transport_defect"]) for row in inherited_rows),
        "theorem_boundary": {
            "resolvent_intertwining_identity": True,
            "riesz_projector_transport_identity": True,
            "source_channel_two_term_budget": True,
            "finite_identity_audit": True,
            "physical_resolvent_supremum_bound": False,
            "closed_physical_transport_certificate": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/riesz_transport_identity_audit.json"
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["resolvent_identity_case_count"] + payload["channel_decomposition_case_count"],
        "failures": payload["identity_failure_count"],
        "max_resolvent_residual": payload["maximum_resolvent_identity_residual"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
