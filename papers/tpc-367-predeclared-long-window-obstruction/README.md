# TPC-367 — Predeclared long-window obstruction for the beta=2 tilt

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

TPC-367 removes the geometry-ranked-origin step from the higher-`Q` audit and
tests the frozen beta=2 rule on three predeclared, equally spaced origins
`(620001,626141,632281)`.  On counts `512` and `1024`, anchors
`Q={512,2048,8192}`, two kernel exponents, and four fixed laws, the complete
replay has 288 rows.  Beta=2 has 6 spectral-cap violations and no Schur-cap
violations; all six occur for the longer count `1024`, at `Q=2048` or
`Q=8192`, and the all-plus law.  The beta=0 control has 36 spectral and 36
Schur violations.

This is a finite, scoped obstruction to transferring the beta=2 cap from the
short-window/higher-`Q` panel to these longer unselected windows.  It is not an
asymptotic theorem and gives no twin-prime conclusion.

## Scientific contribution

TPC-366 left two immediate objections: the origins were selected by a finite
geometry score, and the audited windows were short.  TPC-367 attacks both at
once.  The candidate grid is declared as `620001+307j`, `0<=j<41`; the
origins with indices `0,20,40` are fixed before any signed response is
computed.  No geometry score, source vector, or response is used in this
choice.  The same beta=2 weight `w_(p,beta)=(p/Q)^beta` is then replayed with
the literal beta=0 control.

The finite phase diagram localizes the failure rather than merely reporting a
global maximum:

| beta | count | Q | spectral failures | Schur failures |
|---:|---:|---:|---:|---:|
| 0 | 512 or 1024 | 512, 2048, 8192 | 36 total | 36 total |
| 2 | 512 | 512, 2048, 8192 | 0 | 0 |
| 2 | 1024 | 512 | 0 | 0 |
| 2 | 1024 | 2048, 8192 | 6 total | 0 |

The strongest positive finite signal is that beta=2 remains below the
spectral cap for every shorter-window row and every tested `Q` at count 512,
while its Schur maximum over all 144 beta=2 rows is only
`0.70009945776422788`.  The strongest obstruction is the reproducible
long-window spectral failure: the beta=2 maximum is
`0.67410738070824539`, above the working cap `0.64`, and is
`0.049624503118480101` above the TPC-366 maximum.  The six failures are not
treated as evidence of an asymptotic law; they identify a finite window-scale
boundary.

## Claim firewall

```text
TPC367_ORIGIN_PROTOCOL = PROVED_EXACT_FINITE_PREDECLARED_RESPONSE_BLIND
TPC367_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC367_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC367_LONG_WINDOW_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC367_UNSELECTED_ORIGIN_AUDIT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC367_BETA2_LONG_WINDOW_TRANSFER = REFUTED_SCOPED
TPC367_BETA2_EXPONENT_SENSITIVITY = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC367_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC367_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC367_GROWING_OPERATOR_BOUND = OPEN
TPC367_SOURCE_UNIFORM_L2 = OPEN
TPC367_ARITHMETIC_ADVANCE = NO
TPC367_FIXED_POWER_CREDIT = 0
TPC367_FULL_GATE_B = OPEN
TPC367_TWIN_PRIME_RESULT = NONE
```

`REFUTED_SCOPED` means only the declared finite transfer statement is
refuted.  It does not refute beta=2 in other windows or any asymptotic claim.
The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is a fail-closed finite audit, not
an official evaluator pass.

## Auditable package

The project contains `PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`,
`PROOF_PACKAGE.md`, `notes/`, `code/`, `experiments/`, `results/`, and
`paper/`.  The canonical finite certificate is
`results/tpc367_certificate.json`; the manuscript is `paper/paper.pdf`.
The producer uses increasing shell accumulation.  The independent checker
uses a separately written sieve and descending shell accumulation, rebuilds
all 288 spectra, and checks the exact rational anchor.  The stress checker
rejects 28 protocol, data, audit, and claim-firewall mutations.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-367-predeclared-long-window-obstruction/code/tpc367_predeclared_long_window_obstruction.py --write
python -B papers/tpc-367-predeclared-long-window-obstruction/code/tpc367_predeclared_long_window_obstruction.py --check
python -O -B papers/tpc-367-predeclared-long-window-obstruction/code/tpc367_predeclared_long_window_obstruction.py --check
python -B papers/tpc-367-predeclared-long-window-obstruction/experiments/tpc367_independent_checker.py --check
python -O -B papers/tpc-367-predeclared-long-window-obstruction/experiments/tpc367_independent_checker.py --check
python -B papers/tpc-367-predeclared-long-window-obstruction/experiments/tpc367_adversarial_certificate_stress.py --check
python -O -B papers/tpc-367-predeclared-long-window-obstruction/experiments/tpc367_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc367_predeclared_long_window_obstruction_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc367_predeclared_long_window_obstruction_checker.py --check
```

## Route decision and ROUND2_CLUE

The next minimal question is whether the six beta=2 failures persist under a
second predeclared origin family, while keeping the failing exponent and
long-window scale fixed.  This is an independent replication/phase attack,
not a new beta search.

`ROUND2_CLUE = TEST_BETA2_FAILURE_LOCALIZATION_ON_LONGER_WINDOWS`
