"""Audit the multiplicity burden hidden by the RH-185 Frobenius state type."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
RH185 = PAPERS / "RH-185-physical-bi-krylov-cycle-calibration"
sys.path.insert(0, str(ROOT / "src"))

from frobenius_obstruction import (  # noqa: E402
    complement_count,
    complement_free_compatible,
    riesz_rank,
)


def run(smoke: bool) -> dict[str, object]:
    source_name = "bi_krylov_smoke.json" if smoke else "bi_krylov_audit.json"
    source = json.loads((RH185 / "results" / source_name).read_text(encoding="utf-8"))
    records = []
    for item in source["records"]:
        width = int(item["source_columns"])
        length = int(item["candidate_length"])
        one_root_burden = complement_count(1, 1, width)
        all_root_burden = complement_count(length, length, width)
        records.append({
            "sigma": float(item["sigma"]),
            "side": str(item["side"]),
            "start": int(item["start"]),
            "operator_dimension": int(item["operator_dimension"]),
            "source_columns": width,
            "candidate_length": length,
            "ambient_frobenius_dimension": int(item["operator_dimension"]) * width,
            "one_base_eigenvalue_ambient_riesz_rank": riesz_rank(1, width),
            "one_packet_root_count": 1,
            "one_root_complement_count_if_one_base_mode": one_root_burden,
            "whole_packet_complement_count_if_one_base_mode_per_root": all_root_burden,
            "one_root_complement_free_compatible": complement_free_compatible(1, width),
            "whole_packet_complement_free_compatible": complement_free_compatible(length, width),
        })
    root_case_count = sum(int(item["candidate_length"]) for item in records)
    return {
        "status": "rh192_frobenius_left_multiplication_obstruction",
        "window_count": len(records),
        "root_case_count": root_case_count,
        "source_column_counts": sorted({int(item["source_columns"]) for item in records}),
        "ambient_dimension_range": {
            "minimum": min(int(item["ambient_frobenius_dimension"]) for item in records),
            "maximum": max(int(item["ambient_frobenius_dimension"]) for item in records),
        },
        "one_root_complement_free_compatible_count": sum(bool(item["one_root_complement_free_compatible"]) for item in records),
        "whole_packet_complement_free_compatible_count": sum(bool(item["whole_packet_complement_free_compatible"]) for item in records),
        "one_root_complement_burden_range": {
            "minimum": min(int(item["one_root_complement_count_if_one_base_mode"]) for item in records),
            "maximum": max(int(item["one_root_complement_count_if_one_base_mode"]) for item in records),
        },
        "total_rootwise_complement_burden_if_matched": sum(
            int(item["candidate_length"]) * int(item["one_root_complement_count_if_one_base_mode"])
            for item in records
        ),
        "records": records,
        "theorem_boundary": {
            "left_multiplication_kronecker_equivalence": True,
            "characteristic_polynomial_power_law": True,
            "riesz_rank_multiplicity_law": True,
            "literal_rank_one_or_rank_four_full_frobenius_shell": False,
            "source_cyclic_quotient_obstructed": False,
            "physical_root_matching": False,
            "gate_A": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    payload = run(args.smoke)
    name = "frobenius_obstruction_smoke.json" if args.smoke else "frobenius_obstruction_audit.json"
    output = ROOT / "results" / name
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "output": str(output.relative_to(ROOT)),
        "windows": payload["window_count"],
        "root_cases": payload["root_case_count"],
        "complement_free_windows": payload["whole_packet_complement_free_compatible_count"],
        "burden_range": payload["one_root_complement_burden_range"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
