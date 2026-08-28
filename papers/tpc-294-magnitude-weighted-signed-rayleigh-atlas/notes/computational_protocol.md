# TPC-294 computational protocol

The producer imports the frozen TPC-293 shell construction and the TPC-268
engine, but computes each physical output in target-first order.  It forms
the exact rational Gram matrix, clears denominators, and traverses all
$2^{m-1}$ sign vectors with a Gray update.  The result is written in canonical
JSON; no floating-point comparison decides a sign or an optimum.

The independent checker imports only the frozen TPC-268 engine.  It computes
each output in source-coordinate-first order, forms its own common-denominator
matrix, and uses direct reflected-binary enumeration to reconstruct every row
and aggregate.  It compares the complete row payload and finite audit.

The stress test is certificate-independent.  It compares the Gray routine
with brute force on 84 deterministic integer symmetric matrices, checks all
sign quotients on 49 deterministic Gram matrices, and rechecks the
all-positive complete-graph formula for $m=3,\ldots,12$.

Normal and optimized Python invocations must have empty standard error and
byte-identical standard output.  `PYTHONDONTWRITEBYTECODE=1` is used to keep
the repository clean.
