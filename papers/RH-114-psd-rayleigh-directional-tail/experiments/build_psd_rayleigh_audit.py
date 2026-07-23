"""Audit scalar, positive-block, and exact relative tail Gramians."""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
import sys
from flint import ctx
import numpy as np
ROOT=Path(__file__).resolve().parents[1];PAPERS=ROOT.parent
RH77=PAPERS/'RH-77-postblock-effective-rank-compression';RH82=PAPERS/'RH-82-half-log-postblock-rank-clock';RH94=PAPERS/'RH-94-source-seeded-four-direction-horizon-refresh';RH96=PAPERS/'RH-96-gap-weighted-weak-mode-quotient';RH101=PAPERS/'RH-101-finite-memory-packet-gram-action';RH108=PAPERS/'RH-108-finite-memory-fourth-cross-support';RH113=PAPERS/'RH-113-right-frame-directional-wedge'
sys.path[:0]=[str(ROOT/'src'),str(RH77/'experiments'),str(RH82/'src'),str(RH94/'src'),str(RH94/'experiments'),str(RH96/'src'),str(RH96/'experiments'),str(RH101/'src'),str(RH108/'src'),str(RH113/'src')]
from directional_wedge import top_right_frame  # noqa:E402
from finite_memory_gram import memory_grams,truncated_memory_gram  # noqa:E402
from fourth_cross_support import finite_tail_operator_bound  # noqa:E402
from half_log_rank import clock_rank,half_log_clock  # noqa:E402
from psd_rayleigh_tail import positive_tail_cross_gram_upper,relative_rayleigh_certificate,scalar_tail_gram_upper  # noqa:E402
from run_effective_rank_audit import HORIZONS,SIGMAS,build_models  # noqa:E402
from run_source_seeded_horizon_audit import ETA  # noqa:E402
from run_weak_mode_quotient_audit import one_step  # noqa:E402
from source_seeded_refresh import source_right_packet  # noqa:E402
FULL_OUTPUT=ROOT/'results/psd_rayleigh_audit.json';SMOKE_OUTPUT=ROOT/'results/psd_rayleigh_smoke.json';PRECISION_BITS=384;DEPTH=5;RANK_OFFSET=2;THRESHOLDS=(1e-8,1e-6,1e-4);ACTION_GUARD=2e-14;ROUNDING_FACTOR=64.0

def state_history(model:dict[str,object],endpoint:int)->list[np.ndarray]:
 operator=np.asarray(model['operator'],dtype=float);source=np.asarray(model['source'],dtype=float);states=[source]
 for _ in range(endpoint):states.append(operator@states[-1])
 return states

def psd_upper_with_roundoff(theoretical:np.ndarray,actual:np.ndarray)->tuple[np.ndarray,float]:
 difference=(theoretical-actual+theoretical.T-actual.T)/2;minimum=float(np.linalg.eigvalsh(difference)[0]);scale=max(float(np.linalg.norm(theoretical,2)),float(np.linalg.norm(actual,2)),np.finfo(float).tiny);correction=max(0.0,-minimum)+ROUNDING_FACTOR*np.finfo(float).eps*scale;return theoretical+correction*np.eye(4),correction

