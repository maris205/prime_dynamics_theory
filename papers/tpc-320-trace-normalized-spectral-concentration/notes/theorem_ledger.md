# TPC-320 theorem ledger

## Proven exactly

1. For a finite PSD Gram matrix, the trace-normalized eigenvalues form a
   probability distribution.
2. \(0\leq C_k\leq1\), \(r_{\rm st}\geq1\), and \(r_{\rm part}\geq1\).
3. \(C_k\), stable rank, participation rank, and normalized spectral entropy
   are invariant under \(G\mapsto cG\) for every \(c>0\).
4. Positive numerator/denominator interval division gives the stated outward
   quotient enclosure.

## Numerically certified on the declared panel

1. 24 rows with \(X\in\{640,1280,2560\}\), \(Q\in\{24,36,54,80\}\), and
   \(s\in\{1,2\}\).
2. Five values \(k\in\{1,2,4,8,16\}\), hence 120 concentration intervals.
3. All 80 adjacent scale comparisons have strict trace-normalized
   concentration decrease.
4. The producer's dual shell-order and dual solver paths replay within the
   declared finite Weyl quotient guard; the independent checker reconstructs
   the matrices without importing producer code.

## Numerical observations only

1. Stable rank grows on 16/16 adjacent transitions.
2. Participation rank grows on 16/16 adjacent transitions.
3. Normalized entropy is variable and is not promoted as a monotone law.
4. Edge-gap counts and metric ranges are finite-panel diagnostics.

## Open

- Any uniform-in-\(X\) concentration theorem.
- Any asymptotic exponent or power saving.
- A theorem controlling \(T(G)/N\) at the arithmetic interface.
- Signed prime-shell reassembly, the Route-B Gate-B endpoint, and a twin-prime
  conclusion.

## Labels

    PROVED_EXACT = finite algebraic identities
    NUMERICALLY_CERTIFIED_FINITE = declared panel plus outward guard
    NUMERICAL_OBSERVATION = replayed finite point estimates
    OPEN = not established in this project
