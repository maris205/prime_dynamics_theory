# TPC-298 paper plan

## Question

Does the literal source-profile family become quantitatively expressive only
after a growing number of cutoff directions, and can that statement be made
without confusing an unrestricted finite image with the native source?

## Frozen objects

- the TPC-295 physical operator and 18-row grid;
- the TPC-297 literal source formula;
- ordered cutoffs
  `3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61`;
- weighted minimum, max-cut, and all-positive target controls;
- modular rank checks modulo `1000000007` and `998244353`.

## Planned claims

1. For nested prefixes `V_k=A^T U_k`, least-squares residual equals the
   principal-angle sine and is monotone in `k`.
2. Every registered prefix has rank `min(k,|S|)` in both modular replays.
3. The weighted target's first prefix with RMS at most `1/2` has
   `k/|S| >= 2/3` on all rows; the positive control has `k <= 6`.
4. These are finite diagnostics only; no asymptotic or arithmetic credit is
   assigned.

## Falsification tests

- compare every stored prefix rank and residual with a source-first replay;
- perturb targets and use exact matrix fixtures to test monotonicity,
  threshold bookkeeping, and the `sin^2+cos^2=1` identity;
- run normal and optimized interpreters with empty stderr;
- require canonical JSON, provenance locks, and warning-free PDF output.

## Next decision rule

If the weighted dimension fraction stays large while the positive control stays
small, study least-norm source cost and conditioning for the prefixes.  If the
ladder collapses at small dimension on an expanded grid, attack that apparent
positive signal independently before any arithmetic extrapolation.
