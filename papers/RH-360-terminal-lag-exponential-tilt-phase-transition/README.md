# RH-360: Terminal-lag exponential-tilt phase transition

RH-360 studies the generating function of the exact RH-358 deterministic
terminal-lag distribution.  It proves a sharp transition at the source-locked
value `z=x`, including the critical `1/k` window and the limiting tilted
distributions on both sides.

Let

    pi_k(r)
      = [y_k^(2k-1-r)/(2k-1-r)] / C_k,
      0 <= r <= k-2,

and define

    G_k(z) = sum_(r=0)^(k-2) z^r pi_k(r),  z >= 0.

Then:

- Subcritical, `0 <= z < x`:

      G_k(z) -> (1-x^(-1))/(1-z/x).

- Critical window, `z_k=x exp(tau/k)`:

      G_k(z_k)/k
        -> 2(1-x^(-1)) integral_0^1
             exp[(tau+log C_M)s]/(2-s) ds.

- Supercritical, `z>x`:

      G_k(z)
        ~ [2 C_M(1-x^(-1))/(1-x/z)] (z/x)^(k-2).

Consequently

    (1/k) log G_k(z) -> max(0, log(z/x)),

whose derivative changes at `z=x`.

The tilted probability

    pi_(k,z)(r) = z^r pi_k(r)/G_k(z)

has three different limits:

- for `z<x`, terminal lag `r` converges to a geometric law with ratio `z/x`;
- for `z_k=x exp(tau/k)`, `r/k` converges to the density proportional to
  `exp[(tau+log C_M)s]/(2-s)` on `[0,1]`;
- for `z>x`, the distance `ell=k-2-r` from the opposite endpoint converges to
  a geometric law with ratio `x/z`.

These are normalized deterministic budget laws.  They are not eigenvalue
distributions, root-counting measures, or noisy stochastic laws.

## Conditional actual-head scope

Under the still-open original same-clock unnormalized hypothesis

    D_(4k)(R) -> 0,

RH-358's uniform coordinatewise lag-ratio theorem implies
`G_k^H(z_k)/G_k(z_k)->1` uniformly for every nonnegative tilt sequence, and
the tilted actual/deterministic distributions converge uniformly in relative
mass.  Thus all three regimes transfer only conditionally.  RH-360 does not
prove that leaf, identify roots or ranks, close a determinant or direct/full
trace ledger, activate RH-241 or RH-288, construct a Hilbert--Polya operator,
identify Riemann zeros, or prove RH.

## Reproduction

From this directory:

    make result
    make test
    make pdf
    make archive

Finite exact and high-precision rows reproduce formulas only; they are not
asymptotic or physical evidence.
