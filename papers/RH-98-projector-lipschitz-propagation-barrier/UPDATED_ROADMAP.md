# Updated roadmap after RH-98

## Route correction

The production data tempt one to set every future propagation factor to one.
RH-98 proves that this is not a structural law: a trace-normalized positive
Ritz counterexample amplifies tail loss by more than forty-four.

The correct factorization is

    local tail loss
      -> local projector displacement via compressed gap
      -> future projector displacement via block Lipschitz constant
      -> endpoint tail via endpoint Gram norm.

All finite production pairs satisfy this conditional envelope, but their
projector secant multiplier can exceed eight.

## Preferred RH-99 gate: differential projector envelope

For a separated compressed Ritz cluster, spectral projector derivatives solve
a Sylvester/resolvent equation. RH-99 should:

1. derive the derivative of one reduced refresh in Grassmann/projector form;
2. bound it by cross-direction and compressed-gap data;
3. compose derivative bounds over a short future block;
4. validate a finite neighborhood radius that contains the actual quotient
   displacement.

A successful result would replace pairwise hybrid replay by a certified local
Lipschitz tube. A negative result should identify which branch changes or gap
collapses prevent it.

RH-100 will then review the complete hundred-layer route. No Hilbert--Polya
operator, zero identification, or RH proof is claimed.
