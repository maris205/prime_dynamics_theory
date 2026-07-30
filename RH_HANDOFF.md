# RH Research Handoff

Status date: 2026-07-30

Current completed endpoint: RH-321

Completed research batch: RH-312 through RH-321

Research batch commit:
ca56920373223d396b23ce18c793c27572a4fa5a

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in /root/math/prime_dynamics_theory.

Before the next state-changing batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-321-ten-layer-endpoint-spectral-frontier-review/README.md
- papers/RH-321-ten-layer-endpoint-spectral-frontier-review/UPDATED_ROADMAP.md
- papers/RH-321-ten-layer-endpoint-spectral-frontier-review/results/result.json
- papers/RH-321-ten-layer-endpoint-spectral-frontier-review/main.pdf

The default RH-322 route is the joint first-alias boundary layer.  The other
legitimate route is an actual noisy-complement theorem proving fixed-order
coefficient transport together with endpoint energy tightness.  Synthetic
finite spectra, more tail bounds, and finite-prefix fits are not reopening
inputs.

### Chat and delegation discipline

- Keep the primary chat to conclusions, route choices, theorem boundaries,
  blockers, and final audit summaries.
- Delegate long numerical experiments, source scans, build logs, archive
  checks, and page-by-page PDF review; return compact verdicts and exact
  counts.
- Keep state changes, final integration, staging, and commits coordinated by
  the primary session.
- Preserve unrelated untracked caches, checkpoints, LaTeX intermediates, and
  TPC work.  Stage only the current RH batch and this handoff file.
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

All five gates are false/open.  No paper in RH-312--RH-321 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves completed-zeta divisor equality, or implies RH.

## 3. Decision after RH-321

Current route coordinate:

    endpoint_spectral_realizability_closed_actual_transport_open_first_alias_open

The two typed branches remain

    noisy modulus spectrum       = (true, false, true,  true, true)
    graded monodromy counterloop = (true, true,  false, true, true)
    weighted cross-branch glue   = false
    complete count               = 0

Their coordinatewise maximum is not a legal certificate.  The noisy spectral
complement and graded counterloop still belong to different determinant
decompositions.

The deterministic target inputs remain the all-order unified trace envelope
of RH-267 and the coefficient-anchor identities of RH-263/RH-268.  Finite
tables are reproduction checks only and are not promoted to all-order
theorems.

Use the constants

    q       = 0.5
    q_star  = 0.7008752258547759...
    rho_*   = 1.4267874838640735...
    R       = 1.4
    s       = q_star/q = 1.4017504517095518...
    d       = log(s) = 0.3377217782684642...
    sqrt(d) = 0.5811383469264992...

For the actual complement mismatch write

    g_sigma(z)
      = sum_(n>=2) (tau_(sigma,n)-a_n) z^n/n.

RH-312--RH-321 solve a synthetic finite-normal spectral extremal class.  They
do not prove that the actual noisy complement has the constructed spectrum,
matches even one fixed deterministic moment, or satisfies endpoint energy
tightness.  The batch is therefore a scoped spectral-realizability route
stop, not a reopening theorem.

The direct route now has an exact functional-analytic target.  Put

    e_(sigma,n)
      = (tau_(sigma,n)-a_n) rho_*^n/n.

Then actual endpoint H2 convergence is equivalent to both

    e_(sigma,n) -> 0 for every fixed n

and

    lim_(N->infinity) limsup_(sigma->0)
      sum_(n>N) |e_(sigma,n)|^2 = 0.

Neither statement is known.  In particular, the repository still contains
no theorem proving tau_(sigma,n) -> a_n for the actual complement at any
fixed order.

The default next route is therefore the first natural alias.  Its archived
critical slope is 1/log(lambda), and the alias, parity, and localization
contributions live at the same weighted order.  A successful theorem must
keep their joint cancellation and achieve error o(k R^(-2k)); separate
absolute majorants are insufficient.

