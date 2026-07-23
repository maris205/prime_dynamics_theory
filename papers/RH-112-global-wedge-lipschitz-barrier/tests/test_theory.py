from __future__ import annotations
import numpy as np
import pytest
from wedge_lipschitz import global_wedge_lower_bound, positivity_radius, product_weyl_lower_bound, sharp_scalar_example, wedge_lipschitz_radius

def test_global_bound_is_valid_and_weyl_dominates() -> None:
    rng=np.random.default_rng(112)
    for _ in range(80):
        recent=rng.normal(size=(11,6)); error=rng.normal(size=(11,6)); delta=10**rng.uniform(-5,-1); error*=delta/np.linalg.norm(error,2)
        shat=np.linalg.svd(recent,compute_uv=False); full=np.linalg.svd(recent+error,compute_uv=False)
        global_lower=global_wedge_lower_bound(shat,delta)['normalized_lower']; direct=product_weyl_lower_bound(shat,delta); actual=np.prod(full[:4])/full[0]**4
        assert global_lower<=actual+2e-12
        assert global_lower<=direct+2e-12

def test_sharp_scalar_family() -> None:
    for delta in (0.0,1e-8,1e-3,0.2):
        row=sharp_scalar_example(1.7,delta)
        assert row['exact_difference']==pytest.approx(row['bound'])

def test_positivity_radius() -> None:
    singular=np.array([4.0,3.0,2.0,0.5])
    radii=positivity_radius(singular)
    assert radii['global']<radii['product_weyl']==pytest.approx(0.5)

def test_validation() -> None:
    with pytest.raises(ValueError): wedge_lipschitz_radius(1.0,-1.0)
    with pytest.raises(ValueError): global_wedge_lower_bound([1.0,0.5,0.2],0.1)
