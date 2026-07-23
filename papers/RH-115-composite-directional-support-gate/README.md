# RH-115: composite directional support gate

RH-115 composes the fourth-mode ratio certificates from RH-110, RH-111, and
RH-114.  The exact identity

```text
q4 = nu4 / Lambda23
```

turns every normalized four-volume lower bound and common capacity upper
bound into a valid `q4` lower bound.  The maximum of separately valid lower
bounds remains valid.

The admitted gate uses direct Weyl, capacity-recovered spectral volume,
tail-energy trace volume, and the positive-tail PSD packet block.  Across 360
records it has zero dominance failures.  At `1e-8`, the packet-block route
certifies `114/120`, versus `113/120` for direct Weyl.  Counts at `1e-6` and
`1e-4` remain `109/120` and `98/120`.  Every fine record is certified at all
three ratio thresholds.

An exact-directional diagnostic would give `115/120` at `1e-8`, but it is not
admitted: two independently assembled binary64 Gram chains disagree on one
weak physical record, appearing under three threshold labels.  The maximum
ratio excess is archived.  A rigorous composite must first provide an
outward transport guard between those assembly paths.

This admission filter is part of the result, not a cosmetic caveat.
