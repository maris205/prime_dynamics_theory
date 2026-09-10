# TPC-218 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `c586e5f72db4753b30f2081ac3cea94da6363834bc816439c8f96f0c0619b904`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `d048dae4cd984abe82f4383fcb0cbc4039b9ae0da720214f905e7239e341f689`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `7f967e96466b67e32a3b2447e53f8720b0bf2852384c10974fa271c2794afba2`; 6 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b95c9b17fc83c5ca378005f5839c10b2b9878edcd4337aa7a8c3ba353713d1fd`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC215_219.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `The split common-source object` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `The inherited reduced-frequency identity` | 177 | 3 | `HEADING_TEXT_MATCH` |
| `The Hilbert-valued finite-window theorem` | 190 | 3 | `HEADING_TEXT_MATCH` |
| `Scalar recovery and the packet Gram` | 297 | 4 | `HEADING_TEXT_MATCH` |
| `Adversarial controls` | 336 | 5 | `HEADING_TEXT_MATCH` |
| `A P-saturating prime-label fixture` | 338 | 5 | `HEADING_TEXT_MATCH` |
| `A packet-projection alignment` | 355 | 5 | `HEADING_TEXT_MATCH` |
| `Route position and reproducibility` | 385 | 6 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 401 | 6 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 423 | 6 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `118` before writing and `118` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `30`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `2b5abfdc57550c00118782565eb71b0638fceec853aa2422c9a484b02b739511`.
- Source theorem/proof environment starts: lemma at TeX line 192, proof at TeX line 202, lemma at TeX line 214, proof at TeX line 223, lemma at TeX line 241, proof at TeX line 254, theorem at TeX line 264, proof at TeX line 281, corollary at TeX line 299, proof at TeX line 309.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 44–47 | `2f5f707927b8027fff44dab1db8881df556fecda923be77dda5cd93f4c550c90` |
| D02 | \[...\] | 81–84 | `9ed58102c4e199e92aa855b7f53001830a3a60daaf0cab49181e175368cb92c1` |
| D03 | \[...\] | 86–89 | `3993e7875b3ba4b6eea9de211a6e0566b0949fae9c3b8631fe7e70c30ee046a1` |
| D04 | \[...\] | 91–93 | `021ed54e14749eed14a68278a2fbbcb1306323ee22c084283ca1c107cb017742` |
| D05 | \[...\] | 99–101 | `749bf42bef7fd9e79186c7a51963e7f30fa7b77eadd7274e822d4b1c29c1518c` |
| D06 | \[...\] | 121–125 | `1af4f9f6432457604da5f0429ccc2dc978a5c2d417a46d2e1b25aa8d29abacdf` |
| D07 | \[...\] | 132–134 | `fa926963707a7a9316200da80e274e422c893274f0d52e1386c6c4c2d733b9d7` |
| D08 | equation | 136–143 | `e54b8c3f2df69d56f59b57cbc137313d26678b1eb0dcdefd9d5a0b7ea991699d` |
| D09 | equation | 146–150 | `9fe0d300488dcdee724cdea377bc9592de8dba12a5187aac8ae2656a60c98109` |
| D10 | equation | 152–159 | `0fad3923e4d503b5361281e45ef22b8a1fe64278b97c4051382ede5a405b3954` |
| D11 | equation | 161–164 | `e9fdbcf1dd7f68ac07e7d1a129fd92d779c68e71662778361e5636f1d319a3a6` |
| D12 | equation | 167–173 | `bf52b40081b9a0e9344dc3f4dbbfba24ccd3c2fe20455955997c6edf8242e706` |
| D13 | equation | 180–184 | `880ae2be0c702731828114a594d1bfdcc8fb37ecc1fba8f4968383d836d55eea` |
| D14 | \[...\] | 195–199 | `10d325c0066abe788ad24b435446071846056d8da21483133a18ea4530b2babd` |
| D15 | \[...\] | 205–208 | `393dfe9e1449f00b2d3316414a519d352d7097fc83c0627e96960494a8c955ef` |
| D16 | \[...\] | 217–220 | `144ea426cb0856f9e64b99e4aee1bff3e068f3e0b8efa1ef950f9804dc15c5bd` |
| D17 | \[...\] | 227–231 | `dc308704b5f10efebc4bcc1430feddc504344885c8d76a581bd790aecfc16e9b` |
| D18 | \[...\] | 233–237 | `ac121903c71467dfd3a92ad13ea3953db6f897f9a6b92727c46219cd4910f9de` |
| D19 | \[...\] | 244–251 | `189ee706f6cb71bc6136a779eaa71f37fa13da872fad11589aba23608487755b` |
| D20 | \[...\] | 267–271 | `660e672b2d6dbf93e477e3ef431559de48fb639557aebff8b1d7f4b5259209db` |
| D21 | \[...\] | 273–277 | `923465f953cbde81f641986d6cfe9ddc7d268a0d231896a281795ae548c1ece0` |
| D22 | \[...\] | 283–292 | `285fcd2ce702f79bd7b4d93288457e9a641853bb1076fdfb6339b44685a48afd` |
| D23 | equation | 302–306 | `8fb74e5d707820a730b338ea8b38ef45f0f62597dedd413bf3dba3720500374b` |
| D24 | equation | 317–320 | `12a3af4d203f556fab84b4b790a342824cf1b024f5bebb5c7af360505125aa5b` |
| D25 | equation | 323–327 | `6966f61fc1fdbff8885e3cae62454f3ec9fa0d5ec4d47ed88de762aa38f536f4` |
| D26 | equation | 329–332 | `373f3898f031498cf49fadaddc83f98bd120dc7db7bbd31297f5f0de57ba4f77` |
| D27 | \[...\] | 341–344 | `54961461c001fbdb3b3bb3a9dbda2939b2c6f9fef4186918348c6e6c41506c9e` |
| D28 | \[...\] | 347–350 | `679eed30bc825ab978d582c9fe3fd15d8ef9531b18f4d6df0e25c512c0242999` |
| D29 | \[...\] | 359–362 | `0d17b4555e54e1310f72d9eee28ec5761178ddef0d500373ba019b0e1572e7eb` |
| D30 | \[...\] | 410–412 | `03c5ba98f38e64411af69a68ecdad2bd1d476e4ec62d69c4043068d7c27f14e9` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 39: `kernel to a finite interval by a reduced rational-frequency large sieve, but`
- TeX line 40: `it collapsed the prime shell before the finite-window estimate.  We retain the`
- TeX line 49: `$M$ is a uniform profile bound.  Recombining the prime labels costs exactly`
- TeX line 51: `$x^{11/32}$.  A finite aligned fixture attains the full ratio $P=4$, while a`
- TeX line 54: `collapse barrier; it supplies no arithmetic cancellation, $L^2$ advance,`
- TeX line 61: `declared common-source hypotheses.  The finite fixtures are exact structural`
- TeX line 67: `place where a collective estimate is required.  The recent finite-window`
- TeX line 71: `collapsed the prime shell before invoking the finite-window inequality.`
- TeX line 74: `and the four-packet label be retained in the same finite-window object?  This`
- TeX line 78: `measure exactly what the structural argument does and does not provide.`
- TeX line 108: `\item an exact prime-label- and packet-label-preserving finite-window`
- TeX line 112: `\item a positive-semidefinite packet Gram formulation compatible with exact`
- TeX line 126: `The result is a structural bridge to the next open theorem.`
- TeX line 179: `The divisor-dilation identity from the preceding finite-window stage is`
- TeX line 188: `not an orthogonality assertion.`
- TeX line 190: `\section{The Hilbert-valued finite-window theorem}`
- TeX line 316: `For a finite interval define the packet Gram matrix`
- TeX line 321: `It is positive semidefinite, and Corollary~\ref{cor:scalar} is a trace bound.`
- TeX line 333: `The trace inequality is unsigned and therefore does not supply the signed`
- TeX line 351: `so their ratio is $4=P$.  This is an exact rational finite structural`
- TeX line 365: `cancellation.  It is not a claim that every literal TPC profile realizes this`
- TeX line 379: `Prime shell / four packets & \texttt{OPEN}\\`
- TeX line 380: `Full Gate B / strict one-over-400 & \texttt{OPEN / UNPAID}\\`
- TeX line 391: `the finite $P$-saturating row alignment.  The open theorem is a signed`
- TeX line 396: `optimized-mode checks, and a separate adversarial script.  The finite`
- TeX line 406: `$P\leq2Q$ payment and returns the TPC-217 exponent $11/32$.  The finite`
- TeX line 417: `finite-window normalization.  In particular,`
- TeX line 420: `\texttt{TPC218\_FULL\_GATE\_B=OPEN}.`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:row` → `main.tex#L142` (existing project target or original TeX label line).
- Link relocation: `#eq:coeff` → `main.tex#L149` (existing project target or original TeX label line).
- Link relocation: `#lem:inject` → `main.tex#L193` (existing project target or original TeX label line).
- Link relocation: `#lem:hilbert` → `main.tex#L242` (existing project target or original TeX label line).
- Link relocation: `#eq:scalar` → `main.tex#L163` (existing project target or original TeX label line).
- Link relocation: `#thm:split` → `main.tex#L265` (existing project target or original TeX label line).
- Link relocation: `#cor:scalar` → `main.tex#L300` (existing project target or original TeX label line).
