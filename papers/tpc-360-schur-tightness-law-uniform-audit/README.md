# TPC-360 — Schur-tightness and law-uniform audit

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

On the TPC-359 hostile-origin panel, a new 144-row replay computes the true
spectral norm for all four fixed sign laws at counts `256,512`.  The largest
normalized spectral/Schur ratio is `0.77628391453148915`, the largest
spectral/Frobenius ratio is `0.62110877254133434`, and the all-plus law wins
30 of 36 setting-wise comparisons (mod-4 wins 6).

## Contribution

TPC-359 established finite cap transfer under a geometry-only hostile
selection.  TPC-360 tests whether the cap is simply a nearly saturated Schur
bound and whether calculating spectra only for all-plus could hide a larger
law.  The finite result gives a quantitative slack certificate on the declared
panel and a complete four-law spectral comparison.  It does not promote the
observed slack or winner census to an asymptotic theorem.

The strongest positive result is a finite law-uniform cap: every one of the
144 normalized spectra is below `0.64`.  The strongest obstruction is that the
all-plus law is not the setting-wise winner in all cases, so it cannot be
treated as a universal proxy without a separate theorem.

## Claim firewall

```text
TPC360_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC360_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC360_ALL_LAW_SPECTRAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_144_ROWS
TPC360_SCHUR_SLACK = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC360_LAW_UNIFORM_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC360_GROWING_OPERATOR_BOUND = OPEN
TPC360_SOURCE_UNIFORM_L2 = OPEN
TPC360_ARITHMETIC_ADVANCE = NO
TPC360_FIXED_POWER_CREDIT = 0
TPC360_FULL_GATE_B = OPEN
TPC360_TWIN_PRIME_RESULT = NONE
```

The Session-named official evaluator files are absent.  The local Bridge-B
checker is fail-closed finite reproducibility evidence, not an official
Route-A/Route-B pass.

## Reproduce

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-360-schur-tightness-law-uniform-audit/code/tpc360_schur_tightness_law_uniform_audit.py --write
python -B papers/tpc-360-schur-tightness-law-uniform-audit/code/tpc360_schur_tightness_law_uniform_audit.py --check
python -O -B papers/tpc-360-schur-tightness-law-uniform-audit/code/tpc360_schur_tightness_law_uniform_audit.py --check
python -B papers/tpc-360-schur-tightness-law-uniform-audit/experiments/tpc360_independent_checker.py --check
python -O -B papers/tpc-360-schur-tightness-law-uniform-audit/experiments/tpc360_independent_checker.py --check
python -B papers/tpc-360-schur-tightness-law-uniform-audit/experiments/tpc360_adversarial_certificate_stress.py --check
python -O -B papers/tpc-360-schur-tightness-law-uniform-audit/experiments/tpc360_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc360_schur_tightness_law_uniform_audit_checker.py --check
```

The certificate is `results/tpc360_certificate.json`; the compiled manuscript
is `paper/paper.pdf`.

## Round-2 clue

`TEST_INDEPENDENT_HIGH_ORIGIN_REPLICATION_WITH_TIGHTNESS_LEDGER`.
