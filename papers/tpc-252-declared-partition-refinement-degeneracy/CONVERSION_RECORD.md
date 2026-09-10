# TPC-252 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `46105cd2fafd9f308822ed2f29723ef1886820b651322f014b9e2d8ae47a2051`.
- Bibliography: [paper/references.bib](paper/references.bib), SHA-256 `7995eae7081a391cb498ee5bdfdd7d42ba921d1d2151aa8697894aa18cf6df85`.
- Preserved PDF: [paper/paper.pdf](paper/paper.pdf), SHA-256 `b88c2ed4af43b751d02fb96b529858624b659bb57ce172b95e6e7c82d99482f7`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `2c99a12271626b49f608d18ef2afae8fae6012160586c2bcff5be0d4bc0626b7`.
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
| `Source lock and declared projections` | 51 | 1 | `HEADING_TEXT_MATCH` |
| `Exact binary refinement calculus` | 98 | 2 | `HEADING_TEXT_MATCH` |
| `Fixed probes, singleton collapse, and optimal margins` | 166 | 2 | `HEADING_TEXT_MATCH` |
| `Same-source non-invariance and exact verification` | 246 | 3 | `HEADING_TEXT_MATCH` |
| `Limitations and conclusion` | 311 | 4 | `HEADING_TEXT_MATCH` |
| `References (external bibliography)` | 330 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `113` before writing and `113` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `22`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8fe16a9dcb69c6804dc24fb04faafb18b504c1df719d331b2cbda9f0f5e39660`.
- Source theorem/proof environment starts: theorem at TeX line 107, proof at TeX line 123, proposition at TeX line 170, proof at TeX line 184, corollary at TeX line 197, proof at TeX line 213, theorem at TeX line 223, proof at TeX line 233, proposition at TeX line 250, proof at TeX line 278.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | equation | 56–58 | `58fb35e4cb8e87eec2910e86aee3ada048088b38ae4c39dde01f254b8c6bbb88` |
| D02 | \[...\] | 64–66 | `228c4d178493cefb92365524657d73fe0bfdd3ee9d34b08c9282861ce86ae539` |
| D03 | equation | 68–71 | `6d2a162ce026107a6707ae013794aa16bf6214f4328f406899cc589c88d24c42` |
| D04 | align | 73–77 | `e430bde343172830f809ea5649f05e5d1c4540c84f1b8a38a321dc23d3a7cb11` |
| D05 | equation | 79–81 | `bec103ba85b03a3bd67801eff62de8a65f43fa314f064653406614dc5b731fe6` |
| D06 | equation | 85–88 | `be6c8f12b4865780ade9bcc15cce5f3e48118941f1780c3b6f70c6c4cf24842e` |
| D07 | equation | 92–95 | `201cf0d7fae4615462eac85f759fc7b36e9c184a645acda6721fa0f98c21ab57` |
| D08 | equation | 102–105 | `f37509b76163ef625482ce413e538bdb0dffe5a32eb6253b0d492d0084de4c26` |
| D09 | align | 109–116 | `b49acb3912802661ea3d1fa18d4f57ba742996a7dca5b39b733bf0ae606dd73b` |
| D10 | equation | 118–120 | `c04e6c397bc681084fcef786c7458959ee8d5565b3acecc6734744606dc3ae0c` |
| D11 | \[...\] | 127–131 | `a3e005cbdd8d6e6acf36c3ee0e50eacd0db54d48189cd995282ad4fb1a7fd6c5` |
| D12 | \[...\] | 135–137 | `7d1aeb500a08d3e3fa81ad11e078b8d5c8b654c498df0f3081e02659674db90e` |
| D13 | \[...\] | 145–148 | `c2ac0b90344c16563e32d0f3aa412809da9165e9af849ce5dae002f320c62f9d` |
| D14 | align* | 151–156 | `a5ec5fee0b9ad6487bf4c07b3756b4c50b66785d1b27c6610b5169b15a0ebe53` |
| D15 | \[...\] | 172–175 | `2bc33b6be7ad593d890b7ae81c77b2412f5b5c90ac869aaa7ce98b8c32ff69bf` |
| D16 | equation | 177–181 | `b79cb0826ca0ad5e366608977b044ec21fdc3d2a4d505a8ee25f48f84c4190bb` |
| D17 | \[...\] | 201–203 | `2baf348f1b7af11abdef932dc1bf0b11be8e8b3212def90ff8ccb253e23f81cd` |
| D18 | equation | 205–209 | `c80e883ef769374e43a5556ce4b766aa9ac037b1fa0b2602ff9eedb6ba4878b8` |
| D19 | equation | 225–229 | `61f8fde7e3faf50364be3451335b7aa2cd7df192dc8bd267142575c44f536fe2` |
| D20 | \[...\] | 252–256 | `c6a2edd3a885d3d8a0795b6d232d03c74d97e912f90fdff97a51885794be8e4f` |
| D21 | \[...\] | 294–296 | `9423bb8d35be6d57ff33d7e98e8e69d4438918b4e8fb5c3706dbc5a681facd3b` |
| D22 | \[...\] | 300–303 | `71537c47b83ec237dd715ab9c5b26b05464425fdb1271b6bdb65f1f18de5d811` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 32: `the longitudinal--transverse compiler for the finite V59 source scalar.  A`
- TeX line 44: `synthetic replay proves that the resulting coarse/fine decomposition metrics`
- TeX line 53: `Let $H=\C^I$, where $I$ is finite and nonempty, and take the inner product to`
- TeX line 54: `be conjugate-linear in its first argument.  We freeze the finite source object`
- TeX line 96: `The partition is declared data, not a V59-canonical object.`
- TeX line 161: `longitudinal term; it does not give either term a monotone absolute value.`
- TeX line 193: `not an indexed before/after update for those native arrays.`
- TeX line 198: `For every finite source in \eqref{eq:source}, $M_{\mathcal S}=I$.  Every`
- TeX line 238: `that $\mathcal S$ attains it.  The maximum exists because a finite set has`
- TeX line 239: `only finitely many partitions.`
- TeX line 273: `\caption{Decomposition metrics for the same unchanged synthetic $A,\beta,w$`
- TeX line 286: `\emph{synthetic exact finite source-operator replay, not a literal V59`
- TeX line 305: `duplicate-key, nonfinite-token, and canonical-byte mutations.  A deterministic`
- TeX line 308: `optimized Python modes.  These finite computations reproduce structural`

## Conversion limitations

- 3 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- External bibliography retained as full BibTeX code, without inventing formatted entries or resolving citation keys.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:z` → `main.tex#L102` (existing project target or original TeX label line).
- Link relocation: `#eq:mupdate` → `main.tex#L110` (existing project target or original TeX label line).
- Link relocation: `#eq:cupdate` → `main.tex#L112` (existing project target or original TeX label line).
- Link relocation: `#eq:qupdate` → `main.tex#L115` (existing project target or original TeX label line).
- Link relocation: `#eq:rmono` → `main.tex#L118` (existing project target or original TeX label line).
- Link relocation: `#thm:binary` → `main.tex#L107` (existing project target or original TeX label line).
- Link relocation: `#eq:gramupdate` → `main.tex#L177` (existing project target or original TeX label line).
- Link relocation: `#eq:source` → `main.tex#L56` (existing project target or original TeX label line).
- Link relocation: `#eq:tpc251` → `main.tex#L92` (existing project target or original TeX label line).
- Link relocation: `#eq:margin` → `main.tex#L225` (existing project target or original TeX label line).
- Link relocation: `#cor:singleton` → `main.tex#L197` (existing project target or original TeX label line).
- Link relocation: `#eq:margin` → `main.tex#L225` (existing project target or original TeX label line).
- Link relocation: `#tab:witness` → `main.tex#L275` (existing project target or original TeX label line).
- Link relocation: `#cor:singleton` → `main.tex#L197` (existing project target or original TeX label line).
