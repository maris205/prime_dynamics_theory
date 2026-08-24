# Paper Plan

## Paper identity

- **Number:** TPC-238
- **Title:** A Finite-Window Lower Frame Obstruction for Primitive Rational Frequencies
- **Author:** Liang Wang
- **Affiliation:** Huazhong University of Science and Technology, Wuhan 430074, P.R. China
- **Date:** Aug 24 2026
- **Research class:** structural obstruction paper

## Research question

After all prime variables inside a \(q\)-bucket have been collapsed into a
single coefficient at each primitive rational frequency, can destructive
interference between distinct reduced frequencies provide a fixed-power saving
on a finite interval?

## One-sentence answer

No at the V59 scale: a translated triangular minorant and primitive Farey
spacing give a normalized lower frame of \(1/2-o(1)\), uniformly for every
collapsed coefficient vector.

## Claims-evidence matrix

| ID | Claim | Status | Evidence |
|---|---|---|---|
| C1 | A translated triangular weight of order \(L\) is supported in every \(N\)-point interval and has Fejér transform with diagonal \(L\). | PROVED | DERIVATION_PACKAGE.md, Lemma 1 in PROOF_PACKAGE.md |
| C2 | Distinct primitive fractions of height at most \(U\) are circularly \(U^{-2}\)-separated. | PROVED | Lemma 2 |
| C3 | \(F_L(\theta)\leq(4L\|\theta\|^2)^{-1}\) off the diagonal. | PROVED | Lemma 3 |
| C4 | A circular \(\delta\)-packing has inverse-square row sum at most \(\pi^2/(3\delta^2)\). | PROVED | Lemma 4 |
| C5 | \(E_I(z)\geq[L-\pi^2U^4/(12L)]_+\|z\|_2^2\). | PROVED | Theorem 1 |
| C6 | The normalized lower frame is at least \([1/2-\pi^2U^4/(6N^2)]_+\). | PROVED | Corollary 1 |
| C7 | The V59 frame defect is \(x^{-67/100+o(1)}\). | PROVED | exponent ledger |
| C8 | Cross-reduced-frequency cancellation cannot create fixed-power saving relative to collapsed coefficient energy at V59. | PROVED_STRUCTURAL_OBSTRUCTION_L1 | Corollary 2, claim firewall |
| C9 | Finite fixtures satisfy the exact ledger and numerical Gram inequalities. | NUMERICALLY_CERTIFIED | producer, independent checker, stress experiment |

## Section plan

1. **Introduction.** State the post-collapse question and the obstruction.
2. **Finite-window setup.** Define primitive frequencies, energy, and the V59 regime.
3. **Lower-frame theorem.** State the theorem and normalized corollary.
4. **Proof.** Triangular window, spacing, Fejér decay, packing, and spectral bound.
5. **Route consequence and firewall.** State exactly what has been ruled out and what remains open.
6. **Finite audit.** Describe deterministic certificate, independent checker, and shifted-window stress.
7. **Conclusion.** Extract the reusable mechanism and next theorem.

## Proof dependency map

    translated triangular window
                 |
                 v
          Fejer Gram matrix
            /           \
           v             v
    Farey spacing   off-diagonal decay
           \             /
            v           v
          circular packing
                 |
                 v
       Schur / Gershgorin lower bound
                 |
                 v
     normalized V59 obstruction

## Computational evidence plan

- Use \(U=4\), \(N=41\), \(L=21\).
- Include all six primitive fractions with denominator at most \(4\).
- Verify exact spacing and triangular-window identities using rational arithmetic.
- Test multiple translated intervals.
- Compute unweighted and triangular Gram eigenvalues numerically.
- Mutate a primitive fraction into a nonprimitive representation and duplicate
  a frequency; both mutations must be rejected.
- Keep exact theorem facts separate from floating-point observations in JSON.

## Claim firewall

The paper will not claim:

- sharpness of \(\pi^2/12\) or of the normalized \(1/2\);
- arithmetic cancellation in \(C_h\);
- a signed four-packet estimate;
- any Route-A gate;
- full Route B;
- payment of the global strict \(1/400\) saving.

## Acceptance criteria

- Complete proof with all constants and interval-parity cases explicit.
- Producer and independent checker share no imports.
- Normal and optimized outputs are byte-identical.
- Standard error is empty on all validation runs.
- Final PDF has no undefined references or citations and has embedded fonts.
- Every rendered page passes visual inspection.
