# TPC-269 computational protocol

The producer imports only the released TPC-268 finite interval engine for the
exact finite arithmetic. It computes both kernel outputs separately and combines
them with a rational theta. The independent checker contains its own prime sieve,
factorization, beta, comparison, operator, projection and mixture replay.

Decimal logarithms and the Euler tail use the upstream 100-digit outward
interval protocol with P=50000. Classification is based on rho^2 and threshold
1/16. Normal and optimized executions must be byte-identical.

The stress audit checks the finite z_N schedule, profile flip, mixed contraction
and obstruction counts, and a positive threshold margin.
