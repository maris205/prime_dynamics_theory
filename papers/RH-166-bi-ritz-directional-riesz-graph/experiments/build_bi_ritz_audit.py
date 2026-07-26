"""Audit frame residual identities and directional asymmetry."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from bi_ritz_graph import directional_graph_certificate  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(166)
    identity_failures = 0
    maximum_identity_error = 0.0
    for _ in range(512):
        dimension = 10
        rank = 4
        a = rng.normal(size=(dimension, dimension))
        v, _ = np.linalg.qr(rng.normal(size=(dimension, rank)))
        p = v @ v.T
        q = np.eye(dimension) - p
        h = v.T @ a @ v
        right = np.linalg.norm(a @ v - v @ h, 2)
        left = np.linalg.norm(a.T @ v - v @ h.T, 2)
        outward = np.linalg.norm(q @ a @ p, 2)
        inward = np.linalg.norm(p @ a @ q, 2)
        error = max(abs(right - outward), abs(left - inward))
        maximum_identity_error = max(maximum_identity_error, error)
        identity_failures += int(error > 2e-11)
    examples = []
    for b, c in ((0.1, 0.1), (10.0, 0.001), (0.001, 10.0), (100.0, 0.0)):
        examples.append({"left_residual": b, "right_residual": c, **directional_graph_certificate(1.0, 1.0, 1.0, b, c)})
    payload = {
        "status": "rh166_bi_ritz_directional_graph_audit",
        "sample_count": 512,
        "identity_failure_count": identity_failures,
        "maximum_identity_error": maximum_identity_error,
        "directional_examples": examples,
        "theorem_boundary": {
            "bi_ritz_residual_identity": True,
            "directional_graph_bounds": True,
            "physical_transfer_space_residuals": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "bi_ritz_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "failures": identity_failures}, sort_keys=True))


if __name__ == "__main__":
    main()
