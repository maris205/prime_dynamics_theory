# TPC-339 — Mask-aware Frobenius envelope

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-339 replaces the noncanonical signed-covariance heuristic exposed by
TPC-338 with a sign-free support-restricted operator bound.  For a vector
supported on `S`,

```text
||A x||_2^2 <= ||A[:,S]||_F^2 ||x||_2^2.
```

All 216 declared mask/control records pass this bound.  The global occupancy
of the bound is `0.0074766258--1.0000000000`; for the broad twin, background,
and zero-support masks it is always below `0.2`.  The inequality is reliable,
but its finite slack shows that it cannot by itself serve as a sharp response
estimate.

## New contribution

For each of the nine TPC-338 controls and four source masks, the certificate
records source norm, response gain, support-restricted Frobenius gain, gap, and
occupancy.  This separates a universally valid finite inequality from the
much stronger (and unsupported) hope that the inequality is tight on broad
arithmetic masks.

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

| mask | nonempty records | occupancy range |
|---|---:|---:|
| twin prime | 54 | `0.0288303218--0.1868550366` |
| non-twin prime shift | 54 | `0.0106490382--0.0558500985` |
| prime-power shift | 36 | `0.99999999999999--1.00000000000000` |
| zero support | 54 | `0.0074766258--0.0320675913` |

There are zero bound violations.  The exact anchor attains equality with
`A=[[1,0],[2,1]]` and `x=(3,0)`, for which the response energy is `45`, source
norm is `9`, and restricted Frobenius gain is `5`.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = support-restricted Frobenius bound
NUMERICALLY_CERTIFIED_FINITE = 216 records, 0 bound violations
NUMERICAL_OBSERVATION = occupancy and mask slack ranges
REFUTED_SCOPED = elementary envelope is factor-five tight on broad panel
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
UNIFORM_MASKED_OPERATOR_BOUND = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The factor-five statement is only the declared finite occupancy diagnostic;
the result does not rule out a sharper masked Gram bound.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-339-mask-aware-frobenius-envelope/code/tpc339_mask_aware_frobenius_envelope.py --write
python -B papers/tpc-339-mask-aware-frobenius-envelope/code/tpc339_mask_aware_frobenius_envelope.py --check
python -O -B papers/tpc-339-mask-aware-frobenius-envelope/code/tpc339_mask_aware_frobenius_envelope.py --check
python -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_independent_checker.py --check
python -O -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_independent_checker.py --check
python -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_envelope_stress.py --check
python -O -B papers/tpc-339-mask-aware-frobenius-envelope/experiments/tpc339_envelope_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc339_mask_aware_frobenius_envelope_checker.py --check
```

The canonical result is [results/tpc339_certificate.json](results/tpc339_certificate.json),
and the manuscript is [paper/paper.pdf](paper/paper.pdf).

## Next clue

The next minimal sharpening is to combine the support Frobenius bound with a
sign-free Schur bound for the full operator and test the resulting hybrid
envelope.
