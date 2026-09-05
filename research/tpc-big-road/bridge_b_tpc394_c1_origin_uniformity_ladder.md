# Bridge-B: TPC-394 c=1 origin-uniformity ladder

This is a local, fail-closed Bridge-B artifact for the finite TPC-394 release.
It is repository evidence of reproducibility and contract consistency, not an
official Route-A or Route-B evaluator decision.

```text
TPC394_SCHEMA = TPC394_C1_ORIGIN_UNIFORMITY_LADDER_V1
TPC394_STATUS = NUMERICALLY_CERTIFIED_FINITE_C1_ORIGIN_UNIFORMITY_LADDER_AUDIT
TPC394_SELECTION_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC394_COORDINATE_DISJOINTNESS = PROVED_EXACT_FINITE
TPC394_PARENT_REFERENCE = PROVED_EXACT_FINITE_HASHED
TPC394_ORIGIN_LADDER_PANEL = NUMERICALLY_CERTIFIED_FINITE_64_ROWS
TPC394_ORIGIN_UNIFORMITY_AUDIT = NUMERICALLY CERTIFIED FINITE SCOPED
TPC394_CALIBRATION_HOLDOUT_TRANSFER = NUMERICALLY CERTIFIED FINITE SCOPED
TPC394_SPECTRAL_ENVELOPE = REFUTED_ON_DECLARED_FINITE_PANEL
TPC394_SCHUR_ENVELOPE = NUMERICALLY CERTIFIED FINITE SCOPED ONLY
TPC394_SOURCE_NORMALIZATION_VALIDITY = MODELING_CHOICE_OPEN
TPC394_GROWING_OPERATOR_BOUND = OPEN
TPC394_SOURCE_UNIFORM_L2 = OPEN
TPC394_ARITHMETIC_ADVANCE = NO
TPC394_FIXED_POWER_CREDIT = 0
TPC394_FULL_GATE_B = OPEN
TPC394_TWIN_PRIME_RESULT = NONE
TPC394_ROUND2_CLUE = TEST_C1_ORIGIN_CROSS_FAMILY_HOLDOUT
```

## Locked finite protocol

The candidate grid is `a_j=5000001+401j`, `0<=j<41`; selected indices are
`(0,5,10,15,20,25,30,35)`.  The first five origins are calibration and the
last three are holdout, all with `N=1024`, block length 128, `fixed_c3`, and
`Q=8192`.  The laws are all-plus and alternating-index.  The four declared
normalizations are local diagonal, pooled calibration scalar, current-origin
scalar, and first-calibration frozen scalar.  The origin-spread cap is 1% and
the holdout-transfer cap is 3%.

## Certificate result

The certificate contains 64 rows and 8 cells.  All four all-plus cells pass
the 1% all-origin spread rule; all four alternating-index cells fail, with
maximum alternating spread `0.092863374514779065`.  Holdout transfer passes in
all 8 cells.  The finite spectral cap fails in 32 rows and the Schur cap in
zero rows.  These values are finite, law-dependent proxy diagnostics only.

## Verification commands

The locked checker is
`research/tpc-big-road/tpc_bridge_b_tpc394_c1_origin_uniformity_ladder_checker.py`.
It checks canonical JSON, parent hashes, row/summary contracts, claim
firewalls, PDF identity, clean LaTeX diagnostics, and runs normal and `-O`
producer, independent reverse-shell checker, and 25-mutation stress jobs.

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B research/tpc-big-road/tpc_bridge_b_tpc394_c1_origin_uniformity_ladder_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc394_c1_origin_uniformity_ladder_checker.py --check
```

No arithmetic advance or fixed-power credit is assigned.  The official
Session evaluator files are not present in this checkout, so `ROUTE_A` is not
officially evaluated and `ROUTE_B` remains open.
