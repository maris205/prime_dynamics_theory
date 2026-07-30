import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_archived_sharp_law():
 p=json.loads((ROOT/"results/sharp_coefficient_law.json").read_text());assert p["exact_conclusions"]["a_n_over_q_star_n_tends_to_one"];assert p["exact_conclusions"]["critical_absolute_log_series_diverges"];assert p["finite_order_2_to_28_diagnostic"]["row_count"]==27;assert p["theorem_boundary"]["moving_cloud_sharp_rate"] is False;assert all(p["theorem_boundary"][f"gate_{x}"] is False for x in "ABCDE")
