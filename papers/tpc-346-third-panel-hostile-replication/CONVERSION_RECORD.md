# TPC-346 conversion record

## Provenance and status

- Converter: `source-markdown-audit-v2`; Pandoc `pandoc 2.9.2.1`.
- Repository source commit: `1de1964aa411aa631587da690524beadf1127d3c`.
- TeX: [paper/main.tex](paper/main.tex), SHA-256 `25a97016196e77125a7fd0f4cdb0e630baf3d12b2279d5ce8069de16e96639a2`.

- Preserved PDF: [paper/main.pdf](paper/main.pdf), SHA-256 `a71ce1e34eb76640213323ef322df07a3c6cee388888d41483d4060832369666`; 4 extracted pages. PDF is preserved, not recompiled or certified to match the TeX.
- Reading layer: [paper/main.md](paper/main.md), SHA-256 `d46f65d418ae1aeb073f22241fd06f59bf958fe776b90da351221c2d21fa7945`.
- Conversion status: `FULL_TEX_TO_MARKDOWN_MECHANICAL`.
- Semantic review: `NOT_INDEPENDENTLY_REPROVED`; automated preservation checks are not theorem or certificate validation.
- Supplemental prerequisite audit: [bounded source review](../../research/tpc-big-road/TPC_CONVERSION_SCOPE_TPC345_349.md).
- Repair history and bounded manual source audit: [maintenance audit](../../research/tpc-big-road/TPC_MAINTENANCE_REPAIR_2026-09-07.md). Known manuscript issues remain preserved, not silently corrected.
- Available package materials: [README.md](README.md), [PROOF_PACKAGE.md](PROOF_PACKAGE.md), [DERIVATION_PACKAGE.md](DERIVATION_PACKAGE.md), [notes/claim_firewall.md](notes/claim_firewall.md), [notes/route_evaluation.md](notes/route_evaluation.md).
- Separate proof package: `PRESENT (availability only)`.
- Bibliography/reference section detected: `NO`. A source bibliography receives an explicit References heading; its entries are preserved, not externally verified.

## Source section / PDF location map

| Source heading | TeX line | PDF page(s) | Mapping evidence |
|---|---:|---|---|
| `Introduction` | 46 | 1 | `HEADING_TEXT_MATCH` |
| `Frozen protocol and models` | 73 | 1 | `HEADING_TEXT_MATCH` |
| `Finite identities` | 127 | 2 | `HEADING_TEXT_MATCH` |
| `Hostile finite readout` | 162 | 2 | `HEADING_TEXT_MATCH` |
| `Own fit and model complexity` | 164 | 2 | `HEADING_TEXT_MATCH` |
| `Transfer and hostile controls` | 194 | 3 | `HEADING_TEXT_MATCH` |
| `Pairwise geometry` | 226 | 3 | `HEADING_TEXT_MATCH` |
| `Route evaluation and limitations` | 248 | 3 | `HEADING_TEXT_MATCH` |
| `Conclusion` | 277 | 4 | `HEADING_TEXT_MATCH` |
| `Reproducibility record` | 288 | UNMAPPED | `UNMAPPED_OR_AMBIGUOUS` |

PDF mapping uses heading-text matches at extracted line boundaries; an ambiguous or absent match is explicitly unmapped. TeX line numbers refer to the hashed original above.

## Formula preservation checks

- Source-to-reader scope: full document body and complete abstract, with TeX macros interpreted by Pandoc; title/author/date retained separately.
- Pandoc math-node sequence: `45` before writing and `45` after Markdown parsing; normalized TeX expressions and inline/display kinds: `PASS`.
- Whitespace-normalized plain-text roundtrip: `PASS`.
- Explicit source display blocks: `10`; complete catalog below. This raw-source count is not assumed equal to AST display count (e.g. align rows).
- Math sequence SHA-256: `8cfa652960183bc5f51b2f65a223aa8ce342fb2f8a278fb306c83481cffd4289`.
- Source theorem/proof environment starts: proposition at TeX line 129, proof at TeX line 136, proposition at TeX line 141, proof at TeX line 149.

