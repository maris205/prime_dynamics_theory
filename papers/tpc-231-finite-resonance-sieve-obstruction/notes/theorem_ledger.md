# TPC-231 theorem ledger

| ID | Statement | Status |
|---|---|---|
| T231.1 | `p=3k+a`, `r=16t+3a-7k`, determinant `16Q` | `PROVED_EXACT` |
| T231.2 | Exact local root law at every prime | `PROVED_EXACT` |
| T231.3 | `E_3716(Q)<<S(Q)Q/log^2 Q` | `PROVED_SOURCE_BACKED` |
| T231.4 | `S(Q)<<log log(3Q)` | `PROVED` |
| T231.5 | `E_3716(Q)/P(Q)->0` | `PROVED_ASYMPTOTIC` |
| T231.6 | Any fixed finite primitive linear resonance family has `o(P)` edges | `PROVED_ASYMPTOTIC` |
| T231.7 | Bounded-degree bounded-coefficient comparable-row saving is `o(D)` | `PROVED_EXACT_TRANSFER` |
| T231.8 | Literal aligned first-resonance matched mass has density zero | `PROVED_IN_NAMED_MODEL` |
| T231.9 | First-resonance fixed positive saving, including `1/400` | `STOP_SCOPED` |
| T231.10 | Growing resonance depth | `OPEN` |
| T231.11 | Actual V59 source mass crosswalk | `OPEN` |

Strongest positive result: a uniform Selberg-sieve upper bound with exact determinant
singular series, promoted to a fixed-finite-family theorem.

Strongest obstruction: every fixed finite resonance support occupies `o(1)` of the
prime shell, so comparable row masses cannot supply fixed global saving.

Open theorem: determine whether growing resonance depth accumulates enough physical
mass, or construct the actual V59 source-to-row crosswalk.

Reusable structure: affine determinant → local root law → singular series →
support-density → energy-capacity compiler.

`ROUND2_CLUE = TEST_GROWING_RESONANCE_DEPTH_OR_RETURN_TO_THE_ACTUAL_V59_SOURCE_MASS_CROSSWALK`
