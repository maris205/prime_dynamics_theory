# RH Research Handoff

Status date: 2026-07-30

Current completed endpoint: RH-301

Completed research batch: RH-292 through RH-301

Research batch commit:
7429c877079a33a065d8bf5f8483a9a1fe7a12b3

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in /root/math/prime_dynamics_theory.

Before the next state-changing batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-301-ten-layer-weighted-prefix-frontier-review/README.md
- papers/RH-301-ten-layer-weighted-prefix-frontier-review/UPDATED_ROADMAP.md
- papers/RH-301-ten-layer-weighted-prefix-frontier-review/results/result.json
- papers/RH-301-ten-layer-weighted-prefix-frontier-review/main.pdf

The next result-driven batch starts at RH-302 only with one of two genuine
inputs: an actual annular aggregate theorem for the noisy complement, or the
two synchronized typed estimates on the RH-292 minimal logarithmic clock.
Additional tail estimates, finite endpoint fits, pre-alias-only formulas, or
rate-free selected clocks do not activate the remaining determinant
interface.

### Chat and delegation discipline

- Keep the primary chat to conclusions, route choices, theorem boundaries,
  blockers, and final audit summaries.
- Delegate long numerical experiments, source scans, build logs, archive
  checks, and page-by-page PDF review; return compact verdicts and exact
  counts.
- Keep state changes, final integration, staging, and commits coordinated by
  the primary session.
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

All five gates are false/open.  No paper in RH-292--RH-301 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves a completed-zeta divisor equality, or implies RH.

## 3. Decision after RH-301

Current route coordinate:

    tail_absorbed_annular_prefix_open_complete_zero

The two typed branches remain

    noisy modulus spectrum       = (true, false, true,  true, true)
    graded monodromy counterloop = (true, true,  false, true, true)
    weighted cross-branch glue   = false
    complete count               = 0

Their coordinatewise maximum is all true but is not a legal certificate.
The noisy spectral complement and the graded counterloop still belong to
different determinant decompositions.

Put

    R = 7/5,
    L_sigma = log(1/sigma),
    a_* = 1/log(10/7) = 2.803673252057129...,
    h_sigma = ceil(a_* L_sigma),
    m_sigma = ceil(4 L_sigma).

For orders n at least two, write

    c_(sigma,n) = h_(sigma,n) + tau_(sigma,n),

where c is the total noisy bulk trace, h is the modulus-complete head moment,
and tau is the normal spectral-complement trace.  Let s_(k_sigma,n) be the
exact finite-radius counterloop moment and a_n the deterministic numerator
anchor.  The typed identity remains

    tau_(sigma,n) - a_n
      = (c_(sigma,n) - s_(k_sigma,n) - a_n)
        - (h_(sigma,n) - s_(k_sigma,n)).

RH-292 shortens the missing bridge clock.  With

    P_sigma(u)
      = sum_(2<=n<u) |tau_(sigma,n)-a_n| R^n/n,

one has

    P_sigma(m_sigma)
      <= P_sigma(h_sigma) + S_sigma(h_sigma) + T_sigma(h_sigma),
    S_sigma(h_sigma) <= 40/(3 h_sigma),
    T_sigma(h_sigma) -> 0.

Thus it is enough to prove P_sigma(h_sigma)->0.  Equivalently, a sufficient
typed route must prove on this same minimal clock both

    E_sigma(R)
      = sum_(2<=n<h_sigma)
        |c_(sigma,n)-s_(k_sigma,n)-a_n| R^n/n -> 0,

and

    D_sigma(R)
      = sum_(2<=n<h_sigma)
        |h_(sigma,n)-s_(k_sigma,n)| R^n/n -> 0.

RH-294 supplies a weighted E-type bridge only on an unknown arbitrarily slow
clock.  RH-295 shows that even an unweighted maximum on the exact clock is
insufficient without a rate or aggregate norm.  RH-296 proves that the
archived orbit-tube localization architecture stops at slope
1/log(lambda)=1.930709419..., strictly below a_*.  No current theorem proves
E_sigma or D_sigma on h_sigma.

The preferred direct alternative is the logarithmic mismatch

    g_sigma(z)
      = sum_(n>=2) (tau_(sigma,n)-a_n) z^n/n.

Actual vanishing H-infinity or H2 norm on one certified radius

    1.4 < rho < rho_* = 1.426787483864073...

