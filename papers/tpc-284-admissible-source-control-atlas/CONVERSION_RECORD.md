# TPC-284 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `928077a9bd66c38f38bd0a9ee65d7b903ff25814`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `48cca87e300513e73665153ed511c7863e97e51eb3d9c3927ef98b0648961817`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `e15b825230d514bf9a72b1a9f15a47bc1f2c262290246fd2986599dbcb72a24c`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `c2c4f2a1622cbf9ec7be9c8b347a2a48036539c74d0552c2c09a26d98e4df6fe`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8f9f8a62cf163c46491e111a05da50735a89cb39499f1185c7b362e84359952b`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC280_284.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen operator and control map` | 62 | 1 | `HEADING_TEXT_MATCH` |
| `Interval-sign certification` | 106 | 2 | `HEADING_TEXT_MATCH` |
| `Finite control atlas` | 137 | 2 | `HEADING_TEXT_MATCH` |
| `What the atlas proves, and what it cannot prove` | 189 | 3 | `HEADING_TEXT_MATCH` |
| `Route-B consequence` | 217 | 3 | `HEADING_TEXT_MATCH` |
| `Verification and conclusion` | 234 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 249 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `82` before writing and `82` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `669db002bb4f1d1c5f5374b39a98f322171bc400bf928e9ae0d59cc2d47be332`.
- Source theorem/proof environment starts: proposition at TeX line 124, proof at TeX line 131, theorem at TeX line 191, proof at TeX line 199, remark at TeX line 209.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 46–50 | `534ad64f3d27b5dffb63ad6f4f32d0831f9b18a51776ef935afe3bf3ce73dc54` |
| D02 | equation | 66–71 | `c60a27493aa7423b59fb5674add83e8573500cfa1337322f888c386f2eec50e5` |
| D03 | equation | 73–77 | `04629f7a0b14358729715f92034a3bd19f3ac370e8f83fa8d53f4edac1b91a3b` |
| D04 | equation | 81–84 | `3ca468897cef1383e9dcc3271508c022c3037c99032268d61c7a3f9264a2f20d` |
| D05 | equation | 88–92 | `36ed16afe6db3260573ddb2de8df8f0a17838d574c8b06e1eba9262bc9f1010d` |
| D06 | equation | 94–101 | `9925821a12be9699ec95bf3dc7086e711073f28e5ac5bf752b40293307e894fd` |
| D07 | equation | 117–121 | `010c832b69c07fe0509990186a54a5aca252f942b327d3bdc8f2b291172acebc` |
| D08 | equation | 140–144 | `a542238d8548dfbbb268bac643ad8b217651257a1f4625aadd09029e88440c59` |
| D09 | equation | 147–151 | `df489e0a7faed22d2095debc017310298a1c1603c5d1482dbc2d135c9f1c9c08` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `\title{A Finite Control Atlas for Literal Twin-Prime Source Attachment}`
- TeX line 26: `explicit family of controls inherited from the literal finite operator: change`
- TeX line 29: `kernel exponents this produces a 72-row finite control atlas.  Outward`
- TeX line 34: `upper endpoint is about $0.1539$.  Thus the finite literal source remains`
- TeX line 35: `nonzero under the declared controls, but finite non-vanishing does not imply`
- TeX line 37: `source class; asymptotic stability, arithmetic $L^2$, and Gate B remain open.`
- TeX line 58: `declare a finite control set, replay it, and report exactly what that set does.`
- TeX line 60: `finite table to a growing theorem.`
- TeX line 124: `\begin{proposition}[finite sign predicate]`
- TeX line 137: `\section{Finite control atlas}`
- TeX line 153: `$0.153899$.  Both values are finite extrema over the declared atlas, not`
- TeX line 154: `uniform constants.`
- TeX line 186: `therefore certify orientation sensitivity of the finite source readout under`
- TeX line 191: `\begin{theorem}[declared finite control atlas]`
- TeX line 209: `\begin{remark}[finite versus asymptotic]`
- TeX line 210: `The theorem quantifies only a finite declared set.  It does not say that a`
- TeX line 219: `The literal source interface now has two separate finite facts.  Under the`
- TeX line 222: `nonzero, but the orientation can change.  These facts are compatible: a finite`
- TeX line 224: `the other between sampled parameter values, and a finite nonzero table gives`
- TeX line 227: `Consequently the next useful theorem is not a generic ''stability'' slogan.`
- TeX line 231: `contributes the finite control atlas and identifies the sign-stability`
- TeX line 242: `The main conclusion is deliberately narrow: the declared finite controls`
- TeX line 245: `asymptotic theorem.  The corresponding open problem is to characterize a`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:flips` → `main.tex#L165` (existing project target or original TeX label line).
- Link relocation: `#eq:baseline` → `main.tex#L91` (existing project target or original TeX label line).
- Link relocation: `#eq:controls` → `main.tex#L100` (existing project target or original TeX label line).
- Link relocation: `#eq:census` → `main.tex#L143` (existing project target or original TeX label line).
- Link relocation: `#tab:flips` → `main.tex#L165` (existing project target or original TeX label line).
