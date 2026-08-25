# Bridge B V104: literal V59 declared-block longitudinal--transverse margin compiler

Status: `PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER`

TPC-251 returns the TPC-247 source scalar to one shared physical output lane
per block, specializes the TPC-249 weights to the literal value one, and uses
the TPC-250 coherence envelope only after the probes have been projected.

## 1. Exact literal source contraction

Fix a finite nonempty coordinate set with an exhaustive declared partition
into nonempty blocks.  For the TPC-247 source objects,

```text
v_cb=P_c A_x P_b beta,
w_c=P_c w.
```

The actual scalar uses `lambda_cb=1`.  Therefore

```text
g_c=sum_b v_cb=P_c A_x beta,
C_x=<w,A_x beta>=sum_c<w_c,g_c>.
```

No tagged output copies are introduced.

## 2. Declared block-flat split

For block `J_c`, choose

```text
u_c=|J_c|^(-1/2)1_(J_c).
```

This direction is canonical only relative to the declared block.  Neither the
partition nor this direction is asserted to be V59-canonical, and it is not
the TPC-219 prime-label longitudinal object.

Set

```text
a_c=<u_c,w_c>,       b_c=<u_c,g_c>,
w_c_perp=w_c-a_cu_c,
m_cb=<u_c,v_cb>,
v_cb_perp=v_cb-m_cbu_c,
g_c_perp=sum_b v_cb_perp.
```

Conjugate-linearity in the first slot gives the exact identity

```text
C_x=C_long+Q_trans,
C_long=sum_c conjugate(a_c)b_c,
Q_trans=sum_c<w_c_perp,g_c_perp>.
```

The projected Gram matrix is not the original Gram matrix:

```text
G_c_perp(bb')=G_c(bb')-conjugate(m_cb)m_cb'.
```

## 3. Projected coherence radius

Let `d_cb=||v_cb_perp||`, and compute `D_c,L_c,mu_c` from these projected
probes using the TPC-250 empty-pair convention.  Define the nonnegative root

```text
U_c=sqrt(D_c+mu_c(L_c^2-D_c)).
```

Then

```text
||g_c_perp||<=U_c,

R_trans=sum_c||w_c_perp||||g_c_perp||,
R_coh=sum_c||w_c_perp||U_c,

|C_x-C_long|<=R_trans<=R_coh.
```

Coherence of the unprojected probes cannot replace `mu_c` without separately
paying the rank-one Gram subtraction.

## 4. Conditional external margin

For any independently certified scalar `F` and `E>=0` satisfying
`|F-C_x|<=E`,

```text
|F-C_long|<=R_coh+E,
|F|>=[|C_long|-R_coh-E]_+.
```

Hence

```text
|C_long|>R_coh+E
```

is a rigorous sufficient condition for `F!=0`.  TPC-243 does not
automatically provide this `F,E` pair: common-synthesis identification and
coefficient-norm payment remain separate inputs.

For the block-flat orthonormal pair

```text
u=(1,1,1,1)/2,
t=(1,-1,1,-1)/2,
w=u+t,
g=u-t,
```

one has `C_long=1`, `Q_trans=-1`, `R_trans=1`, and total scalar zero.
Thus equality is insufficient and the strict endpoint is necessary.

## 5. Exact finite replay

The exact rational eight-coordinate replay verifies

```text
C_long=11/2,
Q_trans=-1,
C_x=9/2,
R_trans=R_coh=1,
F=4,
E=1/2,
strict lower margin=4.
```

It is explicitly classified as
`SYNTHETIC_EXACT_FINITE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_ARITHMETIC_INSTANCE`.
An independent checker rejects fifteen mutation classes, and the stress
suite checks 160 exact-rational declared-partition families.

## 6. Route evaluation

Strongest positive result: the literal `lambda=1` V59 source scalar now has
an exact declared-block longitudinal/transverse decomposition, a projected
Gram/coherence radius, and an explicit conditional nonvanishing margin.

Strongest obstruction: equality permits exact transverse cancellation, while
the partition, projected source parameters, and external error remain unpaid.

Open theorem: on one literal V59 clock, prove
`|C_long|>R_coh+E` with all three terms source-certified.

Reusable structure: exhaustive source blocks -> shared-lane contraction ->
block-flat projection -> rank-one Gram subtraction -> projected coherence
radius -> external strict margin.

`ROUND2_CLUE = ESTIMATE_THE_LITERAL_BLOCK_LONGITUDINAL_CENTER_AND_PROJECTED_COHERENCE_RADIUS_ON_ONE_V59_CLOCK_OR_BUILD_A_SOURCE_LEVEL_MARGIN_OBSTRUCTION`

## 7. Claim firewall

```text
TPC251_LITERAL_LAMBDA_ONE_CONTRACTION = PROVED_EXACT
TPC251_EXHAUSTIVE_HARD_PARTITION = PROVED_FOR_DECLARED_MODELING_CHOICE
TPC251_BLOCK_FLAT_DIRECTION = PROVED_FOR_DECLARED_MODELING_CHOICE
TPC251_LONGITUDINAL_TRANSVERSE_IDENTITY = PROVED_EXACT
TPC251_PROJECTED_GRAM_SUBTRACTION = PROVED_EXACT
TPC251_PROJECTED_COHERENCE_UPPER = PROVED_EXACT_TPC250_INHERITANCE
TPC251_TRANSVERSE_RADIUS_CHAIN = PROVED_EXACT
TPC251_EXTERNAL_MARGIN_COMPILER = CONDITIONAL_THEOREM_ON_CERTIFIED_E
TPC251_STRICT_NONVANISHING = CONDITIONAL_THEOREM_ON_STRICT_MARGIN
TPC251_EQUALITY_NONVANISHING = REFUTED_SCOPED
TPC251_FIXED_SOURCE_DISK_IMAGE = NOT_CLAIMED
TPC251_TPC243_EXTERNAL_ERROR = CONDITIONAL_INPUT_NOT_AUTOMATIC
TPC251_ACTUAL_V59_PROJECTED_COHERENCE_ASYMPTOTIC = OPEN
TPC251_PAYABLE_LONGITUDINAL_DOMINANCE = OPEN
TPC251_ARITHMETIC_ADVANCE = NO
TPC251_FIXED_ATOM_CREDIT = 0
TPC251_L2 = NONE
TPC251_FULL_GATE_B = OPEN
TPC251_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC251_TWIN_PRIME_RESULT = NONE
TPC251_STATUS = PROVED_STRUCTURAL_L1_LITERAL_V59_DECLARED_BLOCK_LONGITUDINAL_TRANSVERSE_MARGIN_COMPILER
```
