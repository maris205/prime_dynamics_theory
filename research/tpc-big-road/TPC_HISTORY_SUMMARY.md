# TPC historical route summary and new-session entry

Updated 2026-09-07 from the current repository, [TPC_HANDOFF.md](../../TPC_HANDOFF.md),
[TPC_ROUTE_MAP.md](TPC_ROUTE_MAP.md), and the complete candidate ledger
[PAPER_CANDIDATE_LEDGER.md](PAPER_CANDIDATE_LEDGER.md). This is an archival
navigation layer; it does not create a theorem or replace a paper's proof
package.

## New-session reading order

1. [AGENTS.md](../../AGENTS.md): durable repository and TPC operating policy.
2. [TPC_HANDOFF.md](../../TPC_HANDOFF.md): current theorem boundary, claim
   firewall, startup checks, and reopen conditions.
3. [TPC_ROUTE_MAP.md](TPC_ROUTE_MAP.md): chronological route edges and
   historical stops.
4. [PAPER_CANDIDATE_LEDGER.md](PAPER_CANDIDATE_LEDGER.md): paper-by-paper
   summaries and provenance notes.
5. [PAPER_MATERIALS_INDEX.md](PAPER_MATERIALS_INDEX.md): material inventory and
   Markdown coverage status.
6. The active paper directory's `README.md`, `PROOF_PACKAGE.md`, certificate,
   independent checker, and Bridge-B record, in that order.
7. [REFERENCE_PRIMEGAPS186.md](REFERENCE_PRIMEGAPS186.md): external reference
   review and conditional-formalization crosswalk.

## 2026-09-07 conversion batch

The contiguous range TPC-418–320 has 99 mechanical full-source Markdown
reading layers at `paper/main.md`. This pass repaired the previous 64
conversions and added TPC350–354, then converted TPC320–349. The batch record
[TPC_CONVERSION_BATCH_2026-09-07.md](TPC_CONVERSION_BATCH_2026-09-07.md) links
each Markdown file, conversion record, README summary, available proof/application
notes, TeX original, and PDF original. Each record includes source and PDF
hashes, actual heading-based page mapping, displayed-equation catalogues,
formula-sequence and normalized text roundtrip checks, and explicit review
limits. TPC350–358 have references/BibTeX, correcting the older blanket
no-bibliography claim. No abstract/reference heuristic substitutes for
independent semantic review, so `reliable-full-md` remains zero.

The [repair audit](TPC_MAINTENANCE_REPAIR_2026-09-07.md) documents the fixed
text-trimming defect, TPC350–354 prerequisite checks, missing separate proof
packages in TPC359–363, the unresolved TPC352 printed-operator/producer
mismatch, TPC353–354 notation issues, and the ambiguous TPC402 page match.
Original scientific files are preserved; no certificate rerun is claimed.

The [TPC345–349 prerequisite audit](TPC_CONVERSION_SCOPE_TPC345_349.md)
adds the exact scope of the five subsequent conversions, including
nonzero-denominator/hit-set conditions, the integer-cutoff qualification for
TPC347, and the limited multiple-divisibility coverage of TPC349's anchor.
The automatic TPC346 appendix map is supplemented by a direct page-4
extraction; TPC347's ambiguous heading match remains explicit.

The [TPC340–344 prerequisite audit](TPC_CONVERSION_SCOPE_TPC340_344.md)
checks the Schur/Frobenius and projection/model identities with their exact
symmetry, nonzero-denominator, and common-weighting requirements. Source
notation, interval-direction, and holdout-product discrepancies are flagged,
not silently corrected. All five new manuscripts have unique section/page
heading matches and retain their finite-only scope.

The [TPC335–339 prerequisite audit](TPC_CONVERSION_SCOPE_TPC335_339.md)
records disjoint-mask norm and output-Gram conditions, common finite control
averaging, trace-positive spectral normalization, and placement-specific
Frobenius support bounds. Empty-source gain and zero-cross-support labels are
not promoted to mathematical quotients or zero residual vectors.

The [TPC330–334 prerequisite audit](TPC_CONVERSION_SCOPE_TPC330_334.md)
checks permutation and quadratic-form boundaries, nonzero polarization
denominators, and nonnegative cross-support masses. It flags the TPC332
proof-package square-root substitution, overlapping new windows, and
TPC333's immediate-parent disjointness claim. Source notation and external
BibTeX are preserved; numerical certificates are not revalidated.

