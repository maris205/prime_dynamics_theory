# TPC-286 derivation package

## Frozen finite object

Let $I$ be the finite integer source interval, let $q$ be an odd prime, and
let

```text
m_q(u) = 1_{q does not divide u},
B_q(u,t) = m_q(u)m_q(t)(1_{u=t mod q}-1/(q-1)),
D_q = B_q - diag(B_q).
```

The kernel is

```text
K_H(h) = H^(2s)/(H^2+h^2)^s,  s in {1,2}.
```

The diagonal-including and physical outputs for a source profile `beta` are

```text
g_full(u) = sum_{q in shell} sum_{t in I} q K_H(u-t) B_q(u,t) beta(t),
g_phys(u) = sum_{q in shell} sum_{t in I} q K_H(u-t) D_q(u,t) beta(t).
```

For active $u$ the diagonal entry is

```text
B_q(u,u) = (q-2)/(q-1),
```

and it is zero when $q$ divides $u$.  Hence

```text
g_diag(u) = sum_{q in shell} q K_H(0)(q-2)/(q-1)m_q(u)beta(u),
g_phys = g_full - g_diag.
```

## Scalar attachment

The finite audit uses the four-block projected scalar from TPC-268/TPC-284:

```text
C(w,g) = sum_u w(u)g(u)
         - sum_{r in three contrasts} W_r(w)G_r(g)/d_r.
```

The weights $w$ are interval-valued source weights and $g$ is an exact
rational output.  The map is linear in $g$, so the exact identity is

```text
C_phys = C_full - C_diag.
```

The implementation stores exact internal grid endpoints for the reconstructed
interval and the existing 12-significant-digit decimal serialization for
cross-release comparison.  The independent checker compares both: exact
reconstruction containment and normalized serialized endpoints.

## Registered ledger

The six baseline tuples are

```text
(64,15,4,4), (96,20,5,4), (128,24,5,4),
(192,32,6,5), (256,38,6,5), (384,50,7,5).
```

Each is evaluated for $s=1,2$ and the six controls
$H\pm2$, $z\pm1$, and $Q\pm1$, giving $6\times2\times6=72$ rows.

## Interpretation boundary

The decomposition is a theorem for the declared finite operator.  The sign
and ratio counts are numerical certificates for this finite registry.  No
limit passage, source-class uniformity, prime-shell cancellation, or
arithmetic norm estimate is hidden in the notation.