would directly imply the full weighted coefficient budget.  RH-300 proves
this implication only as a criterion; it does not supply annular convergence
for the actual noisy complement.

## 4. Compact conclusions from RH-292 through RH-301

- RH-292: The bridge need not reach the convenient slope-four spectral cut.
  At the sharp mass-and-cap clock
  a_*=1/log(10/7)=2.803673252057129..., the intervening complement tail is
  at most 40/(3h_sigma), and the deterministic anchor tail also vanishes.
  Therefore P_sigma(h_sigma)->0 already implies the RH-288 prefix at
  m_sigma.  The paper shortens the clock but does not prove the bridge.
- RH-293: If only a uniform coefficient error epsilon_sigma is known on
  h_sigma=ceil(a log(1/sigma)), then the weighted prefix has the sharp
  information-class threshold beta_*=a log R for a power rate
  epsilon_sigma=O(sigma^beta).  Equality still gives logarithmic decay.  At
  the minimal clock beta_*=0.9433582098747317....  No archived noisy
  moving-order estimate has this rate.
- RH-294: Refining the diagonal tolerances in RH-287 yields an exact weighted
  full-trace bridge on some clocks h_sigma->infinity and k_sigma->infinity
  with h_sigma<2k_sigma.  The selected clock can grow arbitrarily slowly and
  has no logarithmic lower bound, so determinant gluing remains inactive.
- RH-295: For every prescribed growing cut, an escaping coefficient spike can
  make the unweighted prefix maximum tend to zero while the R-weighted prefix
  diverges.  This is a scoped abstract coefficient obstruction, not a claimed
  physical noisy spectrum.
- RH-296: The current mass-and-cap tail requires slope at least
  2.803673252057129..., whereas the existing Gaussian orbit-tube boundary
  clearance can cover a full moving prefix only up to slope
  1.930709419186936....  The ranges are disjoint by
  0.872963832870193.  This blocks reuse of the archived proof mechanism; it
  does not prove actual trace nonconvergence.
- RH-297: On the RH-16 natural rank clock,
  2k_sigma<h_sigma<4k_sigma<m_sigma<6k_sigma for small noise.  The minimal
  bridge crosses exactly one counterloop alias and the slope-four cut exactly
  two.  Their isolated limiting-radius absolute weights grow with exponents
  0.463406944517003 and 0.926813889034006.  An admissible theorem must be
  alias-inclusive; cancellation by the actual noisy aggregate remains open.
- RH-298: The fixed-order square-root parity law is
  (c^H_(sigma,n)-c^H_n)/sqrt(sigma)
  ->(-1)^n n C_* r_H^(-n).  Separately absolute-majorizing this correction on
  the minimal clock gives growth exponent 0.8990081854606016>0.  This excludes
  that proof architecture only; it does not prove divergence of the combined
  E_sigma budget.
- RH-299: Zero-padding unequal finite multisets gives
  |sum x_j^n-sum y_j^n|<=nB^(n-1)d_1^0.  The resulting root-l1 Lipschitz bound
  has sharp disk-bounded information-class threshold a_*log(BR).  The local
  shell threshold is 0.6729348509145321..., while the global Hardy cap gives
  1.399008185460602....  No actual modulus-head matching theorem is known.
- RH-300: If g_sigma is holomorphic past |z|=rho>R, then
  P_sigma^infinity(R)<=M_sigma x^2/(1-x) under an H-infinity bound and
  P_sigma^infinity(R)<=H_sigma x^2/sqrt(1-x^2) under an H2 bound, where
  x=R/rho.  At rho=1.41 the constants are 139.0070921986 and
  8.2924678943.  Endpoint H2 control at rho=R does not imply coefficient-l1
  control.  The criteria are proved but inactive.
- RH-301: The ten-layer review records the shortened clock, sharp prefix
  rates, clock incompatibility, exact alias ledger, parity-majorant barrier,
  root-l1 criterion, and annular reopening target.  Both typed ledgers remain
  at score four, weighted cross-branch glue is false, complete count is zero,
  and Gates A--E remain open.

## 5. Route firewall and RH-302 reopening triggers

Do not promote the batch beyond its hypotheses:

- Tail absorption shortens the required bridge window; it does not create a
  noisy coefficient bridge or a head-to-counterloop transport theorem.