| Source display | Environment | TeX lines | Raw block SHA-256 |
|---|---|---:|---|
| D01 | \[...\] | 76–78 | `aa8a6522d787c42f5e7daa46a577c4db4022b2c11c4a1e6ff1181599204a4961` |
| D02 | \[...\] | 104–111 | `46e1d93b7deff22d80d52ba1c7942dc43659ee926978710df5129b206d7e01aa` |
| D03 | \[...\] | 118–120 | `e2269fe4f4d6a838b194e03ae11e966744eca0e401c043380e17ebbc7da9e5c3` |
| D04 | \[...\] | 132–134 | `4e6f418393118eaf216d5203d157b1c387730765b8c023482435259bd446f434` |
| D05 | \[...\] | 144–147 | `0f21d111699cb978da6f59450b9bfad7b750dd7a0309df6e9a1c840fb9ac6284` |
| D06 | \[...\] | 151–153 | `c839b7cf4ed28b0a027e2a83290d9c29c5fafa393e0cd0fdc0bd31c0482caad6` |
| D07 | \[...\] | 231–233 | `2cb780bdd60ed04ad790e329de743604f061d58cf804206159a9296afd6be133` |
| D08 | \[...\] | 235–237 | `bd42ad5b5bb8b3887b104fef9018bc6af3cdc7c51316f339cc4a25def8743519` |
| D09 | \[...\] | 240–243 | `6548f663490d4ede65d3ec18e9f12bf7ec18925df402171e69060a092de8c105` |
| D10 | \[...\] | 260–262 | `682c9b72b6a431c0b94f80efe229021ecab21ca49657ac37a14dc09e5520b392` |

## Prerequisite / claim-boundary audit scope

The automated check verifies expression retention, not mathematical implication. It does not prove the source assumptions, reproduce numerical certificates, check uniform constants, identify a physical operator, or supply arithmetic L2/fixed-power credit. The original package and current TPC418 STOP remain authoritative. Generic historical `PASS` labels have been superseded by the explicit checks above.

The following are source-located keyword excerpts for manual review, not a semantic verdict (first 32 matches; the linked TeX contains the full scope):

- TeX line 17: `and a Finite Freeze of the Panel-Adaptive Route}}`
- TeX line 28: `Recent finite audits of a twin-prime dynamical response model found that a`
- TeX line 40: `projections exceed $0.30$.  Thus the raw crossing is a finite,`
- TeX line 42: `frozen.  No arithmetic $L^2$ estimate, asymptotic saving, or twin-prime`
- TeX line 48: `The current twin-prime route studies finite response vectors produced by a`
- TeX line 52: `coefficient does not meet the inherited residual guard on either of two`
- TeX line 60: `finite question.  A fresh panel is selected inside the same cutoff, with no`
- TeX line 67: `\texttt{PROVED\_EXACT\_FINITE\_DECLARED\_MODEL}.  Numerical values are`
- TeX line 68: `\texttt{NUMERICALLY\_CERTIFIED\_FINITE}.  Threshold failures are`
- TeX line 71: `Route-B Gate B remains \texttt{OPEN}.`
- TeX line 122: `a held-out panel.  This produces a prediction residual, not a projection`
- TeX line 127: `\section{Finite identities}`
- TeX line 130: `For a finite matrix $N$ and its orthogonal projector $P_N$, every finite`
- TeX line 155: `projection onto the larger finite subspace cannot increase the residual norm.`
- TeX line 158: `These propositions are exact finite facts.  They do not identify an`
- TeX line 160: `coordinates are a modeling choice, not a source-uniform theorem.`
- TeX line 162: `\section{Hostile finite readout}`
- TeX line 175: `\caption{Pooled finite residual retentions.}`
- TeX line 224: `alone accounts for the fresh-panel obstruction; it does not.`
- TeX line 229: `parent in raw coordinates, but the alignment is not a stable common law.`
- TeX line 244: `These finite subspace comparisons are`
- TeX line 259: `tests fail.  Together these observations justify the finite scoped decision`
- TeX line 261: `\texttt{FREEZE\_PANEL\_ADAPTIVE\_ROUTE\_FINITE\_SCOPED}.`
- TeX line 264: `\paragraph{Open theorem.}`
- TeX line 265: `The central unpaid mathematical interface remains a source-uniform`
- TeX line 266: `arithmetic $L^2$ estimate (and the associated uniform masked-operator`
- TeX line 267: `bound).  No finite panel fit supplies fixed-power credit or the strict`
- TeX line 272: `checkout.  The local Bridge-B checker is fail-closed and is not an official`
- TeX line 273: `evaluator pass.  The finite freeze concerns only the declared`
- TeX line 274: `panel-adaptive branch; it is not a universal no-go theorem for every future`
- TeX line 280: `interpretation of the TPC-344 repair: it is not a weighting-stable,`
- TeX line 281: `transferable finite law on the declared panel family.  The route map should`

## Conversion limitations

- Theorem/proof environment names and boundaries retained as labeled quotes; printed environment numbering is not reconstructed. Consult the source/PDF for numbering.

- Link relocation: `#tab:models` → `main.tex#L176` (existing project target or original TeX label line).
