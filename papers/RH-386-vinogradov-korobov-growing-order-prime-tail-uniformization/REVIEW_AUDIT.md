# RH-386 peer-review audit

## Review question

Does the manuscript prove a genuinely uniform growing-order prime-tail
theorem from the cited explicit prime-number-theorem bound, with correct
endpoint, kernel, partition, and sharpness bookkeeping?

## Major-claim review

1. **Source transfer.** The proof starts from the exact strict Stieltjes
   identity, not from a fitted finite tail. The monotonicity threshold is
   `L>=512`, while the cited source theorem retains its own `x>=23` domain.
2. **Hazard bound.** Both terms of
   `q_r=2rt/(t^2-1)+1/(t log t)` are decreasing. The lower bound
   `J_r>=h_r/q_r` and `xq_r<=3r` produce the stated `7r` relative error.
3. **Middle kernel.** The weighted-average argument gives the stronger
   hypothesis-free `r/(x^2-1)` bound. The coarse `4r/x^2` form is not used
   as the canonical theorem.
4. **Leading kernel.** The change of variables gives
   `I/K=E[(1+aV)^(-1)]` with exponential moments 1 and 2. Jensen's
   direction and the signed first correction are correct.
5. **Growing partitions.** Multiplicity summation yields exactly `d`, `H`,
   and `H2`; no hidden factor depends on partition length or largest part.
6. **Necessity of H.** Since `H2<=H`, the refined remainder is smaller than
   the main `H/L` term by `O(1/L)`. This supports the stated iff criterion.
7. **Sharpness.** For `lambda=1^floor(cL)`, source, power, and second-order
   errors vanish while `H/L->c`, giving `exp(-c)`.

## Adversarial review

The field-level verifier rejects 24 targeted mathematical mutations:
source constants and signs; source domain/hash; inclusive endpoint;
missing boundary or logarithmic factors; hazard/Jensen direction errors;
wrong kernel denominator/rate; replacement of degree by length; wrong `H`
denominator; deletion of `H/L`; degree-only leading sufficiency; and
redistribution reclassification. Seven separate source-type and strict
JSON attacks are also rejected.

## Scope review

The source fallback constants from Corollary 1.2/Table 1 are not promoted
to a theorem. The manuscript does not infer an effective first index, a
growing clock, active `c11` cancellation, an operator or trace formula,
zero identification, or RH. The surrounding phasewise statement remains
fixed finite `q` with `c11=0`.

## Decision

**Accept.** The mathematical argument is self-contained conditional only on
the precisely cited Johnston--Yang estimate. Final replay gives a
warning-clean PDF, fresh schema/result equality, exact 59+1 source replay,
77 passing tests, and archive failure count zero.
