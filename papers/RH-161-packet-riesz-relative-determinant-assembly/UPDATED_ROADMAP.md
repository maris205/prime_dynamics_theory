# Roadmap after RH-161

RH-161 replaces the phrase "typed assembly" by the explicit graph

```text
S_native ----\
              OR -> R -> Q -> U -> Z -> T -> enhanced Gate-A datum
S_lagged ----/
```

The enhanced datum contains both the canonical meromorphic relative
determinant and a fixed separating vector of directed marked traces. The
determinant type is part of the data: `p=1` is the two-step Fredholm branch,
and `p=2` is the one-step regularized branch used by RH-MVP1.

## Immediate next target: physical interface R

For the actual finite/noisy family:

1. choose the proposed moving-cloud contour `Gamma_j`;
2. prove that the packet block and complement are separated on that contour;
3. bound the block resolvent `M_j`;
4. bound the off-packet coupling `epsilon_j`;
5. test `M_j epsilon_j < 1` and the stronger graph margin `delta_j < 1`;
6. transport the resulting Riesz cloud to a common coordinate system.

If `M_j epsilon_j >= 1` persists, the current Neumann corridor is rejected,
but another Riesz construction could still exist. If the spectral homotopy
works while `delta_j >= 1`, rank is certified but the present quantitative
packet graph remains too weak.

## Next wall after R: interface U

Prove or refute a uniform common-space Schatten-norm limit for the Riesz
complement: `S_1` for the two-step branch or `S_2` for the one-step branch.
This is the fixed-disk normal-family gate. A packet support floor cannot
replace it.

## Parallel interfaces

- `Q`: identify the finite cloud coefficients and complete deterministic pole
  divisor without target zero data.
- `Z`: prove mesh, schedule, packet-gauge, reset, and cutoff independence and
  fix the zero-free normalization.
- `T`: transport a fixed separating list of three/six-step marked traces.
- `S`: prove or refute RH-160's eventual native O/E/S route; invoke bounded
  lag L only when `T` needs directional fourth-cross information.

Only after every interface in one completion bundle closes may macro Gate `A`
be promoted. Gate `B` remains the subsequent scattering problem.
