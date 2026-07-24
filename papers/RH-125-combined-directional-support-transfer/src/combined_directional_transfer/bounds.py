"""Combined four-volume, Rayleigh, leading, and capacity transfer."""
from __future__ import annotations
import math

def _nn(x,name):
 v=float(x)
 if not math.isfinite(v) or v<0:raise ValueError(f'{name} must be finite and nonnegative')
 return v
def _pos(x,name):
 v=float(x)
 if not math.isfinite(v) or v<=0:raise ValueError(f'{name} must be finite and positive')
 return v

def directional_candidate(gamma:float,frame_volume:float,leading_upper:float,capacity_upper:float)->float:
 g=_nn(gamma,'gamma');v=_nn(frame_volume,'frame volume');l=_pos(leading_upper,'leading upper');c=_pos(capacity_upper,'capacity upper')
 return max(0.,1-g)**4*v/l**4/c

def combined_transfer_lower(source_gamma:float,source_volume:float,source_leading:float,source_capacity:float,gram_factor:float,tail_factor:float,gram_defect_fraction:float,additive_tail_defect:float,gauge_determinant:float,leading_factor:float,capacity_factor:float)->dict[str,float]:
 g=_nn(source_gamma,'source gamma');v=_nn(source_volume,'source volume');l=_pos(source_leading,'source leading');c=_pos(source_capacity,'source capacity');a=_pos(gram_factor,'gram factor');b=_nn(tail_factor,'tail factor');eta=float(gram_defect_fraction);delta=_nn(additive_tail_defect,'tail defect');det=abs(float(gauge_determinant));ell=_pos(leading_factor,'leading factor');cap=_pos(capacity_factor,'capacity factor')
 if not math.isfinite(eta) or not 0<=eta<1:raise ValueError('gram defect fraction must lie in [0,1)')
 if not math.isfinite(det) or det<=0:raise ValueError('gauge determinant must be nonzero')
 retained=a*(1-eta);gamma2=(b*g*g+delta)/retained;gamma_upper=math.sqrt(gamma2);volume_factor=retained**2*det;normalization_factor=volume_factor/(ell**4*cap);lower=normalization_factor*max(0.,1-gamma_upper)**4*v/l**4/c;source=directional_candidate(g,v,l,c);multiplier=lower/source if source>0 else 0.
 return {'gamma_squared_upper':gamma2,'gamma_upper':gamma_upper,'volume_factor':volume_factor,'normalization_factor':normalization_factor,'source_candidate':source,'target_candidate_lower':lower,'candidate_multiplier':multiplier}

