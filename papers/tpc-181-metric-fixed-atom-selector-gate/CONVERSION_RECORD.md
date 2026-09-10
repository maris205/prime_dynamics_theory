# TPC-181 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `460c5255e7fa4513f3e120e634d2e27229635e6a1f40b3cfa8ddf3a3229b2fa9`.
- Bibliography: [references.bib](references.bib), SHA-256 `f9202753caaee1b490e542b6c5b63a3ea88086be409235d99419be59529153d0`.
- Preserved PDF: [tpc-181-metric-fixed-atom-selector-gate.pdf](tpc-181-metric-fixed-atom-selector-gate.pdf), SHA-256 `37b0704cc33fc2cd1299bbdf16c83cd265fb8b2547f1db60b457a7da310ceb57`; 5 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `727fd9172b5e3bf6aa625fea64e572330969af6702d1b717424ce8c204593b95`.
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
| `The imported metric theorem` | 87 | 1 | `HEADING_TEXT_MATCH` |
| `The two independent missing inputs` | 160 | 2 | `HEADING_TEXT_MATCH` |
| `The singleton obstruction` | 205 | 3 | `HEADING_TEXT_MATCH` |
| `Selector verdict and sufficient bridge hypotheses` | 274 | 3 | `HEADING_TEXT_MATCH` |
| `Return to the two pointwise routes` | 304 | 4 | `HEADING_TEXT_MATCH` |
| `Level ledger and reproducible audit` | 365 | 4 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 390 | 5 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 403 | 5 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `61` before writing and `61` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `18`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `6964f75f85889a2e087f52578f9bf18ca6e8abfedc61bf20a26fbe1580d03c16`.
- Source theorem/proof environment starts: definition at TeX line 184, proposition at TeX line 207, proof at TeX line 214, corollary at TeX line 224, proof at TeX line 230, theorem at TeX line 245, proof at TeX line 264, proposition at TeX line 330, proof at TeX line 338.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 92–98 | `bbacc9351ab62fb5824c7682728204054492a14a3f5e4e3217c4c015b01f0452` |
| D02 | \[...\] | 100–103 | `6e3f580ab756c95557632148ce5bf8893616c9b1f3e6df7670b33511c11ed256` |
| D03 | \[...\] | 105–112 | `60c290989211e1bc8fe6e4368d5badc508dd7395b7938bc4e8faa345dfc3563c` |
| D04 | \[...\] | 114–121 | `9d94354acd87ed0f0889acf773ce879ebb2ff1dedf301b05cfb7ab899e63fd53` |
| D05 | \[...\] | 123–127 | `b309603498db3d82b52b71cd80603edd1270eed005cf7547014a5ec19238b8cc` |
| D06 | \[...\] | 129–132 | `4b5efa26dae34fd452094c926ce124098b5ad1a4ecebf6ce093c5759cecb798e` |
| D07 | \[...\] | 138–141 | `417952adc99b59157779ae8e16e69dd79e3e65917f6903d48868010c7ac56910` |
| D08 | \[...\] | 143–155 | `b29d2a3c779e6987403062ec7c42686de5fdcefe5e4ae4690dbbd20bb59ba528` |
| D09 | \[...\] | 163–170 | `0dce82c82db36aa6c63f47e1a46ecd32c4508bf7e50d2f60fc99917509562b3f` |
| D10 | \[...\] | 176–179 | `fbc4ef846fbce40d1ea73e4e0ae9398aad3a06f591d41fd87564570a9722985a` |
| D11 | \[...\] | 216–218 | `c130c26209ca7e53a08146226e23c86806f9a610a3d706f85923c42ec5c88980` |
| D12 | \[...\] | 232–234 | `81c737802bb75025d9af9a24af40fc72a5ff5e77392bad29d17bd2ab33a78ff9` |
| D13 | \[...\] | 248–253 | `c45accef2a8ed61ee38fabe0892434b70caeeb6f18c27bdef5e5a1d587723428` |
| D14 | \[...\] | 256–259 | `24d43e942f51845d07562d1e9e46c41897adb34b3942c3527615f182d8cdb6f8` |
| D15 | \[...\] | 280–288 | `5e31ff3b29b827ddb52d349849b432fc20514b96e34e0c74c0754779fd4f4da3` |
| D16 | \[...\] | 307–317 | `1b8b69d4a1acc4ee0b5d4de54d6938fd6986e2089cdcc607056e84e30a2b4f6e` |
| D17 | \[...\] | 319–328 | `6283935d75d893a48af17bd71ae38bfc7e158a023c51f55bfe3f194d60b4fef9` |
| D18 | \[...\] | 350–363 | `113dc56ff7f14df184570fafc07b1aa5bba86fe99e018876a7f6a0e0bb069923` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 32: `\newcommand{\OPEN}{\textnormal{\textsc{open}}}`
- TeX line 55: `schedule.  TPC-180 shows that the frozen source corpus does not yet`
- TeX line 61: `\(\operatorname{meas}(\limsup E_n)=0\).  It does not prove that a`
- TeX line 71: `additive-twist routes remain parent-ready and open.  This is a`
- TeX line 72: `rigorous \(\Lone\) quantifier obstruction, not a program-positive`
- TeX line 80: `through the prescribed schedule; it does not identify a named atom.`
- TeX line 81: `The scoped nonimplication below does not prove a large literal`
- TeX line 157: `followed across \(n\).  It does not change the almost-everywhere`
- TeX line 171: `The fixed-\(h_0=2\) data fact remains proved, but is not a phase value`
- TeX line 199: `A source hash certifies only identity.  It does not prove item (iv).`
- TeX line 207: `\begin{proposition}[Full measure does not select a singleton]`
- TeX line 227: `\(\alpha_\star\), does not imply \eqref{eq:avoid}.`
- TeX line 306: `TPC-171 and TPC-172 keep two targets parent-ready and open:`
- TeX line 332: `The scoped stop in \cref{thm:stop} does not change either element of`
- TeX line 334: `\(\mathsf{OPEN\_PARENT\_READY}\), and it does not stop or reroute an`
- TeX line 357: `\mathsf{OPEN\_PARENT\_READY}\\`
- TeX line 359: `\mathsf{OPEN\_PARENT\_READY}\\`
- TeX line 370: `and finite mutation diagnostics;`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:En` → `../main.tex#L120` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:limsup` → `../main.tex#L131` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#prop:singleton` → `../main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#prop:singleton` → `../main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#def:bridge` → `../main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:bad-implication` → `../main.tex#L252` (existing project target or original TeX label line).
- Link relocation: `#def:bridge` → `../main.tex#L185` (existing project target or original TeX label line).
- Link relocation: `#eq:registry` → `../main.tex#L169` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#eq:avoid` → `../main.tex#L178` (existing project target or original TeX label line).
- Link relocation: `#thm:stop` → `../main.tex#L246` (existing project target or original TeX label line).
- Link relocation: `#eq:pointwise` → `../main.tex#L316` (existing project target or original TeX label line).
- Link relocation: `#eq:bad-implication` → `../main.tex#L252` (existing project target or original TeX label line).
- Link relocation: `#prop:singleton` → `../main.tex#L208` (existing project target or original TeX label line).
- Link relocation: `#thm:stop` → `../main.tex#L246` (existing project target or original TeX label line).
- Link relocation: `#prop:frontier` → `../main.tex#L331` (existing project target or original TeX label line).
- Link relocation: `#eq:power` → `../main.tex#L140` (existing project target or original TeX label line).
