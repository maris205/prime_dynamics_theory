# Bridge B V85: subcritical growing resonance depth

TPC-231 leaves growing resonance depth open.  Keep the exact TPC-226 modeled
clock \(h=4LQ\), primitive cutoff \(|m|\le\lfloor Lq/Q\rfloor\), and prime
shell \(Q<q<2Q\).

For \(L<Q/4\), every support collision has opposite signs and exactly one wrap:

\[
a r+b p=4LQ,\qquad 1\le a,b<2L,\qquad (a,b)=1.
\]

For fixed \(a,b\), solutions are two affine forms on an interval of length
\(O(Q/\max(a,b)+1)\), with determinant \(4LQ\).  The local exceptional primes
divide \(ab(4LQ)\).  The Selberg upper-bound sieve, with its interval remainder
kept explicit, is uniform for \(L\le(\log Q)^A\) and gives

\[
C_{a,b}(Q)\ll_A
\left(\frac{Q}{\max(a,b)}+1\right)
\frac{\log\log(3LQ)}{(\log Q)^2}
+O_A(Q^{1/2}).
\]

Here channels with parameter length below \(Q^{1/2}\) are counted trivially;
the Selberg branch handles the complementary intervals.  This prevents a
grazing shell intersection from being assigned a false large interval.

Since

\[
\sum_{a,b<2L}\frac1{\max(a,b)}<4L,
\]

the total channel count obeys

\[
C_L(Q)\ll_A\frac{LQ\log\log(3LQ)}{(\log Q)^2}.
\]

Hence \(L=o(\log Q/\log\log Q)\) implies \(C_L(Q)/P(Q)\to0\).
TPC-230's unmatched-mass floor then prohibits any fixed saving for
fixed-comparability rows throughout that range.

```text
TPC232_ROUTE_ADVANCE = YES
TPC232_GROWING_COLLISION_NORMAL_FORM = PROVED_EXACT
TPC232_UNIFORM_POLYLOG_DEPTH_SIEVE = PROVED_SOURCE_BACKED
TPC232_COLLISION_INCIDENCE_BOUND = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_DEPTH_DENSITY_ZERO = PROVED_ASYMPTOTIC
TPC232_SUBCRITICAL_FIXED_SAVING = STOP_SCOPED
TPC232_CRITICAL_DEPTH_SUFFICIENCY = OPEN
TPC232_DILATED_CLOCK = MODELING_CHOICE
TPC232_ACTUAL_V59_CLOCK_ATTACHMENT = OPEN
TPC232_ARITHMETIC_ADVANCE = NO
TPC232_ARITHMETIC_OBSTRUCTION = PROVED_SOURCE_BACKED
TPC232_FIXED_ATOM_CREDIT = 0
TPC232_L2 = NONE
TPC232_FULL_GATE_B = OPEN
TPC232_FULL_GATE_B_STRICT_1_OVER_400 = UNPAID_GLOBAL
TPC232_STATUS = PROVED_ARITHMETIC_OBSTRUCTION_L1
TPC232_ROUND2_CLUE = TEST_CRITICAL_DEPTH_CLOCK_MASS_AND_DEGREE_BEFORE_V59_ATTACHMENT
```

Strongest positive result: a uniform growing-channel sieve bound.  Strongest
obstruction: all subcritical depths remain density zero.  Open theorem:
critical-depth mass/degree or actual V59 attachment.  Reusable structure:
one-wrap normal form, determinant-local-density sieve, and coefficient weight
summation.

The finite scan covers 19 \((Q,L)\) records with two independent compilers.
It is reproduction evidence only.  The theorem does not prove a critical-depth
lower bound, source concentration, signed cancellation, \(L^2\), Gate B, or
the twin-prime conjecture.
