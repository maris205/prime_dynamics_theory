# TPC-313 theorem ledger

| Item | Status | Evidence |
|---|---|---|
| Ridge dual formula and weak-duality lower bound | `PROVED_EXACT_FINITE` | `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md`, exact checker |
| First feasible profile prefix on each weighted row | `PROVED_EXACT_FINITE` | 8 exact prefix scans in certificate |
| Rational primal/dual witnesses | `PROVED_EXACT_FINITE` | 16 exact systems, digested coefficient and scalar values |
| Outward `10^-36` interval enclosure | `PROVED_EXACT_FINITE` | 16 independent interval replays |
| Weighted lower threshold | `NUMERICALLY_CERTIFIED` | 8/8 dual ratios `>5e-5` |
| Positive-control upper threshold | `NUMERICALLY_CERTIFIED` | 8/8 primal ratios `<1e-5` |
| External weighting law | `OPEN` | no law fixed by arithmetic input |
| Fresh physical holdout | `OPEN` | panel remains inside locked engine |
| Uniform growing-shell budget | `OPEN` | no asymptotic passage |
| Arithmetic `L2` / fixed power / Gate B | `OPEN` / `NONE` | not addressed by finite certificate |
| Twin-prime conclusion | `NONE` | no implication claimed |
