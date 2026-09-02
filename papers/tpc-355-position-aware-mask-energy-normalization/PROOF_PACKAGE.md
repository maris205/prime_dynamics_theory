# TPC-355 proof and scope package

## Proposition 1: finite geometry positivity

For a declared row, `G_u=sum_{p,t} B_p(u,t)^2` is a finite sum of
nonnegative terms.  The producer and the independent checker verify the
stronger row-level fact `G_u>0` for every coordinate used in the `648` rows.
Hence `D_G^(-1/2)` exists on each audited finite row.

This is a finite declared-model statement; positivity for a growing family of
intervals is not claimed.

## Proposition 2: finite diagonal congruence

If `D_G=diag(G_u)` with all `G_u>0`, then
`A#=D_G^(-1/2) A D_G^(-1/2)` is a finite real matrix.  No norm bound follows
from this definition alone.

## Proposition 3: polarization and Cauchy envelope

For any finite real matrix `T` and `beta=L-b`, expansion of the finite square
gives

```text
||T beta||_2^2=||T L||_2^2+||T b||_2^2-2<T L,T b>.
```

Applying finite Cauchy--Schwarz to the cross term yields the normalized
residual envelope in the derivation package.  Taking `T=A` or `T=A#` is
legitimate because both are finite matrices.

## Proposition 4: certified finite audit

The canonical certificate has three panels and `648` law-level rows.  Both raw
and normalized replay metrics are recorded.  Each metric has `647` positive,
`1` negative, and `0` unresolved alignments.  Reverse-shell accumulation,
exact rational anchor checks, and ten in-memory mutation tests are separate
controls.

## Narrowest obstruction

The normalization partially reduces the TPC-353-to-TPC-354 all-plus minimum
drop (`0.042151146184724153` to `0.026236988152766205`), but the all-plus
mean drop becomes larger (`0.021249745559872912` to
`0.024839744603963321`).  On the fresh panel a mod-4 row is negative after
normalization (`33001/512/Q24/s=1`), and the higher-panel half-split minimum
also decreases.  Thus the diagonal congruence is a finite partial repair, not
a law-uniform or source-uniform theorem.

## Missing theorem

No source-uniform masked arithmetic `L2` estimate, growing geometry bound,
canonical sign law, fixed-power saving, Route-B reassembly, or twin-prime
conclusion is proved.  The official Session-named evaluator files are absent;
the local Bridge-B checker is fail-closed fallback evidence only.
