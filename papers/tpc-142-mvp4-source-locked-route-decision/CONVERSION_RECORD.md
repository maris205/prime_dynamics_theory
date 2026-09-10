# TPC-142 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `43d5546ae21c66f92ea9eabbd492f84741901cba5357514306ac4f7c4dbcb059`.
- Bibliography: [references.bib](references.bib), SHA-256 `d88909ae54cf4a941f18726e6b8f96df7103845825ed324f53b0562c9ec7c271`.
- Preserved PDF: [tpc-142-mvp4-source-locked-route-decision.pdf](tpc-142-mvp4-source-locked-route-decision.pdf), SHA-256 `1ccb4d3e84ec8eeb0cbb6b77fb7c3c6a58bfd7f20fb88c054a6c074495ec800e`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `db8f4563a4f778496d39af8cbc651de54ca88b02ba30e7ae3564676c57ee00f0`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC140_142.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `What changed after MVP3` | 133 | 2 | `HEADING_TEXT_MATCH` |
| `A frozen source-locked snapshot` | 173 | 2 | `HEADING_TEXT_MATCH` |
| `Statuses, evidence and active requirements` | 204 | 2 | `HEADING_TEXT_MATCH` |
| `Eight total audit outcomes` | 239 | 3 | `HEADING_TEXT_MATCH` |
| `The strict endpoint and stop directions` | 292 | 4 | `HEADING_TEXT_MATCH` |
| `H9 must be arithmetically independent` | 322 | 4 | `HEADING_TEXT_MATCH` |
| `Projection of TPC-133--141` | 350 | 4 | `HEADING_TEXT_MATCH` |
| `First missing and current verdict` | 393 | 4 | `HEADING_TEXT_MATCH` |
| `Publishable outcomes and next branch` | 432 | 5 | `HEADING_TEXT_MATCH` |
| `Deterministic regression and claim boundary` | 471 | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 503 | 1, 6 | `UNMAPPED_OR_AMBIGUOUS` |
| `References (external bibliography)` | 525 | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `85` before writing and `85` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `9`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `f04d26337adee63223fe7075bc1f23b7371bc94f4bf0526b522e4ae4d74f323a`.
- Source theorem/proof environment starts: definition at TeX line 175, remark at TeX line 198, definition at TeX line 244, theorem at TeX line 265, proof at TeX line 277, remark at TeX line 286, proposition at TeX line 302, proposition at TeX line 334, proof at TeX line 341, theorem at TeX line 406, proof at TeX line 415, corollary at TeX line 425.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 84–91 | `595e08e764c4450af31e9cc956586b3a4312cf18ec2f7e6c04d49ee0b032bf4e` |
| D02 | \[...\] | 107–110 | `8b3a2791d96d2abac2400f32d4689ca760f3e4d96c56da1beb982e6fccff4207` |
| D03 | \[...\] | 141–145 | `009e7ad5c3dd50af05a270a35914852d8b1a50bdda505338c89ec17508e0310b` |
| D04 | \[...\] | 207–209 | `2eb799da87bb01855a422115d9e1c5e8eed0947899c8a742b32d4986baa74d38` |
| D05 | \[...\] | 269–274 | `8a796cd848ba209c5d5c08ec33361395ba9efeab294e324e010db4acfc476bb4` |
| D06 | \[...\] | 295–297 | `6d24b32314728e1948c4bef51f865967fc42c47100d5fecfda25b32cee4f1776` |
| D07 | \[...\] | 326–331 | `d0f284659944ae52b74aeb7c52a7482557a8329a6979c1e9e8e24f067544f9c9` |
| D08 | \[...\] | 396–404 | `c5b77b9cf01964abb408af991608999b65bda845ee4179c6ed4ad79581445baa` |
| D09 | \[...\] | 409–411 | `db6406b2a9c47e48a08d13b0eea55322eec620ed5b17a92bf46b4555b217b2f2` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 36: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 78: `manifest.  Hash equality is only a drift/integrity check; it does not`
- TeX line 89: `\textsc{arithmetic-frontier},\quad \textsc{open}.`
- TeX line 112: `\textsc{go}, not the arithmetic frontier, and not a negative theorem`
- TeX line 142: `|B_{h_0,\delta}(X)|`
- TeX line 167: `TPC-140 then expose, rather than assume, the remaining actual-family`
- TeX line 199: `A content hash detects source drift.  It does not prove a theorem,`
- TeX line 208: `\PROVED,\quad \COND,\quad \OPEN,\quad \NT,\quad \REFUTED.`
- TeX line 210: `An \(\Lzero\) record is a finite or abstract identity.  An`
- TeX line 211: `\(\Lone\) record is attached to the literal fixed-\(h_0\) carrier and`
- TeX line 212: `normalization.  A positive \(\Ltwo\) record must be a uniform growing`
- TeX line 224: `\item a shift-one estimate is not an estimate on a scope-mismatched`
- TeX line 229: `\item a conditional power-ledger formula is not a certified positive`
- TeX line 259: `status-\(\OPEN\), scope-compatible and explicitly a positive`
- TeX line 261: `\item \(\OPEN\): every remaining valid case.`
- TeX line 272: `\STOPR,\quad \NT,\quad \AF,\quad \OPEN.`
- TeX line 286: `\begin{remark}[Conditional synthesis is not a verdict]`
- TeX line 302: `\begin{proposition}[Upper failure is not a lower obstruction]`
- TeX line 311: `lower certificate, merely fails to prove the endpoint and does not`
- TeX line 330: `\mathsf{H7.fixed\mbox{-}h_0},\mathsf{H8.reconnection}\},`
- TeX line 345: `the physical registry assumes a downstream premise and makes that`
- TeX line 364: `H2 & \(\OPEN\) & positive \(\Ltwo\) &`
- TeX line 366: `H3 & \(\OPEN\) & positive \(\Ltwo\) &`
- TeX line 370: `H4 & \(\OPEN\) & positive \(\Ltwo\) &`
- TeX line 377: `Total fixed-\(h_0\) map on every terminal leaf.\\`
- TeX line 416: `The source manifest passes validation, so \(\INVALID\) does not`
- TeX line 420: `hence \(\NT\) occurs before \(\AF\) and \(\OPEN\).  Independently,`
- TeX line 428: `structural \(\Lone\) progress.  It is not a positive \(\Ltwo\)`
- TeX line 449: `A bare missing file is not a negative theorem.  The publishable`
- TeX line 456: `\item attach \(Q_D,Q_Z,G\) and fixed-\(h_0\) maps, or prove the`
- TeX line 466: `remain the only open compatible arithmetic targets, a new frozen`
- TeX line 469: `is \(\STOPR\) or \(\REROUTE\), not a claim about twin primes.`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 8 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#def:valid` → `../main.tex#L176` (existing project target or original TeX label line).
- Link relocation: `#def:verdicts` → `../main.tex#L245` (existing project target or original TeX label line).
- Link relocation: `#eq:synthesis` → `../main.tex#L144` (existing project target or original TeX label line).
