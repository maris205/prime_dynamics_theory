# Bridge B V105: declared-partition refinement calculus and singleton degeneracy

Date: 2026-08-25

Status: `PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY`

TPC-252 audits the freedom left in TPC-251's exhaustive declared hard
partition.  It keeps the literal TPC-247 source scalar fixed and changes only
the block-averaging projection.

## 1. Frozen scalar and block-averaging projection

Let `H=C^I`, where `I` is finite and nonempty, and retain

```text
g=A_x beta,
C_x=<w,g>.
```

The inner product is conjugate-linear in the first slot.  For an exhaustive
partition `P` into nonempty coordinate blocks, let

```text
u_J=|J|^(-1/2)1_J,
M_P=sum_(J in P) u_J tensor u_J.
```

Thus `M_P` is the orthogonal projection onto the block-constant subspace.
The TPC-251 decomposition can be written without changing the source:

```text
C_long(P)=<M_P w,M_P g>,
Q_trans(P)=<(I-M_P)w,(I-M_P)g>,
C_x=C_long(P)+Q_trans(P).
```

The partition remains a declared modeling choice.  No hard partition is
identified with the smooth bounded-overlap V59 partition.

## 2. One binary refinement is a rank-one covariance transfer

Suppose `P'` is obtained by replacing one block `J` by nonempty disjoint
children `J_1,J_2`.  Put `n_r=|J_r|`, `n=n_1+n_2`, and

```text
z=sqrt(n_2/(n_1 n))1_(J_1)-sqrt(n_1/(n_2 n))1_(J_2).
```

The vector `z` is unit, is orthogonal to the old flat direction `u_J`, and is
orthogonal to every other old block-flat direction.  The refined
block-constant space adds exactly this contrast:

```text
M_(P')=M_P+z tensor z.
```

Consequently, with `w,g` fixed,

```text
C_long(P')-C_long(P)=conjugate(<z,w>)<z,g>,
Q_trans(P')-Q_trans(P)=-conjugate(<z,w>)<z,g>.
```

The refinement therefore transfers one signed covariance term between the
two ledgers.  Neither `C_long` nor its modulus is monotone under refinement.

For a fixed auxiliary probe family `v_b`, the output projection alone also
has the rank-one update

```text
G_perp_(P')(b,b')
 =G_perp_P(b,b')-conjugate(<z,v_b>)<z,v_b'>.
```

This fixed-probe identity is not a comparison of the common input/output
TPC-251 Gram matrices after their input block labels are repartitioned; that
operation changes the probe family itself.

## 3. Exact transverse radius is nonincreasing

Only the split block changes.  Resolve its old residuals into the two child
residuals plus the contrast component.  If the child residual norms are
`a_1,a_2` for `w` and `b_1,b_2` for `g`, the refined contribution is

```text
a_1 b_1+a_2 b_2
 <=sqrt(a_1^2+a_2^2)sqrt(b_1^2+b_2^2)
 <=||w_J^perp||||g_J^perp||.
```

Hence

```text
R_trans(P')<=R_trans(P).
```

No intermediate-refinement monotonicity for the computable `R_coh` follows
from TPC-250 or TPC-251, because repartitioning changes both the projected
probe families and their coherence envelopes.

## 4. Singleton collapse and exact optimization ceiling

For the singleton partition `P_atom`, every block-flat direction is a
coordinate basis vector.  Therefore

```text
M_(P_atom)=I,
C_long(P_atom)=C_x,
Q_trans(P_atom)=0.
```

Every projected source probe is zero.  With TPC-250's total empty-pair
convention,

```text
G_perp=D=L=mu=U=R_trans=R_coh=0.
```

The ratio `kappa=L^2/D` is not formed at `D=0`.

For any declared partition and fixed independently certified `E>=0`, TPC-251
gives

```text
[|C_long(P)|-R_coh(P)-E]_+ <= [|C_x|-E]_+.
```

The singleton partition attains equality, so

```text
max_P [|C_long(P)|-R_coh(P)-E]_+ = [|C_x|-E]_+.
```

Thus optimization over freely declared partitions cannot strengthen the
direct reverse-triangle certificate from `|F-C_x|<=E`.  At `F=C_x,E=0`, the
singleton criterion is exactly the assertion `C_x!=0`; it is not an
independent proof of that assertion.

## 5. Same-source synthetic non-invariance witness

Keep the finite source data fixed:

```text
A=[[0,1],[1,0]],
beta=(-1,1),
w=(1,-1),
g=A beta=(1,-1),
C=<w,g>=2.
```

For the one-block partition,

```text
C_long=0,
Q_trans=R_trans=R_coh=2.
```

For the singleton partition,

```text
C_long=2,
Q_trans=R_trans=R_coh=0.
```

The matrix is real and has the deleted diagonal required by the finite source
operator algebra, but this is
`SYNTHETIC_EXACT_FINITE_SOURCE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_ARITHMETIC_INSTANCE`.
It proves existential partition non-invariance, not instability for every
source and not actual V59 arithmetic instability.

## 6. Route evaluation

Strongest positive result: binary refinement has an exact rank-one covariance
transfer law, the exact transverse radius is nonincreasing, and the complete
partition optimization ceiling is attained by singleton collapse.

Strongest obstruction: a freely selected partition can move the entire known
scalar into the nominal longitudinal center and erase the projected radius,
so favorable margin created solely by refinement is tautological rather than
arithmetic credit.

Open theorem: freeze a nontrivial source-only partition before inspecting the
coefficient realization, then estimate one actual V59 contrast product and
the associated projected radius on a common physical clock.

Reusable structure: block-averaging projection -> binary contrast -> rank-one
covariance transfer -> transverse-radius monotonicity -> singleton optimization
firewall.

`ROUND2_CLUE = FREEZE_A_NONTRIVIAL_SOURCE_ONLY_PARTITION_TREE_AND_TEST_ONE_LITERAL_V59_BINARY_CONTRAST_BEFORE_ANY_MARGIN_OPTIMIZATION`

## 7. Claim firewall

```text
TPC252_LITERAL_V59_SINGLETON_IDENTITY = PROVED_EXACT_FINITE
TPC252_BINARY_REFINEMENT_PROJECTION = PROVED_EXACT_RANK_ONE
TPC252_BINARY_REFINEMENT_COVARIANCE_TRANSFER = PROVED_EXACT
TPC252_FIXED_PROBE_PROJECTED_GRAM_UPDATE = PROVED_EXACT_WITH_FIXED_PROBE_FIREWALL
TPC252_TRANSVERSE_RADIUS_REFINEMENT = PROVED_NONINCREASING
TPC252_SINGLETON_PROJECTED_GRAM_AND_RADIUS = PROVED_ZERO
TPC252_PARTITION_MARGIN_OPTIMIZATION = PROVED_EQUAL_TO_DIRECT_BOUND
TPC252_SAME_SOURCE_SYNTHETIC_NONINVARIANCE = PROVED_EXACT
TPC252_EVERY_SOURCE_PARTITION_INSTABILITY = REFUTED_SCOPED
TPC252_ACTUAL_V59_ARITHMETIC_INSTABILITY = OPEN
TPC252_CANONICAL_PARTITION = NOT_CLAIMED
TPC252_ARITHMETIC_ADVANCE = NO
TPC252_FIXED_ATOM_CREDIT = 0
TPC252_L2 = NONE
TPC252_FULL_GATE_B = OPEN
TPC252_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC252_TWIN_PRIME_RESULT = NONE
TPC252_STATUS = PROVED_STRUCTURAL_L1_DECLARED_PARTITION_REFINEMENT_DEGENERACY
```
