"""Random audit of the exact source-cyclic reduction identities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from source_cyclic import (  # noqa: E402
    moment_sequence,
    reduced_moment_sequence,
    source_cyclic_arnoldi,
    synthesis_inclusion_defect,
)


def run() -> dict[str, object]:
    rng = np.random.default_rng(193)
    records = []
    for dimension in range(2, 9):
        for width in range(1, 5):
            for trial in range(5):
                eigenvalues = np.linspace(-0.75, 0.8, dimension) + 0.01j * np.arange(dimension)
                similarity = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
                while np.linalg.cond(similarity) > 30.0:
                    similarity = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
                operator = similarity @ np.diag(eigenvalues) @ np.linalg.inv(similarity)
                source = rng.normal(size=(dimension, width)) + 1j * rng.normal(size=(dimension, width))
                observation = rng.normal(size=(dimension, width)) + 1j * rng.normal(size=(dimension, width))
                data = source_cyclic_arnoldi(operator, source, tolerance=2e-11)
                basis = np.asarray(data["basis"])
                reduced = np.asarray(data["reduced_operator"])
                coordinate = np.asarray(data["source_coordinate"])
                full_moments = moment_sequence(operator, source, observation, 2 * dimension)
                reduced_moments = reduced_moment_sequence(basis, reduced, coordinate, observation, 2 * dimension)
                states = []
                state = source
                for _ in range(min(5, dimension)):
                    states.append(state.reshape(-1))
                    state = operator @ state
                synthesis = np.column_stack(states)
                intertwining = np.column_stack([
                    (operator @ basis[:, j].reshape(source.shape)).reshape(-1)
                    for j in range(basis.shape[1])
                ]) - basis @ reduced
                scale = max(1.0, float(np.max(np.abs(full_moments))))
                record = {
                    "dimension": dimension,
                    "width": width,
                    "trial": trial,
                    "cyclic_dimension": int(data["dimension"]),
                    "closed": bool(data["closed"]),
                    "orthogonality_defect": float(data["orthogonality_defect"]),
                    "relative_intertwining_defect": float(np.linalg.norm(intertwining, 2) / max(1.0, np.linalg.norm(operator, 2))),
                    "relative_moment_error": float(np.max(np.abs(full_moments - reduced_moments)) / scale),
                    "synthesis_inclusion_defect": synthesis_inclusion_defect(basis, synthesis),
                }
                record["passed"] = (
                    record["closed"]
                    and record["cyclic_dimension"] == dimension
                    and record["orthogonality_defect"] < 1e-10
                    and record["relative_intertwining_defect"] < 1e-9
                    and record["relative_moment_error"] < 1e-8
                    and record["synthesis_inclusion_defect"] < 1e-9
                )
                records.append(record)
    return {
        "status": "rh193_source_cyclic_identity_audit",
        "case_count": len(records),
        "failure_count": sum(not bool(item["passed"]) for item in records),
        "maximum_orthogonality_defect": max(float(item["orthogonality_defect"]) for item in records),
        "maximum_relative_intertwining_defect": max(float(item["relative_intertwining_defect"]) for item in records),
        "maximum_relative_moment_error": max(float(item["relative_moment_error"]) for item in records),
        "maximum_synthesis_inclusion_defect": max(float(item["synthesis_inclusion_defect"]) for item in records),
        "records": records,
        "theorem_boundary": {
            "source_cyclic_invariance": True,
            "dimension_at_most_base_dimension": True,
            "temporal_packet_inclusion": True,
            "all_source_observation_moments_preserved": True,
            "physical_uniform_dimension_bound": False,
            "canonical_all_level_quotient": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/source_cyclic_identity_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["case_count"],
        "failures": payload["failure_count"],
        "max_moment_error": payload["maximum_relative_moment_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
