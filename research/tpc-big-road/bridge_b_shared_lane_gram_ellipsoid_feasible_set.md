# Bridge B: shared-lane Gram-ellipsoid feasible set

TPC-247 exposes, for every fixed output block `c`, the source-native probes

```text
v_cb=A_cb beta_b in P_c H_x
```

paired with the single lane `w_c=P_cw`.  TPC-248 classifies their joint
covariance vector exactly.  For the analysis operator `V*W=(<v_b,W>)_b` and
`G=V*V`,

```text
V*{W:||W||<=rho}
 = {y in ran(G): y*G^dagger y<=rho^2}.
```

The minimum preimage is `VG^dagger y`.  Exact spheres fill the solid ellipsoid
when `ker(V*)` is nonzero and otherwise give its equality shell.  Physical
covariances `<W,v_b>` use the entrywise-conjugate Gram ellipsoid.

Independent output-lane balls produce a product only because their domain is
declared Cartesian.  One global direct-sum norm budget instead gives

```text
sum_c y_c*G_c^dagger y_c<=rho^2.
```

Repeated probes give a diagonal disk rather than a bidisk, so marginal-disk
promotion is strictly refuted.

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

The next bridge contracts weighted probes inside each output lane before any
cross-output summation.  No arithmetic saving is assigned here.
