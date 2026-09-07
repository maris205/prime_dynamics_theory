# TPC-311 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `b455416a0d2eddb9c4b3413fc899ada16643b9f7d6a0ff44d2144e3b8ce16e55`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `aa7051f88a7052a55b2b2ddec0484361649ef34862e1fda6cf3513d66ca6f525`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `560a045f7e6eb091027846827dfb10ebd095902c263d1cabef371f9929a1c200`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e5d934b0e5433b2108ef3b69705f22d920fb34e7840464862304c22e608a6637`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC310_314.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and route position` | 42 | 1 | `HEADING_TEXT_MATCH` |
| `Locked data and notation` | 60 | 1 | `HEADING_TEXT_MATCH` |
| `Declared two-stage protocol` | 89 | 2 | `HEADING_TEXT_MATCH` |
| `Finite statements` | 119 | 2 | `HEADING_TEXT_MATCH` |
| `Primary results` | 153 | 2 | `HEADING_TEXT_MATCH` |
| `Adversarial localization controls` | 190 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and obstruction` | 224 | 3 | `HEADING_TEXT_MATCH` |
| `Claim firewall and conclusion` | 245 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 275 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `48` before writing and `48` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `42fe14e77d8962f4d08fe8cab2d2d5d7b2eff9010cb4fb092ebf5eb9d0d171b9`.
- Source theorem/proof environment starts: lemma at TeX line 121, proof at TeX line 129, proposition at TeX line 134, proof at TeX line 138.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align* | 66–69 | `168ec8faaa32e1cf947f95f7c85c927440578102f3be5bd99d070318843aa729` |
| D02 | \[...\] | 72–74 | `d493f262361977eb592bc34abc110fc3a12af248ee04acdd893bb4e56b305581` |
| D03 | \[...\] | 80–87 | `10202cec9a4899d13dc1b7133245c8eb09a0b2a07126bb103a0abb6ab9d60342` |
| D04 | equation | 92–98 | `134da477f6a0821a37a919a0c178337345a6398e1275457d4a8dd2832ef6b316` |
| D05 | equation | 101–107 | `3a44eb2b4066245675e6cd9cb38b9663b748446fa923570b46b76d672df67188` |
| D06 | \[...\] | 124–127 | `f38776a70b56fea68136540c624c6a0502bd8d4ad54f9bb9a906a0f5c4d9e812` |
| D07 | \[...\] | 180–185 | `57e1e9014e855ae5139d1eaa19c48e56f90850065ccf3e588f3584974042a49b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 24: `We test whether a single balanced aggregation rule can replicate a finite`
- TeX line 27: `shell transitions, two kernel exponents, three tolerances, and three finite`
- TeX line 36: `unresolved.  We prove the finite two-stage interval algebra and independently`
- TeX line 38: `parameter-slice obstruction on one padded float-replay atlas, not a fresh-data,`
- TeX line 44: `The recent finite diagnostics have progressively separated several sources of`
- TeX line 51: `can reverse a finite class \cite{tpc310}.`
- TeX line 57: `is not an independent physical sample.  Likewise, the rule is declared in`
- TeX line 58: `this child project but is not an externally timestamped preregistration.`
- TeX line 114: `with $r\in\{0,1,2\}$ are adversarial stress controls, not a second primary`
- TeX line 119: `\section{Finite statements}`
- TeX line 121: `\begin{lemma}[Independent finite extrema]`
- TeX line 122: `Let $X_j$ be nonempty finite sets with extrema $x_j^-$ and $x_j^+$.  If the`
- TeX line 136: `interval enclosures for the declared finite operations.`
- TeX line 147: `The finite class relation between calibration $C$ and confirmation $H$ is`
- TeX line 150: `otherwise.  This terminology is a finite decision diagnostic, not a`
- TeX line 184: `\qquad\text{a strict finite reversal.}`
- TeX line 186: `The all-radius stress relation is not a reversal because the confirmation`
- TeX line 221: `Right, Unresolved, and Right.  These are controls on the finite atlas, not`
- TeX line 229: `supplies positive finite extrema with the same independence structure.`
- TeX line 231: `It does not solve the problem exposed by TPC-310.  The primary orientation`
- TeX line 232: `does not replicate from the two-point calibration tolerance slice to the`
- TeX line 235: `finite orientation is still structured by other axes.  A weighting convention`
- TeX line 248: `extrema, the positive equal-stratum interval map, and the finite tau partition.`
- TeX line 251: `TPC-302 target-generation leakage remains inherited.  No arithmetic $L^2$`
- TeX line 252: `estimate, fixed-power credit, uniform asymptotic budget, causal identification,`
- TeX line 257: `For the locked TPC-309 finite atlas, the declared profile-pooled,`

## Conversion limitations

- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:within` → `main.tex#L97` (existing project target or original TeX label line).
- Link relocation: `#eq:between` → `main.tex#L106` (existing project target or original TeX label line).
- Link relocation: `#eq:within` → `main.tex#L97` (existing project target or original TeX label line).
- Link relocation: `#tab:primary` → `main.tex#L164` (existing project target or original TeX label line).
- Link relocation: `#tab:exponent` → `main.tex#L201` (existing project target or original TeX label line).
