# Bridge B V123 / TPC-270: cross-scale endpoint-normalized radius

Date: 2026-08-27

Status: `NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT`

TPC-269 established a finite growing-cutoff/profile-transfer interface but
left the size of the Schur residual radius unmeasured across scale. TPC-270
adds that missing finite observable while retaining the literal V59 physical
operator, prime shell, masks, deleted diagonal, beta source, cutoff registry,
convex profile interface, and rank-three block projection.

## Frozen finite object

For each registered row, let `R_(N,theta)^2` denote the product of the two
positive residual squared norms after removal of the three block contrasts.
The endpoint-normalized observable is

```text
Xi_(N,theta) = (R_(N,theta)^2)^3 / N^10
             = (R_(N,theta)/N^(5/3))^6.
```

The second expression explains the endpoint exponent; the first expression
keeps every finite certificate rational after outward interval evaluation.
The base registry is

```text
(N,H,Q) = (64,15,4), (96,20,5), (128,24,5),
          (192,32,6), (256,38,6), (384,50,7),
z_N = floor(log N).
```

Three matched `theta=1/2` controls are recorded at `N=96,128,256`.

## Certified finite result

The four dyadic ratio intervals for the base rows are

```text
64->128:  [0.231753859227, 0.231847466257]
96->192:  [23.9597604587, 23.9685339622]
128->256: [7.17162080603, 7.17448479796]
192->384: [0.802913654645, 0.803207691586]
```

Thus the certified finite pattern is `DROP_RISE_RISE_DROP`. The three profile
ratios satisfy

```text
1/2 < Xi_(N,1/2) / Xi_(N,0) < 3/4,
N in {96,128,256}.
```

The producer uses the released TPC-269 exact interval engine. The independent
checker reconstructs the sieve, Mobius weights, prime shell, two kernels,
projection, radius, and normalization without importing that producer. The
normalization stress audit rechecks the pattern and rejects malformed or
asymptotically promoted certificates.

```text
TPC270_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
TPC270_ROUTE_ADVANCE = YES_SCOPED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
TPC270_ENDPOINT_NORMALIZATION = PROVED_EXACT_FINITE_IDENTITY
TPC270_CROSS_SCALE_VARIATION = NUMERICALLY_CERTIFIED_FINITE
TPC270_PROFILE_CONTROL = NUMERICALLY_CERTIFIED_FINITE
TPC270_FINITE_STABILITY = REFUTED_SCOPED
TPC270_SOURCE_LEVEL_RADIUS = OPEN_ASYMPTOTIC
TPC270_SOURCE_LEVEL_PHASE = OPEN_ASYMPTOTIC
TPC270_FIXED_POWER_CREDIT = 0
TPC270_ARITHMETIC_ADVANCE = NO
TPC270_L2 = NONE
TPC270_FULL_GATE_B = OPEN
TPC270_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC270_TWIN_PRIME_RESULT = NONE
TPC270_STATUS = NUMERICALLY_CERTIFIED_FINITE_CROSS_SCALE_RADIUS_NORMALIZATION_AUDIT
TPC270_ROUND2_CLUE = TEST_SOURCE_LEVEL_RADIUS_UPPER_BOUND_WITH_EXPLICIT_POWER_NORMALIZATION
```

Strongest positive result: the exact sixth-power endpoint normalization and a
four-pair, threshold-separated dyadic certificate with an independently
reproduced profile-control band.

Strongest obstruction: the same declared growing proxy exhibits both a more
than `23`-fold dyadic rise and a drop below `1/4`; finite normalized radius is
therefore not stable on this registry.

Open theorem: a source-compatible, uniform radius bound with an explicit
power and effective clock, followed by signed phase and arithmetic `L2`
reassembly.

Reusable structure: positive outward interval for `R^2` -> rational sixth-power
normalization -> positive interval division -> scale/profile classification.

The Session-named `propose.md` and route evaluator files are absent from this
checkout. The project proof package, theorem ledger, certificate, independent
replay, stress audit, bridge checker, and `AGENTS.md` are used as the
fail-closed fallback. This release makes no arithmetic Route-B closure and no
twin-prime claim.
