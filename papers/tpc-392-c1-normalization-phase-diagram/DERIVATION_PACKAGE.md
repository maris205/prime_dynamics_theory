# TPC-392 derivation package

## Finite object

For $p\in(Q,2Q]$, $H=66$, and $u,v$ in a finite interval, the producer uses

\[
 K_p(u,v)=p(p/Q)^2\frac{H^2}{H^2+(u-v)^2}
 \left(\mathbf 1_{p\mid u-v}-\frac1{p-1}\right)
 \mathbf 1_{u\ne v}\mathbf 1_{p\nmid u}\mathbf 1_{p\nmid v}.
\]

The row geometry is $G(u)=\sum_{p,v}K_p(u,v)^2$, and a law-dependent matrix is
$M_\ell(u,v)=\sum_p s_\ell(p)K_p(u,v)$.  The fixed band masks entries whose
block indices differ by at most three.

## Four declared normalizations

The local matrix is $M_\ell/(G_uG_v)^{1/2}$.  The three scalar matrices are
$M_\ell/d_N$ with $d_N$ equal to the pooled calibration mean at $N$, the
current-origin mean at $N$, or the frozen pooled calibration mean at $1024$.
At $1536$, the pooled scalar uses a predeclared log extrapolation from the two
calibration scalar means.

## Forecast functional

Writing $S_N$ for the mean fixed-band spectral diagnostic in a cell, the
finite slope and forecast are

\[
 \alpha=\frac{\log(S_{1280}/S_{1024})}{\log(1280/1024)},\qquad
 \widehat S_{1536}=S_{1024}(1536/1024)^\alpha.
\]

The reported forecast error is $S_{1536}/\widehat S_{1536}-1$.  This is a
finite diagnostic functional; it is not an asymptotic exponent and is not
transferred to a different source family.

## Exact anchor

A rational 13-point anchor at $[3800001,3800014)$ and $Q=8$ checks positive
geometry and symmetry for all four laws.  The large panel is evaluated in
double precision, with finite-value, symmetry, Schur, and spectral-envelope
checks recorded row by row.
