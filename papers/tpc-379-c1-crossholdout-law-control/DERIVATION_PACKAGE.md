# TPC-379 derivation package

## 1. Common finite operator

For `I=[a,a+N-1]` and `p` in `(Q,2Q]`, define the unsigned component

```text
K_p(u,t) = p (p/Q)^2 66^2/(66^2+(u-t)^2)
            (1_{p|(u-t)} - 1/(p-1))
            1_{u!=t} 1_{p not|u} 1_{p not|t}.
```

For a declared sign law `ell`, let `s_p(ell)` be its sign on the ordered
prime shell and set

```text
A_ell(u,t) = sum_p s_p(ell) K_p(u,t)
G(u)       = sum_t sum_p K_p(u,t)^2
T_ell      = A_ell / sqrt(G(u)G(t)).
```

The four frozen laws are

```text
s_p(all_plus)          = 1
s_p(alternating_index) = (-1)^index(p)
s_p(mod4_character)    = 1 if p=1 (mod 4), -1 otherwise
s_p(half_split)        = 1 for the first half of the ordered shell,
                         -1 for the second half.
```

The geometry `G` is deliberately common to all four laws.  For block index
`b(u)=floor((u-a)/256)`, define

```text
B_ell(u,t) = T_ell(u,t) 1_{|b(u)-b(t)| <= 1},
R_ell      = T_ell-B_ell.
```

## 2. Exact finite relations

The geometry is a finite sum of nonnegative rational squares.  The selected
grid indices, endpoint interval separation, sign vectors, and c=1 mask are
literal finite definitions.  The exact 13-point anchor `[1200001,1200014)`
at `Q=8` has positive geometry and symmetric rational matrices for all four
laws.  For every selected unit eigenvector `v` of `T_ell`,

```text
v^T B_ell v + v^T R_ell v = v^T T_ell v.
```

These are finite identities.  They do not provide a bound uniform in the
origin, count, sign law, or Q, and they do not identify a source-valid
arithmetic normalization.

## 3. Finite law-control result

The complete panel has 36 rows `(origin,Q,law)`.  Its band spectral profile by
law and increasing Q is

```text
all_plus          = (0,3,3)
alternating_index = (0,0,0)
mod4_character    = (0,0,0)
half_split        = (0,0,0).
```

The total spectral-cap census is 6/36 and the Schur-cap census is 0/36.  The
largest band spectral values by law are respectively

```text
0.65334758792533143, 0.0094084540584888146,
0.011835976723613296, 0.2117349490215118.
```

Thus the all-plus threshold is a finite sign-law-dependent feature of this
declared model.  It is not a theorem that the signed controls are arithmetical
or that all-plus is physically privileged.

## 4. What this does not derive

The result does not derive law uniformity, origin uniformity, window-scale
uniformity, cross-block causality, a growing masked-operator estimate, a
source-uniform arithmetic `L2` estimate, a power saving, Route-B reassembly,
or a twin-prime theorem.  It pays zero fixed-power credit and remains a
finite obstruction/diagnostic within the established TPC dynamical family.
