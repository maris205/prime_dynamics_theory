# Updated roadmap after RH-91

## Current position

The preferred Stage-A effective-rank route has been reduced from a physical
endpoint factorization to a small late-memory packet condition. The new core
operator wall is an all-level version of the RH-90 Schur trial sign:

    Phi_(C-rho E)(x) <= 0

after a controlled burn-in, at clock rank `O(log(1/sigma))`, for both
directional channels and every sufficiently fine dyadic level.

If this holds for enough consecutive updates, RH-91 gives exponential memory
tail decay automatically.

## Stage A

The finite assembly/deflation/Hardy chain remains closed at the archived
anchors. There are two all-level completion alternatives.

### Corridor L: full-block law

Prove the RH-75 log-square full-block estimate with polylogarithmic Hardy
energy. This route is unchanged.

### Corridor E: Schur packet bundle

Three analytic components remain:

1. **Uniform Schur update law.** Construct the cross-block trial at every late
   update and prove a fixed contraction factor `rho<1`.
2. **Reduced packet future.** Bound the rank-`O(log(1/sigma))` packet future by
   a polylogarithm, as required by RH-78.
3. **Prefix/observability bridge.** Prove the inherited finite-prefix,
   normalization, and observability quantities are polylogarithmic uniformly.

The first component is the new operator-theoretic wall isolated by RH-82--90.
The other two are inherited composition/scaling walls and must not be hidden
inside the word “effective rank.”

## Stage A5

After either Stage-A corridor closes, the relative fixed-disk determinant
still requires all three RH-81 gates:

1. an actual moving-cloud Riesz projection;
2. the corresponding coefficient bridge;
3. a uniform trace-class complementary limit.

RH-82--91 do not close or weaken these three A5 gates.

## Negative route markers

Do not reuse the following as presumed shortcuts:

- direct coordinate identity between endpoint and physical packets;
- unweighted prefix Gramians;
- principal-angle/Davis--Kahan continuity at the tail boundary;
- global operator-norm contraction;
- uniform one-step point-packet contraction.

Each failure is branch-specific. None is a no-go theorem for the Schur packet
route or the broader program.

## Later spectral stages

Canonical scattering completion, self-adjoint generator, intrinsic
`T log T` counting, a prime-power trace formula, and any completed-zeta
identity remain later stages. They should be reopened only after Stage A and
the moving-cloud A5 bridge are genuinely controlled.

There is no Hilbert--Polya operator, zeta-zero identification, or proof of the
Riemann Hypothesis in this roadmap.
