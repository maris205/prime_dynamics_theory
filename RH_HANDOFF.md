# RH Research Handoff

Status date: 2026-07-30

Current completed endpoint: RH-311

Completed research batch: RH-302 through RH-311

Research batch commit:
19edbdd1a714d47e037523a526cb4d84b2b2c474

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in /root/math/prime_dynamics_theory.

Before the next state-changing batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-311-ten-layer-annular-mass-frontier-review/README.md
- papers/RH-311-ten-layer-annular-mass-frontier-review/UPDATED_ROADMAP.md
- papers/RH-311-ten-layer-annular-mass-frontier-review/results/result.json
- papers/RH-311-ten-layer-annular-mass-frontier-review/main.pdf

The next result-driven batch starts at RH-312 on one of two legitimate
frontiers: actual endpoint H2 convergence for the complement mismatch, or a
joint first-alias boundary-layer trace law including parity and shell
cancellation.  Additional tail estimates, finite endpoint fits,
pre-alias-only formulas, or separate absolute majorants do not activate the
remaining determinant interface.

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

All five gates are false/open.  No paper in RH-302--RH-311 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves a completed-zeta divisor equality, or implies RH.

## 3. Decision after RH-311

Current route coordinate:

    endpoint_h2_or_joint_first_alias_open_complete_zero

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
    rho_* = 1.426787483864073...,
    L_sigma = log(1/sigma),
    a_* = 1/log(10/7) = 2.803673252057129...,
    h_sigma = ceil(a_* L_sigma),
    m_sigma = ceil(4 L_sigma).

For the actual complement mismatch write

    g_sigma(z)
      = sum_(n>=2) (tau_(sigma,n)-a_n) z^n/n.

RH-302 proves that, on every fixed 1.4<rho<rho_*, the tails beyond m_sigma
vanish in H-infinity(rho) and H2(rho).  Hence full annular convergence is
equivalent to convergence of the moving polynomial head; the head is still
uncontrolled.  RH-303 further shows that annular convergence would force
each fixed noisy-head/counterloop moment, but this is only a necessity result
and supplies no growing-clock transport.

At the endpoint rho_*, RH-309 proves g_sigma belongs to H2 for every fixed
noise and does not belong to H-infinity.  Moreover

    sum_(n>=2) |tau_(sigma,n)-a_n| R^n/n
      <= 4.992111068649647 ||g_sigma||_H2(rho_*).

Thus actual endpoint H2 convergence would close the weighted complement
budget.  The exact odd witness also gives only the lower-rate restriction

    ||g_sigma||_H2(rho_*)
      >= C / sqrt(log(e+M_sigma))
      >= C' / sqrt(log(e+1/sigma)),

which neither proves nor disproves convergence.

The other legitimate frontier is the first natural alias.  On the archived
natural rank clock its slope equals the localization ceiling
1/log(lambda)=1.9307094191869356..., the isolated alias and parity terms have
the same weighted growth exponent 0.46340694451700304..., and any successful
minimal-clock argument must prove their joint boundary-layer cancellation
with error o(k R^(-2k)).  No such joint law is currently available.

## 4. Compact conclusions from RH-302 through RH-311

- RH-302: On every fixed certified strict annulus, both slope-four tails
  vanish in H-infinity and H2.  Full norm convergence is therefore equivalent
  to moving-head convergence, which remains open.
- RH-303: Annular convergence controls every fixed complement coefficient and,
  with archived fixed-order limits, necessarily forces fixed-order noisy-head
  transport to the counterloop.  It proves no actual growing-clock transport.
- RH-304: Relative matching of an exact odd anchor forces explicit complement
  mass.  At the minimal clock the exponent is 0.9468615163684616, only
  0.05313848363153839 below the archived sigma^(-1) cap.  The conclusion is
  conditional on the unproved relative matching hypothesis.
- RH-305: An exact least-odd witness yields, on each strict annulus,
  ||g|| >= C_rho M^(-kappa(rho))/log(e+M).  At rho=1.41,
  kappa=0.035045705260961....  Under M_sigma<=sigma^(-1), faster power decay
  is excluded, while slower convergence remains open.
- RH-306: Truncated deterministic anchors saturate the RH-305 exponent and
  logarithmic factor for the coefficient-envelope information class.  No
  spectral power-sum or actual noisy-complement realization is constructed.
- RH-307: For rho_sigma=R exp(c log L_sigma/L_sigma), the sharp mass-and-cap
  tail threshold is c_*=log(10/7)=0.3566749439387324.  Repeated-q saturation
  is model-scoped and does not prove failure of the actual moving head.
- RH-308: The Hardy conversion improves the annular coefficient constant from
  gap order eta^(-1) to eta^(-1/2).  H2 optimality is exact, and dyadic
  Rudin--Shapiro lengths 8, 64, and 512 prove the same H-infinity unit-ball
  order.  Actual mismatch decay remains open.
