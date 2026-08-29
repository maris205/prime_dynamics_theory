# TPC-308 claim firewall

## PROVED_EXACT_FINITE

- Hamming-ball construction and candidate-count formula;
- exact finite extrema for a fixed prediction;
- radius monotonicity, radius-zero recovery, and global-sign invariance;
- conditional soundness of the positive ratio interval classification.

## NUMERICALLY_REPRODUCED_FINITE / NUMERICAL_OBSERVATION

- 18 locked shell-transition cells, three radii, 54 envelope observations;
- candidate totals `36`, `186`, `480`;
- agreement counts `13/3/2`, `11/2/5`, `10/1/7`;
- discordance counts `3`, `2`, `1`, all localized to `70->90`, exponent 1.

The producer uses a vectorized float64 physical replay, decimalized entries,
and high-precision frontier solves with padded enclosures.  The independent
checker uses a separate NumPy replay and slack.  This is not directed rounding.

## MODELING_CHOICE / INHERITED_LEAKAGE

The radii, binary completion family, frozen coefficients, and fixed profile
prefixes are finite protocol choices.  Labels inherit TPC-302's
physical-Gram-dependent construction, so this paper does not identify an
independent target law.

## OPEN / NONE

Completion invariance beyond the tested finite radii, causal identification,
uniform growing-budget asymptotics, arithmetic `L2`, fixed-power credit, full
Route-B Gate B, and a twin-prime conclusion remain open or none.
