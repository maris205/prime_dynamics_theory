# RH Research Handoff

Status date: 2026-08-03

Current completed endpoint: RH-351

Completed research batch: RH-342 through RH-351

Research batch publication commit:
`99d9fad06d44843ac24b9ccdb15bda09179cccf6`

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in `/root/math/prime_dynamics_theory`.

Before the next state-changing paper:

```bash
git status --short --branch
git pull --rebase origin main
```

Read these entry points completely before older papers:

- `AGENTS.md`
- `RH_HANDOFF.md`
- `papers/RH-351-ten-layer-signed-completion-frontier-review/README.md`
- `papers/RH-351-ten-layer-signed-completion-frontier-review/UPDATED_ROADMAP.md`
- `papers/RH-351-ten-layer-signed-completion-frontier-review/results/result.json`
- `papers/RH-351-ten-layer-signed-completion-frontier-review/main.pdf`

The default next investigation is the actual moving-order signed remainder
on the RH-350 triangular lower-even window.  It must work with

```text
m_(k,j)=k-j,                    2<=j<=J_k,
J_k->infinity,                  J_k=o(k),
Y_(k,j)=T_(k,m_(k,j))^rest-d_(sigma,k,2m_(k,j)),
p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j).
```

The next numbered paper is not activated by RH-351 alone.  It requires a
new theorem for the **actual** signed `Y` family, an actual critical or
first-lower combined complement, actual head transport, a full signed
off-alias aggregate, or a direct physical annular theorem.  Another abstract
completion, finite fit, scalar fixture, or inactive criterion is not a
reopening input.

The alternative direct route remains an aggregate theorem for

```text
g_sigma(z) = sum_(n>=2) (tau_(sigma,n)-a_n) z^n/n
```

on one certified annulus `1.4 < rho < r_H*lambda`.  RH-300 proves that a
vanishing `H-infinity` or `H2` norm there would close the direct weighted
prefix.  No such actual noisy annular theorem is currently proved.

### Codex agent pipeline

The durable orchestration rules are in `AGENTS.md` and the descriptive role
profiles are in `.codex/agents/`.

- The primary agent is the RH project lead and the only route, handoff, git,
  integration, and publication owner.
- At most three subagents run concurrently: `rh-source-lock`,
  `rh-proof-auditor`, and one exclusive `rh-paper-writer` after a primary
  `GO`.
- Once a draft exists, `rh-release-qa` replaces one read-only station; it is
  not a fourth concurrent subagent.
- Read-only scouting for RH-(N+1) may overlap the RH-N writer, but RH-(N+1)
  is not activated until RH-N creates the required theorem edge.
- Subagents return compact evidence, exact counts, and executable blockers.
  They never commit, push, modify `RH_HANDOFF.md`, or edit overlapping paper
  directories.
- As long as a repository-backed route exists, continue without requesting
  per-paper approval.  Stop with `STOP_SCOPED` or `NOT_TESTABLE` when the
  exact route conditions fail; do not manufacture the next number.

Preserve unrelated untracked caches, checkpoints, LaTeX intermediates, and
all TPC work.  Stage only the active RH paper/batch, its archive metadata,
approved agent configuration, and this handoff when a batch closes.

Pull with `git pull --rebase origin main` before every commit and again
immediately before every push.

## 2. Program objective and claim boundary

The project develops a conditional prime-dynamics route inspired by the
Hilbert--Polya program.  It is not a proof of the Riemann Hypothesis.

- Gate A: canonical intrinsic dynamical spectral determinant.
- Gate B: time-oriented scattering or unitary completion.
- Gate C: genuine self-adjoint generator and intrinsic `T log T` law.
- Gate D: von Mangoldt-weighted prime-power traces.
- Gate E: equality with the completed-zeta divisor.

All five gates are false/open.  No paper in RH-342--RH-351 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves completed-zeta divisor equality, or implies RH.

The inherited typed branch ledgers, in coordinate order

```text
(head, bridge, tail, target, boundary)
```

remain

```text
noisy modulus spectrum       = (true, false, true,  true, true)
graded monodromy counterloop = (true, true,  false, true, true)
weighted cross-branch glue   = false
complete count               = 0
```

Their coordinatewise maximum is not a legal certificate.  The noisy
spectral complement and graded counterloop still belong to different
determinant decompositions.

The deterministic target inputs remain exact and all-order:

- RH-263 proves the deterministic numerator coefficient anchor at every
  order;
- RH-267 proves `|a_n| < 48 q_*^n` for every `n>=2`;
- RH-268 proves `a_n/q_*^n -> 1` and the sharp target radius.

