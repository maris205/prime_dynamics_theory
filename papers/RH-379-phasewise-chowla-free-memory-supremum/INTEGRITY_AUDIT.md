# RH-379 integrity and citation audit

## Audit scope and source lock

This audit follows the ARS integrity, citation-compliance, and
research-to-paper checks, subject to the repository's stricter source
firewall: the repository is the sole factual source.  No fresh web result is
introduced.  The executable result locks 28 immutable predecessor files
byte-for-byte: the README, theorem ledger, manuscript, bibliography, core, and
result ledgers of RH-374, RH-375, RH-376, and RH-378; the updated roadmaps of
RH-374 and RH-378; and the MVP2 summary and four-volume archive verification.
The five declared release commits are stored separately.  Mutable root policy
and handoff files govern the workflow but are deliberately excluded from the
publication source lock, so later endpoint updates cannot invalidate this
sealed paper.

The six bibliography keys used by the manuscript all resolve:

| Key | Claim role | Verification basis |
|---|---|---|
| `RH374` | square-clock support word, run counts, `B_y` and its limit | locked RH-374 manuscript, ledger, result, and core |
| `RH375` | one-site optimum, same-support value used only for the retained set, reverse supremum | locked RH-375 manuscript, ledger, result, and core |
| `RH376` | ordinary shift-two Chowla boundary | locked RH-376 manuscript, ledger, result, and core |
| `RH378` | lag-two interpolation and unphased classification | locked RH-378 manuscript, ledger, result, and core |
| `Davenport1937` | fixed arithmetic-progression Möbius cancellation | metadata and theorem usage copied from the locked repository bibliographies |
| `Mirsky1948` | squarefree-pattern progression densities | metadata and theorem usage copied from the locked repository bibliographies |

Every in-text key has one bibliography entry and every bibliography entry is
cited.  The two historical entries were not independently re-queried on the
web because that would violate the declared repository-only evidence rule;
the audit therefore certifies repository consistency, not a new external
bibliographic lookup.

## Claim-to-evidence audit

- The fixed-clock limiting formula is proved with the order
  `q fixed -> cutoff fixed -> N -> infinity -> cutoff -> infinity`.  No
  uniform-in-clock cancellation is inferred.
- The full `2^9=512` truth-table enumeration finds exactly 192 rows with
  `c11=0`, nine main coefficient pairs, and canonical counts
  `0/J/K/I = 120/40/24/8`.  The census serialization hash is
  `aaae39b0af85b13e7cc75baa7170a29f1ac60355443d7b80f3fee06d4af56121`.
- Canonical subset dominance is checked on every one of the 192 rows before
  the `K -> I` replacement.  Full incoming and outgoing compatibility is
  checked after canonicalization.
- Input reflection checks the coefficient sign rule for all 512 tables and
  compatibility for all `512^2=262144` ordered neighbor pairs; there are zero
  failures.
- The three-state cyclic max-plus solver and an independent cycle-MWIS solver
  agree at `q=1,...,6,36,180,900,44100`.  All comparisons are performed in
  the exact Euler-symbol basis with a certified interval used only to decide
  signs.
- Directed interval arithmetic treats subtraction correctly: for
  `q=2/p^2`, it forms `factor_low=1-q_high` and
  `factor_high=1-q_low`.  Exact `Fraction` products at four small prime
  cutoffs lie inside the returned interval.  A deliberately ambiguous
  Euler-symbol comparison raises `ArithmeticError`, confirming fail-closed
  behavior.
- Exact `q | Q` aggregation of both progression densities is checked on ten
  fibers of `Q=720`, including odd clocks and prime powers.
- The cofinal fixtures check the lifted score, retained/discarded exact
  decomposition, retained-set independence, one-site weights and `B_y`
  bound, and the unsupported-square precondition for discarded `J` phases.
  The analytic infinite-prime union bound remains a proof in the manuscript,
  not a finite numerical extrapolation.
- The result builder exposes a pure `build_payload()`; tests recompute the
  entire payload, compare its canonical JSON bytes with `result.json`, and
  recompute every source digest.  The Draft 2020-12 schema recursively fixes
  every substantive row shape.  Its only key-variable object is the 28-entry
  source map, whose exact membership is separately enforced by regeneration
  and tests.

## Seven failure-mode review

1. **Finite-to-asymptotic upgrade:** absent.  Decimal intervals and finite
   clock rows are explicitly reproduction-only.
2. **Average upgrade:** absent.  The first excluded term is the phase-weighted
   ordinary shift-two correlation; RH-376 is not promoted to ordinary
   Chowla cancellation.
3. **Endpoint or padding drift:** absent.  The first two padded sites are
   isolated as an `O(1)` term in the cofinal count.
4. **Safety shortcut:** absent.  Compatibility is the exact ordered
   composability test; canonical replacement uses subsets before `K -> I`.
5. **Model-class inflation:** absent.  The theorem is phasewise `c11(r)=0`
   at each fixed finite clock, not unrestricted or growing-clock memory.
6. **Same-support or attainment inflation:** absent.  Same-support saturation
   is invoked only for the retained one-site set.  No finite-clock attainment,
   nonattainment, or monotonicity of `Delta_y` is claimed.
7. **Spectral/RH inflation:** absent.  Gates A--E remain false/open; there is
   no operator, trace, zero identification, Hilbert--Pólya construction, or
   RH implication.

## Originality and disclosure checks

The manuscript states its dependency on the four locked predecessor papers
and separates imported inputs from the new phasewise census, optimizer,
square-clock correction, and cofinal proof.  Targeted repository phrase
review removed inherited wording that could suggest a uniqueness claim
stronger than RH-378: the manuscript now says that the displayed monomials
form a basis and that expansion in that basis is unique.  This is a scoped
repository comparison, not a claim of exhaustive similarity detection over
external literature.

The paper contains data, ethics, contribution, funding, competing-interest,
and AI-assisted-workflow declarations.  No human, animal, personal, or
biological data are used.

## Integrity verdict

**PASS for the declared repository release scope.**  The exact certificate,
source-lock regeneration, closed schema, and adversarial proof review leave
no known integrity blocker.  The first mathematical blocker outside scope is
phase-weighted shift-two `D2` cancellation.
