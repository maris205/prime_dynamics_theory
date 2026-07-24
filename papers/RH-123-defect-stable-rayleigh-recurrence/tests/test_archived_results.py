import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(n): return json.loads((ROOT/'results'/n).read_text())
def test_audit():
 s=load('defect_recurrence_audit.json')['audit_summary']; assert s['sample_count']==4096; assert s['hypothesis_failure_count']==0; assert s['conclusion_failure_count']==0; assert s['sharp_relative_error']<1e-12
def test_smoke_boundary():
 assert load('defect_recurrence_smoke.json')['audit_summary']['sample_count']==128
 b=load('defect_recurrence_audit.json')['theorem_boundary']; assert b['defect_stable_affine_recurrence']; assert b['scalar_sharpness']; assert not b['uniform_physical_coefficients_proved']

