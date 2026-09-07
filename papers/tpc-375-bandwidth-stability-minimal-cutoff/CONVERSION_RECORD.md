# TPC-375 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9f3caca4ec9c543277af86d2ec8c74931a166602acbd81b67a6cac500bec726a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `d1c94d8ff9cc75c479ac02ce6c0285d49265af54ce3b6c7314c0d4ead3a6d85d`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `f923ec651b3df7b55442af1cbff5c1cb92ba3823ec1b5f2f9bf6e87d6000fd9a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and frozen panel` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Operator and nested bands` | 47 | 1 | `HEADING_TEXT_MATCH` |
| `Certification` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Finite bandwidth census` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 141 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `16` before writing and `16` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6968c95478f3aeee2cb8d4129dadd13d4576b5056fd41cc4a3e1a455a1aa1eed`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 50–54 | `f5db465b2dc6d087179609c0df2bf1c818213f06479a9448037c34e308600406` |
| D02 | \[...\] | 56–60 | `878d1ddaa175f9955ab8c9397f8427133ad8d82fdc26ba05578678d163508fb6` |
| D03 | \[...\] | 65–67 | `2e683b578a11684f33d08fa4049089fbd698ceccd12d6821f5f92cc16fd44a67` |
| D04 | \[...\] | 69–71 | `fc33f73db3c6647340ddc9e1e9039fafcf60bb908d4f3db93e2c822a849c606d` |
| D05 | \[...\] | 74–76 | `599dcea121245e6c51f168fbbb85ad6331d0d177cc04da42c6adc89f78245779` |
| D06 | \[...\] | 122–130 | `3642b3fce3b82e28d754cee0ef6c02deb14343b001c0082beb166773c45f8932` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 8: `\title{Bandwidth stability and the minimal finite cutoff for a\newline`
- TeX line 20: `We refine a finite near-block reduction of a response-blind prime-shell`
- TeX line 27: `matching cutoff in the declared finite list.  This is a finite bandwidth`
- TeX line 28: `census under common normalization, not a global bandwidth optimum, a`
- TeX line 29: `uniform operator theorem, an arithmetic estimate, or a twin-prime result.`
- TeX line 36: `left open whether the observed width was merely conservative.  We therefore`
- TeX line 68: `The masks are nested and symmetric, and the exact finite identity`
- TeX line 96: `geometry and does not choose a main-panel row.`
- TeX line 98: `\section{Finite bandwidth census}`
- TeX line 133: `diagnostic profile, not a monotone approximation guarantee.`
- TeX line 143: `This finite census identifies a narrower structural candidate: once the`
- TeX line 149: `The result does not prove that adjacent blocks cause the excess.  It does not`
- TeX line 152: `super-cap on the six high-(Q) rows is a finite obstruction to a purely`
- TeX line 153: `block-local explanation, not an asymptotic theorem.`
- TeX line 155: `The next finite question is an independently declared origin/window holdout`
- TeX line 160: `TPC375_FAILURE_CUTOFF_CENSUS = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 161: `TPC375_PARENT_SUPPORT_REPRODUCTION = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 162: `TPC375_MINIMAL_CUTOFF = NUMERICALLY_CERTIFIED_FINITE_SCOPED`
- TeX line 163: `TPC375_BANDWIDTH_UNIFORMITY = OPEN`
- TeX line 164: `TPC375_CROSS_BLOCK_CAUSALITY = OPEN`
- TeX line 167: `TPC375_FULL_GATE_B = OPEN`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:census` → `main.tex#L106` (existing project target or original TeX label line).
