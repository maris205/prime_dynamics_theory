# RH-305: Interior annular norm rate barrier

For every strict certified annulus and every modulus-capped complement of
squared mass `M`, an exact odd witness gives a rigorous coefficient lower
bound.  As `M -> infinity`, both `H-infinity` and `H2` mismatch norms obey

    norm >= C_rho M^(-kappa(rho)) / log(e+M).

At `rho=1.41`, `kappa=0.035045705260961...`.  With `M_sigma <= sigma^-1`,
power decay faster than `sigma^kappa` is excluded.  Convergence at a slower
rate remains open.

The numerical builder uses the exact least odd witness, not a unit-constant
asymptotic surrogate.  Gates A--E remain open.
