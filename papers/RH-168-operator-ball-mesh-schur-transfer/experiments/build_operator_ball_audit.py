"""Dense audit of nominal-to-exact operator-ball resolvent transfer."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from operator_ball_transfer import robust_resolvent_envelope  # noqa: E402


def resolvent_norm(matrix: np.ndarray, z: complex) -> float:
    singular = np.linalg.svd(z * np.eye(matrix.shape[0]) - matrix, compute_uv=False)
    return float(1.0 / singular[-1])


def main() -> None:
    rng = np.random.default_rng(168)
    failures = 0
    accepted = 0
    maximum_ratio = 0.0
    for _ in range(256):
        dimension = 5
        nominal = np.triu(rng.normal(size=(dimension, dimension)))
        nominal *= rng.uniform(0.05, 0.25) / np.linalg.norm(nominal, 2)
        perturbation = rng.normal(size=(dimension, dimension))
        eta = rng.uniform(1e-4, 0.015)
        perturbation *= eta / np.linalg.norm(perturbation, 2)
        exact = nominal + perturbation
        radius = rng.uniform(1.0, 1.6)
        node_count = int(rng.integers(24, 65))
        nodes = radius * np.exp(2j * np.pi * np.arange(node_count) / node_count)
        samples = [resolvent_norm(nominal, z) for z in nodes]
        h = 2.0 * radius * np.sin(np.pi / (2.0 * node_count))
        result = robust_resolvent_envelope(samples, h, eta)
        if not result["transfer_certified"]:
            continue
        accepted += 1
        dense = radius * np.exp(2j * np.pi * np.arange(2048) / 2048)
        actual = max(resolvent_norm(exact, z) for z in dense)
        upper = float(result["exact_continuous_resolvent_upper"])
        maximum_ratio = max(maximum_ratio, actual / upper)
        failures += int(actual > upper * (1.0 + 1e-11) + 1e-12)
    payload = {
        "status": "rh168_operator_ball_mesh_transfer_audit",
        "trial_count": 256,
        "accepted_count": accepted,
        "failure_count": failures,
        "maximum_exact_dense_to_upper_ratio": maximum_ratio,
        "theorem_boundary": {
            "joint_mesh_operator_ball_transfer": True,
            "fixed_packet_coupling_inflation": True,
            "diagnostic_float_audit": True,
            "outward_physical_operator_balls": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "operator_ball_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "accepted": accepted, "failures": failures}, sort_keys=True))


if __name__ == "__main__":
    main()
