# TPC-317 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| `G=A^*A` is PSD | `PROVED_EXACT` | finite linear algebra |
| `lambda_max(G)<=sqrt(trace(G^2))` | `PROVED_EXACT` | eigenvalue proof |
| `sqrt(trace(G^2))<=trace(G)` | `PROVED_EXACT` | nonnegative eigenvalues |
| normalized Schatten-4 `L2` envelope | `PROVED_EXACT_FINITE` | every finite row |
| trace-square entry identity | `PROVED_EXACT` | finite matrix multiplication |
| small rational trace anchor | `PROVED_EXACT_FINITE` | `I={17,...,32}`, `p=5`, `s=1` |
| large-panel dual accumulation | `NUMERICALLY_CERTIFIED` | 24 rows |
| normalized Schatten-4 decrease | `NUMERICALLY_CERTIFIED` | 16/16 adjacent-scale comparisons |
| normalized Frobenius increase | `NUMERICALLY_CERTIFIED` | 16/16 adjacent-scale comparisons |
| Frobenius as sharp spectral proxy | `REFUTED_SCOPED` | declared panels only |
| true operator-norm decay | `OPEN` | top eigenvalue not certified here |
| arithmetic cancellation | `OPEN` | no prime-shell reassembly |
| fixed-power credit | `0` | no asymptotic estimate |
| Route-B Gate B | `OPEN` | signed reassembly and endpoint unpaid |
| twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

The exact finite PSD trace-power chain replaces the TPC-316 Frobenius envelope
with a strictly sharper operator-norm upper envelope, and its 24-row finite
certificate is independently replayable.

## Strongest obstruction

The calculation remains a finite numerical diagnostic: it does not certify the
top eigenvalue or a uniform growing estimate.  The large-panel intervals are
not a substitute for arithmetic cancellation.

## Open theorem

Establish a true top-eigenvalue or higher trace-power estimate with a uniform
source-scale law, then test whether it can pay any Route-B power budget.

## Reusable structure

`PSD Gram -> eigenvalue trace-power sandwich -> normalized finite envelope ->
dual accumulation interval -> trend firewall`.

## ROUND2_CLUE

`AUDIT_THE_TRUE_TOP_EIGENVALUE_OR_A_CERTIFIED_TRACE_POWER_LADDER_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION`
