# Paper Plan

**Title:** Coherence-Controlled Gram Quadratic Bounds and Sharpness
**Author:** Liang Wang
**Date:** August 25, 2026
**Type:** self-contained finite Hilbert-space theory note
**One-sentence contribution:** The exact shared-lane Gram quadratic is trapped
between sharp coherence-controlled weighted-\(\ell^1\) envelopes, with a
necessary zero floor and exact transfer to the TPC-249 support radii.

## Claims--evidence matrix

| Claim | Evidence | Status | Location |
|---|---|---|---|
| Absolute Gram deviation is at most `mu(L^2-D)` | Exact expansion and termwise coherence estimate | Proved | Theorem 1 |
| The normalized bound uses `kappa=L^2/D`, with `1<=kappa<=|A|` | Cauchy--Schwarz on the active weights | Proved for `D>0` | Corollary 2 |
| `mu(kappa-1)<1` prevents cancellation | Strictly positive lower envelope | Proved | Corollary 2 |
| TPC-249 independent/global radii inherit the bounds | Monotonicity of square root and exact TPC-249 identities | Proved structural transfer | Corollary 3 |
| Upper and signed-lower coefficients are sharp | PSD equicorrelation and two-vector negative-correlation Grams | Exact rational certificate | Section 5 |
| The zero floor is necessary | Regular simplex and rank-one rational collinear cancellation | Exact rational certificate | Section 5 |
| Marginals alone cannot improve `L^2` or force positivity | Aligned/anti-aligned unit-vector pair with identical weights and norms | Exact rational certificate | Section 5 |
| Actual V59 coherence or Gram asymptotics | No source estimate supplied | Open | Limitations/firewall |

## Structure

1. Abstract: theorem, sharpness, radius inheritance, and open arithmetic gate.
2. Introduction and source lock: import only `g_c` and its Gram identity from TPC-249.
3. Definitions and edge cases: active set, total `mu`, and conditional `kappa`.
4. Main theorem and proof: exact quadratic expansion and coherence envelope.
5. Radius transfer: independent and global TPC-249 budgets.
6. Sharpness and marginal obstruction: PSD constructions with no tuplewise overclaim.
7. Exact finite verification: producer, independent checker, mutation rejection, stress.
8. Limitations and conclusion: all arithmetic gates remain open.

## Figure and table plan

No plot or architecture figure is needed.  The contribution is an exact scalar
inequality whose full proof and saturating matrices fit in displayed equations.
The figure-generation phase therefore terminates with `NO_FIGURE_REQUIRED`.
The sharpness constructions are presented as explicit Gram matrices, avoiding
decorative or non-reproducible graphics.

## Citation plan

The only imported result is TPC-249's project-local exact shared-lane identity.
Its title, author, year, formula, and repository location were verified against
the locked TPC-249 source.  No external historical or priority claim is made.

## Review plan

Round 1 audits conjugation, active-set definitions, `D=0`, PSD of every fixture,
and the distinction between signed lower bound and nonnegative floor.  Round 2
audits claim strength, radius transfer, mutation resistance, and the arithmetic
firewall.  Compilation and PDF diagnostics follow both rounds.
