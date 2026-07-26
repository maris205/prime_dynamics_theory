"""Numerical check of the RH-163 block resolvent inequalities."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from schur_packet import scalar_block_norm  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(163)
    failures = 0
    maximum_ratio = 0.0
    accepted = 0
    for _ in range(512):
        p, q = 3, 4
        x = np.diag(rng.uniform(0.2, 1.0, p)).astype(complex)
        y = np.diag(rng.uniform(0.2, 1.0, q)).astype(complex)
        b = rng.normal(size=(p, q))
        c = rng.normal(size=(q, p))
        b *= rng.uniform(0.0, 0.6) / max(np.linalg.norm(b, 2), 1e-15)
        c *= rng.uniform(0.0, 0.6) / max(np.linalg.norm(c, 2), 1e-15)
        a_norm = np.linalg.norm(x, 2)
        d_norm = np.linalg.norm(y, 2)
        b_norm = np.linalg.norm(b, 2)
        c_norm = np.linalg.norm(c, 2)
        kappa = a_norm * d_norm * b_norm * c_norm
        if kappa >= 0.9:
            continue
        accepted += 1
        r0 = np.block([[x, np.zeros((p, q))], [np.zeros((q, p)), y]])
        # X and Y are block resolvents; invert them to synthesize z-A0 at z=0.
        z_minus_a = np.block([[np.linalg.inv(x), -b], [-c, np.linalg.inv(y)]])
        full = np.linalg.inv(z_minus_a)
        actual = np.linalg.norm(full - r0, 2)
        scalar = np.array([
            [a_norm * kappa, a_norm * b_norm * d_norm],
            [d_norm * c_norm * a_norm, d_norm * kappa],
        ]) / (1.0 - kappa)
        upper = scalar_block_norm(*scalar.ravel())
        failures += int(actual > upper * (1.0 + 1e-11) + 1e-12)
        maximum_ratio = max(maximum_ratio, actual / upper if upper else 0.0)
    payload = {
        "status": "rh163_two_sided_schur_audit",
        "sample_count": 512,
        "accepted_count": accepted,
        "failure_count": failures,
        "maximum_actual_to_upper_ratio": maximum_ratio,
        "imbalanced_witness": {
            "a": 1.0,
            "d": 1.0,
            "b": 10.0,
            "c": 0.01,
            "feedback_product": 0.1,
            "symmetric_neumann_product": 10.0,
        },
        "theorem_boundary": {
            "schur_feedback_certificate": True,
            "physical_contour_bounds": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "schur_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "accepted": accepted, "failures": failures}, sort_keys=True))


if __name__ == "__main__":
    main()
