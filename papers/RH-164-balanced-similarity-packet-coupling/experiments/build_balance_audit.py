"""Audit the exact off-diagonal norm and scalar balance optimum."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from balanced_coupling import balance_data  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(164)
    norm_failures = 0
    optimum_failures = 0
    maximum_norm_error = 0.0
    for _ in range(512):
        b = rng.normal(size=(3, 5))
        c = rng.normal(size=(5, 3))
        bn = np.linalg.norm(b, 2)
        cn = np.linalg.norm(c, 2)
        data = balance_data(bn, cn)
        t = float(data["optimal_scale"])
        e = np.block([[np.zeros((3, 3)), t * b], [c / t, np.zeros((5, 5))]])
        exact = np.linalg.norm(e, 2)
        predicted = max(t * bn, cn / t)
        maximum_norm_error = max(maximum_norm_error, abs(exact - predicted))
        norm_failures += int(abs(exact - predicted) > 2e-12)
        nearby = [max((t * factor) * bn, cn / (t * factor)) for factor in (0.5, 0.8, 1.2, 2.0)]
        optimum_failures += int(any(value < predicted - 2e-12 for value in nearby))
    payload = {
        "status": "rh164_balanced_similarity_audit",
        "sample_count": 512,
        "norm_identity_failure_count": norm_failures,
        "local_optimum_failure_count": optimum_failures,
        "maximum_absolute_norm_error": maximum_norm_error,
        "theorem_boundary": {
            "optimal_scalar_similarity": True,
            "original_norm_condition_penalty": True,
            "physical_scale_balance": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "balance_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "failures": norm_failures + optimum_failures}, sort_keys=True))


if __name__ == "__main__":
    main()
