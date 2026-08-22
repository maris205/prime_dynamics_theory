# TPC-223 proof package

## Conditional compiler theorem

Assume a baseline exponent `E0`, nonnegative savings `delta_AP` and `kappa_pol`,
and a nonnegative structural loss `lambda_struct`.  Suppose the literal shell
quantity admits the conditional two-channel interface

```text
A_x << x^(E0-delta_AP+o(1)),
P_x << x^(E0-kappa_pol+o(1)),
S_x << x^lambda_struct(A_x+P_x).
```

Then

```text
S_x << x^(E0-sigma+o(1)),
sigma = min(delta_AP,kappa_pol)-lambda_struct.
```

In particular, `sigma > 1/400` implies
`S_x << x^(E0-1/400-epsilon+o(1))` for some `epsilon>0`.

## Proof

The sum of two positive terms is bounded by twice the larger power.  Thus its
exponent is the maximum of `E0-delta_AP` and `E0-kappa_pol`, namely
`E0-min(delta_AP,kappa_pol)`.  Multiplication by the structural factor adds
`lambda_struct`.  Rearranging gives the displayed `sigma`.  If `sigma` is strictly
larger than `1/400`, choose any `epsilon` with
`0<epsilon<sigma-1/400`; the endpoint inequality follows.

This is a conditional theorem about exponent bookkeeping.  It does not prove the
AP dispersion estimate, the polarized cross-correlation estimate, or the literal
prime-shell identification required to instantiate the interface.

## Exact boundary logic

The certificate uses rational arithmetic.  `sigma=1/400` is `BORDERLINE`, not a
strict pass; `sigma<1/400` is rejected.  A zero saving in either channel also fails,
which records the fact that both the TPC-220 collision channel and the TPC-222
polarized channel are required by this compiler.
