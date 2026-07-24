import pytest
from combined_directional_transfer import combined_transfer_lower,directional_candidate

def test_formula_and_sharp_scalar_congruence():
 gamma=.2;v=3.;l=2.;c=.4;a=.8;b=.7;eta=.1;delta=.02;det=1.4;ell=1.2;cap=1.1
 r=combined_transfer_lower(gamma,v,l,c,a,b,eta,delta,det,ell,cap)
 gp=r['gamma_upper'];vp=(a*(1-eta))**2*det*v;lp=ell*l;cp=cap*c
 assert r['target_candidate_lower']==pytest.approx(directional_candidate(gp,vp,lp,cp))

def test_zero_when_gamma_crosses_one():
 r=combined_transfer_lower(.9,1,1,1,1,2,0,.1,1,1,1);assert r['target_candidate_lower']==0

def test_validation():
 with pytest.raises(ValueError):combined_transfer_lower(.1,1,1,1,1,1,1,0,1,1,1)

