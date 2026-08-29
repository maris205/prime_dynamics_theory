# TPC-303 computational protocol

1. Lock the TPC-302 producer/result by normalized LF SHA-256.
2. Select exactly the eight fixed-source rows `(N,H,z)=(512,58,5)` with
   `Q in {50,60,70,90}` and exponents 1 and 2.
3. Read the outward common-prefix weighted budget intervals for each tolerance
   and normalizer.
4. Compare adjacent interval endpoints; classify descent, ascent, or overlap.
5. Independently repeat the interval census without importing the TPC-303
   producer and run exact decimal stress fixtures.

No centers are used to decide strict order, and no finite transition is
interpreted as an asymptotic theorem.
