# Bridge B V103: coherence-controlled Gram quadratic sharpness

Status: `PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS`

TPC-249 reduces each physical shared lane to the exact weighted probe

```text
g=sum_i lambda_i v_i,
||g||^2=lambda^*G lambda.
```

TPC-250 gives a computable structural envelope for this quadratic from its
diagonal weighted energy, weighted one-norm, and active coherence.  It does
not estimate those quantities on the asymptotic V59 source.

## 1. Total definitions

Put

```text
a_i=|lambda_i|||v_i||,
A={i:a_i>0},
D=sum_i a_i^2,
L=sum_i a_i.
```

When `|A|<=1`, define `mu=0`.  Otherwise,

```text
mu=max_(i!=j in A) |<v_i,v_j>|/(||v_i||||v_j||).
```

Thus the coherence is defined even when there is no active pair.  The
effective sparsity `kappa=L^2/D` is defined only when `D>0`.

## 2. Exact coherence envelope

Expanding the Gram quadratic with the inner product conjugate-linear in its
first slot gives

```text
||g||^2-D
 =sum_(i!=j) conjugate(lambda_i)lambda_j<v_i,v_j>.
```

Every active cross term has modulus at most `mu a_i a_j`, while
`sum_(i!=j)a_i a_j=L^2-D`.  Therefore

```text
| ||g||^2-D | <= mu(L^2-D),

[D-mu(L^2-D)]_+
 <= ||g||^2
 <= D+mu(L^2-D).
```

For `D>0`,

```text
D[1-mu(kappa-1)]_+
 <= ||g||^2
 <= D[1+mu(kappa-1)],

1<=kappa<=|A|.
```

In particular, `mu(kappa-1)<1` is a rigorous finite noncancellation
certificate.

## 3. TPC-249 radius inheritance

For lane `c`, write

```text
B_c^-=[D_c-mu_c(L_c^2-D_c)]_+,
B_c^+= D_c+mu_c(L_c^2-D_c).
```

The exact independent-lane radius satisfies

```text
sum_c rho_c sqrt(B_c^-)
 <= sum_c rho_c||g_c||
 <= sum_c rho_c sqrt(B_c^+).
```

For one global direct-sum budget,

```text
rho sqrt(sum_c B_c^-)
 <= rho sqrt(sum_c||g_c||^2)
 <= rho sqrt(sum_c B_c^+).
```

These are different domain ledgers and must not be interchanged.

## 4. Sharpness and obstruction

- Positive equicorrelated PSD Gram matrices attain the upper coefficient one.
- The PSD matrix `[[1,-mu],[-mu,1]]` attains the signed-lower coefficient
  one.
- A regular simplex attains the zero lower endpoint.
- The rational rank-one family `(u,u,-u)` with weights `(1,1,2)` has
  `D=6`, `L=4`, raw lower endpoint `-4`, and exact quadratic zero, so the
  nonnegative floor is necessary.
- Aligned and anti-aligned unit pairs with the same weights and marginal
  norms give exact squared norms `4` and `0`.  Hence marginal norms alone
  cannot improve the universal `L^2` upper endpoint or provide a positive
  lower bound.

The sharpness claim concerns universal constants and the floor.  It does not
assert a saturating Gram family for every arbitrary parameter tuple.

## 5. Route evaluation

Strongest positive result: a total, two-sided and universally sharp
coherence envelope for the exact TPC-249 Gram quadratic, including a strict
finite noncancellation criterion.

Strongest obstruction: when coherence is unavailable, fixed marginal norms
permit both full alignment and exact cancellation.

Open theorem: prove favorable asymptotics for the projected or unprojected
literal V59 values of `D_c`, `L_c`, and `mu_c`.

Reusable structure: diagonal energy + weighted one-norm + active coherence
-> exact quadratic envelope -> independent/global radius inheritance.

`ROUND2_CLUE = PROJECT_THE_LITERAL_LAMBDA_EQUALS_ONE_PROBES_ONTO_A_DECLARED_BLOCK_LONGITUDINAL_DIRECTION_AND_TEST_THE_STRICT_MARGIN`

## 6. Claim firewall

```text
TPC250_GRAM_DEVIATION_BOUND = PROVED_EXACT
TPC250_TWO_SIDED_COHERENCE_ENVELOPE = PROVED_EXACT
TPC250_EMPTY_PAIR_COHERENCE = PROVED_TOTAL_MU_ZERO
TPC250_KAPPA_DOMAIN = PROVED_ONLY_FOR_D_POSITIVE
TPC250_NONCANCELLATION_CONDITION = PROVED_IF_MU_TIMES_KAPPA_MINUS_ONE_LT_ONE
TPC250_INDEPENDENT_RADIUS_ENVELOPE = PROVED_EXACT_INHERITANCE
TPC250_GLOBAL_RADIUS_ENVELOPE = PROVED_EXACT_INHERITANCE
TPC250_UPPER_CONSTANT_SHARPNESS = PROVED_PSD_EQUICORRELATED
TPC250_SIGNED_LOWER_CONSTANT_SHARPNESS = PROVED_PSD_TWO_VECTOR
TPC250_NONNEGATIVE_FLOOR = PROVED_NECESSARY
TPC250_MARGINAL_ONLY_IMPROVEMENT = REFUTED_SCOPED
TPC250_ACTUAL_V59_COHERENCE_ASYMPTOTIC = OPEN
TPC250_ARITHMETIC_ADVANCE = NO
TPC250_FIXED_ATOM_CREDIT = 0
TPC250_L2 = NONE
TPC250_FULL_GATE_B = OPEN
TPC250_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC250_TWIN_PRIME_RESULT = NONE
TPC250_STATUS = PROVED_STRUCTURAL_L1_COHERENCE_CONTROLLED_GRAM_QUADRATIC_SHARPNESS
```
