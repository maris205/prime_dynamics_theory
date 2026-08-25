# TPC-248: Shared-Lane Gram-Ellipsoid Feasible Sets

Status: `PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET`

TPC-247 exposes, for every fixed physical output block `c`, the probes

```text
v_cb := A_cb beta_b in P_c H_x
```

against one shared lane `w_c=P_cw`.  This paper exactly classifies the joint
covariance vector before any Cartesian-product promotion.

Let `V:C^m -> H`, `Va=sum_b a_bv_b`, put `G=V*V`, and use an inner product
conjugate-linear in its first slot.  For

```text
y=V*W=(<v_b,W>)_b,
```

the closed radius-`rho` ball has exact image

```text
{y in ran(G): y*G^dagger y <= rho^2}.
```

The minimum-norm preimage is `VG^dagger y`.  For the exact sphere
`||W||=rho`, the image is the same solid ellipsoid iff `ker(V*)` is nonzero;
if `ker(V*)=0`, it is the equality shell.  The physical orientation
`z_b=<W,v_b>` is the conjugate ellipsoid over `conjugate(G)`.

Across output groups, a product of ellipsoids is exact only for an explicitly
Cartesian product of lane balls.  A global direct-sum norm budget instead gives
one coupled sum-of-Gram-energies ellipsoid.  In particular, the repeated-probe
fixture `v_1=v_2` gives a diagonal disk, not a bidisk.

```text
TPC248_SHARED_LANE_SOURCE_LOCK = PROVED_EXACT_FROM_TPC247
TPC248_BALL_IMAGE = PROVED_EXACT_GRAM_ELLIPSOID
TPC248_MINIMUM_NORM_PREIMAGE = PROVED_EXACT
TPC248_SPHERE_IMAGE_WITH_SLACK = PROVED_EXACT_SOLID_ELLIPSOID
TPC248_SPHERE_IMAGE_WITHOUT_SLACK = PROVED_EXACT_BOUNDARY_SHELL
TPC248_PHYSICAL_CONJUGATE_ORIENTATION = PROVED_EXACT
TPC248_CARTESIAN_GROUP_PRODUCT = PROVED_FOR_DECLARED_PRODUCT_DOMAIN
TPC248_CARTESIAN_PRODUCT_FROM_MARGINALS = UNJUSTIFIED
TPC248_GLOBAL_NORM_BUDGET = PROVED_EXACT_COUPLED_ELLIPSOID
TPC248_POLYDISK_PROMOTION = REFUTED_SCOPED
TPC248_ARITHMETIC_ADVANCE = NO
TPC248_FIXED_ATOM_CREDIT = 0
TPC248_L2 = NONE
TPC248_FULL_GATE_B = OPEN
TPC248_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC248_TWIN_PRIME_RESULT = NONE
TPC248_STATUS = PROVED_STRUCTURAL_L1_SHARED_LANE_GRAM_ELLIPSOID_FEASIBLE_SET
```

Strongest positive result: exact rank-degenerate joint feasible set and exact
ball/sphere/global-budget classification.  Strongest obstruction: local disk
marginals do not determine the joint set; a single shared lane can collapse a
bidisk to a diagonal disk.  Open theorem: extract a sharp weighted aggregate
radius from the source Gram matrices.  Reusable structure: analysis operator,
Gram range, pseudoinverse energy, and orthogonal-slack ledger.

`ROUND2_CLUE = CONTRACT_WEIGHTED_PROBES_INSIDE_EACH_SHARED_OUTPUT_LANE_BEFORE_SUMMING_ACROSS_OUTPUT_BLOCKS`
