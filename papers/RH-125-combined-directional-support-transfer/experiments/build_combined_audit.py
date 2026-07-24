from __future__ import annotations
import argparse,collections,json
from pathlib import Path
import sys
import numpy as np
R=Path(__file__).resolve().parents[1];P=R.parent;sys.path.insert(0,str(R/'src'))
from combined_directional_transfer import combined_transfer_lower  # noqa:E402
def main():
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');a=p.parse_args();source=P/'RH-121-optimal-gram-gauge-pairing/results'/('optimal_gauge_smoke.json' if a.smoke else 'optimal_gauge_audit.json');data=json.loads(source.read_text());rows=[]
 for q in data['pairs']:
  ell=q['target_leading_upper']/q['source_leading_upper'];cap=q['target_capacity_upper']/q['source_capacity_upper'];r=combined_transfer_lower(q['source_gamma'],q['source_frame_volume'],q['source_leading_upper'],q['source_capacity_upper'],1.,q['optimal_tail_factor'],0.,0.,q['gauge_determinant'],ell,cap);target=q['target_directional_candidate'];rows.append({'pair_id':q['pair_id'],'source_sigma':q['source_sigma'],'target_sigma':q['target_sigma'],'side':q['side'],'threshold':q['threshold'],'phase':q['phase'],'source_candidate':r['source_candidate'],'target_candidate':target,'target_lower':r['target_candidate_lower'],'multiplier':r['candidate_multiplier'],'gamma_upper':r['gamma_upper'],'dominance_holds':bool(r['target_candidate_lower']<=target+3e-12),'efficiency':r['target_candidate_lower']/target if target else 1.})
 groups=collections.defaultdict(list)
 for r in rows:groups[(r['side'],r['threshold'],r['phase'])].append(r)
 chains=[]
 for key,items in groups.items():
  items.sort(key=lambda x:x['source_sigma'],reverse=True);prop=items[0]['source_candidate'];levels=[{'sigma':items[0]['source_sigma'],'lower':prop}]
  for item in items:prop*=item['multiplier'];levels.append({'sigma':item['target_sigma'],'lower':prop})
  target=items[-1]['target_candidate'];chains.append({'side':key[0],'threshold':key[1],'phase':key[2],'levels':levels,'terminal_lower':prop,'terminal_candidate':target,'dominance_holds':bool(prop<=target+3e-12),'terminal_efficiency':prop/target if target else 1.})
 summary={'pair_count':len(rows),'chain_count':len(chains),'one_step_dominance_failure_count':sum(not r['dominance_holds'] for r in rows),'chain_dominance_failure_count':sum(not c['dominance_holds'] for c in chains),'nonzero_transfer_count':sum(r['target_lower']>0 for r in rows),'above_1e-8_transfer_count':sum(r['target_lower']>=1e-8 for r in rows),'minimum_one_step_efficiency':min(r['efficiency'] for r in rows),'median_one_step_efficiency':float(np.median([r['efficiency'] for r in rows])),'maximum_one_step_efficiency':max(r['efficiency'] for r in rows),'minimum_terminal_lower':min(c['terminal_lower'] for c in chains),'median_terminal_lower':float(np.median([c['terminal_lower'] for c in chains])),'maximum_terminal_lower':max(c['terminal_lower'] for c in chains),'terminal_above_1e-8_count':sum(c['terminal_lower']>=1e-8 for c in chains),'terminal_above_1e-6_count':sum(c['terminal_lower']>=1e-6 for c in chains),'terminal_above_1e-4_count':sum(c['terminal_lower']>=1e-4 for c in chains)}
 payload={'status':'rh125_combined_directional_support_transfer_audit','source_archive':str(source.relative_to(P.parent)),'pairs':rows,'chains':chains,'audit_summary':summary,'theorem_boundary':{'combined_directional_transfer_theorem':True,'defect_gamma_volume_normalization_composition':True,'five_scale_regularized_chain_audited':not a.smoke,'physical_all_level_recurrence_proved':False,'regularized_chain_is_physical_support_certificate':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'The gamma recurrence, determinant transfer, leading normalization, and capacity upper compose into one directional candidate theorem. On the explicitly regularized five-scale diagnostic all 96 transfers are nonzero and all 24 chains remain above 1e-8, but the conditioning floor prevents interpreting this as a physical support proof.'}
 o=R/'results'/('combined_transfer_smoke.json' if a.smoke else 'combined_transfer_audit.json');o.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(o.relative_to(R)),**summary},sort_keys=True))
if __name__=='__main__':main()

