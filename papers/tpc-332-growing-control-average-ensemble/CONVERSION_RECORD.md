# TPC-332 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ba1fb3efe59e51e62f64f4dcb607bd390b4b4062`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `af63c4faed47272badfae0765dbff9bb826ad756843313a78b0978d15f33e322`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `26151898fe19ac90e4d68a83b2386cc44c50bff495e31d2580f42b1192c7c3cb`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `820628ff7f5d17f6299e1745ac3c0dbd6a01e6471046b5de85e415b650b4cf86`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `accc0b78dbedfdcd2c62fd639c569d3605c57ae02937654ed626abd83930f4c1`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC330_334.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `Declared finite model` | 48 | 1 | `HEADING_TEXT_MATCH` |
| `Five controls and exact identities` | 85 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate and exact anchor` | 126 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 155 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 194 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility and next question` | 223 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 231 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7e00372c6616732c09590e86a3abc69982bee7adf605c77f2ee0ea2aa3190149`.
- Source theorem/proof environment starts: none.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 50–52 | `ef00deb1077ad608cf8719ca830a5278889cb260b18a0c1c71d2acd970398f30` |
| D02 | \[...\] | 54–56 | `86d949a8a80953c33998e6e470e41f9a2c4428857462eae0a4394245b79f6174` |
| D03 | equation | 58–62 | `a4f5f77780129a29679c3bc005b709759971a7fd165bc0eaa59fbf0371bd2d6b` |
| D04 | equation | 68–72 | `02a7d51cf3ee35a5f59c8ce365d2b8e196e02495199441697ec8bf977392bcf2` |
| D05 | align | 77–81 | `f08e41f245908a0ccca6c8ea770b7f37c19731ac419f2efe47243d0ddf9e503f` |
| D06 | \[...\] | 87–90 | `88d8a2b52ed41ef3afa23472d3d222bb2f106394089e8c2d49f9a0f6f5e19dcc` |
| D07 | \[...\] | 91–93 | `07a9669e578c9f4c6a1823bb72d65b7716e3ca534a1999362550376119a60faf` |
| D08 | \[...\] | 96–99 | `1c5d462446e187e9b4dde942d45347c21074da1213fdd6124ee9861b47f86fcd` |
| D09 | equation | 101–104 | `ca2d4e1c685591921cb66489d944f7865ad80d5ab32232c465668d96297511cc` |
| D10 | \[...\] | 107–110 | `e78888d86fa387269a654022ddf538f5154c9a14ff500f9391936571fac3bcb1` |
| D11 | align | 112–117 | `9c8047dcf743290a770f6081eb880ac1fd61879991f61ab07c78666656734d66` |
| D12 | equation | 120–122 | `6d0d64a4fc48ed1aac98269454656258fc7cb8b48c85c065cba1b78fb2864ebc` |
| D13 | \[...\] | 175–177 | `becfa270c9a247d7cec6d9191a3174bc8af2f822c78b8b72f3b45998d998a068` |
| D14 | \[...\] | 183–186 | `81ee0f97e40ad60a3cc637498deff05d1ed6beddd5aca797890fc941ad707284` |
| D15 | \[...\] | 188–191 | `d8c03863ade53a0ac1dec62df4e5027dbb21b7688c18db00255aaff4bca4abc0` |
| D16 | \[...\] | 216–219 | `2751fabe389f9ba0edffe2ba430b7deb5c4605df3715f6341af2ebdcaa6c6990` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 10: `\title{A Growing Control Ensemble for a Finite Signed-Gram Diagnostic}`
- TeX line 17: `We study the finite signed-Gram diagnostic used in this session's twin-prime`
- TeX line 21: `and 192 law-level decompositions.  Finite quadratic algebra proves an exact`
- TeX line 27: `residual has 27 negative and 21 positive rows.  This is a stable finite`
- TeX line 28: `localization, not an arithmetic estimate: source growth, a canonical sign,`
- TeX line 30: `endpoint remain open.  The algebra is the standard finite quadratic-form`
- TeX line 36: `The signed-Gram object combines a literal prime-shell matrix with a finite`
- TeX line 46: `readouts replicate.  The canonical unpermuted residual sign does not.`
- TeX line 48: `\section{Declared finite model}`
- TeX line 67: `The arithmetic vector is the finite V59 model`
- TeX line 75: `below that cutoff, so ''growing ensemble'' names a finite nested panel only.`
- TeX line 100: `Then $\sum_jz_j=0$.  For any real matrix $A$, finite bilinearity gives`
- TeX line 106: `finite identity with no limiting or arithmetic input.  If`
- TeX line 119: `source layer obeys the exact finite polarization identity`
- TeX line 155: `\section{Finite results}`
- TeX line 192: `These finite descriptors are not a source-uniform asymptotic law.`
- TeX line 204: `\item \texttt{PROVED\_EXACT\_FINITE}: equations`
- TeX line 207: `\item \texttt{NUMERICALLY\_CERTIFIED\_FINITE}: the 48-row decomposition,`
- TeX line 211: `\item \texttt{OPEN}: source-uniform $L^2$, a position-response theorem,`
- TeX line 218: `\texttt{FULL\_GATE\_B=OPEN},\quad\texttt{TWIN\_PRIME\_RESULT=NONE}.`
- TeX line 221: `Bridge-B result is a fail-closed repository check, not an official route pass.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.

- Link relocation: `#eq:three` → `main.tex#L116` (existing project target or original TeX label line).
- Link relocation: `#tab:census` → `main.tex#L160` (existing project target or original TeX label line).
- Link relocation: `#eq:quad` → `main.tex#L101` (existing project target or original TeX label line).
- Link relocation: `#eq:polar` → `main.tex#L120` (existing project target or original TeX label line).
