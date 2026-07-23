# TPC-64: True Terminal Activation on Canonical Multiscale Incidences

This directory contains the source and final PDF for:

> *True Terminal Activation on Canonical Multiscale Incidences: Pair-Lift
> Minimality, Parent Inflation, and Sharp Capacity Laws*.

## Main results

- The literal full incidence defines exact pre-terminal parent masses
  `P_m`, terminal-support masses `H_m`, and shaped terminal energies `T_m`
  before the free row coefficient is chosen.
- A parent-complete, terminal-atomically faithful pair lift exists exactly
  when the terminal-active rectangle of the literal parent projection equals
  the literal terminal incidence. The projection is then the unique least
  pair relation. If the test fails, no such pair-rectangular lift exists; the
  canonical fallback retains the literal active hypergraph.
- Pair-good blocks and hypergraph blocks form a canonical hybrid repair. Its
  exact repaired parent is `Ptilde_m = P_m + Delta_m`; the literal-active-
  hypergraph baseline has zero parent inflation.
- The optimal full-row parent domination is the largest row inflation. A
  new-only row makes it infinite, and one dyadic block can already produce
  arbitrary polynomial inflation. Thus `O(log X)` labels control bookkeeping,
  not denominator dilution.
- True terminal activation factors into terminal-support alignment, literal
  multiplier intensity, and inverse parent inflation. The paper proves the
  sharp uniform row minimum, distinguished weighted average, and optimal
  inflation-corrected transfer laws.
- Threshold-good rows occupying repaired-parent fraction `delta_eta`, together
  with occupied coefficient capacity `kappa_X`, give the sharp lower bound
  `eta * (1 - (1-delta_eta)/kappa_X)_+`. This certified lower bound is
  positive exactly when `kappa_X > 1-delta_eta`.
- A denominator-compatible chain charges inflation exactly once inside the
  effective terminal loss and retains the strict `< 1/400` endpoint rule.

## Claim boundary

The finite-incidence identities, minimax laws, capacity extremizers, and
compatible-form composition are L0. Their specialization to one literal
fixed nonzero shift and coefficient field is L1 and remains conditional.
The paper does not prove a favorable terminal-incidence lower bound,
favorable `delta_eta` or `kappa_X`, a physical label-erasure lower bound, a
signed fixed-shift cancellation estimate, a parity advance, a prime-pair
lower bound, or a twin-prime result.

## Build

```text
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The archived paper is `true-terminal-activation-parent-inflation.pdf`.
