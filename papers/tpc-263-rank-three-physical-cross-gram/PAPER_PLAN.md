# TPC-263 paper plan

## One-sentence contribution

The source-backed rank-three Haar frame pays a new, explicitly typed
physical cross-Gram channel: the entire `span(z0,z1,z2)` contribution to the
literal V59 coupling is `O(x^(5/3)/(log x)^(M+3))` for every fixed `M`, while
the orthogonal residual remains the only unscreened channel.

## Research question

After TPC-262 identified the correct signed growing-shell observable, can the
three source-only Haar directions already controlled by TPC-257 be coupled to
the source-backed hybrid `w` moments of TPC-254 without confusing a lower
floor with an upper bound?

## Frozen inputs

- The literal V59 interval, kernel, unit masks, deleted diagonal, and prime
  weights from TPC-257.
- The source-only four-block orthonormal frame `z0,z1,z2`.
- TPC-254's maximal-interval estimate for every fixed logarithmic strength,
  applied to the four consecutive blocks.
- TPC-257's three source-backed adjoint asymptotics
  `<zi,A_x beta>=-(9/2 kappa_i+o(1))x^(7/6)/log^3(x)`.

## Claims and evidence

| ID | Claim | Evidence | Label |
|---|---|---|---|
| C1 | `z0,z1,z2` form an exact orthonormal source-only frame. | Rational block-length replay over integer and noninteger clocks. | `PROVED_EXACT` |
| C2 | Every frame moment of the literal hybrid `w` is `O(x^(1/2)(log x)^(-M))` for fixed `M`. | Four block sums extracted from TPC-254's nonnegative `m=1` row. | `PROVED_SOURCE_BACKED` |
| C3 | The adjoint frame coefficients have the TPC-257 `x^(7/6)/log^3(x)` asymptotics. | Frozen source theorem and curvature constants. | `PROVED_SOURCE_BACKED` |
| C4 | The rank-three physical channel is `O(x^(5/3)/(log x)^(M+3))`. | Orthogonal projection identity plus Cauchy/finite summation. | `PROVED_SOURCE_BACKED` |
| C5 | The whole coupling has the same bound. | Not asserted; the orthogonal complement is explicit and open. | `OPEN` |

## Experiments

1. Exact rank/block frame and variation checks on a mixed integer/noninteger
   clock grid.
2. Exact Gaussian-rational projection decomposition with a nonzero residual,
   verifying that the residual cannot be silently dropped.
3. Symbolic exponent and logarithmic ledger, including the `1/400` firewall.
4. Independent replay and mutation rejection without importing the producer.

Finite checks validate identities and source-contract typing.  They do not
replace the asymptotic PNT or maximal Type-I inputs.

## Non-claims

This paper proves no fixed-power saving, no arithmetic `L2` upper estimate,
no estimate for the orthogonal residual, no full Gate B payment, and no
twin-prime conclusion.  The result is a new logarithmic channel, not a
global endpoint payment.
