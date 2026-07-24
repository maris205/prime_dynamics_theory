"""Outward spectral-radius guards for cross-assembly Loewner comparisons."""
from __future__ import annotations
import math
import numpy as np

def _sym(x,name):
 a=np.asarray(x,dtype=float)
 if a.ndim!=2 or a.shape[0]!=a.shape[1] or np.any(~np.isfinite(a)):raise ValueError(f'{name} must be a finite square matrix')
 return (a+a.T)/2
def _nn(x,name):
 v=float(x)
 if not math.isfinite(v) or v<0:raise ValueError(f'{name} must be finite and nonnegative')
 return v
def outward_loewner_certificate(source_gram_hat,source_tail_hat,target_gram_hat,target_tail_hat,gauge,gram_factor,tail_factor,additive_tail_defect,source_gram_radius,source_tail_radius,target_gram_radius,target_tail_radius):
 g=_sym(source_gram_hat,'source gram approximation');d=_sym(source_tail_hat,'source tail approximation');gp=_sym(target_gram_hat,'target gram approximation');dp=_sym(target_tail_hat,'target tail approximation');s=np.asarray(gauge,dtype=float)
 if s.shape!=g.shape or np.any(~np.isfinite(s)):raise ValueError('gauge has incompatible shape')
 a=float(gram_factor);b=_nn(tail_factor,'tail factor');delta=_nn(additive_tail_defect,'additive tail defect')
 if not math.isfinite(a) or a<=0:raise ValueError('gram factor must be positive')
 rg=_nn(source_gram_radius,'source gram radius');rd=_nn(source_tail_radius,'source tail radius');rgp=_nn(target_gram_radius,'target gram radius');rdp=_nn(target_tail_radius,'target tail radius');snorm=float(np.linalg.norm(s,2));s2=snorm**2
 gram_numeric=float(np.linalg.eigvalsh(gp-a*s.T@g@s)[0]);gram_guard=rgp+a*s2*rg;gram_outward=gram_numeric-gram_guard
 tail_numeric=float(np.linalg.eigvalsh(b*s.T@d@s+delta*s.T@g@s-dp)[0]);tail_guard=rdp+s2*(b*rd+delta*rg);tail_outward=tail_numeric-tail_guard
 return {'gauge_norm':snorm,'gram_numeric_slack':gram_numeric,'gram_required_guard':gram_guard,'gram_outward_slack':gram_outward,'tail_numeric_slack':tail_numeric,'tail_required_guard':tail_guard,'tail_outward_slack':tail_outward,'gram_comparison_certified':bool(gram_outward>=0),'tail_comparison_certified':bool(tail_outward>=0),'both_certified':bool(gram_outward>=0 and tail_outward>=0)}

