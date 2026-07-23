from __future__ import annotations
import numpy as np
import pytest
from psd_rayleigh_tail import positive_tail_cross_gram_upper,relative_rayleigh_certificate,relative_tail_constant,scalar_tail_gram_upper

def test_relative_rayleigh_certificate()->None:
 rng=np.random.default_rng(114)
 for _ in range(30):
  y=rng.normal(size=(10,4));r=rng.normal(size=(10,4))*1e-3;d=r.T@r;u=np.linalg.norm(y+r,2)+.1;cert=relative_rayleigh_certificate(y,d,u);actual=np.prod(np.linalg.svd(y+r,compute_uv=False))/u**4;assert cert['normalized_lower']<=actual+2e-12

def test_positive_tail_cross_gram_upper()->None:
 rng=np.random.default_rng(2114)
 for _ in range(20):
  z=rng.normal(size=(9,9));t=z.T@z;t/=np.linalg.norm(t,2);p,_=np.linalg.qr(rng.normal(size=(9,6)));q,_=np.linalg.qr(rng.normal(size=(6,4)));r=(np.eye(9)-p@p.T)@t@p@q;b=q.T@p.T@t@p@q;upper=positive_tail_cross_gram_upper(b,1.0);assert np.linalg.eigvalsh(upper-r.T@r)[0]>=-2e-12

def test_sharp_relative_factor()->None:
 rng=np.random.default_rng(3114);y=rng.normal(size=(8,4));gamma=.2;r=-gamma*y;cert=relative_rayleigh_certificate(y,r.T@r,np.linalg.norm(y+r,2));actual=np.prod(np.linalg.svd(y+r,compute_uv=False))/np.linalg.norm(y+r,2)**4;assert cert['normalized_lower']==pytest.approx(actual,rel=2e-12)

def test_validation()->None:
 with pytest.raises(ValueError):scalar_tail_gram_upper(-1)
 with pytest.raises(ValueError):relative_tail_constant(np.eye(3),np.eye(4))
