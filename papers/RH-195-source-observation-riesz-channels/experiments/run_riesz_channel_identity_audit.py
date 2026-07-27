"""Complex random audit of source-observation Riesz-channel identities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import eig


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from riesz_channels import (  # noqa: E402
    cross_channel_gram,
    normalized_eigenprojector,
    residue_normalized_frames,
    simple_channel_transfer,
    source_observation_channel,
    transfer_value,
)


def run() -> dict[str, object]:
    rng = np.random.default_rng(195)
    records = []
    for dimension in range(2, 10):
        for width in range(1, 5):
            for trial in range(5):
                values = np.linspace(-0.8, 0.75, dimension) + 0.03j * np.arange(dimension)
                similarity = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
                while np.linalg.cond(similarity) > 20.0:
                    similarity = rng.normal(size=(dimension, dimension)) + 1j * rng.normal(size=(dimension, dimension))
                operator = similarity @ np.diag(values) @ np.linalg.inv(similarity)
                source = rng.normal(size=(dimension, width)) + 1j * rng.normal(size=(dimension, width))
                observation = rng.normal(size=(width, dimension)) + 1j * rng.normal(size=(width, dimension))
                computed, left, right = eig(operator, left=True, right=True)
                order = sorted(range(dimension), key=lambda index: (float(computed[index].real), float(computed[index].imag)))
                projectors = [normalized_eigenprojector(right[:, index], left[:, index]) for index in order]
                channels = [source_observation_channel(projector, source, observation) for projector in projectors]
                right_states = [np.asarray(item["right_state"]) for item in channels]
                left_states = [np.asarray(item["left_state"]) for item in channels]
                residues = np.asarray([complex(item["residue"]) for item in channels])
                eigenvalues = np.asarray([computed[index] for index in order])
                gram = cross_channel_gram(right_states, left_states)
                right_frame, left_frame = residue_normalized_frames(right_states, left_states, residues)
                z = 1.7 + 0.9j
                full_transfer = transfer_value(operator, source, observation, z)
                modal_transfer = simple_channel_transfer(eigenvalues, residues, z)
                projector_sum = sum(projectors, np.zeros_like(operator, dtype=complex))
                idempotence = max(float(np.linalg.norm(projector @ projector - projector, 2)) for projector in projectors)
                cross_error = float(np.linalg.norm(gram - np.diag(residues), 2))
                record = {
                    "dimension": dimension,
                    "width": width,
                    "trial": trial,
                    "projector_resolution_error": float(np.linalg.norm(projector_sum - np.eye(dimension), 2)),
                    "maximum_projector_idempotence_error": idempotence,
                    "maximum_pairing_error": max(float(item["pairing_error"]) for item in channels),
                    "cross_channel_diagonal_error": cross_error,
                    "biorthogonality_defect": float(np.linalg.norm(left_frame.conj().T @ right_frame - np.eye(dimension), 2)),
                    "relative_transfer_error": float(abs(full_transfer - modal_transfer) / max(1.0, abs(full_transfer))),
                }
                record["passed"] = max(
                    record["projector_resolution_error"],
                    record["maximum_projector_idempotence_error"],
                    record["maximum_pairing_error"],
                    record["cross_channel_diagonal_error"],
                    record["biorthogonality_defect"],
                    record["relative_transfer_error"],
                ) < 1e-9
                records.append(record)
    keys = [
        "projector_resolution_error",
        "maximum_projector_idempotence_error",
        "maximum_pairing_error",
        "cross_channel_diagonal_error",
        "biorthogonality_defect",
        "relative_transfer_error",
    ]
    return {
        "status": "rh195_source_observation_riesz_channel_identity_audit",
        "case_count": len(records),
        "failure_count": sum(not bool(item["passed"]) for item in records),
        "maxima": {key: max(float(item[key]) for item in records) for key in keys},
        "records": records,
        "theorem_boundary": {
            "source_observation_projector_channels": True,
            "cross_channel_residue_diagonalization": True,
            "simple_pole_transfer_expansion": True,
            "residue_normalized_biorthogonality": True,
            "physical_interval_projectors": False,
            "uniform_residue_lower_bound": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/riesz_channel_identity_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "cases": payload["case_count"],
        "failures": payload["failure_count"],
        "max_transfer_error": payload["maxima"]["relative_transfer_error"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
