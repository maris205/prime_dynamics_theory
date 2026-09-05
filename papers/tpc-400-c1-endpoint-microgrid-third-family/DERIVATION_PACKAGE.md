# TPC-400 derivation package

## 1. Finite object

For each prime `p` in `(Q,2Q]`, with `Q=8192`, `H=66`, exponent one, and
`beta=2`, the producer forms

```text
K_p(u,v) = p (p/Q)^2 H^2/(H^2+(u-v)^2)
            * (1_{p | u-v} - 1/(p-1))
            * 1_{u != v} 1_{p !| u} 1_{p !| v}.
```

The diagonal geometry is

```text
G(u) = sum_p sum_v K_p(u,v)^2.
```

The prime shell is indexed increasingly in the producer and decreasingly in
the independent checker.  The endpoint matrices are

```text
M_plus = sum_p K_p,
M_alt  = sum_p (-1)^(index(p)) K_p,
M_lambda = (1-lambda) M_plus + lambda M_alt.
```

The four finite probes use `lambda=7/8,15/16,31/32,1`.  The identity is
linear algebra at the finite matrix level; it is not an arithmetic character
identity.

## 2. Third-family protocol

The current response-blind affine family is

```text
a_j = 7600001 + 401j, 0 <= j < 41.
selected indices = (0,8,16,24,32,40)
origins = (7600001,7603209,7606417,7609625,7612833,7616041)
```

The first three origins are calibration and the last three are holdout.  Each
window has `N=1024` points, eight blocks of length 128, and the fixed `c=3`
band.  Four normalization choices are evaluated without response-dependent
selection: local diagonal, pooled calibration scalar, current-origin scalar,
and a scalar frozen at the first calibration origin.

The parent interface is the direct same-law all-origin mean recorded by the
hash-locked TPC-399 certificate.  No current segment fit, threshold fit, or
parent interpolation is performed.  For a law/normalization cell, the two
cross-family errors are the calibration and holdout cohort means divided by
the frozen parent mean, minus one.  The within-family error divides the
holdout cohort mean by the calibration cohort mean, minus one.

## 3. Finite gates

The origin-spread diagnostic is `(max-min)/mean` over the six current origins,
with a 1% descriptive cap.  Cross-family and within-family errors use a 3%
descriptive cap.  The spectral and Schur diagnostics use caps 0.64 and 0.83.
These are finite audit gates, not asymptotic hypotheses.

## 4. Exact anchor

At the anchor interval `[7600001,7600014)`, with `Q=8` and shell `{11,13}`,
exact `Fraction` arithmetic verifies positive geometry, endpoint symmetry, and
all four interpolation identities.  This anchor validates the algebraic
construction independently of floating-point aggregate readout.

## 5. Boundary

The package establishes a finite third-family replication/obstruction pattern
only.  It supplies no source-valid growing operator bound, source-uniform
arithmetic `L2` estimate, fixed-power saving, Route-A/Route-B closure, or
twin-prime theorem.
