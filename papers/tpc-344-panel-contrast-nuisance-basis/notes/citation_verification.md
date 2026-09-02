# TPC-344 citation and provenance verification

No external literature claim is needed for this finite audit.  The mathematical
identities are proved directly in `PROOF_PACKAGE.md`; all numerical inputs are
repository artifacts.

The producer checks the TPC-343 producer and certificate before reading its
lineage, and then uses the TPC-340 producer/source implementation.  The
independent checker uses the TPC-340 reverse-shell engine and checks the same
parent locks without importing the TPC-344 producer.  Parent status labels,
operator parameters, panel origins, and canonical certificate encoding are
part of the executable provenance contract.

The missing Session evaluator files are explicitly disclosed in
`notes/route_evaluation.md`.  No official evaluator pass is claimed.
