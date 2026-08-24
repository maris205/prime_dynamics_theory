# Source Lock

## Repository identity

```text
observed_HEAD = 9603bffddb97f10dad81b2afbcbb1b0a2ddaff8a
declared_baseline_HEAD = 9603bffddb97f10dad81b2afbcbb1b0a2ddaff8a
observed_TPC_HANDOFF_sha256 = dee2986cbb0cb1cf698fa8a5edc557f9991fb8a03494617d19cfb80688ac4ef0
declared_TPC_HANDOFF_sha256 = dee2986cbb0cb1cf698fa8a5edc557f9991fb8a03494617d19cfb80688ac4ef0
target_at_baseline = ABSENT
target_before_write = ABSENT
```

## Frozen interfaces

| File | SHA-256 | Interface used |
|---|---|---|
| `papers/tpc-237-collision-compressed-finite-window-reassembly/DERIVATION_PACKAGE.md` | `6a506ada581e424900c5587c157e851324b525a2426189d91af0b8796bd8f961` | Exact common-source kernel, direct energy, finite-window large-sieve composition, exponent ledger |
| `papers/tpc-237-collision-compressed-finite-window-reassembly/PROOF_PACKAGE.md` | `9464a698148f57c7b0ed57ad1f45760585d68b6b8d56969de2347833b6aee425` | Theorems T1--T3 and claim boundary |
| `papers/tpc-236-physical-multiwrap-collision-envelope/DERIVATION_PACKAGE.md` | `143c3620725350ad2658c022e0d32b5d0baefbebd2f3d41feaf8c7b2839152ec` | Physical support, `R_h(a)`, and internal row injectivity |
| `papers/tpc-236-physical-multiwrap-collision-envelope/PROOF_PACKAGE.md` | `71f1b7a7f8d75dafed54ec5d59f4586483ddfaaa6001e5c2d21d0d22a9123c57` | Exact injectivity proof and row incidence definition |
| `papers/tpc-61-cofactor-exposure-parity-kernel/sections/cofactor-ladder.tex` | `ea33868e7360e21d02da6d3dc587c29f8438945c57bb681eec85bf15fdaa8332` | Lines 118--167: reduced-class interval Brun--Titchmarsh row template |
| `papers/tpc-61-cofactor-exposure-parity-kernel/references.bib` | `8c4352a5bf0154e7ebb30099e3e5d99b3d2c5fcdedfb7ed713a1ef2a6326e9a3` | Lines 65--71: `MontgomeryVaughan2007` metadata |

No frozen source file was modified. TPC-239 replaces only the primitive-row
upper bound at the TPC-237 pre-large-sieve interface.

## Exact inherited objects

The source object remains

```text
K_j(n)
 = sum_(h<=U) sum_((a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h).
```

The `q` weight is one. There is no packet transform, row normalization,
replacement of `C_h`, or change from primitive frequencies.
