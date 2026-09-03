# TPC-374 — Near-block band truncation

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-374 freezes the block-distance band `B3` consisting of distances `0,1,2,3`
in the same count-2048, common-normalization prime-shell operator studied by
TPC-373.  On the complete 18-row panel, `B3` reproduces exactly the six beta=2
full spectral-cap failures: all three origins at `Q=2048,8192`.  On those
rows, the selected full-mode absolute-Rayleigh retention is at least
`0.99157117644491055`, and the omitted tail contributes at most
`0.0084288235550895561` of absolute Rayleigh mass.

This is a finite near-block reduction certificate.  It is not a causal,
uniform, asymptotic, arithmetic, or twin-prime theorem.

## Frozen protocol

```text
origins       = (1010001, 1018021, 1026041)
window count  = 2048
blocks        = eight contiguous blocks of length 256
band cutoff   = 3 (block distances 0,1,2,3)
Q             = (512, 2048, 8192)
exponent      = 1
law           = all_plus
beta          = (0, 2)
rows          = 18
caps          = spectral 0.64, Schur 0.83
```

The full-window square-energy geometry is used for the full matrix, `B3`, and
the complement `R3=T-B3`.  The panel and band are fixed before results are
read.  The selected full eigenmode is the largest-absolute-eigenvalue mode;
the minimum mode wins exact ties.

## Finite census

| setting | spectral failures | Schur failures |
|---|---:|---:|
| beta=0, full | 9/9 | 9/9 |
| beta=0, `B3` | 9/9 | 9/9 |
| beta=2, full | 6/9 | 0/9 |
| beta=2, `B3` | 6/9 | 0/9 |

The six beta=2 failure keys are exactly:

```text
(1010001, 2048, 2048, 1, all_plus)
(1010001, 2048, 8192, 1, all_plus)
(1018021, 2048, 2048, 1, all_plus)
(1018021, 2048, 8192, 1, all_plus)
(1026041, 2048, 2048, 1, all_plus)
(1026041, 2048, 8192, 1, all_plus)
```

Over those six rows, the band absolute-Rayleigh retention ranges from
`0.99157117644491055` to `0.99157357537480051`; the tail fraction ranges from
`0.0084264246251999891` to `0.0084288235550895561`.  The beta=2 band spectral
values at `Q=512`, `2048`, and `8192` lie respectively in
`[0.5152073962, 0.5152083702]`, `[0.7037611538, 0.7037762223]`, and
`[0.7051585288, 0.7051589867]`.  At `Q=512` the band can be slightly larger
than the full value, so no monotone truncation principle is inferred.

## Claim firewall

```text
TPC374_FULL_WINDOW_PROTOCOL = PROVED_EXACT_FINITE_INHERITED_RESPONSE_BLIND
TPC374_COMMON_NORMALIZATION = PROVED_EXACT_FINITE
TPC374_NEAR_BLOCK_BAND = PROVED_EXACT_FINITE_PREDECLARED
TPC374_BAND_REPLAY = NUMERICALLY_CERTIFIED_FINITE_18_ROWS
TPC374_BAND_FAILURE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC374_PARENT_FAILURE_REPRODUCTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC374_RAYLEIGH_RETENTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC374_TAIL_PROFILE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC374_BAND_OPERATOR_UNIFORMITY = OPEN
TPC374_CROSS_BLOCK_CAUSALITY = OPEN
TPC374_ORIGIN_UNIFORMITY = OPEN
TPC374_WINDOW_UNIFORMITY = OPEN
TPC374_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC374_GROWING_OPERATOR_BOUND = OPEN
TPC374_SOURCE_UNIFORM_L2 = OPEN
TPC374_ARITHMETIC_ADVANCE = NO
TPC374_FIXED_POWER_CREDIT = 0
TPC374_FULL_GATE_B = OPEN
TPC374_TWIN_PRIME_RESULT = NONE
```

The official Route-A/Route-B evaluator files named by the Session are absent;
the local Bridge-B checker is repository evidence only and remains fail
closed with respect to an official route verdict.

## Package and reproduction

This project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical certificate is
`results/tpc374_certificate.json`; the compiled manuscript is
`paper/paper.pdf`.

```bash
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
python -B papers/tpc-374-near-block-band-truncation/code/tpc374_near_block_band_truncation.py --write
python -B papers/tpc-374-near-block-band-truncation/code/tpc374_near_block_band_truncation.py --check
python -O -B papers/tpc-374-near-block-band-truncation/code/tpc374_near_block_band_truncation.py --check
python -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_independent_checker.py --check
python -O -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_independent_checker.py --check
python -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_adversarial_certificate_stress.py --check
python -O -B papers/tpc-374-near-block-band-truncation/experiments/tpc374_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc374_near_block_band_truncation_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc374_near_block_band_truncation_checker.py --check
```

```text
ROUND2_CLUE = TEST_BANDWIDTH_STABILITY
```
