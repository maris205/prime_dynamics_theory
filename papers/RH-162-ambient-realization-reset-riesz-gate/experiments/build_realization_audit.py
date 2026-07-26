"""Finite audit of the RH-162 realization inequalities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from ambient_realization import realization_coupling_bounds  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(162)
    failures = 0
    maximum_primal_ratio = 0.0
    maximum_adjoint_ratio = 0.0
    records = []
    for trial in range(512):
        h, e, rank = 10, 7, 3
        j, _ = np.linalg.qr(rng.normal(size=(h, e)))
        p = np.diag([1.0] * rank + [0.0] * (e - rank))
        m = np.diag(rng.normal(size=e))
        a = j @ m @ j.T + 0.08 * rng.normal(size=(h, h))
        phat = j @ p @ j.T
        qhat = np.eye(h) - phat
        primal = np.linalg.norm((a @ j - j @ m) @ p, 2)
        adjoint = np.linalg.norm((a.T @ j - j @ m.T) @ p, 2)
        outward = np.linalg.norm(qhat @ a @ phat, 2)
        inward = np.linalg.norm(phat @ a @ qhat, 2)
        bound = realization_coupling_bounds(primal, adjoint)
        failures += int(outward > primal + 1e-11 or inward > adjoint + 1e-11)
        maximum_primal_ratio = max(maximum_primal_ratio, outward / primal)
        maximum_adjoint_ratio = max(maximum_adjoint_ratio, inward / adjoint)
        if trial < 6:
            records.append({
                "trial": trial,
                "outward": outward,
                "outward_upper": bound["packet_to_complement_upper"],
                "inward": inward,
                "inward_upper": bound["complement_to_packet_upper"],
            })
    payload = {
        "status": "rh162_ambient_realization_audit",
        "sample_count": 512,
        "failure_count": failures,
        "maximum_outward_to_primal_ratio": maximum_primal_ratio,
        "maximum_inward_to_adjoint_ratio": maximum_adjoint_ratio,
        "sample_records": records,
        "theorem_boundary": {
            "isometric_realization_coupling_theorem": True,
            "nonidentifiability_without_realization": True,
            "physical_prime_dynamics_realization": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "realization_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "failures": failures}, sort_keys=True))


if __name__ == "__main__":
    main()
