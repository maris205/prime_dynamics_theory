# TPC-270 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `6be994e34a06fda0de2ed0bcaa42ff3db716ffef`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `6056fecb17aad48ce203328283f11db469052d03c7cea51fc74a606235b8162a`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `e145be2709dc08c1b839f85593b8cf2c71f60be47dab9b6d69b90ccb20f0ae09`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `16814496b92c160f0e2043fa307fddcd439d20a594161d71b5a946dfed72eb4c`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC270_274.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position and claim firewall` | 35 | 1 | `HEADING_TEXT_MATCH` |
| `The frozen finite residual` | 53 | 1 | `HEADING_TEXT_MATCH` |
| `Endpoint normalization` | 104 | 2 | `HEADING_TEXT_MATCH` |
| `Certified finite result` | 141 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 212 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 227 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 236 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `67` before writing and `67` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `893a30deeffd47336a9e845ea88487f19c7fc0d2e673583969e1d94de70cadc3`.
- Source theorem/proof environment starts: lemma at TeX line 113, proof at TeX line 124, theorem at TeX line 170, proof at TeX line 197.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 55–58 | `6d8ab4bf835dff72e1c64599f9f292b2bcfbc5cdd51e022091255aea8983bf1c` |
| D02 | \[...\] | 60–64 | `c712d2ff398aa6a0c144dbcf3cee89f3c8155902120e0e0ee70f226c4f0b5ec2` |
| D03 | \[...\] | 66–70 | `5cbfc0183f63c3e12f6856f3c36a38f67b12f9fc460cfa28e78430ac71e31329` |
| D04 | \[...\] | 75–77 | `5cdfa79bd7eb2012f885b2340c7596dc9202bb7577a95ac2aaf93b9d56c2b006` |
| D05 | \[...\] | 80–83 | `177aace148296be3174142e2f618f93663095b4892ba95e0bf4ebdcac5554ba2` |
| D06 | \[...\] | 86–89 | `5783916bf0cf2adda5fd5194db8aa8548d53694e67f6548df4821b4e78ce182d` |
| D07 | \[...\] | 93–95 | `af3e4079b23905a7150d9b3b3a9f2aba8e977cb19a1bfad3235b1b5a49130350` |
| D08 | \[...\] | 97–100 | `00d6a0a09a99b583150ac4d093511880e654f63325cda2f8f50335d7001701ae` |
| D09 | \[...\] | 108–111 | `2fadb67f01f1258e33954ba02b346996cc33a72784e41e5a9e709f1074bc6fef` |
| D10 | \[...\] | 115–117 | `62e8a35538bbcd052c16c045a9f84847cff2b8fb10831a03d7964e65bb550861` |
| D11 | \[...\] | 119–122 | `e168f31ed5c74c815701e6f4e277ede87484f58e75b24f4a5d9a87da4bdc7c40` |
| D12 | \[...\] | 133–137 | `55d3b517c243c025ac7d408517013574aa2d4a7e4b0840627ab22eea3fed5a38` |
| D13 | \[...\] | 143–146 | `f53a7b4b982352fe9898ad8feb4ec7ab1965fa5a4bf10e07f0537487c97e3fde` |
| D14 | \[...\] | 183–185 | `b6ba4e59e161f04d4a1ea3c8b6c9963a339f3e3ce14be13f99566345cc6c6cd4` |
| D15 | \[...\] | 187–194 | `13544f99779915df5cf41d352e843fe2c225d461228646fe869a0f856f33620f` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 15: `\title{Cross-Scale Endpoint-Normalized Radius in a Finite V59 Residual}`
- TeX line 23: `residual radius. We introduce the dimensionless finite observable`
- TeX line 27: `source-compatible finite registry, four dyadic ratio intervals exhibit the`
- TeX line 31: `finite normalization audit and a scoped stability obstruction; it is not an`
- TeX line 37: `TPC-267 instantiated the literal prime-shell object at finite scale, and`
- TeX line 38: `TPC-268 showed that declared finite cutoff changes can alter its quarter-sector`
- TeX line 40: `two-profile path, finding a finite profile flip. The remaining minimal question`
- TeX line 42: `same finite interface?`
- TeX line 46: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_CROSS\_SCALE\_RADIUS\_NORMALIZATION\_AUDIT}.`
- TeX line 48: `The word ''finite'' is part of the claim. The registered scales are a diagnostic`
- TeX line 49: `registry, not an asymptotic sequence with a proved source-level uniformity law.`
- TeX line 53: `\section{The frozen finite residual}`
- TeX line 59: `The source and shifted-prime comparison are the finite objects used in TPC-269:`
- TeX line 72: `and the Euler product is enclosed by the finite tail protocol.`
- TeX line 85: `matched scales we also use the source-compatible finite mixture`
- TeX line 101: `All non-logarithmic terms are rational on a finite row. The logarithms and the`
- TeX line 107: `number into a finite certificate. We instead define`
- TeX line 128: `in (2) is rational in the finite interval engine.`
- TeX line 141: `\section{Certified finite result}`
- TeX line 148: `stored radius-square intervals are inherited from the exact finite operator`
- TeX line 170: `\begin{theorem}[finite cross-scale normalization audit]`
- TeX line 174: `\(a\to b\)& \(D(a,b)\) interval & finite classification\\`
- TeX line 198: `The finite operator and projection are the frozen TPC-269 objects. The interval`
- TeX line 207: `\(\mathrm{DROP, DROP, RISE, DROP, RISE}\), with the largest finite rise at`
- TeX line 209: `ratios at the same scale: they quantify a finite profile effect without being`
- TeX line 214: `positive quantity and makes cross-scale comparisons auditable. The main finite`
- TeX line 220: `asymptotic sequence or a uniform source-level estimate. Second, a finite rise`
- TeX line 221: `of \(D(a,b)\) does not refute an eventual bound`
- TeX line 223: `Third, a finite drop does not prove such a saving. Finally, the radius product`
- TeX line 224: `is not an arithmetic \(L^2\) estimate and does not reassemble the signed`
- TeX line 228: `TPC-270 adds the missing finite scale lens to the TPC-267--269 chain. The exact`
- TeX line 229: `sixth-power normalization and positive interval ratios expose strong finite`

## Conversion limitations

- 4 whitespace separator(s) inserted after inline math before numeric prose to preserve dollar-delimiter parsing; formulas and original TeX are unchanged.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:base` → `main.tex#L154` (existing project target or original TeX label line).
