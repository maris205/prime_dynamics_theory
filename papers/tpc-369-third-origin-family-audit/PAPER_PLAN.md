# TPC-369 paper plan (pre-response declaration)

## Question

Does the finite beta=2 long-window failure pattern certified in TPC-367 and
TPC-368 persist on a third origin family selected without response, source,
law, or geometry information?

## Frozen protocol

- candidate grid: `a_j=1010001+401j`, `0<=j<41`;
- predeclared indices: `0,20,40`, hence origins
  `(1010001,1018021,1026041)`;
- selection reads no response, source, law result, or geometry score;
- counts: `512,1024`;
- shell anchors: `Q={512,2048,8192}`;
- kernel exponent: `1`;
- laws: `all_plus`, `alternating_index`, `mod4_character`, `half_split`;
- compared betas: `0,2`;
- height: `66`;
- finite working caps: spectral `0.64`, Schur `0.83`;
- weight: `w_(p,beta)=(p/Q)^beta`;
- normalization: weighted square-energy symmetric congruence.

The complete Cartesian product has 144 law rows.  The exact rational anchor
is the half-open interval `[1010346,1010359)` at `Q=4`, exponent one, for
beta `0` and `2`.

### Pre-response anchor amendment

The initially written proof anchor `[1010342,1010355)` had a zero geometry
row and failed before any TPC-369 spectrum or signed response was evaluated.
The family, origins, counts, shell anchors, laws, beta values, and caps were
not changed.  The proof anchor alone is repaired by the deterministic rule:
starting at 1010342, scan consecutive 13-point intervals to the right and
take the first interval whose exact geometry is positive for both beta 0 and
2.  The first valid interval is `[1010346,1010359)`.  This rule reads only
unsigned exact geometry and is fixed before spectral replay.

## Outcome-neutral decision rule

The family and all protocol fields above are fixed before the first TPC-369
response is evaluated.  The producer must write the actual failure keys and a
boolean comparison with the parent six-key pattern; it must not reject a
non-replication outcome.  Exact replication leads next to a count-2048
window attack.  A changed pattern leads instead to residue-phase
localization.  Either result remains finite and carries no arithmetic or
fixed-power credit.
