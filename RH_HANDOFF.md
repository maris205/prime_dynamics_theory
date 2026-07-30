# RH Research Handoff

Status date: 2026-07-30

Current completed endpoint: RH-291

Completed research batch: RH-282 through RH-291

Research batch commit:
6158fd8845955d69d269b438147dcf5b9b351715

The repository, not an old chat transcript, is the source of truth.

## 1. Continuation protocol

Work in /root/math/prime_dynamics_theory.

Before the next state-changing batch:

    git status --short --branch
    git pull --rebase origin main

Read these compact entry points before older papers:

- RH_HANDOFF.md
- papers/RH-291-ten-layer-spectral-tail-frontier-review/README.md
- papers/RH-291-ten-layer-spectral-tail-frontier-review/UPDATED_ROADMAP.md
- papers/RH-291-ten-layer-spectral-tail-frontier-review/results/result.json
- papers/RH-291-ten-layer-spectral-tail-frontier-review/main.pdf

The next result-driven batch starts at RH-292 only with a genuine weighted
prefix input on the same logarithmic clock as the RH-282 spectral tail.
Additional tail estimates, finite endpoint fits, or head-only transport do
not activate the remaining determinant interface.

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

All five gates are false/open.  No paper in RH-282--RH-291 constructs a
Hilbert--Polya operator, identifies Riemann zeros, proves a von Mangoldt trace
formula, proves a completed-zeta divisor equality, or implies RH.

## 3. Decision after RH-291

Current route coordinate:

    typed_modulus_complement_weighted_prefix_open_complete_zero

The five obligations remain

    (legal head, coefficient bridge, uniform high-order tail,
     analytic target tail, certified target boundary constant).

The two typed branches now read

    noisy modulus spectrum       = (true, false, true,  true, true)
    graded monodromy counterloop = (true, true,  false, true, true)

Both have score four and complete-certificate count zero.  Their
coordinatewise maximum is all true but is not a legal certificate because
the prefix and tail belong to different determinant decompositions.

For orders n at least two, write

    c_(sigma,n) = h_(sigma,n) + tau_(sigma,n),

where c is the total noisy bulk trace, h is the modulus-complete head moment,
and tau is the normal spectral-complement trace.  Let s_(k_sigma,n) be the
finite-radius counterloop moment and a_n the deterministic numerator anchor.
The exact typed identity is

    tau_(sigma,n) - a_n
      = (c_(sigma,n) - s_(k_sigma,n) - a_n)
        - (h_(sigma,n) - s_(k_sigma,n)).

The missing direct prefix on R=7/5 and
m_sigma=ceil(4 log(1/sigma)) is

    P_sigma(R)
      = sum_(2<=n<m_sigma) |tau_(sigma,n)-a_n| R^n/n -> 0.

A sufficient route must prove on this same clock both

    E_sigma(R)
      = sum |c_(sigma,n)-s_(k_sigma,n)-a_n| R^n/n -> 0,

and

    D_sigma(R)
      = sum |h_(sigma,n)-s_(k_sigma,n)| R^n/n -> 0.

RH-287 gives only an unweighted, rate-free version of the first error on an
unspecified growing clock.  No current theorem gives the second weighted
error.  Head-to-counterloop transport alone is therefore insufficient.

## 4. Compact conclusions from RH-282 through RH-291

- RH-282: For the Hardy-scaled folded Gaussian operator after the two
  peripheral roots are removed, choose every algebraic eigenvalue with
  modulus greater than q=1/2 as the genuine noisy spectral head.  Put the
  remaining eigenvalues on a normal diagonal operator C_sigma.  From
  sum |mu_j|^2 <= ||A_sigma||_(S_2)^2 <= sigma^(-1), one obtains
  ||C_sigma^m||_1 <= sigma^(-1) q^(m-2), ||C_sigma^m|| <= q^m, and the
  all-order trace envelope.  At R=7/5 and
  m_sigma=ceil(4 log(1/sigma)), the RH-279 root-rate upper bound is
  (7/10)e^(1/4)=0.898817791681419<1.  This is an exact projection-free
  determinant-factor realization, not a physical Riesz compression.
