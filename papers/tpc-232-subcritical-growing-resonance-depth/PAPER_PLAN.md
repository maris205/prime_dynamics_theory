# TPC-232 paper plan

## Research question

How quickly must the dilation depth \(L=L(Q)\) grow before the primitive
shared-clock resonance family can even support a fixed proportion of prime rows?

## One-sentence contribution

For the exact TPC-226 dilated-clock family, the total growing-depth collision
incidence satisfies

\[
C_L(Q)\ll_A \frac{LQ\log\log(3LQ)}{(\log Q)^2}
\quad (L\le(\log Q)^A),
\]

so every subcritical depth \(L=o(\log Q/\log\log Q)\) still has zero normalized
support density and cannot pay any fixed comparable-row saving.

## Claims-evidence matrix

| Claim | Evidence | Status |
|---|---|---|
| Every collision at \(L<Q/4\) has one-wrap form \(ar+bp=4LQ\) | Exact support congruence and short-multiplier proof | `PROVED_EXACT` |
| Every collision channel has two sign-symmetric coordinates and bucket multiplicity at most two | Sign and no-same-sign lemmas | `PROVED_EXACT` |
| Uniform channel count is \(O_A(LQ\log\log(3LQ)/\log^2Q)\) | Explicit Selberg remainder and coefficient-weight summation | `PROVED_SOURCE_BACKED` |
| Subcritical depth has zero row density | PNT normalization | `PROVED_ASYMPTOTIC` |
| Fixed saving fails for comparable row masses | TPC-230 unmatched-mass floor | `PROVED_IN_DECLARED_MODEL` |
| The actual V59 source realizes the dilated clock | No identification theorem | `OPEN` |

## Experiment plan

1. Compile supports directly on 19 \((Q,L)\) scales.
2. Independently enumerate solutions of \(ar+bp=4LQ\).
3. Require exact equality of channel and edge counts in normal and optimized modes.
4. Attack primitive support, unsafe depths, exact types, and the coefficient-weight bound.
5. Treat all finite records as reproduction only.

## Claim ceiling

`PROVED_ARITHMETIC_OBSTRUCTION_L1`.  No lower bound for resonance occurrence,
no source attachment, no signed cancellation, no \(L^2\), and no Gate-B payment.
