# TPC-380 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `381a85624245b7177946e9678b6ff7bb50184a4fe5dc0cc72874e679d6d0c2c6`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `a90a5bfd0aa5c2117fe1351cdbc6152ad0a7505610c7bb34eadd0d37a04ef970`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `08ef51dad3d4e789eebf1daa439aff3e81f308b4ed6de23c20b4a1de4004da8f`.
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
| `Finite operator` | 44 | 1 | `HEADING_TEXT_MATCH` |
| `Predeclared count-replay protocol` | 72 | 1 | `HEADING_TEXT_MATCH` |
| `Results` | 91 | 2 | `HEADING_TEXT_MATCH` |
| `Independent audit` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `Route status and conclusion` | 136 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `62` before writing and `62` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `b169508e22cf7cc018c75839fdc890eac96943868320283caa96864b3ae789a2`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 47–52 | `6bf5d91f3017d3972b4a0a8c0bca402a1e8d3b7b9bed75d2e6f41519f7c4f54f` |
| D02 | \[...\] | 54–58 | `8ab9ddd495690cd531908c07f4aee82f3ad863efd3214d8b85320d0e657ece5f` |
| D03 | \[...\] | 62–65 | `0ea5dff2be936ee3da688ead86c7611e35b2f4faedb7fea3d601b37febab5b16` |
| D04 | \[...\] | 67–69 | `e8214712a30d05d534eb4d3382771ad684d74510636dbfcc48303eb036b639ec` |
| D05 | \[...\] | 75–77 | `7bd6dd615a3da76c0ce983c55b3efe67019ca9d58e5a98fd6662e664cbac5c17` |
| D06 | \[...\] | 117–120 | `48b39db4195b60a19499c6d6ebedbcc0d7becdae81fdbba4edd9d98962fca437` |
| D07 | \[...\] | 152–156 | `408ee08c5572ba79f7bb0fc9228f12dab6c865c41d209d57ee495534c3eb07c0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `{\Large\bf A Count-Replay Audit of a Finite $c=1$ Prime-Shell Law Control}\\[5pt]`
- TeX line 20: `TPC-379 found that a finite high-$Q$ spectral signature of the all-plus`
- TeX line 27: `finite count persistence with a law-dependence obstruction; it is neither a`
- TeX line 28: `scale-uniform theorem nor a twin-prime result.`
- TeX line 33: `The finite operator family is designed to expose where a proposed near-block`
- TeX line 34: `Route-B bridge needs uniformity.  TPC-379 held the count at $1024$ and found`
- TeX line 39: `All assertions below are scoped to one explicit finite computation.  The`
- TeX line 41: `arithmetic weights.  In particular, finite sub-cap values do not pay an`
- TeX line 44: `\section{Finite operator}`
- TeX line 70: `is an exact finite identity.`
- TeX line 89: `all four laws.  This anchor is an audit object, not a row-selection signal.`
- TeX line 98: `\caption{TPC-380 finite count-2048 law-control panel.}`
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
