from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name:str):return json.loads((ROOT/'results'/name).read_text())
def test_full_audit() -> None:
 a=load('wedge_lipschitz_audit.json');s=a['audit_summary'];assert (s['scale_count'],s['channel_count'],s['update_count'],s['fine_update_count'])==(5,10,360,234);assert s['domination_failure_count']==0;assert s['archived_formula_failure_count']==0;assert s['fine_global_positive_count']<=s['fine_direct_positive_count']
 for row in a['threshold_summary'].values():assert row['fine_global_support_count']<=row['fine_direct_support_count']
def test_sharpness_and_boundary() -> None:
 a=load('wedge_lipschitz_audit.json');assert max(row['error'] for row in a['sharpness_examples'])<1e-15;boundary=a['theorem_boundary'];assert boundary['sharp_global_wedge_lipschitz_bound'];assert boundary['product_weyl_dominates_global_wedge'];assert boundary['global_route_declared_negative'];assert not boundary['directional_wedge_route_ruled_out'];assert not boundary['uniform_stage_A_closed']
def test_smoke() -> None:assert load('wedge_lipschitz_smoke.json')['audit_summary']['update_count']==24
