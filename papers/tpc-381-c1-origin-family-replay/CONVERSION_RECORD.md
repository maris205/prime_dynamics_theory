# TPC-381 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `0b7ec09219e688a463e4f5c6e939403ceb9c25bb289fb38380b677f22021788d`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `87167ecf8f2d082214bc065e28c74fd1f4949322968bc4b57f1cd17703ba71b8`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `3e61befc14638c91eb98a59b816e677b0f8696480737adef91b77c80953699c0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and claim boundary` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator` | 45 | 1 | `HEADING_TEXT_MATCH` |
| `Predeclared origin-family protocol` | 73 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Independent audit` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `Route status and conclusion` | 136 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `e121f07d0317f996da9639d2754ce11e3d54803b55d8389c2f66d0dab53503dd`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 48–53 | `6bf5d91f3017d3972b4a0a8c0bca402a1e8d3b7b9bed75d2e6f41519f7c4f54f` |
| D02 | \[...\] | 55–59 | `8ab9ddd495690cd531908c07f4aee82f3ad863efd3214d8b85320d0e657ece5f` |
| D03 | \[...\] | 63–66 | `0ea5dff2be936ee3da688ead86c7611e35b2f4faedb7fea3d601b37febab5b16` |
| D04 | \[...\] | 68–70 | `e8214712a30d05d534eb4d3382771ad684d74510636dbfcc48303eb036b639ec` |
| D05 | \[...\] | 76–78 | `dece4a2a0022ba236fdc192703ab0d730e54f9549940b964df27ab7bf9447b67` |
| D06 | \[...\] | 117–120 | `6a35e9ca854c69139b26775028a13fd62684cc1eca44dbeab1af0a3f19a03d05` |
| D07 | \[...\] | 152–156 | `408ee08c5572ba79f7bb0fc9228f12dab6c865c41d209d57ee495534c3eb07c0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `{\Large\bf An Origin-Family Replay of a Finite $c=1$ Prime-Shell Law Control}\\[5pt]`
- TeX line 20: `TPC-380 found that a finite high-$Q$ spectral signature of the all-plus`
- TeX line 27: `finite origin-family persistence with a law-dependence obstruction; it is`
- TeX line 28: `neither an origin/scale-uniform theorem nor a twin-prime result.`
- TeX line 33: `The finite operator family is designed to expose where a proposed near-block`
- TeX line 34: `Route-B bridge needs uniformity.  TPC-380 held the count at $2048$ on its`
- TeX line 40: `All assertions below are scoped to one explicit finite computation.  The`
- TeX line 42: `arithmetic weights.  In particular, finite sub-cap values do not pay an`
- TeX line 45: `\section{Finite operator}`
- TeX line 71: `is an exact finite identity.`
- TeX line 89: `four laws.  This anchor is an audit object, not a row-selection signal.`
- TeX line 98: `\caption{TPC-381 finite count-2048 origin-family law-control panel.}`
- TeX line 122: `and finite numerical residuals.`
- TeX line 133: `summaries.  The local Bridge-B repeats these finite checks and locks the`
- TeX line 140: `evidence rather than an official evaluator verdict.  The exact finite`
- TeX line 142: `are proved finite statements.  The replay and failure census are numerically`
- TeX line 143: `certified finite statements.`
- TeX line 148: `promoted to a law-invariant mask theorem.  Law/origin/scale uniformity,`
- TeX line 150: `source-uniform arithmetic $L^2$, signed prime-shell reassembly, and a`
- TeX line 151: `twin-prime conclusion remain open.  The certificate records`
- TeX line 155: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 157: `The next minimal finite question is`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:count` → `main.tex#L99` (existing project target or original TeX label line).
