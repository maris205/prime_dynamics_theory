import numpy as np
import pytest
from outward_loewner_guards import outward_loewner_certificate
def test_certified_comparison_implies_exact():
 rng=np.random.default_rng(127)
 for _ in range(40):
  x=rng.normal(size=(4,4));g=x.T@x+np.eye(4);x=rng.normal(size=(4,4));d=x.T@x+np.eye(4);s=rng.normal(size=(4,4))+2*np.eye(4);a,b,delta=.7,.8,.05;h=s.T@g@s;cap=b*s.T@d@s+delta*h;gp=a*h+2*np.eye(4);dp=.5*cap;r=.01
  cert=outward_loewner_certificate(g,d,gp,dp,s,a,b,delta,r,r,r,r)
  if cert['both_certified']:
   assert np.linalg.eigvalsh(gp-a*h)[0]>=-1e-12;assert np.linalg.eigvalsh(cap-dp)[0]>=-1e-12
def test_scalar_guard_sharpness():
 a,b,delta=2.,3.,0.;rg,rd,rgp,rdp=.1,.2,.3,.4;gh=np.array([[1.]]);dh=np.array([[2.]]);s=np.array([[1.]])
 g=gh+rg;gp_exact=a*g;gph=np.array([[float(gp_exact[0,0]+rgp)]])
 d=dh-rd;dp_exact=b*d+delta*g;dph=np.array([[float(dp_exact[0,0]-rdp)]])
 cert=outward_loewner_certificate(gh,dh,gph,dph,s,a,b,delta,rg,rd,rgp,rdp);assert cert['gram_outward_slack']==pytest.approx(0);assert cert['tail_outward_slack']==pytest.approx(0)
def test_validation():
 with pytest.raises(ValueError):outward_loewner_certificate(np.eye(1),np.eye(1),np.eye(1),np.eye(1),np.eye(1),1,1,0,-1,0,0,0)
