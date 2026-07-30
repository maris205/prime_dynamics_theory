from pathlib import Path
import sys
from flint import arb,ctx
ROOT=Path(__file__).resolve().parents[1]
for rel in ("../RH-13-validated-reduced-sector-spectral-gap/src","../RH-262-certified-deterministic-numerator-boundary-budget/src"):sys.path.insert(0,str(ROOT/rel))
from coefficient_envelope import certify_envelope,clean_envelope
from validated_gap.certificate import certify_reduced_gap
def test_clean_envelope_certificate():
 ctx.dps=100;b=certify_reduced_gap(decimal_precision=100,dimension=50,tail_degree=100);c=certify_envelope(b)
 assert c.envelope_constant<arb(48);assert c.scaled_cube<arb("0.801254");assert clean_envelope(29,c.q_star)>0
