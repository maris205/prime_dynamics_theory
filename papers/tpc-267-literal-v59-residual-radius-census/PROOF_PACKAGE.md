# TPC-267 proof package

## Theorem 1 — exact finite operator and projection split

For every listed tuple ((N,H,Q,s)), the program constructs exactly the
finite matrix (A) displayed in the derivation package, including the
off-diagonal restriction, both unit masks, the prime-only shell, outer factor
(q), and the (1/(q-1)) centered term.  The vector (g=A\beta_N) is thus
the literal finite operator output for the selected kernel profile.

The four block contrasts are pairwise orthogonal.  Dividing their cross-Gram
terms by (4B,2B,2B) is therefore the orthogonal projection onto their span,
and direct expansion gives

\[
 \langle w,g\rangle
 =\langle P_3w,P_3g\rangle
  +\langle (I-P_3)w,(I-P_3)g\rangle.
\]

No residual is discarded.

## Theorem 2 — outward finite enclosure

The finite Euler product is multiplied with decimal precision 100 and rounded
outward to a (10^{-30}) rational grid.  The uncomputed product tail is
bounded using (\prod(1-a_i)\geq1-\sum a_i) and

\[
 \sum_{m=P}^{\infty}m^{-2}<1/(P-1).
\]

For every prime logarithm, the decimal logarithm is surrounded by a
(10^{-25}) guard before the same outward grid conversion.  Subsequent sums,
products, squares, and quotients are exact rational interval operations.  The
certificate is consequently a reproducible numerical enclosure at the stated
guard and cutoff; its epistemic label is `NUMERICALLY_CERTIFIED`, not
`PROVED_EXACT_REAL_ARITHMETIC`.

## Theorem 3 — twelve finite phase contractions

For each row

\[
 (N,H,Q,s)\in\{(64,15,4,1),(64,15,4,2),\ldots,(384,50,7,2)\},
\]

the certificate verifies (R^2>0) and

\[
 \sup { |C_\perp|^2\over R^2}<1/16.
\]

The independent replay recomputes the same twelve ratios with a separate
implementation and finds each below (1/4).  The largest stored upper bound
is (0.2320126753), attained at the (N=64,s=1) row.

## Scope boundary

The finite profile (K_{H,s}), rounded (H,Q), fixed coarse comparison
(z=2), and finite (N) rows are modeling choices.  They do not identify
the smooth asymptotic V59 profile uniformly in (x).  In particular, this
package proves neither (R_x\ll x^{5/3-\delta}) nor a uniform signed sector
bound.  It supplies no fixed-power credit, arithmetic `L2`, full Gate B, or
twin-prime conclusion.
