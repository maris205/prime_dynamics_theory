# Bridge-B: TPC-332 growing control-average ensemble

## Purpose

TPC-332 is a hostile, disjoint-window replication of TPC-331.  It keeps the
same literal deleted-diagonal centered prime-shell operator, five coordinate
controls, four shell sign laws, and finite V59 source model, but moves to two
new origins and a three-rung source ladder.  The bridge is a finite certificate
only; the Session-named Route-A and Route-B evaluator files are absent from
this checkout.

## Frozen object

```text
origins       = {42001, 44001}
scales        = {2048, 4096, 8192}
source counts = {1024, 2048, 4096}
Q             = {24, 36, 54, 80}
exponents     = {1, 2}
H             = 66
controls      = identity, affine_(3,11), affine_(5,17), affine_(7,29), reversal
tail cutoff  = 50000
ratio guard   = 5e-8
```

Every source interval lies below the declared tail cutoff (including the
`t+2` shift).  The two origins are disjoint from the TPC-331 windows.  The
certificate contains 48 rows, 192 law-level mean/centered decompositions, and
six source-window `L2` records.

## Mathematical and finite results

For `w_j=P_jv`, `vbar=mean_j w_j`, and `z_j=w_j-vbar`, finite bilinearity gives

```text
mean_j E(w_j) = E(vbar) + mean_j E(z_j)
mean_j D(w_j) = D(vbar) + mean_j D(z_j)
mean_j O(w_j) = O(vbar) + mean_j O(z_j).
```

The source layer separately records the exact finite polarization identity

```text
||Lambda-b||_2^2 = ||Lambda||_2^2 + ||b||_2^2 - 2 <Lambda,b>.
```

The certified component census is:

| law | average negative/positive | coherent negative/positive | centered negative/positive |
|---|---:|---:|---:|
| all-plus | 0 / 48 | 1 / 47 | 0 / 48 |
| alternating index | 31 / 17 | 38 / 10 | 29 / 19 |
| mod-4 character | 48 / 0 | 44 / 4 | 47 / 1 |
| half split | 48 / 0 | 39 / 9 | 48 / 0 |

For the unpermuted all-plus residual, the sign census is `27 negative / 21
positive / 0 unresolved`, with ratio range
`[0.44646203339149909, 1.1102919670326215]`.  The all-plus average and centered
components remain positive on every one of the 48 rows, while the coherent
component has one negative row.  This is a structural replication, not a
canonical-sign theorem.

The source-native residual `L2` growth pairs (adjacent rungs, both origins)
have residual growth factors

```text
1.8736551016394614, 1.9695310092544431,
1.9140068638900343, 2.037675446375288.
```

The corresponding base-2 local slopes lie in
`[0.90585540926787733, 1.0269242825184262]`; residual energy per source changes
by factors in `[0.93682755081973068, 1.018837723187644]`.  These are finite
observations and do not certify a limit or a growing arithmetic bound.

## Claim firewall

```text
TPC332_EXACT_MEAN_CENTERED_DECOMPOSITION = PROVED_EXACT_FINITE
TPC332_SOURCE_NATIVE_VECTOR = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC332_SOURCE_L2_IDENTITY = PROVED_EXACT_FINITE_FLOAT64_REPLAY
TPC332_GROWING_ENSEMBLE = NUMERICALLY_CERTIFIED_FINITE_48_ROWS
TPC332_CONTROL_AVERAGE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
TPC332_CENTERED_POSITION_CENSUS = NUMERICALLY_CERTIFIED_FINITE_48_OF_48
TPC332_COHERENT_CENSUS = NUMERICALLY_CERTIFIED_FINITE_47_OF_48
TPC332_SOURCE_L2_GROWTH = NUMERICALLY_CERTIFIED_FINITE_OBSERVATION
TPC332_ARITHMETIC_ADVANCE = NO
TPC332_FIXED_POWER_CREDIT = 0
TPC332_GROWING_SOURCE_NATIVE_L2 = OPEN
TPC332_FULL_GATE_B = OPEN
TPC332_TWIN_PRIME_RESULT = NONE
TPC332_STATUS = NUMERICALLY_CERTIFIED_FINITE_GROWING_CONTROL_AVERAGE_ENSEMBLE
TPC332_ROUND2_CLUE = SEPARATE_SOURCE_L2_CROSS_TERM_AND_TEST_CONTROL_COVARIANCE_SPECTRUM
```

The strongest obstruction is that finite control averaging stabilizes the
positive components but does not stabilize the actual source-native all-plus
sign: the fresh ensemble still has both signs.  The next minimal question is
to isolate the arithmetic `L2` cross term and its prime/twin-prime support
before attempting any control-covariance theorem.

## Local fallback checks

```text
python -B papers/tpc-332-growing-control-average-ensemble/code/tpc332_growing_control_average_ensemble.py --check
python -B papers/tpc-332-growing-control-average-ensemble/experiments/tpc332_independent_checker.py --check
python -B papers/tpc-332-growing-control-average-ensemble/experiments/tpc332_growing_ensemble_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc332_growing_control_average_ensemble_checker.py --check
```

Normal and optimized local runs must have byte-identical stdout and empty
stderr.  A successful local bridge is not an official Route-A or Route-B
evaluation.
