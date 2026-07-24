from __future__ import annotations
import argparse,json
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[1];P=R.parent;sys.path.insert(0,str(R/'src'))
from gauge_route_review import minimal_missing_sets  # noqa:E402
ARCHIVES=[
 ('RH-120-gauge-covariant-rayleigh-transfer',lambda s:s['theorem']['gauge_covariant_gamma_transfer']),
 ('RH-121-optimal-gram-gauge-pairing',lambda s:s['audit']['pair_count']==96 and s['audit']['contractive_tail_pair_count']==25),
 ('RH-122-fixed-coordinate-gauge-obstruction',lambda s:s['audit']['log_log_slope']==-1.0),
 ('RH-123-defect-stable-rayleigh-recurrence',lambda s:s['audit']['conclusion_failure_count']==0),
 ('RH-124-spectral-normalization-capacity-transport',lambda s:s['audit']['q4_failure_count']==0),
 ('RH-125-combined-directional-support-transfer',lambda s:s['audit']['chain_count']==24 and s['audit']['terminal_above_1e-8_count']==24),
 ('RH-126-direct-margin-scale-recurrence',lambda s:s['audit']['positive_terminal_chain_count']==0),
 ('RH-127-outward-loewner-transport-guards',lambda s:s['audit']['certified_count']==4096 and s['audit']['false_certification_count']==0),
 ('RH-128-conditional-eventual-directional-support',lambda s:s['audit']['support_floor_failure_count']==0),]
def main():
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');a=p.parse_args();selected=ARCHIVES[:3] if a.smoke else ARCHIVES;checks=[]
 for name,test in selected:
  summary=json.loads((P/name/'results/summary.json').read_text());checks.append({'paper':name,'status':summary['status'],'check_holds':bool(test(summary))})
 rules=[(frozenset({'direct_physical_recurrence'}),'eventual_support'),(frozenset({'trace_concentration_physical_packet'}),'eventual_support'),(frozenset({'directional_gamma_recurrence','directional_base_liminf'}),'eventual_support'),(frozenset({'eventual_support','all_level_outward_radii'}),'validated_independent_support')]
 candidates={'direct_physical_recurrence','trace_concentration_physical_packet','directional_gamma_recurrence','directional_base_liminf','all_level_outward_radii'}
 math=[sorted(x) for x in minimal_missing_sets(set(),rules,'eventual_support',candidates)];valid=[sorted(x) for x in minimal_missing_sets(set(),rules,'validated_independent_support',candidates)]
 layers=[{'number':120,'class':'constructive','result':'sharp gauge-covariant gamma and volume transfer'},{'number':121,'class':'constructive','result':'optimal ordered generalized-eigenframe gauge'},{'number':122,'class':'negative','result':'unbounded fixed-coordinate loss'},{'number':123,'class':'constructive','result':'defect-stable affine gamma recurrence'},{'number':124,'class':'constructive','result':'sharp normalization and capacity exponents'},{'number':125,'class':'synthesis','result':'combined directional candidate and finite chains'},{'number':126,'class':'negative','result':'scalar direct-margin finite barrier'},{'number':127,'class':'constructive','result':'sharp outward Loewner guards'},{'number':128,'class':'synthesis','result':'conditional eventual-support floor'},{'number':129,'class':'synthesis','result':'proof-frontier and revised roadmap'}]
 counts={k:sum(x['class']==k for x in layers) for k in ('constructive','negative','synthesis')};summary={'layer_count':10,'upstream_archive_count':len(checks),'upstream_check_failure_count':sum(not x['check_holds'] for x in checks),'class_counts':counts,'mathematical_frontier_count':len(math),'validated_frontier_count':len(valid),'directional_regularized_chain_count':24,'directional_terminal_above_1e-8_count':24,'direct_positive_terminal_chain_count':0,'outward_random_certification_count':4096}
 payload={'status':'rh129_ten_layer_gauge_recurrence_review_audit','layers':layers,'upstream_checks':checks,'mathematical_frontier':math,'validated_independent_frontier':valid,'audit_summary':summary,'closed_or_held_routes':[{'route':'forced common coordinates','status':'closed sharply by RH-122'},{'route':'unguarded independent assembly fusion','status':'closed as a proof method; RH-127 gives the guard'},{'route':'scalar-profile direct recurrence','status':'finite mechanism held after 0/24 terminal chains'},{'route':'trace-concentration','status':'held pending a new physical trace source law'},{'route':'directional recurrence','status':'primary; algebra conditionally closed, physical packet open'}],'theorem_boundary':{'directional_algebra_conditionally_closed':True,'outward_validation_logic_closed':True,'finite_regularized_directional_chain_positive':True,'simple_direct_scalar_chain_negative':True,'any_all_level_physical_packet_proved':False,'directional_gamma_recurrence_proved_physically':False,'directional_base_liminf_proved_physically':False,'all_level_outward_radii_proved':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'zeta_zero_identification':False,'riemann_hypothesis':False},'route_consequence':'The ten layers close the coordinate, perturbation, normalization, composition, validation, and conditional-limit algebra. The primary directional frontier is now the conjunction of an all-level subunit affine gamma recurrence and a positive normalized-base liminf, plus outward radii for independent assemblies. No physical frontier packet is currently proved.'}
 o=R/'results'/('ten_layer_review_smoke.json' if a.smoke else 'ten_layer_review_audit.json');o.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(o.relative_to(R)),**summary},sort_keys=True))
if __name__=='__main__':main()

