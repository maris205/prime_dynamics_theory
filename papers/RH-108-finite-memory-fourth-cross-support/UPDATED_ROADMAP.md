# Route update after RH-108

## What RH-108 closes

RH-95 and RH-101 now combine into an explicit conditional gate:

1. compute a recent projected-cross spectrum (directly or through
   `M_2-A^2`);
2. pay the positive finite-memory tail `delta`;
3. certify `s4/s1 >= tau` from the Weyl margin.

The two finest archived scales pass this certificate at all three tested
cutoffs.  This is stronger than a raw numerical observation because the
forgotten history is paid by an explicit positive operator bound.

## The route barrier

The exact normalized-memory family in RH-108 keeps the memory clock and the
packet/complement diagonal blocks fixed while sending the fourth cross mode
to zero.  Therefore generic moment identities and finite-memory positivity
cannot prove an all-level lower bound.  The missing input must be specific to
the physical source-seeded family: a transverse-volume, determinant, or
singular-margin law.

## Next candidate layer

The next paper should test a physical nondegeneracy surrogate, ordered by
difficulty:

- a lower bound for a recent four-column cross determinant on the fine scales;
- a source/observation wedge-product or exterior-power estimate;
- a recurrence-level lower bound that survives the positive memory tail.

If none survives, the RH-108 barrier is a rigorous route boundary rather than
a failure of the numerical chain.  Moving-cloud, arithmetic trace,
zero-identification, and Hilbert--Polya work remain deferred.
