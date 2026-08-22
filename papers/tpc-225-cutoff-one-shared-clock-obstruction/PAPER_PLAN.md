# TPC-225 paper plan

## Research question

Does the TPC-224 source-surrogate clock `x=Q^3`, `H=4Q^2`, `h=4Q` provide a
genuine prime-label AP marginal saving for the literal row family, when the
same packet profiles and normalization are retained?

## One-sentence contribution

In the cutoff-one source clock, the literal prime rows have pairwise disjoint
residue support, so the AP marginal is exactly the diagonal energy and the full
reassembly is exactly the polarized marginal; hence this clock cannot pay any
positive AP saving, although packet-direction cancellation remains profile
dependent.

## Claims and evidence

| Claim | Evidence | Status |
|---|---|---|
| cutoff is exactly one on the source clock | `floor(hq/H)=floor(q/Q)=1` for `Q<q<=2Q` | `PROVED_EXACT` |
| distinct prime rows have disjoint `±q^{-1}` support | modular support lemma | `PROVED_EXACT` |
| AP marginal equals diagonal energy | orthogonality identity `E_AP=E_diag` | `PROVED_STRUCTURAL_L1` |
| full energy equals polarized marginal | q-block orthogonality identity `E_all=E_pol` | `PROVED_STRUCTURAL_L1` |
| positive AP saving on this clock | contradicted whenever `E_diag>0` | `REFUTED_SCOPED` |
| packet-direction saving | depends on profile sums | `PROFILE_DEPENDENT / OPEN_FOR_V46` |
| V46 asymptotic transfer | no source-locked identification supplied | `OPEN` |

## Experimental design

1. Rebuild the literal rows independently over `Fraction` for nine actual-prime
   source-surrogate scales.
2. Audit affine TPC-224 profiles, aligned profiles, and balanced profiles on
   the same clock.
3. Check exact identities, support disjointness, boundary values `Q=3..99`,
   and normal/optimized replay.
4. Keep the source-surrogate clock explicitly separate from the V46 asymptotic
   clock and from TPC-224's collision-stress clock.

## Claim ceiling

This is a proved structural obstruction for a named finite growing clock. It
does not prove that no other clock can produce AP dispersion, and it supplies
no arithmetic `L2`, fixed-atom credit, strict `1/400` payment, or twin-prime
theorem.
