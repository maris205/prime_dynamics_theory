# TPC-57: Singleton energy and factor-exchange collisions

This directory contains the source and final PDF for:

> *Singleton Energy and Factor-Exchange Collisions in Fixed-Shift Prime
> Fibers: Exact Undeleted Floors, Orbit Sparsity, and the Occupancy Barrier*

## Core result

TPC-56 extracted a constant-energy phase sector only after an adaptive
post-terminal deletion.  TPC-57 instead studies the complete undeleted
fixed-`h0` output.  For any finite fiber system, if `D` is diagonal energy,
`G` is the grouped energy, `D1` is the energy in active singleton fibers,
and

```text
I1 = sum_u |x_u|^2 (n_{q(u)} - 1),
```

then

```text
G >= D1 >= max(D - I1, 0).
```

Higher rooted collision moments give an exact finite inclusion-exclusion
formula for `D1` and alternating Bonferroni bounds.  The first-moment
inequality is sharp using only `(D,I1)`.

For literal terminal amplitudes `x_u = c_u zeta_{m(u)}`, the best singleton
constant uniform over the bounded row-coefficient class is exactly

```text
beta_X = min_m W_{m,1}/W_m.
```

This converts the undeleted problem into a rowwise weighted occupancy gate.
A cofactor core can be tested against the full output without an invalid
grouped-norm monotonicity step, because every partner of a root with
`r in [R,2R]` lies in the enlarged block `r' in [R/2,4R]`.

Every literal collision has the unique factor-exchange form

```text
d1 = a b,   d2 = a c,   r1 = c e,   r2 = b e,
```

with pairwise-coprime squarefree factors, and obeys

```text
e/gcd(e,h0) divides b*l1 - c*l2.
```

Same-divisor collisions require `r <= rad(|h0|) L`.  Cross-divisor
collisions in a balanced block require large exchanged factors.  In
particular, `R > 48 rad(|h0|) L D^2` makes every core atom a singleton in
its full output fiber.  The inherited large-prime carrier has
`r < X^(1/2+o(1))`, whereas this threshold is
`X^(0.8589...+o(1))`; hence the structural range is empty for the current
physical packet.

## Exact remaining gate

At the inherited scale, the missing statement is a coefficient-weighted
one-atom versus two-atom factor-exchange incidence estimate.  A maximal-degree
bound alone cannot supply it: even a carrier made entirely of doubletons
can have zero singleton energy.  The paper records the exact weighted
incidence target and the separate losses for packet selection, block
occupancy, terminal activation, singleton occupancy, native-Gram
comparison, boundary control, and tail reconnection.

## Claim boundary

The collision identities and extremal laws are unconditional L0 results.
Their specialization to the declared fixed-`h0` terminal carrier, partner
localization, factor exchange, and orbit ladders are exact L1 interface
results.  No positive singleton proportion or terminal-activation theorem
is proved at the inherited endpoint.  No native affine-Gram comparison,
parity improvement, or twin-prime consequence is claimed.

## Build

Run `pdflatex`, `bibtex`, and two further `pdflatex` passes in this
directory.  The archived PDF is
`singleton-factor-exchange-fixed-shift-prime-fibers.pdf`.
