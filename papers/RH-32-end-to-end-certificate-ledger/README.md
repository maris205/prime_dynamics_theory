# RH-32: end-to-end certificate ledger

This paper composes the RH-24--RH-31 finite-model certificate chain and
records exactly where the contour argument closes and where it does not.

For the exact binary64 primal base realizations actually rebuilt by RH-28 at
`sigma = 1e-2, 4e-3, 2e-3`, 256-bit Arb eigenvalue balls certify:

- one augmented zero inside each stored circle;
- no projected Hessenberg pole inside or on each circle;
- projected determinant winding `1 - 0 = 1` with no ambiguous ball.

The audit found that RH-28's extended-Arnoldi base prefixes are not bitwise
identical to RH-24's earlier short-Arnoldi discovery NPZ files. They are
therefore snapshotted and certified separately. A full replay exactly
reproduces all 9,369 archived RH-28 arcs in every one of their 30 non-timing
fields, all deterministic scale-summary fields, and the snapshot arrays
bitwise. The RH-24 discovery realizations also have separate archived Arb
count certificates, but they are not silently substituted for the RH-28
base models.

The RH-31 sparse inertia bounds are then inserted into the exact RH-29
rank-one formula and transported to the selected RH-28 arc.  All three
selected arcs close with large margins.  The same rigorous one-center
Neumann transport reaches exactly one of `936`, `2065`, and `6368` arcs.
Its premise is rigorously false for every other archived arc, so a local
tightest-budget certificate cannot be promoted to a full-contour theorem.

The remaining gates are therefore explicit: complement-resolvent bounds on
all other arcs and a rigorous complement pole count/interior analyticity
certificate.  The result is for exact stored finite binary64 models.  It is
not a full-contour root count, continuum limit, Hilbert--Polya construction,
zeta-zero identification, or proof of the Riemann hypothesis.

## Reproduce

Run the fast unit and archive tests:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider
~~~

Rebuild the RH-28 base snapshots, recompute the three rigorous
eigenvalue-ball counts, and rebuild the ledger (about three minutes on the
archived server). To reproduce the committed bit patterns, use the archived
default BLAS environment rather than forcing a different thread count:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python experiments/run_end_to_end_audit.py
~~~

Replay the complete RH-28 archive one scale per process (continuing ARPACK
after a fork in the same process is intentionally avoided):

~~~bash
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_rh28_reconstruction.py \
  --sigma 0.01
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_rh28_reconstruction.py \
  --sigma 0.004
PYTHONDONTWRITEBYTECODE=1 python experiments/verify_rh28_reconstruction.py \
  --sigma 0.002
~~~

Rebuild only the inexpensive composition and provenance layers:

~~~bash
PYTHONDONTWRITEBYTECODE=1 python experiments/run_end_to_end_audit.py \
  --skip-projected-counts
~~~

The formal manuscript is `end-to-end-certificate-ledger.pdf`.
