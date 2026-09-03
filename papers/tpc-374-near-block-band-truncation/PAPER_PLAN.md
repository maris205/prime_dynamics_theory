# TPC-374 paper plan

## Question

TPC-373 found that the selected extremal mode on the six beta=2 parent
failure rows has a strongly near-block Rayleigh profile.  The smallest
operator-level follow-up is to freeze the band consisting of block distances
`0,1,2,3` and ask whether that band itself reproduces the parent spectral
failure census under exactly the same full-window normalization.

## Frozen protocol

The inherited panel has origins `(1010001, 1018021, 1026041)`, count-2048
windows, eight contiguous blocks of length 256, `Q=(512,2048,8192)`,
kernel exponent one, the all-plus law, and `beta=(0,2)`.  All 18 rows are
constructed before any band metric or eigenmode is inspected.  The full
matrix is `T`; the predeclared near-block matrix is

```text
B3(i,j) = T(i,j) if |block(i)-block(j)| <= 3, and 0 otherwise.
R3 = T - B3.
```

The full matrix uses the full-window square-energy geometry for both `T` and
`B3`.  The selected full eigenmode is the largest-absolute-eigenvalue mode,
with the minimum mode winning exact ties.  No row, origin, response, or
component is selected after inspection.

## Decision rule

If `B3` preserves the parent beta=2 failure keys, record a finite operator
reproduction and quantify the omitted tail.  If it does not, record the
failure keys as an obstruction to this bandwidth.  In either case, do not
promote the result to an operator-uniform or growing-window statement.

## Claim boundary

The intended contribution is a predeclared, common-normalization,
response-blind finite band audit with independent replay and adversarial
mutation tests.  It supplies no cross-block causality, origin/window
uniformity, arithmetic `L2`, fixed-power credit, Route-A/Route-B closure, or
twin-prime theorem.  The official evaluator files named by the Session are
absent, so local Bridge-B evidence remains fail-closed repository evidence.

## Next decision

The result determines the next finite question.  A successful reproduction
opens a bandwidth-stability audit over smaller fixed cutoffs; a failure would
open a tail-sensitive counterexample audit.  The next clue is frozen as
`TEST_BANDWIDTH_STABILITY` until that decision is made.
