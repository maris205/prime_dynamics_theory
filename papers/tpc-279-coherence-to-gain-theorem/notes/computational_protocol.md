# TPC-279 computational protocol

The producer hash-locks the released TPC-278 code and canonical result.  For
each of its 12 positive outward gain intervals `[r_-,r_+]`, it computes the
exact reciprocal interval `[1/r_+,1/r_-]`.  It intersects the corresponding
reciprocal deficit interval with the parent cancellation interval, retaining
only the overlap.

The independent checker does not import the producer.  It recomputes all 12
reciprocals, signs, parent identities, and four sharpness witnesses with
`Fraction` arithmetic.  The stress checker mutates six theorem or provenance
fields and requires every mutation to be rejected.  Normal and optimized
Python paths must have byte-identical stdout.
