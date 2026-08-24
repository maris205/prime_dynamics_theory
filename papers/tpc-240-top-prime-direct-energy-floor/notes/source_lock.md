# Source Lock

Date: 2026-08-24

Verdict: `GO_SOURCE_LOCK`

## Exact object

The scales are the literal V59 scales
`H=x^(21/32)`, `Q=x^(1/3)`, and `U=x^(133/400)`.  The profile is fixed,
real, smooth, compactly supported in `[-1,1]`, nonnegative, bounded by one,
and normalized to integral one.  The energy is the q-split unsigned top-prime
direct residue-row energy.  It carries no complete-period factor and no
finite-window normalization in its main theorem.

## Repository anchors

- TPC-215, `paper/main.tex`, proposition `exact ratio one in the top shell`:
  top-shell cluster coefficient `C_p=c_p=-log(p)/p`.
- TPC-216, `paper/main.tex`, theorem `fixed-q no-collision`: exact fixed-`q`
  row norm under `4Q<H`.
- TPC-237,
  `research/tpc-big-road/bridge_b_collision_compressed_finite_window_reassembly.md`:
  exact q-split common-source interface and primitive frequency index.
- TPC-238, `paper/sections/2_setup.tex`, theorem `finite-window lower frame`:
  optional normalized lower-frame transfer.

## Locked distinctions

The main object is not the TPC-215 complete-period q-collapsed energy, not a
signed `C_h` scalar, and not the signed four-packet Gate-B object.  The
fixed-`q` identity is inherited rather than claimed as new.  A profile equal
to one throughout `[-1,1]` is excluded because its zero extension is not a
literal smooth compactly supported profile with that plateau.

## Audited theorem ceiling

`EXACT_FIXED_PROFILE_TOP_PRIME_Q_SPLIT_UNSIGNED_DIRECT_ENERGY_ASYMPTOTIC_WITH_CONSTANT`

The source/proof audit independently verified the constant `1197/800`, the
power `1/96`, the relative error `x^(-23/2400)`, and the profilewise quantifier.
