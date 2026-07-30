# RH-314: Optimal endpoint-logarithm polynomial approximation

For `L(w)=log(1-w)+w`, the degree-`N` Taylor projection is the exact best
`H2` polynomial approximation and

    E_N(L)^2 = sum_(n>N) 1/n^2,
    E_N(L) ~ N^(-1/2).

The analytic remainder from RH-312 has exponentially smaller projection
error, so the complete deterministic endpoint target has the same sharp
asymptotic approximation rate.  Translating `N` into a mass clock is legal
only inside an explicitly stated information class; no spectral realization
rate is claimed.

Gates A--E remain false/open.
