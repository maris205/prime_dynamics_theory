# TPC-307 proof package

## Claim

On the declared finite shell spine, the common-ambient union-shell holdout
protocol is well-defined and separates overlap fitting from exclusive-shell
testing.  Its numerical replay has 13 concordant, 3 discordant, and 2
unresolved budget/holdout classifications.

## Status

```text
PROVED_EXACT_FINITE = protocol definitions and finite algebraic lemmas
NUMERICALLY_REPRODUCED_FINITE = 18-case atlas and its classifications
OPEN = formal directed-rounding certificate, causal identification, uniform
       asymptotics, arithmetic L2, fixed-power credit, full Gate B, twin primes
```

## Assumptions and notation

Fix finite sets `S_L,S_R`, binary label maps `a_L,a_R`, a real matrix `V_U`,
and a positive semidefinite source Gram matrix `M_k`.  Let `O,E_L,E_R,U` and
`sigma` be as in the derivation package.  A directional target is nonzero on
the overlap and has a nonempty exclusive holdout.  All three normalizers are
positive on the finite replay.

## Proof strategy

First prove the set identities and sign invariance directly.  Then observe
that the constrained optimization for a direction is a function only of
`(V_{O,k},b_X,M_k,tau)`, so exclusive rows are not used in coefficient
selection.  Finally use nested feasible prefixes to justify the common prefix.
The numerical census is treated separately: it is an executable replay of
the stated finite optimization, not a deduction from the exact lemmas.

## Dependency map

```text
TPC-302 source-first rows
        -> TPC-305 transported-label parent lock
        -> TPC-306 two-way interaction context
        -> TPC-307 U/O/E partition and directional targets
        -> overlap frontier + exclusive holdout
        -> finite numerical agreement/discordance atlas
```

## Proposition 1: finite partition

For finite `S_L,S_R`, the sets
`O=S_L intersect S_R`, `E_L=S_L\O`, and `E_R=S_R\O` are pairwise disjoint,
and `U=S_L union S_R=O disjoint-union E_L disjoint-union E_R`.

### Proof

If an element lies in both `E_L` and `O`, it is simultaneously outside and
inside `O`, a contradiction; the same argument handles `E_R` and `O`.  If an
element lies in both exclusive sets, it lies in both shells and hence in `O`,
contradicting exclusivity.  Every element of either shell is either in `O` or
in exactly one exclusive difference, proving the union identity.  Finiteness
is inherited from the two finite shells. `\square`

## Proposition 2: global-sign invariance

Replacing one directional overlap target and its matching exclusive holdout
target by their negatives leaves its source budget and squared holdout loss
unchanged.

### Proof

If `c` is feasible for `b`, then `-c` is feasible for `-b`, because both the
residual norm and the quadratic source cost are unchanged.  The feasible
cost sets are therefore identical, so their minima agree.  The prediction
also changes from `Vc` to `-Vc`; simultaneously changing the holdout label
from `h` to `-h` changes the residual to its negative.  Its square, and hence
the holdout loss, is unchanged. `\square`

## Proposition 3: common-prefix feasibility

If the first feasible prefix lengths for the left and right overlap targets
are `k_L` and `k_R`, then `k=max(k_L,k_R)` is feasible for both, provided the
prefix family is nested and coefficients may be padded by zero.

### Proof

Suppose a target is feasible at prefix `j`.  At any longer prefix `k>=j`,
embed its coefficient vector as `(c,0,...,0)`.  The represented overlap
vector and residual are unchanged, so feasibility persists.  Apply this to
each direction at its own first feasible prefix and take the maximum. `\square`

## Proposition 4: holdout separation

For fixed `X`, the coefficient set and budget in the TPC-307 frontier depend
only on `V_{O,k}`, `b_X`, `M_k`, and `tau`; the rows in `E_X` are not consulted
by the optimization.  The holdout loss is evaluated only after a coefficient
vector has been selected.

### Proof

This follows by inspection of the displayed constrained minimization: neither
the objective nor the constraint contains an exclusive row.  The exclusive
rows occur only in the subsequent prediction-and-loss expression. `\square`

## Proposition 5: conditional interval classification

If a valid enclosure `[L,U]` contains a positive budget or holdout ratio and
`U<0.9`, then the ratio is strictly right-lower; if `L>1.1`, it is strictly
left-lower.

### Proof

The inequalities imply the corresponding strict inequality for every value
inside the enclosure.  The three classes are defined by those inequalities
and their complement. `\square`

## Numerical statement

The producer and independent replay agree on the locked finite atlas:
18 cases, 36 directional fits, and 54 normalizer rows.  The agreement census
is 13 concordant, 3 discordant, and 2 unresolved.  All three discordances are
at `Q=70 -> 90`, exponent 1, across the three tolerances.  This statement is
supported as a numerical reproduction by the included scripts.  It is not a
formal proof of the decimal enclosures and does not identify a causal effect.

## Corrections and missing assumptions

- A naive union target formed by mixing left and right labels coordinatewise
  is not used, because the transported vectors can disagree on `O`.
- Zero-padding a shell-specific operator into `U` would create an avoidable
  support penalty and is not the common-ambient object here.
- The labels are inherited source/physical-Gram-dependent labels from
  TPC-302, so target-generation leakage remains explicit.
- The finite numerical replay uses floating-point construction and broad
  padding; a formal interval proof would require directed rounding or exact
  rational bounds for the entire physical matrix and frontier solve.
- No finite atlas by itself supplies a growing-`Q` or growing-`N` theorem.

## Open risks

The three discordances may be artifacts of the native exclusive completion,
profile-prefix choice, or true finite extrapolation instability.  TPC-308 is
therefore assigned to adversarial completion envelopes and prefix perturbation
tests.  Until those tests and an identification theorem are available, the
Route-B arithmetic and twin-prime gates remain open.
