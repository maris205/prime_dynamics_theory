# RH-395 format audit

## Frozen source and build

- Exact title: *All-Clock Rigidity for Centered Three-Window Möbius
  Capacity*.
- `main.tex`, `references.bib`, `main.pdf`, and `main.log` are hash-frozen by
  the release manifest.
- LaTeX and BibTeX complete with no undefined references or citations, no
  overfull or underfull boxes, no multiply defined labels, and no fatal
  errors.
- Four bibliography keys are cited and all four resolve.
- The manuscript has nine A4 pages with one-inch margins.
- No ARS provenance marker, draft sentinel, or unresolved warning token is
  present in the final manuscript or extracted PDF text.

## PDF

- `main.pdf` is 401,435 bytes with SHA-256
  `24aec8e0e28fc6e9d88bb42ad8c2ae51efe33791ce8ba68d220dbf6c62887cde`.
- The PDF is unencrypted and has nine A4 pages.  The printed title uses
  `Möbius`; the metadata uses the ASCII transliteration `Mobius` with the same
  semantic title.
- Ghostscript null-device validation succeeds.
- `pdftotext` extracts the theorem, optimizer, endpoint, source boundary,
  declarations, and references without error markers.
- All 25 reported font rows are embedded, subset, and Unicode-mapped.
- `all-clock-rigidity-for-centered-three-window-mobius-capacity.pdf` is
  byte-identical to `main.pdf`.

## JSON and text

- Result, schema, manifest, and report use sorted two-space-indented UTF-8
  JSON with one terminal line feed and no `NaN` or `Infinity` values.
- Strict loaders reject duplicate keys and nonfinite constants.
- Recursive equality retains exact Boolean, integer, string, list, and object
  types.
- Official `jsonschema` Draft 2020-12 `check_schema` accepts the closed schema,
  and validation of the stored result returns zero errors.
- Publication text members are UTF-8 with exactly one terminal line feed;
  `main.log` and PDFs are excluded from that hand-edited EOF rule.

## Whole-tree hygiene

Release gates reject and test the following classes:

- unsafe relative paths, path traversal, oversize path literals, missing or
  nonregular members, and SHA-256 syntax/type errors;
- symlinks and special filesystem objects;
- bytecode, cache directories, editor temporaries, filename sentinels, and
  literal sealing sentinels;
- carriage returns, missing/doubled terminal line feeds, invalid UTF-8, and
  unlisted regular files;
- external source payload identities and any publication PDF beyond the
  manuscript and its exact semantic copy.

Verdict: format gate passes.
