# TPC-314 proof package

## Proposition 1: weighted Gram identity

For every finite vector family and every coefficient vector c,

    E_w(c) = || sum_{p in S_Q} c_p w_p g_p ||_2^2
           = sum_{p,q} c_p c_q w_p G_{p,q} w_q.

Proof. Substitute G_{p,q}=<g_p,g_q> and expand the finite square.  No limit
or floating-point operation is involved.

## Proposition 2: positive normalizer and scale invariance

If at least one g_p is nonzero and all w_p>0, then
D_w=sum_p w_p^2 ||g_p||_2^2>0.  For a>0, R_{aw}(c)=R_w(c).

Proof. Each summand in D_w is nonnegative and a nonzero component has a
positive square.  The scaling statement is direct substitution.

## Proposition 3: rational logarithm enclosure

For 0<=z<1, the identity
2 atanh(z)=2 sum_{j>=0} z^(2j+1)/(2j+1) has positive remainder after any
finite prefix.  Since every denominator in the remainder is at least
2N+1, the geometric bound in the derivation package follows.  Range
reduction gives log(p)=k log(2)+log(y) with z<=1/3.  Thus the producer's
120-term rational interval contains the exact real logarithm.

## Proposition 4: directed interval soundness

If input intervals contain their exact values, taking the minimum of the four
endpoint products encloses multiplication; analogous endpoint formulas hold
for addition, subtraction, and division by an interval that avoids zero.
Rounding the lower endpoint down and the upper endpoint up on a common grid
preserves containment.  Induction over the finite expression tree proves that
the stored numerator, denominator, and ratio intervals contain their exact
values.

## Proposition 5: finite audit statement

The producer and the independent checker rebuild the same eight physical
rows, reconstruct all three laws, and compare the resulting intervals.  The
certificate therefore supports exactly these finite statements:

* all 24 minimum-target intervals have upper endpoint below one;
* all 24 positive-control intervals have lower endpoint above one;
* the minimum-law order is log < count < reduced-residue on 7 rows and
  count < log < reduced-residue on one row;
* the positive-control law order has four strict order types across the eight
  rows.

These are finite certificates.  They neither identify a canonical law nor
provide a growing-shell, arithmetic, or twin-prime theorem.
