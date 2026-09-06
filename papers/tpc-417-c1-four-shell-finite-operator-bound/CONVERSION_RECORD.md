# TPC-417 conversion record

## Conversion identity

- **Repository source commit:** `dd326323c19356e401d293c1831495ba69e90e9b`
- **TeX:** [`paper/main.tex`](paper/main.tex), SHA-256 `f92f1bd23b6c5738216ebbb91f1336f133346e4c3e3f28333ba0d560ec0fb780`
- **PDF:** [`paper/main.pdf`](paper/main.pdf), SHA-256 `7484892d443c4115bbb7329ac9408d4aec3aef7fd46da83136f1acd5faa9e842`
- **Converted Markdown:** [`paper/main.md`](paper/main.md)
- **Conversion tool:** `pandoc -f latex -t gfm --wrap=none` plus a metadata/abstract preface
- **Conversion status:** `FULL_TEX_TO_MARKDOWN_MECHANICAL`
- **Semantic review status:** `SCOPED_REVIEW_AGAINST_README_AND_PROOF_PACKAGE`
- **References:** no bibliography/reference section is present in the source TeX; the inventory therefore remains conservative.

## Source location map

| Source section | TeX line | PDF page (inferred from section text) | Match score |
|---|---:|---:|---:|
| `Finite model` | 20 | 1 | 2 |
| `Exact matrix identities` | 29 | 1 | 3 |
| `Bound` | 45 | 1 | 1 |
| `Scope and audit` | 62 | 2 | 3 |
| `Reproduction` | 77 | 2 | 1 |

The abstract begins before the first section in the front matter. PDF page numbers refer to the preserved compiled `main.pdf`; the TeX line numbers refer to the exact source hash above.

## Formula and theorem-prerequisite audit

- Source has `5` displayed-equation environment markers before conversion; the Markdown retains the corresponding TeX math as Pandoc inline/display math.
- The converted claim was checked against the paper README and `PROOF_PACKAGE.md`; no stronger theorem, asymptotic conclusion, physical identification, arithmetic advance, fixed-power credit, Route-B closure, or twin-prime conclusion was added.
- proof package present: `PASS`.
- README scope boundary present: `PASS`.
- source proof/claim symbols represented: `PASS`.
- finite-only boundary preserved: `PASS` (source and proof package both state the finite synthetic scope).

### Declared prerequisites

- **Domain/premises:** use the finite synthetic assumptions stated in the source manuscript and its proof package; do not silently generalize them.
- **Exact/computational evidence:** certificate, independent replay, and stress commands remain linked by the package README; this conversion does not reclassify computation as an arithmetic proof.
- **Scope gate:** the source’s finite-only and open-gate language is preserved verbatim in substance.

## Audit note

This record audits provenance and theorem-boundary preservation. It is not an independent proof certificate; the TeX manuscript, proof package, code, certificate, and Bridge-B checks remain the authoritative release chain.
