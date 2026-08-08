# RH-389 research-integrity audit

## Source integrity

- TPC-137, at its frozen release commit, is the direct theorem source for
  the full determinant-two periodic Mobius correlation.
- Tao's Theorem 2, equation (3), printed/PDF page 3, is cited only as
  TPC-137's upstream Liouville input.  Its printed `n`/`x` typo is recorded
  as typographical and causes no hypothesis change.
- Johnston--Yang and Maynard are inherited closure-only records and are
  not represented as RH-389 proof inputs.
- The Tao Cambridge VOR is CC BY 4.0 and conservatively remains nonvendored
  by project policy.  The inherited Johnston--Yang and Maynard locks retain
  their stricter redistribution boundaries.
- All five external payload hashes are absent from publication members and
  from a recursive scan of the entire RH-389 tree.

## Mathematical integrity

- Every occurrence of the shifted value at `n<=2` is interpreted through
  the declared zero-padded `mu_0` convention.
- The Abel argument explicitly handles both `X/omega>=T` and `X/omega<T`;
  it does not silently assume the lower endpoint tends to infinity.
- RH-379 is used only for the independent prefix-channel cancellations
  in its proof; its `c11=0` proposition is not applied to active tables.
- The active channel uses exactly the primitive determinant-two TPC-137
  hypotheses and deletes only finitely many positivity endpoints.
- Projection is a subset operation with pointwise nonnegative finite-`X`
  gain, not an output complement.
- Compatibility is recomputed from edge triples for all 64 action pairs.
- The charge records both cone inequalities, the exact half-plus-half
  decomposition, the injective translation, and the `q=1,2` self-loops.
- Input reflection has parity `(+,-,-,+,+,-)`; the paper never claims all
  six interpolation coefficients negate.
- Fixed-clock maximization is post-limit over a finite family.  The
  all-clock statement is a supremum of those fixed-clock capacities, not
  a growing-`q` or max-before-limit theorem.
- RH-378's prior `q=1` conditional constant and witness are disclosed.

## Artifact integrity

- The verifier enforces exact integer, Boolean, string, list, and object
  types and strict finite JSON with duplicate-key rejection.
- `compare_fresh=false` independently recomputes field semantics while
  tests disable the certificate, all group builders, and contract builder.
- Global projection checks all 262,144 table pairs; the finite contract
  records 3,375 compatible pairs and zero projection failures.
- The charge, global reflection involution/parity/compatibility, and every
  fixed-clock attainment are hard gates in `all_pass`.
- All 24 genuine semantic mutations are changed and rejected.
- The official Draft 2020-12 schema is recursively closed, fixes array
  lengths, and rejects extra members and Boolean aliases for integers.
- Normal and optimized `-OO` builds reproduce certificate, result, schema,
  manifest, and archive report exactly.

## Closure and archive integrity

The closure is exactly 95 immutable Git release blobs plus three ordered
remote logical objects, for 98 logical inputs.  The fixed publication
manifest has 37 members; manifest and report bring the release-stage set
to 39 files.  Group, ordered-Git, canonical-remote, logical-digest,
offline-zero-request, semantic-PDF, and payload-exclusion gates are all
executable.

## Declarations audit

The manuscript includes data/code availability, ethics, author
contributions, competing interests, funding, and AI-use disclosures.  No
human or animal subjects, personal data, clinical intervention, external
funding, or competing interest is present.

## Verdict

Accept.  Independent theorem and source/citation/PDF reviews reported zero
blockers and zero minors.  The final archive replay reports zero failures.
