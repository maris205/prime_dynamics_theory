# Source lock

The literal source is TPC-247.  For each fixed hard output block `c`, it gives

```text
w_c=P_cw,
v_cb:=A_cb beta_b=P_cA_xP_b beta,
sum_b <w_c,v_cb>.
```

The symbol `v_cb` is new shorthand only; the vector `A_cb beta_b` is explicit
in TPC-247.  All `b` share the same physical `w_c`.  Tagged copies repeat that
lane and therefore do not certify Cartesian-product realizability.

The hard partition remains a bookkeeping specialization and is not identified
with V59's smooth bounded-overlap partition.  No external theorem is needed;
the Gram-ellipsoid result is proved from finite-dimensional Hilbert geometry.
