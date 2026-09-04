# TPC-377 paper plan

## Question

TPC-376 reproduced the finite c=1 high-Q failure profile on a
response-blind grid-index holdout at count 2048. Does that profile survive
when the same origin windows are read at a predeclared ladder of nested
window counts?

## Frozen design

Keep the three TPC-376 holdout origins
(1012006,1016016,1022031). Before reading any new response, freeze the
count ladder (1024,1536,2048), the common block length 256, the c=1 band,
the all-plus beta-2 law, exponent one, height 66, and Q anchors
(512,2048,8192). Each count is a prefix with the same left endpoint and
has respectively 4, 6, or 8 blocks. The complete Cartesian panel has 27
rows.

## Decision rule

The primary finite question is whether every count has the parent profile
(0,3,3) by Q. A match is a scoped scale-ladder replication; a mismatch
would be a finite scale obstruction. The nested prefixes are not claimed
to be independent samples, and no asymptotic statement is attached.

## Required audit

1. Verify the finite normalization, band/tail, nested-prefix, and Rayleigh
   identities.
2. Build all 27 rows before reading the failure profile.
3. Recompute them with a descending-shell implementation that does not
   import the producer.
4. Run schema/firewall mutations and normal/optimized replay.
5. Compile and render the PDF; retain the arithmetic and growing-operator
   claim ceiling.

## Observed decision

The complete panel gives (0,3,3) at each of the three counts, with 18
spectral failures and zero Schur failures. The profile therefore survives
this finite scale ladder, while the spectral magnitudes change with count.
The next minimal hostile test is a response-blind new-origin cross-holdout
at the same count ladder, recorded as
TEST_C1_SCALE_ORIGIN_CROSSHOLDOUT.
