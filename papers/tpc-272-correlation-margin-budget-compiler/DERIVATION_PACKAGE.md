# TPC-272 derivation package

## 1. Coordinates

On a positive finite row let

```text
C = C_perp,  W = W_perp,  G = G_perp,
R = sqrt(W G),  m = |C|/R.
```

The TPC-271 rational coordinates satisfy

```text
Xi   = (W G)^3/N^10,
Xi_C = |C|^6/N^10,
```

and therefore

```text
m^6 = Xi_C/Xi,       Xi/Xi_C = m^(-6).
```

All divisions used by the certificate have positive denominators.

## 2. Conditional endpoint compiler

Put `E0=5/3` and `E*=1997/1200=E0-1/400`. Assume `eta>=0` and, for every
sufficiently large `x`,

```text
|C(x)| <= A x^(E0-sigma_c+epsilon),
m(x) >= b x^(-eta-epsilon),       A,b>0.
```

Since `R=|C|/m`,

```text
R <= (A/b) x^(E0-sigma_c+eta+2 epsilon),
|C|+R <= A(1+b^(-1)) x^(E0-sigma_c+eta+2 epsilon).
```

After renaming the harmless epsilon, the endpoint has effective saving
`sigma_c-eta`.  It beats the target exponent precisely under the strict
condition

```text
sigma_c - eta > 1/400.
```

If a raw scalar estimate is written with saving `delta_c` and loss
`lambda_c`, substitute `sigma_c=delta_c-lambda_c`; the condition becomes
`delta_c-lambda_c-eta>1/400`.

## 3. Sharp converse

For `W,G>0` and `0<m<=1`, define in `R^2`

```text
w = (sqrt(W),0),
g = sqrt(G)*(-m,sqrt(1-m^2)).
```

Then `||w||^2=W`, `||g||^2=G`, `C=-sqrt(WG)m`, `R=sqrt(WG)`, and the
phase is negative real for every `m`.  Letting `m` tend to zero makes the
radius-to-scalar ratio diverge.  Thus phase sign and norm data do not imply a
positive correlation margin.

## 4. Finite interval transfer

TPC-271 stores positive intervals for `Xi_C` and `Xi`.  The producer forms
`[Xi_C,-/Xi_+]` and `[Xi_C,+/Xi_-]`, exactly as positive interval division
requires.  The independent checker recomputes these fractions directly from
the parent JSON rather than importing the producer.

The most severe registered diagnostic is `96->192`: its sixth-power margin
ratio is below `(1/32)^6` while both endpoint phase labels remain negative
real.  This is a finite audit only; it is not an asymptotic lower-bound
counterexample.
