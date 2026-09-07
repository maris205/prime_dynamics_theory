# TPC-307 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ed725e6537012bd17a32d061d9d8e6dd3b253613`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `69d133a8364f1cf7414d49db097d8e4440b3318a2edae3919657a45e4eb013bb`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `2db3c33475450a6e074be507b6232250f6567fac398b0e9f7c84d0e8db248595`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `fc0a30567dc3231b4863440517824136f8fc9a7dfbf4b95e4f8a32abded74ca4`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `fd9ff9cb207f793989993249b6fa13fbe9f945fc10c0cfc4be3c3eabbfa2281a`.
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
| `Motivation and frozen object` | 38 | 1 | `HEADING_TEXT_MATCH` |
| `A directional holdout protocol` | 69 | 2 | `HEADING_TEXT_MATCH` |
| `Finite replay and obstruction` | 143 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and route status` | 192 | 3 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 215 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 224 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `79` before writing and `79` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `6`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `3f61fc059a50e01f7468e30bc7fc2bafce213dec425ca3c9a7785de9affaa3c1`.
- Source theorem/proof environment starts: proposition at TeX line 107, proof at TeX line 112, proposition at TeX line 121, proof at TeX line 126, remark at TeX line 135.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 54–56 | `7a902f879b6e40b391aeb8aa2d02b3abb67255089091a4506038a4d6a6d331df` |
| D02 | \[...\] | 60–63 | `20fe4742c0f18dd3feee3346631f33cf8784a004e3a910d788abd2b4c4499436` |
| D03 | \[...\] | 73–78 | `07a00565023628781f0cf6745b925c6b39c26145e4a03887d4d5b581a4cd67bb` |
| D04 | \[...\] | 84–87 | `01dcebe5a27acc0b96749992375228410e9cbdadbdf76f567e0ee9fc6d88ee5b` |
| D05 | \[...\] | 92–95 | `081b2f1e50da72c4236c1860c9c484bf9db6d8dbb97c6d755bd114b26468a1c8` |
| D06 | \[...\] | 99–102 | `710bb2b2c931410f9c0a0ed80b8afe7bce553bf59b98219f5e6329d63a9b37c7` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 26: `properties are exact finite facts.  A replay on the locked`
- TeX line 31: `exponent one, one at each tolerance.  The result is a finite obstruction to`
- TeX line 45: `on the shell row.  The next minimal question is therefore finite and`
- TeX line 107: `\begin{proposition}[Finite partition and holdout separation]`
- TeX line 108: `For finite $S_L,S_R$, (1) is a pairwise-disjoint partition of $U$.  For each`
- TeX line 109: `direction, the minimization (4) does not consult rows in $E_L$ or $E_R$;`
- TeX line 137: `does not manufacture a common target on $U$.  Moreover, the labels are`
- TeX line 139: `Thus the holdout is a diagnostic of finite completion stability, not a causal`
- TeX line 143: `\section{Finite replay and obstruction}`
- TeX line 153: `The independent checker does not import the producer.  It loads the frozen`
- TeX line 157: `finite algebraic identities.`
- TeX line 176: `Table~\ref{tab:census} is the central finite result.  Budget preferences alone`
- TeX line 194: `The positive result is a clean finite protocol: a common ambient operator can`
- TeX line 199: `the withheld native exclusive pieces.  This is a finite obstruction to a`
- TeX line 202: `The result does not pay the arithmetic $L^2$ gate, a uniform growing-budget`
- TeX line 203: `estimate, or any fixed-power credit.  It does not prove full Route-B Gate B,`
- TeX line 204: `and it says nothing by itself about the existence of infinitely many twin`
- TeX line 220: `finite observations under the locked protocol and should not be extrapolated`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:census` → `main.tex#L162` (existing project target or original TeX label line).
