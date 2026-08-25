# TPC-256 proof package

## Theorem

For the source-frozen literal V59 coefficient and operator, on the
coefficient-independent ordered-rank midpoint Haar vector and for all
sufficiently large real `x`,

```text
<z_mid,beta>
 = [log(32/27)/sqrt(2)]sqrt(x)/log^2 x
   +O(sqrt(x)/log^3 x)>0,

<z_mid,A_x beta>
 = -[9log(32/27)/(2sqrt(2))+o(1)]x^(7/6)/log^3 x
```

in `C`.  The second scalar has eventually negative real part, is eventually
nonzero, and has normalized phase tending to `-1`.

Maximum status:

```text
PROVED_SOURCE_BACKED_L1_LITERAL_BETA_RANK_MIDPOINT_AND_DIAGONAL_DOMINANT_ADJOINT_ASYMPTOTIC
```

## Dependency ledger

| Step | Input | Output | Status |
|---|---|---|---|
| P1 | Floor/rank definitions | `ell,r=x/4+O(1)`, `rho=sqrt(x)/(2sqrt(2))+O(x^-1/2)` | PROVED |
| P2 | Consecutive interval counts | divisor Haar lane `O(U/rho)=O(x^-67/400)` | PROVED |
| P3 | de la Vallée Poussin PNT | `F(y)=Li(y)+O(y exp(-c sqrt(log y)))` | PROVED_SOURCE_BACKED |
| P4 | Second-order `1/log(xy)` expansion | child-mean difference `2log(32/27)/log^2x` | PROVED |
| P5 | P1--P4 | literal beta-Haar positive asymptotic | PROVED_SOURCE_BACKED |
| P6 | Weighted PNT | `B_Q=(9/2+o(1))x^(2/3)/log x` | PROVED_SOURCE_BACKED |
| P7 | TPC-255 exact compiler | diagonal/unit/hard/jump decomposition | PROVED_SOURCE_BACKED |
| P8 | Combined mask residue cases | `|v(t+h)|<=1_(q|h)+2/q` | PROVED |
| P9 | Schwartz decay | weighted first moment `O_psi(H^2/q)` | PROVED |
| P10 | One-boundary crossing count | hard/jump `O(x^(55/48+epsilon))` | PROVED |
| P11 | `epsilon<1/48` | diagonal dominance and complex phase | PROVED_SOURCE_BACKED |

## Quantifier ledger

- `x` is real and tends to infinity.
- The profile `psi_+` is fixed, smooth, supported in `[-1,1]`, and normalized
  by integral one.
- The operator, coefficient, prime shell, and rank split are the frozen
  literal objects; no modeled surrogate is substituted.
- Each remainder estimate holds for every fixed `epsilon>0`; diagonal
  dominance selects one fixed `0<epsilon<1/48`.
- Eventual positivity, negativity of the real part, and nonvanishing all mean
  there exists a profile-dependent finite threshold beyond which the
  statement holds for every real `x`.

## Hostile checks

### Rank and endpoint rounding

The proof uses `a=floor(x/2)`, `b=floor(x)`, and the ordered rank
`m=a+floor((b-a)/2)`.  Every endpoint differs from its scaled location by
`O(1)`.  After child normalization, replacing endpoints in a `Li` difference
costs `O(1/(x log x))`, which is absorbed by `O(log^-3 x)`.

### Prime powers

`Lambda(n)/log n` equals `1/k` at `n=p^k`, not merely the prime indicator.
The exact summatory identity includes all `k>=2`; their total is
`O(sqrt(y)log y)` and is absorbed by the strong PNT error.

### Divisor lane

The estimate does not use `sum mu(d)` cancellation.  It first cancels the
deterministic density `1/d` for each layer between the two child means.  The
subsequent triangle has only one endpoint discrepancy per child and divisor.

### Adjoint orientation

The inner product is conjugate-linear in the first slot.  TPC-255's adjoint
contains `conjugate(K_H)`; pairing with real `beta,z_mid` conjugates it back
to `K_H`.  No evenness, reality, or self-adjointness is inserted.

### Output-unit separation

The two algebraic pieces have period sums `-1/(q-1)` and `+1/(q-1)`.  Applying
the centered Poisson theorem to either piece separately is invalid.  The
pointwise majorant and first-moment estimate retain their sum `v`.

### Boundary exponents

The outer and inner crossings are each bounded by `|h|`, not by the full
interval length.  The resulting exponent is exactly

```text
1/3+42/32-1/2=55/48.
```

The diagonal exponent is `56/48`; the fixed gap is `1/48`, not a logarithmic
margin.

### Complex phase

The asymptotic is an equality in `C` with a negative-real leading constant.
The safe branch-free consequence is `S/|S| -> -1`.  The claims `S is real`
and `principal Arg(S) -> +pi` are explicitly not made.

## Computational role

The executable files reproduce exact finite identities, source hashes,
schema, mask bounds, and crossing counts.  The two finite beta samples are
`NUMERICAL_OBSERVATION`.  The asymptotic theorem is proved from the cited PNT,
the frozen exact TPC-255 identity, and the displayed analytic estimates; it
is not extrapolated from those samples.