- The RH-293 and RH-299 thresholds are sharp for their declared information
  classes.  They do not assert that the physical noisy spectrum saturates the
  bounds or that an actual matching cost must have those rates.
- RH-294 is weighted but rate-free.  An unknown slow diagonal clock cannot be
  substituted for the certified logarithmic clock.
- RH-295 is an abstract escaping-spike construction.  It is not evidence that
  the physical trace coefficients contain such a spike.
- RH-296 obstructs the archived orbit-tube proof architecture only.  A new
  moving-order boundary-layer theorem could still prove convergence.
- RH-297 counts exact aliases.  Pre-alias fixed-moment formulas cannot be
  extended past 2k without the alias impulses, but those impulses may cancel
  inside a grouped noisy aggregate.
- RH-298 rejects a separate absolute parity majorant.  It does not prove that
  the combined E_sigma budget diverges.
- Zero-padded root-l1 transport is a criterion, not an actual identification
  of the modulus-complete noisy head with the finite-radius counterloop.
- RH-300 proves annular H-infinity/H2 implications only.  No actual annular
  norm convergence has been established.
- No Gate A--E status changes follow from either incomplete typed branch.

Admissible RH-302 inputs are:

1. An actual theorem that g_sigma tends to zero in H-infinity or H2 on one
   radius 1.4<rho<1.426787483864073..., or an equivalent direct contour or
   trace-aggregate theorem giving P_sigma(h_sigma)->0.
2. A parity-renormalized, alias-inclusive weighted full-trace theorem giving
   E_sigma->0 on h_sigma=ceil(a_*log(1/sigma)), paired with actual
   modulus-head transport giving D_sigma->0 on that same clock.
3. For the head constituent, a quantified root-l1, weighted-Fourier, or
   contour theorem for the actual modulus-complete noisy head to the exact
   finite-radius counterloop, but only when paired with the required
   full-trace theorem.

If no new input supplies one of these, publish a scoped route stop rather than
another tail estimate, finite fit, pre-alias-only theorem, separate parity
majorant, or global nonexistence claim.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-292--RH-301 audit:

- Tests: 34/34 passed across ten directories, with per-paper counts
  4,4,3,3,3,3,4,4,4,2.
- Individual archives: 10/10 verified with zero failures.  RH-292--RH-300
  manifests contain 15 publication files each; RH-301 contains 19.
- Batch archive: 154 publication files, zero failures.
- PDFs: RH-292--RH-300 have 2 pages each and RH-301 has 3, for 21 pages total.
  Every semantic PDF is byte identical to main.pdf and every PDF has
  extractable text.
- All ten LaTeX logs have zero errors, undefined citations/references, rerun
  warnings, and overfull/underfull boxes.
- Ghostscript parsed 10/10 PDFs; all fonts are embedded.
- Page-by-page visual review found no clipping, overlap, anomalous blank page,
  formula or table overflow, footer conflict, or rendering anomaly.
- All 10 result JSON files parse, contain complete Gate A--E ledgers, and keep
  all 50 gate values false.  The RH-301 Hilbert--Polya, Riemann-zero,
  von-Mangoldt, zeta-divisor, and RH flags are all false.
- The paper batch commit contains 176 files after adding per-paper and batch
  archive metadata.  RH_HANDOFF.md is committed separately so it records the
  batch commit exactly.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The compact review is
papers/RH-301-ten-layer-weighted-prefix-frontier-review/.

## 7. Continuation prompt

    Continue RH research in /root/math/prime_dynamics_theory.  Run
    git status --short --branch and git pull --rebase origin main.  Treat the
    repository as the sole source of truth.  Read RH_HANDOFF.md and the
    RH-301 README, UPDATED_ROADMAP.md, result.json, and main.pdf.  Proceed to
    RH-302 only with an actual annular H-infinity/H2 theorem for the noisy
    complement on some 1.4<rho<1.426787483864073..., or with both typed
    estimates on the minimal clock ceil(log(1/sigma)/log(10/7)): an
    alias-inclusive parity-renormalized weighted full-trace bridge and actual
    modulus-head transport to the exact finite-radius counterloop.  More tail
    estimates, finite fits, rate-free clocks, separate parity majorants, and
    pre-alias-only formulas are insufficient.  Keep Gates A--E false/open; do
    not imply a Hilbert--Polya operator, Riemann-zero identification,
    zeta-divisor equality, or RH.
