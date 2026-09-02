# TPC-342 — Independent fresh-panel reproduction

**Author:** Liang Wang

**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

The TPC-341 nuisance-projection protocol reproduces its aggregate-versus-holdout
split on three disjoint windows: the nine-control twin-mean residual retains
0.270141--0.295101 in-sample, while all 27 leave-one-control-out tests retain
0.589484--0.942917.

## Why this is a separate paper

TPC-341 found that a low residual for an aggregate twin-prime mean did not
transfer to an omitted control.  TPC-342 is an independent reproduction of that
specific claim, not a larger sample appended to the old certificate.  The
TPC-341 producer and certificate are hash-locked as the protocol reference;
TPC-342 changes only the source panel to three new, contiguous, cutoff-safe
windows below the earlier panel endpoint 40096.  Its reverse-shell checker
recomputes the projection and holdout loop without importing the TPC-342
producer.

## Frozen design

~~~text
protocol reference = TPC-341 producer + certificate (hash locked)
source/operator     = TPC-340 all-plus deleted-diagonal engine (hash locked)
origins             = {40097, 40609, 41121}
scales              = {1024}
source intervals    = [40097,40608], [40609,41120], [41121,41632]
operator            = all-plus, Q=54, exponent=1, H=66
controls            = TPC-338/TPC-340 nine-control orbit
categories          = twin, non-twin prime shift, prime-power shift, zero
raw records         = 3 x 9 x 4 = 108
nonempty records    = 81
in-sample fits      = 3
holdout fits        = 3 x 9 = 27
~~~

Every shifted argument is below the parent cutoff 50,000.  The prime-power mask
is empty in all three rows, so the effective nuisance rank is two throughout.
That degeneracy is recorded rather than padded away.

## Certified finite readout

| quantity | finite result |
|---|---:|
| raw records | 108 |
| nonempty raw records | 81 |
| in-sample residual retention | 0.2701410521--0.2951006120 |
| in-sample energy removed | 0.7048993880--0.7298589479 |
| held-out residual retention | 0.5894842476--0.9429165296 |
| held-out energy removed | 0.0570834704--0.4105157524 |
| effective nuisance rank | 2 in all rows |
| rank/Pythagorean failures | 0 |

The predeclared guards are in-sample retention < 0.30 and
held-out retention > 0.40; both hold on every applicable record.  The largest
finite condition numbers are 9.7888224 in-sample and 10.1391310 on holdout.
They are diagnostics of the chosen finite coordinates, not a canonicality claim.

## Claim firewall

~~~text
TPC342_PROJECTION_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL
TPC342_INDEPENDENT_FRESH_REPLAY = NUMERICALLY_CERTIFIED_FINITE_108_RAW_RECORDS
TPC342_IN_SAMPLE_PROJECTION = NUMERICALLY_CERTIFIED_FINITE_3_ROWS
TPC342_HOLDOUT_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE_27_RECORDS
TPC342_IN_SAMPLE_RETENTION = NUMERICAL_OBSERVATION_0.270_TO_0.296
TPC342_HOLDOUT_RETENTION = NUMERICAL_OBSERVATION_0.589_TO_0.943
TPC342_CONTROL_STABILITY = REFUTED_SCOPED
TPC342_ARITHMETIC_ADVANCE = NO
TPC342_FIXED_POWER_CREDIT = 0
TPC342_SOURCE_UNIFORM_L2 = OPEN
TPC342_UNIFORM_MASKED_OPERATOR_BOUND = OPEN
TPC342_FULL_GATE_B = OPEN
TPC342_TWIN_PRIME_RESULT = NONE
~~~

The finite projection is a modeling choice.  The result does not identify the
nuisance span with arithmetic noise, does not establish probabilistic
independence, and does not imply a twin-prime theorem.  The official
Session-named propose.md, Route-A, and Route-B evaluator files are absent in
this checkout.  The local Bridge-B wrapper is therefore a fail-closed
repository audit and is not an official evaluator pass.

## Reproduction

~~~bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py --write
python -B papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py --check
python -O -B papers/tpc-342-independent-fresh-holdout-reproduction/code/tpc342_independent_fresh_holdout_reproduction.py --check
python -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_independent_checker.py --check
python -O -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_independent_checker.py --check
python -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_holdout_stress.py --check
python -O -B papers/tpc-342-independent-fresh-holdout-reproduction/experiments/tpc342_holdout_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc342_independent_fresh_holdout_reproduction_checker.py --check
~~~

The canonical finite certificate is
results/tpc342_certificate.json, and the compiled manuscript is paper/paper.pdf.

## Next research decision

The independent panel confirms that the TPC-341 mean-only nuisance projection
is not control-stable in this finite family.  The next smallest non-duplicative
question is whether the obstruction persists after pooling the two panels in a
cross-panel certificate.  Only after that audit can an alternative nuisance
basis be tested; neither step carries automatic arithmetic credit.
