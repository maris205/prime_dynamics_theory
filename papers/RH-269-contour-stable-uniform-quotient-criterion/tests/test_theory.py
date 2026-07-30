import math,pytest
from contour_criterion import criterion_status,riesz_projection_difference_bound
def test_projection_bound():
 assert riesz_projection_difference_bound(2*math.pi,3.0,0.01)==pytest.approx(0.09)
def test_all_hypotheses_required():
 p=criterion_status(hilbert_schmidt_convergence=True,common_finite_rank_isolating_contour=True,uniform_resolvent_bound=True,limit_block_contraction=False);assert p["satisfied_hypothesis_count"]==3;assert p["criterion_complete"] is False
