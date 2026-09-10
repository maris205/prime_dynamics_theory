# TPC-182 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `04fdac9f9919f183e39ae42106ef7acd5b2aadede7b3b6e03c6f424957d8d416`.
- Bibliography: [references.bib](references.bib), SHA-256 `4f32cc051d34e291280d4c829003a0edfb742dbf26963606006263c10797a816`.
- Preserved PDF: [tpc-182-mvp8-source-phase-route-decision.pdf](tpc-182-mvp8-source-phase-route-decision.pdf), SHA-256 `9db7942c861a5fd3ad00d261fcc5929e5af1a441f523a540efbdfee7375581b6`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `5ac96526771ae772c0fe14814e2bfe2b1d470b2ac66802721d1e5491f90ee92a`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC180_184.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Dynamic imported state` | 83 | 1 | `HEADING_TEXT_MATCH` |
| `The scoped structural stop` | 114 | 2 | `HEADING_TEXT_MATCH` |
| `Vacuity is not a certificate` | 165 | 2 | `HEADING_TEXT_MATCH` |
| `The production phase registry` | 205 | 3 | `HEADING_TEXT_MATCH` |
| `The selector obstruction` | 236 | 3 | `HEADING_TEXT_MATCH` |
| `Typed routes and endpoint ledger` | 274 | 3 | `HEADING_TEXT_MATCH` |
| `MVP8 decision` | 341 | 4 | `HEADING_TEXT_MATCH` |
| `Claim firewall` | 375 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 389 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `50` before writing and `50` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `15`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `302bc938f5ca3e120857d48f3fad9bd4ef38a359550009950ae5db08e64dcb99`.
- Source theorem/proof environment starts: proposition at TeX line 130, proof at TeX line 135, proposition at TeX line 171, proof at TeX line 182, theorem at TeX line 238, proof at TeX line 244, theorem at TeX line 343, proof at TeX line 358.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 74–76 | `94907c85547b200c63db5d781992da1e0c650f643a0ac9a53eda1d6489aaf784` |
| D02 | \[...\] | 94–102 | `d5d6d7a96fda83526a8120c554cfcdb99763e7cfb6807d559465a73cf2bfd024` |
| D03 | \[...\] | 104–109 | `edb6487a85177d0b97af1d8bd452eaa3997e9a6a7af7b5ef8f1ffeba0af78d0a` |
| D04 | \[...\] | 117–122 | `6c74eb09ea87e00b1fa5c683a0e5ee7b94ccaed63196664b35565faf4183e48b` |
| D05 | \[...\] | 146–149 | `0f9c1541b04554a847c0b889a5531543b44b0d891dfe6fb6c0e5fd5ce2f7f634` |
| D06 | \[...\] | 155–160 | `80c2fe8585f42fc2db5e37dc39fd81e5870156f9c135ea99a7f5742569418c4c` |
| D07 | \[...\] | 174–177 | `b2053557fa54c77dad22cc46780d146f06730cd344d449b9401d31fd68d11c47` |
| D08 | \[...\] | 191–194 | `d296fab01e4d4e25df54b39145b8c78050c97a1ac310f795e345e8489c8f8b0a` |
| D09 | \[...\] | 209–216 | `3c48fedf680addd83b1f84a2c77e06a112c06622f9768e2faa838735d682ad98` |
| D10 | \[...\] | 220–224 | `bcca107c6aa2d04db2f4b00f3a71868de59c22dae2c04f2b7dfb26d079c12c07` |
| D11 | \[...\] | 246–249 | `b4887f1960ca2769c973113f838c8461e71eab953138aff1f6fb78d7b17543fb` |
| D12 | \[...\] | 259–267 | `3167cff4e7c40212cb9b8a0c787afdbb2b66db9d5994a9a81712786da7ffc64e` |
| D13 | \[...\] | 312–319 | `b88ef4dcee674a5b86365abb955195abd24ac09bc88a13c532896c6b71febba0` |
| D14 | \[...\] | 327–339 | `0e9ccdb975c8c3a03297ae88463800d507896b854dc66304ebb99ec0967ba7be` |
| D15 | \[...\] | 346–349 | `797c70230f439a425651788a874df65111ec5bac5af5688dc6ee38b08fe9d307` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 32: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 52: `TPC-173--181 test two interfaces left open by MVP7.  The structural`
- TeX line 58: `cuts.  Empty eligibility does not certify actual active support, and`
- TeX line 59: `the five-field archive address is not a canonical physical`
- TeX line 61: `the occurrence-augmented architecture remains open and`
- TeX line 64: `The phase side source-locks the fact \(h_0=2\), but finds no named`
- TeX line 70: `pointwise fixed-atom targets remain open.`
- TeX line 86: `roots \citep{WangTPC172}.  The present classifier does not assume that`
- TeX line 128: `weight, fixed-\(h_0=2\) lineage, and physical-normalization lineage.`
- TeX line 138: `its two-edge nonvacuity fixture synthetic.  TPC-175 requires every`
- TeX line 162: `does not satisfy the nonempty local-totality hypotheses of the`
- TeX line 165: `\section{Vacuity is not a certificate}`
- TeX line 178: `is vacuously true but does not identify the required production`
- TeX line 197: `does not imply canonical physical representation`
- TeX line 202: `\(\OPEN/\NT\).  The three-root antichain \eqref{eq:h1-roots} is`
- TeX line 210: `h_0=2\quad\text{is source-backed},\qquad`
- TeX line 225: `Neither the value \(h_0=2\) nor a future registry would manufacture a`
- TeX line 241: `does not imply that it contains \(\alpha_\star\).`
- TeX line 269: `reopened by a source-locked named phase, its exact production schedule,`
- TeX line 282: `\caption{MVP8 route cells.  A scoped cell stop does not stop its`
- TeX line 290: `& \(\OPEN/\NT\)`
- TeX line 297: `& Almost-every phase does not select a prescribed singleton.\\`
- TeX line 299: `& \(\OPEN/\NT\)`
- TeX line 302: `& \(\OPEN\)`
- TeX line 305: `& \(\OPEN\)`
- TeX line 331: `\text{carrier}&\text{explicit packet corridor}&\text{actual fixed-}h_0\text{ packet}\\`
- TeX line 354: `The two O161 pointwise fixed-atom targets remain open and`
- TeX line 384: `In particular, this paper does not prove RH, a strict \(1/400\)`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 9 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#prop:empty` → `../main.tex#L130` (existing project target or original TeX label line).
- Link relocation: `#eq:h1-roots` → `../main.tex#L101` (existing project target or original TeX label line).
- Link relocation: `#eq:h1-roots` → `../main.tex#L101` (existing project target or original TeX label line).
- Link relocation: `#tab:routes` → `../main.tex#L284` (existing project target or original TeX label line).
- Link relocation: `#eq:phase-registry` → `../main.tex#L223` (existing project target or original TeX label line).
- Link relocation: `#eq:selector` → `../main.tex#L266` (existing project target or original TeX label line).
- Link relocation: `#eq:ledger` → `../main.tex#L318` (existing project target or original TeX label line).
