# TPC-277 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `225edf5e32a3a90ca64da6f3a05ec312dff962cb`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `e3fb31133af4861318ce1c96f976c46078c21f5edfe501fb636928071280112f`.

- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `8ee6a1753a9e4be804ea06af96dc2586566b2a340836b901bb3f46314a2f09ec`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `96d373b873a2825c946c3808b0a4c903b67cabf0a197c060271c986eb4f8905a`.
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
| `Question and frozen object` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `The geometric floor` | 56 | 1 | `HEADING_TEXT_MATCH` |
| `The cancellation coordinate` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `Exact source scan` | 128 | 2 | `HEADING_TEXT_MATCH` |
| `Implications for the endpoint ledger` | 165 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and route evaluation` | 174 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 193 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1605305b56b4e9c2158a17f65e04670757da64f4a8cf290ce44141cce72b0b30`.
- Source theorem/proof environment starts: theorem at TeX line 70, proof at TeX line 79, proposition at TeX line 113, proof at TeX line 118.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 60–63 | `f4fa73d8f5a6f3563e9557ad1e6600358cf18d72b73204f9e50944e79bf2ac6f` |
| D02 | \[...\] | 65–67 | `bb8ea51330e4cbea87af5a70dc5ec9f076df607bf782bcdfe565de8b9de2f836` |
| D03 | \[...\] | 72–75 | `27cf2385edf5d07d60e6f25f23680906da6c8c5c6d711677d186157a86fa5e74` |
| D04 | \[...\] | 93–95 | `01753e613a326da7cded660c8ea7f80d078476e9e8ee74549e08416a636f0952` |
| D05 | \[...\] | 97–101 | `de486f32fffc8ef5dfd035354576cd1c6b4f01b9b747739f90f6a8b32a7dfae4` |
| D06 | \[...\] | 104–107 | `dbd177655b898beab0178902329c37784a3e975a2b3053a976f77769be952217` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 37: `The result is a reusable geometric floor and a finite source diagnostic, not`
- TeX line 45: `that their signed energy can improve a margin, but left open whether the`
- TeX line 52: `TPC-268--275 chain.  No synthetic packet is introduced.  The new finite rows`
- TeX line 53: `are a declared extension of the same computation; they are not a claim about`
- TeX line 123: `This proposition is not an assertion that the literal prime source is`
- TeX line 159: `$r<101/100$.  Consequently this finite registry refutes the stronger`
- TeX line 160: `one-percent floor as a scoped finite claim, while retaining the weaker`
- TeX line 170: `estimate for the reassembled packet sum.  The finite source rows are useful`
- TeX line 178: `precise: geometry alone cannot provide a positive power, and the finite scan`
- TeX line 185: `\texttt{ROUTE-A} & not applicable to this finite gain-floor audit\\`
- TeX line 186: `\texttt{ROUTE-B} & yes, scoped source-gain floor and finite attack\\`
- TeX line 188: `\texttt{ARITHMETIC-L2 / FULL-GATE-B} & open\\`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
