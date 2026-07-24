"""Transport normalized fourth-mode metrics under two-sided Gram comparison."""

from __future__ import annotations
import math
import numpy as np


def _singular(values: np.ndarray) -> np.ndarray:
    s=np.asarray(values,dtype=float)
    if s.ndim!=1 or s.size<4 or np.any(~np.isfinite(s)) or np.any(s<0):raise ValueError('at least four finite nonnegative singular values are required')
    s=np.sort(s)[::-1]
    if s[0]<=0:raise ValueError('the leading singular value must be positive')
    return s


def normalized_metrics(singular_values: np.ndarray) -> dict[str,float]:
    s=_singular(singular_values);q=s/s[0]
    return {'leading':float(s[0]),'q4':float(q[3]),'capacity23':float(q[1]*q[2]),'normalized_four_volume':float(q[1]*q[2]*q[3])}


def transport_factor_bounds(gram_lower:float,gram_upper:float)->dict[str,float]:
    """Return sharp metric factors for ``m K*K <= K'*K' <= M K*K``."""
    m=float(gram_lower);M=float(gram_upper)
    if not math.isfinite(m) or not math.isfinite(M) or m<=0 or M<m:raise ValueError('require 0 < gram_lower <= gram_upper')
    r=m/M
    return {
      'condition_ratio':r,
      'q4_lower_factor':math.sqrt(r),'q4_upper_factor':1/math.sqrt(r),
      'capacity_lower_factor':r,'capacity_upper_factor':1/r,
      'volume_lower_factor':r**1.5,'volume_upper_factor':r**-1.5,
      'separate_volume_capacity_factor':r**2.5,
      'separation_loss_against_direct':r**2,
    }

