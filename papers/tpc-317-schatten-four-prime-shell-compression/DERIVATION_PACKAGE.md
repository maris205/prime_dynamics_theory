# TPC-317 derivation package

## 1. Locked literal operator

For an even `X`, write

```text
I_X={X/2+1,...,X},       N_X=X/2,
S_Q={p prime: Q<p<=2Q}.
```

With `H=66` and `s in {1,2}`, retain exactly the TPC-316 entry

```text
K_(p,u,t) = 1_(t!=u, p does not divide u*t)
             p H^(2s)/(H^2+(u-t)^2)^s
             (1_(u==t mod p)-1/(p-1)).
```

The source operator is

```text
(A beta)_(p,u) = sum_(t in I_X) K_(p,u,t) beta_t,
```

from `ell^2(I_X)` to `ell^2(S_Q x I_X)`.  Every entry is rational, and the
finite Gram matrix is `G=A^*A`.

## 2. Trace-power chain

Because `G` is positive semidefinite, its eigenvalues are real and nonnegative.
If they are `lambda_1,...,lambda_N`, then

```text
lambda_max(G)^2 <= sum_i lambda_i^2 <= (sum_i lambda_i)^2.
```

Taking square roots gives

```text
||A||_(2->2)^2 = lambda_max(G)
                 <= sqrt(trace(G^2))
                 <= trace(G)=||A||_HS^2.
```

Thus every finite source vector satisfies the sharper envelope

```text
N^(-1)||A beta||_2^2
 <= (sqrt(trace(G^2))/N)||beta||_2^2.
```

The lower trace-power quantity `trace(G^2)/trace(G)` is also no larger than
the true top eigenvalue, but it is not used as an asymptotic claim here.

## 3. Entrywise trace identities

The exact finite identities are

```text
trace(G) = sum_(p,u,t) K_(p,u,t)^2,

trace(G^2)
 = sum_(t,v in I_X) [sum_(p,u) K_(p,u,t) K_(p,u,v)]^2.
```

The first is the TPC-316 Hilbert--Schmidt mass.  The second is the new
Schatten-4 quantity.  Both are rational for a fixed finite panel.  The main
certificate computes the Gram entries from the literal formula and reduces
the final trace-square with two accumulation orders; a tiny rational panel
checks these identities without floating arithmetic.

## 4. Finite numerical protocol

The three source scales are `640,1280,2560`, so the source intervals are
`{321,...,640}`, `{641,...,1280}`, and `{1281,...,2560}`.  The shell anchors are
`24,36,54,80`; their cardinalities are `6,9,12,15`; and both exponents `1,2`
are retained.

For each row, the producer accumulates `G=A^*A` once in increasing prime order
and once in decreasing prime order.  The latter is not a new physical model;
it is a numerical reproducibility control.  The trace-square is reduced once
in binary64 and once after conversion to x87 `longdouble`.  A coarse IEEE
binary64 entrywise Gram guard, amplified for block accumulation and
symmetrization, is propagated to an outward decimal interval.  The interval
also contains both accumulation paths and has a fixed relative display guard.

The certificate calls a trend strict only when the upper endpoint at the
larger scale is below the lower endpoint at the smaller scale.  No fitted
exponent is used.

## 5. Parent and route boundary

The TPC-316 canonical certificate is locked by SHA-256 before any TPC-317
number is produced.  The finite compression result is a sharper diagnostic
of the same source operator, not arithmetic reassembly.  The next question is
whether the true top eigenvalue, or a more refined trace-power ladder, can be
certified without importing a power-saving claim.
