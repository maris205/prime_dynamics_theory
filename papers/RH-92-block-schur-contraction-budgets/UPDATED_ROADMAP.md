# Updated roadmap after RH-92

## What changed

RH-91 used a pointwise late Schur law `S1`: every update after burn-in should
contract by one fixed factor such as `0.24`. RH-92 shows that this is not the
right finite target for the current packet window.

Seven of the forty audited updates have a rigorously positive-definite
`0.24` threshold matrix, so the named rank-one compressed corrector cannot
meet the pointwise target there. Nevertheless every four-step rational budget
has product below `0.24^4`.

The preferred operator gate is therefore weakened to a repeated block law:

    S_blk: product(rho_j over each fixed-length late block) <= Q < 1,

with a uniformly bounded within-block prefix product.

## Exact scalar target

At a coercive update, the Schur gate is exactly

    b* M_delta^{-1} b >= delta,

where `M_delta = A-(d-delta)I`. If `M_delta` has a nonpositive direction, the
requested gain is automatic. An all-level proof may therefore estimate an
average secular surplus over a block instead of forcing the same surplus at
every update.

## Revised Stage A frontier

The two sufficient alternatives are now

    L

or

    S_blk AND R AND O.

Here:

- `L` is the inherited full-block law;
- `S_blk` is a repeated uniform block Schur budget;
- `R` is a polylogarithmic reduced packet refresh/future;
- `O` is the finite-prefix, normalization, and observability bridge.

RH-92 validates one block per frozen channel. It does not prove repetition,
derive the rational factors analytically, or close `R` or `O`.

## Important separation

The audit refreshes with a leading ambient packet and verifies that this
refresh is no worse than the rank-one corrected packet. This does not prove
that repeated one-direction corrections alone track the packet. The reduced
refresh remains an independent gate and must not be absorbed into `S_blk`.

## Stage A5 and later stages

The RH-81 moving-cloud projection, coefficient bridge, and uniform
trace-class complement remain unchanged. Canonical scattering completion,
self-adjoint generation, intrinsic `T log T` counting, a prime-power trace
formula, and any completed-zeta identity remain later stages.

There is no Hilbert-Polya operator, zeta-zero identification, or proof of the
Riemann Hypothesis in this roadmap.
