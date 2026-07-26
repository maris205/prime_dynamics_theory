"""Join RH-15 cloud degrees to the RH-82/RH-151 half-log rank clock."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH15 = PAPERS / "RH-15-parity-extracted-bulk-scattering"
RH82 = PAPERS / "RH-82-half-log-postblock-rank-clock"
RH151 = PAPERS / "RH-151-ky-fan-reset-packet-atlas"
sys.path[:0] = [str(ROOT / "src"), str(RH82 / "src")]

from clock_cycle_calibration import cycle_clock_translation  # noqa: E402
from half_log_rank import clock_rank, half_log_clock  # noqa: E402


def run(smoke: bool) -> dict[str, object]:
    with (RH15 / "results/cloud_summary.csv").open(newline="", encoding="utf-8") as stream:
        cloud_rows = list(csv.DictReader(stream))
    if smoke:
        cloud_rows = cloud_rows[:2]
    reset = json.loads((RH151 / "results/reset_packet_audit.json").read_text(encoding="utf-8"))
    actual_ranks = {float(row["sigma"]): int(row["clock_rank"]) for row in reset["rows"]}
    rows = []
    for source in cloud_rows:
        sigma = float(source["sigma"])
        degree = int(source["effective_cloud_degree"])
        clock = half_log_clock(sigma)
        translated = cycle_clock_translation(clock, degree, rank_offset=2)
        actual = actual_ranks.get(sigma)
        rows.append({
            "sigma": sigma,
            **translated,
            "archived_half_localization_horizon": float(source["half_localization_horizon"]),
            "archived_degree_defect": float(source["degree_defect_from_half_horizon"]),
            "cloud_eigenvalue_count": int(source["cloud_eigenvalue_count"]),
            "formal_clock_rank_check": clock_rank(sigma, offset=2),
            "actual_reset_atlas_rank": actual,
            "actual_reset_overlap": actual is not None,
            "actual_reset_rank_matches_clock": actual is None or actual == translated["clock_rank"],
            "translation_identity_residual": int(translated["rank_cycle_gap"]) - int(translated["translated_rank_cycle_gap"]),
        })
    gaps = sorted({int(row["rank_cycle_gap"]) for row in rows})
    overlap = [row for row in rows if row["actual_reset_overlap"]]
    return {
        "status": "rh179_clock_cycle_cloud_degree_calibration",
        "row_count": len(rows),
        "actual_reset_overlap_count": len(overlap),
        "observed_rank_cycle_gap_values": gaps,
        "minimum_degree_defect": min(float(row["degree_defect"]) for row in rows),
        "maximum_degree_defect": max(float(row["degree_defect"]) for row in rows),
        "translation_identity_failure_count": sum(int(row["translation_identity_residual"]) != 0 for row in rows),
        "actual_reset_rank_mismatch_count": sum(not row["actual_reset_rank_matches_clock"] for row in overlap),
        "rows": rows,
        "theorem_boundary": {
            "integer_clock_cycle_translation": True,
            "seven_row_formal_gap_corridor": True,
            "actual_reset_overlap_rows": len(overlap),
            "asymptotic_cloud_degree_law": False,
            "unique_cycle_calibration": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "clock_cycle_smoke.json" if args.smoke else "clock_cycle_audit.json"
    output = ROOT / "results" / name
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(output.relative_to(ROOT)), "rows": payload["row_count"], "gaps": payload["observed_rank_cycle_gap_values"], "overlap": payload["actual_reset_overlap_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
