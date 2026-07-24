"""Random and sharp-family audit for the RH-120 transfer theorem."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from gauge_rayleigh_transfer import gauge_transfer_certificate  # noqa: E402


def spd(rng: np.random.Generator, condition: float) -> np.ndarray:
    q, _ = np.linalg.qr(rng.normal(size=(4, 4)))
    values = np.geomspace(1.0, condition, 4)
    return q @ np.diag(values) @ q.T


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    count = 128 if args.smoke else 4096
    rng = np.random.default_rng(120120 if args.smoke else 120)
    records = []
    for index in range(count):
        g = spd(rng, 10.0 ** rng.uniform(0.0, 6.0))
        d = spd(rng, 10.0 ** rng.uniform(0.0, 5.0))
        s = rng.normal(size=(4, 4)) + 2.5 * np.eye(4)
        if abs(np.linalg.det(s)) < 1e-3:
            s += np.eye(4)
        a = 10.0 ** rng.uniform(-2.0, 1.0)
        b = 10.0 ** rng.uniform(-2.0, 1.0)
        extra = rng.normal(size=(4, 4))
        gp = a * s.T @ g @ s + 0.1 * extra.T @ extra
        theta = rng.uniform(0.05, 1.0)
        dp = theta * b * s.T @ d @ s
        cert = gauge_transfer_certificate(g, d, gp, dp, s, a, b)
        records.append(
            {
                "index": index,
                "target_gamma": cert["target_gamma"],
                "gamma_upper": cert["gamma_upper"],
                "gamma_efficiency": cert["target_gamma"] / cert["gamma_upper"] if cert["gamma_upper"] else 1.0,
                "target_volume": cert["target_volume"],
                "volume_lower": cert["target_volume_lower"],
                "volume_efficiency": cert["target_volume_lower"] / cert["target_volume"] if cert["target_volume"] else 1.0,
                "gram_hypothesis_holds": cert["gram_hypothesis_holds"],
                "tail_hypothesis_holds": cert["tail_hypothesis_holds"],
                "gamma_conclusion_holds": cert["gamma_conclusion_holds"],
                "volume_conclusion_holds": cert["volume_conclusion_holds"],
            }
        )

    g = np.diag([1.0, 2.0, 4.0, 8.0])
    d = 0.04 * g
    s = np.diag([0.5, 1.5, 2.0, 3.0])
    sharp = gauge_transfer_certificate(g, d, 0.6 * s.T @ g @ s, 1.7 * s.T @ d @ s, s, 0.6, 1.7)
    summary = {
        "sample_count": count,
        "hypothesis_failure_count": sum(not (r["gram_hypothesis_holds"] and r["tail_hypothesis_holds"]) for r in records),
        "gamma_failure_count": sum(not r["gamma_conclusion_holds"] for r in records),
        "volume_failure_count": sum(not r["volume_conclusion_holds"] for r in records),
        "minimum_gamma_efficiency": min(r["gamma_efficiency"] for r in records),
        "maximum_gamma_efficiency": max(r["gamma_efficiency"] for r in records),
        "minimum_volume_efficiency": min(r["volume_efficiency"] for r in records),
        "maximum_volume_efficiency": max(r["volume_efficiency"] for r in records),
        "sharp_gamma_relative_error": abs(sharp["target_gamma"] - sharp["gamma_upper"]) / sharp["gamma_upper"],
        "sharp_volume_relative_error": abs(sharp["target_volume"] - sharp["target_volume_lower"]) / sharp["target_volume"],
    }
    payload = {
        "status": "rh120_gauge_covariant_rayleigh_transfer_audit",
        "records": records,
        "sharp_record": sharp,
        "audit_summary": summary,
        "theorem_boundary": {
            "gauge_covariant_gamma_transfer": True,
            "four_volume_transfer": True,
            "simultaneous_sharpness": True,
            "all_level_physical_gauge_law_proved": False,
            "uniform_stage_A_closed": False,
            "hilbert_polya_operator": False,
            "riemann_hypothesis": False,
        },
        "route_consequence": "A relative tail constant and its four-frame volume can be transported through any invertible cross-level gauge once two Loewner comparisons are known. The theorem is exact and sharp; this audit does not supply a physical all-level gauge comparison.",
    }
    name = "gauge_transfer_smoke.json" if args.smoke else "gauge_transfer_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), **summary}, sort_keys=True))


if __name__ == "__main__":
    main()

