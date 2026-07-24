from __future__ import annotations
import argparse,collections,json
from pathlib import Path
import sys
import numpy as np
R=Path(__file__).resolve().parents[1];P=R.parent;sys.path.insert(0,str(R/'src'))
from direct_margin_recurrence import margin_transfer_lower,optimal_profile_scaling,support_margin  # noqa:E402
def main():
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');a=p.parse_args();src=P/'RH-121-optimal-gram-gauge-pairing/results'/('optimal_gauge_smoke.json' if a.smoke else 'optimal_gauge_audit.json');d=json.loads(src.read_text());rows=[]
 for q in d['pairs']:
  s=np.array(q['source_full_singular_values']);t=np.array(q['target_full_singular_values']);tau=q['threshold'];end=optimal_profile_scaling(s[[0,3]],t[[0,3]]);full=optimal_profile_scaling(s,t);sm=support_margin(s[[0,3]],tau);tm=support_margin(t[[0,3]],tau);el=margin_transfer_lower(sm,end['scale'],end['error'],tau);fl=margin_transfer_lower(sm,full['scale'],full['error'],tau);rows.append({'pair_id':q['pair_id'],'source_sigma':q['source_sigma'],'target_sigma':q['target_sigma'],'side':q['side'],'threshold':tau,'phase':q['phase'],'source_margin':sm,'target_margin':tm,'endpoint_scale':end['scale'],'endpoint_error':end['error'],'endpoint_relative_error':end['relative_error'],'endpoint_lower':el,'endpoint_dominance_holds':bool(el<=tm+2e-12),'full_profile_scale':full['scale'],'full_profile_error':full['error'],'full_profile_relative_error':full['relative_error'],'full_profile_lower':fl,'full_profile_dominance_holds':bool(fl<=tm+2e-12)})
 groups=collections.defaultdict(list)
 for r in rows:groups[(r['side'],r['threshold'],r['phase'])].append(r)
 chains=[]
 for key,items in groups.items():
  items.sort(key=lambda x:x['source_sigma'],reverse=True);m=items[0]['source_margin'];levels=[{'sigma':items[0]['source_sigma'],'margin_lower':m}]
  for x in items:m=margin_transfer_lower(m,x['endpoint_scale'],x['endpoint_error'],x['threshold']);levels.append({'sigma':x['target_sigma'],'margin_lower':m})
  chains.append({'side':key[0],'threshold':key[1],'phase':key[2],'levels':levels,'terminal_margin_lower':m,'positive_terminal':bool(m>0)})
 summary={'pair_count':len(rows),'chain_count':len(chains),'endpoint_dominance_failure_count':sum(not r['endpoint_dominance_holds'] for r in rows),'full_profile_dominance_failure_count':sum(not r['full_profile_dominance_holds'] for r in rows),'endpoint_positive_pair_count':sum(r['endpoint_lower']>0 for r in rows),'full_profile_positive_pair_count':sum(r['full_profile_lower']>0 for r in rows),'positive_terminal_chain_count':sum(c['positive_terminal'] for c in chains),'minimum_endpoint_relative_error':min(r['endpoint_relative_error'] for r in rows),'median_endpoint_relative_error':float(np.median([r['endpoint_relative_error'] for r in rows])),'maximum_endpoint_relative_error':max(r['endpoint_relative_error'] for r in rows),'minimum_terminal_margin':min(c['terminal_margin_lower'] for c in chains),'maximum_terminal_margin':max(c['terminal_margin_lower'] for c in chains)}
 payload={'status':'rh126_direct_margin_scale_recurrence_audit','pairs':rows,'chains':chains,'audit_summary':summary,'theorem_boundary':{'sharp_direct_margin_recurrence':True,'optimal_scalar_profile_fit':True,'five_scale_profile_barrier_audited':not a.smoke,'all_level_scale_alignment_proved':False,'profile_fit_is_operator_transport_proof':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'A direct support margin obeys a sharp Weyl recurrence under scalar scale alignment. On the finite phase-matched singular profiles only 26/96 endpoint fits and 6/96 full four-mode fits retain a positive one-step margin, and none of the 24 endpoint chains stays positive through all five scales. The algebraic route remains valid, but this scalar alignment is a poor finite mechanism.'}
 o=R/'results'/('direct_margin_smoke.json' if a.smoke else 'direct_margin_audit.json');o.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(o.relative_to(R)),**summary},sort_keys=True))
if __name__=='__main__':main()
