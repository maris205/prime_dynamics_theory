# TPC-379 source-to-Markdown conversion

## Conversion identity

- **Repository source commit:** `ddfb775a88bced9a1bcafff5c65b13e6df441e55`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `93aec9c2c3b9986b2517aa53fe8e5bc72668b0c90acd203e24e6beec5b5745bd`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `8acb1351a169ff77f9a8ce10e7647398da04144a5fb121e54f6ed012d96be4c4`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and claim boundary` | 31 | 1 | 3 |
| `Finite operator and four laws` | 46 | 1 | 3 |
| `Predeclared protocol` | 85 | 1 | 3 |
| `Results` | 105 | 2 | 3 |
| `Audits and interpretation` | 135 | 2 | 3 |
| `Route status and conclusion` | 152 | 2 | 3 |


The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audi

- Source has `10` displayed-equation markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and `PROOF_PACKAGE.md`; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- Proof package present: `PASS`.
- README scope boundary present: `PASS`.
- Source proof/claim symbols represented: `PASS` (displayed formulas, inequalities, sums, masks, and named quantities are retained in the Markdown math).
- Finite-only boundary preserved: `PASS` (source and proof package both state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and its proof package; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent checker, and stress commands remain linked by the package README; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** The finite operator, predeclared panel, computed profile, and audit language remain finite-scope objects; no scale/origin uniformity, arithmetic estimate, fixed-power credit, Route-B closure, or twin-prime conclusion is inferred.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package, code, certificate, and Bridge-B checks remain the authoritative release chain.
