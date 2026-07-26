"""Finite audit of the normal-block midpoint contour theorem."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from midgap_contour import centered_circle_certificate  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(165)
    rank_failures = 0
    resolvent_failures = 0
    maximum_resolvent_ratio = 0.0
    for _ in range(512):
        p, q = 2, 3
        rho = rng.uniform(0.1, 0.8)
        gap = rng.uniform(1.0, 2.5)
        outer = rho + gap
        packet_values = rho * rng.uniform(0.0, 0.95, p) * np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, p))
        complement_values = (outer + rng.uniform(0.0, 1.0, q)) * np.exp(1j * rng.uniform(0.0, 2.0 * np.pi, q))
        ap = np.diag(packet_values)
        aq = np.diag(complement_values)
        b = rng.normal(size=(p, q)) + 1j * rng.normal(size=(p, q))
        c = rng.normal(size=(q, p)) + 1j * rng.normal(size=(q, p))
        bn = np.linalg.norm(b, 2)
        cn = np.linalg.norm(c, 2)
        target_product = rng.uniform(0.0, 0.55) * gap * gap / 4.0
        c *= target_product / max(bn * cn, 1e-15)
        cn = np.linalg.norm(c, 2)
        certificate = centered_circle_certificate(rho, outer, bn, cn)
        radius = float(certificate["midpoint_radius"])
        angles = np.linspace(0.0, 2.0 * np.pi, 1024, endpoint=False)
        actual_a = max(np.linalg.norm(np.linalg.inv(z * np.eye(p) - ap), 2) for z in radius * np.exp(1j * angles))
        actual_d = max(np.linalg.norm(np.linalg.inv(z * np.eye(q) - aq), 2) for z in radius * np.exp(1j * angles))
        upper = 2.0 / gap
        ratio = max(actual_a, actual_d) / upper
        maximum_resolvent_ratio = max(maximum_resolvent_ratio, ratio)
        resolvent_failures += int(ratio > 1.0 + 1e-11)
        full = np.block([[ap, b], [c, aq]])
        count = int(np.sum(np.abs(np.linalg.eigvals(full)) < radius))
        rank_failures += int(not certificate["rank_certified"] or count != p)
    payload = {
        "status": "rh165_midgap_normal_block_audit",
        "sample_count": 512,
        "rank_count_failure_count": rank_failures,
        "resolvent_bound_failure_count": resolvent_failures,
        "maximum_sampled_resolvent_to_upper_ratio": maximum_resolvent_ratio,
        "theorem_boundary": {
            "normal_midgap_optimality": True,
            "normal_gap_feedback_gate": True,
            "physical_block_normality": False,
            "physical_R_interface": False,
            "gate_A": False,
        },
    }
    output = ROOT / "results" / "midgap_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "failures": rank_failures + resolvent_failures}, sort_keys=True))


if __name__ == "__main__":
    main()
