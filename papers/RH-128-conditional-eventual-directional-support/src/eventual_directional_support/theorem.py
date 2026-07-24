"""Conditional eventual support from a contractive gamma-squared recurrence."""
from __future__ import annotations
import math

def _nn(x,name):
 v=float(x)
 if not math.isfinite(v) or v<0:raise ValueError(f'{name} must be finite and nonnegative')
 return v
def affine_envelope(initial:float,rho:float,forcing:float,steps:int)->float:
 x=_nn(initial,'initial');r=_nn(rho,'rho');q=_nn(forcing,'forcing');n=int(steps)
 if n<0:raise ValueError('steps must be nonnegative')
 if r==1:return x+n*q
 return r**n*x+q*(1-r**n)/(1-r)
def eventual_support_floor(rho:float,forcing:float,base_liminf:float)->dict[str,float|bool]:
 r=float(rho);q=_nn(forcing,'forcing');a=_nn(base_liminf,'base liminf')
 if not math.isfinite(r) or not 0<=r<1:raise ValueError('rho must lie in [0,1)')
 xstar=q/(1-r);gamma=math.sqrt(xstar) if xstar>=0 else 0.;floor=max(0.,1-gamma)**4*a
 return {'gamma_squared_limsup':xstar,'gamma_limsup':gamma,'support_liminf_lower':floor,'subunit_gamma':bool(xstar<1)}

