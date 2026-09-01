# TPC-326 derivation package

## 1. Same operator family, new origin

For `I_N=[16001,16000+N/2]` and `p in (Q,2Q]`, use the literal block

\[
B_{p,N}^{(s)}(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
\left(1_{p\mid u-t}-\frac1{p-1}\right)
1_{u\ne t}1_{p\nmid u}1_{p\nmid t}.
\]

Set `G_0=sum_p B_p^*B_p` and
`G_e=(sum_p e_p B_p)^*(sum_p e_p B_p)`.  The second origin is the only
intervention relative to TPC-325.

## 2. Cross-origin observables

For each scale, define the all-plus TV lower envelope as the minimum over its
eight `(Q,s)` rows, and the all-plus energy upper envelope as the maximum of
the signed/direct trace ratio.  Compare these four values to the corresponding
TPC-325 values.  The thresholds are frozen at `0.001` and `0.005`; they are
finite control thresholds, not analytic error terms.

## 3. Why this is not a translation identity

The source shift from `12001` to `16001` is not asserted to be divisible by
every prime in every active shell.  The stress test explicitly checks a
one-step residue-mask perturbation, so the replication is a source-environment
test rather than a consequence of conditional common-multiple covariance.
