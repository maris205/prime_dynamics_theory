# Roadmap after RH-242

## Current coordinate

```text
finite_noise_periodic_superloop_open_grouped_envelope_and_anchor
```

The cloud-extracted trace is now an exact graded periodic-loop object: the
physical positive loop sector is paired with a finite spectral counterloop
sector.  This removes the need for a uniformly bounded Euclidean Riesz
projector at the identity level.

The next strict target is cancellation-preserving grouping.  One must group
physical and atomic loop contributions before taking absolute values and test
whether the resulting long-loop majorant is uniform in both order and noise.
In parallel, the one-step/two-step variable and the Hardy scaling must be
bridged before deterministic numerator coefficients can be used as an anchor.
