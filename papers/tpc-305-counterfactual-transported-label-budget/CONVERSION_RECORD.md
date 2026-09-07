# TPC-305 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ed725e6537012bd17a32d061d9d8e6dd3b253613`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `4dde8522839d02b9a74cccaf01f60e19a103fac6567b744e8a3e50929f6d071c`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `4621ca9103bf897967c8d94a4ffbd1720bf94e69afc1f8a231ff0d0427d808aa`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `ba9a5e58027e3059fdfc4d52f2235aa13392dccfa0194a38072821e7d13f8d01`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `c54f6a225d8738174c619b6357c7b5e9e1768b554d7353e0ca575672da5009e1`.
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
| `Position of the question` | 36 | 1 | `HEADING_TEXT_MATCH` |
| `Counterfactual protocol` | 63 | 2 | `HEADING_TEXT_MATCH` |
| `Finite exact statements` | 120 | 2 | `HEADING_TEXT_MATCH` |
| `Certified finite atlas` | 165 | 3 | `HEADING_TEXT_MATCH` |
| `Interpretation and obstruction` | 234 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility` | 256 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 267 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `70` before writing and `70` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `7`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `c47fd6910a2f77e25a3d6053e456385df342f2b0624ede63c60388e31b33b5a2`.
- Source theorem/proof environment starts: proposition at TeX line 122, proof at TeX line 129, proposition at TeX line 138, proof at TeX line 144, proposition at TeX line 152, proof at TeX line 157.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 58–60 | `7a902f879b6e40b391aeb8aa2d02b3abb67255089091a4506038a4d6a6d331df` |
| D02 | \[...\] | 68–71 | `f5fd6bda9819a94ed89c09576e31259e9b5cc1dd3c77ed80e6e14c1951a09f12` |
| D03 | \[...\] | 74–79 | `6b03d9755dde156af51967ff0fd9db8bcd87e95438e26640a86e0ffb139d0fe7` |
| D04 | \[...\] | 88–92 | `ba4c4010d85e8985a23dd4515b67252d97069270c2dda2bf7d133e9c221413ed` |
| D05 | \[...\] | 96–98 | `d25ad0bb64a9abf15050448e0c446e3f5392e62bfa260ac369ee25e09d9d3387` |
| D06 | \[...\] | 101–103 | `6e8bae9a587b4b4fcc825462b53b2d28491cb2077a706cd1cf8570bb6a294119` |
| D07 | \[...\] | 110–117 | `8e69e6ff9a324a312f777299df5342769d9af110cb43f87afeedde100d1e5832` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 18: `The preceding finite crosswalk found that the $Q=60\to70$ transition is the`
- TeX line 21: `shell/operator and the target simultaneously.  We introduce a finite`
- TeX line 31: `numerically certified finite target-swap atlas and a partial counterfactual`
- TeX line 32: `control.  The cross-operator interaction term, uniform asymptotics, and any`
- TeX line 33: `twin-prime conclusion remain open.`
- TeX line 38: `We work on the finite source-first prime-shell line developed in the local`
- TeX line 41: `TPC-303 shows that the resulting constrained native budget is not a function`
- TeX line 52: `This is a target-swap experiment, not a claim that the two physical operators`
- TeX line 82: `the target vector inside an operator row and does not rebuild that row.`
- TeX line 84: `For completeness, let $V_Q$ denote the finite physical-output/profile matrix`
- TeX line 120: `\section{Finite exact statements}`
- TeX line 140: `same finite constrained quadratic program with only its target vector changed.`
- TeX line 165: `\section{Certified finite atlas}`
- TeX line 170: `ratios, and classifications.  The independent replay does not import the`
- TeX line 171: `TPC-305 producer: it reconstructs the finite target protocol and checks every`
- TeX line 224: `an increase in the common profile dimension.  It is still not a causal proof:`
- TeX line 231: `finite index changes are part of the declared protocol, not an asymptotic`
- TeX line 244: `target variation within each row but does not make $V_L=V_R$.  The outer-pair`
- TeX line 262: `are embedded in the certificate.  The manuscript is intentionally a finite`

## Conversion limitations

- 2 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:pairs` → `main.tex#L182` (existing project target or original TeX label line).
- Link relocation: `#tab:middle` → `main.tex#L206` (existing project target or original TeX label line).
