# RH-387 research-integrity audit

## Source integrity

- Primary source: Daniel R. Johnston and Andrew Yang, Some explicit
  estimates for the error term in the prime number theorem, JMAA 527(2),
  article 127460 (2023), DOI 10.1016/j.jmaa.2023.127460.
- The proof uses only Theorem 1.4 equation (1.8), printed page 2.
- Corollary 1.2, Table 1, and the two recorded source typos are
  provenance-only and are not RH-387 theorem inputs.
- The versioned arXiv author manuscript is locked by URL, PDF MIME, byte
  count, page count, and SHA-256. The source tar and its main.tex are
  separately locked.
- The arXiv nonexclusive license grants distribution to arXiv, not a
  general third-party republication right. The version of record is
  Copyright 2023 Elsevier Inc., all rights reserved. Neither external
  payload is included in the release.

## Mathematical integrity

- The endpoint is p>x. The Stieltjes boundary and both integral units are
  retained, yielding epsilon_x(2xh_r+J_r).
- The absolute error is summed over all r before any relative logarithm;
  no unbounded-order use of RH-386's per-r smallness condition occurs.
- Tonelli is applied only to nonnegative terms with c/(p^2-1)<=7/24<1.
- The exact-to-power integrand retains direction PhiJ>=PhiI and the
  denominator t^2(t^2-1-c), giving the 2c/3 bound.
- L>=512 is explicitly bridged to x>256 before the coordinate cube is
  used. No false x=23 cube assertion appears.
- The endpoint arrays, positive infinite products, 7 and 49/8 ledgers,
  derivative coefficients 2,4,4, and l_infinity/l_1 norm pairing are
  explicit.
- GapP, GapJ, and GapI are separately defined; every master bound retains
  pi^2.
- epsilon_x x^2 tends to infinity, so no second-order or P_2-scale
  precision is claimed.

## Artifact integrity

- The verifier uses exact integer/Boolean/string/object types and strict
  JSON parsing with duplicate and nonfinite rejection.
- compare_fresh=false performs field-level semantic recomputation and is
  regression-tested with the canonical builder disabled.
- Scalar-leaf mutation coverage is fail-closed, and all 24 genuine
  mathematical mutations are rejected.
- The official Draft 2020-12 schema is recursively closed; every object
  rejects extra properties and every array has an exact length.
- The 14 degree-four formal rows are reproduction fixtures and not
  evidence for the analytic infinite-order theorem.

## Source and archive integrity

The source closure is exactly 68 immutable Git blobs plus one canonical
remote logical lock. The logical digest is hard-gated. The external PDF,
source tar, and locked source-main payload hashes are absent from the
publication tree. The default remote verifier makes zero requests.

## Declarations audit

The manuscript includes data/code availability, author contributions,
funding, competing interests, ethics, and AI-assistance disclosures. No
human or animal subjects, personal data, clinical intervention, funding,
or competing interest is present.

## Verdict

The integrity review finds no fabricated result, unsupported
finite-to-analytic inference, source-license overreach, citation
laundering, or scope inflation. Final archive and PDF replay have zero
failures as recorded in the companion audit files.
