from __future__ import annotations
import argparse,json
from pathlib import Path
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from defect_rayleigh_recurrence import defect_transfer_certificate,iterate_affine_upper  # noqa:E402

def spd(rng,condition):
 q,_=np.linalg.qr(rng.normal(size=(4,4)));return q@np.diag(np.geomspace(1,condition,4))@q.T

def main():
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');a=p.parse_args();count=128 if a.smoke else 4096;rng=np.random.default_rng(123 if not a.smoke else 123123);rows=[]
 for i in range(count):
  g,d=spd(rng,10**rng.uniform(0,4)),spd(rng,10**rng.uniform(0,4));s=rng.normal(size=(4,4))+3*np.eye(4);af=10**rng.uniform(-1,1);b=10**rng.uniform(-1,1);eta=rng.uniform(0,.7);delta=10**rng.uniform(-5,-.3);h=s.T@g@s;e=rng.normal(size=(4,4));gp=af*(1-eta)*h+.05*e.T@e;cap=b*s.T@d@s+delta*h;dp=rng.uniform(.05,1)*cap;c=defect_transfer_certificate(g,d,gp,dp,s,af,b,eta,delta);rows.append({'actual':c['target_gamma_squared'],'upper':c['target_gamma_squared_upper'],'efficiency':c['target_gamma_squared']/c['target_gamma_squared_upper'],'gram_holds':c['gram_hypothesis_holds'],'tail_holds':c['tail_hypothesis_holds'],'conclusion':c['conclusion_holds']})
 x,af,b,eta,delta=.09,.8,.7,.2,.03;sharp=defect_transfer_certificate(np.eye(1),x*np.eye(1),af*(1-eta)*np.eye(1),(b*x+delta)*np.eye(1),np.eye(1),af,b,eta,delta)
 grid=[]
 for rho in (.2,.5,.8,.95,1.05):
  for forcing in (.001,.01,.05):
   values=iterate_affine_upper(.4,rho,forcing,80);grid.append({'rho':rho,'forcing':forcing,'last':values[-1],'fixed_point':forcing/(1-rho) if rho<1 else None})
 summary={'sample_count':count,'hypothesis_failure_count':sum(not(r['gram_holds'] and r['tail_holds']) for r in rows),'conclusion_failure_count':sum(not r['conclusion'] for r in rows),'minimum_efficiency':min(r['efficiency'] for r in rows),'maximum_efficiency':max(r['efficiency'] for r in rows),'sharp_relative_error':abs(sharp['target_gamma_squared']-sharp['target_gamma_squared_upper'])/sharp['target_gamma_squared_upper']}
 payload={'status':'rh123_defect_stable_rayleigh_recurrence_audit','records':rows,'recurrence_grid':grid,'sharp_record':sharp,'audit_summary':summary,'theorem_boundary':{'defect_stable_affine_recurrence':True,'constant_coefficient_iteration':True,'scalar_sharpness':True,'uniform_physical_coefficients_proved':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'Relative Gram loss and additive tail error combine into an exact affine upper recurrence for gamma squared. This is the form needed by outward transport, but no physical all-level coefficients are inferred.'}
 out=ROOT/'results'/('defect_recurrence_smoke.json' if a.smoke else 'defect_recurrence_audit.json');out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(out.relative_to(ROOT)),**summary},sort_keys=True))
if __name__=='__main__':main()

