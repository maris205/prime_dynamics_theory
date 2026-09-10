# TPC-162 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `546cc0c209506c9a9831a665efa8ff4c4057afad01aa5a8773773ad4670b13d2`.
- Bibliography: [references.bib](references.bib), SHA-256 `f1fb0da3ab041bcf51fa930f6db9562b04c28ace5111c844fed4b7bb9d3d635c`.
- Preserved PDF: [tpc-162-mvp6-actual-carrier-endpoint-route-decision.pdf](tpc-162-mvp6-actual-carrier-endpoint-route-decision.pdf), SHA-256 `be95697a31a290e975ebda1554cfc88659190870159227ea952a5932af0f3c75`; 7 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `1972a1a0c0514b4c62b57c288a0757e76c42e76cf93153e29a90bd590ec0b8d4`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC160_164.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `The two corridors entering MVP6` | 115 | 1 | `HEADING_TEXT_MATCH` |
| `The structural corridor` | 117 | 1 | `HEADING_TEXT_MATCH` |
| `The arithmetic corridor` | 162 | 2 | `HEADING_TEXT_MATCH` |
| `A source-locked MVP6 snapshot` | 229 | 3 | `HEADING_TEXT_MATCH` |
| `Two frontiers that must not be merged` | 260 | 3 | `HEADING_TEXT_MATCH` |
| `Route semantics and classifier` | 341 | 4 | `HEADING_TEXT_MATCH` |
| `Endpoint V3` | 427 | 1, 5 | `UNMAPPED_OR_AMBIGUOUS` |
| `The MVP6 decision` | 474 | 5 | `HEADING_TEXT_MATCH` |
| `Next forced objects` | 521 | 6 | `HEADING_TEXT_MATCH` |
| `Reproducible audit` | 553 | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 589 | 7 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 603 | 7 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `87` before writing and `87` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `21`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `5b3ff1d49369370b836f085c115e4fa71b56cf80b6f81fb96a31e7dd3b627f17`.
- Source theorem/proof environment starts: definition at TeX line 234, proposition at TeX line 295, proof at TeX line 327, definition at TeX line 379, theorem at TeX line 406, proof at TeX line 418, proposition at TeX line 462, proof at TeX line 469, theorem at TeX line 476, proof at TeX line 497, corollary at TeX line 514.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 83–93 | `b6e5721e1066104fe6b39472efa22470c042f7609da0853e739fe9ffc10fc64d` |
| D02 | \[...\] | 126–141 | `1117dc707a2942c9d71c1c1b51cedab7208cb84db6272035bb324565fe97f7b6` |
| D03 | \[...\] | 143–145 | `e1bc626a4df155f16c5d4fbb4d3ecb4c983ab2ca47dcfb294d0d120051c4dbe8` |
| D04 | \[...\] | 152–156 | `e9151a74a61567641220d6c06e0fd15602f0d38c3f3a6f11aba5aa4e9980b30c` |
| D05 | \[...\] | 171–174 | `f156a8f484ecb49fa25af9acd52c92ad7d8dc67a301840244ac346c6d6a87639` |
| D06 | \[...\] | 177–188 | `f751232fa05497cf4e1ebd1b6f8fd9d232941b01b1e77f55cb22dc25f33a3cfd` |
| D07 | \[...\] | 190–194 | `81d72b87cacf12e8e94291882361f85dab323ae4e602d8a7152c971ec6d451c2` |
| D08 | \[...\] | 197–199 | `b36059f7e9ec91956c70d730fd42985cdb846658b72013235bbd8d2c2ddf9a77` |
| D09 | \[...\] | 204–207 | `7797d398b6f041e2e937f30028b2e9eed95e1292def94dc4bb507bd9568438e6` |
| D10 | \[...\] | 209–217 | `a6834a571ebced7415ed8d42b9205729c3da3259f7508984aac494f6dbafbcee` |
| D11 | \[...\] | 264–271 | `859661a367a4bdac9ec6cfc015a32f2cfbaee971f4dd287f91938341bc04970b` |
| D12 | \[...\] | 280–288 | `5bfc69ac9e219e0742b8898d4677591e0fd7fb453534e07272c72956c63d2167` |
| D13 | \[...\] | 298–311 | `675568c10054efbf4b38a4aa4fed7cd10b1f14df3e2cfac6fb391f428235993a` |
| D14 | \[...\] | 314–324 | `8694524fde59d86d4ec5f67ad2eaad5b63d166249e1898f74a99c52f5b4ba6f5` |
| D15 | \[...\] | 344–357 | `f4d6557c4eb1f825f0c4a329c74eafd7ccc3112efcd23afe9b087d6037e136c9` |
| D16 | \[...\] | 382–388 | `31b688bac2f8ea79def8f2f2ef946fc5516e5c8c9310e264a93c3fdd13b2b97f` |
| D17 | \[...\] | 408–413 | `d35bc0576a77922e9cfccf5f126af9a435354b4b03ddfa0ab6b7027b0169107e` |
| D18 | \[...\] | 444–449 | `6736e56bf57539bbaf6a61cec7d94701a9ca38ae0cd7161847fb8e260f4c8e20` |
| D19 | \[...\] | 453–456 | `cd325fba1ccf0ac41160f25e57e8756830e7706a679aa85bd015dce75703941b` |
| D20 | \[...\] | 479–491 | `3a89cb6002abe5cc7f1323af013f6e408eb90644e5021b9dabc4af43cbc2b456` |
| D21 | \[...\] | 525–527 | `9e3cc4d31fea3a44e6b681e71d4128aa70b916490d914c1758bd69caf2f5a396` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 39: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 41: `\newcommand{\Bhard}{B_{h_0,\delta}}`
- TeX line 65: `the scalar-plus-eligible-tail route also remains open under its own`
- TeX line 72: `\(\Lone_{\rm actual}\) progress.  It is not a deterministic`
- TeX line 78: `minimal \(\NT\) blocker antichain and the parent-ready \(\OPEN\)`
- TeX line 104: `An \(\Lone\) theorem on an actual periodic core is not a theorem on`
- TeX line 107: `continuous logarithmic measure does not control every prescribed`
- TeX line 108: `atomic endpoint.  The scoped current-artifacts stop is not a global`
- TeX line 125: `eligible-tail-open path.  In symbols,`
- TeX line 149: `The finite archive has a canonical conservative cut shadow.  It also`
- TeX line 157: `in that exact cell.  It does not imply that an enriched`
- TeX line 258: `the certificate stale; it does not make a mathematical theorem false.`
- TeX line 279: `Separately define the parent-ready open frontier`
- TeX line 281: `\mathcal F_{\rm open}`
- TeX line 284: `\operatorname{status}(v)=\OPEN,`
- TeX line 287: `\tag{6}\label{eq:open-frontier}`
- TeX line 289: `A node in \(\mathcal F_{\rm open}\) is a live mathematical target.`
- TeX line 315: `\mathcal F_{\rm open}`
- TeX line 323: `\tag{8}\label{eq:current-open}`
- TeX line 337: `\cref{eq:current-open} are status-\(\OPEN\), have ready artifacts and`
- TeX line 363: `alternative is open, a theorem-backed typed crosswalk connects their`
- TeX line 373: `\(\mathsf{SYNTHETIC\_REACHABILITY}\) mode.  Its two file-backed`
- TeX line 374: `predicate fixtures and inline stopped-cell assumptions explicitly`
- TeX line 376: `\(\mathsf{NONE\_SYNTHETIC\_REACHABILITY\_ONLY}\) semantics; they are`
- TeX line 385: `\NT,\quad\AF,\quad\OPEN.`
- TeX line 400: `proved, and all remaining unresolved nodes are scope-matched open`
- TeX line 402: `\item \(\OPEN\): every other valid state.`
- TeX line 411: `\STOPR,\quad\NT,\quad\AF,\quad\OPEN.`
- TeX line 414: `Every result is reachable on a finite typed synthetic`
- TeX line 415: `assumed-predicate regression fixture.`
- TeX line 420: `a finite valid state.  The ordered list has a final catch-all, hence`
- TeX line 424: `it asserts none of the synthetic predicates as mathematics.`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:almost-prefix` → `../main.tex#L187` (existing project target or original TeX label line).
- Link relocation: `#eq:shadow-measure` → `../main.tex#L193` (existing project target or original TeX label line).
- Link relocation: `#eq:almost-prefix` → `../main.tex#L187` (existing project target or original TeX label line).
- Link relocation: `#eq:nt-antichain` → `../main.tex#L270` (existing project target or original TeX label line).
- Link relocation: `#eq:current-blockers` → `../main.tex#L310` (existing project target or original TeX label line).
- Link relocation: `#eq:current-open` → `../main.tex#L323` (existing project target or original TeX label line).
- Link relocation: `#eq:precedence` → `../main.tex#L387` (existing project target or original TeX label line).
- Link relocation: `#eq:arith-ledger` → `../main.tex#L448` (existing project target or original TeX label line).
- Link relocation: `#eq:arith-ledger` → `../main.tex#L448` (existing project target or original TeX label line).
- Link relocation: `#eq:physical-ledger` → `../main.tex#L455` (existing project target or original TeX label line).
- Link relocation: `#prop:blocker` → `../main.tex#L296` (existing project target or original TeX label line).
- Link relocation: `#eq:weighted-interface` → `../main.tex#L216` (existing project target or original TeX label line).
