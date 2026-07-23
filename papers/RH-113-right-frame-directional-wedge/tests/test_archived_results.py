from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n:str):return json.loads((ROOT/'results'/n).read_text())
def test_audit_and_counts()->None:
 a=load('directional_wedge_audit.json');s=a['audit_summary'];assert (s['scale_count'],s['channel_count'],s['update_count'],s['fine_update_count'])==(5,10,360,234);assert s['frame_variational_failure_count']==s['leading_upper_failure_count']==s['global_frame_identity_failure_count']==0;assert s['minimum_capture_ratio']>.99999
 expected={'1e-08':(78,78,78,78),'1e-06':(72,72,72,72),'1e-04':(55,55,55,55)}
 for key,counts in expected.items():r=a['threshold_summary'][key];assert (r['fine_global_frame_support_count'],r['fine_restricted_frame_support_count'],r['fine_exact_directional_support_count'],r['fine_actual_spectral_support_count'])==counts
def test_boundary()->None:
 b=load('directional_wedge_audit.json')['theorem_boundary'];assert b['directional_frame_variational_certificate'];assert b['recent_frame_recovers_product_weyl'];assert not b['all_level_directional_tail_law_proved'];assert not b['uniform_stage_A_closed']
def test_smoke()->None:assert load('directional_wedge_smoke.json')['audit_summary']['update_count']==24
