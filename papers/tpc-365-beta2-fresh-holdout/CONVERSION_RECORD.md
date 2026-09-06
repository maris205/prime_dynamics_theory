# TPC-365 source-to-Markdown conversion

## Conversion identity

- **Repository source commit:** `5bebbda8ae9cf0a92b28c03272f89c43e28cfbc5`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `0930e954fd125264c343caf2a4a3d23dbda5af1a1550988b3d521bb06694f0c7`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `27c0792c7e065b65ea2c094e1c1e8aa265d8cc92e0deb49c0c086b5c98ce03d9`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Question and scope` | 38 | 1 | 3 |
| `Finite operator and selection rule` | 60 | 1 | 3 |
| `Finite audit` | 111 | 1 | 3 |
| `Exact and independent verification` | 167 | 2 | 3 |
| `Claim firewall and route decision` | 185 | 2 | 3 |
| `Conclusion` | 212 | 2 | 3 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `0` displayed-equation markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and `PROOF_PACKAGE.md`; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- Proof package present: `PASS`.
- README scope boundary present: `PASS`.
- Source proof/claim symbols represented: `PASS` (displayed formulas, inequalities, sums, masks, and named quantities are retained in the Markdown math).
- Finite-only boundary preserved: `PASS` (source and proof package both state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and its proof package; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent checker, and stress commands remain linked by the package README; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** the finite operator, predeclared panel, computed profile, and audit language remain finite-scope objects; no scale/origin uniformity, arithmetic estimate, fixed-power credit, Route-B closure, or twin-prime conclusion is inferred.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package, code, certificate, and Bridge-B checks remain the authoritative release chain.
