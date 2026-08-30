# TPC-313 paper plan

## Research question

Can the profile-budget interface left open by TPC-312 be certified with
strict, outward-rounded finite bounds on the same new source--shell panel?

## Frozen inputs

- source interval `I={321,...,640}` and `H=66`;
- shells `S_Q={p:Q<p<=2Q}` for `Q=24,36,54,80`;
- kernel exponents `s=1,2`;
- the TPC-312 physical `beta` rule and exact Gram-minimum labels;
- profile cutoffs `(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61)`;
- normalized target tolerance `tau=1/2`.

## Main finite claim

For every row, let `k*` be the first profile prefix whose least-squares
residual for the Gram-minimum target is at most `tau`.  Evaluate both that
target and the all-positive control on the common prefix `k*`.  Exact
rational ridge systems produce a feasible primal witness and a weak-dual
lower-bound witness.  Outward propagation on the `10^-36` grid certifies

```text
minimum-target dual budget ratio > 1/20000,
all-positive primal budget ratio < 1/100000.
```

## Proof obligations

1. Reconstruct the profile image and source Gram over `Q`.
2. Prove the ridge dual formula and weak-duality inequality.
3. Prove exact first-feasible-prefix scans.
4. Verify exact rational feasibility and digest every witness.
5. Enclose residuals, objectives, duals, ratios, and gaps by directed endpoint
   rounding.
6. Replay all rows independently and run signed/cancellation stress fixtures.

## Claim ceiling

The result is a finite certificate and an interface obstruction/advance.  It
does not claim external independence, causal identification, a uniform
asymptotic budget, arithmetic `L2`, fixed-power credit, Gate-B completion, or
the twin-prime conjecture.

## Next decision rule

If the certificate is stable, test an externally motivated weighting law on a
fresh physical source interval.  If it is not stable, preserve the exact
interval obstruction and do not make a global preference claim.