This closes only the deterministic target side.  It does **not** close the
RH-241 moving cloud-extracted uniform envelope, the no-over-extraction
coefficient bridge, a moving noisy coefficient theorem, or Gate A.  RH-350's
growing lower-even deterministic/scalar uniformity is not a substitute for
the RH-241 moving noisy all-order envelope.  Finite tables reproduce formulas
only; they are never promoted to physical or all-order asymptotics.

## 3. Decision after RH-351

Current route coordinate:

```text
actual_growing_lower_even_signed_remainder_open
```

Use the physical natural clock and Hardy normalization

```text
k = log(1/sigma)/(2 log(lambda)) + O(1)
eta_k = k-log(1/sigma)/(2 log(lambda))
H_m = m R^(-2m),                   R=7/5
x = (beta R)^2 > 1
x lambda = (R/r_H)^2 = (28/17)^2 > 2.
```

On every triangular window

```text
m_(k,j)=k-j,                       2<=j<=J_k,
J_k->infinity,                     J_k=o(k),
```

RH-348 gives the exact direct coefficient

```text
p_(k,j)=Y_(k,j)+P_(k,j)-S_(k,j),
Y_(k,j)=T_(k,m_(k,j))^rest-d_(sigma,k,2m_(k,j)).
```

RH-350 proves the unconditional deterministic/scalar uniform laws

```text
sup_j |C_M S_(k,j)/(2 H_m x^m)-1| -> 0,
sup_j |C_M P_(k,j)/(2 H_m x^m)-a_k lambda^(2-j)| -> 0,
a_k=C_* C_M lambda^(eta_k-2).
```

For

```text
F_N(a)=sum_(r=0)^N x^(-r)|a lambda^(-r)-1|,
```

the exact weighted minimax is attained uniquely at `a=1` and equals

```text
A_N=(1-x^(-N))/(x-1)-(1-(x lambda)^(-N))/(x lambda-1),
A_N -> A_infinity=1/(x-1)-1/(x lambda-1)>0.
```

Define the normalized selected budgets

```text
L_k(Y)=x^(-(k-2)) sum_(j=2)^(J_k)
       |Y_(k,j)+P_(k,j)-S_(k,j)|/(2H_(m_(k,j))),

Yagg_k(Y)=x^(-(k-2)) sum_(j=2)^(J_k)
          |Y_(k,j)|/(2H_(m_(k,j))).
```

RH-351 proves a growing-depth coefficient-ledger information-class theorem.
For any formal residual array `r`, the affine completion

```text
Y=S-P+r
```

gives `p=r` exactly.  In particular, the same proved `P/S` arrays admit

```text
close ledger: Y=S-P,  p=0,
far ledger:   Y=0,    p=P-S.
```

They obey the exact budget exchange

```text
Yagg_k(close)=L_k(far),
Yagg_k(far)=L_k(close)=0.
```

The RH-350 uniform laws give algebraically

```text
L_k(far)=F_(J_k-2)(a_k)/C_M+o(1),
liminf L_k(far)>=A_infinity/C_M>0.
```

Thus the far ledger has an unnormalized selected subprefix diverging at
least on the `x^(k-2)` scale, while the close ledger vanishes identically on
the selected window.  The close ledger correspondingly has a non-small `Y`
budget, so there is no contradiction with RH-350's conditional theorem.

These are abstract signed coefficient arrays, not two physical noisy
operators, Markov kernels, raw trace partitions, or determinant
realizations.  No physical realizability or impossibility theorem is
asserted.  The actual `Y` family remains unestimated.  Therefore current
proved information determines neither physical selected-window closure nor
nonclosure.

The earlier same-clock physical obligations also remain open:

```text
D_(4k) -> 0,
critical signed completion at n=2k,
first-lower signed completion at n=2k-2,
odd-order control,
upper-alias control on 2k<n<4k,
full signed E_off,(4k).
```

RH-340 still closes both analytic tails at `u=4k`, but tail closure alone
does not activate RH-288.

## 4. Compact conclusions from RH-342 through RH-351

- **RH-342:** Locks the actual noisy head and graded counterloop in one Hardy
  normalization, proves an exact zero-padding rank lower bound and shifted
  moment recovery under a rank cap, and gives a hidden `4k`-shell
  information-class counterexample.  Actual head-rank identification and
  root transport remain open.

- **RH-343:** Equal rank, squared spectral mass, cap, maximum modulus, normal
  realizability, and eventual fixed-order data do not determine the moving
  strict-prefix budget.  The two finite normal spectra are not physical noisy
  operators.