def channel_audit(model:dict[str,object],sigma:float,threshold:float,rank:int)->dict[str,object]:
 endpoint=max(4,int(math.ceil(2*HORIZONS[sigma]/3)));states=state_history(model,endpoint);full_grams=memory_grams(states,ETA);packet=source_right_packet(states[0],rank);steps=[]
 for time in range(1,endpoint+1):
  full_gram=full_grams[time];recent_gram=truncated_memory_gram(states,eta=ETA,time=time,depth=DEPTH);tail_gram=(full_gram-recent_gram);tail_gram=(tail_gram+tail_gram.T)/2
  recent=recent_gram@packet-packet@(packet.T@recent_gram@packet);full=full_gram@packet-packet@(packet.T@full_gram@packet);residual=full-recent;frame=top_right_frame(recent);recent_action=recent@frame;residual_action=residual@frame
  recent_singular=np.linalg.svd(recent,compute_uv=False);full_singular=np.linalg.svd(full,compute_uv=False);past_count=max(0,time-DEPTH+1);analytic=finite_tail_operator_bound(ETA,DEPTH,past_count);tail_norm=float(np.linalg.norm(tail_gram,2));delta=math.nextafter(max(analytic+ACTION_GUARD,tail_norm+ACTION_GUARD),math.inf);leading=float(recent_singular[0]+delta)
  exact_d=residual_action.T@residual_action;scalar_d=scalar_tail_gram_upper(delta);packet_block=frame.T@packet.T@tail_gram@packet@frame;packet_block=(packet_block+packet_block.T)/2;block_scale=max(float(np.linalg.norm(packet_block,2)),np.finfo(float).tiny);block_min=float(np.linalg.eigvalsh(packet_block)[0]);packet_correction=max(0.0,-block_min)+ROUNDING_FACTOR*np.finfo(float).eps*block_scale;packet_block=packet_block+packet_correction*np.eye(4);block_d=positive_tail_cross_gram_upper(packet_block,delta);block_d,correction=psd_upper_with_roundoff(block_d,exact_d)
  scalar=relative_rayleigh_certificate(recent_action,scalar_d,leading);block=relative_rayleigh_certificate(recent_action,block_d,leading);exact=relative_rayleigh_certificate(recent_action,exact_d,leading)
  product=float(np.prod(np.maximum(recent_singular[:4]-delta,0))/leading**4) if leading else 0.;actual=float(np.prod(full_singular[:4])/full_singular[0]**4) if full_singular[0] else 0.;exact_frame=float(np.prod(np.linalg.svd(full@frame,compute_uv=False))/leading**4) if leading else 0.
  next_packet,selector=one_step(full_gram,packet,threshold)
  steps.append({'time':time,'threshold':threshold,'packet_rank':rank,'selected_width':int(selector['selected_width']),'analytic_tail_bound':float(analytic),'audited_tail_norm':tail_norm,'tail_norm_upper':delta,'tail_norm_enlargement':delta/max(analytic+ACTION_GUARD,np.finfo(float).tiny),'packet_block_roundoff_correction':packet_correction,'block_roundoff_correction':correction,'block_psd_dominates':bool(np.linalg.eigvalsh(block_d-exact_d)[0]>=-2e-15),'scalar_gamma':float(scalar['gamma']),'block_gamma':float(block['gamma']),'exact_gamma':float(exact['gamma']),'scalar_relative_lower':float(scalar['normalized_lower']),'block_relative_lower':float(block['normalized_lower']),'exact_relative_lower':float(exact['normalized_lower']),'product_weyl_lower':product,'exact_frame_lower':exact_frame,'actual_spectral_volume':actual,'scalar_support':bool(scalar['normalized_lower']>=threshold),'block_support':bool(block['normalized_lower']>=threshold),'exact_relative_support':bool(exact['normalized_lower']>=threshold),'product_support':bool(product>=threshold),'actual_support':bool(actual>=threshold),'all_certificates_valid':bool(max(scalar['normalized_lower'],block['normalized_lower'],exact['normalized_lower'],product,exact_frame)<=actual+3e-12)})
  packet=next_packet
 return {'sigma':sigma,'side':model['side'],'threshold':threshold,'clock_rank':rank,'refresh_endpoint':endpoint,'steps':steps}

