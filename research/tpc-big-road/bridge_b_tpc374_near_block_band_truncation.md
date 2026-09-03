# Bridge-B — TPC-374 near-block band truncation

This bridge records the local, fail-closed validation for the TPC-374 finite
band audit.  It is repository evidence, not an official Route-A/Route-B
evaluator verdict.  The official evaluator files named by the Session are
absent from this checkout.

## Frozen object

```text
schema          = TPC374_NEAR_BLOCK_BAND_TRUNCATION_V1
panel           = 3 origins x 3 Q anchors x 2 beta values = 18 rows
window          = 2048 points, eight contiguous blocks of length 256
band            = block distance <= 3
normalization   = full-window square-energy geometry
caps            = spectral 0.64, Schur 0.83
```

The band is formed before any result-dependent row selection.  The full
matrix, band, and complement satisfy the exact finite identity
`T = B3 + (T-B3)`.  The selected full eigenmode is the largest-absolute
eigenvalue mode, with the minimum mode winning ties.

## Evidence and claim firewall

The producer and independent reverse-shell checker both certify all 18 rows.
The adversarial suite rejects mutations to protocol, provenance, row census,
band definition, numerical fields, audit counts, anchor, firewall, and clue.
The finite result is:

```text
beta=2 full spectral failures = 6/9
beta=2 band spectral failures = 6/9
beta=2 full Schur failures   = 0/9
beta=2 band Schur failures   = 0/9
```

The six band failures are exactly the three declared origins at `Q=2048` and
`Q=8192`.  On those rows the selected full-mode absolute band-Rayleigh
retention is at least `0.99157117644491055`; the omitted tail fraction is at
most `0.0084288235550895561`.

```text
TPC374_BAND_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC374_BAND_FAILURE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC374_PARENT_FAILURE_REPRODUCTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC374_BAND_OPERATOR_UNIFORMITY = OPEN
TPC374_CROSS_BLOCK_CAUSALITY = OPEN
TPC374_ORIGIN_UNIFORMITY = OPEN
TPC374_WINDOW_UNIFORMITY = OPEN
TPC374_ARITHMETIC_ADVANCE = NO
TPC374_FIXED_POWER_CREDIT = 0
TPC374_FULL_GATE_B = OPEN
TPC374_TWIN_PRIME_RESULT = NONE
ROUND2_CLUE = TEST_BANDWIDTH_STABILITY
```

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-374-near-block-band-truncation/code/tpc374_near_block_band_truncation.py --check
python -O -B papers/tpc-374-near-block-band-truncation/code/tpc374_near_block_band_truncation.py --check
python -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_independent_checker.py --check
python -O -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_independent_checker.py --check
python -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_adversarial_certificate_stress.py --check
python -O -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc374_near_block_band_truncation_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc374_near_block_band_truncation_checker.py --check
```

The checker also locks the source, certificate, documentation, PDF, and
compile log by LF-normalized SHA-256 digests.  It requires `main.pdf` and
`paper.pdf` to be byte-identical and all normal/optimized subcheck outputs to
match exactly.
