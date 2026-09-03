# TPC-365 paper plan

## Question

Does the beta=2 shell tilt discovered on the reused TPC-364 panel transfer to
a fresh high-origin panel when its origins are selected by a declared rule
that reads geometry but no signed response?

## Frozen finite protocol

- candidate origins: `410001+257j`, `0<=j<51`;
- pilot count: `256`;
- selection beta: `2`;
- selection score: largest `max(G)/min(G)` over `Q={80,128,256,512}` and
  kernel exponents `{1,2}`;
- selection tie-break: descending score, then ascending origin;
- greedy minimum origin separation: `2048`;
- selected origins: `(413342,410258,416940)`;
- audited counts: `256,512`;
- audited shell anchors: `80,128,256,512`;
- audited kernel exponents: `1,2`;
- sign laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- compared betas: `0,2`;
- block weight: `w_(p,beta)=(p/Q)^beta`;
- normalization: weighted square-energy symmetric congruence.

The full Cartesian product has `2*3*2*4*2*4=384` law rows.  The selection
rule is frozen before any signed matrix is evaluated.  The inherited value
`0.64` remains only a finite working cap.

## Claim discipline

The exact contribution is the deterministic response-blind selection rule,
the finite weighted-block definition, positivity of the weighted geometry,
and the finite Schur/Frobenius envelopes.  The numerical contribution is a
complete beta=0 versus beta=2 fresh-panel replay with all four laws.  A
zero-failure beta=2 result is finite-scoped transfer evidence; it is not a
source-valid normalization theorem, an asymptotic estimate, a fixed-power
saving, a Route-A/Route-B pass, or a twin-prime conclusion.

## Decision rule for the next paper

The transfer result does not license another beta search.  The next minimal
test is to keep beta=2 fixed and extend the shell ladder beyond `Q=512` on a
new declared scale panel.  A failure is an obstruction locating the first
scale boundary; a pass remains finite evidence and moves the unresolved issue
to growing-`Q` control and source validity.
