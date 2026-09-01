# TPC-331 derivation package

## 1. Finite control orbit

Let `I` be the finite source index set and let `P_1,...,P_m` be the five
permutation matrices frozen in TPC-330, with `m=5`.  For a source vector `v`
define

```text
w_j = P_j v
v_bar = (1/m) sum_j w_j
z_j = w_j - v_bar.
```

The modular-unit argument gives `P_j^T P_j=I`, so every `w_j` has the same
Euclidean norm and coordinate multiset as `v`.  By construction,
`sum_j z_j=0`.

## 2. General quadratic-form identity

For a real symmetric positive-semidefinite matrix `A`, write
`q_A(x)=x^T A x`.  Then

```text
mean_j q_A(w_j)
  = q_A(v_bar) + mean_j q_A(z_j).
```

Indeed, expand `w_j=v_bar+z_j` and use
`mean_j z_j=0`:

```text
mean_j [q_A(v_bar) + 2 v_bar^T A z_j + q_A(z_j)]
  = q_A(v_bar) + mean_j q_A(z_j).
```

This is a finite identity; it uses no limit, positivity estimate, or
arithmetic input.

## 3. Three forms used by the diagnostic

For a coherent shell matrix `C_e`, set

```text
A_E = C_e^T C_e
A_D = diag( sum_u C_e(u,t)^2 )_t
A_O = A_E - A_D.
```

Then

```text
E_e(x) = x^T A_E x = ||C_e x||_2^2
D_e(x) = x^T A_D x
O_e(x) = x^T A_O x = E_e(x)-D_e(x).
```

Applying the general identity to `A_E`, `A_D`, and `A_O` gives

```text
mean_j E_e(w_j) = E_e(v_bar) + mean_j E_e(z_j)
mean_j D_e(w_j) = D_e(v_bar) + mean_j D_e(z_j)
mean_j O_e(w_j) = O_e(v_bar) + mean_j O_e(z_j).
```

The last line is subtraction of the first two and is not an average of
ratios.  This distinction is essential: the certificate reports ratios only
after each of the three quadratic terms has been computed.

## 4. Relation to the Gram expansion

Writing `C_e x=sum_t x_t C_e e_t` gives

```text
E_e(x) = sum_t x_t^2 ||C_e e_t||_2^2
         + sum_(t != t') x_t x_t'
             <C_e e_t, C_e e_t'>.
```

The first term is `D_e(x)` and the second is `O_e(x)`.  Thus the new
mean/centered identity is a decomposition of the same signed Gram mass into
a control-orbit coherent part and a position-centered part.

## 5. Source model

The finite declared source is

```text
beta_o^(2)(t) = Lambda(t+2) - b^(2)(t)
b^(2)(t) = 2 C_2 1_(2 does not divide t)
             product_(p|t,p>2) (p-1)/(p-2).
```

The Euler product is evaluated through `50000`; the inherited lower/upper
tail enclosure and 100-digit logarithm midpoint protocol are retained.  The
source is therefore a finite declared model, not a theorem about the true
prime-pair correlation.

## 6. Numerical observables

For each row and law, the producer stores:

- the average quadratic triple `(E,D,O)`;
- the coherent triple at `v_bar`;
- the centered triple averaged over `z_j`;
- guarded ratios `E/D`, energy fractions, and identity residuals.

The ratio classification is negative when the outward interval lies below
`1`, positive when it lies above `1`, and unresolved otherwise.  The panel
has no unresolved component observation.  The largest float64 identity
residual is recorded rather than silently rounded away.

## 7. Exact anchor

At `[36001,36016]`, `Q=4`, `s=1`, use the shell `{5,7}` and the rational vector
`1_(t+2 prime)-1_(t odd)`.  All five permutations, their mean, and their four
centered vectors are rational.  The certificate stores reduced-fraction
digests for the identity, average, coherent, and centered triples, and checks
the three mean/centered identities symbolically.
