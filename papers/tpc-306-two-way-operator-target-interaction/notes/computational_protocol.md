# TPC-306 computational protocol

The producer locks the normalized-LF SHA-256 digests of the TPC-305 producer and
certificate.  It reads the 18 parent cases and, for each of the three
normalizers, converts the two TPC-305 transported/native ratio enclosures into
log-effect enclosures using 80-digit `mpmath`.  A padding of `1e-30` is added
before interval arithmetic; the printed endpoints retain 38 significant
digits.

For each row it stores the left and right effects, main contrast, interaction
contrast, squared dominance gap, and `|i|/|m|`.  The finite checks require all
effects to be strictly ordered and all three normalizers to agree on the
classification.  The independent checker does not import the producer: it
replays the logarithms with 100-digit `Decimal`, verifies enclosure containment,
the center identity, and the full census.  The stress suite exhausts 625 small
positive four-cell tables, independent row scalings, and signed contrast
fixtures.
