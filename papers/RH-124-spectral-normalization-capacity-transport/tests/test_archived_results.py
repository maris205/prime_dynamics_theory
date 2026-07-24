import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'results'/n).read_text())
def test_audit():
 s=load('spectral_transport_audit.json')['audit_summary'];assert s['sample_count']==4096;assert s['q4_failure_count']==0;assert s['capacity_failure_count']==0;assert s['volume_failure_count']==0;assert s['sharp_failure_count']==0
def test_smoke_boundary():
 assert load('spectral_transport_smoke.json')['audit_summary']['sample_count']==128;b=load('spectral_transport_audit.json')['theorem_boundary'];assert b['two_sided_singular_transport'];assert b['separate_factor_loss_quantified'];assert not b['all_level_gram_comparability_proved']

