# TPC-279 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `550d0e7ec972aa60ef429c9396eb5f27aad2d482fad404d27141d1cb80f76f3c`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `ebf609c372f1e516a040f285b8fe6390762c2b210995da6429c1b785eb814653`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `8f03c1dd47f3262ddc54ac87f8f360b88ab62ca23b0fb44abe2471cf26b7f2e8`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC275_279.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Motivation and notation` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `The exact deficit criterion` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `What pairwise coherence can and cannot prove` | 118 | 2 | `HEADING_TEXT_MATCH` |
| `Sharp adversaries and near cancellation` | 173 | 3 | `HEADING_TEXT_MATCH` |
| `Transfer of the TPC-278 source rows` | 197 | 3 | `HEADING_TEXT_MATCH` |
| `Route consequence and claim firewall` | 239 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 272 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `119` before writing and `119` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `16`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `80e41ea811b4bb8481296019ff7c7d825e3e8874165da8ad8e8eed7f2469b933`.
- Source theorem/proof environment starts: theorem at TeX line 65, proof at TeX line 84, corollary at TeX line 108, proof at TeX line 113, theorem at TeX line 128, proof at TeX line 145.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 46–50 | `37b247061ff506c44d3338f4c7ca24acc94d765eb02f5e0e3909fb9956a37753` |
| D02 | \[...\] | 58–61 | `96aa7273209e784c628f980ada275be6b97bedcc3a7aa79bc2ceb88b051b1a95` |
| D03 | \[...\] | 67–69 | `4e63722a2dc5dd52b7ae40bba401480bbe214d32ac4d95aa42f906e06450f886` |
| D04 | \[...\] | 71–73 | `2555be3eb6da8d70f10e16a3ffdd3c56232a0421a4838fc0967237a9fade5883` |
| D05 | \[...\] | 75–81 | `a72c9643f5cdf2da5d6bc72cda65439061aab77f2a0b59029752d2a765f9435b` |
| D06 | \[...\] | 86–88 | `767e7e9fadc4bc82da5fba8511ed54cf38236c18fa9f7f986e3e75c1147d1923` |
| D07 | \[...\] | 90–93 | `20bbb5bba535358ad1b55900b0a40ffa1fa4bbf3352b43c7d4caf347ee852678` |
| D08 | \[...\] | 121–124 | `eb2eb91c574ce16fd0e4261a23c82b472f95902b6c62adc20d3f51db27492bf7` |
| D09 | \[...\] | 130–133 | `3eabc7497f7a56d8ffcfc6609f99340a406c543a1bd74d972a784f461c900df7` |
| D10 | \[...\] | 135–137 | `4810b5c914e4f2e0eb9340eafc1a89194d66737f58fd1b2491093678575ad854` |
| D11 | \[...\] | 139–141 | `a267d19062c6e509518cac34a46fbf010d4ab7633eab4a8f9d9a9d262df74df6` |
| D12 | \[...\] | 148–151 | `fb7cd229f189475f5970251700413f232c7c9a3710cff2c80c7f32ae3555dc30` |
| D13 | \[...\] | 157–159 | `574f683b9759daf3b961abdb91dac2b7f7141c05e214891cc7c1a8206aedc710` |
| D14 | \[...\] | 182–184 | `4795404303b17a736fc33e045550b253e148423f80d1f0f95c58654995466b66` |
| D15 | \[...\] | 186–191 | `64e11e2ed713dda1fae1b463701f1281530087a1aa91621ae5bfd16fa3b1573d` |
| D16 | \[...\] | 244–248 | `80700333d01d4cdea8a70ec6eac74bc40f88fc61e74805190404bde76d20426d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 24: `a nearby finite shell or clock choice.  This paper isolates the exact`
- TeX line 25: `finite-dimensional input that a growing source theorem would have to provide.`
- TeX line 52: `an eight-row finite source scan.  TPC-278 then varied only a declared shell`
- TeX line 53: `endpoint or clock and found four finite sign flips.  Thus the next useful`
- TeX line 57: `Throughout, assume $D>0$.  When $G>0$ write`
- TeX line 108: `\begin{corollary}[sign is not a power estimate]`
- TeX line 167: `The envelope is useful as a ceiling, but it is not a signed source theorem.`
- TeX line 168: `At $\mu=0$ it gives $r\geq1$, not a positive power.  More generally, any`
- TeX line 169: `uniform bound on $\mu$ leaves $1/(1+3\mu)$ at constant scale.  The missing`
- TeX line 170: `quantity is the signed aggregate deficit $\Delta$, not an absolute pairwise`
- TeX line 233: `matching the parent cross-sign census.  It does not create a growing`
- TeX line 234: `quantifier: the finite values merely illustrate the exact coordinates and`
- TeX line 254: `This paper proves a finite-dimensional theorem and certifies a coordinate`
- TeX line 255: `transfer only.  It does not estimate the arithmetic coefficient, prove an`
- TeX line 267: `\texttt{ARITHMETIC-L2 / FULL-GATE-B} & open\\`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
