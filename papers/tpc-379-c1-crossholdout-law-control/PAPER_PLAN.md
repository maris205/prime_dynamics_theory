# TPC-379 paper plan

## Question

TPC-378 transferred the finite c=1 support profile to fresh origins while
keeping the all-plus law fixed.  Is the profile a property of the c=1 mask and
common geometry, or is it specific to the all-plus sign choice?

## Frozen design

Use the response-blind affine grid `a_j=1200001+401j`, `0<=j<41`, and select
indices `(0,20,40)` before reading any response.  This gives origins
`(1200001,1208021,1216041)`, disjoint from all declared prior windows.  Use
the fixed count `N=1024`, four contiguous 256-point blocks, the inherited c=1
band, beta 2, exponent 1, height 66, and Q anchors `(512,2048,8192)`.  Freeze
all four parent sign laws in the order `all_plus`, `alternating_index`,
`mod4_character`, `half_split`; the panel is the complete 3-by-3-by-4
Cartesian product.

## Decision rule

Compute every law and origin at every Q before reading any failure census.  A
law-specific profile difference is a finite obstruction to promoting the
all-plus signature as law-invariant.  A common profile would support only a
scoped finite robustness observation.  Neither outcome is asymptotic evidence.

## Required audit

1. Verify the affine selection, exact coordinate separation, and common
   geometry.
2. Rebuild all four sign vectors directly from prime order, prime mod 4, and
   shell position; use one identical c=1 mask.
3. Evaluate all 36 rows before reading the law profile.
4. Recompute the panel with a direct-sieve reverse-shell checker that does not
   import the producer.
5. Run normal/optimized replay and 25 semantic/schema mutations.
6. Compile, render, and inspect every PDF page; preserve the TPC claim ceiling.

## Observed decision

The all-plus profile is `(0,3,3)` with 6/9 failures.  The alternating-index,
mod-4-character, and half-split controls each have `(0,0,0)`, with no Schur
failures in any law.  The law-control hypothesis is therefore refuted on this
finite panel: the inherited high-Q signature is strongly sign-law dependent.

The next minimal continuation is a count-2048 replay of the same frozen law
family and a new response-blind origin panel, recorded as
`TEST_C1_LAW_CONTROL_COUNT_REPLAY`.
