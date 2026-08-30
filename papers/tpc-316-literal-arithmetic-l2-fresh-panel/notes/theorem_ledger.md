# TPC-316 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| Literal source-to-output matrix is rational | `PROVED_EXACT` | finite displayed kernel on `I_X` |
| Difference/residue formula for `HS(A)^2` | `PROVED_EXACT` | equality for every declared finite row |
| Frobenius `L2` interface | `PROVED_EXACT_FINITE` | `||A beta||^2 <= HS(A)^2 ||beta||^2` |
| Coordinate-column lower witnesses | `PROVED_EXACT_FINITE` | 5 exact columns per row |
| Two-panel normalized-HS rise | `NUMERICALLY_CERTIFIED` | 8/8 matched `(Q,s)` rows, `640 -> 1280` |
| Frobenius/probe gap on fresh panel | `NUMERICALLY_CERTIFIED` | 16/16 finite rows; fresh ratios exceed 517 |
| HS envelope as a decaying proxy | `REFUTED_SCOPED` | false on the two declared panels |
| True operator-norm decay | `OPEN` | Frobenius envelope is too loose |
| Growing arithmetic `L2` theorem | `OPEN` | no fixed power supplied |
| Canonical normalization | `OPEN` | no law selected by this audit |
| Fixed-power credit | `0` | no asymptotic credit claimed |
| Route-B Gate B | `OPEN` | arithmetic reassembly and endpoint remain open |
| Twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

The literal finite operator is now instantiated and its full Frobenius
interface is exact and independently replayable, rather than merely typed as a
conditional hypothesis.

## Strongest obstruction

The normalized Hilbert--Schmidt envelope rises on every matched two-panel row,
while the fresh-panel upper/lower sandwich remains very wide.  Thus this
particular envelope cannot pay a negative power or identify the true spectral
scale.

## Open theorem

Prove a genuinely growing estimate for the true source-to-output operator, or
extract arithmetic cancellation that is sharper than the Frobenius mass while
preserving the literal prime-shell and deleted-diagonal structure.

## Reusable structure

`literal matrix -> signed-difference count -> exact HS mass -> coordinate lower
witness -> finite sandwich -> growth/no-credit firewall`.

## ROUND2_CLUE

`REPLACE_THE_FROBENIUS_ENVELOPE_BY_A_GROWING_OPERATOR_OR_ARITHMETIC_CANCELLATION_ESTIMATE_WITHOUT_IMPORTING_A_POWER_CLAIM`
