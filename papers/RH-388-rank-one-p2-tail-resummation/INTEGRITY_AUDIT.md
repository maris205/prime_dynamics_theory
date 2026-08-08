# RH-388 research-integrity audit

## Source integrity

- Johnston--Yang is used only for Theorem 1.4, equation (1.8), printed
  page 2, through the inherited exact remote lock.
- Maynard is used only for unconditional Theorem 1.3, printed page 385
  (PDF page 3), which states a liminf consecutive-prime-gap bound of 600.
- The Maynard official article metadata, DOI, locator, publisher PDF URL,
  MIME, byte count, page count, and SHA-256 are locked.  Its explicit
  verifier is offline by default.
- The current Annals policy materials do not establish the agreement
  applicable to the 2015 article.  The conservative lock therefore sets
  `published_version_cc_by=false`, `redistributable_in_release=false`,
  and `pdf_vendored=false`.
- The Johnston--Yang author PDF/source tar and the Maynard publisher PDF
  are not publication members.  All four locked external payload hashes
  are recursively absent.

## Mathematical integrity

- The endpoint is strictly `p>x`; the Stieltjes boundary and both
  `xh_r` contributions are retained.
- Source and power replacement start at `r=2`.  The exact `P_1` term is
  never smoothed in the positive theorem.
- Tonelli is applied to nonnegative absolute majorants; no finite-order
  relative logarithmic estimate is summed over unbounded `r`.
- The common denominator is used twice and the `1/6`, `1/5`, `60`, and
  `13` arithmetic is displayed in the manuscript.
- The factorial identity is a finite geometric identity with exact
  remainder.  No convergence of `sum (-1)^j j!a^j` is asserted.
- The full integer window is proved by the universal `b_K` recurrence;
  twelve small-`K` rows are explicitly only regression fixtures.
- `L>=512` is bridged to `x>256` before positivity and cube bounds are
  used.  The path stays in the real cube.
- The endpoint norm pairing is `l_infinity/l_1`; every master bound
  retains `pi^2`.  Gradient, Hessian, and Taylor constants are
  `126`, `224`, and `112`.
- Maynard's integer-valued liminf implies infinitely many consecutive
  gaps at most 600.  Exact successor atoms and smooth interval terms are
  separately retained.
- The sharp scalar and endpoint limsup constants are `1/2` and
  `X_infinity`.  The artifact's `1/16` witness is labelled eventual and
  nonsharp.
- Necessity is restricted to the declared `P/J/I` hierarchy.  No
  universal surrogate impossibility is claimed.

## Artifact integrity

- The verifier enforces exact integer, Boolean, string, list, and object
  types and strict finite JSON with duplicate-key rejection.
- `compare_fresh=false` performs independent field-level recomputation;
  tests disable the certificate, row, and contract builders.
- All 24 genuine semantic mutations and every scalar leaf are rejected.
- The official Draft 2020-12 schema is recursively closed, fixes array
  lengths, and rejects extra members and Boolean aliases for integers.
- Direct and optimized `-OO` builders reproduce identical certificate,
  result, schema, source, and archive objects.
- The 56 finite rows have role `reproduction_not_analytic_proof`.

## Closure and archive integrity

The closure is exactly 77 immutable Git release blobs plus two ordered
remote logical objects, for 79 logical sources.  Group, ordered-Git,
canonical-remote, and logical digests are hard-gated.  The fixed
publication manifest has 36 members; external payload exclusion,
semantic-PDF identity, fresh regeneration, and the outer verifier are
all executable gates.

## Declarations audit

The manuscript includes data/code availability, author contributions,
funding, competing interests, ethics, and AI-assistance disclosures.  No
human or animal subjects, personal data, clinical intervention, funding,
or competing interest is present.

## Verdict

Accept.  Independent mathematical and source/citation/PDF reviews each
reported zero blockers and zero minors.  The release replay reports zero
archive failures; exact details are recorded in the companion audit
files.
