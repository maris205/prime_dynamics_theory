# TPC-377 source-to-Markdown conversion

## Conversion identity

- **Repository source commit:** `ddfb775a88bced9a1bcafff5c65b13e6df441e55`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `03db7fc8f3e6255c887e2b58795ce997b214aad7838c07e9cfb8ab0debec9eb9`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `0a487ec51afbaedc34d3efc793db719fc59a00a44a0114ab2dc3dead393acb64`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and claim boundary` | 35 | 1 | 3 |
| `Finite object and exact identities` | 49 | 1 | 3 |
| `Predeclared scale protocol` | 80 | 1 | 3 |
| `Results` | 104 | 2 | 3 |
| `Independent audit and limitations` | 148 | 2 | 3 |
| `Conclusion and next question` | 165 | 2 | 3 |


The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audi

- Source has `9` displayed-equation markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
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
