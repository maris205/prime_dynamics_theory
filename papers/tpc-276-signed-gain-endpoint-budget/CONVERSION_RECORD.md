# TPC-276 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `a200c968d1891682caf7c7b069177d4f7a40b634885e0d6234c3a07de68dc7df`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `933b30a47c672162b4d2dbf6116b77f89a01ea8fdbbc15683289f06791f5c541`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `b15d5dad815635f042ad54428b8bc0049de9e9ca89cc35740114854666164121`.
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
| `Question and claim ceiling` | 43 | 1 | `HEADING_TEXT_MATCH` |
| `Exact margin recovery` | 65 | 1 | `HEADING_TEXT_MATCH` |
| `Conditional strict endpoint compiler` | 96 | 2 | `HEADING_TEXT_MATCH` |
| `Finite signed-margin transfer` | 150 | 2 | `HEADING_TEXT_MATCH` |
| `Why the finite gain is not power credit` | 196 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and route evaluation` | 210 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 220 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `66` before writing and `66` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `80aeb8dc7c05e09fef2b687d094257fadb462428a197addcfa37b63d56afc434`.
- Source theorem/proof environment starts: theorem at TeX line 76, proof at TeX line 85, theorem at TeX line 104, proof at TeX line 131, proposition at TeX line 183, proof at TeX line 189.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 47–50 | `fd3d30924fe50553215ab83ae3de2cb585eba0336227b13c2da4d80e6dd4c674` |
| D02 | \[...\] | 57–61 | `642ab48c01aa8a0976addd35f294542e73916575bf9c1f388f6e29746fb93e92` |
| D03 | \[...\] | 69–74 | `ef204aeadf54b06eb51297e8603d5b710b787087868452146620e0f5df35a56a` |
| D04 | \[...\] | 78–80 | `ee1b6796e59de2ca49d0534cd1f8f9ba71598ed73cc29db971146f217da26996` |
| D05 | \[...\] | 87–91 | `68458117127ea26bc8b77a2c9089a925284aca4a7f2671546f3c541daee1085c` |
| D06 | \[...\] | 99–102 | `7e3de1f9c0fa6e6a7dce89623570d02a6b1bf791a60087c9732c6679eceb1cd5` |
| D07 | \[...\] | 107–111 | `633f28647d73015d3d7908dede581937e27efa3940d35faf873045d1b106286f` |
| D08 | \[...\] | 113–115 | `c551b0af1d35ab48af7d2866c926cf3074161221884b45c346e9761b023866d5` |
| D09 | \[...\] | 117–122 | `382342c39c9b40f6a364a73127621ccf41b6ac41e606f7809cb37a7241dfc440` |
| D10 | \[...\] | 124–126 | `a772ebab04dd9c02fc3550fcee6651557e1be64fa71cecf3a7e9ce46843ea3a2` |
| D11 | \[...\] | 133–137 | `e4bbe24723983ad1f2868ce15c1b768752416d9da6e1e109aaf20b7a9a2ae9dd` |
| D12 | \[...\] | 139–142 | `172817fca7d8494b64044fca7cff11be38312767608bb3c8f06910d52c349a66` |
| D13 | \[...\] | 203–205 | `4dc2db92607a5a96eb24238c1afec77ebc2e93b94a983a91935117fb792bb95d` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 30: `packets and found a finite diagonal-to-signed energy gain`
- TeX line 34: `endpoint compiler then shows that a uniform source-level gain`
- TeX line 39: `margin threshold, and five above the eighth threshold.  The finite table is not`
- TeX line 59: `\texttt{PROVED\_EXACT\_FINITE}\;+`
- TeX line 60: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}.`
- TeX line 62: `No finite ratio is promoted to a power saving, and no arithmetic \(L^2\) or`
- TeX line 143: `Because \(\meff\geq0\), the assumed scalar bound is no larger than the same`
- TeX line 150: `\section{Finite signed-margin transfer}`
- TeX line 183: `\begin{proposition}[registered finite counts]`
- TeX line 196: `\section{Why the finite gain is not power credit}`
- TeX line 199: `\(\Dpack/\Gpack\geq b x^\gamma\) for all sufficiently large \(x\).  A finite`
- TeX line 202: `the finite table proves a useful threshold recovery but assigns`
- TeX line 206: `This is a scoped finite-to-asymptotic obstruction, not a negative theorem about`
- TeX line 207: `the literal growing source.  The missing result is a uniform source-level`
- TeX line 215: `with half its exponent.  The finite literal audit recovers the quarter margin`
- TeX line 216: `on three rows and the eighth margin on five rows, but it does not establish a`
- TeX line 218: `\(L^2\), full Gate B, and the twin-prime conclusion remain open.`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
