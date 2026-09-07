# TPC-371 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `388a605cbc0ce49256310c2efc1f2df77edafadd`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `9b19af1f905d66ca092f2335f80d148eba47e008a43138de8f7f8a21e285facc`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `911dab7cf748f633684268541633b5658c02eb09bfbf16ce5958ba956de876e2`; 2 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7b24bfbdebcaa93b75f20ca3a1661770b3f3f096bdae775e5d9a12cb5804ccc2`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Finite operator and frozen protocol` | 58 | 1 | `HEADING_TEXT_MATCH` |
| `Exact finite facts and certification` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 113 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and next step` | 146 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall` | 157 | 2 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `27` before writing and `27` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `99210caa308725360542d66f517fb6f42d4a191038915d26f035b6cdcc4a108c`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 61–65 | `853a2e7d3405aa5cee102032a976038bde03584d57d2a551caaf159a93e4e042` |
| D02 | \[...\] | 68–73 | `28c9a3ac42121366f18b80cf3332b012c193f6762cd8e3c8968e7100b167d0c6` |
| D03 | \[...\] | 74–76 | `aea57f030bbba6313ae7fb2030558b9685df2935069d3f18ca0967c725d09513` |
| D04 | \[...\] | 98–102 | `654c4b345b20344440e2e0fd5b3ebe68c1e600c84456612d88c743b5259cee12` |
| D05 | \[...\] | 139–142 | `16d0f0fd775d2987358decd85fb8114068961f6bcd8873a050758d9dc8622e01` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `\title{Block-local phase localization of a finite\newline`
- TeX line 24: `We study the next finite question raised by a count-2048 prime-shell audit:`
- TeX line 36: `All claims are finite and scoped; no arithmetic or twin-prime consequence is`
- TeX line 52: `The question is deliberately finite.  A positive answer would identify a`
- TeX line 54: `simplest local explanation, while leaving open interactions between blocks and`
- TeX line 58: `\section{Finite operator and frozen protocol}`
- TeX line 89: `exponent one, with shell \(\{5,7\}\).  It is checked separately and does not`
- TeX line 92: `\section{Exact finite facts and certification}`
- TeX line 95: `finite sum of rational squares.  Hence positivity can be checked exactly on`
- TeX line 96: `the declared finite blocks.  The resulting matrices are symmetric.  For any`
- TeX line 97: `finite real symmetric matrix,`
- TeX line 121: `\caption{Complete block-local finite census.}`
- TeX line 137: `high-\(Q\) failures.  The finite observation therefore rules out the narrow`
- TeX line 143: `This is a scoped refutation, not a statement about every partition or every`
- TeX line 149: `Consequently, the absence of a local failure does not prove that off-block`
- TeX line 154: `can test whether the finite excess survives in a component with a common`
- TeX line 160: `TPC371_BLOCK_LOCAL_REPLAY = NUMERICALLY_CERTIFIED_FINITE_576_ROWS`
- TeX line 162: `TPC371_CROSS_BLOCK_COHERENCE = OPEN`
- TeX line 165: `TPC371_FULL_GATE_B = OPEN`
- TeX line 171: `this paper proves no source-uniform arithmetic \(L^2\) estimate, no growing`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#tab:census` → `main.tex#L122` (existing project target or original TeX label line).
