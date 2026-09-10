# TPC-178 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [main.tex](main.tex), SHA-256 `ce5433f55fb13c127e59c6da504eac6a654c298c75eba937a8f1498404c30946`.
- Bibliography: [references.bib](references.bib), SHA-256 `f76a5bf49ac5e09a54e824120975070bfb55ce254442e5a0ed5b48ee134cfa32`.
- Preserved PDF: [tpc-178-canonical-minimal-representation-eligibility.pdf](tpc-178-canonical-minimal-representation-eligibility.pdf), SHA-256 `7a82f66f0159e5028332a3b93ac6ace96352b145d14727fd15f782ec67135bb9`; 3 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `42f317305e6af4fa307f09d14c82d73029d4cec414fe70a251f9e6bb1cbd1e8d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC175_179.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md).
- Separate proof package: `ABSENT`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Three notions that must not be merged` | 64 | 1 | `HEADING_TEXT_MATCH` |
| `A positive representation contract` | 97 | 1 | `HEADING_TEXT_MATCH` |
| `Eligibility audit` | 124 | 2 | `HEADING_TEXT_MATCH` |
| `What is preserved for a future nonempty family` | 163 | 2 | `HEADING_TEXT_MATCH` |
| `Reproducible audit and claim boundary` | 193 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 208 | 3 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 220 | 3 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `32` before writing and `32` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `fb2f85ff9e0873e6ea2e60aad9917c92f470c421d9a8a200f989dbc63c9a6720`.
- Source theorem/proof environment starts: proposition at TeX line 83, proof at TeX line 89, theorem at TeX line 146, proof at TeX line 155.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 67–69 | `29eb4fb3184e672944b274bc29b46b06e9d5ca6283d6addb0af4b9b6c39e6dfa` |
| D02 | \[...\] | 71–74 | `e7be4da5c7cabb71f7219cf932ff1fddf955484ca243356207df6a75eb1f474d` |
| D03 | \[...\] | 114–116 | `1573debab88a97545d2f5e9ec2192b75a052306c29431fedab3a6e8e1e7b0ae9` |
| D04 | \[...\] | 118–120 | `1b2eb385407032202a2f733b4068445aaa5637e46954f538c4508180abc1d4db` |
| D05 | \[...\] | 129–131 | `74bcfc2a8d923d88db1800836063bc21492a796dd90e5fffb65756f209396f71` |
| D06 | \[...\] | 135–144 | `7fe4eb0383749bd66e7e66caff2b86aecd4a482461f936a2ee4d1f6e49a5527a` |
| D07 | \[...\] | 148–150 | `59d7d9af777879f419721f8ea0ddede53e60ecddc88ade7d0e8993c8c1c9de54` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `pdfsubject={Why an archive key is not a physical representative},`
- TeX line 35: `\textbf{Why an Archive Key Is Not a Physical Representative}}`
- TeX line 75: `This is an exact finite theorem \cite{WangTPC164}.`
- TeX line 90: `The domain of (2) is \(\mathcal A\), a finite set of archived rows.`
- TeX line 109: `\item compatibility with literal coefficient, fixed-\(h_0\), and`
- TeX line 203: `The audit consumes no named fixed phase, fixed physical \(h_0=2\)`
- TeX line 211: `proved finite uniqueness here concerns addresses inside a frozen`

## Conversion limitations

- The preserved manuscript is root main.tex; this reading layer remains at paper/main.md with links back to root sources and the versioned original PDF. No source file is copied, moved, or treated as a new paper.
- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- No PROOF_PACKAGE.md is present; no proof-package review is claimed.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
