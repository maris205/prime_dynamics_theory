# TPC-386 derivation package

Let `I` be a consecutive integer window of count `N`, partitioned into blocks
of length 128. For a prime `p` in `(Q,2Q]`, define

\[
 K_p(u,v)=p(p/Q)^2\frac{66^2}{66^2+(u-v)^2}
 \left({\bf1}_{p\mid u-v}-\frac1{p-1}\right)
 {\bf1}_{u\ne v}{\bf1}_{p\nmid u}{\bf1}_{p\nmid v}.
\]

For a declared sign law `sigma`, `K_sigma` is the sum of `sigma(p)K_p`.
The diagonal geometry is

\[
 G(u)=\sum_{p\in(Q,2Q]}\sum_{v\in I}K_p(u,v)^2.
\]

The local matrix is `K_sigma(u,v)/sqrt(G(u)G(v))`; the pooled matrix divides
by the mean of `G` over the three `N=512` calibration windows at the same
`Q`. Both are then masked either by three adjacent block distances (`fixed`
mode) or by the full block graph (`full_relative` mode).

For each symmetric masked matrix `B`, the certificate records
`||B||_2`, the Schur row-mass maximum, Frobenius norm, and symmetry error.
The count-transfer ratio is the `N=1024` holdout mean divided by the `N=512`
calibration mean within one fixed law/normalization/Q/mode cell. The reported
`log2` ratio is descriptive; it is not asserted to be an exponent theorem.

The only exact symbolic step is the 13-point `Q=8` anchor. It proves positive
geometry and symmetry by rational arithmetic. All large-panel values are
finite floating-point observations checked by independent replay.
