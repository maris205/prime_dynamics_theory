# Proof Package

## Theorem: coherence-controlled Gram quadratic

Let `H` be a complex Hilbert space with inner product conjugate-linear in its
first slot.  For a finite family, set

```text
g=sum_i lambda_i v_i,  a_i=|lambda_i| ||v_i||,
A={i:a_i>0},           D=sum_i a_i^2,  L=sum_i a_i.
```

Define `mu=0` for `|A|<=1`; otherwise take the maximum normalized absolute
inner product over distinct active indices.  Then

```text
| ||g||^2-D | <= mu(L^2-D),
max{D-mu(L^2-D),0} <= ||g||^2 <= D+mu(L^2-D).
```

If `D>0`, define `kappa=L^2/D`.  Then

```text
D[1-mu(kappa-1)]_+ <= ||g||^2 <= D[1+mu(kappa-1)],
1<=kappa<=|A|.
```

Consequently, `mu(kappa-1)<1` implies `g!=0`.

### Proof

Conjugate linearity in the first argument yields

```text
||g||^2-D=sum_(i!=j) conjugate(lambda_i)lambda_j<v_i,v_j>.
```

Terms involving an inactive index are zero.  On the active set, the absolute
value of the `(i,j)` term is at most `mu a_i a_j`.  The triangle inequality and
`sum_(i!=j)a_i a_j=L^2-D` prove the deviation bound.  Adding the universal
nonnegativity of a squared norm gives the floored lower estimate.  When `D>0`,
division by `D` gives the normalized form.  Finally,
`D<=L^2<=|A|D`; the left inequality expands `L^2`, while the right inequality
is Cauchy--Schwarz on the active coordinates.  Strict positivity of the lower
envelope proves noncancellation.  When `D=0`, every `lambda_i v_i=0`, so `g=0`
and the unnormalized statement holds; `kappa` is not defined.  QED.

## Corollary: inherited TPC-249 radii

For each lane let

```text
B_c^-=[D_c-mu_c(L_c^2-D_c)]_+,
B_c^+= D_c+mu_c(L_c^2-D_c).
```

The exact TPC-249 independent and global radii satisfy

```text
sum_c rho_c sqrt(B_c^-) <= sum_c rho_c||g_c||
                        <= sum_c rho_c sqrt(B_c^+),

rho sqrt(sum_c B_c^-) <= rho sqrt(sum_c||g_c||^2)
                       <= rho sqrt(sum_c B_c^+).
```

### Proof

Apply the theorem lane by lane.  Square root is monotone on nonnegative reals;
nonnegative multiplication and summation preserve order.  For the global
budget, sum the squared-norm bounds before taking the square root.  QED.

## Sharpness audit

### Upper coefficient one

For `m>=2` and `0<=mu<=1`, let `G` have diagonal `1` and every off-diagonal
entry `mu`.  Its eigenvalues are `1-mu` with multiplicity `m-1` and
`1+(m-1)mu` once, so `G` is PSD and is a Gram matrix.  With all weights one,

```text
lambda^*G lambda = m+mu(m^2-m)=D+mu(L^2-D).
```

Thus no universal coefficient below one can replace the upper coefficient.

### Signed-lower coefficient one

For `0<=mu<=1`, the matrix

```text
G=[[1,-mu],[-mu,1]]
```

has eigenvalues `1-mu` and `1+mu`.  With weights `(1,1)`,

```text
lambda^*G lambda=2-2mu=D-mu(L^2-D).
```

Thus no universal coefficient below one can replace the coefficient in the
signed lower estimate.

### Necessity of the nonnegative floor

A regular simplex with `m` unit vectors has off-diagonal Gram entry
`-1/(m-1)` and sums to zero.  Here `mu=1/(m-1)`, `kappa=m`, and the signed
lower endpoint is exactly zero.  A strict demonstration of negative raw lower
value is rational and collinear: take `(v_1,v_2,v_3)=(u,u,-u)` and weights
`(1,1,2)`.  Its rank-one PSD Gram matrix has coherence one,

```text
D=6, L=4, D-mu(L^2-D)=-4, ||g||^2=0.
```

Therefore the displayed nonnegative floor cannot be removed.

### Same-marginal obstruction

With weights `(1,1)` and two unit vectors, the aligned Gram
`[[1,1],[1,1]]` gives squared norm `4`, while the anti-aligned Gram
`[[1,-1],[-1,1]]` gives squared norm `0`.  The weights and marginal norms are
identical.  Marginal data alone therefore cannot improve the universal upper
bound `L^2` and cannot supply a positive universal lower bound.

## Proof-audit conclusion

All fixtures are PSD.  The coherence maximum is never taken over an empty
pair set, and `kappa` is never formed at `D=0`.  No sharpness statement is made
for every arbitrary parameter tuple.  No V59 coherence asymptotic or
arithmetic saving is used.
