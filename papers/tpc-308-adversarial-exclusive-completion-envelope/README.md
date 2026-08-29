# TPC-308 — Adversarial Exclusive-Completion Envelope

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-308 freezes the common-ambient overlap fits from TPC-307 and exhaustively
tests binary label completions within Hamming radii `0,1,2` on each exclusive
holdout.  The 18-cell finite atlas has agreement counts `13/3/2`, `11/2/5`,
and `10/1/7` (concordant/discordant/unresolved), so the three native
discordances attenuate to one but do not disappear; every survivor remains on
the final `Q=70 -> 90`, exponent-one transition.

This is a scoped finite stability/fragility result.  It is not a causal,
asymptotic, arithmetic, or twin-prime theorem.

## Claim firewall

```text
PROVED_EXACT_FINITE = Hamming completion protocol; candidate counts; exact
                      fixed-prediction extrema; radius monotonicity; radius-
                      zero recovery; global-sign invariance; conditional
                      interval classification
NUMERICALLY_REPRODUCED_FINITE = 18 cases x 3 radii = 54 envelope observations
                                 and 702 candidate evaluations
NUMERICAL_OBSERVATION = discordance attenuation 3 -> 2 -> 1; localization to
                        Q=70->90, exponent 1
MODELING_CHOICE = radii 0,1,2; fixed TPC-307 predictions and profile prefixes
INHERITED_LEAKAGE = TPC-302 physical-Gram-dependent target labels
OPEN = formal directed-rounding certificate; completion generation/causal
       identification; uniform asymptotic budget; arithmetic L2; fixed-power
       credit; full Gate B; twin-prime conclusion
```

## Research extraction

```text
STRONGEST_POSITIVE_RESULT = exact finite adversarial completion-envelope
                            protocol with independent replay
STRONGEST_OBSTRUCTION = final-transition discordance survives at least one
                        radius-two completion envelope; widening also creates
                        seven unresolved cells
OPEN_THEOREM = determine whether the surviving discordance is invariant under
               admissible profile-prefix perturbations
REUSABLE_STRUCTURE = frozen overlap fit -> fixed predictions -> finite Hamming
                     balls -> extrema -> conservative ratio interval ->
                     class/stability census
ROUND2_CLUE = TEST_PROFILE_PREFIX_PERTURBATION_AND_COMPLETION_INVARIANCE_ON_THE_SURVIVING_DISCORDANCE_CELLS_BEFORE_ANY_PREFERENCE_CLAIM
```

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc308_adversarial_exclusive_completion_envelope.py --write
python -B code/tpc308_adversarial_exclusive_completion_envelope.py --check
python -B experiments/tpc308_independent_checker.py
python -B experiments/tpc308_completion_stress.py
python -B research/tpc-big-road/tpc_bridge_b_tpc308_adversarial_exclusive_completion_envelope_checker.py --check
```

The manuscript is [paper/paper.pdf](paper/paper.pdf).  The canonical result
is `results/tpc308_certificate.json`.  The Session-named `propose.md` and
Route-A/Route-B evaluator files are absent from this checkout; no official
evaluator pass is asserted.  The local fail-closed path is the locked parent,
independent replay, exact stress suite, proof package, PDF audit, and Bridge-B
checker.
