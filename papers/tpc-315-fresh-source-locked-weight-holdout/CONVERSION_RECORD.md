# TPC-315 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `b9723facc6f4c261e20e0d86513230e5351dfe4d`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2fadc1540022b418ac016389f4195e1f9a19ab1467de4b8da63bdaf357f96ea8`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `b02f5e5f17b8f63f26da2b5437da7dc4ead12eb9b3fd0e806a198d93ac17b892`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `79b612c5e6f4b7f1dfb6044d0cce8c8dccbe4a76b705c54cae4e165c2228f672`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2861e076b5ec05c058ca038811997ee437cfce98353df11e1e60ec098c2c7959`.
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
| `Question and route position` | 40 | 1 | `HEADING_TEXT_MATCH` |
| `Fresh physical panel and locked menu` | 54 | 1 | `HEADING_TEXT_MATCH` |
| `Exact identities and interval protocol` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 160 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and route firewall` | 212 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next gate` | 234 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 253 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `71` before writing and `71` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5e8430fb6965adbce0b3e88b2c4dd8498b94d2ea5846e774a207fd00349a9651`.
- Source theorem/proof environment starts: lemma at TeX line 98, proof at TeX line 107, lemma at TeX line 112, proof at TeX line 117, proposition at TeX line 122, proof at TeX line 128, proposition at TeX line 135, proof at TeX line 147.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 60–65 | `95c5bd1e329366728397de96cf1c7d9ccead02dd6bdbbec49814faed459494e0` |
| D02 | equation | 67–70 | `a676f4763403ba7193e37f23e647423fda43132e8be674128f281ab05f83b639` |
| D03 | equation | 76–81 | `9a04f35f0798b9e2ce44f0829e2df931412fb724289cd51ce14cbc4b7f43aa73` |
| D04 | equation | 100–104 | `849138661d0406e17fbf7c30afe0ce27566d2c495cdacd50d897f1f36237d34d` |
| D05 | equation | 138–144 | `68dcc963eecc749956116a574a42ef9e60e7cb50bbd47cbfbf13c22fd78e8e6a` |
| D06 | align* | 198–202 | `67ea256183a5f5ab2286a120ae4e090fc8b8103a3d375b89188fde36feefd867` |
| D07 | align* | 204–207 | `3f74b37921b8aa3b76f6c1816de68bac1ac1b089a6b5587163244146703ce8db` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 12: `\title{Fresh-Source Replication and Weight-Order Obstruction in a Finite Prime--Shell Diagnostic}`
- TeX line 23: `We test whether a finite prime--shell separation class survives a source`
- TeX line 35: `and positive controls have two.  This is a finite same-engine holdout and a`
- TeX line 36: `weight-order obstruction, not an external physical validation, an asymptotic`
- TeX line 43: `a finite below/above-one class, but its target labels came from the same`
- TeX line 49: `This paper answers that question only at the declared finite scale.  The word`
- TeX line 83: `laws.  Their arithmetic motivation does not make any one of them canonical.`
- TeX line 86: `label; these conventions are used here only to name a finite menu`
- TeX line 99: `For every finite sign vector $c$ and weight vector $w$,`
- TeX line 108: `Substitute $G_{p,q}=\langle g_p,g_q\rangle$ and expand the finite squared`
- TeX line 122: `\begin{proposition}[Exact finite sign enumeration]`
- TeX line 160: `\section{Finite results}`
- TeX line 209: `the source change does not select a canonical amplitude law; it exposes a`
- TeX line 210: `finite order obstruction while preserving the coarse class.`
- TeX line 214: `The strongest positive result is a source-first finite replication: after the`
- TeX line 223: `panel.  The finite result therefore supports a class-level diagnostic, not a`
- TeX line 228: `fixed-power credit, leaves full Route-B Gate B open, and makes no statement`
- TeX line 236: `TPC-315 establishes a finite fresh-source holdout under a pre-locked`
- TeX line 245: `keeping any growing claim explicitly open until that interface is paid.`
- TeX line 248: `This manuscript is a finite diagnostic release by Liang Wang (HUST).  It does`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:output` → `main.tex#L64` (existing project target or original TeX label line).
- Link relocation: `#eq:gram` → `main.tex#L69` (existing project target or original TeX label line).
- Link relocation: `#tab:ratios` → `main.tex#L174` (existing project target or original TeX label line).
