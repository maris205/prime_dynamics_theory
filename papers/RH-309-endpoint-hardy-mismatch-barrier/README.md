# RH-309: Endpoint Hardy mismatch barrier

At `rho_star`, the actual mismatch belongs to `H2` for every fixed noise but
does not belong to `H-infinity`.  Endpoint `H2` convergence would imply the
full weighted coefficient bridge with constant `4.992111068649647`.

An exact odd cutoff gives

    ||g_sigma||_H2(rho_star) >= C / sqrt(log(e+M_sigma))
                               >= C' / sqrt(log(e+1/sigma)).

Endpoint `H2` convergence and nonconvergence are both still unproved.

Gates A--E remain false/open.  No Hilbert--Polya operator, Riemann-zero
identification, zeta-divisor equality, or RH conclusion is asserted.
