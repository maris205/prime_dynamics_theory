# TPC-363 — Bulk persistence at the first shell-scale failure

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On the frozen TPC-361 high-origin panel, all 18 rows that violate the inherited
`0.64` spectral cap at `Q=128` or `Q=256` remain above that cap after removing
`floor(N/20)` rows by either Schur row mass or principal-eigenvector mass.  The
smallest retained restricted spectral value is
`0.86120283374232454`.

## Scientific contribution

TPC-362 established that the previous normalized cap first fails at `Q=128`.
TPC-363 tests the most immediate finite explanation: a small exceptional row
or a single localized eigenvector coordinate.  It freezes the same three
origins, uses counts `256,512`, shell anchors `80,128,256`, both kernel
exponents, and all four fixed sign laws, giving 144 law rows with true
spectra.

For every row, two deterministic five-percent principal restrictions are
formed.  One removes the largest normalized Schur row masses; the other
removes the largest squared coordinates of the eigenvector associated with
the largest absolute eigenvalue.  The `Q=80` controls have no cap violation
and their largest restricted spectrum is `0.60313535281541197`.  The six
`Q=128` failures and twelve `Q=256` failures are all-plus rows, and every one
persists under both restrictions.  The minimum restricted spectrum among the
`Q=128` failures is `1.1843597700033823`; among `Q=256` failures it is
`0.86120283374232454`.

The result is a scoped bulk obstruction to the particular single-row or
single-coordinate explanation.  It is not a universal statement about other
normalizations and supplies no arithmetic advance toward twin primes.

## Claim firewall

```text
TPC363_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC363_FINITE_ENVELOPE_INEQUALITIES = PROVED_EXACT_FINITE
TPC363_FIRST_Q128_FAILURE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_BULK_PERSISTENCE = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_SINGLE_ROW_SPIKE_EXPLANATION = REFUTED_SCOPED_ON_DECLARED_TRIMS
TPC363_EIGENVECTOR_DELOCALIZATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC363_RENORMALIZED_REPAIR = OPEN
TPC363_GROWING_OPERATOR_BOUND = OPEN
TPC363_SOURCE_UNIFORM_L2 = OPEN
TPC363_ARITHMETIC_ADVANCE = NO
TPC363_FIXED_POWER_CREDIT = 0
TPC363_FULL_GATE_B = OPEN
TPC363_TWIN_PRIME_RESULT = NONE
```

The official Session-named Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed finite evidence,
not an official evaluator pass.  No response vector, source profile,
arithmetic reassembly, or fixed-power credit is used.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-363-bulk-persistence-localization/code/tpc363_bulk_persistence_localization.py --write
python -B papers/tpc-363-bulk-persistence-localization/code/tpc363_bulk_persistence_localization.py --check
python -O -B papers/tpc-363-bulk-persistence-localization/code/tpc363_bulk_persistence_localization.py --check
python -B papers/tpc-363-bulk-persistence-localization/experiments/tpc363_independent_checker.py --check
python -O -B papers/tpc-363-bulk-persistence-localization/experiments/tpc363_independent_checker.py --check
python -B papers/tpc-363-bulk-persistence-localization/experiments/tpc363_adversarial_certificate_stress.py --check
python -O -B papers/tpc-363-bulk-persistence-localization/experiments/tpc363_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc363_bulk_persistence_localization_checker.py --check
```

The canonical certificate is `results/tpc363_certificate.json`; the compiled
manuscript is `paper/paper.pdf`.  The frozen protocol and route decision are
in `experiments/protocol.md` and `notes/route_evaluation.md`.

## Round-2 clue

`TEST_RENORMALIZED_HIGH_Q_REPAIR_ON_EXPLICIT_HOLDOUT`.
