# RH-386 theorem ledger

## Frozen input

For `x=p_y`, `L=log x`, and

```text
V(L) = L^(3/5) (log L)^(-1/5),
epsilon_x = (27/1000) L^(1801/1000) exp(-(1853/10000)V),
```

Johnston--Yang Theorem 1.4, equation (1.8), gives

```text
|theta(x)-x| <= epsilon_x x       (x>=23).
```

The transfer uses monotonicity of `epsilon` only for `L>=512`. The exact
fractions `27/1000`, `1801/1000`, `1853/10000`, `3/5`, and `-1/5` are
frozen in the certificate.

## Strict endpoint and source transfer

```text
P_r(y) = sum_{p>p_y} (p^2-1)^(-r)
       = integral_(x,infinity) h_r dtheta,
h_r(t) = (t^2-1)^(-r)/log t.
```

The exact identities are

```text
P_r(y) = (p_(y+1)^2-1)^(-r) + P_r(y+1),
P_r = -theta(x)h_r(x) - integral_x^infinity theta(t)h_r'(t)dt,
P_r-J_r = -E(x)h_r(x) - integral_x^infinity E(t)h_r'(t)dt.
```

The hazard

```text
q_r(t) = -h_r'(t)/h_r(t)
       = 2rt/(t^2-1) + 1/(t log t)
```

is decreasing, `J_r>=h_r(x)/q_r(x)`, and `xq_r(x)<=3r` for `x>=23`.
The two boundary contributions give `2xh_r+J_r`, hence

```text
|P_r/J_r-1| <= (6r+1)epsilon_x <= 7r epsilon_x,
|log(P_r/J_r)| <= 14r epsilon_x   if 7r epsilon_x<=1/2.
```

## Kernel ledger

The canonical, hypothesis-free middle comparison is

```text
0 <= log(J_r/I_2r)
   <= -r log(1-x^-2)
   <= r/(x^2-1).
```

The optional `4r/x^2` bound is only a coarser corollary and is not used in
the master ledger.

For `a_r=((2r-1)L)^(-1)`, substitution gives

```text
I_2r/K_r = G(a_r),
G(a) = integral_0^infinity e^-v/(1+av) dv,
1/(1+a) <= G(a) <= 1,
|log G(a)| <= a,
0 <= log G(a)+a <= 2a^2      (a<=1/4).
```

## Partition theorem

For `lambda=1^k1 2^k2 ...`, define

```text
ell = sum k_r,
d   = sum r k_r,
R   = max{r:k_r>0},
H   = sum k_r/(2r-1),
H2  = sum k_r/(2r-1)^2.
```

When `L>=512` and `7R epsilon_x<=1/2`:

```text
exact-J: |log(P_lambda/J_lambda)| <= 14d epsilon_x;
power-I: add d/(x^2-1);
leading-M: add H/L;
refined: |log(P_lambda/M_lambda)+H/L|
         <=14d epsilon_x+d/(x^2-1)+2H2/L^2.
```

Consequences:

- `d epsilon_x+d/x^2 -> 0` gives the exact- and power-kernel limits.
- Under that condition, the leading limit is equivalent to `H/L -> 0`.
- `log d=o(V)` and `H=o(L)` suffice.
- For one factor, `log R=o(V)` suffices uniformly; the sharper range is
  `R<=exp((0.1853-delta)V)` for fixed `delta in (0,0.1853)`.
- `lambda=1^floor(cL)` gives `P_lambda/M_lambda -> exp(-c)`.

The `d epsilon_x` condition is a robust sufficient consequence of the
available source upper bound, not a claim of logical necessity for the
actual signed prime error.

## Claim firewall

The following are all false: Gates A--E, growing clock, active phasewise
`c11`, adaptive capacity, effective threshold, operator/trace formula,
zeta-zero identification, proof of RH, and replacement of the VK theorem
by a finite fit. The 96-row artifact reproduces exact interfaces; it does
not prove the analytic source estimate.
