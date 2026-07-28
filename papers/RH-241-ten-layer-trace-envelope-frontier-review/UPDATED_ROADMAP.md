# Roadmap after RH-241

## Current coordinate

```text
projection_free_relative_det2_open_uniform_trace_envelope
```

## Gate A route

```text
rank-growing shell-complete cloud                 [done, finite]
reciprocal Fredholm variable                      [done]
direct uniform Riesz projector                    [ill-conditioned wall]
projection-free finite det2 factor                [done]
Hilbert--Schmidt complement route                 [too strong / bypassed]
cloud-extracted trace moments 2--12               [done, finite]
dual-channel finite-jet coherence                 [done, finite]
trace-adaptive shell selector                     [done, finite]
all-order uniform trace envelope                  [next wall]
coefficient anchor to deterministic numerator     [next wall]
locally uniform relative det2 family              [open]
dynamical small-noise realization                 [open]
Gate A closure                                    [open]
```

RH-242 should connect the complement traces to noisy periodic-loop integrals
and seek a bound uniform in both orbit length and noise.  A successful bound
must be accompanied by a no-over-extraction theorem identifying the residual
coefficient germ.  Gates B--E remain untouched.
