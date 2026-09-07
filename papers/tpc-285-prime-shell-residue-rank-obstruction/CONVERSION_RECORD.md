# TPC-285 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `c9f2a3559e421cb10eaf51c1268a03b838c5ed68`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `b3b13c8de5e4656a1fe45880c2859326de14b4ff401e911b7244d4cb392e9540`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `b4a9d4985e9705129bd54064ebee45c7a090907906777330590998043cb31cc6`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `9d21f251042014110556435dd60ba513e7b8148c6eae25e34dcf66145250ec83`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8fa06a51fd3c02b4545ec54dc17df6a90e1462016839f8fb52e3d7528e6c67d1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC285_289.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and frozen object` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Exact centered factorization` | 79 | 2 | `HEADING_TEXT_MATCH` |
| `Diagonal deletion restores full active rank` | 105 | 2 | `HEADING_TEXT_MATCH` |
| `Finite kernel-Schur audit` | 159 | 3 | `HEADING_TEXT_MATCH` |
| `Consequence for the twin-prime route` | 210 | 3 | `HEADING_TEXT_MATCH` |
| `Verification and conclusion` | 228 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 247 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `93` before writing and `93` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `921a16e346118cfed33a047cb05c7caa2af73d9aa60d257e7c6c840587c8dfa2`.
- Source theorem/proof environment starts: theorem at TeX line 81, proof at TeX line 92, theorem at TeX line 117, proof at TeX line 126, remark at TeX line 152.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 51–56 | `0de02c26c9137d42cc2ab484423b7af6a39285955dffac7c5482bb622a54bb37` |
| D02 | equation | 59–63 | `992684574af9ddd0cce128898f26af037b12304855d32dc08d0c88d2db6e184a` |
| D03 | equation | 65–69 | `a6542c8e2ca9ab7695841f21c5ca3f8dcb7ea5e11b055bc628d2fade62673a2f` |
| D04 | equation | 71–74 | `7018afd76149b9900d7509497d98a9690c7cca284adac3b198c405efe860a153` |
| D05 | equation | 83–87 | `6d51b6cff8b8a96b4b6ce82af56eda1308d6d67562e7eef8636cd4653eab8433` |
| D06 | equation | 111–115 | `3adfa7cccf43fc77595a48a67aec62f84fb5b9596c9876495a17c79d5f4c5551` |
| D07 | \[...\] | 120–122 | `8cc2fa921e5d1c43e2a67ad94cb455f1353de94d85259b36b7bf44de6ecfdc8b` |
| D08 | \[...\] | 134–136 | `7d3657e727a153d01be39ffcc128c26a3773bcd66292865283c35fcd19ae3983` |
| D09 | equation | 140–145 | `ec04adcff6f08f7af480406a78502de19903ba5a026cac325f35e6847ec9d150` |
| D10 | equation | 162–166 | `0fd034a89ad8782ca5574a4006f2f4b3ca5674fb3a28b0b7f6ba0b21206570e4` |
| D11 | equation | 194–203 | `6bc484ddd6168cdc04a912c550c906a0c110db44e9f7f40c7f2cc96ff418a9b9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 23: `The finite control atlas of TPC-284 shows that small changes in a prime-shell`
- TeX line 43: `finite schedule controls and found eight baseline sign flips~\cite{tpc284}.`
- TeX line 49: `Let $I$ be a finite interval of integer indices and let $q\geq3$ be prime.`
- TeX line 82: `For every odd prime $q$ and finite index set $I$,`
- TeX line 108: `$J_q$ congruent to $a$ modulo $q$.  Assume $n_a>0$ for every`
- TeX line 153: `The result is not a claim that diagonal deletion destroys every possible`
- TeX line 159: `\section{Finite kernel-Schur audit}`
- TeX line 175: `\caption{Finite rank audit.  The modular ranks are rational-rank witnesses.}`
- TeX line 206: `finite check of the implementation.  The fourth line is intentionally only a`
- TeX line 207: `finite certificate.  No general theorem is asserted for the kernel Schur`
- TeX line 215: `physical matrix is not a rank-$q-2$ object after the diagonal convention, and`
- TeX line 216: `the kernel-weighted finite blocks remain full rank.  Therefore a literal`
- TeX line 223: `Schur weights.  The observed finite sign flips are therefore compatible with`
- TeX line 225: `orientation claim.  Conversely, full rank alone is not a negative result for`
- TeX line 239: `kernel-Schur blocks are finitely certified full rank.`
- TeX line 242: `The next open theorem is a signed full-shell spectral or $L^2$ bound that uses`
- TeX line 244: `open, and no twin-prime conclusion follows.`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:B` → `main.tex#L62` (existing project target or original TeX label line).
- Link relocation: `#eq:factor` → `main.tex#L86` (existing project target or original TeX label line).
- Link relocation: `#eq:det` → `main.tex#L144` (existing project target or original TeX label line).
- Link relocation: `#eq:factor` → `main.tex#L86` (existing project target or original TeX label line).
