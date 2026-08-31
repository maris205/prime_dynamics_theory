# TPC-318 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| `G=A^*A` is positive semidefinite | `PROVED_EXACT` | finite linear algebra |
| top eigenvalue is a spectral-radius readout of `G` | `PROVED_EXACT_FINITE` | finite PSD Gram construction |
| finite Weyl perturbation control | `PROVED_EXACT` | `\|E\|_2\leq\|E\|_F\leq N\max_{ij}|E_{ij}|` |
| dual forward/reverse shell top-spectrum audit | `NUMERICALLY_CERTIFIED` | 24 rows, two shell orders |
| independent symmetric solver agreement | `NUMERICALLY_CERTIFIED` | 24/24 rows, SciPy/NumPy paths |
| a-posteriori residual audit | `NUMERICALLY_CERTIFIED` | 24/24 top vectors |
| normalized top-eigenvalue decrease | `NUMERICALLY_CERTIFIED` | 16/16 adjacent-scale intervals |
| near-degenerate top eigenspace census | `NUMERICALLY_CERTIFIED_FINITE` | 10/24 rows have relative gap `<0.01` |
| unnormalized growing top-eigenvalue law | `OPEN` | normalization and source-scale law unpaid |
| clustered eigenspace stability theorem | `OPEN` | top/second gaps can be small |
| prime-shell arithmetic cancellation | `OPEN` | no signed reassembly |
| fixed-power credit | `0` | no uniform asymptotic estimate |
| Route-B Gate B | `OPEN` | arithmetic bridge and endpoint unpaid |
| twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

The actual top eigenvalue can be read on the frozen finite operator, with two
shell orders, two symmetric numerical paths, residual checks, and a finite
Weyl guard.  All 16 adjacent normalized comparisons are strictly separated.

## Strongest obstruction

The leading eigenspace is not uniformly simple on the audited panel: 10 of 24
rows have relative top/second gap below `0.01`, with minimum approximately
`0.001704`.  A normalized finite decrease therefore cannot be promoted to an
unnormalized power saving or to a canonical arithmetic eigenvector.

## Open theorem

Prove a uniform source-scale law for the top spectral cluster (including a
normalization invariant under shell and source changes), and then connect its
projector to signed prime-shell cancellation.

## Reusable structure

`literal matrix -> PSD Gram -> dual top spectrum -> residual/Weyl interval ->
normalized trend -> eigenspace-gap firewall`.

## ROUND2_CLUE

`AUDIT_THE_TOP_EIGENSPACE_CLUSTER_AND_NORMALIZATION_LAW_BEFORE_ANY_ARITHMETIC_CANCELLATION_PROMOTION`