- RH-283: In the mass-and-cap class
  M_sigma<=C sigma^(-alpha), |mu_j|<=q, qR<1, the sharp logarithmic tail
  clock is a_crit=alpha/log(1/(qR)).  Equality still gives logarithmic
  decay; below the threshold a repeated-q diagonal saturation family
  diverges.  Strict supercritical slope uniformly guarantees the RH-279
  root-rate test.  A particular nonsaturating family may do better.
- RH-284: H_q(A)={mu:|mu|>q} is finite, conjugation complete for real
  operators, and the unique smallest spectral submultiset leaving complement
  radius at most q.  Its size is at most
  sum |mu_j|^2/q^2 <= ||A||_2^2/q^2.  Canonicality is relative to the declared
  threshold q; q=1/2 is not claimed intrinsic to the dynamics.
- RH-285: For every fixed derivative order s, the moving logarithmic tail has
  an envelope of size
  O(M_sigma m^(max(s-1,0)) (qR)^m), with constants depending on s and qR.
  Hence the high-order complementary det_2 tail factor tends to one with
  every fixed derivative under a strictly supercritical logarithmic clock.
  The constants are not uniform in s.
- RH-286: The exact RH-17 comparison shell uses the finite radius beta_k,
  not the limiting beta.  From
  beta_k=beta exp[-log(C_M)/(2k)+o(k^(-1))],
  2(k-1)|beta_k-beta| tends to beta|log C_M|, while every fixed pre-alias
  even moment has only O(k^(-1)) radial bias.  Re-centering the seven RH-15
  floating clouds reduces total root-error range from 0.6424--1.2481 to
  0.2841--0.8992 and maximum moment-defect range from 0.5096--1.4573 to
  0.3640--1.0450.  These are multiprecision/floating diagnostics, not
  interval or asymptotic cloud transport.
- RH-287: A diagonal argument gives clocks h_sigma->infinity and
  k_sigma->infinity with h_sigma<2k_sigma such that
  max_(2<=n<=h_sigma)|c_(sigma,n)-s_(k_sigma,n)-a_n|->0.  The construction is
  exact but nonquantitative, unweighted, and not synchronized to the RH-282
  logarithmic clock.  It does not identify noisy spectral roots.
- RH-288: The three-budget gluing theorem gives
  sup_|z|<=R |F_sigma/F-1| <= exp(P_sigma+S_sigma+T_sigma)-1.
  In the typed spectral application b_(sigma,n)=tau_(sigma,n); RH-285 gives
  the noisy complement tail S_sigma and the deterministic-envelope batch
  gives T_sigma.  The direct complement-to-anchor prefix P_sigma remains
  open and decomposes exactly into the two weighted errors E_sigma and
  D_sigma above.
- RH-289: The hidden shell
  {gamma exp(2 pi i j/L):0<=j<L} has zero moments through order L-1, order-L
  moment L gamma^L, and exact genus-one factor 1-(gamma z)^L.  Therefore
  finite or merely growing unweighted prefixes do not identify a divisor.
  Weighted root, Fourier, or contour control can exclude this construction;
  no global impossibility theorem is claimed.
- RH-290: The noisy and graded ledgers both score four, but their
  coordinatewise union is ill typed.  The cross-branch glue bit remains
  false.  A direct weighted complement prefix, or both synchronized typed
  constituent estimates, is required before the two branches can be merged.
- RH-291: The ten-layer review records the first archived instantiation of
  the RH-279 projection-free spectral tail, corrects the monodromy audit to
  finite beta_k, preserves the theorem/numerics firewall, and identifies the
  direct weighted complement-to-anchor prefix as the sole remaining analytic
  determinant leaf.

## 5. Route firewall and RH-292 reopening triggers

Do not promote the batch beyond its hypotheses:

- The normal diagonal C_sigma realizes an exact canonical-product tail; it is
  not asserted to be similar to a bounded physical quotient or to have
  well-conditioned Riesz projectors.
