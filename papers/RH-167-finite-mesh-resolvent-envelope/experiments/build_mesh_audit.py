"""Dense-grid audit of the finite-mesh resolvent envelope."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from mesh_resolvent import circle_covering_radius, sampled_resolvent_envelope  # noqa: E402


def resolvent_norm(matrix: np.ndarray, z: complex) -> float:
    singular = np.linalg.svd(z * np.eye(matrix.shape[0]) - matrix, compute_uv=False)
    return float(1.0 / singular[-1])


def main() -> None:
    rng = np.random.default_rng(167)
    failures = 0
    accepted = 0
    maximum_actual_to_upper_ratio = 0.0
    for _ in range(256):
        dimension = 5
        matrix = np.triu(rng.normal(size=(dimension, dimension)))
        matrix *= rng.uniform(0.05, 0.35) / np.linalg.norm(matrix, 2)
        radius = rng.uniform(1.0, 1.8)
        node_count = int(rng.integers(20, 65))
        nodes = radius * np.exp(2j * np.pi * np.arange(node_count) / node_count)
        samples = [resolvent_norm(matrix, z) for z in nodes]
        h = circle_covering_radius(radius, node_count)
        result = sampled_resolvent_envelope(samples, h)
        if not result["mesh_certified"]:
            continue
        accepted += 1
        dense = radius * np.exp(2j * np.pi * np.arange(2048) / 2048)
        actual = max(resolvent_norm(matrix, z) for z in dense)
        upper = float(result["continuous_resolvent_upper"])
        maximum_actual_to_upper_ratio = max(maximum_actual_to_upper_ratio, actual / upper)
        failures += int(actual > upper * (1.0 + 1e-11) + 1e-12)
    payload = {
        "status": "rh167_finite_mesh_resolvent_audit",
        "trial_count": 256,
        "accepted_count": accepted,
        "failure_count": failures,
        "maximum_dense_resolvent_to_envelope_ratio": maximum_actual_to_upper_ratio,
        "theorem_boundary": {
            "finite_mesh_covering_theorem": True,
            "dense_float_audit": True,
            "validated_physical_sample_inverses": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "mesh_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "accepted": accepted, "failures": failures}, sort_keys=True))


if __name__ == "__main__":
    main()
