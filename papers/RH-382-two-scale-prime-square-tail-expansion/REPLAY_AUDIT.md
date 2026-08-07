# RH-382 replay audit

## Deterministic layers

1. `make result` regenerates the exact result and checks 33 live/release
   source locks.
2. `make schema` regenerates the recursively closed exact Draft 2020-12
   schema.
3. `make test` checks arithmetic identities, ambient Decimal-context
   independence, optimized mode, full result/schema regeneration, and
   fail-closed mutations.
4. `make pdf` compiles the manuscript and makes the semantic PDF
   byte-identical to `main.pdf`.
5. `make archive` regenerates and independently verifies publication and
   external-input hashes.

## Frozen exact fixture

- Certificate canonical bytes: `22543`.
- Certificate SHA-256:
  `5fe227102a0a88307b5788f55d61bbbe07a17e5158aca11cfbbc79ec9e0cb624`.
- External source count: `33`.
- External aggregate digest:
  `7b62b7e77ad313a52a07851e700aff197c2cc4bc3d910c6a464cd3cec0b55cb6`.

## Final replay snapshot

- Tests: `22/22` passed, including `-OO`, ambient Decimal context, exact
  schema regeneration, and adversarial source/archive mutations.
- Individual archive: `29` publication members plus `33` external inputs;
  `0` failures; full manifest rebuild and semantic-PDF equality pass.
- PDF: `8` A4 pages, `327524` bytes, `21` embedded/subsetted/Unicode-mapped
  font rows; Ghostscript, Poppler text extraction, and `8/8` visual pages
  pass.
- LaTeX/BibTeX: no undefined citation/reference, overfull/underfull box,
  actionable warning, rerun request, or literal carriage return.
- Read-only outer four-volume replay: `4` volumes, `73` archive members,
  `1548` dependency hashes, `8` result hashes, `361` numbered sources, and
  `0` failures. Manifest SHA-256 is
  `24dcf3c6e74c5252e7e278d9141a656c6b97bb30fad6578da8c193cc1063a897`.

Stable primary hashes before the final archive manifest is rebuilt:

```text
main.tex
929b4304390036843c5e4f0d165f3be45d683e36f2a7537a3a5d14ed197b5d0c

main.pdf / semantic PDF
099f87a612a7b5b51ed50b05de2c6a4304d0f85efcb30e15106329767a8783ee

result.json
960ef6ce017ad62b6c552ed30a41b9f0c3e41a9a217ef103c4a3f812c80a71d2

result.schema.json
573b631820edd3b911b9792f9587fee07a03cf13ecefd03a6247d115cfa42394
```
