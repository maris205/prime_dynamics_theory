# TPC-289 paper plan

## Question

Does the physical energy surplus observed in TPC-288 come from a stable
source-native cross-prime coherence pattern, or can the pairwise signs and
coherence collapse along the same finite route?

## Claim-driven contributions

1. Define the normalized cross-prime Gram coherence
   `Gamma_(q,r)=G_(q,r)^2/(G_(q,q)G_(r,r))` and the signed off-diagonal energy
   surplus.
2. Prove exactly the Cauchy coherence bound and a conditional accumulation
   inequality converting a positive coherence floor and diagonal balance into
   an aggregate energy lower bound.
3. Recompute 18 finite rows: eight common-scale `s=2` growth anchors, four
   exponent-crossover rows, and six late-shell source controls.
4. Certify a finite phase diagram: 17/18 rows have pairwise-positive Gram
   cross terms, while one early `s=1` row has three negative pairs and a
   near-zero coherence pair; all 18 rows nevertheless have aggregate energy
   ratio greater than one.
5. Isolate an eight-row late-shell block satisfying the exact finite tests
   `Gamma>=9/25` and `d_min/d_max>=4/5`, hence the conditional lower envelope
   `R_E>=1+(3/5)(4/5)(k-1)`.

## Evidence map

| Claim | Evidence |
|---|---|
| Exact coherence identities | `DERIVATION_PACKAGE.md`, `PROOF_PACKAGE.md` |
| Finite phase diagram | producer and canonical JSON certificate |
| Independent arithmetic | `experiments/tpc289_independent_checker.py` |
| Hostile mutation rejection | `experiments/tpc289_coherence_stress.py` |
| Route ceiling | `notes/claim_firewall.md`, `notes/route_evaluation.md`, bridge checker |

## Non-claims

The rows are finite and use the frozen literal operator and source.  The
late-shell block is not a growing-shell theorem, a uniform source theorem, an
arithmetic `L2` estimate, a fixed-power saving, a Gate-B proof, or a twin-prime
theorem.  The finite negative pairs refute only the tested uniform rule, not
every possible restricted or weighted Gram estimate.

## Next-paper trigger

`TEST_ADAPTIVE_SHELL_WEIGHTING_OR_SOURCE_RESTRICTED_COHERENCE_BEYOND_FINITE_BLOCK`
