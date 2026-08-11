# RH-396 gate audit

## Mathematical release gates

| Gate | Required condition | Result |
|---|---|---|
| M1 | fixed `h`, fixed `q`, fixed tables, every admissible terminal clock | pass |
| M2 | RH-394 exact three-shift table law at `(+h,0,-h)` is the sole analytic input | pass |
| M3 | collision-deduplicated `Theta`, phase-sum `kappa_h`, exact-support `Pi`, and `lambda` are exact | pass |
| M4 | positive projection, relation saturation, and reflection preserve the claimed optimization | pass |
| M5 | full eight-state tropical trace holds for every finite `q` | pass |
| M6 | four-state compression is restricted to `q` not dividing `2h` | pass |
| M7 | `h=2,q=4` strictly obstructs a universal four-state reduction | pass |
| M8 | raw `alpha`, weighted `M`, collision-aware marginal, and qualified equality `C=M` are exact | pass |
| M9 | same-support cover has the `p0(h)` base condition and no spurious gcd condition | pass |
| M10 | finite/infinite run densities, cutoff, MWIS identity, and Euler endpoint are exact | pass |
| M11 | fresh-prime recurrence permits plateaus but CRT proves eventual strictness | pass |
| M12 | every finite clock is strictly below `B_infinity(h)` | pass |
| M13 | fixed-lag endpoint is strictly above `3/pi^2`; lag infimum is unattained | pass |
| M14 | no supremum, maximum, or monotonicity claim over lags | pass |

## Source and integrity gates

| Gate | Required condition | Result |
|---|---|---|
| S1 | RH-395 direct predecessor identity exact | pass |
| S2 | RH-394 analytic-source identity and role exact | pass |
| S3 | RH-375 and RH-395 finite-precedent roles only | pass |
| S4 | Git source groups `148+8+4=160` exact | pass |
| S5 | four ordered remote locks give 164 logical inputs | pass |
| S6 | redistribution vector `false,false,true,false`; no external vendoring | pass |
| S7 | all six external payload identities absent from members and whole tree | pass |
| S8 | four offline replays make exactly zero requests | pass |
| S9 | all five bibliography keys resolve with declared roles | pass |
| S10 | proof and source/PDF reviews each report zero blockers and zero minors | pass |

## Executable and archive gates

| Gate | Required condition | Result |
|---|---|---|
| E1 | all 21 frozen Stage-1/manuscript identities exact | pass |
| E2 | result and schema fresh/stored equality | pass |
| E3 | official closed Draft 2020-12 validation has zero errors | pass |
| E4 | 96-row certificate digest exact | pass |
| E5 | all 32 core, 65 result, and 28 schema mutations rejected | pass |
| E6 | normal and optimized tests use runtime requirements; release tests contain no bare assertions | pass |
| E7 | semantic PDF byte-identical to `main.pdf` | pass |
| E8 | exact 41-member publication and 43-file release-stage membership | pass |
| E9 | unsafe path, type, symlink, cache, bytecode, sentinel, CR, EOF, unlisted, and special-file attacks fail closed | pass |
| E10 | fresh manifest and verification report match stored bytes | pass |
| E11 | archive verification `failure_count=0` | pass |

## PDF gates

| Gate | Required condition | Result |
|---|---|---|
| P1 | complete LaTeX/BibTeX log has no unresolved citation/reference or box warning | pass |
| P2 | Ghostscript parses the PDF | pass |
| P3 | theorem, endpoint, lag, firewall, declarations, and references extract | pass |
| P4 | 15 A4 pages, unencrypted | pass |
| P5 | 24/24 font rows embedded, subset, Unicode-mapped | pass |
| P6 | all 15 rendered pages visually clean | pass |

## RH program Gates A--E

| Program gate | State after RH-396 |
|---|---:|
| A: intrinsic determinant | false |
| B: scattering completion | false |
| C: self-adjoint generator | false |
| D: von Mangoldt weighted prime-power traces | false |
| E: completed-zeta divisor equality | false |

RH-396 is a fixed-lag Möbius finite-state capacity theorem.  It does not
construct an operator, prove a trace formula, identify zeta zeros, establish
completed-zeta divisor equality, or prove RH.  Release verdict: every in-scope
gate passes; program Gates A--E remain false.
