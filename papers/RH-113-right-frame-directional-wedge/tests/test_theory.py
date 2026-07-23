from __future__ import annotations
import numpy as np
import pytest
from directional_wedge import approximate_frame_certificate,capture_ratio,exact_frame_certificate,frame_volume,spectral_four_volume,top_right_frame

def test_variational_and_optimal_frames() -> None:
 rng=np.random.default_rng(113)
 for _ in range(30):
  matrix=rng.normal(size=(12,7));q,_=np.linalg.qr(rng.normal(size=(7,4)));assert frame_volume(matrix@q)<=spectral_four_volume(matrix)+1e-10
  optimal=top_right_frame(matrix);assert capture_ratio(matrix,optimal)==pytest.approx(1.0,abs=2e-12)

def test_approximate_action_certificate() -> None:
 rng=np.random.default_rng(2113)
 for _ in range(30):
  recent=rng.normal(size=(10,4));error=rng.normal(size=(10,4));delta=1e-3;error*=delta/np.linalg.norm(error,2);full=recent+error;leading=np.linalg.norm(full,2)+.1
  bound=approximate_frame_certificate(recent,delta,leading)['normalized_lower'];actual=exact_frame_certificate(full,leading);assert bound<=actual+2e-12

def test_recent_top_frame_matches_product_formula() -> None:
 rng=np.random.default_rng(313)
 matrix=rng.normal(size=(11,6));frame=top_right_frame(matrix);delta=1e-3;leading=np.linalg.norm(matrix,2)+delta;bound=approximate_frame_certificate(matrix@frame,delta,leading)['normalized_lower'];singular=np.linalg.svd(matrix,compute_uv=False);expected=np.prod(np.maximum(singular[:4]-delta,0))/leading**4;assert bound==pytest.approx(expected)

def test_validation() -> None:
 with pytest.raises(ValueError):frame_volume(np.eye(3))
 with pytest.raises(ValueError):approximate_frame_certificate(np.eye(4),-1,1)
