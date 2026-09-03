# TPC-361 route evaluation and proof package

## Object and scope

The object is the literal finite matrix

\[
 B_p(u,t)=p\frac{66^{2s}}{(66^2+(u-t)^2)^s}
 (1_{p\mid u-t}-(p-1)^{-1})1_{u\ne t}1_{p\nmid u}1_{p\nmid t},
\]

summed over primes `Q < p <= 2Q`.  Its unsigned mask energy is
`G_u=sum_{p,t} B_p(u,t)^2`, and the normalized matrix is
`D_G^{-1/2} A D_G^{-1/2}`.  This paper makes no source-response query and
does not perform the arithmetic reassembly needed by the twin-prime route.

## What is established

* **PROVED_STRUCTURAL:** for each finite real matrix, the Schur row-sum and
  Frobenius inequalities bound the operator norm.  The rational anchor on
  `[313060,313073]` has symmetric matrix and strictly positive geometry.
* **PROVED_EXACT_FINITE_RESPONSE_BLIND:** the six-setting geometry score,
  deterministic ordering, and 1536-separated greedy selection produce
  `(313030,311166,321651)` from the declared 51-candidate grid.
* **NUMERICALLY_CERTIFIED:** the producer and reverse-shell checker agree on
  288 rows, including 180 independently replayed spectra; the mutation stress
  rejects all 15 declared certificate mutations.
* **NUMERICALLY_CERTIFIED_FINITE_SCOPED:** the normalized Schur maximum is
  `0.80830232610282304`, the normalized spectral maximum is
  `0.62690716242733457`, and the largest spectral/Schur and
  spectral/Frobenius ratios are `0.77585950058997` and
  `0.62120835204021907`, respectively.

## Strongest obstruction

On the declared all-plus scale ladder, 54 adjacent transitions contain 12
increases, 36 decreases, and 6 flats.  The finite cap therefore does not
license a monotone-decay assertion, an origin-uniform growing bound, or a
fixed power saving.  The short-panel law census also has six mod-4 wins, so
all-plus is a useful stress law but not a theorem-level universal proxy.

## Claim firewall

```text
TPC361_GEOMETRY_SELECTION = PROVED_EXACT_FINITE_RESPONSE_BLIND
TPC361_HIGH_ORIGIN_REPLAY = NUMERICALLY_CERTIFIED_FINITE_288_ROWS
TPC361_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC361_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC361_TIGHTNESS_REPLICATION = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC361_LAW_UNIFORM_SHORT_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC361_SCALE_MONOTONE_DECAY = REFUTED_SCOPED_ON_DECLARED_LADDER
TPC361_GROWING_OPERATOR_BOUND = OPEN
TPC361_SOURCE_UNIFORM_L2 = OPEN
TPC361_ARITHMETIC_ADVANCE = NO
TPC361_FIXED_POWER_CREDIT = 0
TPC361_FULL_GATE_B = OPEN
TPC361_TWIN_PRIME_RESULT = NONE
```

The official evaluator files named by the Session are absent from this
checkout.  Accordingly, Route A and Route B are not declared passed; the
local Bridge-B checker is only a fail-closed reproducibility control.

## Reusable structure and next clue

The reusable pattern is

```text
geometry-only candidate scan
  -> separated high-origin selection
  -> all-law finite envelopes
  -> short all-law and long all-plus spectra
  -> reverse-shell replay + mutation stress + exact anchor
  -> finite cap/tightness transfer with explicit obstruction
```

`ROUND2_CLUE = TEST_SCALE_LADDER_AND_SIGN_LAW_INTERACTION_ON_A_NEW_PANEL`.
The natural next paper is a distinct scale-or-shell stress on this newly
selected panel, with any stronger claim conditional on the observed finite
transition and law interaction rather than assumed in advance.
