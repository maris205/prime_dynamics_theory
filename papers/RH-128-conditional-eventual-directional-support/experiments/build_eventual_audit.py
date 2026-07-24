from __future__ import annotations
import argparse,json
from pathlib import Path
import sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from eventual_directional_support import affine_envelope,eventual_support_floor  # noqa:E402
def main():
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');a=p.parse_args();n=128 if a.smoke else 4096;rng=np.random.default_rng(128128 if a.smoke else 128);rows=[]
 for i in range(n):
  rho=rng.uniform(0,.97);xstar=rng.uniform(0,.95);q=(1-rho)*xstar;base=rng.uniform(1e-5,.5);x0=rng.uniform(0,2);x=x0;minimum_ratio=1.
  for k in range(300):
   rn=rho*rng.uniform(.7,1);qn=q*rng.uniform(.7,1);x=rn*x+qn;an=base*(1+rng.uniform(0,.4)/(k+1));candidate=max(0,1-np.sqrt(x))**4*an;floor=eventual_support_floor(rho,q,base)['support_liminf_lower'];
   if k>=200 and floor>0:minimum_ratio=min(minimum_ratio,candidate/floor)
  envelope=affine_envelope(x0,rho,q,300);theory=eventual_support_floor(rho,q,base);rows.append({'rho':rho,'forcing':q,'base_liminf':base,'gamma_squared':x,'affine_envelope':envelope,'support_floor':theory['support_liminf_lower'],'tail_minimum_ratio':minimum_ratio,'recurrence_holds':bool(x<=envelope+2e-12),'support_floor_holds':bool(minimum_ratio>=1-2e-10)})
 rho,q,base=.75,.05,.3;xstar=q/(1-rho);sharp=eventual_support_floor(rho,q,base);x=.9
 for _ in range(2000):x=rho*x+q
 actual=max(0,1-np.sqrt(x))**4*base;sharp_error=abs(actual-sharp['support_liminf_lower'])/sharp['support_liminf_lower']
 summary={'sample_count':n,'recurrence_failure_count':sum(not r['recurrence_holds'] for r in rows),'support_floor_failure_count':sum(not r['support_floor_holds'] for r in rows),'minimum_tail_support_ratio':min(r['tail_minimum_ratio'] for r in rows),'maximum_support_floor':max(r['support_floor'] for r in rows),'sharp_relative_error':sharp_error}
 payload={'status':'rh128_conditional_eventual_directional_support_audit','records':rows,'sharp_record':{'rho':rho,'forcing':q,'base_liminf':base,'theorem_floor':sharp['support_liminf_lower'],'actual_limit':actual},'audit_summary':summary,'required_physical_packet':['eventual validated recurrence x_{n+1} <= rho x_n + q with rho<1','strict subunit fixed point q/(1-rho)<1','positive liminf for V_n/(L_n^4 C_n)','same-operator or RH-127 outward admissibility'],'theorem_boundary':{'conditional_eventual_support_theorem':True,'nonstationary_eventual_coefficient_version':True,'sharp_constant_coefficient_floor':True,'physical_recurrence_packet_proved':False,'finite_rh125_chain_implies_all_level_packet':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'A validated contractive affine recurrence for gamma squared plus a positive normalized-frame liminf gives an explicit eventual support floor. The remaining gap is now exactly a physical recurrence packet; finite RH-125 chains cannot supply it.'}
 o=R/'results'/('eventual_support_smoke.json' if a.smoke else 'eventual_support_audit.json');o.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(o.relative_to(R)),**summary},sort_keys=True))
if __name__=='__main__':main()

