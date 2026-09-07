# TPC-342 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `e848dbf1895cb067bad6665654a7c992406bcf65`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `6f487d2b61330639797e34081ef345607da1eb0a38731bc46df0ab6e174368d9`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `582b7d80bc6b3881f727b6711adc5052f1e1033a3d7e35623523174cc8ecc4f6`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `6c65e1db6ec9ac20a12b6392eac4c3a40b40db188bd0b400c65f43dbb6f1cd07`.
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
| `Question and fresh finite panel` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `Projection and holdout statistic` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Audit protocol` | 105 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 122 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 155 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 183 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `37` before writing and `37` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `684e358101b89ec5e66e5bcefb1f26764e8c202456e4b7f2fe2634a1fdf10071`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 42–44 | `ac062c18460f9bdc0f2392551384f0f5dfdbdb6d9f4d2821bb6973689c66ef63` |
| D02 | \[...\] | 52–54 | `eb9965855c50c092c65635832f79b78dcf298a02a0f35e81236186e843f30ce6` |
| D03 | \[...\] | 66–68 | `40f6fad018b70eca8e2b31df3ff006543bf4f0f8c968882498ad01d794e35054` |
| D04 | \[...\] | 70–74 | `f7d7222ac82663591f3ffe5a5a65aa24a98e1320431c995da50c01671b6fe410` |
| D05 | equation | 77–81 | `d052e32dd65ef30371cf90e983a289f530a5c8c138ab1a4098aaa14f44b532b3` |
| D06 | equation | 86–90 | `d81920424c41664701dc86c027ca2e5716409754169e5a25834b0c73e9090607` |
| D07 | equation | 97–100 | `aece4c361384041545b9bf80f7811f2fde085367acf2805229a327c5e5a1d799` |
| D08 | \[...\] | 174–178 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `holdout split survives a new panel, while the finite projection identity is`
- TeX line 28: `exact and no arithmetic advance is claimed.`
- TeX line 31: `\section{Question and fresh finite panel}`
- TeX line 50: `To obtain a genuinely independent finite check, lock the protocol to TPC-341`
- TeX line 58: `remain below the parent finite cutoff 50,000.  The prime-power mask is empty`
- TeX line 92: `leave-one-control-out diagnostic, not a claim of random sampling or`
- TeX line 95: `\paragraph{Finite identity.}`
- TeX line 96: `For any finite matrix $N$ and vector $y$, the orthogonal projector satisfies`
- TeX line 130: `quantity & finite range\\`
- TeX line 146: `aggregate residual does not transfer to the individual control outputs.`
- TeX line 150: `values are finite diagnostics: they document the geometry and warn against`
- TeX line 166: `\texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}.  The raw replay, rank census,`
- TeX line 167: `and 27 held-out calculations are \texttt{NUMERICALLY\_CERTIFIED\_FINITE}; the`
- TeX line 168: `retention and conditioning ranges are finite numerical observations.  The`
- TeX line 171: `files are absent, so the local Bridge-B wrapper is fail-closed and does not`
- TeX line 177: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 180: `modeling choice, and the finite cutoff-safe holdout does not imply an`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:pythagorean` → `main.tex#L99` (existing project target or original TeX label line).
