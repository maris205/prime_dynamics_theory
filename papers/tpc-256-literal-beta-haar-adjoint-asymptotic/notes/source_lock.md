# TPC-256 source lock

## Frozen release

```text
baseline HEAD = 4695df00b1c6962bc94e21474e101c698f39f4bd
TPC_HANDOFF.md sha256 = 1da1d8a74c5fd85a2401a389762966aaa0cb0405e2df16465edae09ead47600e
TPC-255 bridge sha256 = cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97
```

The executable checks source blobs with
`git show 4695df00...:<path>`, so later dynamic documentation updates cannot
silently change the theorem inputs.

## Frozen source matrix

| Path | SHA-256 | Locked role |
|---|---|---|
| `TPC_HANDOFF.md` | `1da1d8a74c5fd85a2401a389762966aaa0cb0405e2df16465edae09ead47600e` | TPC-255 release baseline and route state |
| `research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md` | `705b0dfd4d94d70bad798ca6cccf7e0f37f049683d30373ea895d97a6db93da1` | Literal raw beta and proper-factor envelope |
| `research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md` | `b45ef249175c84758f6052a647f54f74c227351d317034766c5988c7c98f7c5e` | Frozen `H,Q,U` scales and exact beta formula |
| `research/tpc-big-road/bridge_b_source_frozen_rank_midpoint_contrast_compiler.md` | `31333053692ca404b6de9a5463cdc803f6b784bbdcc4ca3af36c9ebe16431b16` | Ordered-rank split, Haar normalization, adjoint orientation |
| `research/tpc-big-road/bridge_b_exact_adjoint_diagonal_boundary_compiler.md` | `cd57bf302938946489a509991a50c3945b793371914e1fd7c99c5ace57ca1e97` | Exact `B_Q`/input-unit/hard-window/child-jump identity |
| `research/tpc-big-road/bridge_b_proper_factor_poisson_transference.md` | `fd02eaf5504b7a7c2182a8a045b9ec03488ef72ef7b88e750ba781163c10525a` | Complete centered Poisson zero and `H^2/q` first moment |
| `research/tpc-big-road/bridge_b_top_prime_direct_energy_floor.md` | `093fa3bc9c3512d760462526daac7aa1867ee41eb5b6b0e2bfd0a7ee8d580906` | Weighted-prime shell asymptotic |
| `papers/tpc-233-critical-depth-row-mass-obstruction/notes/source_lock.md` | `a61a7a8f43ef4cbf46a69443b01bd2d4d41cc31a418612ad7a66fd5d54af6446` | de la Vallée Poussin PNT input |

## Exact locked claims

1. The literal coefficient is

   ```text
   beta(t)=Lambda(t)/log(t)-sum_(d|t,d<=x^(133/400))mu(d).
   ```

2. The literal clock is `I_x=(x/2,x] intersect Z`, with
   `H=x^(21/32)` and `Q=x^(1/3)`.
3. The rank midpoint is chosen from the ordered physical coordinates before
   inspecting any coefficient, with `rho^2=ell*r/N`.
4. The first inner-product slot is conjugate-linear.  No kernel reality,
   evenness, or self-adjointness is frozen.
5. TPC-255 proves exactly

   ```text
   <z_mid,A_x beta>
    =-B_Q<z_mid,beta>+R_unit+R_hard+R_jump.
   ```

6. The complete unit-centered row must retain the output mask.  Its two
   algebraic pieces have opposite nonzero period sums and only their sum is
   centered.
7. Smooth compact support of the profile makes `K_H` Schwartz; the frozen
   centered first moment is `O_psi(H^2/q)`.
8. Weighted PNT supplies
   `sum_(Q<q<=2Q)q=(3/2+o(1))Q^2/log Q`.
9. The source-locked classical arithmetic input is

   ```text
   pi(y)=Li(y)+O(y exp(-c sqrt(log y))).
   ```

## Source-backed versus derived here

- `SOURCE_BACKED`: the literal object definitions, the exact TPC-255
  decomposition, the complete-row Poisson attachment, the strong PNT, and
  weighted PNT.
- `PROVED_HERE`: layerwise divisor-density cancellation, second-order `Li`
  curvature, real-clock endpoint control, the combined-mask pointwise bound,
  hard/jump crossing counts, exponent comparison, and phase-safe corollaries.
- `NUMERICAL_OBSERVATION`: finite beta-Haar values at `10^5` and `10^6`.
