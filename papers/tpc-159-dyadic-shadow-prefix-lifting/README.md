# TPC-159: Dyadic-shadow prefix lifting

Paper title:

> *Dyadic-Shadow Lifting from Good-Scale Mobius Correlations
> to Almost-Endpoint Prefixes*

TPC-149 controls the determinant-two periodic core on every
nonexceptional interval `(N,2N]`. This paper performs an exact dyadic
telescoping to obtain cumulative prefixes.

Let

```text
J = ceil(A*log_2(log X)),
S_X,J = union over 1 <= j <= J of 2^j E_X^*.
```

For

```text
2^J*sqrt(X) <= T <= X,
T not in S_X,J,
```

the cumulative periodic core satisfies

```text
(q/T) |sum_{0 < t(z) <= T} c_z rho(z)|
  << ||rho||_infinity [
       (log X)^(-kappa_0) + 2^(-J) + q/T
     ].
```

There is no factor `J` in the correlation error because the dyadic
block lengths form a geometric series. The exceptional shadow obeys

```text
(1/log X) int_(S_X,J) dT/T
  << J*(log X)^(-kappa_0)
   = (log X)^(-kappa_0+o(1)).
```

Thus TPC-159 genuinely advances the actual periodic two-Mobius core
from source-native dyadic blocks to cumulative prefixes outside a
sparse dyadic shadow. Its level is
`L1_ACTUAL_PREFIX_ALMOST_ENDPOINT`.

It does not control every predetermined endpoint: a discrete endpoint
can lie in a set of logarithmic measure zero. It also gives only a
power of `log X`, not a fixed power of `X`; there is no `1/400`,
prime-pair, or twin-prime theorem.

Reproduce:

```powershell
python experiments/tpc159_dyadic_shadow_audit.py
python experiments/tpc159_dyadic_shadow_audit.py --check
```
