# TPC-251 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `73a85534ef1f34ed52b1e18bbddb15980c0d8af9a6191aaa1d7dbc5b327177c7`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `06fc55b836ea2db1f03372026ca13cdac7bba45595a6c6070bca908fac03b524`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `6a51fdc64ef8b6dbe4578c69a8f0dc07e44c9370264f71cc588f93b0c2a1d180`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `e975da64928ff3f5ef2bcf5151e4fb620dab8467c4177dc6726da4710ad320b3`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC250_254.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Source lock and scope` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `The declared-block compiler` | 77 | 1 | `HEADING_TEXT_MATCH` |
| `External margins and the strict endpoint` | 148 | 2 | `HEADING_TEXT_MATCH` |
| `Exact finite operator replay` | 192 | 3 | `HEADING_TEXT_MATCH` |
| `Computational trust boundary and limitations` | 251 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 281 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 294 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `96` before writing and `96` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `20`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `4401c4e8989b1e6df99d72134b4351cccc33a471b48d8136a7a0a17e110c87eb`.
- Source theorem/proof environment starts: theorem at TeX line 106, proof at TeX line 125, corollary at TeX line 150, proof at TeX line 160, proposition at TeX line 172, proof at TeX line 186.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 51–53 | `f427226ecdcb105303d94f97cc01a9d6d0288c6829e154bc78ff0715ad1230fb` |
| D02 | \[...\] | 57–60 | `26d8e887c0ce1067959849a131a988e3ebebaebd0ba38aa40a01cbaf1f7c53e9` |
| D03 | equation | 62–65 | `72fd3a9bb361a9c71ef531d0faa2023d8035aa03f9a6fb24af0a972526b58adf` |
| D04 | \[...\] | 69–71 | `2cb03a59b7783f677da7ccbf33228076dadcfcd222c51f28df0a403c429c1ff2` |
| D05 | \[...\] | 80–83 | `06769a5260053599339b389b552697820a90e35d3f5ee182249c0e2a59b75c6d` |
| D06 | \[...\] | 85–89 | `ee96b8915e930da71e7d7e74ebc8fd63f8d49a347bc744cc2dbefd4e68ead3ac` |
| D07 | \[...\] | 92–94 | `8d2d1d3aaefaf2a2946cee16f54e4b26e3345efe5da57b07e2d313b6e9938c92` |
| D08 | \[...\] | 96–99 | `61a52ce098c63c14aa71da9a28e1c1e920293c3541fe9e6b87b201126b36e247` |
| D09 | equation | 102–104 | `478239ed27fbbdbcda78702b83e626b14369858a8867bbbf0eba390fb8000772` |
| D10 | align* | 108–113 | `278679ea1c8ec0c89918a3475fbbe894b1ce2f7aa8cd0cbbb9d76e88e6ec1a7a` |
| D11 | equation | 115–118 | `f407c42022819120409abc8f67a3c022035de92af67aff898d1eedf49c3e09f1` |
| D12 | equation | 120–122 | `d874d31e0e690cb13b4830d34d9c6be0ccddd9bc7bde244d9bb768eb823772cd` |
| D13 | \[...\] | 129–131 | `fedb106728c585b2fa1168f1d8ac82b1ff61b1ef3d550cb699f9f11cf6ce8da7` |
| D14 | equation | 153–156 | `a0e5630fd2843f8c3db0a2b29f6472b56ef9791d0f3ac95de9f78cfdf6480ae6` |
| D15 | \[...\] | 174–177 | `644942b859055453be53fe65d9768fcd1d571efbc87948e1e2be22350c06d7a4` |
| D16 | \[...\] | 179–182 | `1d69537fc7f30cbc008ca55a89e21ec8ee75a8f1fe5ba5e4d9e01d07529c00f9` |
| D17 | \[...\] | 197–201 | `c9d39ccc7ddead171b046666b148275a1015b57c7f83fa1f271d908faf1430eb` |
| D18 | align* | 203–208 | `e31dbbeb9aaca8e02203f8d56864ac412750c9fc3053035daaa72b353ba7eba5` |
| D19 | \[...\] | 210–213 | `73995cc4aea50f2b5b4965422cc84e6d9e4b0dad4b44987ade5cccd7078bd875` |
| D20 | \[...\] | 234–237 | `4d25fdd8d1d8ea85a81a0da1c8d671909f8ea0dc18ba23a76c45c2727c7549bf` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 48: `Let $H=\C^I$, where $I$ is finite and nonempty, with inner product`
- TeX line 72: `This unit is canonical only relative to $J_c$.  It is not a V59-canonical`
- TeX line 74: `These distinctions prevent the finite decomposition below from acquiring an`
- TeX line 144: `The theorem is a pointwise enclosure for fixed source data.  It does not`
- TeX line 169: `paper does not obtain it automatically from the conditional synthesis`
- TeX line 192: `\section{Exact finite operator replay}`
- TeX line 226: `\caption{Exact projected data for the synthetic finite operator replay.  The`
- TeX line 241: `\emph{synthetic exact finite operator replay, not a literal V59 arithmetic`
- TeX line 259: `Python modes.  None of these finite checks proves an asymptotic statement.`
- TeX line 271: `longitudinal dominance are open.  Arithmetic advance is no; fixed-atom credit`
- TeX line 272: `is zero; L2 and the twin-prime result are none.  Full Gate B is open, and its`
- TeX line 289: `conditional, and the actual arithmetic margin remains open.  There is no`

## Conversion limitations

- 4 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:literal` → `main.tex#L62` (existing project target or original TeX label line).
- Link relocation: `#eq:chain` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:gram` → `main.tex#L120` (existing project target or original TeX label line).
- Link relocation: `#eq:upper` → `main.tex#L102` (existing project target or original TeX label line).
- Link relocation: `#eq:chain` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#thm:compiler` → `main.tex#L106` (existing project target or original TeX label line).
- Link relocation: `#eq:external` → `main.tex#L153` (existing project target or original TeX label line).
