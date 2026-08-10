# RH-391 research-integrity audit

## Source integrity

- Maynard Theorem 1.3, printed page 385/PDF page 3, is used only for the
  unconditional bound on consecutive prime gaps and the finite-pigeonhole
  extraction of one fixed repeated `h_*<=600`.
- Johnston--Yang is an inherited provenance lock only.  No
  Johnston--Yang estimate or linear-rank prime-tail asymptotic is invoked
  in the RH-391 proof.
- RH-383 supplies the exact endpoint normal form; RH-384 supplies directed
  `u_m` intervals; RH-388 supplies the fixed-rank prototype; RH-390 is the
  frozen immediate release and source closure.
- RH-389, TPC-137, and the Tao active-log source chain are explicitly
  excluded as irrelevant.
- Both remote locks retain `redistributable_in_release=false`.  External
  PDFs and the Johnston--Yang source tar are not vendored.
- All four external payload hashes are absent from publication members and
  from a recursive scan of the complete RH-391 tree.

## Mathematical integrity

- A positive integer gap value at most 600 is extracted from infinitely
  many bounded consecutive gaps; the proof does not replace consecutive
  primes with arbitrary prime pairs.
- Every prime tail is strict at `p>x`.
- One exact integer `r` is used at both endpoints, with `r->infinity` and
  `r<=C*x` for one fixed `C>0`.
- The optional hypothesis `r/x->lambda` is used only for the finite-slope
  profile.  The edge theorem and coarse bound allow oscillation.
- The atom is exactly `a=(x^2/(q^2-1))^r`; the right-scale conversion is
  `rho=(x/q)^(2r)` and `rho/a=(1-q^-2)^r->1`.
- The I and J smooth intervals are controlled separately, with their exact
  signs and kernels.
- The integer-tail ledger pays constants `4/2/4/14` using explicit
  geometric denominators, the eventual fixed-C bound
  `(1-x^-2)^(-r-1)<=2`, and an exact telescope.
- No prime number theorem transfer and no linear-rank `P_r~K_r` assertion
  appears.
- The endpoint direction uses exact RH-384 rational intervals and proves
  `gamma_r>=kappa_gamma*7^r/r` for exact `r>=7`.
- The Taylor lift pays the common head, all higher ranks, the complete J/I
  bridge, Hessian 224, square factor 112, and normalized remainders 18816
  and 2240.
- The conclusion is a natural pair maximum with unequal left/right scales.
  It does not select one endpoint or permit an arbitrary single-vertex
  schedule.
- Next-rank divergence uses an elementary one-sided integer upper bound for
  `P_(r+1)`, not an asymptotic equivalent.

## Artifact integrity

- The verifier enforces exact integers, Booleans, strings, lists, objects,
  strict finite JSON, duplicate-key rejection, and exact leaf membership.
- `compare_fresh=false` independently checks semantic cross-contracts and
  invokes no row or certificate builder.
- All 24 named semantic mutations change a theorem-critical field and are
  rejected.
- The official Draft 2020-12 schema is recursively closed, fixes all array
  lengths, and rejects extra members and Boolean aliases for integers.
- The result and schema are byte-identical under normal and optimized
  `python -OO` regeneration.

## Closure and archive integrity

The closure is exactly 97 immutable release-bound Git objects in groups
`87+8+2`, plus two ordered remote logical objects, for 99 logical inputs.
The fixed publication manifest has 34 members; manifest and report bring
the release-stage set to 36 files.  Exact Stage 1 and manuscript hashes,
Git identity, group and logical digests, both default-offline zero-request
replays, semantic-PDF identity, remote rights/nonvendoring, and four-hash
payload exclusion are executable gates.

## Declarations audit

The manuscript includes data/code availability, ethics, author
contributions, competing interests, funding, and AI-use disclosures.  No
human or animal subjects, personal data, clinical intervention, external
funding, or competing interest is present.

## Verdict

Accept.  Independent theorem and source/citation/PDF reviews each reported
zero blockers and zero minors.  The final archive replay reports zero
failures.
