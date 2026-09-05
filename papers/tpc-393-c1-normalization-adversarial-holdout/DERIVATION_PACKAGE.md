# TPC-393 derivation package

## Finite source object

For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, the producer uses

\[
 K_p(u,v)=p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac1{p-1}\right)
 \mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.
\]

The row geometry is $G(u)=\sum_{p,v}K_p(u,v)^2$ and the law-dependent matrix
is $M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v)$.  The fixed band retains pairs of
blocks whose indices differ by at most three.

## Declared normalizations

The local diagnostic is
$M_\ell(u,v)/(G(u)G(v))^{1/2}$.  The three scalar diagnostics divide by,
respectively, the pooled calibration mean at the current count, the current
origin mean, and the frozen pooled calibration mean at $N=1024$.  At $N=1536$
the pooled scalar is log-extrapolated from the two calibration scalar means.
All four choices are fixed before the current response is inspected.

## Targeted panel and forecast functional

TPC-393 retains only $Q=8192$ and the two declared laws all-plus and
alternating-index.  With $S_N$ denoting the mean fixed-band spectral
diagnostic in one cell,

\[
 \alpha=\frac{\log(S_{1280}/S_{1024})}{\log(1280/1024)},\qquad
 \widehat S_{1536}=S_{1024}(1536/1024)^\alpha.
\]

The reported forecast error is
$S_{1536}/\widehat S_{1536}-1$, and the forecast cap is $0.03$.  The
one-percent spread flag is
$(\max S_N-\min S_N)/\operatorname{mean}(S_N)\leq0.01$ over the declared
origins at each count.  Both are finite diagnostic functionals only.

## Exact anchor and numerical layer

A rational 13-point anchor at $[4200001,4200014)$ and $Q=8$ checks positive
geometry and exact symmetry for both declared laws.  The large panel is
evaluated in double precision.  Every row records finite values, symmetry,
Schur envelope, spectral envelope, and normalization role; the canonical JSON
payload hashes the complete row set and its parent provenance.

## Interpretation boundary

The observed difference between all-plus stability and alternating-index
instability is a finite origin diagnostic.  It does not imply origin
uniformity failure for an analytic operator, nor does the finite Schur pass
prove a Schur bound in a growing family.  The universal spectral-cap failure
is retained as an obstruction to this particular finite envelope.
