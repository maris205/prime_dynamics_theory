# TPC-329 paper plan

## Research question

Does the source-native finite V59 residual retain the TPC-328 signed-Gram
behavior on a genuinely held-out origin/scale family, and can a fixed
source-multiset-preserving null distinguish arithmetic coordinate placement
from source-norm effects?

## Minimal advance

This paper is not a larger copy of TPC-328.  It adds two independent tests:

1. a two-origin, two-scale holdout with an explicit growth pairing; and
2. a predeclared affine permutation of the source coordinates that preserves
   the source multiset and `L2` norm but changes its placement relative to the
   literal matrix.

The first tests whether the finite sign pattern is immediately lost on new
scales.  The second attacks the weaker explanation that the readout is caused
   only by the marginal source values or their norm.

## Frozen protocol

* Origins: `28001`, `36001`.
* Scales: `4096`, `8192`; source counts are `2048`, `4096`.
* Shell anchors: `24`, `36`, `54`, `80`; exponents: `1`, `2`; height `H=66`.
* Source: the finite V59 model inherited and hash-locked from TPC-328 and
  TPC-267.
* Ratio guard: `5e-8`; arithmetic cutoff: `50000`.
* Placement null: `pi(i)=(5*i+17) mod source_count`.

The affine map is bijective because the source counts are powers of two and
`gcd(5,2^k)=1`.  It therefore preserves `sum_i v_i^2` exactly as a finite
vector operation.

## Claim-bearing outputs

1. A finite theorem/proof package for `E=D+O` and permutation norm invariance.
2. A canonical 32-row certificate with actual and permuted four-law metrics.
3. A 64-pair scale-growth audit and a 128-comparison placement audit.
4. An independent reverse-order replay and a mutation stress suite.
5. A narrow obstruction: all-plus classifications change on `31/32` rows under
   a norm-preserving placement permutation.

## Evaluation and stop rules

The release is accepted only if the producer, independent checker, optimized
variants, stress suite, PDF audit, and local Bridge-B normal/optimized equality
pass.  The Session-named Route-A/Route-B evaluator files are not present, so
the local proof/ledger/checker stack is explicitly a fallback.  No finite
observation may be promoted to a source-uniform estimate, fixed-power credit,
or twin-prime conclusion.

## Decision rule for the next paper

If the placement null changes the sign while preserving the source norm, the
next paper should quantify the placement mechanism (multiple predeclared
permutations or a position-aware kernel decomposition).  If it does not, the
next paper should attempt a structural signed-Gram inequality.  The observed
TPC-329 result selects the first branch.
