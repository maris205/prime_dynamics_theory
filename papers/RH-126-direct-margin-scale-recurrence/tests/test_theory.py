import numpy as np
import pytest
from direct_margin_recurrence import margin_transfer_lower,optimal_profile_scaling,support_margin
def test_weyl_margin_recurrence():
 s=np.array([10.,6.,3.,1.]);c=.8;e=.1;t=np.array([c*s[0]+e,c*s[1],c*s[2],c*s[3]-e]);tau=.05;assert support_margin(t,tau)==pytest.approx(margin_transfer_lower(support_margin(s,tau),c,e,tau))
def test_optimal_profile_fit():
 s=np.array([10.,2.]);t=np.array([7.,1.]);r=optimal_profile_scaling(s,t);assert max(abs(t-r['scale']*s))==pytest.approx(r['error']);
 for c in np.linspace(0,2,1000):assert r['error']<=max(abs(t-c*s))+1e-8
def test_validation():
 with pytest.raises(ValueError):support_margin([1,0],.1)

