"""Finite audit of common-contour Riesz transport for Hermitian pairs."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from riesz_transport import projector_step_bound  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(169)
    failures = 0
    maximum_ratio = 0.0
    stable_count = 0
    for _ in range(512):
        dimension, rank = 8, 3
        eigenvalues = np.concatenate([rng.uniform(-0.3, 0.3, rank), rng.uniform(2.0, 3.0, dimension - rank)])
        q0, _ = np.linalg.qr(rng.normal(size=(dimension, dimension)))
        skew = rng.normal(size=(dimension, dimension))
        skew = skew - skew.T
        epsilon = rng.uniform(1e-5, 5e-3)
        q1, _ = np.linalg.qr(q0 + epsilon * skew @ q0)
        a0 = q0 @ np.diag(eigenvalues) @ q0.T
        a1 = q1 @ np.diag(eigenvalues) @ q1.T
        p0 = q0[:, :rank] @ q0[:, :rank].T
        p1 = q1[:, :rank] @ q1[:, :rank].T
        defect = np.linalg.norm(a1 - a0, 2)
        # Unit circle: exact normal resolvent bound from spectral distance.
        distance = min(np.min(1.0 - np.abs(eigenvalues[:rank])), np.min(np.abs(eigenvalues[rank:]) - 1.0))
        m = 1.0 / distance
        result = projector_step_bound(2.0 * np.pi, m, m, defect)
        actual = np.linalg.norm(p1 - p0, 2)
        upper = float(result["projector_step_upper"])
        maximum_ratio = max(maximum_ratio, actual / upper if upper else 0.0)
        failures += int(actual > upper * (1.0 + 1e-10) + 1e-12)
        stable_count += int(result["stable_range_transport"])
    payload = {
        "status": "rh169_common_coordinate_transport_audit",
        "sample_count": 512,
        "failure_count": failures,
        "stable_range_transport_count": stable_count,
        "maximum_actual_to_upper_ratio": maximum_ratio,
        "theorem_boundary": {
            "common_contour_transport_bound": True,
            "summable_fixed_rank_limit": True,
            "physical_common_coordinates": False,
            "growing_cloud_limit": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "transport_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "failures": failures}, sort_keys=True))


if __name__ == "__main__":
    main()
