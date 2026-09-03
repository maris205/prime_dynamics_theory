# Bridge-B proof package: TPC-362

```text
TPC362_MAXIMUM_CLAIM = NUMERICALLY_CERTIFIED_FINITE_SHELL_SCALE_CAP_OBSTRUCTION
TPC362_SHELL_SCALE_REPLAY = NUMERICALLY_CERTIFIED_FINITE_384_ROWS
TPC362_FINITE_SCHUR_ENVELOPE = PROVED_EXACT_FINITE
TPC362_FINITE_FROBENIUS_ENVELOPE = PROVED_EXACT_FINITE
TPC362_LOW_Q_CAP = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC362_HIGH_Q_CAP_EXTENSION = REFUTED_SCOPED_ON_DECLARED_Q_LADDER
TPC362_LAW_WINNER_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED
TPC362_GROWING_OPERATOR_BOUND = OPEN
TPC362_SOURCE_UNIFORM_L2 = OPEN
TPC362_ARITHMETIC_ADVANCE = NO
TPC362_FIXED_POWER_CREDIT = 0
TPC362_FULL_GATE_B = OPEN
TPC362_TWIN_PRIME_RESULT = NONE
```

TPC-362 keeps the TPC-361 high-origin panel fixed and widens the shell ladder
to `Q=12,24,36,54,80,128,256,512`.  All four fixed laws are replayed at
counts `256,512`, giving 384 rows with true spectra.  The old working caps
`0.83` (Schur) and `0.64` (spectral) hold through `Q=80`; the first violations
occur at `Q=128`.  Across the full ladder there are 33 Schur and 30 spectral
cap-violating rows, with global maxima `1.7172665118910415` and
`1.6398895499394266`.

The 96-setting winner census is all-plus 78, alternating-index 4, mod-4 14,
and half-split 0.  The 336 adjacent Q transitions contain 200 increases and
136 decreases.  These are finite scoped diagnostics and a shell-scale
obstruction; they do not establish or refute an appropriately renormalized
asymptotic theorem.  Source-uniform arithmetic `L2`, a growing operator bound,
Route-B reassembly, fixed-power credit, and a twin-prime result remain open.

The Session-named official Route-A/Route-B evaluator files are absent, so this
is fail-closed local finite evidence rather than an official evaluator pass.
