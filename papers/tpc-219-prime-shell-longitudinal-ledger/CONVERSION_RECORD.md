# TPC-219 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `c769c4dd5af856b6d78da8e133f9938f11abb2fdec6a54b774b1b45b49ddb744`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `cb422bb42b3507deae8a42ef5f6b2061d20347c437094294cf1249f554e2ecb6`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `3cc217a8295cfa890f2aaba7a3a6b2a89e027ce0001745cdf485f88e0be87deb`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d8c34b601776e46b78d100032c26945151d5e9331b8187f328810452c0414726`.
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
| `\texorpdfstring{Why the $P$ factor must be opened}{Why the P factor must be opened}` | 47 | 1 | `HEADING_TEXT_MATCH` |
| `The labelled packet object` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Exact longitudinal/transverse theorem` | 90 | 2 | `HEADING_TEXT_MATCH` |
| `Sharp finite endpoints` | 135 | 3 | `HEADING_TEXT_MATCH` |
| `Route position and reproducibility` | 166 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 183 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 192 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `65` before writing and `65` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `7ccd6f979ba0b7bd0f867f090392cde54577929d6aa2892fa3e30f445ca9c7ad`.
- Source theorem/proof environment starts: theorem at TeX line 92, proof at TeX line 107, corollary at TeX line 128.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 32–34 | `b3cd299b45251675d3f1114cd47e9a21b3c9badf22a07ddd6e91cb6b5d8f16a7` |
| D02 | \[...\] | 67–70 | `64eeff013064c93437a9317485d903667b6b7a7b29ebecf8273a20ba86a0960b` |
| D03 | \[...\] | 75–78 | `919292b3ff19fa2227c51bc6899c2c8965d57ec343d5dc0550d63d3633bb6fcf` |
| D04 | align* | 80–84 | `fddc584355f88d322747dade172f81f9aa9e0efbd8e2c46a281661bb0f3cc709` |
| D05 | \[...\] | 94–97 | `1b6123aa30a7fd43d02523b4933dcc05417b910778d99d510d42638e8629bccd` |
| D06 | \[...\] | 100–104 | `875df3e1b615e0f7bbdd67c508c0f54e97e99d00b2d666d916bf6992dfa88e81` |
| D07 | \[...\] | 110–113 | `b28e76eb5f3a4430c2cce4154fb60bf5ce4edc5932f53d3f37649c50afc69d26` |
| D08 | \[...\] | 115–117 | `7f56de6593310887e91a63898dfc6088eca3bb41b448bf94ff9f78b149eb5f88` |
| D09 | \[...\] | 119–122 | `a077e801b1111d7c4e2d57ced7dd22d945806d4d7d4609ccd2a78993a8d9debf` |
| D10 | \[...\] | 171–175 | `0df6afd89a2cb38716948647c066fd88eef6ca197b7f202b35522404b4daf902` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 27: `TPC-218 retained the prime label in a Hilbert-valued finite-window estimate, but scalar`
- TeX line 44: `The theorem is an exact Hilbert identity; the finite fixtures are controls, not asymptotic`
- TeX line 47: `\section{\texorpdfstring{Why the $P$ factor must be opened}{Why the P factor must be opened}}`
- TeX line 49: `The previous finite-window stages control a common-source kernel after its rational`
- TeX line 54: `inherited finite-window estimate uses the standard additive large-sieve interface`
- TeX line 65: `Let $\Qx$ be a nonempty finite set of primes and put $P=\#\Qx$.  Let`
- TeX line 74: `For a finite interval $I$ define`
- TeX line 87: `$V^P$ into the constant q-direction and its orthogonal complement.  They do not assume`
- TeX line 135: `\section{Sharp finite endpoints}`
- TeX line 141: `Table~\ref{tab:firewall} records the exact finite certificate.  The vectors are rational,`
- TeX line 163: `is scoped: it does not say that the literal growing prime shell is aligned.  It says that`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:firewall` → `main.tex#L159` (existing project target or original TeX label line).
