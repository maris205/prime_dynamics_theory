import pytest
from eventual_directional_support import affine_envelope,eventual_support_floor
def test_affine_formula():
 assert affine_envelope(.5,.8,.03,20)==pytest.approx(.8**20*.5+.03*(1-.8**20)/.2)
def test_support_floor():
 r=eventual_support_floor(.6,.1,.2);assert r['gamma_squared_limsup']==pytest.approx(.25);assert r['support_liminf_lower']==pytest.approx(.2*.5**4);assert r['subunit_gamma']
def test_boundary():
 r=eventual_support_floor(.5,.5,.2);assert not r['subunit_gamma'];assert r['support_liminf_lower']==0
 with pytest.raises(ValueError):eventual_support_floor(1,0,.1)

