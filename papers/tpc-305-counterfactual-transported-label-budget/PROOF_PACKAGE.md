# TPC-305 proof package

## Proposition 1: well-defined finite transported target

For a nonempty overlap and binary labels, the integer inner product determines
an optimal global alignment sign.  The displayed `t_L` and `t_R` are therefore
binary full-shell vectors, agree with the neighboring label on the overlap up
to the unique deterministic gauge choice (with `+1` at a tie), and retain the
home vector away from the overlap.

**Proof.** The two possible overlap inner products are `u` and `-u`, so the
choice `sigma=+1` for `u>=0` and `-1` otherwise maximizes the aligned inner
product.  Each transported coordinate is a product of two signs.  The
off-overlap clauses copy the native sign.  ∎

## Proposition 2: fixed-operator target comparison

For each finite operator row, the native and transported budgets are values of
the same constrained quadratic program with only the target vector changed.
The common prefix `k=max(k_native,k_transport)` is feasible for both targets.

**Proof.** The profile columns are nested, so feasibility of a target is
monotone under adding columns.  By construction each target is feasible at its
own first feasible prefix and hence at their maximum.  The operator matrix
and source Gram are passed unchanged to both programs; only `b` changes.  ∎

## Proposition 3: finite orientation logic

If the left fixed-operator ratio is below one and the right fixed-operator
ratio is above one, the right neighboring label is cheaper on both operators;
the reversed inequalities give the left label.  If both ratios exceed one the
home operator is favored, and if both are below one the cross target is favored.

**Proof.** On the left operator the native target is `a_L` and the transported
target is the aligned right label; on the right operator the native target is
`a_R` and the transported target is the aligned left label.  Comparing each
ratio to one gives exactly the four cases.  ∎

## Numerical certificate statement

At fixed `(N,H,z)=(512,58,5)`, `Q=(50,60,70,90)`, `e in {1,2}`, and
`tau in {1/4,1/2,3/4}`, the locked high-precision atlas contains 18 cases and
36 fixed-operator tables.  Every ratio is strictly ordered with the same
classification under all three declared normalizers.  At `60->70`, five of
six cases are right-label-cheaper and one is home-operator-favored; all three
same-prefix parent descent cases are right-label-cheaper.

This last paragraph is a finite numerical certification, not an asymptotic
theorem.  The physical-operator interaction term and the arithmetic Route-B
gate remain open.
