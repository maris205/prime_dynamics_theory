# TPC-269 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `524af4ad2c623e839511e915db5d85e6c41c7c9e`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `5289bccb1ae976558007eb9c7dbc3f3677955b1c4b300bcc0ae258f4fe5e675f`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `07aa60325d36c2c4eabd70000021bcabaea0ccc9594ea45d1bfe02e89cbc3da0`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `7faf2adbda46ef034a9e5e36a49576b2cd4ffea701700e43258e07afef8fc81d`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC265_269.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Position and claim firewall` | 31 | 1 | `HEADING_TEXT_MATCH` |
| `The finite source and operator` | 47 | 1 | `HEADING_TEXT_MATCH` |
| `Exact profile transfer` | 84 | 2 | `HEADING_TEXT_MATCH` |
| `Interval certificate` | 117 | 2 | `HEADING_TEXT_MATCH` |
| `Interpretation and limits` | 180 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 192 | 4 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 200 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `63` before writing and `63` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `12`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8fbc2c3f5ae37665c906e800d3083fd1030a60b393191d985956ea42ba53308e`.
- Source theorem/proof environment starts: proposition at TeX line 103, proof at TeX line 109, theorem at TeX line 134, proof at TeX line 149.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 49–52 | `df732d24eef530af8f0d9557f6a969f862af81a537b82ae59dcda757d047ae66` |
| D02 | \[...\] | 55–59 | `d8ef7f24e196addd7e1d101939c8ef9dc46362d02627cfa547d193e42297f2d3` |
| D03 | \[...\] | 62–66 | `6e6372024f8c2fc54f35c74662c91539baa7715a0cca695eeaab85b7c9156a1d` |
| D04 | \[...\] | 68–71 | `00de9cea0ad7dc55d8ca242fd7ae67bf0a32bd77fbcecc28e12825e8de12170c` |
| D05 | \[...\] | 75–78 | `2835a3025866d9c7e117e9c5977d974615ce295cd4454aad1cf26d51783ca52d` |
| D06 | \[...\] | 80–83 | `b1eee6a1231101de3332cd912bb108cd5bfa82ce02b9bf0c12c0c74e8840b992` |
| D07 | \[...\] | 87–90 | `93acae8b9a42c20d7dcec9018922e82484f6750ef808abacf8929bf393133ed5` |
| D08 | \[...\] | 92–96 | `a8bf889c13d91941832b2071631a4bbbd047e196064fca3385851977a342d422` |
| D09 | \[...\] | 98–102 | `ea9ace7d302d7840a4c170f9a8209f1dda78e9efae0a3d32f02c8bf1c4148b5c` |
| D10 | \[...\] | 119–122 | `3482c1d9b220daeb80b8be9a439d7823717e80b14e1ec2d6b31894aad2d5ba8e` |
| D11 | \[...\] | 126–129 | `ed60178397f544705565afba92fe671c69f62ac03cd2dc6aefe67a6f290d8ad9` |
| D12 | \[...\] | 138–145 | `268b728d22f8bed3d000075ceb5a94deea6dbac336d8132a8a674a3baef54655` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 20: `TPC-268 showed that a fixed finite comparison cutoff can move a literal V59`
- TeX line 22: `registered finite proxy $z_N=\lfloor\log N\rfloor$ and move the kernel along`
- TeX line 28: `$\theta=9/10$ above and $\theta=24/25$ below $1/4$. This is a finite`
- TeX line 29: `model-relative transfer obstruction, not an asymptotic V59 estimate.`
- TeX line 34: `instantiated that object at twelve finite rows with a $z=2$ comparison and`
- TeX line 36: `declared finite cutoff, clock, or kernel parameters can reverse the verdict.`
- TeX line 38: `cutoff together with a convex profile path remove that finite sensitivity?`
- TeX line 42: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE\_GROWING\_CUTOFF\_PROFILE\_TRANSFER}`
- TeX line 44: `The word ''growing'' below refers to the finite proxy registry unless it is`
- TeX line 47: `\section{The finite source and operator}`
- TeX line 53: `For an integer $z\geq2$, let $b_N^{(z)}$ be the finite shifted-prime`
- TeX line 67: `The finite cutoff proxy is`
- TeX line 73: `finite kernel representatives inherited from the previous audit. If $A_s$`
- TeX line 104: `For every finite row and rational $\theta$,`
- TeX line 110: `All entries of $A_1,A_2$ are rational on a finite row. Linearity of matrix`
- TeX line 134: `\begin{theorem}[finite growing-cutoff/profile transfer]`
- TeX line 150: `The finite identities are the proposition. The interval producer enumerates the`
- TeX line 155: `profile flip. These checks establish the stated finite theorem.`
- TeX line 181: `The finite proxy does two useful things. It removes the arbitrary fixed $z=2$`
- TeX line 184: `not imply a profile-uniform phase bound, because $\rho_\theta$ is a quotient`
- TeX line 188: `not a proof of the source-level V59 cutoff theorem. The twelve rows do not`
- TeX line 190: `the finite profile path is not an arithmetic $L^2$ estimate and does not close`
- TeX line 193: `TPC-269 supplies a finite transfer obstruction with a new source-compatible`
- TeX line 196: `canonicalized finite interface is not uniformly inside the quarter sector.`
- TeX line 199: `arithmetic $L^2$, strict $1/400$ payment, and twin-prime conclusion remain open.`
- TeX line 207: `\bibitem{tpc268} L.~Wang, ''A finite cutoff-sensitivity obstruction for the`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.
