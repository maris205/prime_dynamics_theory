import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_archived_smoke_pilot_when_present():
    output = ROOT / "results" / "factor_aware_transfer_pilot_smoke.json"
    if not output.exists():
        subprocess.run(
            [sys.executable, "experiments/run_factor_aware_pilot.py", "--smoke"],
            cwd=ROOT,
            check=True,
        )
    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["status"] == "binary64_factor_aware_sparse_full_intrinsic_transfer_audit"
    assert len(data["rows"]) == 2
    assert data["extrema"]["all_factor_bounds_dominate_actual"]
    assert data["extrema"]["all_transferred_blocks_contract"]
    for row in data["rows"]:
        assert [item["cutoff_multiple"] for item in row["comparisons"]] == [
            5.0,
            6.0,
            8.0,
        ]
        for comparison in row["comparisons"]:
            for side in ("left", "right"):
                assert comparison[side]["actual_block_power_defect"] <= (
                    comparison[side]["semigroup_telescope_upper"]
                    * (1.0 + 1.0e-8)
                    + 1.0e-14
                )
