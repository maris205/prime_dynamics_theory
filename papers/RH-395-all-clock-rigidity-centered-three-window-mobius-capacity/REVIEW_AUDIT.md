# RH-395 independent review audit

## Theorem review

The final exact manuscript snapshot received zero blockers and zero minors.
The adversarial proof review checked:

- the centered/noncausal model, fixed `q` and phase tables, universal
  distance-two safety, and every admissible terminal clock;
- the order fixed table, terminal limit, finite safe maximum, then scalar
  supremum over finite clocks;
- RH-394 as the sole terminal-log analytic input and the exact
  `L=+1,C=0,R=-1` shift convention;
- positive projection, the 512 relations, `2^18` full-table preimages,
  relation safety, nonnegative saturation, and the projected weight;
- the full eight-state tropical trace for every `q` and the sign-reflection
  argument for absolute value;
- the `q>=3` scope of four-state compression and the separate `q=1,2`
  self-loop proofs;
- `C(1),C(2),C(3),C(4),C(6)`, the one-site clock-6 value, and the rigorous
  sign of `2K2-K1`;
- divisibility lift, common square-support center charge, shared-coordinate
  marginal identity, pair charge, forced phase resets, run summation, and
  same-prime-support saturation;
- the cofinal lcm bridge, embedded one-site witnesses, strict finite
  nonattainment, and all model/scope/Gate firewalls.

The review specifically rejected three invalid substitutions: using the
four-state proof at `q=1,2`, treating RH-375's ordinary-Cesàro formula as a
terminal-clock theorem, and replacing the coordinatewise marginal identity
by a total-mass-only assertion.

## Source, citation, and PDF review

An independent source/citation/PDF review of the same exact snapshot also
returned zero blockers and zero minors.  It checked:

- RH-394 Theorem 1.1 equation (8), Theorem 1.2 equations (11)--(12), and
  Corollary 1.3 on printed/PDF pages 2--3;
- RH-375 Theorem 2.2 equation (7), Lemma 3.1 and Proposition 3.2 equations
  (8)--(9), equations (10)--(12), Proposition 4.1 equation (13), and
  Theorem 5.1 equations (16)--(17) on printed/PDF pages 2--5;
- all four bibliography keys, with Tao 2016 and Tao--Teräväinen 2019 kept as
  inherited RH-394 provenance rather than new direct analytic inputs;
- the `148+4=152` source closure, direct RH-394/RH-375 release identities,
  redistribution vector, nonvendoring, and six-payload exclusion;
- Ghostscript parsing, text extraction, A4 geometry, font embedding,
  LaTeX/BibTeX log cleanliness, metadata, and all nine rendered pages.

## Frozen manuscript snapshot

```text
main.tex         27596 B  8e3d65418d229bd5b990e2c528d2c3c8774b16ef3450d0a8a57f2be4291a30fe
references.bib    1438 B  e14fa2e2eea417bd2649f852478b212f8cfdb382dff69310b332527ff4f512f3
main.pdf        401435 B  24aec8e0e28fc6e9d88bb42ad8c2ae51efe33791ce8ba68d220dbf6c62887cde
main.log         25916 B  070f9ab3b98db18a197ab15906ee0fd405c51f7e773fb9fc654725046885cdab
```

The PDF has nine A4 pages and 25/25 embedded, subset, Unicode-mapped font
rows.  Verdict: accept within the stated fixed-clock, centered, noncausal
scope.
