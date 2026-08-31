# TPC-317 claim firewall

```text
PROVED_EXACT_FINITE = G=A^*A is PSD; lambda_max(G)<=sqrt(trace(G^2));
                      sqrt(trace(G^2))<=trace(G); finite normalized L2 envelope;
                      exact rational trace-power identities
NUMERICALLY_CERTIFIED_FINITE = exact small rational anchor; 24 large rows;
                               16/16 Schatten-4 decreases; 16/16 HS increases
NUMERICAL_OBSERVATION = opposite finite trends suggest spectral compression
REFUTED_SCOPED = the TPC-316 Frobenius mass is not a sharp spectral proxy on
                 the declared finite panels
HEURISTIC = none used to decide a pass/fail comparison
CONJECTURE = none
MODELING_CHOICE = H, shell anchors, exponents, three finite scales, IEEE guard
OPEN = true top-eigenvalue asymptotic; arithmetic cancellation; canonical
       normalization; fixed-power credit; full Gate B; twin-prime endpoint
ARITHMETIC_ADVANCE = NO
FIXED_POWER_CREDIT = 0
FULL_GATE_B = OPEN
TWIN_PRIME_RESULT = NONE
```

The finite trend is not a claim that the true operator norm decays.  The
Schatten-4 quantity is an upper envelope; only a future growing theorem could
turn it into an asymptotic Route-B estimate.
