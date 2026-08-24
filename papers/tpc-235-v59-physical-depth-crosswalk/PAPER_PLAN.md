# TPC-235 paper plan

## Question

Can the normalized TPC-226--234 single-clock rows be identified exactly with the V59
physical source rows?

## Contribution

Derive the exact physical depth variable and prove an iff scale criterion for the
single-clock attachment.  Audit packet normalization against the four-phase source
identity and isolate the correct next object: a weighted direct sum over physical
denominators with one common packet transform.

## Sections

1. Frozen V59 source row.
2. Exact physical-depth reparameterization.
3. Single-clock compatibility iff theorem.
4. Polarization/normalization obstruction.
5. Corrected route and finite certificate.

## Claim class

`PROVED_STRUCTURAL_L1`.  This is an exact crosswalk and scoped obstruction, not an
arithmetic estimate.
