# RH Research Handoff

Status date: 2026-07-30

Current completed endpoint: RH-281

Completed research batch: RH-272 through RH-281

Research batch commit:
ac4e2105337737118410a32d6c1fe9c79f228ba3

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in /root/math/prime_dynamics_theory.

Before the next state-changing batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-281-ten-layer-counterloop-quotient-frontier-review/README.md
- papers/RH-281-ten-layer-counterloop-quotient-frontier-review/UPDATED_ROADMAP.md
- papers/RH-281-ten-layer-counterloop-quotient-frontier-review/results/result.json
- papers/RH-281-ten-layer-counterloop-quotient-frontier-review/main.pdf

The next result-driven batch starts at RH-282 only after a genuinely new
operator-level input.  More frozen endpoints, finite phase fits, or target-only
bounds do not activate either open tail/identification obligation.

### Chat and delegation discipline

- Keep the primary chat to conclusions, route choices, theorem boundaries,
  blockers, and final audit summaries.
- Delegate long numerical experiments, source scans, build logs, archive checks,
  and page-by-page PDF review; return compact verdicts and exact counts.
- Keep state changes, final integration, staging, and commits coordinated by the
  primary session.
- Preserve unrelated untracked caches, checkpoints, and TPC work.  Stage only
  the current RH batch and this handoff file.
- Pull with git pull --rebase origin main before every commit and again
  immediately before pushing.

## 2. Program objective and claim boundary

The project develops a conditional prime-dynamics route inspired by the
Hilbert--Polya program.  It is not a proof of the Riemann Hypothesis.

- Gate A: canonical intrinsic dynamical spectral determinant.
- Gate B: time-oriented scattering or unitary completion.
- Gate C: genuine self-adjoint generator and intrinsic T log T law.
- Gate D: von Mangoldt-weighted prime-power traces.
- Gate E: equality with the completed-zeta divisor.

All five gates are false/open.  No paper in RH-272--RH-281 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves a completed-zeta divisor equality, or implies RH.

## 3. Decision after RH-281

Current route coordinate:

    dual_counterloop_spectral_variable_rank_tail_open_complete_zero

The five obligations are

    (legal anchored head, coefficient bridge, uniform quotient tail,
     analytic target tail, certified target boundary constant).

They must now be recorded in two separate branches:

    noisy spectral quotient       = (false, false, false, true, true)
    graded monodromy counterloop  = (true,  true,  false, true, true)

The spectral branch satisfies two of five obligations.  The graded
counterloop branch satisfies four of five.  Both complete-certificate counts
are zero.

The first two counterloop entries are exact all-order fixed-coefficient
statements.  They do not identify the counterloop atoms as a spectral
submultiset of the noisy operator.  Consequently the noisy spectral ledger
does not flip.

## 4. Compact conclusions from RH-272 through RH-281

- RH-272: The weighted boundary monodromy gives a deterministic,
  operator-derived graded counterloop.  With
  beta=(r_H sqrt(lambda))^(-1)=0.908052360407104..., its exact moments are
  s_(k,n)=beta_k^n(2k 1_(2k|n)-1-(-1)^n).  Before the first alias at order
  2k, odd moments vanish and even moments are -2 beta_k^n.  Combining this
  with the fixed-order noisy flat-trace limit gives an exact coefficientwise
  bridge for every fixed order.  This is not noisy spectral identification.
- RH-273: In the zero-odd/even-pole-prefix class, matching through order 2N
  requires at least 2N counterloop atoms.  At equality the factor is uniquely
  Pi_N((beta z)^2), up to permutation of its atoms.  The proof explicitly
  includes S_1=0 and uses logarithmic coefficient uniqueness.
- RH-274: Fixed moments are controlled by aggregate l1 phase and radial
  defects.  Maximum phase error alone is insufficient: the common shift
  (N+1)^(-1/2) tends to zero pointwise while the third moment is asymptotic to
  -4 beta^3 sqrt(N+1)/pi.  The counterexample is logical, not a claim about
  the archived noisy family.
- RH-275: The seven RH-15 floating clouds have total root error
  0.6424--1.2481, N times mean root error 0.3212--0.6240, and maximum
  pre-alias moment defect 0.5096--1.4573.  These finite rows do not activate
  the RH-274 asymptotic hypothesis and do not prove actual nonconvergence.
- RH-276: For the natural folded Gaussian family
  A_sigma=r_H^(-1)K_sigma,
  sigma ||A_sigma||_(S_2)^2 tends to
  1/(2 sqrt(pi) r_H^2)=0.3904426183721497....  Hence raw zero-noise S_2
  convergence is impossible.  The independent unscaled square lower
  constant is 0.07003252620371733.  Rank-growing cancellation is not excluded.