- **RH-344:** Completes the physical critical boundary-orbit extraction at
  `n=2k`.  The full atom differs from the earlier partial atom by a
  super-target point and creates an exact double-alias-sized compensation
  demand.  The orbit-free rest and head defect remain unestimated.

- **RH-345:** Off the unique critical scalar balance phase, actual critical
  divergence follows conditionally from `Y_k=o(H_k)`.  At balance, the scalar
  parity information class is underdetermined at target scale.  No actual
  critical verdict follows.

- **RH-346:** Completes the physical boundary-orbit extraction at the first
  lower sideband `2k-2`, including the exact radial sideband and its lower
  relative scale.  The actual combined signed remainder remains open.

- **RH-347:** Off the first-lower scalar balance phase, physical divergence
  follows conditionally from the named actual remainder hypothesis.  At
  balance, scalar parity data remain underdetermined.  The scalar completions
  are not noisy operators.

- **RH-348:** Extracts the complete punctured lower-even boundary-orbit ladder,
  proves its geometric aggregate asymptotic, bounds the radial ladder as
  lower order, and derives a necessary divergent signed-supply law.  No
  source estimates the actual supply.

- **RH-349:** A single bounded phase cannot balance the fixed `j=2,3`
  sidebands.  The exact relative and physical weighted minimax values are
  proved, but exponential direct-subprefix divergence remains conditional on
  two unproved actual remainder estimates.

- **RH-350:** Extends the demand and parity laws uniformly to
  `J_k->infinity`, `J_k=o(k)`, proves exact finite-depth and physically
  weighted minimax families, and derives a conditional growing selected
  subprefix obstruction.  The actual aggregate `Y` hypothesis is unproved.

- **RH-351:** Proves affine completion surjectivity and opposite close/far
  growing-depth coefficient ledgers with exact budget exchange and a positive
  far normalized lower bound.  This is an information-class insufficiency
  theorem, not a physical realization theorem.

## 5. Route firewall and actual reopening triggers

Do not promote the batch beyond its hypotheses:

- RH-342's hidden shell and RH-343's equal-invariant spectra are finite
  normal information-class objects, not noisy quadratic operators.
- A physical boundary-orbit atom is not a lower bound for its fully signed
  coefficient.
- The RH-345, RH-347, RH-349, and RH-350 physical divergence statements are
  conditional on named actual remainder hypotheses.
- `Y=0` and `Y=S-P` in RH-351 are formal coefficient ledgers, not physical
  noisy remainder theorems.
- The close ledger does not satisfy the RH-350 small-`Y` hypothesis; its `Y`
  budget equals the positive far residual budget.
- A selected lower-even subprefix is not the full strict prefix or full
  `E_off` aggregate.
- Growing deterministic/scalar uniformity on `J_k=o(k)` is not the RH-241
  moving noisy all-order envelope or coefficient bridge.
- Tail closure and an inactive criterion do not activate RH-288 or Gate A.
- Finite rows are reproduction checks, never asymptotic or physical evidence.

Admissible reopening inputs are:

1. An actual moving-order theorem for `Y_(k,j)` on one
   `J_k->infinity`, `J_k=o(k)` window.  In particular, proving

   ```text
   Yagg_k(Y_actual) -> 0
   ```

   would activate RH-350 and prove genuine physical divergence of the
   selected lower-even subprefix.  Conversely, proving

   ```text
   sum_(j=2)^(J_k) |Y_actual-(S-P)|/(2H_m) -> 0
   ```

   would close only that selected subprefix and not the remaining prefix.

2. A physical moving-order theorem for the critical combined complement at
   `n=2k`, proving compensation or a nonzero target-normalized failure.

3. A physical moving-order theorem for the first-lower combined complement
   at `n=2k-2`, proving compensation or a nonzero target-normalized failure.

4. Actual noisy-head/counterloop transport proving `D_(4k)->0` in the same
   Hardy normalization, or a genuine physical obstruction.

5. An alias-inclusive signed theorem for odd orders, upper-alias orders, and
   the remaining `E_off,(4k)` background.

6. A direct aggregate annular theorem for `g_sigma` on one certified
   `1.4<rho<r_H*lambda` annulus.

7. Only after the direct prefix and both analytic tails close in one physical
   determinant data type may RH-288 be activated; Gate A still separately
   requires a canonical intrinsic physical determinant.

If a positive route fails, publish only a theorem-backed local obstruction,
an explicit physical counterexample, or a precise `NOT_TESTABLE` stop.  Do
not fill the next paper with another abstract completion, finite fit,
wrong-clock comparator, nonphysical similarity family, separate absolute
majorant, or restatement of an inactive criterion.

