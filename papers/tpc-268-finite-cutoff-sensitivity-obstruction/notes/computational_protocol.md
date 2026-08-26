# TPC-268 computational protocol

The producer uses exact Fraction arithmetic for rational operator entries,
beta values, and projection algebra. Decimal logarithms use 100-digit
precision and a 10^-25 guard; the finite Euler product is enclosed by the
positive tail estimate

~~~text
sum_(p>P) (p-1)^(-2) < 1/(P-1), P=50000.
~~~

All interval endpoints are rounded outward to a 10^-30 rational grid.
Classification is made from rho^2: upper endpoint below 1/16 means
contraction, lower endpoint above 1/16 means obstruction. No square-root
rounding is used for the decision.

The independent checker uses a separate floating-point implementation,
replays all 16 rows, and rejects seven schema/claim mutations. The stress
script independently checks the central cutoff flip and designated controls.
