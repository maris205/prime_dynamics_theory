# TPC-341 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `e848dbf1895cb067bad6665654a7c992406bcf65`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `0a3360717f8180cdcc9c07f09d08f022b5a96d8f8632a730f06d2d0b4ba426a1`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `a4cf2e01f2839108248962f4e5143966a9edf46ad7c578d326165de7f2433e07`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `f1873cea17641d2685f9200f275766a337b6c9b48f34cbcac1f8276dbbf8909b`.
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
| `Question and fresh finite panel` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Projection and holdout statistic` | 62 | 1 | `HEADING_TEXT_MATCH` |
| `Audit protocol` | 104 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 121 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 154 | 2 | `HEADING_TEXT_MATCH` |
| `Conclusion and next clue` | 181 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `38` before writing and `38` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `249181c5c325c1e33468bde19b89e5843da31ea292949bd5f93e0e4252685442`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 43–45 | `ac062c18460f9bdc0f2392551384f0f5dfdbdb6d9f4d2821bb6973689c66ef63` |
| D02 | \[...\] | 52–54 | `8582116bbe255b299bca9d373e22bc5161ecb4959982bb33071c546f5840bc63` |
| D03 | \[...\] | 65–67 | `40f6fad018b70eca8e2b31df3ff006543bf4f0f8c968882498ad01d794e35054` |
| D04 | \[...\] | 69–73 | `f7d7222ac82663591f3ffe5a5a65aa24a98e1320431c995da50c01671b6fe410` |
| D05 | \[...\] | 76–80 | `a1458b90e8d22f54f4c7b890bbcdd448d5274673c9a5263d94b92e034c9ce97a` |
| D06 | \[...\] | 85–89 | `44c31bb9ede978c75a8166bc6429aa229fbe9ec7db2e18208b921a1a4ee43582` |
| D07 | \[...\] | 96–99 | `796d049e43c400c28c3c18204534fc6fb40235b21ed9855fe82fb5ca4be3a02e` |
| D08 | \[...\] | 172–176 | `b1ecb493a23905cd4330ee82c941a731d747254a15a561fc47d6d449060a62e0` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 28: `tests.  The finite projection identity is exact, but mean-only nuisance`
- TeX line 29: `removal is not control-stable on this panel and yields no arithmetic advance.`
- TeX line 32: `\section{Question and fresh finite panel}`
- TeX line 51: `To obtain a genuinely new finite check, use the three origin/scale pairs`
- TeX line 58: `remain below the parent finite cutoff 50,000.  The prime-power mask is empty`
- TeX line 91: `leave-one-control-out diagnostic, not a claim of random sampling or`
- TeX line 94: `\paragraph{Finite identity.}`
- TeX line 95: `For any finite matrix $N$ and vector $y$, the orthogonal projector satisfies`
- TeX line 129: `quantity & finite range\\`
- TeX line 145: `aggregate residual does not transfer to the individual control outputs.`
- TeX line 149: `values are finite diagnostics: they document the geometry and warn against`
- TeX line 164: `\texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}.  The raw replay, rank census,`
- TeX line 165: `and 27 held-out calculations are \texttt{NUMERICALLY\_CERTIFIED\_FINITE}; the`
- TeX line 166: `retention and conditioning ranges are finite numerical observations.  The`
- TeX line 169: `files are absent, so the local Bridge-B wrapper is fail-closed and does not`
- TeX line 175: `\texttt{FULL\_GATE\_B=OPEN}.`
- TeX line 178: `modeling choice, and the finite cutoff-safe holdout does not imply an`
- TeX line 189: `batch; no new project is opened here.`

## Conversion limitations

- No reader warning or automated roundtrip discrepancy detected. Independent proof/semantic review is still not claimed.

- Link relocation: `#eq:pythagorean` → `main.tex#L98` (existing project target or original TeX label line).
