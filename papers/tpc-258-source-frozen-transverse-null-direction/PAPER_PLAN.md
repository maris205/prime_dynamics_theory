# TPC-258 paper plan

## One-sentence contribution

The explicit two-dimensional transverse floor from TPC-257 contains a
source-frozen unit direction whose leading `B_Q` diagonal cancels exactly;
the remaining theorem is a logarithmic/o(1) cancellation, not a fixed-power
estimate.

## Research question

After TPC-257 showed that both descendant Haar coordinates can be of the same
order as the old midpoint, is there a coefficient-independent direction in
that plane that removes the common diagonal main term?  The direction must be
chosen from the limiting rank geometry and must retain the literal V59 masks,
deleted diagonal, prime shell, and boundary lanes.

## Frozen inputs

- TPC-257's four-block frame on `I_x=(x/2,x] intersect Z`.
- `H=x^(21/32)`, `Q=x^(1/3)`, `U=x^(133/400)` and the literal beta/operator.
- `kappa1=log(3456/3125)/2` and
  `kappa2=log(884736/823543)/2`.
- The TPC-255 bounded-variation adjoint compiler, including all masks and
  boundary terms.

## Main claim boundary

Define

```text
L1=log(3456/3125), L2=log(884736/823543),
z_null=(L2 z1-L1 z2)/sqrt(L1^2+L2^2).
```

Then `z_null` is source-only, unit, and orthogonal to `z0`, and

```text
<z_null,A_x beta>=o(x^(7/6)/log^3 x).
```

With an explicitly rate-controlled PNT remainder this becomes
`O(x^(7/6)/log^4 x+x^(55/48+epsilon))`; that rate statement is recorded as
conditional unless the cited source rate is separately reopened.

## Evidence and experiments

1. Exact rational four-block geometry on integral and nonintegral clocks.
2. Formal logarithm-vector verification of `L2*kappa1-L1*kappa2=0`.
3. Independent mutation tests rejecting swapped, sign-flipped, and
   data-dependent coefficient vectors.
4. An adversarial `1/sqrt(log x)` error model showing why `o(1)` alone does
   not imply a fixed-power saving.

Finite beta samples are observations only and carry no proof credit.

## Non-claims

No arithmetic `L2` upper bound, full Gate B payment, strict global `1/400`
payment, fixed-atom credit, or twin-prime conclusion is obtained.
