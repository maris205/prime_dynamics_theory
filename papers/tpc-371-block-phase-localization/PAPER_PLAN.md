# TPC-371 paper plan

## Question

TPC-370 found a persistent beta=2 spectral-cap failure in the full count-2048
window at high `Q` under the all-plus law.  The next minimal, response-blind
question is whether the same signal is already present inside a fixed local
phase of that window.  TPC-371 therefore partitions every declared window
into eight contiguous blocks of length 256 and recomputes the finite operator
on every block.

## Frozen protocol

The protocol is inherited from TPC-370 and is fixed before the formal replay:

* origins are the three response-blind grid points
  `(1010001,1018021,1026041)` from `1010001+401j`, indices `(0,20,40)`;
* the parent window count is `2048`, partitioned into block indices `0,...,7`,
  each containing exactly 256 consecutive integers;
* shell anchors are `Q in {512,2048,8192}`, exponent is `1`, laws are
  `all_plus`, `alternating_index`, `mod4_character`, and `half_split`, and
  beta is `0` or `2`;
* all `3*8*3*1*4*2 = 576` rows are retained; no block, law, origin, or shell
  is selected by a response, source, or geometry score;
* the inherited exact anchor is `[1010346,1010359)` at `Q=4`, exponent `1`.

The block-local normalization is recomputed on each block.  Consequently the
result is a localization audit of a family of finite local objects, not an
assertion that a block-normalized matrix is a principal submatrix of the
full-window-normalized matrix.

## Decision rule

If a beta=2 block-local cap violation occurs, the next project will use a
predeclared residue/origin partition to localize that surviving phase.  If all
beta=2 blocks pass while the parent full window has failures, the next project
will decompose the full-window normalized matrix into block-diagonal and
off-block parts.  No post-response cell repair is allowed.

## Claim boundary

The target contribution is a finite, independently replayed localization
statement.  It may refute, only on this declared panel, the hypothesis that
the parent failure is already visible in a single 256-point block.  It cannot
establish cross-block causality by itself, origin/window uniformity, an
asymptotic estimate, arithmetic `L2`, fixed-power credit, Route-A/Route-B
closure, or a twin-prime theorem.

All numerical values will be stored in a canonical certificate and checked by
a separate sieve plus descending-shell implementation.  The local Bridge-B
checker is repository evidence only because the Session-named official
evaluator files are not present in this checkout.
