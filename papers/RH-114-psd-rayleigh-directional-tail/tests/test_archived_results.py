from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n:str):return json.loads((ROOT/'results'/n).read_text())
def test_audit()->None:
 a=load('psd_rayleigh_audit.json');s=a['audit_summary'];assert (s['scale_count'],s['channel_count'],s['update_count'],s['fine_update_count'])==(5,10,360,234);assert s['block_psd_failure_count']==0;assert s['certificate_failure_count']==0
 expected={'1e-08':(78,78,78,78,78),'1e-06':(72,72,72,72,72),'1e-04':(55,55,55,55,55)}
 for key,c in expected.items():r=a['threshold_summary'][key];assert (r['fine_scalar_support_count'],r['fine_block_support_count'],r['fine_exact_relative_support_count'],r['fine_product_support_count'],r['fine_actual_support_count'])==c
def test_boundary()->None:
 b=load('psd_rayleigh_audit.json')['theorem_boundary'];assert b['positive_tail_cross_gram_upper'];assert b['relative_psd_rayleigh_volume_bound'];assert not b['all_level_directional_tail_gram_law_proved'];assert not b['uniform_stage_A_closed']
def test_smoke()->None:assert load('psd_rayleigh_smoke.json')['audit_summary']['update_count']==24
