# Bridge-B — TPC-375 bandwidth stability and minimal cutoff

This is the local fail-closed bridge for TPC-375.  It is repository evidence,
not an official Route-A/Route-B evaluator verdict; the official evaluator
files named by the Session are absent.

## Frozen object

```text
schema        = TPC375_BANDWIDTH_STABILITY_MINIMAL_CUTOFF_V1
panel         = 3 origins x 3 Q anchors, beta=2, all-plus = 9 rows
window        = 2048 points, eight contiguous blocks of length 256
cutoffs       = c=0,1,2,3
normalization = full-window square-energy geometry
caps          = spectral 0.64, Schur 0.83
```

All rows and cutoffs are fixed before any metric is read.  For each cutoff,
`B_c` retains block distances at most `c`, and `R_c=T-B_c` is its exact finite
complement.

## Finite result and firewall

```text
spectral failure counts by cutoff c=0,1,2,3 = 0,6,6,6
Schur failure counts by cutoff c=0,1,2,3    = 0,0,0,0
first cutoff matching parent six-key support = c=1
```

The six `c=1` failures are all three origins at `Q=2048,8192`; the three
`Q=512` rows never fail.  “Minimal” is only the first hit in this declared
finite cutoff list.

```text
TPC375_FAILURE_CUTOFF_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_PARENT_SUPPORT_REPRODUCTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_MINIMAL_CUTOFF = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC375_BANDWIDTH_UNIFORMITY = OPEN
TPC375_CROSS_BLOCK_CAUSALITY = OPEN
TPC375_ORIGIN_UNIFORMITY = OPEN
TPC375_WINDOW_UNIFORMITY = OPEN
TPC375_ARITHMETIC_ADVANCE = NO
TPC375_FIXED_POWER_CREDIT = 0
TPC375_FULL_GATE_B = OPEN
TPC375_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_BANDWIDTH_HOLDOUT
```

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/code/tpc375_bandwidth_stability_minimal_cutoff.py --check
python -O -B papers/tpc-375-bandwidth-stability-minimal-cutoff/code/tpc375_bandwidth_stability_minimal_cutoff.py --check
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_independent_checker.py --check
python -O -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_independent_checker.py --check
python -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_adversarial_certificate_stress.py --check
python -O -B papers/tpc-375-bandwidth-stability-minimal-cutoff/experiments/tpc375_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc375_bandwidth_stability_minimal_cutoff_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc375_bandwidth_stability_minimal_cutoff_checker.py --check
```

The checker locks every source, certificate, package document, PDF, and final
compile log by LF-normalized SHA-256.  It requires normal and optimized output
to be byte-identical and standard error to be empty.
