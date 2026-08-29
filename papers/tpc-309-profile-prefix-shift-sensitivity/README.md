# TPC-309 — Profile-Prefix Shift Sensitivity

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University
of Science and Technology (HUST), Wuhan, China

## One-line result

TPC-309 keeps the TPC-308 common-ambient operator, shell labels, and exclusive
completion protocol fixed while shifting the 17 source-backed profile cutoff
window one prime down (LOW), at the TPC-308 baseline (BASE), or one prime up
(HIGH).  The 54 profile cases and 162 radius observations reproduce BASE
exactly, but LOW/HIGH move strict discordances from the baseline final-
transition location to earlier transitions and expand the unresolved band.

This is a finite model-selection sensitivity obstruction.  It is not a causal,
asymptotic, arithmetic, or twin-prime theorem.

## Claim firewall

```text
PROVED_EXACT_FINITE = neighboring-window definition; prefix nesting; Hamming
                      candidate enumeration/extrema; radius monotonicity;
                      radius-zero recovery; normalizer cancellation; interval
                      class rule
NUMERICALLY_REPRODUCED_FINITE = 3 ladders x 18 cases x 3 radii = 162 envelope
                                 observations; candidates 108/558/1440
NUMERICAL_OBSERVATION = BASE has 3/2/1 strict discordances at 70->90 as
                        radius 0/1/2; LOW and HIGH relocate/attenuate them
MODELING_CHOICE = 19-prime pool, three contiguous 17-cutoff windows, profile-
                  recomputed primary budget, frozen-parent secondary audit
INHERITED_LEAKAGE = TPC-302 physical-Gram-dependent target labels
OPEN = directed rounding; profile-independent preference; causal identification;
       uniform asymptotic budget; arithmetic L2; fixed-power credit; full Gate
       B; twin-prime conclusion
```

## Locked finite census

| profile ladder | budget `(R,L,U)` | radius 0 agreement `(C,D,U)` | radius 1 | radius 2 |
|---|---:|---:|---:|---:|
| LOW | `(11,6,1)` | `(13,4,1)` | `(10,2,6)` | `(8,1,9)` |
| BASE | `(13,5,0)` | `(13,3,2)` | `(11,2,5)` | `(10,1,7)` |
| HIGH | `(9,7,2)` | `(10,5,3)` | `(5,0,13)` | `(5,0,13)` |

At radius zero, LOW's strict discordances are distributed across
`50->60`, `60->70`, and `70->90`; HIGH has strict discordances on the first
two transitions and one final-transition cell.  At radius two, strict
discordance remains in LOW and BASE but disappears in HIGH, with many cells
unresolved.  These are finite class counts, not estimates of a limiting law.

## Reproduction

```bash
export PYTHONDONTWRITEBYTECODE=1
python -B code/tpc309_profile_prefix_shift_sensitivity.py --write
python -B code/tpc309_profile_prefix_shift_sensitivity.py --check
python -B experiments/tpc309_independent_checker.py --check
python -B experiments/tpc309_profile_shift_stress.py --check
python -B research/tpc-big-road/tpc_bridge_b_tpc309_profile_prefix_shift_sensitivity_checker.py --check
```

The manuscript is [paper/paper.pdf](paper/paper.pdf); the canonical result is
`results/tpc309_certificate.json`.  The Session-named `propose.md` and
Route-A/Route-B evaluator files are absent from this checkout, so no official
evaluator pass is asserted.  The local fail-closed evaluation is the locked
TPC-308 parent, independent replay, exact stress suite, PDF audit, theorem
ledger, claim firewall, and Bridge-B checker.
