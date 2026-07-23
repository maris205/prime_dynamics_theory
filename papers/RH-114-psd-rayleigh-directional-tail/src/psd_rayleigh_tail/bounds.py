"""Relative PSD tail bounds and multiplicative four-volume certificates."""
from __future__ import annotations
import math
import numpy as np

ORDER=4

def _square(matrix:np.ndarray,name:str)->np.ndarray:
 value=np.asarray(matrix,dtype=float)
 if value.shape!=(ORDER,ORDER) or np.any(~np.isfinite(value)):
  raise ValueError(f"{name} must be a finite 4 by 4 matrix")
 return (value+value.T)/2.0

def _action(matrix:np.ndarray)->np.ndarray:
 value=np.asarray(matrix,dtype=float)
 if value.ndim!=2 or value.shape[1]!=ORDER or np.any(~np.isfinite(value)):
  raise ValueError("the recent action must have exactly four finite columns")
 return value

def scalar_tail_gram_upper(tail_norm_upper:float)->np.ndarray:
 """Return the scalar Gram upper ``delta^2 I``."""
 delta=float(tail_norm_upper)
 if not math.isfinite(delta) or delta<0:raise ValueError("tail norm upper must be finite and nonnegative")
 return delta**2*np.eye(ORDER)

def positive_tail_cross_gram_upper(tail_packet_block:np.ndarray,tail_norm_upper:float)->np.ndarray:
 """Return ``delta B`` for a positive tail packet block ``B``.

 For ``T>=0``, ``||T||<=delta`` and ``R=(I-PP*)TPQ``, one has
 ``R*R <= delta Q*P*T*P Q``.
 """
 block=_square(tail_packet_block,"tail packet block");delta=float(tail_norm_upper)
 if not math.isfinite(delta) or delta<0:raise ValueError("tail norm upper must be finite and nonnegative")
 if np.linalg.eigvalsh(block)[0]<-1e-10:raise ValueError("tail packet block must be positive semidefinite")
 return delta*block

def relative_tail_constant(recent_gram:np.ndarray,residual_gram_upper:np.ndarray)->float:
 """Return the least gamma inferred from ``D <= gamma^2 G``."""
 gram=_square(recent_gram,"recent Gramian");upper=_square(residual_gram_upper,"residual Gram upper")
 values,vectors=np.linalg.eigh(gram)
 if values[0]<=0:return math.inf
 inverse_root=(vectors*(values**-0.5))@vectors.T
 relative=(inverse_root@upper@inverse_root);relative=(relative+relative.T)/2
 return math.sqrt(max(0.0,float(np.linalg.eigvalsh(relative)[-1])))

def relative_rayleigh_certificate(recent_action:np.ndarray,residual_gram_upper:np.ndarray,leading_upper_bound:float)->dict[str,float]:
 """Apply the multiplicative ``(1-gamma)^4`` volume theorem."""
 action=_action(recent_action);leading=float(leading_upper_bound)
 if not math.isfinite(leading) or leading<0:raise ValueError("leading upper must be finite and nonnegative")
 gram=action.T@action;gamma=relative_tail_constant(gram,residual_gram_upper);volume=float(np.prod(np.linalg.svd(action,compute_uv=False)))
 factor=max(0.0,1.0-gamma)**ORDER if math.isfinite(gamma) else 0.0
 lower=factor*volume/leading**ORDER if leading else 0.0
 return {'gamma':gamma,'multiplicative_factor':factor,'recent_frame_volume':volume,'normalized_lower':float(lower)}
