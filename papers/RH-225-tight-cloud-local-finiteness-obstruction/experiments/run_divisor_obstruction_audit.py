"""Audit compact divisor-mass growth in direct cloud coordinates."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH222 = PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas"
sys.path.insert(0, str(ROOT / "src"))

from divisor_obstruction import disk_count, tightness_count_lower  # noqa: E402


EPSILON = 0.25
NORMALIZED_RADIUS = 2.0
RAW_RADIUS = 1.0


def values(payload: dict[str, list[float]]) -> np.ndarray:
    return np.asarray(payload["real"]) + 1j * np.asarray(payload["imag"])


def run() -> dict[str, object]:
    source = json.loads((RH222 / "results/cloud_atlas.json").read_text(encoding="utf-8"))
    rows = []
    for endpoint in source["endpoint_rows"]:
        normalized = values(endpoint["normalized_roots"])
        raw = values(endpoint["selected_roots"])
        rank = int(endpoint["actual_rank"])
        rows.append({
            "sigma": endpoint["sigma"],
            "side": endpoint["side"],
            "rank": rank,
            "tightness_count_lower": tightness_count_lower(rank, EPSILON),
            "normalized_disk_count": disk_count(normalized, NORMALIZED_RADIUS),
            "raw_unit_disk_count": disk_count(raw, RAW_RADIUS),
            "maximum_normalized_modulus": float(np.max(np.abs(normalized))),
            "maximum_raw_modulus": float(np.max(np.abs(raw))),
        })
    channel_rows = []
    for side in ("left", "right"):
        sequence = [row for row in rows if row["side"] == side]
        channel_rows.append({
            "side": side,
            "rank_sequence": [row["rank"] for row in sequence],
            "tightness_lower_sequence": [row["tightness_count_lower"] for row in sequence],
            "normalized_disk_count_sequence": [row["normalized_disk_count"] for row in sequence],
            "raw_unit_disk_count_sequence": [row["raw_unit_disk_count"] for row in sequence],
            "normalized_compact_mass_growth": sequence[-1]["normalized_disk_count"] - sequence[0]["normalized_disk_count"],
            "raw_compact_mass_growth": sequence[-1]["raw_unit_disk_count"] - sequence[0]["raw_unit_disk_count"],
        })
    return {
        "status": "rh225_tight_cloud_local_finiteness_obstruction",
        "epsilon": EPSILON,
        "normalized_certificate_radius": NORMALIZED_RADIUS,
        "raw_audit_radius": RAW_RADIUS,
        "endpoint_count": len(rows),
        "minimum_tightness_count_slack": min(row["normalized_disk_count"] - row["tightness_count_lower"] for row in rows),
        "all_normalized_roots_inside_certificate_disk": all(row["normalized_disk_count"] == row["rank"] for row in rows),
        "all_raw_roots_inside_unit_disk": all(row["raw_unit_disk_count"] == row["rank"] for row in rows),
        "maximum_raw_modulus": max(row["maximum_raw_modulus"] for row in rows),
        "channel_rows": channel_rows,
        "endpoint_rows": rows,
        "theorem_boundary": {
            "tight_rank_growth_precludes_local_finite_direct_divisor": True,
            "direct_normalized_cloud_route_rejected": True,
            "finite_raw_unit_disk_growth_observed": True,
            "reciprocal_fredholm_divisor_rejected": False,
            "all_level_small_noise_obstruction": False,
            "gate_A": False,
        },
    }


def main() -> None:
    payload = run()
    output = ROOT / "results/divisor_obstruction_audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "all_normalized_inside": payload["all_normalized_roots_inside_certificate_disk"],
        "all_raw_inside": payload["all_raw_roots_inside_unit_disk"],
        "maximum_raw_modulus": payload["maximum_raw_modulus"],
        "compact_growth": [row["normalized_compact_mass_growth"] for row in payload["channel_rows"]],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