def main()->None:
 parser=argparse.ArgumentParser();parser.add_argument('--smoke',action='store_true');args=parser.parse_args();old=ctx.prec;ctx.prec=PRECISION_BITS;rows=[]
 try:
  for sigma in (SIGMAS[:1] if args.smoke else SIGMAS):
   rank=clock_rank(sigma,offset=RANK_OFFSET);_,models=build_models(sigma);rows.append({'sigma':sigma,'clock':half_log_clock(sigma),'clock_rank':rank,'channels':[{'side':m['side'],'thresholds':[channel_audit(m,sigma,t,rank) for t in THRESHOLDS]} for m in models]})
 finally:ctx.prec=old
 records=[(r['sigma'],q) for r in rows for c in r['channels'] for q in c['thresholds']];all_steps=[s for _,q in records for s in q['steps']];threshold_summary={}
 for threshold in THRESHOLDS:
  chosen=[(sigma,q) for sigma,q in records if q['threshold']==threshold];steps=[s for _,q in chosen for s in q['steps']];fine=[s for sigma,q in chosen if sigma<=.02 for s in q['steps']];threshold_summary[f'{threshold:.0e}']={'threshold':threshold,'update_count':len(steps),'scalar_support_count':sum(s['scalar_support'] for s in steps),'block_support_count':sum(s['block_support'] for s in steps),'exact_relative_support_count':sum(s['exact_relative_support'] for s in steps),'product_support_count':sum(s['product_support'] for s in steps),'actual_support_count':sum(s['actual_support'] for s in steps),'fine_update_count':len(fine),'fine_scalar_support_count':sum(s['scalar_support'] for s in fine),'fine_block_support_count':sum(s['block_support'] for s in fine),'fine_exact_relative_support_count':sum(s['exact_relative_support'] for s in fine),'fine_product_support_count':sum(s['product_support'] for s in fine),'fine_actual_support_count':sum(s['actual_support'] for s in fine)}
 fine_steps=[s for sigma,q in records if sigma<=.02 for s in q['steps']];reported=fine_steps or all_steps;summary={'scale_count':len(rows),'channel_count':sum(len(r['channels']) for r in rows),'update_count':len(all_steps),'fine_update_count':len(fine_steps),'block_psd_failure_count':sum(not s['block_psd_dominates'] for s in all_steps),'certificate_failure_count':sum(not s['all_certificates_valid'] for s in all_steps),'maximum_tail_norm_enlargement':max(s['tail_norm_enlargement'] for s in all_steps),'maximum_packet_block_roundoff_correction':max(s['packet_block_roundoff_correction'] for s in all_steps),'maximum_block_roundoff_correction':max(s['block_roundoff_correction'] for s in all_steps),'minimum_fine_scalar_gamma':min(s['scalar_gamma'] for s in reported),'maximum_fine_scalar_gamma':max(s['scalar_gamma'] for s in reported),'minimum_fine_block_gamma':min(s['block_gamma'] for s in reported),'maximum_fine_block_gamma':max(s['block_gamma'] for s in reported),'minimum_fine_exact_gamma':min(s['exact_gamma'] for s in reported),'maximum_fine_exact_gamma':max(s['exact_gamma'] for s in reported)}
 payload={'status':'rh114_psd_rayleigh_directional_tail_audit','precision_bits':PRECISION_BITS,'eta':ETA,'depth':DEPTH,'thresholds':list(THRESHOLDS),'rows':rows,'threshold_summary':threshold_summary,'audit_summary':summary,'theorem_boundary':{'positive_tail_cross_gram_upper':True,'relative_psd_rayleigh_volume_bound':True,'sharp_multiplicative_factor':True,'five_scale_psd_audit_validated':not args.smoke,'all_level_directional_tail_gram_law_proved':False,'all_level_physical_volume_lower_bound_proved':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'Positive memory tails admit a four-dimensional PSD cross-Gram upper, and a relative Rayleigh comparison converts it into a multiplicative exterior-volume certificate. The theorem isolates the needed physical input as a relative generalized eigenvalue gamma. The five-scale audit compares scalar, packet-block, and exact relative versions; no all-level gamma law is inferred.','limitations':['The packet-block tail Gramian is evaluated on finite models and lacks an all-level physical bound.','Roundoff corrections are archived explicitly and are not part of the abstract exact theorem.','No uniform Stage A, Hilbert--Polya, zero identification, or Riemann Hypothesis result is claimed.']}
 output=SMOKE_OUTPUT if args.smoke else FULL_OUTPUT;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(output.relative_to(ROOT)),**summary},sort_keys=True))
if __name__=='__main__':main()
