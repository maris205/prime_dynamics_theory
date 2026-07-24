import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def load(n):return json.loads((R/'results'/n).read_text())
def test_audit():
 a=load('ten_layer_review_audit.json');s=a['audit_summary'];assert s['layer_count']==10;assert s['upstream_archive_count']==9;assert s['upstream_check_failure_count']==0;assert s['class_counts']=={'constructive':5,'negative':2,'synthesis':3};assert a['mathematical_frontier']==[['direct_physical_recurrence'],['trace_concentration_physical_packet'],['directional_base_liminf','directional_gamma_recurrence']]
def test_validated_frontier_boundary():
 a=load('ten_layer_review_audit.json');assert all('all_level_outward_radii' in x for x in a['validated_independent_frontier']);b=a['theorem_boundary'];assert b['directional_algebra_conditionally_closed'];assert not b['any_all_level_physical_packet_proved'];assert not b['riemann_hypothesis']
def test_smoke():assert load('ten_layer_review_smoke.json')['audit_summary']['upstream_archive_count']==3

