# TPC-333 derivation package

## 1. Polarization

For finite real vectors `a,b`, expand

```text
||a-b||_2^2 = <a-b,a-b>
              = ||a||_2^2 + ||b||_2^2 - 2<a,b>.
```

Set `a=Lambda` and `b=b^(2)` to obtain the declared source identity.

## 2. Dimensionless diagnostics

Let `S=||Lambda||_2^2+||b||_2^2` and define

```text
kappa = 2<Lambda,b>/S,
rho = ||Lambda-b||_2^2/S = 1-kappa,
corr = <Lambda,b>/(||Lambda||_2 ||b||_2).
```

These quantities separate three possibilities: near orthogonality
(`kappa` near zero), near total cancellation (`kappa` near one), and a
finite mixed regime.  No inequality in this package makes a claim about
`x -> infinity`.

## 3. Scale comparison

For nested windows at the same origin, compare each term by the ratio of its
large-scale value to its small-scale value.  The comparison is descriptive:
the spaces have different dimensions and the inherited source cutoff remains
fixed.

## 4. Exact anchor

With `Lambda=(3,-2,5,1)` and `b=(1,1,-1,2)`, the residual is
`(2,-3,6,-1)`.  The four exact values are

```text
||Lambda||^2 = 39, ||b||^2 = 7, <Lambda,b> = -2,
||Lambda-b||^2 = 50 = 39+7-2(-2).
```

The machine certificate stores reduced-fraction digests of these values.
