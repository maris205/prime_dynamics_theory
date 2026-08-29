# TPC-310 computational protocol

1. Lock the released TPC-309 producer and canonical JSON result by normalized
   SHA-256.
2. Parse the 162 positive envelope records without regenerating labels or
   changing the physical source.
3. Enumerate all nonempty profile-ladder subsets and radius subsets.
4. For each selector compute pooled-MSE, balanced-ratio, and geometric-ratio
   intervals using decimal high precision.
5. Apply the strict `0.9/1.1` class rule and retain unresolved intervals.
6. Write a canonical JSON certificate; `--check` must reproduce it byte for
   byte.
7. Run the independent parser/replay and the exact rational stress suite in
   normal and optimized Python modes.

The parent interval inputs are padded float-replay enclosures.  The producer
therefore makes no directed-rounding claim.  No source target is regenerated,
and no claim is made that a pooled ratio is a canonical arithmetic observable.