## 6. Default RH-352 investigation

RH-352 is a read-only investigation until a theorem edge is found.  Its
source-lock order is:

1. Freeze the exact actual types of
   `T_(k,m)^rest`, `d_(sigma,k,2m)`, `P_(k,j)`, and `S_(k,j)` on the same
   `(sigma,k)` clock and RH-334 direct coefficient data type.
2. Search the repository for cross-order identities, sign constraints,
   trace-partition conservation laws, contour/Fourier formulas, or operator
   estimates that genuinely restrict the actual `Y_(k,j)` array.
3. Test separately the aggregate small-`Y` route, the exact cancellation
   route, and any intermediate theorem with a new rigorous scale.
4. Audit whether a candidate controls a growing `J_k=o(k)` window rather than
   finitely many fixed sidebands.
5. Keep the critical, first-lower, head, odd, upper-alias, and full `E_off`
   obligations separate.
6. Issue `GO` only for an actual theorem, a genuine physical obstruction, or
   another strict scoped result.  If the source contains no such estimate,
   return `NOT_TESTABLE` and do not create RH-352.

The direct annular route may supersede this coefficientwise investigation if
a genuine actual theorem is found.

## 7. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
```

Final RH-342--RH-351 audit:

- Tests: 187/187 passed across ten independent directories, with per-paper
  counts `19,22,18,16,20,19,17,18,22,16`.
- RH-351 result regeneration is deterministic.  Its tests check affine
  completion surjectivity, exact budget exchange, strict input types, the
  RH-241/deterministic separation, all upstream Gate ledgers, and the claim
  firewall.
- Individual archives: 10/10 verified with zero failures.  RH-342--RH-350
  contain 15 publication files each; RH-351 contains 19.
- Batch archive: 154 publication files, zero failures.
- The ten controlled paper trees contain 176 files after individual and batch
  archive metadata.
- PDFs: page counts are `7,6,6,4,5,5,5,5,6,5`, for 54 pages total.  All ten
  semantic PDFs are byte-identical to `main.pdf` and have extractable text.
- Ghostscript parsed 10/10 PDFs.  All 181 reported font rows are embedded.
- All ten LaTeX logs have zero warnings, undefined citations/references,
  rerun notices, and overfull/underfull boxes.
- Page-level review of all five RH-351 pages found no clipping, overlap,
  blank-page anomaly, formula/table overflow, footer conflict, or rendering
  defect.
- Strict JSON parsing passed for 32/32 result/archive files with no duplicate
  keys or nonfinite values.
- The nine upstream result files contain 45 false Gate values; RH-351 adds
  five more, for 50/50 false.
- Unrelated caches, checkpoints, LaTeX intermediates, and TPC work remain
  untracked and unstaged.

RH-351 result SHA-256:
`a9b37a1e235fe66842812f7e515d22f8833276aea0444d62596ca1f042a641d7`

RH-351 PDF SHA-256:
`56e8e6fa5d16de8995ef88302045673ba2adf67bfd71bdf62ff573b5bd58ab75`

RH-342--RH-351 batch manifest SHA-256:
`4797b64fba4e6b3a99ab5acca8197b5ef8817f67f4d9cf8f962ddc89ec8ea3b9`

RH-342--RH-351 batch verification SHA-256:
`e62e61cfd028ee07d0a50b8bdd61147362da20acb9b49ff802d9236a68001516`

The compact review is
`papers/RH-351-ten-layer-signed-completion-frontier-review/`.

## 8. Continuation prompt

```text
Continue RH research in /root/math/prime_dynamics_theory.  Treat the
repository as the sole source of truth.  Read AGENTS.md, RH_HANDOFF.md, and
the RH-351 README, UPDATED_ROADMAP.md, result.json, and main.pdf completely.
Run git status --short --branch and git pull --rebase origin main.  Begin with
a read-only RH-352 source lock on the actual growing lower-even signed
remainder Y_(k,j)=T_(k,m)^rest-d_(sigma,k,2m) for
m=k-j, 2<=j<=J_k, J_k->infinity, J_k=o(k).  Use the primary agent plus at
most three subagents: source lock, adversarial proof audit, and one exclusive
paper writer only after GO; replace one station with release QA after a
draft.  Create RH-352 only if the repository supports an actual moving-order
theorem, a genuine physical obstruction, or another strict scoped result.
Do not turn the RH-351 abstract completions into physical operators, do not
promote RH-350's conditional theorem without the actual Y hypothesis, do not
identify the selected lower-even window with full E_off, and do not activate
RH-288 or Gates A--E without every exact hypothesis.
```
