# TPC-376 derivation package

## 1. Finite object

For a frozen interval \(I=[a,a+2047]\cap\mathbb Z\), shell anchor \(Q\), and
prime \(p\in(Q,2Q]\), define
\[
 K_p(u,t)=p\left(\frac pQ\right)^2
 \frac{66^2}{66^2+(u-t)^2}
 \left({\bf1}_{p\mid(u-t)}-\frac1{p-1}\right)
 {\bf1}_{u\ne t}{\bf1}_{p\nmid u}{\bf1}_{p\nmid t}.
\]
The unnormalised all-plus matrix is \(A(u,t)=\sum_pK_p(u,t)\), and the
row geometry is
\[
 G(u)=\sum_{t\in I}\sum_{p\in(Q,2Q]}K_p(u,t)^2.
\]
The normalized full matrix is
\[
 T(u,t)=A(u,t)/\sqrt{G(u)G(t)}.
\]

## 2. Exact finite identities

The kernel is symmetric in \(u,t\), and \(G(u)\) is a finite sum of
nonnegative rational squares.  The exact anchor calculation in the package
checks \(G(u)>0\) and matrix symmetry using rational arithmetic.

Let \(b(u)=\lfloor(u-a)/256\rfloor\).  The fixed band is
\[
 B_1(u,t)=T(u,t){\bf1}_{|b(u)-b(t)|\leq1},\qquad R_1=T-B_1.
\]
Hence \(T=B_1+R_1\) entrywise.  If \(Tv=\lambda v\) for the selected
unit eigenvector, then
\[
 v^TB_1v+v^TR_1v=v^TTv=\lambda.
\]
These are finite algebraic identities; they do not imply a uniform bound
as the interval grows.

## 3. Holdout logic

The candidate grid and training indices are inherited as a protocol lock.
The holdout indices \((5,15,30)\) are distinct from \((0,20,40)\), and the
complete nine-row panel is formed before any signed metric is used.  The
experiment therefore tests transfer across predeclared grid positions, not
post-selection on a failure.

## 4. Observed finite profile

The c=1 band has spectral failure counts
\[
(0,3,3)\quad\text{at }Q=(512,2048,8192),
\]
and zero Schur-cap failures.  This matches the parent Q-profile, while the
full-mode band Rayleigh retention remains between
0.93760019185559207 and 0.976941204869197.

## 5. Unpaid implications

No source-valid arithmetic \(L^2\) theorem, growing-window operator bound,
origin/window uniformity, cross-block causality, fixed-power credit, official
Route-B evaluator result, or twin-prime conclusion follows from this finite
calculation.
