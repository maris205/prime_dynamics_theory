# Bridge B: TPC-273 finite margin-stability matrix

TPC-273 is the next hostile test after the TPC-272 correlation-margin budget.
It keeps the literal finite V59 physical operator inherited from TPC-268 fixed
and varies only registered comparison cutoffs and kernel exponents.  The
purpose is to test whether a finite margin interface can be treated as stable
before a source-level growing theorem has been proved.

## New finite result

For the four physical scale triples

```text
(N,H,Q) = (64,15,4), (96,20,5), (128,24,5), (192,32,6)
```

and the grid `z in {2,3,4,5}`, `s in {1,2}`, the parent outward interval for
the normalized correlation transfers exactly as

```text
m^2 = rho^2,
m^6 = (rho^2)^3.
```

The 32 rows contain 12 rows with `m<1/8`, 11 middle-band rows, and 9 rows
with `m>1/4`.  Two fixed-scale cutoff-only comparisons cross a threshold:

```text
(N,s)=(64,1),  z=2 -> 5: middle -> above one quarter,
(N,s)=(128,1), z=2 -> 3: middle -> below one eighth.
```

The phase census retains all rows: 30 are `NEGATIVE_REAL_AXIS`, two are
`POSITIVE_REAL_AXIS`, and none crosses zero.  The kernel-only control at
`(N,z)=(96,3)` keeps both exponent choices in the high band.  These are exact
finite interval decisions and not powers in `N`.

## Claim firewall

```text
TPC273_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION
TPC273_ROUTE_ADVANCE = YES_SCOPED_FINITE_MARGIN_STABILITY_OBSTRUCTION
TPC273_MARGIN_STABILITY_OBSTRUCTION = NUMERICALLY_CERTIFIED_FINITE
TPC273_CUTOFF_FLIPS = NUMERICALLY_CERTIFIED
TPC273_PHASE_FLIP = NUMERICALLY_CERTIFIED_FINITE_TWO_ROWS
TPC273_SOURCE_LEVEL_MARGIN = OPEN_ASYMPTOTIC
TPC273_GROWING_UNIFORMITY = OPEN_ASYMPTOTIC
TPC273_FIXED_POWER_CREDIT = 0
TPC273_ARITHMETIC_ADVANCE = NO
TPC273_L2 = NONE
TPC273_FULL_GATE_B = OPEN
TPC273_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC273_TWIN_PRIME_RESULT = NONE
TPC273_STATUS = NUMERICALLY_CERTIFIED_FINITE_MARGIN_STABILITY_OBSTRUCTION
TPC273_ROUND2_CLUE = TEST_SOURCE_LEVEL_MARGIN_UNIFORMITY_ON_THE_LITERAL_GROWING_CUTOFF
```

The finite obstruction cannot be promoted to an asymptotic counterexample:
the registered grid is not the source-level growing sequence.  In particular,
the two positive phase rows are retained rather than removed, and no fixed
power credit is assigned.  The Session-named `propose.md` and evaluator files
are absent in this checkout; the project proof package, theorem ledger,
certificate, independent replay, stress audit, bridge checker, and `AGENTS.md`
are the fail-closed local fallback.