## 4. Compact conclusions from RH-312 through RH-321

- RH-312: The endpoint-scaled deterministic numerator logarithm is exactly

      log(1-w) + w + H_reg(w),

  where H_reg is analytic for at least
  |w| < 1.0376199142321623.  This is an all-order deterministic theorem.

- RH-313: The universal logarithm splits into orthogonal even and odd Hardy
  channels.  Endpoint H2 convergence is equivalent to convergence of both
  parity projections, with an exact Pythagorean identity.

- RH-314: The degree-N Taylor projection is the unique best H2 polynomial
  approximation to the endpoint logarithm, with

      E_N^2 = sum_(n>N) n^(-2),    E_N ~ N^(-1/2).

  The analytic remainder is exponentially smaller.

- RH-315: A complete root packet for

      z^d = w/(dL),

  repeated L times, has zero moments below d, moment w at order d, and

      p_(md) = w^m/(dL)^(m-1).

  It is a genuine finite conjugate spectrum with integer multiplicities.

- RH-316: Triangular iteration of the packets realizes every finite real
  moment prefix exactly inside |mu| <= q.  Applied to the all-order
  deterministic anchors, it gives a synthetic finite normal realization for
  every prefix.  The numerical reproduction uses archived RH-263 anchors,
  not a q_star^n proxy.

- RH-317: Among finite spectra in |mu| <= q matching through order N, the
  least rank and least squared mass are both

      Theta((q_star/q)^N).

  The upper proof uses divisor sparsity: an e-packet affects order d only if
  e divides d, so every proper feedback order is at most d/2.

- RH-318: For the finite-spectral endpoint extremal problem,

      E_spec(M)^2 ~ d/log M,
      d = log(q_star/q).

  The actual mass cap gives only the universal class-sharp lower-rate bound

      liminf log(1/sigma) ||g_sigma||_H2(rho_*)^2 >= d.

  The lower scale tends to zero and proves neither convergence nor
  nonconvergence.

- RH-319: On every fixed 1.4 < rho < rho_*, the finite-spectral extremal
  H-infinity and H2 errors have optimal order

      Theta_rho(M^(-kappa(rho))/log M),

  with

      kappa(rho)
        = log(1/(q_star rho))/log(q_star/q).

  This upgrades RH-306 from abstract coefficient arrays to genuine finite
  normal power sums only.

- RH-320: Exact-prefix spectra plus one escaping packet give a synthetic
  sequence with eventual equality of every fixed moment, convergence on
  every strict radius, squared mass compatible with sigma^(-1), and endpoint
  H2 norm at least one.  Thus fixed moments and strict-annulus convergence do
  not imply endpoint convergence without energy tightness.

- RH-321: The ten-layer review records the batch as a scoped route stop.
  Both typed ledgers remain score four of five, cross-branch glue is false,
  complete count is zero, and Gates A--E remain open.

## 5. Route firewall and RH-322 reopening triggers

Do not promote the batch beyond its hypotheses:

- The endpoint logarithmic decomposition concerns the deterministic target,
  not the actual noisy complement.
- Polynomial approximation and finite-prefix realization are extremal
  information-class theorems, not noisy spectral transport.
- Integer-multiplicity normal matrices are synthetic.  They are not
  eigenvalue models identified with the transfer operator.
- The Theta rank and mass laws concern optimal finite realizations.  They are
  not actual noisy rank or complement-mass asymptotics.
- The constant d/log M is sharp for the finite spectral class.  The actual
  consequence is a lower-rate restriction only.
- Strict-annulus saturation does not prove actual annular convergence.
- The escaping packet disproves logical sufficiency of coarse axioms only.
  It does not prove actual endpoint nonconvergence.
- No Gate A--E status change follows from the synthetic class.

Admissible RH-322 inputs are:

