# TPC-365 — Response-blind fresh holdout for the beta=2 shell tilt

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of
Science and Technology (HUST), Wuhan, China

## One-line result

The beta=2 rule selected from TPC-364 was frozen before response evaluation
and tested on three new, separated high-origin windows.  Across 384 rows
(two betas, three origins, two counts, four shell anchors, two exponents, and
four fixed laws), beta=2 has zero spectral-cap failures, while the beta=0
control has 30.  The beta=2 maximum normalized spectrum is
`0.61633188509480319`, only `4.4345466941875245e-05` above the TPC-364
maximum.

This is a finite, response-blind transfer observation.  It is not an
asymptotic repair, a source-valid normalization theorem, an arithmetic
advance, or a twin-prime result.

## Scientific contribution

TPC-364 found a unique zero-failure point, beta=2, in a finite tilt menu on a
reused panel.  TPC-365 attacks the most immediate selection objection without
refitting beta.  It scans the fixed candidate origins
`410001+257j`, `0<=j<51`, using only the unsigned beta=2 weighted square
geometry on a 256-point pilot window.  Candidates are ranked by their largest
geometry spread over `Q in {80,128,256,512}` and kernel exponents `{1,2}`;
the declared greedy separation rule (`2048`) selects
`(413342,410258,416940)`.  Only after this rule is frozen are the signed
matrices and all four laws evaluated.

The fresh panel gives a positive finite transfer signal: beta=2 stays below
the inherited working cap `0.64` for all 192 beta=2 rows, while the same
normalization with beta=0 exceeds it in 30 of 192 rows.  The result survives
an independently written reverse-shell replay and a 19-mutation certificate
stress test.  The selection is response-blind, but it is still a deterministic
finite geometry selection and therefore is not an independent probabilistic
sample or a uniform theorem.

## Claim firewall

```text
TPC365_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC365_WEIGHTED_GEOMETRY_POSITIVITY = PROVED_EXACT_FINITE
TPC365_FINITE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
TPC365_BETA2_HOLDOUT = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC365_BETA2_CAP_TRANSFER = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC365_BETA2_ASYMPTOTIC_REPAIR = OPEN
TPC365_NORMALIZATION_SOURCE_VALIDITY = MODELING_CHOICE_OPEN
TPC365_GROWING_OPERATOR_BOUND = OPEN
TPC365_SOURCE_UNIFORM_L2 = OPEN
TPC365_ARITHMETIC_ADVANCE = NO
TPC365_FIXED_POWER_CREDIT = 0
TPC365_FULL_GATE_B = OPEN
TPC365_TWIN_PRIME_RESULT = NONE
```

The Session-named official Route-A/Route-B evaluator files are absent from
this checkout.  The local Bridge-B checker is fail-closed finite evidence
only, not an official evaluator pass.

## Package

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable package.
The canonical certificate is
`results/tpc365_certificate.json`; the compiled manuscript is
`paper/paper.pdf`.

## Reproduce

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-365-beta2-fresh-holdout/code/tpc365_beta2_fresh_holdout.py --write
python -B papers/tpc-365-beta2-fresh-holdout/code/tpc365_beta2_fresh_holdout.py --check
python -O -B papers/tpc-365-beta2-fresh-holdout/code/tpc365_beta2_fresh_holdout.py --check
python -B papers/tpc-365-beta2-fresh-holdout/experiments/tpc365_independent_checker.py --check
python -O -B papers/tpc-365-beta2-fresh-holdout/experiments/tpc365_independent_checker.py --check
python -B papers/tpc-365-beta2-fresh-holdout/experiments/tpc365_adversarial_certificate_stress.py --check
python -O -B papers/tpc-365-beta2-fresh-holdout/experiments/tpc365_adversarial_certificate_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc365_beta2_fresh_holdout_checker.py --check
python -O -B research/tpc-big-road/tpc_bridge_b_tpc365_beta2_fresh_holdout_checker.py --check
```

## Round-2 clue

`TEST_BETA2_ON_HIGHER_Q_AND_NEW_SCALE_LADDER`.
