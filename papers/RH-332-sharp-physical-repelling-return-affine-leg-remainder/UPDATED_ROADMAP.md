# Roadmap after RH-332

RH-332 closes the sharp local theorem for the physical repelling-return row
in the exact data type needed by the second retained-path Duhamel term.  The
incoming law is the actual RH-324 physical first-leg prefix, `u` is retained,
and both orientations have a strictly positive order-`sigma` coefficient.

This advances one local interface only.  It does not compare a fully
physical two-leg law with a fully affine two-leg law by equality: replacing
the first leg is a separate hybrid term.  It also does not give a global
uniform row estimate.  The explicit source `x=b` has order-one physical
boundary/fold behavior, so all-cycle work must transport localized incoming
moments rather than take a supremum over the state interval.

The next route is **RH-333: Full boundary-cycle clearance-phase transport**.
It must:

1. freeze one natural-clock subsequence and its common phase
   `eta_sigma -> eta`;
2. transport the actual incoming laws, not repeatedly restart from the same
   local seed;
3. prove uniform moment bounds on every ordinary and critical chart;
4. sum the retained hybrid row errors through all `2k` legs and target
   `O(k*sigma)=o(k*R^(-2k))`; and
5. stop with a precise phase or stability obstruction if any chart loses
   those moment bounds.

The first admissible RH-333 test is the raw mass-one forward all-affine
chain: quantify whether early Gaussian noise creates a positive escape gap
before the closing source when its propagated standard deviation and the
physical chart are both on the `1/sigma` scale.  That is a candidate route,
not a conclusion of RH-332.  RH-333 must distinguish this raw forward model
from any cyclic bridge, Doob transform, or branch-complete non-Gaussian
reference, none of which has yet been defined in the required physical data
type.

Even a positive retained-path result in RH-333 would not be cyclic trace
control.  RH-334 must first freeze the physical observation map, and RH-335
must obtain the required physical trace-observation upper stability exponent
before signed two-channel trace Duhamel work can activate.  Parity/alias
replacement, the signed far remainder, off-alias background, and
head/counterloop determinant gluing remain separate later obligations.

Finite rows remain reproduction checks only.  Gates A--E remain false/open.
