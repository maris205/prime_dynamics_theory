# Roadmap after RH-249

## Current coordinate

```text
unbounded_shell_cone_partly_reachable_only_by_multiplicity_explosion
```

The frozen candidate window cannot be repaired by a mild multiplicity
relaxation.  Six endpoints are outside even the full nonnegative cone, while
the other 26 need weights incompatible with the fixed spectral multiset.

The current batch should therefore stop trying larger finite reweightings.
The next paper should state the exact finite-head/analytic-tail gluing
obligation: combine a certified anchored finite head with the RH-246 block
tail, and quantify precisely which missing certificates prevent application
of RH-240.

Gates A--E remain open.
