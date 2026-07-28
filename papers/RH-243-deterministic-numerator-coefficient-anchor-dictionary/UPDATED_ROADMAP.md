# Roadmap after RH-243

## Current coordinate

```text
deterministic_anchor_target_defined_open_cloud_bridge_and_envelope
```

The deterministic trace-style target is no longer an unspecified symbol.
Its one-step Hardy-scaled coefficients are explicit periodic-orbit quantities,
and the two-step numerator supplies exactly their even subsequence.

The next strict test is anchored availability: replace the zero target of
RH-238 by the coefficient vector defined here and scan every shell-complete
candidate prefix.  A pass would produce a finite anchored selector candidate;
a failure must be recorded as a scoped obstruction for the frozen candidate
window, not as nonexistence of a different cloud.
