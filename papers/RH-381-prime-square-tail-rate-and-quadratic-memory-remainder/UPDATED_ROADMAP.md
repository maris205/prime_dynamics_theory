# RH-381 updated roadmap

RH-381 closes the first-order square-clock gap-rate trigger opened by
RH-380. The exact chain is

```text
RH-374 finite run Euler products
  -> normalized numerator X_j
  -> factorwise |X_j-X_infinity| <= 170T_j
  -> exact RH-379 H-tail product
  -> 0 <= M_j/A_j <= 1
  -> two exact tail-sum identities
  -> finite RH-380 telescope + cofinal limit
  -> 342T_y^2/pi^2 remainder
  -> positive normalized gap limit.
```

This chain is elementary at the prime-tail level. It does not use the prime
number theorem and does not replace `T_y` by a function of `p_y`.

## Immediate within-class edge

Define

```text
S_y = sum_(j>=y) a_(j+1)^2.
```

The exact identities in RH-381 show that `T_y^2+S_y` and `T_y^2-S_y`
enter the numerator and memory channels differently. A second-order
successor therefore has a real theorem edge only if it:

1. expands the normalized Euler ratios through first order with an
   all-order quadratic error;
2. identifies the Euler-product limit of `M_j/A_j` with a uniform error;
3. expands the `H` tail with a uniform quadratic error;
4. retains every surviving quadratic scale rather than silently replacing
   `S_y` by a multiple of `T_y^2`;
5. proves a cubic remainder without PNT unless a new prime-tail theorem is
   explicitly sourced.

RH-381 does not state the resulting second-order coefficients. Computing
more finite rows or fitting the gap does not reopen that edge.

## Class-enlargement edge

The first blocker beyond phasewise `c11=0` remains a natural-average theorem
for the required fixed-period weighted shift-two Mobius correlations. No
current source supplies it. Until such a theorem appears, nonzero phasewise
`c11` is `STOP_SCOPED`.

## Excluded promotions

There is no growing clock `q(N)`, adaptive-capacity convergence, intrinsic
operator, spectral determinant, prime-power trace formula, Riemann-zero
identification, Hilbert--Polya construction, or RH implication. Gates A--E
remain false/open.
