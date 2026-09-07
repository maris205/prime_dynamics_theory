# TPC-343 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `e848dbf1895cb067bad6665654a7c992406bcf65`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `987db1c6758d05650266485f790ab788cdb40500e04e163814e1f12baf9f3925`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `103527be9d78484112508c4c56fb9e6c864f9c09d3cf7fbe5c19acf83c4da8a8`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ea40911aece95fbdd3c57605ceda11f3c972730b38806e856fdf03b45da34dd9`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC340_344.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen finite protocol` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Finite identities` | 82 | 2 | `HEADING_TEXT_MATCH` |
| `Independent computational audit` | 115 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 181 | 3 | `HEADING_TEXT_MATCH` |
| `Next finite question` | 208 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `50` before writing and `50` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `d6ad2d56b218aea0725b428ba4ee54125d3222ebddeb3406f969816c779b96ce`.
- Source theorem/proof environment starts: proposition at TeX line 87, proof at TeX line 94.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | align* | 61–64 | `d942fa27a973e9de0d43d45e21b33e301e74ad534e8638323b3731ab3a15d0d2` |
| D02 | equation | 89–92 | `7dcd557ec5f3b7d2246d75c385c1a49446a2ad97919c496809e845770ba3494f` |
| D03 | \[...\] | 108–110 | `b65ceca59b1977f802c305cf035578d6d877d57e73a001b32d90a79cf8789a86` |
| D04 | \[...\] | 175–177 | `cbe38a91fd737c7458025ebf97d0c78f2de15a51a4287b0245e7bcf22515c77b` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 16: `for a Finite Twin-Prime Response Model}`
- TeX line 26: `We perform a finite, protocol-locked meta-audit of two independent panels in a`
- TeX line 35: `finite obstruction to one particular shared nuisance law, while preserving`
- TeX line 36: `the distinction between exact finite linear algebra and the still-open`
- TeX line 37: `source-uniform arithmetic estimates required by the twin-prime route.`
- TeX line 49: `This paper answers only that finite model-comparison question.  The words`
- TeX line 54: `\section{Frozen finite protocol}`
- TeX line 82: `\section{Finite identities}`
- TeX line 84: `Let $N$ be any finite real matrix and let $P_N$ be the Euclidean orthogonal`
- TeX line 88: `For every finite vector $Y$,`
- TeX line 102: `is an energy-weighted finite average of the six row retentions.  The shared`
- TeX line 125: `The exact finite census is summarized in Table~\ref{tab:census}.`
- TeX line 129: `\caption{Frozen census and pooled finite readout.}`
- TeX line 168: `$192.25$ and $320.17$, respectively.  They are reported to make the finite`
- TeX line 169: `coordinate choice visible; they are not a conditioning theorem.`
- TeX line 179: `does not rescue the failed shared in-sample law.`
- TeX line 183: `The strongest positive result is a reproducible finite distinction: row-local`
- TeX line 187: `cross-panel coefficient-stability failure, not a failure of the orthogonal`
- TeX line 192: `TPC343_STACKED_IDENTITY = PROVED_EXACT_FINITE_DECLARED_MODEL`
- TeX line 193: `TPC343_ROW_BLOCK_META = NUMERICALLY_CERTIFIED_FINITE_6_ROW_POOLED_PROJECTION`
- TeX line 195: `TPC343_HOLDOUT_META = NUMERICALLY_CERTIFIED_FINITE_54_RECORDS`
- TeX line 198: `TPC343_SOURCE_UNIFORM_L2 = OPEN`
- TeX line 199: `TPC343_FULL_GATE_B = OPEN`
- TeX line 203: `does not refute an alternative nuisance basis, and it cannot be promoted to a`
- TeX line 204: `source-uniform arithmetic $L^2$ estimate or to an official Route-A/Route-B`
- TeX line 208: `\section{Next finite question}`
- TeX line 213: `same finite/asymptotic firewall and earns zero fixed-power credit until an`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:census` → `main.tex#L130` (existing project target or original TeX label line).
