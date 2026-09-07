# TPC-349 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `1de1964aa411aa631587da690524beadf1127d3c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `c58d9894f66cbd3ed1a829cf014623f4f7d51f3778282c69c9558723a6bf3708`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `0b029e9ff302773e22f2a587e79d8ea3220f2ae884af927c8ffe1e112faa769b`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `26c2f3ea7764e9e2136a6a549d07bad973a38de1bb8770ed0e7d55e6d58aff1e`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC345_349.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `YES`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Question and scope` | 49 | 1 | `HEADING_TEXT_MATCH` |
| `The literal masked object` | 63 | 1 | `HEADING_TEXT_MATCH` |
| `Prime balance and the exact Gram interface` | 81 | 2 | `HEADING_TEXT_MATCH` |
| `Frozen audit protocol` | 153 | 2 | `HEADING_TEXT_MATCH` |
| `Finite results` | 176 | 3 | `HEADING_TEXT_MATCH` |
| `Exact multi-hit anchor` | 213 | 3 | `HEADING_TEXT_MATCH` |
| `Adversarial checks and claim boundary` | 231 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion and next question` | 249 | 3 | `HEADING_TEXT_MATCH` |
| `References (thebibliography)` | 263 | 4 | `HEADING_TEXT_MATCH` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `69` before writing and `69` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `13`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `a6f9a50ca722635a337665c3ca16733e6db7155910a3ae06ee11b7584a838c9d`.
- Source theorem/proof environment starts: proposition at TeX line 102, proof at TeX line 107, proposition at TeX line 112, proof at TeX line 122, theorem at TeX line 128, proof at TeX line 137, remark at TeX line 147.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 36–38 | `d635de92ed8fc03884cfdb0d914b0bb17ce152da6defe1f247fdb0e43c1d563c` |
| D02 | \[...\] | 67–69 | `6436e13f217a914c410449a6fca86c0779471339df068414f8d42750f2532ec7` |
| D03 | align* | 72–76 | `94d3c3fbd40844a8caf011a9570c738d1afd3a6554b2bd383004f6a417d4acaf` |
| D04 | \[...\] | 85–91 | `5c44d10ad79d58e882cca6fb46e9c3c23a7182d92e3afb05a38de25c4f5bf9f0` |
| D05 | \[...\] | 94–97 | `39e87ba9b69d1eae442bed3ef2e5ba2bd66fee64f9988f8ed9b35fe499cdd239` |
| D06 | equation | 114–119 | `48aef31c1134d4f21d084d8f1afdd4a4ef4edf9f80ae903ffb806f66141c518c` |
| D07 | equation | 130–134 | `7521753468e02586c3bad580cc50b3fb520e195259f5687f42e932a13e52c9f9` |
| D08 | \[...\] | 140–143 | `dba9178a0520e6101cb14b1fa973a315b1034deb598a4404ef3f6c7b5a2fa067` |
| D09 | \[...\] | 156–159 | `8f4f4e448a859b21bc890f9171db81fe1d793796783681a8f233e1a9c71c2496` |
| D10 | \[...\] | 167–170 | `22494e0ccb7c9572cfb3ffab8aa3970dd9bf25e1678ac0989256618cdf1dab53` |
| D11 | \[...\] | 217–220 | `0157e45da8bdb11478d98e7d41f10d77a9b6b7b3fe8c5cdbdac8d4febd17a197` |
| D12 | \[...\] | 222–226 | `3a853c294435d4000e06553cdeb7da621c907765fb74b9d2fbad4af27b2a85e1` |
| D13 | \[...\] | 252–256 | `b0e155d92ae5a7b5eb1bc6060a9ac2849cc80933e69d224341f12d9b5cd3615e` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 43: `one half of that norm on 175 rows.  The comparison is not uniform: the signed`
- TeX line 44: `vector loses to the coordinate baseline on 56 rows.  These are finite`
- TeX line 45: `observations, not a growing arithmetic estimate; the source-uniform masked`
- TeX line 46: `$L^2$ problem and the twin-prime endpoint remain open.`
- TeX line 54: `structure.  We study one rule fixed before the finite audit: an equal positive`
- TeX line 58: `The exact algebra below is finite-dimensional.  The numerical table is a`
- TeX line 60: `source-native arithmetic vector, a uniform-in-$x$ estimate, a fixed power of`
- TeX line 113: `For every finite matrix $D_I$,`
- TeX line 124: `expand the Euclidean inner product.  The sum is finite, so no convergence`
- TeX line 125: `assumption is involved.`
- TeX line 148: `The theorem is exact finite linear algebra.  It does not say that the Gram`
- TeX line 171: `The baseline is used only for a finite comparison.  The independent checker`
- TeX line 176: `\section{Finite results}`
- TeX line 189: `Quantity & Certified finite readout\\`
- TeX line 207: `comparison is not uniform: 56 rows do not beat $C_I$.  This is why the claim`
- TeX line 209: `The response/defect ratio itself is a valid finite lower-witness ratio because`
- TeX line 211: `open question.`
- TeX line 242: `strongest finite observation is the 136/192 baseline improvement.  The main`
- TeX line 244: `panel.  We claim neither a source-uniform masked operator bound nor an`
- TeX line 255: `\longrightarrow\text{finite norm witness}.`
- TeX line 257: `It demonstrates substantial finite response while exposing the limit of a`
- TeX line 258: `single balanced rule: no uniform gain follows.  The next minimal question is`

## Conversion limitations

- 1 unsupported/citation TeX command(s) retained explicitly as code; citation keys are not bibliographically resolved.
- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#eq:lower` → `main.tex#L133` (existing project target or original TeX label line).
- Link relocation: `#eq:gram` → `main.tex#L118` (existing project target or original TeX label line).
- Link relocation: `#tab:summary` → `main.tex#L186` (existing project target or original TeX label line).
- Link relocation: `#eq:lower` → `main.tex#L133` (existing project target or original TeX label line).
