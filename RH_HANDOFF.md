# RH Research Handoff

Status date: 2026-07-30

Current completed endpoint: RH-271

Completed research batch: RH-262 through RH-271

Research batch commit:
94b0be4d6bd9f3f62a86892e22c4402b18d2ca02

The repository, not an old chat transcript, is the source of truth.

## 1. Fresh-session protocol

Work in /root/math/prime_dynamics_theory.

At the start of the next batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-271-ten-layer-deterministic-envelope-quotient-frontier-review/README.md
- papers/RH-271-ten-layer-deterministic-envelope-quotient-frontier-review/UPDATED_ROADMAP.md
- papers/RH-271-ten-layer-deterministic-envelope-quotient-frontier-review/results/frontier_review.json
- papers/RH-271-ten-layer-deterministic-envelope-quotient-frontier-review/main.pdf

The next result-driven batch starts at RH-272 only after a genuinely new
operator-level reopening input. A finite fit, another frozen endpoint scan,
or a target-only bound is not a reopening input for the cloud/quotient route.

### Chat and delegation discipline

- Keep the primary chat to conclusions, route choices, theorem boundaries,
  blockers, and final audit summaries.
- Delegate long numerical experiments, source scans, build logs, archive checks,
  and page-by-page PDF review; return compact verdicts and exact counts.
- Keep state changes, final integration, staging, and commits coordinated by the
  primary session.
- Preserve unrelated untracked caches, checkpoints, and TPC work. Stage only
  the current RH batch and this handoff file.
- Pull with git pull --rebase origin main before every commit and again
  immediately before pushing.

## 2. Program objective and claim boundary

The project develops a conditional prime-dynamics route inspired by the
Hilbert--Polya program. It is not a proof of the Riemann Hypothesis.

- Gate A: canonical intrinsic dynamical spectral determinant.
- Gate B: time-oriented scattering or unitary completion.
- Gate C: genuine self-adjoint generator and intrinsic T log T law.
- Gate D: von Mangoldt-weighted prime-power traces.
- Gate E: equality with the completed-zeta divisor.

All five gates are false/open. The batch remains inside Gate A. No paper in
RH-262--RH-271 constructs a Hilbert--Polya operator, identifies Riemann zeros,
proves a zeta-divisor equality, or implies RH.

## 3. Decision after RH-271

Current route coordinate:

    deterministic_target_envelope_sharp_legal_head_bridge_uniform_quotient_open_complete_zero

The RH-270 ledger has five independent obligations:

    (legal anchored head, coefficient bridge, uniform quotient tail,
     analytic target tail, certified target boundary constant)
    = (false, false, false, true, true).

Exactly two of five obligations are satisfied. The complete certificate count
is zero. This is scoped to presently archived components and is not a global
nonexistence theorem.

The deterministic target problem requested at the start of the batch is now
closed within its stated normalization: there is an exact all-order coefficient
anchor, a certified all-order envelope, and a sharp geometric base/radius. The
moving-cloud and quotient obligations remain logically separate.

## 4. Compact conclusions from RH-262 through RH-271

- RH-262: Arb replays at 100/150/200 decimal places certify
  M_(7/5)<107.906078<108 without angular sampling. With first omitted order
  29, the clean Cauchy logarithmic tail is <0.021866475 and multiplicative
  error is <0.022107298. The obligation vector becomes 2/5.
- RH-263: The deterministic coefficients have exact all-order parity formulas:
  for odd n>=3,
  a_n=(r_H lambda)^(-n)/(1+lambda^(-n)); for n=2k,
  a_(2k)=r_H^(-2k)[2 tr(T^k)+2 lambda^(-2k)/(1+lambda^(-k))
  -lambda^(-2k)/(1-lambda^(-2k))]. All 27 RH-253 rows through order 28
  cross-check with maximum floating residual 6.442918843840156e-14. The
  finite check is not a cloud bridge.
- RH-264: A direct factorwise interval argument certifies, at R=1 and N=29,
  even tail <0.000024488616, odd tail <0.000002136130, total logarithmic tail
  <0.000026624745, and multiplicative error <0.000026625100.
- RH-265: The factorwise method gives a certified first-omitted-order ladder
  N=13,21,29,37,45,53,61. The N=61 logarithmic tail is <7.175542e-11.
  Only N=29 is aligned with the archived order-28 head; higher rows are
  conditional interfaces, not constructed heads.
- RH-266: A finite-sample logical counterexample proves that pointwise
  contractions do not imply continuum uniformity without a modulus or interval
  family enclosure. The inherited audit has 23/23 contractive twelfth powers,
  0/23 one-step contractions, first contraction depths 3--9, and nine missing
  archived endpoints. Actual family nonuniformity is not proved.
