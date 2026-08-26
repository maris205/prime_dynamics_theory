# TPC-263 computational protocol

All executable checks are read-only and require an explicit `--check` flag.
The producer uses exact `Fraction` arithmetic for the block geometry,
Gaussian-rational arithmetic for the channel split, and rational exponent
ledgers.  The independent checker reimplements those calculations and applies
mutations to the parsed certificate; it does not import the producer.

The clock grid includes integer and noninteger clocks, odd and even child
cardinalities, and several asymmetric four-block sizes.  A separate residual
fixture has nonzero coordinates outside the first three frame coordinates, so
the identity is tested with `C_perp != 0`.

The certificate labels the asymptotic ingredients as source-backed inputs and
does not treat finite samples as proof of PNT or maximal Type-I estimates.