1. An actual theorem proving tau_(sigma,n) -> a_n for every fixed n together
   with endpoint coefficient-energy tightness, or a direct proof that
   ||g_sigma||_H2(rho_*) tends to zero.
2. A joint moving-order first-alias boundary-layer trace law including
   parity, the neighboring shell, and the remainder, with total error
   o(k R^(-2k)).
3. A growing-clock actual head-transport theorem synchronized with an
   alias-inclusive full-trace law on the same clock.

If none is available, publish a scoped local theorem or explicit model
failure.  Do not advertise a local half-line Gaussian profile, an isolated
cycle calculation, or a finite numerical fit as the joint first-alias law.

### Default RH-322--RH-331 route

The preferred next batch is a joint first-alias program:

1. RH-322: certified half-line Gaussian profile for one critical folded row;
2. RH-323: paired affine Gaussian chain for the two critical contacts;
3. RH-324: curvature and normalization remainder for a single critical leg;
4. RH-325: moving-order Duhamel composition criterion on k asymptotic to
   log(1/sigma);
5. RH-326: parity-renormalized first-alias packet identity;
6. RH-327: neighboring-shell coupling and same-order cancellation budget;
7. RH-328: joint alias/parity/shell matching equation;
8. RH-329: validated isolated-model audit, with a scoped negative result if
   the matching equation fails;
9. RH-330: full-trace transfer criterion retaining joint cancellation;
10. RH-331: ten-layer first-alias frontier review.

Each paper must retain its own theorem, counterexample, validated numerical
finding, or scoped negative result.  Local model theorems remain local until
the full joint trace replacement is proved.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-312--RH-321 audit:

- Tests: 46/46 passed across ten directories, with per-paper counts
  4,4,4,5,5,5,5,4,6,4.
- Individual archives: 10/10 verified with zero failures.  RH-312--RH-320
  manifests contain 15 publication files each; RH-321 contains 19.
- Batch archive: 154 publication files, zero failures.
- PDFs: per-paper page counts are 2,1,1,1,1,2,2,1,2,2, for 15 pages total.
  Every semantic PDF is byte identical to main.pdf and every PDF has
  extractable text.
- All ten LaTeX logs have zero errors, undefined citations/references, rerun
  warnings, and overfull/underfull boxes.
- Ghostscript parsed 10/10 PDFs; all fonts are embedded.
- Page-by-page visual review found no clipping, overlap, anomalous blank page,
  formula or table overflow, footer conflict, or rendering anomaly.
- All 10 result JSON files parse, contain complete Gate A--E ledgers, and keep
  all 50 gate values false.
- RH-321 records reopening_trigger_supplied=false,
  scoped_spectral_route_stop=true, weighted cross-branch glue false,
  complete count zero, and all Hilbert--Polya, Riemann-zero, von-Mangoldt,
  zeta-divisor, and RH flags false.
- The paper batch commit contains 176 files after adding per-paper and batch
  archive metadata.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The compact review is
papers/RH-321-ten-layer-endpoint-spectral-frontier-review/.

## 7. Continuation prompt

    Continue RH research in /root/math/prime_dynamics_theory.  Run
    git status --short --branch and git pull --rebase origin main.  Treat the
    repository as the sole source of truth.  Read RH_HANDOFF.md and the
    RH-321 README, UPDATED_ROADMAP.md, result.json, and main.pdf.  Start
    RH-322 on the joint first-alias route: first certify the local critical
    half-line Gaussian row profile, but keep it explicitly model/local until
    parity, neighboring-shell cancellation, and the moving-order remainder
    are combined with error o(k R^(-2k)).  The alternative legitimate route
    is actual complement coefficient transport plus endpoint energy
    tightness.  Synthetic spectra, finite prefixes, and extra tail bounds are
    not reopening inputs.  Keep Gates A--E false/open and do not imply a
    Hilbert--Polya operator, Riemann-zero identification, zeta-divisor
    equality, or RH.
