# TPC-372 paper plan

## Question

TPC-371 found no beta=2 cap failure in any independently normalized 256-point
block, while TPC-370 found six high-`Q` failures for the full-window-normalized
object.  TPC-372 keeps one common count-2048 normalization and asks how much
of the finite operator lies in a fixed block-diagonal part versus its
off-block remainder.

## Frozen protocol

The protocol is fixed from the TPC-371 result and parent failure phase:

* origins are `(1010001,1018021,1026041)`;
* the window is the full 2048-point interval at each origin, with the same
  square-energy normalization used by TPC-370;
* the fixed partition is eight contiguous blocks of length 256;
* `Q` is the complete declared set `{512,2048,8192}`, exponent is `1`, the
  law is the inherited `all_plus` law, and beta is `{0,2}`;
* all `3*3*2 = 18` rows are evaluated before any component metric is read.

For each normalized full matrix `A`, define `D` by retaining exactly the
entries whose two indices lie in the same fixed block, and define `R=A-D`.
The geometry is always the full-window geometry for all three matrices.  No
component is selected by its observed norm.

## Decision rule

If `D` stays below the spectral cap while `A` exceeds it, record the reverse
triangle lower bound `||R||_2 >= ||A||_2-||D||_2` and proceed to an eigenmode
block-separation audit.  If `D` itself fails, localize that fixed component
with a predeclared block-pair panel.  Either outcome remains finite and
scoped.

## Claim boundary

The intended contribution is a common-normalization decomposition certificate.
It can show that an off-block remainder is mathematically necessary for a
particular finite excess under the triangle inequality.  It cannot establish
causality, positivity of the remainder, origin/window uniformity, asymptotic
behavior, arithmetic `L2`, fixed-power credit, Route-A/Route-B closure, or a
twin-prime theorem.
