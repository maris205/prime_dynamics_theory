# RH-383 replay audit

## Deterministic layers

1. `make result` regenerates the exact result and checks 41 live/release source
   locks.
2. `make schema` regenerates the recursively closed exact Draft 2020-12
   schema.
3. `make test` checks all three exact-rational oracles, certificate and
   source-lock regeneration, optimized mode, closed schema, genuine negative
   mutations, and archive mutations.
4. `make pdf` compiles the manuscript and makes the semantic PDF
   byte-identical to `main.pdf`.
5. `make archive` regenerates and independently verifies all publication and
   external-input hashes.

## Frozen exact fixture

- Certificate canonical bytes: `12245`.
- Certificate SHA-256:
  `9e2742fcdb2f626909eeb528c5081c9ace5414a1e6466c15b8b6800f427b6f16`.
- External source count: `41`.
- External aggregate digest:
  `492100fe3b6b823a39b58cec25b0dcddf6d52c02bd1941f0978611f01a2b8db9`.

## Final replay snapshot

- Tests: `25/25` passed, including `-OO`, ambient Decimal-context
  independence, exact result/schema regeneration, and fail-closed mutations.
- Individual archive: `29` publication members plus `41` external inputs;
  `0` failures; full manifest rebuild, release-blob identity, exact fixture,
  and semantic-PDF equality pass.
- PDF: `9` A4 pages, `368911` bytes, `25`
  embedded/subsetted/Unicode-mapped font rows; Ghostscript, Poppler text
  extraction, and `9/9` visual pages pass.
- LaTeX/BibTeX: no undefined citation/reference, overfull/underfull box,
  actionable warning, rerun request, or literal carriage return.
- Read-only outer four-volume replay: `4` volumes, `73` archive members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  `0` failures. Manifest SHA-256 is
  `24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897`.

Stable primary hashes before the final archive manifest is rebuilt:

```text
main.tex
b1030a1203685121ddc99504d0d8a5b389611b41e47a1009fea70a0215ab3bb3

main.pdf / semantic PDF
a3d467a54e99b8de0ff9da796cad3423e0683115b5998517e6493f95e77592b0

result.json
519f585f4cf867c0d41ae674c3fb16bc0fbcf529af32131ad1afbba6692355ab

result.schema.json
8985f41cd7043b58d3b2fa9ee387bd6da4cb9d6156d3e5226acf57123674c118
```
