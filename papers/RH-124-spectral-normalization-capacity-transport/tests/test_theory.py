import numpy as np
import pytest
from spectral_capacity_transport import normalized_metrics,transport_factor_bounds

def test_random_diagonal_transport():
 rng=np.random.default_rng(124)
 for _ in range(100):
  s=np.sort(rng.uniform(.2,3,7))[::-1];m,M=.2,2.5;scales=rng.uniform(np.sqrt(m),np.sqrt(M),s.size);sp=np.sort(s*scales)[::-1];a=normalized_metrics(s);b=normalized_metrics(sp);f=transport_factor_bounds(m,M)
  assert f['q4_lower_factor']*a['q4']<=b['q4']+1e-12<=f['q4_upper_factor']*a['q4']+1e-12
  assert f['capacity_lower_factor']*a['capacity23']<=b['capacity23']+1e-12<=f['capacity_upper_factor']*a['capacity23']+1e-12
  assert f['volume_lower_factor']*a['normalized_four_volume']<=b['normalized_four_volume']+1e-12<=f['volume_upper_factor']*a['normalized_four_volume']+1e-12

def test_sharp_families():
 m,M=.25,4.;f=transport_factor_bounds(m,M);s=np.array([100.,10.,1.,.1]);a=normalized_metrics(s)
 q=normalized_metrics(s*np.array([np.sqrt(M),1,1,np.sqrt(m)]));assert q['q4']/a['q4']==pytest.approx(f['q4_lower_factor'])
 v=normalized_metrics(s*np.array([np.sqrt(M),np.sqrt(m),np.sqrt(m),np.sqrt(m)]));assert v['normalized_four_volume']/a['normalized_four_volume']==pytest.approx(f['volume_lower_factor'])
 sc=np.array([100.,1.,.5,.1]);ac=normalized_metrics(sc);c=normalized_metrics(sc*np.array([np.sqrt(m),np.sqrt(M),np.sqrt(M),1]));assert c['capacity23']/ac['capacity23']==pytest.approx(f['capacity_upper_factor'])

def test_validation():
 with pytest.raises(ValueError):transport_factor_bounds(0,1)
