# TPC-313 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `abdb8bfb644f8d81c8d74b6ac609d88d191b913b`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `7655d52f5285d3019b40fbf776a9de60ced93a931dc8dc8d56fec7c637edc21a`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `409d529cd73eb52f877f1a8434809ee9bb6cc631e1a338de9566316b8959ece0`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `31706a1e3ea96c87f45d67c67d3bfc14be288730aeb0a56e97d9c7dff1417187`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `ab09cf84b8dbf29de540424fc24f3ce64281b66416158f476b784eb2f6526c91`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC310_314.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and route position` | 42 | 1 | `HEADING_TEXT_MATCH` |
| `Finite profile model` | 57 | 1 | `HEADING_TEXT_MATCH` |
| `Rational primal--dual certificate` | 82 | 2 | `HEADING_TEXT_MATCH` |
| `Directed interval layer` | 122 | 2 | `HEADING_TEXT_MATCH` |
| `Results` | 154 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limitations` | 198 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 228 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 245 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `73` before writing and `73` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `8`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `edd81bd46009bce389f8a25c66456829bc5e8a63c3edbc5787c34bde69b70e7c`.
- Source theorem/proof environment starts: proposition at TeX line 84, proof at TeX line 102, lemma at TeX line 136, proof at TeX line 141.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 60–65 | `d2e8cfcde459b7b5cdb50c682b0bc6c052d33de52d3fa1298041911750f17394` |
| D02 | \[...\] | 69–71 | `47cd1f649449892ce5237cb131a3d0cedbd38d0f5b9100ec500af15d4728659d` |
| D03 | \[...\] | 74–77 | `9f88942eee9a22cc18736deff01ab342b8e76d59b5d6e3984b759822c9ba96f2` |
| D04 | \[...\] | 86–88 | `073a8fb63c601fafb574fb74447922eb7510f0dcd2a7a59450ce4c9320db6e7b` |
| D05 | \[...\] | 90–94 | `dccd2c4405edb4fad2adcd8ea8ab17f12cf59acdf149fbcde025b3c451f170ba` |
| D06 | \[...\] | 96–99 | `8c2a2f8785b05ca75c7eff46e039fa9a5cb4396b77cba34c2aac95270d75d85c` |
| D07 | \[...\] | 104–107 | `e26e12cbd6aa30d96cfb386b5313f3095d34cff794414edb340b3c1b78580f5e` |
| D08 | \[...\] | 126–129 | `ad0203943d01098a78f1b871a18fbb038074cb61052d8268532f83a2a2563f62` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 14: `on a New Finite Prime-Shell Panel}`
- TeX line 25: `We close a finite analytic-interface gate left open by the preceding`
- TeX line 38: `finite certificate, not an external holdout, an arithmetic $L^2$ estimate, a`
- TeX line 44: `The prime-shell Bridge-B line has repeatedly separated finite physical`
- TeX line 47: `but explicitly left the profile-budget interface open \cite{tpc312}.  This`
- TeX line 49: `with a genuinely directed finite certificate?`
- TeX line 53: `label; it is not a claim that this label is externally justified.  This`
- TeX line 57: `\section{Finite profile model}`
- TeX line 85: `Assume $M_k$ is positive definite and let $\rho>0$.  Define`
- TeX line 133: `when the denominator interval does not contain zero.  Each operation is`
- TeX line 146: `the finite expression tree proves the claim.`
- TeX line 151: `interval families.  It does not import the producer or TPC-312's producer`
- TeX line 163: `\caption{Finite common-prefix budget certificate.}`
- TeX line 200: `The finite advance is specific but useful.  It turns the previously`
- TeX line 210: `certificate is consequently a source-first diagnostic, not a causal or`
- TeX line 213: `finite engine.  They are new coordinates within that engine, not an`
- TeX line 215: `\item A finite family of rational budgets supplies no uniform estimate as`
- TeX line 216: `$x$ and the shell grow.  In particular, it supplies no arithmetic`
- TeX line 226: `source-first finite separation as a global preference.`
- TeX line 230: `TPC-313 proves a finite interface result: eight first-feasible profile`
- TeX line 236: `theorem, arithmetic $L^2$, full Gate B, and the twin-prime conclusion open.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:main` → `main.tex#L164` (existing project target or original TeX label line).
