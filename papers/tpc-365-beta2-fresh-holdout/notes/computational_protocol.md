# TPC-365 computational protocol

The producer first scans 51 candidate origins using only beta=2 unsigned
weighted square geometry on 256-point pilots.  It ranks the resulting spread
scores, applies the declared 2048 separation rule, and freezes
`(413342,410258,416940)`.  Signed responses are not read during selection.

The frozen holdout evaluates beta `{0,2}`, counts `{256,512}`, shell anchors
`{80,128,256,512}`, exponents `{1,2}`, and laws
`{all_plus, alternating_index, mod4_character, half_split}`.  Thus there are
`384` rows, with all four true spectra per setting.  The producer accumulates
primes in increasing shell order; the independent checker accumulates them in
reverse order and uses an independently written sieve and exact anchor.

The inherited spectral cap `0.64` and Schur cap `0.83` are finite working
thresholds.  The stress protocol applies 19 mutations and requires every one
to be rejected without changing the baseline certificate.  The Bridge-B
checker locks claim-bearing files, verifies the PDF and compile diagnostics,
and runs producer, independent, and stress checks in normal and optimized
modes with empty stderr and byte-identical stdout.
