"""Direct fourth-mode support-margin recurrence."""
from __future__ import annotations
import math
import numpy as np

def _profile(values):
 s=np.asarray(values,dtype=float)
 if s.ndim!=1 or s.size<2 or np.any(~np.isfinite(s)) or np.any(s<=0):raise ValueError('a finite positive singular profile is required')
 return s
def support_margin(singular_values,threshold):
 s=_profile(singular_values);tau=float(threshold)
 if not math.isfinite(tau) or tau<0:raise ValueError('threshold must be finite and nonnegative')
 return float(s[-1]-tau*s[0])
def margin_transfer_lower(source_margin,scale,error,threshold):
 m=float(source_margin);c=float(scale);e=float(error);tau=float(threshold)
 if not all(math.isfinite(x) for x in (m,c,e,tau)) or c<0 or e<0 or tau<0:raise ValueError('invalid recurrence data')
 return c*m-(1+tau)*e
def optimal_profile_scaling(source,target):
 """Minimize ``max_j |target_j-c source_j|`` over ``c>=0``."""
 s=_profile(source);t=_profile(target)
 if s.shape!=t.shape:raise ValueError('profiles must have the same shape')
 low,high=0.,float(np.max(t))
 for _ in range(120):
  error=(low+high)/2;lower=max(float(np.max((t-error)/s)),0.);upper=float(np.min((t+error)/s))
  if lower<=upper:high=error
  else:low=error
 error=high;lower=max(float(np.max((t-error)/s)),0.);upper=float(np.min((t+error)/s));scale=(lower+upper)/2
 return {'scale':scale,'error':error,'relative_error':error/(scale*s[0]) if scale*s[0] else math.inf,'maximum_residual':float(np.max(np.abs(t-scale*s)))}

