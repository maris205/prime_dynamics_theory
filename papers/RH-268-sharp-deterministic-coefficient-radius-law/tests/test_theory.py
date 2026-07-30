import pytest
from sharp_coefficient import critical_harmonic_lower_bound,even_endpoint_normalized_ratio,odd_normalized_ratio
LAM=1.6785735104283223
def test_endpoint_ratios_tend_toward_one():
 assert odd_normalized_ratio(101,LAM)>0.999999
 assert even_endpoint_normalized_ratio(50,LAM)>0.999999
def test_critical_lower_bound_grows():
 assert critical_harmonic_lower_bound(10,1000,0.9)>critical_harmonic_lower_bound(10,100,0.9)
def test_invalid_parity():
 with pytest.raises(ValueError):odd_normalized_ratio(4,LAM)
