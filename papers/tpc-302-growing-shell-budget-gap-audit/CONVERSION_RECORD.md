# TPC-302 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `55240d2d7254cbf8bd7fc0b4755fa8f24254e424`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a7a0e482afc0113481618da36f48341c8e011e407269d16df33fdc8dae34a33e`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `45b49ff7c0cfd760585863eb75c7201a07e7d5d66372450f4b3ce626578310d1`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `bcd9db9c484d72cd264787c65f9df1ed0c447dbb1edae9c42e357d9d33195cd1`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5478c2476717383320cbf75a1e989fe2b210a2ac90ae8ba80219387a775efe35`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC300_304.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and finite model` | 32 | 1 | `HEADING_TEXT_MATCH` |
| `Exact finite identities` | 65 | 2 | `HEADING_TEXT_MATCH` |
| `Source-first audit` | 103 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 118 | 2 | `HEADING_TEXT_MATCH` |
| `Claim firewall and next question` | 148 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 159 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 167 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `49` before writing and `49` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `4`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `38b883aabb90bd09088ef2266e9c868fb67c1620253c09b61dc918626be39671`.
- Source theorem/proof environment starts: proposition at TeX line 67, proof at TeX line 71, proposition at TeX line 81, proof at TeX line 86, proposition at TeX line 93, proof at TeX line 98.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 42–45 | `092054d1083cbbb2c6875e7f402775567d721d8c1b3c59f8f777e2dd49901a8a` |
| D02 | \[...\] | 49–52 | `137fd545b7237e8164d68e3089739d185fcb296e890c62493848fb7ed30ef4aa` |
| D03 | \[...\] | 56–59 | `de3f009790fd6b4c06f2f3cf91cb16d8f1ca5c0cbd3a337e7218cf327ff3008a` |
| D04 | \[...\] | 73–76 | `ef27feab49bf9a548e0a287b6a900ff0e3887a692556442ff1e8ae662f1a8617` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `The preceding finite native-profile audit found a robust budget separation`
- TeX line 23: `row.  The finite Gram and sign-enumeration identities are exact.  At relative`
- TeX line 28: `source-first finite growing-grid certificate.  It does not prove uniform`
- TeX line 32: `\section{Question and finite model}`
- TeX line 34: `TPC-301 showed that a finite native obstruction survives a tolerance ladder,`
- TeX line 40: `Let $S$ be a finite prime shell and let $g_q$ be the exact literal physical`
- TeX line 65: `\section{Exact finite identities}`
- TeX line 68: `For every finite shell, $G$ is positive semidefinite and $R(a)=R(-a)$.`
- TeX line 81: `\begin{proposition}[Finite enumeration]`
- TeX line 141: `The finite result is stronger than a mere reuse of the old target atlas: the`
- TeX line 145: `constitute a lower bound uniform in shell size, source scale, or profile`
- TeX line 150: `The exact claims are finite Gram positivity, global-sign reduction,`
- TeX line 153: `profiles, three tolerances, and two target classes.  A uniform native`
- TeX line 154: `profile-budget theorem and literal arithmetic $L^2$ estimate remain open;`
- TeX line 157: `uniform growth law, or to construct the first growing-shell counterexample.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
