# TPC-289 computational protocol

All vectors, Gram entries, signs, and threshold comparisons use Python
`Fraction` arithmetic over the frozen TPC-268 literal deleted-diagonal engine.
The result is canonical JSON with a payload hash.  The producer locks the
TPC-288 source code/result and the frozen engine by normalized-LF SHA-256.

The grid has 18 rows and 1,380 unordered pair comparisons.  The independent
checker reconstructs the output with the summation order reversed and checks
the complete canonical document.  The stress checker freezes one trusted
document and rejects ten mutations.  Normal and `-O` modes are required to
produce byte-identical stdout.  Decimal strings are display fields only.
