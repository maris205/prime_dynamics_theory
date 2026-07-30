import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_archived_envelope():
 p=json.loads((ROOT/"results/coefficient_envelope.json").read_text());assert p["clean_envelope_constant"]==48;assert len(p["replays"])==3;assert all(all(r["comparisons"].values()) for r in p["replays"]);assert p["theorem_boundary"]["deterministic_target_all_order_envelope"] is True;assert p["theorem_boundary"]["moving_cloud_uniform_trace_envelope"] is False;assert all(p["theorem_boundary"][f"gate_{x}"] is False for x in "ABCDE")
