# Source lock

## Frozen internal object

The exact target is the V59/V60 standard-zero-hole remainder:

```text
prime-only modulus shell
+ outer q weight
+ Schwartz kernel localization
+ exact (q-2)/(q-1) coefficient-diagonal subtraction
+ four literal packets a^(j)=beta+i^j w
+ one signed block and prime-shell reassembly.
```

The frozen internal sources are:

```text
TPC_HANDOFF.md, V59 and V60 current lineage
research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md
research/tpc-big-road/bridge_b_moving_hole_bdh_translation_compiler.md
papers/tpc-207-critical-moving-hole-bdh-defect/
```

TPC-208 changes only the internal representation of the standard-zero-hole
remainder.  It does not alter packets, block order, kernel, prime shell,
diagonal coefficient, or physical outer normalization.

## Primary external sources

1. Adam J. Harper, *Simple Barban--Davenport--Halberstam type asymptotics for
   general sequences*, arXiv:2412.19644v1 (2024).
2. Valentin Blomer and Alexandru Pascadi, *Bilinear forms with Kloosterman
   sums via quadratic characters*, arXiv:2607.24311v1 (2026).
3. Alexandru Pascadi, *Large sieve inequalities for exceptional Maass forms
   and the greatest prime factor of n^2+1*, arXiv:2404.04239v3; published in
   *Forum of Mathematics, Pi* 14 (2026), e8.

Metadata and theorem boundaries were checked against official arXiv records
and theorem text on 2026-08-17.

## Exact boundary of each source

Harper supplies a general-sequence BDH architecture under explicit
Progressions, Non-concentration, and additional hypotheses.  It does not state
the TPC-208 edge decomposition, verify its hypotheses uniformly for the four
literal packets, select prime moduli after signed diagonal subtraction, or
perform the physical collective reassembly.

Blomer--Pascadi Theorem 1.1 accepts an already emitted fixed-modulus bilinear
Kloosterman form and supplies the critical `c^(-1/32+o(1))` local saving.  The
TPC-208 additive edge cell is upstream of that input: no transformation from
the literal coefficients to the source arrays is claimed here.

Pascadi supplies sparse-Fourier and Kloosterman machinery after a valid
emitter and norm ledger exist.  It does not by itself create the TPC-208
emitter, prime-shell selection, packet signs, or block reassembly.

## Bounded novelty statement

A bounded arXiv metadata query for the exact combinations
`reduced residue + graph Laplacian`, `BDH + additive Fourier`, and
`leave-one-out variance + Fourier` returned no direct match on 2026-08-17.
This is not a literature-wide novelty proof.  The complete-graph Laplacian
identity is standard linear algebra.  The paper claims the exact attachment
to the frozen V59 object, edgewise diagonal distribution, physical-kernel
crosswalk, and scoped literal-edge uniqueness theorem.

## Source-locked claim

```text
ZERO_HOLE_EDGE_FRAME=PROVED_EXACT
EDGEWISE_DIAGONAL_DELETION=PROVED_EXACT
LITERAL_EDGE_NO_SPARSIFICATION=PROVED_SCOPED
HARPER_DIRECT_FULL_GATE_B_ATTACHMENT=NO
BLOMER_PASCADI_DIRECT_PRE_EMITTER_ATTACHMENT=NO
COLLECTIVE_KLOOSTERMAN_COMPILER=OPEN
```
