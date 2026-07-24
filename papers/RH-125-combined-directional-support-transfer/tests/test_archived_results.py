import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'results'/n).read_text())
def test_audit():
 s=load('combined_transfer_audit.json')['audit_summary'];assert s['pair_count']==96;assert s['chain_count']==24;assert s['one_step_dominance_failure_count']==0;assert s['chain_dominance_failure_count']==0;assert s['nonzero_transfer_count']==96;assert s['terminal_above_1e-8_count']==24
def test_smoke_boundary():
 s=load('combined_transfer_smoke.json')['audit_summary'];assert s['pair_count']==4;assert s['chain_count']==4;b=load('combined_transfer_audit.json')['theorem_boundary'];assert b['combined_directional_transfer_theorem'];assert b['five_scale_regularized_chain_audited'];assert not b['physical_all_level_recurrence_proved']

