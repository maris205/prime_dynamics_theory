# TPC-227 theorem ledger

| ID | Statement | Status |
|---|---|---|
| T227.1 | V59 packet dependence is `a^(j)=beta+i^j w` | `SOURCE_LOCKED` |
| T227.2 | V59 uses one common Poisson profile `psi_+` | `SOURCE_LOCKED` |
| T227.3 | Four packet-dependent transforms reproduce the physical bilinear form iff all four Grams equal the physical Gram | `PROVED_EXACT` |
| T227.4 | Global unit packet phases are Gram-invisible | `PROVED_EXACT` |
| T227.5 | The Q25 row-dependent odd profile changes the collision Gram off diagonal by `-1/80000` | `PROVED_EXACT_FINITE_BLOCK` |
| T227.6 | TPC-226 balanced AP saving automatically supplies the V59 source sign | `REFUTED_SCOPED` |
| T227.7 | Source-native common-profile collision compiler | `OPEN` |
| T227.8 | Arithmetic signed saving | `OPEN` |
| T227.9 | Route-B `L2` or strict `1/400` payment | `OPEN` |

## Strongest positive result

The packet/profile transfer problem is reduced to an exact necessary-and-sufficient
Gram equality, with an executable Q25 obstruction witness.

## Strongest obstruction

A row-dependent profile sign changes cross-row Gram data and cannot be renamed as the
V59 source packet phase.

## Reusable structure

Four-point Gram DFT, target-Gram compatibility test, and collision-block witness.

## ROUND2_CLUE

`KEEP_THE_V59_PACKET_PHASE_ON_THE_SOURCE_SEQUENCE_AND_THE_POISSON_PROFILE_COMMON`
