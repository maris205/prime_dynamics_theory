# Roadmap after RH-342

RH-342 replaces the vague phrase “match the noisy head to the counterloop”
with three mandatory, separately typed obligations on the common Hardy
clock `u=4k`:

1. an eventual rank law or a source-backed rank cap for the actual spectral
   head;
2. a common root modulus cap and an actual zero-padded root matching theorem;
3. a matching rate exceeding the threshold belonging to that cap.

With the source-safe global cap `B=1/r_H`, RH-299 requires

    gamma > 2 log(R/r_H)/log(lambda)
          = 1.926813889034... .

Replacing this by `0.926813889034...` is legal only after proving that every
actual-head root has modulus at most `beta+o(1)`; any strict exponent above
that limiting threshold then permits an eventual cap `B=beta+epsilon`.  A
decaying padded matching already forces
the exact rank law `#H_sigma=2k-2`, so rank equality cannot be treated as an
innocent padding convention.

Exact shifted moments can identify the roots if a rank cap `2k-2` is first
proved.  Without that cap, the hidden `4k`-shell has zero contribution at
every strict-prefix order while remaining root-l1 distance at least `2k`.
This closes only the cap-free inference from aggregate strict-prefix moments
to root matching.  It does not close or refute the actual aggregate
moment/Fourier/Hardy route.

The narrow positive reopen triggers are therefore:

- an actual spectral-head rank theorem synchronized to `k`;
- an actual zero-padded root matching with a proved common cap and rate above
  the corresponding threshold; or
- direct convergence of
  `g_sigma(z)=sum_(n>=2)(tau_(sigma,n)-a_n)z^n/n` on an annulus
  `1.4<rho<r_H lambda`.

Until one of those inputs exists, RH-299 root-l1 activation is
`STOP_SCOPED`, while aggregate and annular routes remain
`NOT_TESTABLE`/open.  The current paper does not activate RH-288 and does not
change Gates A--E.
