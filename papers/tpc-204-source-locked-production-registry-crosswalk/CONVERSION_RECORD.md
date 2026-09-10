# TPC-204 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `dd95678d4bbbc4aa5a2e0cfdf07e6c431d0c19faea78e385c1596d1e36136354`.
- Bibliography: [references.bib](references.bib), SHA-256 `3ee9e3dda0cf4e899efc7979c0a0d679c44266e1a87b692ae6f91fc1dbeb6f2e`.
- Preserved PDF: [tpc-204-source-locked-production-registry-crosswalk.pdf](tpc-204-source-locked-production-registry-crosswalk.pdf), SHA-256 `85d4dcd8436e5b049933584d68407924019c1d82b6b9c85122d84c3e101290f9`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2ad4dcbdae7f683888c910953765de4f55ad772ab6c209bf865b079aef772eb6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC200_204.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Authorization and mathematical boundary` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Declared candidate universe` | 50 | 1 | `HEADING_TEXT_MATCH` |
| `Three formula types` | 92 | 2 | `HEADING_TEXT_MATCH` |
| `The finite first-mismatch theorem` | 114 | 2 | `HEADING_TEXT_MATCH` |
| `Scope, stop cell, and open parents` | 163 | 3 | `HEADING_TEXT_MATCH` |
| `Machine certificate and trust boundary` | 180 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 200 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `34` before writing and `34` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `5`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `9b9a8e2f428291a2b8cda3092641f2ec32cd48a0ca6def8196873fcc9c84c67d`.
- Source theorem/proof environment starts: theorem at TeX line 116, proof at TeX line 131.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 35–37 | `c75c320000954c75eea58382484d4a658d664e8489da228290ee3e9801d073a8` |
| D02 | align* | 95–106 | `daac55aa68b417061f2477f33bbad076fcbc22cfa69718b67c3a1c9410b22da4` |
| D03 | \[...\] | 122–124 | `113b5b763d4e605d2114085222a9bde78056cc3df9590dd2a4327128818e821f` |
| D04 | \[...\] | 126–128 | `3404712622226b007099ad05eaa46fb4e9a6d8ac8606e3535708b6504523766d` |
| D05 | \[...\] | 166–169 | `3f0ec4fa761c47d4a8f9197dec854822de85c1e64a0980c6ff4255cb08e344a6` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `\title{\textbf{Source-Locked Production Registry Crosswalks: A Finite Exact-Matching and First-Mismatch Certificate}}`
- TeX line 22: `plausibly enter the production packet-prefix crosswalk left open by TPC-194.`
- TeX line 28: `This is an L0/L1 finite-corpus result, not a fixed-atom cancellation theorem,`
- TeX line 29: `a direct-route reopen, or an L2 gain.`
- TeX line 39: `subsequently authorized one finite TPC-204 whose outcome had to be either an`
- TeX line 41: `workflow input only.  It neither supplies source data nor makes any reopen`
- TeX line 45: `schedule, one common \(X/N/q\) range, a uniform constant \(C\), a positive`
- TeX line 72: `& \(q/T\) cumulative prefix off the shadow & Periodic \(\rho\) is not a named atom\\`
- TeX line 74: `& Terminal-block Parseval theorem & Phase \(L^2\) is not a named atom\\`
- TeX line 82: `& Every fixed \(\gamma\), logarithmically weighted & Fixed \(\gamma\) is not a production record\\`
- TeX line 114: `\section{The finite first-mismatch theorem}`
- TeX line 125: `Consequently the finite verdict is`
- TeX line 142: `as hypotheses, and its \(N=T\) substitution does not convert the terminal`
- TeX line 153: `\(\xi=(\theta,c,\kappa,r)\) is a resolved key, not a production schedule.`
- TeX line 163: `\section{Scope, stop cell, and open parents}`
- TeX line 170: `It stops only extraction of a complete crosswalk from this explicit finite`
- TeX line 171: `corpus.  It is not a theorem that no production registry exists in a larger`
- TeX line 173: `\texttt{O161} pointwise parents and the global architecture remain open.`
- TeX line 193: `stable PDF.  It is a repository review pin, not an external signature or`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 8 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
