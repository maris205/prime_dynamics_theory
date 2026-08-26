# TPC-261 computational protocol

1. Freeze the TPC-260 release commit and verify the eight source hashes from
   the baseline tree with `git show`.
2. Recompute all budget records using exact `Fraction` arithmetic.  Check the
   strict, borderline, insufficient, local-only, and log-only lanes.
3. Verify the scaled plus/alternating witness symbolically: both packet
   diagonals and null projections agree, while the full squared outputs are
   `16*x^(5/3)` and zero.
4. Run an independent checker that does not import the producer.  Mutate the
   schema, claim, threshold, lane records, witness, and firewall and require
   every mutation to be rejected.
5. Run the rational stress grid over savings and losses in both ordinary and
   optimized Python modes.

These checks certify the algebra and provenance only.  They do not sample or
estimate the literal growing prime shell and cannot pay arithmetic `L2` or
Gate B.
