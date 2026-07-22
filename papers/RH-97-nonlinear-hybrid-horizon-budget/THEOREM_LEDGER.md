# RH-97 theorem ledger

## Proved

1. **Nonlinear hybrid telescoping identity.** The endpoint difference between
   an adaptive composition and a full composition is the sum of exact hybrid
   endpoint increments, with no linearity or differentiability assumption.
2. **Absolute propagated horizon budget.** The endpoint difference is bounded
   by the sum of absolute hybrid increments.
3. **Sparse-decision reduction.** When adaptive and full maps coincide except
   at selected omission times, only those hybrid endpoints need evaluation.

## Validated

- Ten of ten primary hybrid decompositions telescope and match endpoints.
- Five primary propagated contributions.
- Worst primary absolute budget/reference tail: 1.00343e-5.
- Worst primary signed endpoint shift/reference tail: 7.05713e-7.
- Aggressive-cutoff worst budgets: 0.0249207 and 0.0140915.
- Signed contribution reversals occur in each threshold family.

## Not proved

- An a priori Ritz-refresh Lipschitz constant.
- A replay-free block propagation envelope.
- Uniform repeated-horizon control, Stage-A closure, Hilbert--Polya, or RH.
