import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'results'/n).read_text())
def test_audit():
 s=load('outward_guard_audit.json')['audit_summary'];assert s['sample_count']==4096;assert s['certified_count']==4096;assert s['false_certification_count']==0;assert s['sharp_gram_error']<1e-12;assert s['sharp_tail_error']<1e-12
def test_smoke_boundary():
 assert load('outward_guard_smoke.json')['audit_summary']['sample_count']==128;b=load('outward_guard_audit.json')['theorem_boundary'];assert b['outward_loewner_guard_theorem'];assert b['guard_sharpness'];assert not b['all_level_roundoff_radii_proved']

