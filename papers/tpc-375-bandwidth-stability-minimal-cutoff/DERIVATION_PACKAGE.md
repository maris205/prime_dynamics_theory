# TPC-375 derivation package

## 1. Common-normalized operator

For `Q < p <= 2Q`, set

\[
B_p(u,t)=p\frac{66^2}{66^2+(u-t)^2}
\left({\bf1}_{p\mid u-t}-\frac1{p-1}\right)
{\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
\]

For the frozen beta `2` and all-plus law, let `w_p=(p/Q)^2` and define

\[
A=\sum_p w_pB_p,\qquad
G(u)=\sum_p\sum_{s\in I}(w_pB_p(u,s))^2,
\qquad T(u,t)=A(u,t)/\sqrt{G(u)G(t)}.
\]

The geometry is computed on the full 2048-point window and is shared by the
full matrix and every band.

## 2. Nested bands

Let `b(i)=floor(i/256)`.  For `c=0,1,2,3`, define

\[
B_c(i,j)={\bf1}_{|b(i)-b(j)|\le c}T(i,j),
\qquad R_c=T-B_c.
\]

The masks are nested, symmetric, disjoint from their complements, and give
the exact finite identity `T=B_c+R_c` for every cutoff.  For a selected unit
eigenvector `v` of `T`,

\[
v^{\mathsf T}B_cv+v^{\mathsf T}R_cv=v^{\mathsf T}Tv=\lambda.
\]

## 3. Minimal-cutoff criterion

For each cutoff, compare the spectral value of `B_c` with cap `0.64` and
record the failure key `(origin,count,Q,exponent,law)`.  The first cutoff whose
failure-key set equals the parent set is the finite minimal cutoff for this
panel.  This is a descriptive decision rule, not an optimization theorem.

## 4. Numerical result

The spectral failure counts for `c=0,1,2,3` are respectively `0,6,6,6`;
all four cutoffs have zero beta=2 Schur failures.  The six failures at
`c=1` are exactly the three origins at `Q=2048,8192`, so the finite minimal
cutoff is `c=1`.  Across all nine rows, the selected full-mode absolute
Rayleigh retention ranges from `0.65584607757721647` at `c=0` to
`1.0016823596918929` at `c=3`; at `c=1` its range is
`0.93759913028905661--0.9769476322189844`.
