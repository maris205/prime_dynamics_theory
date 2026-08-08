# RH-386 research-integrity audit

## Source integrity

- Primary source: Daniel R. Johnston and Andrew Yang, *Some explicit
  estimates for the error term in the prime number theorem*, JMAA 527(2),
  article 127460 (2023), DOI `10.1016/j.jmaa.2023.127460`.
- The proof uses Theorem 1.4 equation (1.8), with domain `x>=23`.
- Corollary 1.2 equation (1.5) and Table 1 row `X=log 2` are provenance
  locators only; no derived `172 exp(-0.4 sqrt(log x))` result is claimed.
- The versioned arXiv author manuscript is locked by URL, MIME, byte count,
  page count, and SHA-256. The source tar and its `main.tex` are separately
  locked.
- The arXiv nonexclusive license grants distribution to arXiv, not a
  general third-party republication right. The version of record is
  Copyright 2023 Elsevier Inc., all rights reserved. Neither external
  payload is included in the release.
- Two source-text issues outside the RH-386 proof are recorded: the
  Section 5.2 `Corollary 1.5` cross-reference and the arXiv-v2 equation
  (1.9) `pi(x)-x` text corrected to `pi(x)-li(x)` in the version of record.

## Mathematical integrity

- The strict endpoint `p>x` is enforced both by the negative Stieltjes
  boundary and by the exact successor identity.
- The source transfer retains all three units `boundary_xh`, `integral_xh`,
  and `integral_J`; this yields `2xh+J` and constants `6r+1`, `7r`, `14r`.
- The canonical middle ledger is `r/(x^2-1)` and requires no smallness
  assumption. The older `4r/x^2` expression is labelled a coarse corollary.
- The Laplace transform retains rate `2r-1`, Jensen direction, exponential
  moments 1 and 2, and the signed correction `-H/L`.
- The leading condition uses `H`, not degree alone. The all-ones family
  gives the non-unit limit `exp(-c)`.
- `d epsilon_x` is described as a robust sufficient payment from a source
  upper bound, not as a necessary condition on the actual signed error.

## Artifact integrity

- The verifier uses exact integer/Boolean/string/object types and strict
  JSON parsing with duplicate and nonfinite rejection.
- `compare_fresh=False` performs field-level semantic recomputation and is
  regression-tested with the canonical builder disabled.
- Every one of 1,522 scalar leaves is mutated independently; none escapes.
- The 24 theorem mutations are distinct from the 7 auxiliary metadata and
  JSON attacks.
- The official Draft 2020-12 schema is recursively closed; every object
  rejects extra properties and every array has exact tuple length.
- RH-384's 66 partition rows are reproduction-only and are not treated as
  evidence for the new analytic theorem.

## Declarations audit

The manuscript includes data/code availability, author contributions,
funding, competing interests, ethics, and AI-assistance disclosures. No
human or animal subjects, personal data, clinical intervention, funding,
or competing interest is present.

## Verdict

The integrity review finds no fabrication, unsupported finite-to-analytic
inference, source-license overreach, citation laundering, or scope
inflation. Fresh archive and PDF replay are complete with failure count
zero, as recorded in the companion audit files.