- RH-277: On the natural stationary L2 complement the deterministic Koopman
  limit is an isometry.  Any finite-rank compression has the same Calkin
  class, so every power has norm at least one, and at least r_H^(-m) after
  Hardy scaling.  The archived selected rank range is 6--37.  Rank-growing
  selectors, growing block depth, and anisotropic spaces remain open.
- RH-278: The positive-noise folded Gaussian family is real analytic into
  S_2 on every compact interval away from zero.  An exact exterior spectral
  shell therefore has a local common contour, uniform resolvent bound,
  constant Riesz rank, and locally contractive quotient power.  This is a
  positive-noise local chart, not a uniform zero-noise theorem.
- RH-279: A direct variable-space block theorem gives
  |Tr C_sigma^n| <= K_sigma eta_sigma^(ell-1) L_sigma^r for
  n=ell m_sigma+r, together with the corresponding logarithmic tail bound.
  Tail vanishing requires the displayed bound itself to tend to zero; a
  convenient sufficient root-rate condition is
  limsup K_sigma^(1/m_sigma) R max(1,L_sigma R)<1.  No actual uniform
  variable-rank certificate is archived.
- RH-280: The dual ledger records spectral 2/5 and counterloop 4/5, with both
  complete counts zero.  Local positive-noise activation is not the required
  uniform small-noise tail.
- RH-281: The ten-layer review keeps the graded counterloop and noisy spectral
  quotient logically separate, closes the raw fixed-rank zero-noise route
  only in the stated natural L2 geometry, and identifies aggregate cloud
  transport plus a variable-rank tail certificate as the main executable
  frontier.

## 5. Route firewall and RH-282 reopening triggers

Do not promote deterministic or finite data beyond their hypotheses:

- The counterloop is a legal graded atomic superloop, not an identified noisy
  spectral submultiset.
- The exact coefficientwise counterloop bridge is not a noisy spectral-cloud
  coefficient bridge.
- The RH-275 seven-row audit is finite floating evidence, not an asymptotic
  theorem or interval root certificate.
- Raw S_2 divergence does not exclude cancellation after rank-growing
  deflation.
- The fixed-rank Calkin no-go is scoped to the natural stationary L2
  zero-noise geometry.
- A positive-noise local common contour does not glue to one uniform
  small-noise contour.
- Finite twelfth-power contractions do not supply the RH-279 variable-rank
  constants or their root-rate condition.
- No Gate A--E status changes follow from either incomplete ledger.

Admissible RH-282 inputs are:

1. An interval/asymptotic aggregate Fourier or root-transport theorem from the
   actual noisy cloud to the monodromy shell.
2. A genuine noisy spectral-submultiset identification for the counterloop
   atoms, with an ordinary determinant quotient justified at operator level.
3. A variable-rank, variable-block certificate satisfying the RH-279 trace
   norm, operator norm, prefix, and root-rate conditions uniformly as noise
   tends to zero.
4. An independent intrinsic noisy counterterm theorem proving the graded
   factor canonical without mislabeling it as spectral.
5. A rigorously specified anisotropic zero-noise package outside the natural
   L2 fixed-rank obstruction.

If no new input supplies one of these, publish a scoped route stop rather than
another finite fit or a global nonexistence claim.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-272--RH-281 audit:

- Tests: 28/28 passed across ten directories, with per-paper counts
  3,3,4,2,3,3,3,3,2,2.
- Individual archives: 10/10 verified with zero failures.  RH-272--RH-280
  manifests contain 15 publication files each; RH-281 contains 19.
- Batch archive: 154 publication files, zero failures.
- PDFs: pages 2,1,1,1,2,1,2,1,1,2 (14 total).  Every semantic PDF is byte
  identical to main.pdf.
- All ten LaTeX logs have zero errors, undefined citations/references, rerun
  warnings, overfull/underfull boxes, and empty-bibliography warnings.
- Every result JSON explicitly keeps Gate A--E false/open where the full gate
  map is represented; all boundary flags remain negative.
- The paper batch commit contains 176 files after adding per-paper and batch
  archive metadata.  RH_HANDOFF.md is committed separately so it records that
  batch commit exactly.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The compact review is
papers/RH-281-ten-layer-counterloop-quotient-frontier-review/.

## 7. Continuation prompt

    Continue RH research in /root/math/prime_dynamics_theory.  Run
    git status --short --branch and git pull --rebase origin main.  Treat the
    repository as the sole source of truth.  Read RH_HANDOFF.md and the
    RH-281 README, UPDATED_ROADMAP.md, result.json, and main.pdf.  Proceed to
    RH-282 only after a genuine operator-level reopening input: certified
    aggregate transport from the actual noisy cloud, a justified noisy
    spectral identification, or a variable-rank block-power certificate
    satisfying RH-279.  Keep the counterloop and spectral ledgers separate;
    finite fits are not all-order noisy theorems; Gates A--E remain
    false/open; do not imply a Hilbert--Polya operator, Riemann-zero
    identification, zeta-divisor equality, or RH.
