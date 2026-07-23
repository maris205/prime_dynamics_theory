"""Recompute the five-scale packets and audit recent right-frame wedges."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import sys
from flint import ctx
import numpy as np

ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent
RH77=PAPERS/'RH-77-postblock-effective-rank-compression';RH82=PAPERS/'RH-82-half-log-postblock-rank-clock';RH94=PAPERS/'RH-94-source-seeded-four-direction-horizon-refresh';RH96=PAPERS/'RH-96-gap-weighted-weak-mode-quotient';RH101=PAPERS/'RH-101-finite-memory-packet-gram-action';RH108=PAPERS/'RH-108-finite-memory-fourth-cross-support'
sys.path[:0]=[str(ROOT/'src'),str(RH77/'experiments'),str(RH82/'src'),str(RH94/'src'),str(RH94/'experiments'),str(RH96/'src'),str(RH96/'experiments'),str(RH101/'src'),str(RH108/'src')]
from directional_wedge import approximate_frame_certificate,capture_ratio,exact_frame_certificate,frame_volume,spectral_four_volume,top_right_frame  # noqa:E402
from finite_memory_gram import packet_action  # noqa:E402
from fourth_cross_support import finite_tail_operator_bound  # noqa:E402
from half_log_rank import clock_rank,half_log_clock  # noqa:E402
from run_effective_rank_audit import HORIZONS,SIGMAS,build_models  # noqa:E402
from run_source_seeded_horizon_audit import ETA,memory_grams  # noqa:E402
from run_weak_mode_quotient_audit import one_step  # noqa:E402
from source_seeded_refresh import source_right_packet  # noqa:E402

FULL_OUTPUT=ROOT/'results/directional_wedge_audit.json';SMOKE_OUTPUT=ROOT/'results/directional_wedge_smoke.json'
PRECISION_BITS=384;DEPTH=5;RANK_OFFSET=2;THRESHOLDS=(1e-8,1e-6,1e-4);GUARD=2e-14

def state_history(model:dict[str,object],endpoint:int)->list[np.ndarray]:
 operator=np.asarray(model['operator'],dtype=float);source=np.asarray(model['source'],dtype=float);states=[source]
 for _ in range(endpoint):states.append(operator@states[-1])
 return states

def channel_audit(model:dict[str,object],sigma:float,threshold:float,rank:int)->dict[str,object]:
 endpoint=max(4,int(math.ceil(2.0*HORIZONS[sigma]/3.0)));states=state_history(model,endpoint);grams=memory_grams(states);packet=source_right_packet(states[0],rank);steps=[]
 for time in range(1,endpoint+1):
  applied=packet_action(states,packet,eta=ETA,time=time,depth=DEPTH);recent=applied-packet@(packet.T@applied);past_count=max(0,time-DEPTH+1);analytic_tail=finite_tail_operator_bound(ETA,DEPTH,past_count);delta=math.nextafter(analytic_tail+GUARD,math.inf)
  gram=grams[time];full=gram@packet-packet@(packet.T@gram@packet);tail=full-recent
  recent_singular=np.linalg.svd(recent,compute_uv=False);full_singular=np.linalg.svd(full,compute_uv=False);frame=top_right_frame(recent);recent_action=recent@frame;full_action=full@frame
  directional_error=math.nextafter(float(np.linalg.norm(tail@frame,2))+GUARD,math.inf);leading_upper=float(recent_singular[0]+delta)
  global_frame=approximate_frame_certificate(recent_action,delta,leading_upper)['normalized_lower'];restricted_frame=approximate_frame_certificate(recent_action,directional_error,leading_upper)['normalized_lower'];exact_directional=exact_frame_certificate(full_action,leading_upper)
  direct=float(np.prod(np.maximum(recent_singular[:4]-delta,0.0))/leading_upper**4) if leading_upper else 0.0;actual=float(np.prod(full_singular[:4])/full_singular[0]**4) if full_singular[0] else 0.0;capture=capture_ratio(full,frame)
  next_packet,selector=one_step(gram,packet,threshold)
  steps.append({'time':time,'threshold':threshold,'packet_rank':rank,'selected_width':int(selector['selected_width']),'capture_ratio':float(capture),'recent_frame_volume':float(frame_volume(recent_action)),'full_frame_volume':float(frame_volume(full_action)),'full_spectral_volume':float(spectral_four_volume(full)),'global_frame_lower':float(global_frame),'direct_product_lower':float(direct),'global_frame_identity_error':float(abs(global_frame-direct)),'restricted_frame_lower':float(restricted_frame),'exact_directional_lower':float(exact_directional),'actual_normalized_volume':float(actual),'frame_variational_holds':bool(exact_directional<=actual+2e-12),'global_frame_support':bool(global_frame>=threshold),'restricted_frame_support':bool(restricted_frame>=threshold),'exact_directional_support':bool(exact_directional>=threshold),'actual_spectral_support':bool(actual>=threshold),'analytic_tail_operator_bound':float(analytic_tail),'tail_operator_bound':float(delta),'directional_tail_bound':float(directional_error),'directional_tail_gain':float(delta/max(directional_error,np.finfo(float).tiny)),'leading_upper_valid':bool(full_singular[0]<=leading_upper+2e-14)})
  packet=next_packet
 return {'sigma':sigma,'side':model['side'],'threshold':threshold,'clock_rank':rank,'refresh_endpoint':endpoint,'steps':steps}

def main()->None:
 parser=argparse.ArgumentParser();parser.add_argument('--smoke',action='store_true');args=parser.parse_args();previous=ctx.prec;ctx.prec=PRECISION_BITS;rows=[]
 try:
  for sigma in (SIGMAS[:1] if args.smoke else SIGMAS):
   rank=clock_rank(sigma,offset=RANK_OFFSET);_,models=build_models(sigma);channels=[]
   for model in models:channels.append({'side':model['side'],'thresholds':[channel_audit(model,sigma,t,rank) for t in THRESHOLDS]})
   rows.append({'sigma':sigma,'clock':half_log_clock(sigma),'clock_rank':rank,'channels':channels})
 finally:ctx.prec=previous
 records=[(row['sigma'],record) for row in rows for channel in row['channels'] for record in channel['thresholds']];all_steps=[step for _,record in records for step in record['steps']];threshold_summary={}
 for threshold in THRESHOLDS:
  chosen=[(sigma,record) for sigma,record in records if record['threshold']==threshold];steps=[step for _,record in chosen for step in record['steps']];fine=[step for sigma,record in chosen if sigma<=.02 for step in record['steps']]
  threshold_summary[f'{threshold:.0e}']={'threshold':threshold,'update_count':len(steps),'global_frame_support_count':sum(s['global_frame_support'] for s in steps),'restricted_frame_support_count':sum(s['restricted_frame_support'] for s in steps),'exact_directional_support_count':sum(s['exact_directional_support'] for s in steps),'actual_spectral_support_count':sum(s['actual_spectral_support'] for s in steps),'fine_update_count':len(fine),'fine_global_frame_support_count':sum(s['global_frame_support'] for s in fine),'fine_restricted_frame_support_count':sum(s['restricted_frame_support'] for s in fine),'fine_exact_directional_support_count':sum(s['exact_directional_support'] for s in fine),'fine_actual_spectral_support_count':sum(s['actual_spectral_support'] for s in fine)}
 fine_steps=[step for sigma,record in records if sigma<=.02 for step in record['steps']];reported=fine_steps or all_steps
 summary={'scale_count':len(rows),'channel_count':sum(len(r['channels']) for r in rows),'update_count':len(all_steps),'fine_update_count':len(fine_steps),'frame_variational_failure_count':sum(not s['frame_variational_holds'] for s in all_steps),'leading_upper_failure_count':sum(not s['leading_upper_valid'] for s in all_steps),'global_frame_identity_failure_count':sum(s['global_frame_identity_error']>2e-15 for s in all_steps),'minimum_capture_ratio':min(s['capture_ratio'] for s in all_steps),'maximum_capture_loss':max(1-s['capture_ratio'] for s in all_steps),'minimum_fine_capture_ratio':min(s['capture_ratio'] for s in reported),'maximum_fine_capture_loss':max(1-s['capture_ratio'] for s in reported),'minimum_directional_tail_gain':min(s['directional_tail_gain'] for s in all_steps),'maximum_directional_tail_gain':max(s['directional_tail_gain'] for s in all_steps),'minimum_fine_directional_tail_gain':min(s['directional_tail_gain'] for s in reported),'maximum_fine_directional_tail_gain':max(s['directional_tail_gain'] for s in reported)}
 payload={'status':'rh113_right_frame_directional_wedge_audit','precision_bits':PRECISION_BITS,'eta':ETA,'depth':DEPTH,'thresholds':list(THRESHOLDS),'rows':rows,'threshold_summary':threshold_summary,'audit_summary':summary,'theorem_boundary':{'directional_frame_variational_certificate':True,'approximate_action_weyl_certificate':True,'recent_frame_recovers_product_weyl':True,'frame_resolved_tail_gain_validated':not args.smoke,'all_level_directional_tail_law_proved':False,'all_level_physical_volume_lower_bound_proved':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'A four-column action on any orthonormal right frame gives a rigorous lower bound for the full fourth exterior norm. The recent top-four right frame with the global tail radius exactly reproduces product Weyl, while a frame-resolved residual can improve it without a full singular solve. The remaining theoretical input is an all-level directional tail-Gram bound.','limitations':['Directional residuals are evaluated on five finite models; no all-level residual law is proved.','The exact directional action is a reduced computational certificate, not an asymptotic theorem.','No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.']}
 output=SMOKE_OUTPUT if args.smoke else FULL_OUTPUT;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(output.relative_to(ROOT)),**summary},sort_keys=True))
if __name__=='__main__':main()