- RH-309: The actual endpoint mismatch is in H2 but not H-infinity.  Endpoint
  H2 convergence would imply the full weighted bridge, while the exact odd
  witness imposes a 1/sqrt(log) lower-rate barrier.  Convergence and
  nonconvergence are both unproved.
- RH-310: The first alias, parity correction, and localization ceiling are
  critical at the same natural slope.  The alias/parity exponent is
  0.46340694451700304, and a successful argument requires an explicit joint
  first-alias matching law.  Separate majorants do not decay, but combined
  divergence is not proved.
- RH-311: The ten-layer review keeps both typed ledgers at score four of five,
  weighted cross-branch glue false, complete count zero, and Gates A--E open.

## 5. Route firewall and RH-312 reopening triggers

Do not promote the batch beyond its hypotheses:

- Vanishing slope-four tails reduce the problem to the moving head; they do
  not control that head.
- Fixed-order transport is a necessary consequence only.  It cannot be
  promoted to the logarithmic clock without a new uniform theorem.
- The RH-304 mass demand assumes relative moving-order matching; it is not an
  unconditional spectral lower bound.
- The RH-305 lower rate does not prove nonconvergence, and RH-306 sharpness is
  limited to its coefficient-envelope information class.
- The RH-307 threshold concerns certified tail bounds and a repeated-q model;
  it is not an actual shrinking-annulus phase transition.
- Endpoint H-infinity membership is false, but endpoint H2 membership is true
  for each fixed noise.  Neither endpoint H2 convergence nor nonconvergence is
  known.
- Hardy coefficient conversion is a criterion, not a norm-decay theorem for
  the actual complement.
- The first-alias matching law is necessary on the typed natural clock.  No
  joint parity/shell cancellation or full-trace convergence is proved.
- No Gate A--E status changes follow from either incomplete typed branch.

Admissible RH-312 inputs are:

1. An actual proof that ||g_sigma||_H2(rho_*) tends to zero, with a rate no
   faster than the proved logarithmic lower barrier; an actual strict-annulus
   convergence theorem is also sufficient, subject to the RH-305 rate cap.
2. A joint moving-order boundary-layer trace law at the first natural alias,
   including parity and shell cancellation with error o(k R^(-2k)).
3. A new actual growing-clock head-transport theorem may be developed, but it
   must ultimately be synchronized with an alias-inclusive full-trace law on
   the same clock.

If no new input supplies one of these, publish a scoped route stop rather than
another tail estimate, finite fit, pre-alias-only theorem, separate parity
majorant, or global nonexistence claim.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-302--RH-311 audit:

- Tests: 45/45 passed across ten directories, with per-paper counts
  3,3,4,6,5,6,5,5,5,3.
- Individual archives: 10/10 verified with zero failures.  RH-302--RH-310
  manifests contain 15 publication files each; RH-311 contains 19.
- Batch archive: 154 publication files, zero failures.
- PDFs: all ten papers have 2 pages, for 20 pages total.  Every semantic PDF
  is byte identical to main.pdf and every PDF has extractable text.
- All ten LaTeX logs have zero errors, undefined citations/references, rerun
  warnings, and overfull/underfull boxes.
- Ghostscript parsed 10/10 PDFs; all fonts are embedded.
- Page-by-page visual review found no clipping, overlap, anomalous blank page,
  formula or table overflow, footer conflict, or rendering anomaly.
- All 10 result JSON files parse, contain complete Gate A--E ledgers, and keep
  all 50 gate values false.  The RH-311 Hilbert--Polya, Riemann-zero,
  von-Mangoldt, zeta-divisor, and RH flags are all false.
- The paper batch commit contains 176 files after adding per-paper and batch
  archive metadata.  RH_HANDOFF.md is committed separately so it records the
  batch commit exactly.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The compact review is
papers/RH-311-ten-layer-annular-mass-frontier-review/.

## 7. Continuation prompt

    Continue RH research in /root/math/prime_dynamics_theory.  Run
    git status --short --branch and git pull --rebase origin main.  Treat the
    repository as the sole source of truth.  Read RH_HANDOFF.md and the
    RH-311 README, UPDATED_ROADMAP.md, result.json, and main.pdf.  Proceed to
    RH-312 on one of two legitimate routes: prove actual endpoint
    H2(rho_*) convergence for the complement mismatch at a rate compatible
    with the 1/sqrt(log(1/sigma)) lower barrier, or prove a joint moving-order
    first-alias boundary-layer trace law including parity and shell
    cancellation with error o(k R^(-2k)).  More tail estimates, finite fits,
    separate absolute majorants, and pre-alias-only formulas are insufficient.
    Keep Gates A--E false/open; do not imply a Hilbert--Polya operator,
    Riemann-zero identification, zeta-divisor equality, or RH.