The [TPC325–329 prerequisite audit](TPC_CONVERSION_SCOPE_TPC325_329.md)
checks positive-trace spectral normalization, finite envelope comparisons,
source-coordinate versus shell decompositions, and permutation prerequisites.
It flags the TPC328 composite-coordinate twin label and TPC329's
every-law-positive-row prose/table contradiction, with originals preserved.

The [TPC320–324 prerequisite audit](TPC_CONVERSION_SCOPE_TPC320_324.md)
checks trace/dimension and projector conditions, metric normalization, and
the sufficient common-divisibility translation control. It flags the TPC321
README denominator mismatch, TPC323's missing reference scale if its
reconstruction sentence is read standalone, and TPC324's coherent-trace
qualification. Numerical path guards remain source-reported, not re-proved.

The archive inventory is now `full-source-md=99`,
`reliable-full-md=0`, `partial-or-notes=723`, and
`source-inaccessible=1` across 823 directories. This is a searchable
source-layer and provenance improvement, not a scientific result. The next
batch must preserve original TeX/PDF and hand-edited files, distinguish
partial or inaccessible sources and keep the
TPC-418 STOP boundary unchanged.

## Route history by phase

The repository contains 420 TPC paper directories. The ledger and route map
retain the detailed chronological record; the following compressed map records
the scientific meaning of the phases.

| Phase | Durable outcome | Boundary retained |
|---|---|---|
| Early TPC construction and Bridge-B compiler work | Built typed packet, source, Fourier, Gram, sieve, and loss-ledger interfaces; many exact finite identities and scoped obstructions were recorded | Interfaces and compiler PASS do not identify the actual physical object or prove arithmetic cancellation |
| TPC-111 through TPC-206 | Audited source locks, local normalization, packet/row/Gram decompositions, cross-family holds, and failure modes | Finite or model evidence did not supply the required growing physical theorem, exact cover, or endpoint payment |
| TPC-207 onward | The route map records the Bridge-B moving-hole and physical-observable architecture; the translation-compiler directory has code/results but no local Markdown/TeX/PDF manuscript and is marked `source-inaccessible`. The separate critical-moving-hole paper is accessible | A route-map label or the historical `TPC207_CREATED=false` compiler state does not supply the missing manuscript |
| TPC-208 through TPC-335 | Progressively tested whole-frame, Poisson, collision, packet, source-attachment, and signed-reassembly interfaces, including explicit no-go/obstruction records | Model/profile/operator analogies cannot be promoted to literal source coefficients, fixed `h0`, or arithmetic L2 |
| TPC-336 through TPC-403 | Ran finite source-native, origin, bandwidth, normalization, interpolation, diagonal-deletion, and operator audits | Holdouts and finite spectra are scoped computational evidence; they do not establish growing uniformity |
| TPC-404 through TPC-418 | Extended complete-shell finite proxies from a normalization boundary through four heights, four shells, a full finite operator bound, and a parity-aware finite-family envelope | The strongest current result is finite and synthetic; it earns zero fixed-power credit |

## Current endpoint

TPC418 proves the finite-family shell-parity envelope. The actual shell sign is
`σ_j=ε_j(-1)^(n_j+1)`, and the finite operator bound follows from the
endpoint-star/interior-bulk decomposition. The mixed-parity counterexample is
part of the release. This result is limited to the declared finite synthetic
family.

The current blocker is unchanged:

```text
NONE_UNTIL_GROWING_OR_PHYSICAL_GATE_CHANGES
```

The missing input would have to be a source-backed growing operator theorem, a
level-uniform theorem for the actual moving cloud and all required blocks, or a
complete literal production/pair-to-omega/H1 route with the required
normalization and loss ledger. Even one such local change would not by itself
close the global gate. L0 finite algebra, L1 interfaces/certificates, and L2
arithmetic evidence remain distinct; fixed-`h0`, named-atom, actual support,
strict `1/400`, and `STOP_SCOPED` boundaries remain active.

## Archive interpretation

Older route entries remain useful historical evidence but are superseded where
the current handoff says so. A paper README, theorem ledger, or experiment log
is a searchable reading layer, not automatically a Markdown conversion of the
paper's full TeX/PDF manuscript. The material inventory records this distinction
for every RH/TPC directory. Original TeX, PDF, and hand-edited files remain the
primary artifacts.
