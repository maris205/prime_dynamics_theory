from __future__ import annotations
import argparse,json
from pathlib import Path
import sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'src'))
from outward_loewner_guards import outward_loewner_certificate  # noqa:E402
def spd(rng):x=rng.normal(size=(4,4));return x.T@x+np.eye(4)
def perturb(rng,r):
 x=rng.normal(size=(4,4));x=(x+x.T)/2;n=np.linalg.norm(x,2);return x*(r/n if n else 0)
def main():
 p=argparse.ArgumentParser();p.add_argument('--smoke',action='store_true');a=p.parse_args();n=128 if a.smoke else 4096;rng=np.random.default_rng(127127 if a.smoke else 127);rows=[]
 for i in range(n):
  g,d=spd(rng),spd(rng)+100*np.eye(4);s=rng.normal(size=(4,4))+2.5*np.eye(4);af=10**rng.uniform(-1,.5);b=10**rng.uniform(-1,.5);delta=10**rng.uniform(-4,-1);radii=10**rng.uniform(-8,-3,4);rg,rd,rgp,rdp=radii;s2=np.linalg.norm(s,2)**2;h=s.T@g@s;cap=b*s.T@d@s+delta*h;gp=af*h+(4*(rgp+af*s2*rg)+.1)*np.eye(4);dp=cap-(4*(rdp+s2*(b*rd+delta*rg))+.1)*np.eye(4)
  gh=g+perturb(rng,rg);dh=d+perturb(rng,rd);gph=gp+perturb(rng,rgp);dph=dp+perturb(rng,rdp);c=outward_loewner_certificate(gh,dh,gph,dph,s,af,b,delta,rg,rd,rgp,rdp);exact_gram=float(np.linalg.eigvalsh(gp-af*h)[0]);exact_tail=float(np.linalg.eigvalsh(b*s.T@d@s+delta*h-dp)[0]);rows.append({'gram_guard_ratio':c['gram_required_guard']/c['gram_numeric_slack'],'tail_guard_ratio':c['tail_required_guard']/c['tail_numeric_slack'],'certified':c['both_certified'],'exact_gram_holds':exact_gram>=-1e-12,'exact_tail_holds':exact_tail>=-1e-12})
 af,b,delta=2.,3.,0.;rg,rd,rgp,rdp=.1,.2,.3,.4;gh=np.array([[1.]]);dh=np.array([[2.]]);g=gh+rg;gp=af*g;gph=gp+rgp;d=dh-rd;dp=b*d+delta*g;dph=dp-rdp;sharp=outward_loewner_certificate(gh,dh,gph,dph,np.eye(1),af,b,delta,rg,rd,rgp,rdp)
 summary={'sample_count':n,'certified_count':sum(r['certified'] for r in rows),'false_certification_count':sum(r['certified'] and not(r['exact_gram_holds'] and r['exact_tail_holds']) for r in rows),'maximum_gram_guard_ratio':max(r['gram_guard_ratio'] for r in rows),'maximum_tail_guard_ratio':max(r['tail_guard_ratio'] for r in rows),'sharp_gram_error':abs(sharp['gram_outward_slack']),'sharp_tail_error':abs(sharp['tail_outward_slack'])}
 payload={'status':'rh127_outward_loewner_transport_guards_audit','records':rows,'sharp_record':sharp,'audit_summary':summary,'theorem_boundary':{'outward_loewner_guard_theorem':True,'cross_assembly_spectral_radius_transport':True,'guard_sharpness':True,'all_level_roundoff_radii_proved':False,'five_scale_independent_assembly_revalidated':False,'uniform_stage_A_closed':False,'hilbert_polya_operator':False,'riemann_hypothesis':False},'route_consequence':'Spectral-norm enclosure radii transport through a gauge with the exact squared gauge norm. Subtracting the resulting guards from numerical Loewner slacks makes independently assembled comparisons rigorous. The theorem closes the logical gap but does not supply physical all-level radii.'}
 o=R/'results'/('outward_guard_smoke.json' if a.smoke else 'outward_guard_audit.json');o.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(o.relative_to(R)),**summary},sort_keys=True))
if __name__=='__main__':main()
