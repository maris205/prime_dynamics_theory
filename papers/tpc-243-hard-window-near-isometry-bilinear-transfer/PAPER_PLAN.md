# Paper Plan

## One-sentence contribution

The hard rectangular synthesis map on any finite separated frequency set is a
two-sided near-isometry with an explicit harmonic packing error, and the same
operator estimate transfers the signed TPC-242 selected bilinear mode with its
orientation intact.

## Claim--evidence matrix

| Claim | Status | Evidence |
|---|---|---|
| Every hard-window Gram row has off-diagonal absolute mass at most `R_delta` | `PROVED` | Geometric sum, two-sided circular packing, and antipodal tie rule |
| The normalized synthesis map is a two-sided near-isometry | `PROVED` | Hermitian Schur/Gershgorin applied to `G-NI` |
| Signed bilinear forms transfer with error `epsilon ||z|| ||w||` | `PROVED` | Operator norm and polarization-free duality |
| Primitive height `U` permits `delta=U^(-2)` | `PROVED` | Reduced rational spacing |
| V59 has coefficient `133/100` and exponent `-67/200` | `PROVED` | Exact exponent and harmonic-number ledger |
| TPC-242 selects `N^(-1)<Tw,Tz>` and targets `<w,z>` | `PROVED_STRUCTURAL_L1` | TPC-242 source lock plus the bilinear theorem with reversed argument order |
| The literal V59 top-prime lanes satisfy the required coefficient bound | `OPEN` | No physical attachment or coefficient norm theorem is available |

## Paper structure

1. State the hard-window problem and the exact theorem.
2. Lock notation, source identity, and the conjugate-linear-first convention.
3. Prove the geometric-sum and circular harmonic-packing lemmas.
4. Deduce the frame and signed bilinear estimates.
5. Specialize to primitive rationals and derive the exact V59 coefficient.
6. Transport the TPC-242 selected mode with the correct orientation.
7. Report exact finite checks and their non-evidentiary status.
8. Extract the route advance and preserve all arithmetic gates.

## Repo-relative comparison

- TPC-217 already proves the standard upper large-sieve scale and the
  `x^(-67/200)` spacing ratio. This paper does not relabel that upper estimate
  as new.
- TPC-238 proves a hard-window lower estimate through a triangular minorant,
  with normalized baseline `1/2-O(U^4/N^2)`.
- TPC-243 works directly with the rectangular Gram matrix, yielding a
  two-sided baseline `1-O(U^2 log U/N)` and a signed bilinear corollary.
- TPC-242 identifies the abstract phase-selected mode. TPC-243 supplies its
  finite-window transport but not its physical arithmetic attachment.

## Executable evidence plan

The exact fixture uses frequencies `{0,1/4,1/2,3/4}`, `delta=1/4`,
`K=2`, `H_K=3/2`, `R_delta=6`, and the interval `M=-3`, `N=17`.
Fourth roots of unity make every theorem-facing computation exact over
Gaussian rationals. An orientation-sensitive pair `z,w` checks both
`<Tz,Tw>` versus `<z,w>` and the TPC-242 order
`<Tw,Tz>` versus `<w,z>`.

## Claim ceiling

`PROVED_STRUCTURAL_L1_HARD_WINDOW_NEAR_ISOMETRY_BILINEAR_TRANSFER`.

The paper must not claim arithmetic cancellation, a signed `C_h` theorem,
physical attachment, arithmetic `L2`, fixed-atom credit, strict `1/400`, full
Gate B, or a twin-prime result.
