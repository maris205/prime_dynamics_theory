# TPC-323 — Signed profile majorization and amplitude–shape separation

**Author:** Liang Wang
**Affiliation:** School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST), Wuhan, China

## One-line result

On the literal deleted-diagonal prime-shell panel inherited from TPC-322,
the all-plus coherent signed Gram has a trace-normalized spectrum that
majorizes the direct-sum spectrum on all 24 rows.  This profile statement is
stable even though the corresponding unnormalised energy is below the direct
energy on 3 rows and above it on 21 rows.  The other three declared sign laws
have mixed profile rows (7, 3, and 6 respectively), so the finite panel does
not select a universal profile law for them.

This is a finite operator-level result.  It is not a Möbius-weight theorem,
an arithmetic cancellation estimate, a power saving, or a twin-prime proof.

## What is new

TPC-322 supplied the typed map

```text
direct-sum blocks -> sign-labelled projector -> coherent signed operator.
```

TPC-323 adds the shape coordinate.  For the direct Gram
`G_direct=sum_p B_p^T B_p` and signed Gram `G_e=C_e^T C_e`,
`C_e=sum_p e_p B_p`, it records both

```text
rho_e = tr(G_e)/tr(G_direct)       (amplitude / energy)
pi_e  = spectrum(G_e)/tr(G_e)       (normalised shape).
```

The exact factorisation shows why an energy ratio cannot determine a profile
law.  A full-panel certificate then tests four declared laws with forward and
reverse accumulation, SciPy/NumPy spectral paths, and an independent
reverse/einsum replay.

## Claim firewall

```text
TPC323_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT
TPC323_SIGNED_PROFILE_FACTORISATION = PROVED_EXACT_FINITE
TPC323_ALL_PLUS_PROFILE_MAJORISATION = NUMERICALLY_CERTIFIED_FINITE_24_OF_24
TPC323_ALTERNATIVE_PROFILE_CENSUS = NUMERICALLY_CERTIFIED_FINITE_24_ROWS
TPC323_NAMED_LAW_SELECTION = NUMERICAL_OBSERVATION_ALL_PLUS_UNIQUE_ON_PANEL
TPC323_AMPLITUDE_SHAPE_DECOUPLING = NUMERICALLY_CERTIFIED_FINITE_ALL_PLUS_3_BELOW_21_ABOVE
TPC323_ARITHMETIC_ADVANCE = NO
TPC323_FIXED_POWER_CREDIT = 0
TPC323_FULL_GATE_B = OPEN
TPC323_TWIN_PRIME_RESULT = NONE
TPC323_STATUS = NUMERICALLY_CERTIFIED_FINITE_SIGNED_PROFILE_MAJORISATION_AUDIT
TPC323_ROUND2_CLUE = TEST_PROFILE_MAJORISATION_HOLDOUT_OR_SOURCE_NATIVE_ARITHMETIC_L2
```

The word “unique” is scoped to the four predeclared finite laws and the
declared panel.  It is not a uniqueness theorem for arithmetic weights.

## Reproduction

From the repository root:

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B papers/tpc-323-signed-profile-majorization/code/tpc323_signed_profile_majorization.py --write
python -B papers/tpc-323-signed-profile-majorization/code/tpc323_signed_profile_majorization.py --check
python -O -B papers/tpc-323-signed-profile-majorization/code/tpc323_signed_profile_majorization.py --check
python -B papers/tpc-323-signed-profile-majorization/experiments/tpc323_independent_checker.py --check
python -O -B papers/tpc-323-signed-profile-majorization/experiments/tpc323_independent_checker.py --check
python -B papers/tpc-323-signed-profile-majorization/experiments/tpc323_profile_stress.py --check
python -O -B papers/tpc-323-signed-profile-majorization/experiments/tpc323_profile_stress.py --check
```

The machine-readable result is
`results/tpc323_certificate.json`; the manuscript is `paper/paper.pdf`.
The local Bridge-B record and checker are in
`research/tpc-big-road/bridge_b_tpc323_signed_profile_majorization.md` and
`research/tpc-big-road/tpc_bridge_b_tpc323_signed_profile_majorization_checker.py`.

The Session-named `propose.md` and official Route-A/Route-B evaluator files
are absent from this checkout.  The proof package, independent replay, stress
suite, and local Bridge-B checker are therefore a fail-closed local record,
not an official evaluator pass.

## Package contents

`PAPER_PLAN.md`, `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, `notes/`,
`code/`, `experiments/`, `results/`, and `paper/` form the auditable paper
package.  The next question is whether the all-plus profile selection survives
a fresh source panel or an actual source-native arithmetic interface.
