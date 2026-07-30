import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
from calkin_no_go import fixed_rank_contour_compatible, hardy_lower  # noqa: E402


def main() -> None:
    atlas = json.loads((PAPERS / "RH-222-rank-growing-conjugate-cloud-atlas/results/cloud_atlas.json").read_text())
    ranks = [int(row["actual_rank"]) + 2 for row in atlas["endpoint_rows"]]
    payload = {
        "status": "rh277_fixed_rank_calkin_quotient_contraction_obstruction",
        "hardy_power_lowers": {str(m): hardy_lower(m) for m in (1, 2, 4, 8, 12)},
        "archived_total_selected_rank_min": min(ranks),
        "archived_total_selected_rank_max": max(ranks),
        "single_fixed_rank_contour_compatible": fixed_rank_contour_compatible(ranks),
        "rank_growing_selector_excluded": False,
        "gate_A": False,
    }
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/result.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"rank_range": [min(ranks), max(ranks)]}))


if __name__ == "__main__":
    main()