- The modulus head is genuine noisy spectrum, but its threshold is a declared
  design parameter and it is not identified with the monodromy counterloop.
- RH-283 is sharp for the mass-and-cap information class and for its repeated-q
  saturation family, not a statement that every physical spectrum saturates
  the bound.
- RH-285 controls every fixed derivative order of the moving high-order tail;
  it does not prove uniformity in derivative order or identify the finite head.
- RH-286 separates its analytic centering theorem from the non-interval
  seven-row diagnostic.  The decimal C_M value is not a directed-rounding
  certificate.
- RH-287 is coefficientwise on a selected growing window, not a weighted disk
  theorem and not a noisy-root theorem.
- RH-289 proves insufficiency of prefix data only; it does not prove physical
  hidden shells or global failure of cloud transport.
- Weighted head-to-counterloop transport supplies only D_sigma.  It cannot
  replace the missing E_sigma or direct P_sigma estimate.
- No Gate A--E status changes follow from either incomplete branch.

Admissible RH-292 inputs are:

1. A direct proof that P_sigma(7/5)->0 on
   m_sigma=ceil(4 log(1/sigma)).
2. A synchronized pair of explicit estimates proving E_sigma(7/5)->0 and
   D_sigma(7/5)->0 on that same clock.
3. A root-l1, weighted-Fourier, or contour theorem for the actual
   modulus-complete noisy head to the exact finite-radius shell, paired with
   the required weighted full-trace bridge.  The head theorem alone is not
   enough.
4. A direct contour or trace-aggregate theorem proving the
   complement-to-anchor determinant transport without resolving
   ill-conditioned eigenvectors.

If no new input supplies one of these, publish a scoped route stop rather than
another finite fit, another tail theorem, or a global nonexistence claim.

## 6. Reproduction and publication audit

Use the shared environment and avoid new cache noise:

    PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider

Final RH-282--RH-291 audit:

- Tests: 30/30 passed across ten directories, with per-paper counts
  3,3,3,4,3,3,3,3,3,2.
- Individual archives: 10/10 verified with zero failures.  RH-282--RH-290
  manifests contain 15 publication files each; RH-291 contains 19.
- Batch archive: 154 publication files, zero failures.
- PDFs: every paper has 2 pages, for 20 pages total.  Every semantic PDF is
  byte identical to main.pdf and every PDF has extractable text.
- All ten LaTeX logs have zero errors, undefined citations/references, rerun
  warnings, overfull/underfull boxes, and empty-bibliography warnings.
- Page-by-page visual review found no clipping, overlap, anomalous blank page,
  or table overflow.
- Every result JSON keeps Gate A--E false/open where represented; all
  Hilbert--Polya, Riemann-zero, zeta-divisor, and RH boundary flags remain
  negative.
- The paper batch commit contains 176 files after adding per-paper and batch
  archive metadata.  RH_HANDOFF.md is committed separately so it records the
  batch commit exactly.
- Unrelated untracked caches, checkpoints, LaTeX intermediates, and TPC work
  remain unstaged.

The compact review is
papers/RH-291-ten-layer-spectral-tail-frontier-review/.

## 7. Continuation prompt

    Continue RH research in /root/math/prime_dynamics_theory.  Run
    git status --short --branch and git pull --rebase origin main.  Treat the
    repository as the sole source of truth.  Read RH_HANDOFF.md and the
    RH-291 README, UPDATED_ROADMAP.md, result.json, and main.pdf.  Proceed to
    RH-292 only with a direct weighted modulus-complement-to-anchor prefix on
    R=7/5 and m_sigma=ceil(4 log(1/sigma)), or with both synchronized typed
    estimates: total noisy trace versus counterloop plus anchor, and noisy
    head versus the exact finite-radius counterloop.  Head transport alone,
    more tail estimates, and finite endpoint fits are insufficient.  Keep
    Gates A--E false/open; do not imply a Hilbert--Polya operator,
    Riemann-zero identification, zeta-divisor equality, or RH.
