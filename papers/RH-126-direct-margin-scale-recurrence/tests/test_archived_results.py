import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'results'/n).read_text())
def test_audit():
 s=load('direct_margin_audit.json')['audit_summary'];assert s['pair_count']==96;assert s['endpoint_dominance_failure_count']==0;assert s['full_profile_dominance_failure_count']==0;assert s['endpoint_positive_pair_count']==26;assert s['full_profile_positive_pair_count']==6;assert s['positive_terminal_chain_count']==0
def test_smoke_boundary():
 assert load('direct_margin_smoke.json')['audit_summary']['pair_count']==4;b=load('direct_margin_audit.json')['theorem_boundary'];assert b['sharp_direct_margin_recurrence'];assert b['five_scale_profile_barrier_audited'];assert not b['all_level_scale_alignment_proved']
