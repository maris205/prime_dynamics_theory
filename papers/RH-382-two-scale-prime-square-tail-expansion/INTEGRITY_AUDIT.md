# RH-382 integrity audit

This audit applies the repository-only ARS research-to-paper and claim
verification workflow. Repository releases are the sole factual sources;
no web result or uncited external theorem was introduced.

## Claim verification matrix

| Claim | Source or proof location | Verification |
|---|---|---|
| Fixed-clock phasewise `c11=0` class | RH-379/RH-380/RH-381 frozen releases | Source hashes and release blobs locked |
| Exact infinite increment sum | RH-381 `main.tex`, result, core | Predecessor check and direct symbolic restatement |
| Run formula and terminal `R8=P E8` | RH-374 frozen release | Exact run rows; terminal ledger |
| `E9=0`, no `E10` | RH-382 Lemma 2.1 and core | Exact `Fraction` rows; source never constructs `E10` |
| Bonferroni/inverse-product inequalities | RH-382 Lemmas 3.1--3.2 | All-order finite-product proof and monotone passage |
| `931/4` numerator remainder | Proposition 3.3 | Exact five-term ledger |
| `63` memory convergence | Proposition 3.3 | Exact six-term ledger |
| `H` quadratic loss | Equation (4.3) | Bonferroni bound |
| Quadratic and cube telescopes | Lemma 4.1 | Finite identities followed by nonnegative limits |
| `3301/6<551` cubic remainder | Theorem 5.1 | Exact `Fraction` ledger and tests |
| Opposite `S_y` signs | Equations (5.2), (5.5) | Separate current/next-tail identities |
| `p=71` wrong-sign rejection | Exact artifact only | Correct ratio `0.042746...`; memory-only flip `7.335622...`; difference `4mS` |

## Source integrity

- Immutable inputs: 33 unique files.
- Group split: RH-374 `7`; RH-379 `8`; RH-380 `8`; RH-381 `8`;
  RH-MVP2 `2`.
- Aggregate digest:
  `7b62b7e77ad313a52a07851e700aff197c2cc4bc3d910c6a464cd3cec0b55cb6`.
- RH-381 group digest:
  `5d07b1b897aa36127f2f190517229534719f37ce0f3ff904d1c31adebae6c9df`.
- Every live file is checked against the exact blob at its declared commit.
- Mutable `AGENTS.md` and `RH_HANDOFF.md` are explicitly excluded.

## Research-integrity controls

- Finite rows are labeled reproduction-only and are never cited as proof of
  an all-`y` assertion.
- No p-value, statistical fit, or selectively reported regression appears.
- The exact wrong-sign mutation is distinguished from the different
  numerator `YS` mutation.
- Exact arithmetic is used for every coefficient and diagnostic comparison;
  decimal strings are display-only and generated under an explicit local
  context independent of ambient rounding.
- Result JSON rejects duplicate keys and non-finite constants. The generated
  Draft 2020-12 schema is recursively closed and exact.
- Optimized `-OO` execution retains all release checks.

## Boundary verification

The manuscript states, and the result records, that there is no PNT or
`p_y` rewrite, no `q(N)`, no active-`c11` theorem, no adaptive-capacity
limit, no intrinsic operator or determinant, no von Mangoldt trace, no zero
identification, no Hilbert--Polya construction, and no RH implication.
Gates A--E are false/open.

## Disclosure

The manuscript includes data/code availability, author contributions,
funding, competing interests, ethics, and AI-assistance declarations. No
human participants, private data, or undisclosed external funding are used.
