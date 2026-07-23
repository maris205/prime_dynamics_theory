from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n:str):return json.loads((ROOT/'results'/n).read_text())
def test_counts_and_filter()->None:
 a=load('composite_gate_audit.json');s=a['audit_summary'];assert (s['scale_count'],s['channel_count'],s['update_count'],s['fine_update_count'])==(5,10,360,234);assert s['dominance_failure_count']==0;assert s['diagnostic_exact_dominance_failure_count']==3;assert s['composite_support_count']==321
 expected={'1e-08':(113,114,114,115),'1e-06':(109,109,109,109),'1e-04':(98,98,98,98)}
 for key,c in expected.items():r=a['threshold_summary'][key];assert (r['candidate_support_counts']['direct_weyl'],r['candidate_support_counts']['psd_packet_block'],r['composite_support_count'],r['diagnostic_exact_support_count'])==c
def test_boundary()->None:
 b=load('composite_gate_audit.json')['theorem_boundary'];assert b['factorized_capacity_gate'];assert b['monotone_composite_gate'];assert not b['cross_assembly_exact_directional_admitted'];assert not b['uniform_stage_A_closed']
def test_smoke()->None:assert load('composite_gate_smoke.json')['audit_summary']['update_count']==24
