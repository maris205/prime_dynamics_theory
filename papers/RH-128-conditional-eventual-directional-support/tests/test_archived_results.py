import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'results'/n).read_text())
def test_audit():
 s=load('eventual_support_audit.json')['audit_summary'];assert s['sample_count']==4096;assert s['recurrence_failure_count']==0;assert s['support_floor_failure_count']==0;assert s['sharp_relative_error']<1e-10
def test_smoke_boundary():
 assert load('eventual_support_smoke.json')['audit_summary']['sample_count']==128;b=load('eventual_support_audit.json')['theorem_boundary'];assert b['conditional_eventual_support_theorem'];assert b['sharp_constant_coefficient_floor'];assert not b['physical_recurrence_packet_proved']

