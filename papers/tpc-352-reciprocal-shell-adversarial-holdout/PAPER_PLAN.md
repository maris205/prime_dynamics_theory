# TPC-352 paper plan

## Question

Does the single, non-fitted reciprocal-shell contrast from TPC-351 transfer
to genuinely disjoint origins and a new shell ladder, or was its finite repair
specific to the training panel?

## Frozen protocol

- origins: `96097, 120097, 144097`;
- lengths: `256, 512, 1024`;
- shell anchors: `Q=64, 128, 256, 512`;
- kernel exponents: `1,2`;
- source laws: `all_plus`, `alternating_index`;
- height: `H=66`;
- interval: `I_(o,M)={o,...,o+M-1}`;
- reciprocal coefficients: `gamma_j=1/p_j-(1/r)sum_k 1/p_k`;
- parent: first `floor(r/2)` shell coefficients `+1`, last `floor(r/2)`
  coefficients `-1`, middle coefficient `0` when needed.

The origins and shell ladder are fixed before reading any response.  No row,
origin, length, law, matrix entry, singular vector, or response is used to
select coefficients.

## Claim-bearing sections

1. Define the literal masked block and defect.
2. Prove exact reciprocal balance, incidence identity, Gram expansion, and
   induced-norm lower witness.
3. Rebuild the new 144-row panel and compare reciprocal and balanced witnesses
   on exactly the same matrices and coordinate baseline.
4. Report scale breakdown and 48 length-series monotonicity records.
5. Use a different exact rational anchor (`I=[193,206]`, `Q=4`) to check the
   incidence algebra independently of floating point.
6. Run reverse-shell replay, hostile mutations, and Bridge-B provenance checks.

## Decision rule

`118/144` parent improvement is recorded as partial finite transfer.  The
reciprocal `Q=256` floor below the parent is recorded as an obstruction to a
uniform repair claim.  The result does not reopen any arithmetic gate.

## Route status

The reciprocal branch is a finite candidate/obstruction branch.  If this
holdout is not uniform, freeze it and return to the literal source-native
masked arithmetic `L2` interface; do not convert the finite census into a
growing theorem.
