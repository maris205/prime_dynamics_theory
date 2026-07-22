# Updated roadmap after RH-97

## What is now exact

Local quotient losses need not be propagated by a guessed linear recurrence.
Hybrid chains give an exact nonlinear Duhamel decomposition of the endpoint
shift. The primary five omissions consume only about `1e-5` of the reference
tail in the worst channel, while the failed cutoffs consume 1.4--2.5%.

## Remaining weakness

Hybrid replay is a posteriori. For every possible omission, it reruns the
future full-width chain. A uniform theory needs a reusable envelope.

## Preferred RH-98 gate: block propagation envelope

Group future full refreshes into blocks and seek constants `Gamma_{j,b}` such
that

    |endpoint contribution from injection j|
      <= Gamma_{j,b} * local injection,

with `Gamma` computable from small compressed data or a finite portfolio of
probe packets. The RH-97 audit suggests `Gamma <= 1` on all tested omissions,
but this is not yet a theorem.

Useful outcomes for RH-98 are either:

- a certified replay-free envelope; or
- a counterexample showing that unit propagation is not structurally valid,
  followed by the weakest corrected condition.

After that, repeated blocks or a stopped exit clock become the next target.
No Hilbert--Polya operator, zero identification, or RH proof is claimed.