- RH-267: The exact parity anchor and residue-class trace-ideal bounds give
  |a_n|<48 q_*^n for every n>=2, where
  q_*=1/(r_H lambda)=0.7008752258547757.... Certified residue constants are
  below 27.054, 47.538, and 37.062. This is the deterministic all-order trace
  envelope, not a moving-cloud envelope.
- RH-268: The base is sharp: a_n/q_*^n tends to 1. Therefore the logarithmic
  coefficient root rate is exactly q_*, the radius is exactly
  rho_*=1.4267874838640739..., no smaller all-order geometric base is possible,
  and the absolute logarithmic series diverges at the critical radius.
- RH-269: A precise sufficient theorem now handles quotient uniformity. Under
  S_2 convergence, a common finite-rank isolating contour, a uniform resolvent
  bound, and a contractive power of the limiting orthogonal quotient, the
  changing quotient spaces can be transported to one fixed complement;
  the compressions converge in S_2 and uniform RH-246 constants K_m,
  eta_m<1, and L_r follow. The archive verifies 0/4 hypotheses. This is a
  scoped non-activation result, not actual nonuniformity.
- RH-270: The updated ledger performs 111 source-consistency checks with zero
  failures. The coarse envelope-only order-29 tail is <0.000184751, while the
  direct RH-264 endpoint is more than 6.93 times tighter. The truth vector is
  (false,false,false,true,true), exactly 2/5, and complete count 0.
- RH-271: The review proves an exact root-of-unity shell separation theorem.
  An (N+1)-root complete shell has trace moments zero through order N and a
  freely unbounded moment at order N+1. For the current order-28 frontier, a
  29-root shell hides through order 28 and appears at order 29. Thus finite
  matching plus a sharp target envelope cannot replace a cloud bridge. The
  review records 187 structured records and 98 checks with zero failures; its
  batch archive verifies 172 publication files.

## 5. Route firewall and RH-272 reopening triggers

Do not promote deterministic or finite data beyond their hypotheses:

- The exact deterministic all-order envelope is not a moving-cloud envelope.
- The exact deterministic parity formulas do not identify a noisy selector.
- The RH-253 order-28 comparison is a finite regression check, not proof of a
  cloud coefficient bridge.
- Certified target tails do not supply a legal anchored head.
- The higher RH-265 tail rows are interfaces until matching heads exist.
- Twenty-three finite Schur contractions do not imply continuum uniformity.
- The root-of-unity shell theorem is a logical separation witness, not a claim
  that the archived family contains such a shell or is actually nonuniform.
- Activating RH-269 would close only the specified local quotient-tail
  obligation; it would not supply a legal head or coefficient bridge.
- No Gate A--E status changes follow from these target-side theorems.

The admissible RH-272 triggers are:

1. A legal invariant or operator-derived anchored head outside the currently
   obstructed selector classes.
2. An exact all-order cloud-to-deterministic coefficient bridge for that head,
   not a finite fit.
3. A continuum S_2 convergence theorem for the noisy operator family.
4. A common finite-rank isolating contour with a uniform resolvent bound.
5. A contractive power of the limiting orthogonal quotient.

Inputs 3--5 together activate the RH-269 uniform quotient criterion. They do
not replace inputs 1--2. If no new input supplies these obligations, publish a
scoped route stop rather than implying global nonexistence.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-262--RH-271 audit:

- Tests: 36/36 passed across ten directories.
- Individual archives: 10/10 verified, zero failures; RH-262--RH-270
  manifests contain 17 publication files each and RH-271 contains 19.
- Batch archive: 172 publication files, zero failures.
- PDFs: pages 3,2,2,2,2,2,2,2,4,4 (25 total); every semantic PDF is byte
  identical to main.pdf and all ten logs have zero errors, undefined
  citations/references, empty-bibliography warnings, rerun warnings, and
  overfull/underfull boxes.
- Every result JSON explicitly keeps Gate A--E false/open.
- The paper batch commit contains 194 files after adding the per-paper archive
  metadata; RH_HANDOFF.md is committed separately so it can record that batch
  commit exactly.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The next compact review is
papers/RH-271-ten-layer-deterministic-envelope-quotient-frontier-review/.

## 7. Next-session prompt

    Continue RH research. Enter /root/math/prime_dynamics_theory and run
    git status --short --branch followed by git pull --rebase origin main.
    The repository is the sole source of truth. Read RH_HANDOFF.md and the
    RH-271 README, UPDATED_ROADMAP.md, frontier_review.json, and main.pdf.
    Proceed to RH-272 only after a genuine operator-level reopening input:
    a legal anchored head with an exact cloud coefficient bridge, or the
    RH-269 continuum package (S_2 convergence, a common finite-rank isolating
    contour, uniform resolvent control, and a contractive limiting quotient
    power). Finite fits are not all-order cloud theorems; Gate A--E remain
    false/open; do not imply a Hilbert--Polya operator, Riemann-zero
    identification, zeta-divisor equality, or RH.
