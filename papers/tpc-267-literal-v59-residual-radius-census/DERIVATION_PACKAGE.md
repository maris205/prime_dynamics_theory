# TPC-267 derivation package

## 1. Frozen finite object

For an even integer (N), use

\[
 I_N=\{N/2+1,\ldots,N\},\quad
 \mathcal Q_Q=\{q\text{ prime}:Q<q\leq 2Q\}.
\]

The finite replay retains the V59 masks and signed centered residue kernel:

\[
 A(u,t)=1_{u\ne t}\sum_{q\in\mathcal Q_Q}qK_{H,s}(u-t)
 1_{q\nmid ut}\left(1_{u\equiv t\pmod q}-{1\over q-1}\right).
\]

The source coefficient is evaluated exactly as

\[
 \beta_N(t)={\Lambda(t)\over\log t}
 -\sum_{d\mid t,\ d^{400}\leq N^{133}}\mu(d).
\]

If (t=p^k), the first quotient is exactly (1/k); otherwise it is zero.
The shifted coefficient uses the finite interval enclosure of

\[
 w_N(u)=\Lambda(u+2)-2C_2,1_{2\nmid u}
       \prod_{p\mid u, p>2}{p-1\over p-2},qquad
 C_2=\prod_{p>2}\left(1-{1\over(p-1)^2}\right).
\]

The product is not replaced by a floating point constant.  It is computed to
the prime cutoff (P=50000), and its remaining positive tail is enclosed by
\[
 \prod_{p>P}\left(1-{1\over(p-1)^2}\right)
 \geq 1-{1\over P-1}.
\]

## 2. Physical output and frame

Set (g=A\beta_N) and (C=\sum_{u\in I_N}w_N(u)g(u)).  Split (I_N) into
four equal consecutive blocks.  With base contrasts

\[
 c_0=(1,1,-1,-1),\quad c_1=(1,-1,0,0),\quad
 c_2=(0,0,1,-1),
\]

their squared norms are (4B,2B,2B), where (B=|I_N|/4).  Hence

\[
 C_3=\sum_{j=0}^2 {W_jG_j\over \|c_j\|^2},
 \quad C_\perp=C-C_3,
\]

where (W_j) and (G_j) are the corresponding contrast sums.  This is the
same rank-three subspace as the normalized TPC-257 frame; normalization
cancels in the displayed cross-Gram formula.

The residual squared radius is

\[
 R^2=\|(I-P_3)w\|^2\|(I-P_3)g\|^2
 =\left(\|w\|^2-\|P_3w\|^2\right)
  \left(\|g\|^2-\|P_3g\|^2\right).
\]

All terms except logarithms are rational.  Interval arithmetic therefore
certifies (C,C_3,C_\perp,R^2), and (|C_\perp|^2/R^2) without taking an
uncontrolled square root.

## 3. Finite theorem and interpretation

For the twelve rows in the certificate, the upper endpoint of

\[
 \rho^2={|C_\perp|^2\over R^2}
\]

is strictly below (1/16).  Thus (ho<1/4) in every row.  The residual
is on the negative real axis in ten rows and on the positive real axis in two
rows for this even real kernel family.  The sign change is a finite phase
observation, not a uniform phase law.

The result tests the actual finite source-shaped vector against the Schur
radius.  It does not estimate the asymptotic size of (R), and it cannot
convert a finite correlation ratio into a fixed exponent saving.
