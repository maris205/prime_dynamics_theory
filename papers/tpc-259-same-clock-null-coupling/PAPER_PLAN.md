# TPC-259 paper plan

## One-sentence contribution

On the same literal V59 clock, the source-frozen TPC-258 null direction has an
arbitrarily log-small `w` coefficient; therefore its rank-one contribution to
the signed Gate-B scalar is `o(x^(5/3)/log^(M+3) x)` for every fixed `M`, while
an exact orthogonal residual decomposition shows why this does not control the
full scalar.

## Research question

Does the TPC-258 transverse null direction suppress an actual same-clock
`w/beta` coupling, or does it merely cancel an isolated adjoint coordinate?
The test must preserve the literal output/input roles and must not identify a
small rank-one channel with a full `L2` estimate.

## Frozen inputs

- TPC-258's four-block frame and source-frozen `z_null`.
- TPC-254's source-backed maximal-interval bound for the literal hybrid `w`.
- The literal V59 operator `A_x` and coefficient `beta` from TPC-258.
- Inner product convention: conjugate-linear in the first slot.

## Main claim boundary

For `z=z_null`, write `w_parallel=<z,w>z` and
`w_perp=w-w_parallel`.  Then the exact identity is

```text
<w,A_x beta>=conjugate(<z,w>)<z,A_x beta>+<w_perp,A_x beta>.
```

The first term is source-backed
`o(x^(5/3)/log^(M+3) x)` for every fixed `M`; the second term remains open.
The conditional TPC-258 rate gives a corresponding conditional refinement.

## Evidence and experiments

1. Exact rational reconstruction of the four blocks and null weights.
2. A source-contract compiler extending maximal interval control from children
   to all four blocks and the fixed null combination.
3. Exact polarization/decomposition checks with real `w` and complex outputs.
4. Independent mutation rejection for swapped/null, non-unit, and
   data-dependent directions.
5. A zero-diagonal synthetic residual witness showing the full scalar can be
   nonzero while the null rank-one channel is exactly zero.

Synthetic witnesses are not claimed to be literal V59 counterexamples.

## Non-claims

No full arithmetic `L2` upper bound, full Gate B payment, strict global
`1/400` payment, fixed-atom credit, or twin-prime conclusion is obtained.
