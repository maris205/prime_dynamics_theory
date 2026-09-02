# TPC-340 — Schur/Frobenius hybrid envelope

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-340 combines the support-restricted Frobenius envelope from TPC-339 with
a global sign-free Schur envelope.  For a finite symmetric matrix `A` and a
vector supported on `S`,

```text
||A x||_2^2 <= min(||A[:,S]||_F^2, R^2) ||x||_2^2,
R = max_i sum_j |A(i,j)|.
```

The hybrid inequality is exact as a finite norm statement and passes all 216
declared records with zero violations.  It improves the zero-support
Frobenius envelope by factors `1.250245--4.698443` on this panel, but it does
not make the broad-mask response tight: the broad hybrid occupancy remains at
most `0.1868550366`.

## New contribution

The paper supplies a branch-audited, sign-free hybrid bound.  The Schur
branch is active in 54 records (the nine zero-support placements in each of
six windows), while the support-Frobenius branch is active in the other 162
records.  This identifies a concrete finite improvement without treating a
control-dependent covariance sign as an arithmetic input.

## Frozen finite panel

```text
origins       = {42001, 44001}
scales        = {2048, 4096, 8192}
operator      = all-plus, Q=54, exponent=1, H=66
controls      = TPC-338 nine-control orbit
records       = 6 windows x 9 controls x 4 masks = 216
nonempty      = 198
```

## Certified finite readout

| mask | nonempty records | hybrid occupancy range | Frobenius improvement |
|---|---:|---:|---:|
| twin prime | 54 | `0.0288303218--0.1868550366` | `1--1` |
| non-twin prime shift | 54 | `0.0106490382--0.0558500985` | `1--1` |
| prime-power shift | 36 | `0.99999999999999--1.00000000000000` | `1--1` |
| zero support | 54 | `0.0350128142--0.0411644862` | `1.250245--4.698443` |

The global nonempty hybrid occupancy range is
`0.0106490382--1.0000000000`.  An exact rational anchor uses
`A=[[1,-1],[-1,1]]` and `x=(1,1)`: the response energy is zero, the source
norm is two, and the Schur gain is four.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = Schur and hybrid norm envelopes
NUMERICALLY_CERTIFIED_FINITE = 216 records, 0 bound violations
NUMERICALLY_CERTIFIED_FINITE = Schur branch in 54 records
NUMERICAL_OBSERVATION = finite occupancy and improvement ranges
REFUTED_SCOPED = broad-mask factor-five tightness for the hybrid
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
UNIFORM_MASKED_OPERATOR_BOUND = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The improvement is a finite diagnostic, not a growing estimate or a payment
of cancellation.  The Session-named official evaluator files are absent;
the local Bridge-B wrapper is fail-closed and does not claim an official
Route-A or Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py --write
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py --check
python -O -B papers/tpc-340-schur-frobenius-hybrid-envelope/code/tpc340_schur_frobenius_hybrid_envelope.py --check
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py --check
python -O -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_independent_checker.py --check
python -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_hybrid_stress.py --check
python -O -B papers/tpc-340-schur-frobenius-hybrid-envelope/experiments/tpc340_hybrid_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc340_schur_frobenius_hybrid_envelope_checker.py --check
```

The canonical result is
[results/tpc340_certificate.json](results/tpc340_certificate.json), and the
manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next clue

The hybrid envelope still leaves a broad-mask obstruction.  The next minimal
test is a fresh source holdout with explicit nuisance-span orthogonalization,
including adversarial controls, to determine whether the apparent twin
response survives removal of the non-twin/zero background directions.
