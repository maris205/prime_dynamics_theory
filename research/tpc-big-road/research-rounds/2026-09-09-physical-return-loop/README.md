# Physical-return research loop — 2026-09-09

Unnumbered working research; formal endpoint remains TPC418.
Four bounded review rounds are complete; all nine delegated agents are closed.
This directory is disjoint from the preceding reconnaissance and existing papers.

## What has been established in this round

| Result | Evidence and precise ceiling |
|---|---|
| Literal hybrid, Fourier profile, and source-clock recovery | [Object lock](DERIVATION_PACKAGE.md). In particular \(x=2X\), \(h_0=2\), fixed possibly non-even compact profile, and the full original hybrid; no model substitution. |
| Exact physical matrix decomposition and ordinary norm scale | [Proof](PROOF_PACKAGE.md): \(A=T-R-\Delta\), \(0\le A+\Delta\le T\), \(\|A\|\ll Q^2\), and \(\|A\|\ge(3/2+o(1))Q^2/\log Q\). These are actual-matrix norm statements, not arithmetic mixed-scalar cancellation. |
| Full-row normalization and actual coefficient cost | [Lane proof](LANE_NORM_PROOF.md): \(G(u)\asymp HQ^2/\log Q\) uniformly on the full physical interval, \(\|w\|_2^2\sim (x/2)\log x\), and an explicit semiprime lower bound for \(\|\beta\|_2\). The coefficient-blind norm-product route cannot certify a fixed-power saving. |
| Growing-dimensional norm obstruction on the literal operator | [Complex proof](GROWING_RANK_PROOF.md) and [separate real-witness proof](REAL_GROWING_RANK_ADDENDUM.md), both independently audited. At least \(k_x=Q^2/4-x^{11/32}+O(1)\) negative directions survive before constraints; any correction of rank below \(k_x\), in its expressly stated real or complex convention, leaves norm at least \(Q^2/(2\log Q)\). No arithmetic-lane alignment is proved. |
| Exact Kloosterman emission, with its saturation retained | [Emitter proof](LOCAL_EMITTER_PROOF.md). Full arrays have length \(q-1\), not \(\sqrt q\); a critical-size decomposition needs a paid cost and residual. The positive unsubtracted packet has exact norm saturation. |
| One-sided shortening is insufficient as a generic norm theorem | [Next arithmetic obligation](NEXT_ARITHMETIC_OBLIGATION.md): the full Kloosterman Gram identity gives norm exactly \(q\) even when the first support has only two coordinates and both arrays are centered. Actual arithmetic extremizers are not claimed. |
| Constructive derivative control and paid boundary support | [Partition proof](CONSTRUCTIVE_PARTITION_PROOF.md), independently audited. One explicit V59-admissible partition has uniform scaled derivatives; boundary terms have collective cost \(xQ^2x^{-11/64+o(1)}\). This leaves the interior arithmetic estimate open. |
| Prior finite attachment corrected, original preserved | [Erratum](FINITE_ATTACHMENT_ERRATUM.md): upper-star kernel orientation, the qualified zero-interior caveat, reweighting cost, and the physical CRT cover obstruction. |
| Adaptive-prefix condition and sparse counterexample audited | [Full report](agent-reports/physical-loop-prefix-cover-audit.md). The cover-to-prefix lemma is conditional; its local premise already contains nontrivial cancellation. No Möbius realization is proved. |

The real and complex growing-rank results use different subspaces and rank
conventions. Neither result identifies the arithmetic lanes with its witnesses.
The real quadratic identity also does not replace the mixed scalar by the real
part of its matrix. No success threshold for larger-rank correction is proved.

## The arithmetic task that remains

On island 2, toward image Bridge A / repository Gate B, the unchanged target is
\[
 |\mathfrak C_x|\ll xQ^2x^{-\delta+o(1)},\qquad\delta>1/400,
\]
with literal \(\beta,w\), the fixed shift 2, all unit masks, full prime shell,
outer \(q\), off-diagonal deletion, and signed packet recombination.
A possible two-critical-array route still owes the explicit compression and
residual criterion in the emitter proof, with total loss
\(\ell<19/2400\), so that \(\delta=1/96-\ell>1/400\).
Gate A remains separately open, and terminal division retains
\[
 0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]

Source recovery, exact Fourier identities, normalizing denominators, small
dual radius, and finite numerical agreement do not prove this estimate.
Nor does an obstruction to a coefficient-blind method show that the signed
arithmetic scalar is large, that every method fails, or that TPC is false.

## Verification and provenance

[Current round-4 diagnostics](DIAGNOSTIC_RECEIPT_ROUND4.md), with the preserved
[earlier](DIAGNOSTIC_RECEIPT.md) and [round-3](DIAGNOSTIC_RECEIPT_ROUND3.md)
snapshots, record complete normal and optimized-mode outputs.
The [checker](check_diagnostics.py) is
read-only and does not depend on Python assertions. Gaussian kernel and random
vector tests are expressly diagnostic, not replacements for physical data.

Six original task reports, the growing-rank report, and eight independent
round-review responses are retained
verbatim under [agent-reports](agent-reports/). The cumulative
[review log](../../../../AUTO_REVIEW.md) retains full raw independent reviews,
implemented corrections, and status. Reviewer scores certify only their
declared proof-integration scope, not top-venue novelty or publication readiness.

Important supersessions: early raw reports with \(X=x\) are corrected to the
literal \(x=2X\); an early DLMF definition-only pointer is not a PNT theorem
citation; the authoritative fixed profile is not assumed even; and uniform
cutoff derivatives are not inferred from qualitative smoothness. The current
integrated proof texts make these boundaries explicit.
One immutable raw report contains a source-path typo; its corrected navigation
is recorded in [SOURCE_LINK_ERRATA.md](SOURCE_LINK_ERRATA.md), without changing
the original response.

Primary external inputs, checked in source, are the classical prime number
theorem, the unconditional Mertens product theorem, and BP's stated critical
bilinear theorem. Their direct citations are placed where used in the proof
texts. No independent full-proof certification of an external theorem is claimed.

No new numbered directory, PDF, release, commit, push, model-provider upload,
or alteration of existing scientific expected artifacts was performed.
The pre-existing dirty worktree is preserved.
The [final QA and preservation receipt](FINAL_QA_RECEIPT.md) records the
post-handoff startup regression, old-body hash verification, final scoped
file counts, and the limits of the inherited artifact checkers.
