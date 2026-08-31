# TPC-319 theorem ledger

| Item | Status | Scope / evidence |
|---|---|---|
| `G=A^*A` is PSD | `PROVED_EXACT` | finite linear algebra |
| Ky Fan variational identity | `PROVED_EXACT` | finite spectral decomposition |
| `0 <= F_k <= trace(G)` | `PROVED_EXACT` | nonnegative eigenvalues |
| normalization-flip identity | `PROVED_EXACT` | algebra for `N_2=2N_1` |
| dual shell-order top-17 spectrum | `NUMERICALLY_CERTIFIED` | 24 rows |
| Ky Fan interval containment | `NUMERICALLY_CERTIFIED` | 24 rows x 5 values of `k` |
| normalized cluster-mass decrease | `NUMERICALLY_CERTIFIED` | 80/80 adjacent comparisons |
| unnormalized cluster-mass increase | `NUMERICALLY_CERTIFIED` | 80/80 adjacent comparisons |
| edge-gap and effective-rank census | `NUMERICAL_OBSERVATION` | finite 24-row panel |
| uniform source-normalized spectral law | `OPEN` | finite panel cannot imply it |
| canonical clustered eigenspace | `OPEN` | edge gaps can be small |
| prime-shell arithmetic cancellation | `OPEN` | no signed reassembly |
| fixed-power credit | `0` | no asymptotic estimate |
| Route-B Gate B | `OPEN` | endpoint bridge unpaid |
| twin-prime conclusion | `NONE` | no implication asserted |

## Strongest positive

The Ky Fan formulation converts the top-eigenvalue question into a variationally
meaningful cluster mass, and the dual finite audit shows a consistent two-sided trend:
normalized masses fall while unnormalized masses rise for every tested `k` and pair.

## Strongest obstruction

The apparent compression is normalization-sensitive.  The exact factor-of-two identity
places every finite transition in the interval `1 < F_k(2N)/F_k(N) < 2`; no power saving
can be credited from the normalized plot.

## Open theorem

Find a source-scale normalization invariant that is justified by the prime-shell
operator and prove a growing bound for its top spectral cluster, then connect the
associated projector to signed arithmetic cancellation.

## Reusable structure

`literal matrix -> PSD Gram -> Ky Fan cluster mass -> dual interval -> normalization flip -> gap firewall`.

## ROUND2_CLUE

`AUDIT_A_SCALE_INVARIANT_SPECTRAL_MEASURE_OR_PROVE_A_SOURCE_NORMALIZATION_LAW_BEFORE_ANY_POWER_CLAIM`
