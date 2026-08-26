# TPC-262 derivation package

## Frozen object

For a prime `q`, let `U_q={1,...,q-1}` and

```text
C_q = I_(q-1) - (1/(q-1)) 1 1^T.
```

This is the exact zero-frequency reduced-residue centering matrix. The
finite shell used by the certificate is `{5,7,11,13}`, with the literal outer
weight `q` retained.

For a packet `a=(a_q)_q`, set `Y(a)_q=C_q a_q` and use

```text
<<Y(a),Y(b)>> = sum_q q <C_q a_q,C_q b_q>.
```

No square-root of a prime weight is introduced; all certificate arithmetic is
rational.

For the physical finite interval `I`, restore the residue synthesis

```text
(S_(q,v)a)_r = sum_(n in I, n = r mod q) a_n e(vn/H),  r in F_q^*.
```

With (P_q) the diagonal mask of (q)-units, the exact signed remainder
operator is

```text
J_(q,v)=S_(q,v)^* C_q S_(q,v)-((q-2)/(q-1))P_q.
```

Thus
`V_q^times(a;v)-D_q^times(a)=<a,J_(q,v)a>`.
The certificate checks this identity at `v=0` on `I={1,...,24}`, while the
formula itself is the finite-`x`, phase-by-phase identity.

## Four-packet ledger

For vectors `Y_0,...,Y_3`, define

```text
Gamma_jk = <<Y_j,Y_k>>,
D = sum_j Gamma_jj,
R = sum_{j<k} Re(Gamma_jk).
```

Then

```text
||sum_j Y_j||^2 = D + 2R.
```

The four-point DFT gives the same statement as
`||sum_jY_j||^2=4||Yhat_0||^2`. Therefore a diagonal-only argument must be
supplemented by a signed cross-Gram estimate.

## Endpoint translation

The packet-energy Fourier character must also be typed carefully.  For
`E_j=||X+i^jY||^2` and `F_k=(1/4)sum_j i^(kj)E_j`, one has
`F_0=||X||^2+||Y||^2`, `F_1=<Y,X>`, and `F_3=<X,Y>`. Hence aggregate
mode zero and the V59 polarized scalar are distinct observables.

If `D_x` is at baseline scale `x^(5/3)` and all paid losses are included in
`lambda`, the exact endpoint compiler from TPC-261 requires the resulting
mode-zero expression to have effective saving strictly greater than `1/400`.
This package records the criterion; it does not assert the required estimate.
