# TPC-314 theorem ledger

| ID | Statement | Status | Scope |
|---|---|---|---|
| T314.1 | weighted Gram expansion and PSD interpretation | PROVED_EXACT_FINITE | every declared finite row |
| T314.2 | positive diagonal normalizer and weight-scale invariance | PROVED_EXACT_FINITE | nonzero finite physical family |
| T314.3 | range-reduced 120-term atanh enclosure for log(p) | PROVED_EXACT_FINITE | primes in the declared shells |
| T314.4 | outward interval propagation on the 10^-36 grid | PROVED_EXACT_FINITE | finite expression trees |
| T314.5 | minimum target below one for all three laws | NUMERICALLY_CERTIFIED_FINITE | 24 cases on TPC-312 panel |
| T314.6 | all-positive target above one for all three laws | NUMERICALLY_CERTIFIED_FINITE | 24 cases on TPC-312 panel |
| T314.7 | minimum law-order crossover | NUMERICALLY_CERTIFIED_FINITE_OBSTRUCTION | 7 one order, 1 crossover row |
| T314.8 | positive-law amplitude order is not invariant | NUMERICALLY_CERTIFIED_FINITE_OBSTRUCTION | 4 strict order types |
| T314.9 | canonical weighting theorem or growing weighted bound | OPEN | no asymptotic source theorem |

    STRONGEST_POSITIVE_RESULT = 24/24 minimum and 24/24 positive cases retain
                                 the finite separation class under the declared
                                 positive laws
    STRONGEST_OBSTRUCTION = law-dependent amplitude; one minimum crossover and
                            four positive-control ordering types
    OPEN_THEOREM = lock the same law menu before recomputing targets on a fresh
                   source interval, then seek a growing weighted estimate
    REUSABLE_STRUCTURE = frozen physical Gram -> declared positive laws -> exact
                         rational/log interval -> weighted ratio -> order/class
                         firewall
    ROUND2_CLUE = REPLICATE_THE_LOCKED_WEIGHT_LAW_MENU_ON_A_FRESH_SOURCE_INTERVAL_WITH_WEIGHTS_FIXED_BEFORE_TARGET_RECOMPUTATION
