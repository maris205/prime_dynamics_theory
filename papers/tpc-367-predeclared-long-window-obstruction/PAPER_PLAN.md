# TPC-367 paper plan

## Question

Does the finite beta=2 cap signal from TPC-366 survive when both the
geometry-ranked origin selection and the short-window restriction are removed?
If not, where does the first scoped obstruction occur?

## Frozen protocol

- candidate grid: `a_j=620001+307j`, `0<=j<41`;
- predeclared indices: `0,20,40`, hence origins `(620001,626141,632281)`;
- no response, source, or geometry score is used in origin selection;
- counts: `512,1024`;
- shell anchors: `Q={512,2048,8192}`;
- kernel exponents: `1,2`;
- laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- compared betas: `0,2`;
- height: `66`;
- finite working caps: spectral `0.64`, Schur `0.83`;
- weight: `w_(p,beta)=(p/Q)^beta`;
- normalization: weighted square-energy symmetric congruence.

The Cartesian product has
`2*3*2*3*2*4=288` rows, with a true spectrum for every law.  The exact
anchor is the half-open interval `[620362,620375)` at `Q=4`, exponent one,
for beta `0` and `2`.

## Mathematical and numerical claims

The exact finite claims are the deterministic origin protocol, the weighted
block formula, nonnegative-square geometry, positivity on the exact anchor
and replay rows, symmetry, and the elementary finite Schur/Frobenius
envelopes.  The numerical claims are limited to the recorded 288-row
certificate and its independent reverse-order replay.

The result is classified as `NUMERICALLY_CERTIFIED_FINITE_SCOPED`, with the
long-window beta=2 transfer marked `REFUTED_SCOPED`.  No uniform-in-origin,
uniform-in-window, growing-`Q`, source-valid, arithmetic, Route-A, Route-B,
fixed-power, or twin-prime claim is permitted.

## Decision rule for the next paper

Replicate the localized beta=2 failure on a second predeclared origin family,
holding beta=2, exponent one, and the longer count fixed.  If it persists,
the obstruction becomes a broader finite-origin/window phenomenon; if it
disappears, the next paper should map residue-phase dependence.  Either
outcome is a useful route-map update.
