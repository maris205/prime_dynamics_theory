"""Monotone composition of valid volume and capacity certificates."""
from __future__ import annotations
import math

def _finite_nonnegative(value:float,name:str)->float:
 number=float(value)
 if not math.isfinite(number) or number<0:raise ValueError(f"{name} must be finite and nonnegative")
 return number

def factorized_lower_bound(volume_lower:float,capacity_upper:float)->float:
 """Return a q4 lower bound from ``nu4 >= volume_lower`` and ``Lambda <= upper``."""
 volume=_finite_nonnegative(volume_lower,'volume lower');capacity=float(capacity_upper)
 if not math.isfinite(capacity) or capacity<=0: return 0.0
 return volume/capacity

def composite_lower_bound(candidates:dict[str,float])->tuple[float,str]:
 if not candidates:raise ValueError('at least one candidate is required')
 cleaned={name:_finite_nonnegative(value,name) for name,value in candidates.items()}
 label=max(cleaned,key=cleaned.get)
 return cleaned[label],label

def support_decision(lower_bound:float,threshold:float)->bool:
 lower=_finite_nonnegative(lower_bound,'lower bound');cutoff=float(threshold)
 if not math.isfinite(cutoff) or cutoff<=0:raise ValueError('threshold must be finite and positive')
 return bool(lower>=cutoff)
