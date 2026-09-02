# TPC-341 — Fresh holdout test for nuisance orthogonalization

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On three fresh, non-overlapping windows, projecting the nine-control twin-prime
mean onto the span of the non-twin, prime-power, and zero-support means removes
`74.3937%--79.8911%` of its energy.  The same construction fails a hostile
leave-one-control-out test: the omitted twin output retains
`44.3527%--89.0447%` of its energy in all 27 tests.  Mean-only nuisance
removal is therefore a finite control-stability obstruction, not a validated
isolated arithmetic signal.

## New contribution

TPC-341 moves the question to a genuinely fresh holdout panel rather than
adding another generic norm.  It separates two operations that can otherwise
be conflated:

1. an in-sample projection of the nine-control class mean; and
2. a leave-one-control-out projection trained on eight controls and tested on
   the omitted twin response.

The orthogonal decomposition is exact finite linear algebra.  The stability
failure is a new, finite obstruction to reading a low residual of an aggregate
mean as a control-invariant twin-prime component.

## Frozen fresh panel

```text
origins       = {48097, 48609, 49217}
scales        = {1024}
intervals     = [48097,48608], [48609,49120], [49217,49728]
operator      = all-plus, Q=54, exponent=1, H=66
controls      = TPC-338/TPC-340 nine-control orbit
raw records   = 3 windows x 9 controls x 4 masks = 108
nonempty raw  = 90
holdout tests = 3 windows x 9 omitted controls = 27
```

All three intervals lie beyond the TPC-337--TPC-340 panel and remain below the
parent model's `50,000` source cutoff after the `+2` shift.  The prime-power
mask is empty in the first two rows and contains `49727=223^2-2` in the third;
the effective nuisance ranks are consequently `2,2,3`, and are recorded
explicitly.

## Certified finite readout

| quantity | finite range |
|---|---:|
| in-sample residual retention | `0.2010894086--0.2560626551` |
| in-sample energy removed | `0.7439373449--0.7989105914` |
| held-out residual retention | `0.4435267486--0.8904473564` |
| held-out energy removed | `0.1095526436--0.5564732514` |
| nuisance rank | `2` or `3` |
| rank/Pythagorean failures | `0` |

The held-out lower guard was predeclared as `0.40`, while the in-sample upper
guard was `0.30`; both pass in the direction needed to expose the mismatch.
The condition numbers range up to about `92.76`, so the certificate reports
conditioning rather than silently presenting the projection as canonical.

## Claim firewall

```text
PROVED_EXACT_FINITE_DECLARED_MODEL = orthogonal projection identity
NUMERICALLY_CERTIFIED_FINITE = 108 raw records, 90 nonempty
NUMERICALLY_CERTIFIED_FINITE = 3 in-sample and 27 held-out projections
NUMERICAL_OBSERVATION = retention ranges and condition numbers
REFUTED_SCOPED = mean-only nuisance removal is control-stable
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
SOURCE_UNIFORM_L2 = OPEN
UNIFORM_MASKED_OPERATOR_BOUND = OPEN
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The projection is a declared modeling choice.  The result does not prove that
nuisance directions are arithmetic noise, does not establish independence, and
does not imply a twin-prime theorem.  The official Session evaluator files are
absent; local Bridge-B is fail-closed and does not claim an official Route-A or
Route-B pass.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py --write
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py --check
python -O -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/code/tpc341_fresh_holdout_nuisance_orthogonalization.py --check
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_independent_checker.py --check
python -O -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_independent_checker.py --check
python -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_holdout_stress.py --check
python -O -B papers/tpc-341-fresh-holdout-nuisance-orthogonalization/experiments/tpc341_holdout_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc341_fresh_holdout_nuisance_orthogonalization_checker.py --check
```

The canonical result is
[results/tpc341_certificate.json](results/tpc341_certificate.json), and the
manuscript is [paper/paper.pdf](paper/paper.pdf).

## Batch endpoint

TPC-341 is the fifth project in the current TPC-337--TPC-341 batch.  The next
action is independent batch review and route-map update; no TPC-342 is created
in this batch.
