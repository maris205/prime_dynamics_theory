# RH-390 research-integrity audit

## Source integrity

- Johnston--Yang Theorem 1.4, equation (1.8), printed page 2 is used only
  for the explicit prime-counting envelope inherited through RH-386.
- Maynard Theorem 1.3, printed page 385/PDF page 3 is used only for the
  unconditional bounded consecutive gaps needed by fixed-rank necessity.
- The Johnston--Yang fallback corollary and both recorded out-of-scope
  source typos are not theorem inputs.
- RH-389, TPC-137, and Tao are explicitly excluded as irrelevant to this
  proof-minimal closure.
- Both remote locks retain `redistributable_in_release=false`; external
  PDFs and the Johnston--Yang source tar are not vendored.
- All four external payload hashes are absent from publication members and
  from a recursive scan of the entire RH-390 tree.

## Mathematical integrity

- All prime tails and the Stieltjes boundary are strict at `p>x`.
- The source transfer sums the absolute Stieltjes error directly over every
  `r>=s`; no per-r logarithmic smallness argument is misapplied.
- The power ledger consumes exponent `s+1` in `B_(s,c)` and keeps the two
  distinct denominators `x^2-1` and `x^2`.
- The factorial remainder is an exact finite identity with sign
  `(-1)^K`; no convergent factorial series is asserted.
- The full integer `K` window is proved by a symbolic recurrence for a
  positive-real `D`, not finite fixtures or a false integrality claim.
- The common cube uses `L>=512 => x>256`; the endpoint uses the dual
  `l_infinity/l_1` norm and the bound 126.
- Growing-rank uniformity pays the `7^S`, denominator, source, power,
  factorial, and uniform `P_s/K_s` ledgers simultaneously.
- All-rank `gamma_r>0` uses five outward rational intervals and exact
  cross-products; displayed decimals are not floating-point evidence.
- Fixed-rank necessity uses infinitely many consecutive bounded gaps, the
  exact successor atom, all higher-rank negligibility, and a common-head
  Taylor remainder with constants 224 and 112.
- Necessity is limited to fixed `s` and the declared `P/J/I` hierarchy.

## Artifact integrity

- The verifier enforces exact integer, Boolean, string, list, and object
  types and strict finite JSON with duplicate-key rejection.
- `compare_fresh=false` independently recomputes field semantics while
  tests disable the certificate and every row builder.
- All 24 genuine semantic mutations are changed and rejected.
- The official Draft 2020-12 schema is recursively closed, fixes array
  lengths, and rejects extra members and Boolean aliases for integers.
- Normal and optimized `-OO` builds reproduce certificate, result, schema,
  manifest, and archive report exactly.

## Closure and archive integrity

The closure is exactly 87 immutable Git release blobs plus two ordered
remote logical objects, for 89 logical inputs.  The fixed publication
manifest has 34 members; manifest and report bring the release-stage set
to 36 files.  Git identity, source digests, logical digest, offline
zero-request replay, semantic-PDF identity, and payload exclusion are
executable gates.

## Declarations audit

The manuscript includes data/code availability, ethics, author
contributions, competing interests, funding, and AI-use disclosures.  No
human or animal subjects, personal data, clinical intervention, external
funding, or competing interest is present.

## Verdict

Accept.  Independent theorem and source/citation/PDF reviews reported zero
blockers and zero minors.  The final archive replay reports zero failures.
