# TPC-374 derivation package

## 1. Finite operator

For a declared interval `I` and shell `Q < p <= 2Q`, define

\[
B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
\]

With `w_p=(p/Q)^beta`, let

\[
A(u,t)=\sum_p w_pB_p(u,t),\qquad
G(u)=\sum_p\sum_{s\in I}(w_pB_p(u,s))^2,
\qquad T(u,t)=\frac{A(u,t)}{\sqrt{G(u)G(t)}}.
\]

The geometry is the full-window geometry and is shared by every truncation.
It is positive on the declared finite panel because it is a finite sum of
nonnegative squares with at least one nonzero contribution in every row.

## 2. Predeclared band decomposition

For the fixed eight-block partition, write `b(i)=floor(i/256)`.  Define

\[
B_3(i,j)={\bf1}_{|b(i)-b(j)|\leq3}T(i,j),
\qquad R_3(i,j)={\bf1}_{|b(i)-b(j)|>3}T(i,j).
\]

The two masks are disjoint and exhaustive.  Therefore the identity

\[
T=B_3+R_3
\]

holds entrywise, exactly on every finite row.  The tail is symmetric because
`T` and the block mask are symmetric.

## 3. Mode identity

Let `Tv=lambda v` for the selected unit eigenvector.  Linearity gives

\[
v^{\mathsf T}B_3v+v^{\mathsf T}R_3v
 =v^{\mathsf T}Tv=\lambda.
\]

The certificate records both terms, their signed ratios to `lambda`, their
absolute ratios, and the residual and norm error.  These are identities for
the finite computed matrices; they are not a claim that the band causes the
full eigenvalue.

## 4. Inherited exact anchor

The small rational anchor is `[1010346,1010359)` at `Q=4`, exponent one,
with shell `{5,7}`.  It checks symmetry and positivity using exact rational
arithmetic.  It is inherited from TPC-373 and is not used to choose a main
panel row.

## 5. Numerical decision

The fixed band reproduces all six beta=2 full spectral-cap failures:
the keys are the three declared origins at `Q=2048` and `Q=8192`.  It has no
beta=2 Schur-cap failures, exactly as the full matrix.  On those six rows the
selected full-mode band absolute-Rayleigh retention is between
`0.99157117644491055` and `0.99157357537480051`; the omitted tail fraction is
at most `0.0084288235550895561`.  This is a finite near-block reduction
certificate, with no asymptotic exponent or arithmetic gain.
