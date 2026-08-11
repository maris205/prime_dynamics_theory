# RH-396 independent review audit

## Theorem review

The final exact manuscript snapshot received zero blockers and zero minors
from the independent adversarial proof review.  The review checked:

- fixed `h`, fixed `q`, fixed phase tables, every admissible terminal clock,
  and the order limit -> finite maximum -> finite-clock supremum;
- the centered, explicitly noncausal window and universal distance-`2h`
  safety;
- RH-394 as the sole analytic terminal-log input, with collision-deduplicated
  `Theta`, phase-sum `kappa_h`, exact-support `Pi`, and weights `lambda`;
- positive projection, relation safety, nonnegative saturation, reflection,
  and the full eight-state tropical trace;
- four-state compression only when `q` does not divide `2h`, plus the strict
  `h=2,q=4` self-loop counterexample;
- raw `alpha` versus weighted `M`, the load-bearing equality `C=M`, the
  collision-aware `t=0` marginal, and the per-sign marginal identities;
- the `p0(h)` support condition, same-support scaling without a gcd
  hypothesis, and both exact `h=6` fixtures;
- finite and infinite `D`/`R` formulas, nonnegative run densities, the
  `p0(h)^2` cutoff, raw MWIS identity, and cofinal endpoint limit;
- fresh-prime recurrence, the `h=9` plateau, CRT creation of an even run,
  eventual strictness, arbitrary-clock bridge, and finite nonattainment;
- strict positivity above `3/pi^2` at every fixed lag, the outside-prime tail,
  the unattained infimum, and the absence of any other lag-landscape claim;
- every model, source-role, correlation-order, operator, zero, RH, and Gate
  firewall.

The review explicitly rejected: a collision-free `K_|S|` substitution for
`kappa_h`; an all-clock four-state claim; using `M` outside square support;
demanding `gcd(R,2h)=1` in the same-support cover; claiming strictness at
every lift; and promoting RH-375 or RH-395 to an analytic terminal-clock
input.

## Source, citation, and PDF review

An independent source/citation/PDF review of the identical snapshot also
returned zero blockers and zero minors.  It checked:

- RH-394 Theorem 1.1 and equations (8), Theorem 1.2 and equations (11)--(14),
  and Corollary 1.3 on printed/PDF pages 2--3;
- RH-395 Theorem 1.1, Lemmas 2.1--2.3, Propositions 3.1--3.3, Lemmas 4.1--4.2,
  and Proposition 4.3 as finite `h=1` precedent only;
- RH-375 Theorem 2.2, Lemma 3.1, Proposition 3.2, Proposition 4.1, and
  Theorem 5.1 as finite one-site/square-clock precedent only;
- all five bibliography keys and the inherited-only roles of Tao 2016 and
  Tao--Teravainen 2019;
- the `160+4=164` source closure, source commits, redistribution vector,
  nonvendoring, and exclusion of six external payload identities;
- Ghostscript parsing, text extraction, A4 geometry, unencrypted status,
  metadata, 24 embedded/subset/Unicode font rows, and all 15 rendered pages.

## Frozen manuscript snapshot

```text
main.tex          48304 B  5d9a8c6c9a39436d07a94e082fffc003cfba91ece1d3859c11e2facbd5ffe99d
references.bib     1739 B  2a5f201d51355bf0eb930484b4c9d3ad3d02bc145eed11809b0ab533956c599f
main.pdf         447519 B  590f472a38bbe652b4f3a2e1eac11a407d9c5ed8a076abb3419334106834db1d
main.log          25949 B  0cb4d57eb4c1f8ed0203a707fa8915258fb634c7499b69b21a232d731e061a25
```

The PDF has 15 A4 pages and 24/24 embedded, subset, Unicode-mapped font rows.
Verdict: accept within the fixed-lag, fixed-clock, centered, noncausal scope.
