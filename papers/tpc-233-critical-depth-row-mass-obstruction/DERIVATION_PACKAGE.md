# TPC-233 derivation package

## Target

Audit the fixed row-mass comparability hypothesis used in TPC-232 at the first depth
scale not excluded by its sieve theorem.

## Model

For integer `L>=3`, scale `Q`, clock `h=4LQ`, and a prime `Q<q<2Q`, put

\[
R_q=\left\lfloor\frac{Lq}{Q}\right\rfloor,
\qquad
A_h(R)=\#\{1\le m\le R:(m,h)=1\},
\qquad
N_q=2A_h(R_q).
\]

Here `N_q` is the exact support size and hence the row mass up to a common factor for
the uniform-atom profile.  It is not asserted to equal the actual V59 row mass.

## Universal envelope

Since `1` is always primitive and `L<=R_q<=2L-1`,

\[
2\le N_q\le2(2L-1),
\qquad
1\le\kappa_{\rm raw}(Q,L)
\le2L-1. \tag{D1}
\]

The upper bound alone permits comparability to grow with depth.

## Critical construction

Let

\[
P_L=\prod_{\ell\le L\atop \ell\ {m prime}}\ell,
\qquad
j_L=\left\lfloor\frac{L\log L-\log P_L}{\log2}\right\rfloor,
\qquad
Q_L=2^{j_L}P_L. \tag{D2}
\]

For all large `L`, `j_L>=0`, every prime divisor of `Q_L` is at most `L`, and

\[
\log Q_L=L\log L+O(1),
\qquad
L\sim\frac{\log Q_L}{\log\log Q_L}. \tag{D3}
\]

The classical de la Vallee Poussin PNT remainder implies

\[
\pi(x+y)-\pi(x)=\int_x^{x+y}\frac{dt}{\log t}
+O\!\left(xe^{-c\sqrt{\log x}}\right)
\]

for `y<=x` in the applications below.  With `x=Q_L` and
`y=Q_L/(2L)`, the main term dominates because `L` is polylogarithmic in `Q_L`.
Thus there are primes

\[
Q_L<p_L<Q_L+\frac{Q_L}{2L},
\qquad
2Q_L-\frac{Q_L}{2L}<r_L<2Q_L. \tag{D4}
\]

Their cutoffs are exactly

\[
R_{p_L}=L,
\qquad
R_{r_L}=2L-1. \tag{D5}
\]

## Exact coprime counts

Every integer `2<=m<=L` has a prime divisor at most `L`, hence a divisor of `Q_L`.
Therefore

\[
A_{4LQ_L}(L)=1. \tag{D6}
\]

For `L<m<2L`, a composite `m` has a prime divisor below `L`, while a prime `m` has
no common divisor with `4LQ_L`.  Consequently

\[
A_{4LQ_L}(2L-1)=1+\pi(2L-1)-\pi(L). \tag{D7}
\]

Equations (D5)--(D7) give

\[
N_{p_L}=2,
\qquad
N_{r_L}=2\{1+\pi(2L-1)-\pi(L)\}, \tag{D8}
\]

and hence, by the PNT,

\[
\kappa_{\rm raw}(Q_L,L)
\ge1+\pi(2L-1)-\pi(L)
\sim\frac{L}{\log L}\longrightarrow\infty. \tag{D9}
\]

## Interpretation

TPC-232's fixed-comparability energy corollary is valid as a conditional transfer,
but comparability cannot be inferred from raw support geometry.  The minimal repair is
to normalize rows and then audit the collision operator under that normalization.

## Non-claims

- No collision lower bound at critical depth is proved.
- No claim is made about actual V59 coefficients or profiles.
- Row normalization is not yet attached to the source.
- No signed saving, `L2`, strict `1/400`, full Gate B, or twin-prime theorem is proved.
