# RH-303: Fixed-order head transport is necessary

If the actual complement mismatch tends to zero in `H-infinity(rho)` or
`H2(rho)`, each fixed coefficient satisfies

    |tau_(sigma,n)-a_n| <= n rho^(-n) ||g_sigma||.

Together with the archived fixed-order total-trace and counterloop limits,
this forces fixed-order noisy-head/counterloop moment transport.  Root-level
matching is bypassed; head-moment transport is not.

Reproduce with the result builder, per-paper pytest command, and `latexmk`
commands listed in RH-302.  Gates A--E remain open.
