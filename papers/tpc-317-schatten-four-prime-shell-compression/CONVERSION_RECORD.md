# TPC-317 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `69fabb27000d381d3f65ced7ad4864ae5a976be2b64cc2fffe2fadebc65fd2f7`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `80e9f40e383bdd378070b665dd4fbc079032869e21cb82a4e6856c98c5820b62`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `0903a4ed6caadad5c319903335c970e67f897607e66f4f479409e04ea95e1dee`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2df343e188b5226e0dcf8b714f0b42bbfd9e9f18b3d229748aea84e93c49362e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC315_319.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and route position` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `The locked literal operator` | 66 | 1 | `HEADING_TEXT_MATCH` |
| `The trace-power envelope` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Certificate protocol` | 157 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 188 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and claim firewall` | 256 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next gate` | 280 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 305 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `75` before writing and `75` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `11`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2779d6815993a22250583526d2fb356286f450394738a0d74367e5b11b303074`.
- Source theorem/proof environment starts: theorem at TeX line 100, proof at TeX line 117, lemma at TeX line 141, proof at TeX line 151.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 69–71 | `5436e15859f88756b13d4ff181fef21d096046c470d573aba6881d87156c65ef` |
| D02 | \[...\] | 73–75 | `26525f75aa4e1575ff22f71dc5c9c1d1e2b133cd60584e315ad75ed4c1378201` |
| D03 | equation | 77–83 | `749d14db6a51898ab359517b46fd88eb59e7ffb20b683121aecfb4edd93119d1` |
| D04 | equation | 85–91 | `80d8fc936c1f1f92e89937cbccc35ab41198dd356939706bb59659c3499d14a9` |
| D05 | equation | 103–108 | `b6fd128ff78a78a6945376fdb01436bece9a0a718252616b6b9ddef5286eb0fa` |
| D06 | equation | 110–114 | `cc5dd5f3116901266576a7d52e8508a6c3322c691c66b1ab7ddb48e81205139e` |
| D07 | \[...\] | 122–126 | `d11a84a62b41a4867b3e35c1a6cb91a1dd354ea04b63c26c1637d56e6a6aec4d` |
| D08 | \[...\] | 135–137 | `ea60488a7b4d584680c975f72067a7aa6108855af5468fd40834c2ec7c349798` |
| D09 | equation | 143–148 | `107a78d00d77baae73e6086ad92aef58e7cca3179047e7690e9bfec385c160f9` |
| D10 | \[...\] | 160–164 | `a03048c32dd3482e6e25964d4a141932ba1ec8918d658f1cfd3cb93a62d02f50` |
| D11 | \[...\] | 283–287 | `61eb4e686684ddad34b81575cf176ec9ff9276e235b50acc8790e8257bce7349` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `formula into a literal finite source-to-output operator, but used only its`
- TeX line 29: `For the positive-semidefinite Gram matrix $G=A^*A$, finite spectral calculus`
- TeX line 40: `by exact rational arithmetic.  The large-panel values are finite numerical`
- TeX line 41: `certificates under a declared binary64 error budget, not an asymptotic`
- TeX line 43: `Gate-B closure, and a twin-prime conclusion remain open.`
- TeX line 49: `formula and proved a finite Frobenius interface.  Its normalized`
- TeX line 59: `This is a finite norm audit, not a replacement for the missing arithmetic`
- TeX line 60: `reassembly.  In particular, a finite decrease of an upper envelope cannot be`
- TeX line 95: `rational number, so every finite Gram entry and every finite trace power is`
- TeX line 100: `\begin{theorem}[finite Schatten--4 chain]`
- TeX line 101: `Let $G=A^*A$ for any finite row of \eqref{eq:operator}.  Then, for every`
- TeX line 118: `The matrix $G$ is positive semidefinite.  Let its eigenvalues be`
- TeX line 138: `This is a descriptive finite statistic; it is not a rank theorem for a`
- TeX line 176: `safe uniform bound $|K_{p,u,t}|\leq160$.  Trend decisions`
- TeX line 179: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE} under this explicit model, not`
- TeX line 188: `\section{Finite results}`
- TeX line 218: `decreases.  The effect is not an artifact of a single shell or exponent.  The`
- TeX line 248: `The opposite trends are the central finite finding: the Frobenius mass grows`
- TeX line 258: `The strongest positive result is mathematical and finite: the PSD Gram chain`
- TeX line 265: `The strongest obstruction is equally important.  The computation does not`
- TeX line 268: `uniform law in $X$.  Moreover, the prime-shell labels are still aggregated in`
- TeX line 270: `proved.  The result therefore pays no fixed power and does not advance the`
- TeX line 275: `finite diagnostic, not an external physical holdout.  The Session-named`
- TeX line 282: `For the literal prime-shell operator, the finite inequality`
- TeX line 290: `Frobenius envelope is upward in all 16.  This is a real finite spectral`
- TeX line 300: `This manuscript is a finite diagnostic release by Liang Wang (HUST).  It does`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:operator` → `main.tex#L90` (existing project target or original TeX label line).
- Link relocation: `#eq:normalized` → `main.tex#L113` (existing project target or original TeX label line).
- Link relocation: `#tab:s4` → `main.tex#L199` (existing project target or original TeX label line).
- Link relocation: `#eq:normalized` → `main.tex#L113` (existing project target or original TeX label line).
- Link relocation: `#tab:s4` → `main.tex#L199` (existing project target or original TeX label line).
- Link relocation: `#tab:hs` → `main.tex#L230` (existing project target or original TeX label line).
