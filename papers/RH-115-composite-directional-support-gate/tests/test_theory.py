from __future__ import annotations
import pytest
from composite_gate import composite_lower_bound,factorized_lower_bound,support_decision
def test_factorized_gate()->None:
 assert factorized_lower_bound(.2,.5)==pytest.approx(.4)
 assert support_decision(.4,.4)
def test_maximum_preserves_lower_bound()->None:
 value,label=composite_lower_bound({'a':.1,'b':.3,'c':.2});assert value==pytest.approx(.3);assert label=='b'
def test_validation()->None:
 with pytest.raises(ValueError):factorized_lower_bound(-1,.5)
 with pytest.raises(ValueError):composite_lower_bound({})
