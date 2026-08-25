# Derivation Package

## 1. Source-locked quadratic

TPC-249 supplies, for each shared lane, the literal contraction

```text
g = sum_i lambda_i v_i,
||g||^2 = lambda^* G lambda,
G_ij = <v_i,v_j>.
```

The inner product is conjugate-linear in the first slot.  Hence

```text
||g||^2 = sum_(i,j) conjugate(lambda_i) lambda_j <v_i,v_j>.
```

No conjugation is inserted into the definition of `g`.

## 2. Total edge-case definitions

Set

```text
a_i = |lambda_i| ||v_i||,
A = {i : a_i>0},
D = sum_i a_i^2,
L = sum_i a_i.
```

If `|A|<=1`, define `mu=0`; there is no empty maximum.  If `|A|>=2`, define

```text
mu = max_(i!=j in A) |<v_i,v_j>|/(||v_i|| ||v_j||).
```

An active index has nonzero `lambda_i` and nonzero `v_i`, so every denominator
in this maximum is positive.  Define `kappa=L^2/D` only when `D>0`.  When
`D=0`, every `a_i` and every summand `lambda_i v_i` vanish, so `g=0`, `L=0`,
and the unnormalized theorem reads `0<=0` without forming `kappa`.

## 3. Absolute deviation

Split the Gram quadratic into its diagonal and off-diagonal parts:

```text
||g||^2-D
 = sum_(i!=j) conjugate(lambda_i) lambda_j <v_i,v_j>
 = 2 Re sum_(i<j) conjugate(lambda_i) lambda_j <v_i,v_j>.
```

Inactive terms vanish.  For active `i!=j`, coherence gives

```text
|conjugate(lambda_i) lambda_j <v_i,v_j>| <= mu a_i a_j.
```

Therefore

```text
| ||g||^2-D |
 <= mu sum_(i!=j) a_i a_j
 = mu (L^2-D).
```

Intersecting the signed lower estimate with `||g||^2>=0` gives

```text
max{D-mu(L^2-D),0} <= ||g||^2 <= D+mu(L^2-D).
```

## 4. Normalization

For `D>0`, divide by `D` and use `kappa=L^2/D`:

```text
D[1-mu(kappa-1)]_+ <= ||g||^2 <= D[1+mu(kappa-1)].
```

Since all active `a_i` are positive,

```text
D <= L^2 <= |A| D,
```

where the first inequality follows by dropping positive cross terms and the
second is Cauchy--Schwarz.  Thus `1<=kappa<=|A|`.  If
`mu(kappa-1)<1`, the lower bound is strictly positive and `g!=0`.

## 5. Transfer to TPC-249 radii

For lane `c`, attach subscripts to `g,D,L,mu` and write

```text
B_c^- = [D_c-mu_c(L_c^2-D_c)]_+,
B_c^+ = D_c+mu_c(L_c^2-D_c).
```

TPC-249's exact independent-budget radius

```text
R_ind = sum_c rho_c ||g_c||
```

obeys

```text
sum_c rho_c sqrt(B_c^-) <= R_ind <= sum_c rho_c sqrt(B_c^+).
```

Its exact global direct-sum-budget radius

```text
R_glob = rho sqrt(sum_c ||g_c||^2)
```

obeys

```text
rho sqrt(sum_c B_c^-) <= R_glob <= rho sqrt(sum_c B_c^+).
```

These are structural envelopes.  They do not estimate the actual V59 values
of `mu_c`, `D_c`, or the Gram quadratic asymptotically.

## 6. Sharpness ledger

- Upper coefficient: for `m>=2` and `0<=mu<=1`, the Gram with diagonal `1`
  and off-diagonal `mu` is PSD and positive unit weights give equality above.
- Signed-lower coefficient: `[[1,-mu],[-mu,1]]` is PSD for `0<=mu<=1`, and
  unit weights give equality in the signed lower estimate.
- Zero floor: a regular simplex cancels exactly at raw lower value zero.  The
  rational rank-one family `(u,u,-u)` with weights `(1,1,2)` has raw lower
  value `-4` and exact norm zero.
- Marginal obstruction: unit weights and unit norms allow Gram matrices
  `[[1,1],[1,1]]` and `[[1,-1],[-1,1]]`, producing squared norms `4` and `0`.

The constructions prove universal sharpness of the two coefficients and of
the floor.  They do not promise saturation for every prescribed tuple of
`(mu,kappa,|A|)`.
