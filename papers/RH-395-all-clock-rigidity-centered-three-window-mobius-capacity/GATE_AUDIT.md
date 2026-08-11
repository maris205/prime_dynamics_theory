# RH-395 gate audit

## Mathematical release gates

| Gate | Required condition | Result |
|---|---|---|
| M1 | fixed `q`, fixed tables, every admissible terminal clock | pass |
| M2 | RH-394 exact three-shift table law covers the centered score | pass |
| M3 | positive projection and relation saturation preserve the claimed inequality and safety | pass |
| M4 | all-clock optimizer uses the full eight-state formula | pass |
| M5 | four-state compression restricted to `q>=3` | pass |
| M6 | `q=1,2` self-loops separately proved | pass |
| M7 | small-clock values and clock-6 strict gain rigorously ordered | pass |
| M8 | coordinatewise marginal identity and run charge proved | pass |
| M9 | same-support saturation and cofinal lcm bridge proved | pass |
| M10 | strict finite nonattainment and endpoint lower witnesses proved | pass |

## Source and integrity gates

| Gate | Required condition | Result |
|---|---|---|
| S1 | RH-394 identity and sole terminal-log analytic role exact | pass |
| S2 | RH-375 identity and finite-combinatorial-only role exact | pass |
| S3 | Git source groups `128+8+4+8=148` exact | pass |
| S4 | four ordered remote locks, logical total 152, logical digest exact | pass |
| S5 | redistribution vector `false,false,true,false` and no external vendoring | pass |
| S6 | all six payload identities absent from members and whole tree | pass |
| S7 | four offline replays make exactly zero requests | pass |
| S8 | four bibliography keys resolve with correct role/locator scope | pass |
| S9 | theorem and source reviews each report zero blockers and zero minors | pass |

## Executable and archive gates

| Gate | Required condition | Result |
|---|---|---|
| E1 | all frozen Stage-1/manuscript hashes exact | pass |
| E2 | result and schema fresh/stored equality | pass |
| E3 | official closed Draft 2020-12 validation, zero errors | pass |
| E4 | 72-row certificate digest exact; all semantic mutations rejected | pass |
| E5 | normal and optimized release tests use runtime requirements, no bare assertions | pass |
| E6 | semantic PDF byte-identical to `main.pdf` | pass |
| E7 | exact publication membership and regular safe paths | pass |
| E8 | symlink/cache/bytecode/sentinel/CR/EOF/unlisted/special counters zero | pass |
| E9 | fresh manifest and outer verification report match stored bytes | pass |
| E10 | archive verification `failure_count=0` | pass |

## PDF gates

| Gate | Required condition | Result |
|---|---|---|
| P1 | LaTeX/BibTeX log has no unresolved reference/citation or box warning | pass |
| P2 | Ghostscript parses the PDF | pass |
| P3 | title, theorem, endpoint, limitations, declarations, and references extract | pass |
| P4 | nine A4 pages, unencrypted | pass |
| P5 | 25/25 font rows embedded, subset, and Unicode-mapped | pass |
| P6 | all nine rendered pages visually clean | pass |

## RH program Gates A--E

| Program gate | State after RH-395 |
|---|---:|
| A: intrinsic determinant | false |
| B: scattering completion | false |
| C: self-adjoint generator | false |
| D: von Mangoldt weighted prime-power traces | false |
| E: completed-zeta divisor equality | false |

RH-395 is a Möbius finite-state capacity theorem.  It does not construct an
operator, prove a trace formula, identify zeta zeros, establish completed-zeta
divisor equality, or prove the Riemann hypothesis.  Release verdict: all
in-scope gates pass; program Gates A--E remain false.
