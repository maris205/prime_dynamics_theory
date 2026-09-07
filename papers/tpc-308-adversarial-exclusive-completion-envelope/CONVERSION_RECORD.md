# TPC-308 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ed725e6537012bd17a32d061d9d8e6dd3b253613`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `2af3c502146e1ab3e96505b5b173581e687b0baa38f89ec956471a3d75bc7a9c`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `6ea093796d842a34070a4c606f032f4bb690fe4fffa51bbb68903a472395f67d`.
- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `242163dd79d794d11c8789fb588fa3eceb63e05e0e74119c0cd0f734f5d829f3`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c4ed964ead47ca9e2a5a050c6f70d8e7aa95cd76aebb86a2c448fff0b45311d6`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC305_309.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and frozen parent object` | 41 | 1 | `HEADING_TEXT_MATCH` |
| `Completion envelopes` | 80 | 2 | `HEADING_TEXT_MATCH` |
| `Numerical protocol` | 161 | 3 | `HEADING_TEXT_MATCH` |
| `Results` | 187 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 245 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 276 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 287 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `90` before writing and `90` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `1a10b85ea17e29be53f0b592e126ca168c577eb05e960da41a72ae031dd99501`.
- Source theorem/proof environment starts: proposition at TeX line 103, proof at TeX line 114, proposition at TeX line 141, proof at TeX line 148, remark at TeX line 154.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 65–67 | `7a902f879b6e40b391aeb8aa2d02b3abb67255089091a4506038a4d6a6d331df` |
| D02 | \[...\] | 84–86 | `d7794f05fa1f354adede153f660f34ad051a3eae946e928851b06de38ea3ced9` |
| D03 | \[...\] | 89–95 | `41d275093abfa660442e9de680b40788a55814f304f21ce3876f4e807aa38ec6` |
| D04 | \[...\] | 98–101 | `7a1c00bc7f131b80550509be6310fab31ce2a7cc8c8f86aaefbad0a4f3804a81` |
| D05 | \[...\] | 106–109 | `ea76889f31f630ceed5253512a1a7d146bc57dd79b003641ef3a7a19f0299518` |
| D06 | \[...\] | 132–136 | `9565afd10e36f4690d7c186173743888e6c8a8fae093beced3f7a1a2ef51cfe2` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 21: `The common-ambient union-shell holdout of TPC-307 exposed three finite`
- TeX line 29: `finite facts.  On the locked 18-cell twin-prime diagnostic spine, the`
- TeX line 34: `kernel exponent one.  The envelope therefore attenuates but does not remove`
- TeX line 35: `the finite obstruction, while widening several cells into the unresolved`
- TeX line 37: `enclosures, not a directed-rounding certificate.  No causal, asymptotic,`
- TeX line 45: `the exclusive pieces as withheld holdouts \cite{tpc307}.  Its finite atlas`
- TeX line 49: `minimal next question is therefore adversarial and finite:`
- TeX line 83: `the finite Hamming ball`
- TeX line 103: `\begin{proposition}[Finite envelope algebra]`
- TeX line 119: `unique.  This proves the bijection and (2), so the finite list contains all`
- TeX line 150: `$a/b\in[a_-/b_+,a_+/b_-]$.  Apply this to the right and left finite loss`
- TeX line 155: `The completion ball is a set of adversarial diagnostics, not a distribution`
- TeX line 156: `and not a model for how arithmetic labels are generated.  In particular,`
- TeX line 157: `(1) does not create causal separation between the physical operator and the`
- TeX line 175: `is padded by relative radius $10^{-5}$.  The independent checker does not`
- TeX line 181: `This separation supports numerical reproduction of a declared finite object.`
- TeX line 182: `It does not support a formal interval certificate: neither the physical`
- TeX line 184: `rounding.  The exact statements are therefore limited to the finite`
- TeX line 236: `does not support a claim that the native discordance is wholly an artifact,`
- TeX line 240: `The same finite replay produces seven unresolved cells at radius two.  This`
- TeX line 241: `is not a defect in the decision rule: broad extrema genuinely straddle the`
- TeX line 247: `The strongest positive result is an exact, auditable finite stress protocol:`
- TeX line 249: `specified finite completion set, and the extrema and candidate counts have`
- TeX line 260: `\item A finite Hamming envelope is not a probability law, a causal`
- TeX line 264: `\item No arithmetic $L^2$ estimate, fixed-power credit, uniform growing`
- TeX line 272: `the finite profile prefix around the selected $k$ on the surviving cells.`
- TeX line 282: `the project README.  All empirical statements in this paper are finite`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:radius` → `main.tex#L197` (existing project target or original TeX label line).
- Link relocation: `#tab:pair` → `main.tex#L217` (existing project target or original TeX label line).
