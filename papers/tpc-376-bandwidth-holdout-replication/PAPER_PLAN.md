# TPC-376 paper plan

## Question

TPC-375 found that the first cutoff in its finite list matching the parent
failure support was \(c=1\).  Does that profile survive on origins reserved
by the earlier response-blind candidate-grid protocol?

## Frozen design

Use the TPC-370 grid
\[
a_j=1010001+401j,\qquad 0\leq j<41.
\]
TPC-375 used indices \(0,20,40\).  Before reading any TPC-375 or holdout
response, reserve indices \(5,15,30\) for this paper.  Freeze the complete
Cartesian panel of those three origins with \(Q=512,2048,8192\), beta 2,
the all-plus law, exponent one, count 2048, and the inherited eight-block
partition.  Evaluate only the predeclared band \(B_1\).

The word holdout refers to grid indices.  The \(j=5\) and \(j=15\) windows
are not coordinate-disjoint from the nearest training windows; that overlap
is recorded rather than hidden.

## Decision rule

The primary finite question is whether the c=1 spectral failure profile by
Q is \((0,3,3)\), the profile observed by TPC-375.  A match is a scoped
finite replication; a mismatch is a scoped transfer obstruction.  Neither
outcome changes the arithmetic or growing-operator gates.

## Required audit

1. Prove the finite mask, normalization, and Rayleigh identities.
2. Recompute all nine rows before reading the failure profile.
3. Recompute the rows with a descending-shell independent implementation.
4. Run schema/claim mutations, normal/optimized replay, and Bridge-B.
5. Compile and render the paper and keep all numerical claims finite-scoped.

## Next decision

Because the holdout retains the parent Q-profile, the next minimal question
is whether the c=1 profile persists under a predeclared window-scale/count
holdout.  This is recorded as TEST_C1_WINDOW_SCALE_HOLDOUT.
