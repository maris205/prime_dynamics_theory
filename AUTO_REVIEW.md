# TPC autonomous review loop: exact physical operator return

Started 2026-09-09 under the user's explicit request that the primary arrange
subsequent research and keep progressing autonomously. This is research authority,
not permission to ignore theorem gates or overwrite existing work.

## Active branch and boundaries

Primary target: the literal V59/TPC247 physical operator on the entire I_x,
its full component row energy, its ordinary operator norm, and the complete
input/output norm budget. Preserve the actual beta,w, outer q, fixed h0=2,
both unit masks, deleted diagonal, exact domain and all parameter ranges.

The current formal release endpoint remains TPC418. The first research-round
archive is preserved. No model-norm result alone supplies arithmetic fixed-power
credit or a numbered-paper GO.

This branch uses at most four substantive review/fix cycles before a route
assessment. Review scores do not replace proof, source, novelty or physical-loss
gates. Cross-model verification is not enabled; agents inherit the current model.
No GPU pilot is planned for these purely mathematical questions.

## Round 1 — in progress

Baseline HEAD and fetched origin/main: ab23455ba941e5a14ded27d49de0e874aee811ac.
Handoff SHA256: 36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a.
Ten pre-existing tracked-dirty paths, 631 untracked files, empty index. Fetch
succeeded. Existing changes make rebase unsafe; no rebase, auto-stash, commit,
push or numbered release is attempted.

### Assigned independent side tasks

- `physical-loop-hybrid-source-lock`: Laplace (`01a0869e-c1bc-7340-9752-59e526bc6e32`), read-only.
- `physical-loop-finite-attachment-audit`: Maxwell (`01a0869e-c1f2-7aa2-9c2b-12b9f9af728b`), read-only.
- `physical-loop-physical-operator-obstruction`: Bernoulli (`01a0869e-c255-7230-b8d0-f144998b64c6`), read-only.
- `physical-loop-local-emitter-obligation`: Franklin (`01a0869e-c3a4-70f2-a095-e8491ade6dfc`), read-only.
- `physical-loop-prefix-cover-audit`: Rawls (`01a0869e-c334-76d2-a731-19dd9226efc5`), read-only.
- `physical-loop-startup-regression`: Lagrange (`01a0869e-c2c4-7261-bd46-e90ca28b6324`), read-only.

The primary alone writes this log, REVIEW_STATE.json and the new working folder
`research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop`. Those parent writes were declared in every task envelope.

### Parent derivation, not yet certified

1. Extend the full component row-energy calculation to the actual fixed Fourier
   kernel and entire physical interval, with kernel hypotheses explicit.
2. Determine whether elementary nonprincipal-character projection and rational
   frequency separation give the ordinary coefficient-blind operator bound.
3. Compare normalized and unnormalized bounds with the physical weighted lanes;
   never omit the cost of restoring those lanes.

New derivation/proof texts will be placed in the declared working folder, leaving
prior root PROOF_PACKAGE.md and DERIVATION_PACKAGE.md unchanged.

### Reviewer raw responses

Pending. Full substantive responses will be retained verbatim before synthesis.

### Source verification scope

ARS fact-check/source-verification guidance is used only to lock explicit source
claims and distinguish them from the primary's new derivations. This is not a
full ARS research-to-paper pipeline, programmatic bibliographic verification,
automatic external-model upload, or human-read attestation. Source hypotheses
that cannot be recovered remain conditional.


## Round 1 — independent scoped audits received (2026-09-09)

Two independent auditors returned 9/10 for the exact scoped operator and lane-norm theorems.
Neither score is a publication-readiness or arithmetic-GO assessment. The emitter auditor
also returned a scoped 9/10; its integrated-file addendum is still running.

Required corrections before integration: explicitly define the unnormalized residue variance;
restore the source clock x=2X rather than the conflicting X=x in raw reports; rename the
semiprime heading because x/log x is zero natural density; state the fixed-K threshold and
two-sided triangle inequality; complete the terminal normalization ledger. These are queued
while the frozen-draft audit finishes, not silently assumed implemented.

### Operator audit — full raw response

<details>
<summary>Complete independent operator audit, round 1</summary>

```json
{
  "schema": "TPC_AGENT_RESULT_V1",
  "task_id": "physical-loop-independent-operator-audit",
  "role": "tpc_proof_auditor",
  "mode": "READ_ONLY_RESEARCH_AND_AUDIT",
  "proof_verdict": "PROVABLE AS STATED under the explicitly locked fixed-profile assumptions",
  "scoped_theorem_readiness": "9/10; not arithmetic GO",
  "arithmetic_advance": false,
  "publication_GO": false,
  "files_changed": []
}
```

P1–P5 survive independent audit. I found no fatal mathematical mismatch in the written operator theorem. The exact profile reflection is valid, and neither evenness nor a real-valued kernel is needed. Corrections below concern explicit definitions, inherited notation, and downstream scope. The lane-norm theorem and growing-rank extension were not audited.

### 1. Independent proof findings

| Component | Verdict and mathematical check |
|---|---|
| **P1: residue projection** | Correct. On residues, \(F_q=qP_{\mathbf1^\perp}\), while \(S_q\) is \(q\) times the projection onto vectors vanishing at zero and summing to zero on units. Their difference is exactly \(r_qr_q^*/(q-1)\). Pullback preserves positive order even with unequal residue counts. Integrating \(D_vS_qD_v^*\) against the nonnegative profile preserves that order. Deleting \(\Delta\) afterward is essential. [PROOF_PACKAGE.md:10](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:10) |
| **P2: Poisson and spacing** | Correct for the Fourier transform \(\sum_h k(h)e(-\theta h)\). The multiplier is \(H\sum_{\lambda,k}\psi_+(H(\lambda-\theta-k))\), with the printed sign and factor \(H\). Reduced fractions are distinct, including circular spacing across zero. Their lifted spacing is at least \(H/(4Q^2)\). The bound \(2\zeta(2)<4\), compression argument, and diagonal allowance yield the printed \(4B_\psi(H+4Q^2)+3Q^2\). [PROOF_PACKAGE.md:47](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:47) |
| **P3: row energy** | Correct. The coefficient expansion uses \((q-2)^2-1=(q-1)(q-3)\). At \(q=3\), the second term vanishes without invalidating the lower bound: the original congruent entries still have squared coefficient \(a_q^2\). The excluded diagonal justifies both lattice-integral upper bounds. The one-sided lower bound handles endpoint rows. Since \(u\le Q^3\), at most two shell primes divide \(u\), costing at most \(9Q\). This proves the stated uniform comparison eventually. [PROOF_PACKAGE.md:82](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:82) |
| **P4: constant mode** | Correct, interpreting \(V_q\) as the **unnormalized** sum of squared deviations used in V59. The \(N=mq+s\) decomposition includes incomplete residue cycles and arbitrary integer origins. For \(0<|\alpha|q\le1/2\), the geometric-sum estimate gives distance at most \(\pi+1\) from a common value; \(\alpha=0\) is handled separately. Compact support and eventually \(H\ge4Q\) cover the entire integral. Thus \(\langle f,Af\rangle=-\sum_q(q-2)+O_\psi(1/\log Q)\). [PROOF_PACKAGE.md:131](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:131) |
| **P5: normalization** | Correct. The congruence \(A=D_G^{1/2}ZD_G^{1/2}\) gives both norm comparisons. Bounding each weighted lane below using \(G_{\min}\) proves P8. Therefore \(H^{-1}\ll_\psi\|Z\|\ll_\psi(\log Q)/H\). The further conclusion using particular arithmetic lane lower bounds remains conditional on their separate audit. [PROOF_PACKAGE.md:184](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:184) |

The weighted prime asymptotic is legitimate: partial summation of PNT gives
\[
\sum_{Q<q\le2Q}a_q^2q\sim\frac32\frac{Q^2}{\log Q}.
\]
The cited [Selberg paper, introductory equation (1.1)](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf) supplies PNT; the dyadic weighted formula is a derivation, not a quotation.

### 2. Exact identification and actionable corrections

**Profile crosswalk succeeds.** The ancestor fixes a nonnegative smooth compact profile; the primary [Blomer–Li Lemma 1](https://arxiv.org/html/2511.03294v1#S2.SS1) confirms this class. The earlier positive-transform convention appears at [corrected emitter:87](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_corrected_fourier_factorable_emitter.md:87), while V59 uses the negative transform. Direct substitution proves
\[
\int\psi(v)e(yv)\,dv
=\int\psi(-v)e(-yv)\,dv.
\]
Thus the draft’s explicit \(\psi_+(v)=\psi(-v)\) preserves the same kernel. This is a derived convention crosswalk, not a source-printed equality.

For a non-even profile, silently using \(\psi\) instead would conjugate the kernel and operator. With real arithmetic lanes it conjugates the scalar, preserving its absolute value but **not its literal identity**.

Make these corrections before integration:

1. **Define variance explicitly.** Replace the prose at [PROOF_PACKAGE.md:140](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:140) by
   \[
   V_q(\alpha)=\sum_{r\ne0}|S_r(\alpha)-\bar S^\times(\alpha)|^2,\qquad
   \bar S^\times=\frac1{q-1}\sum_{r\ne0}S_r.
   \]
   A probabilistically normalized “variance” would introduce a missing factor \(q-1\). V59’s intended convention is explicit at [V59:230](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:230).

2. **Restore \(X\).** Add \(x=2X\) and \(N=\lfloor x\rfloor-\lfloor x/2\rfloor\) beside the draft’s parameter lock. The original [literal emitter:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md:43) states \(x=2X\). The archived [operator report:39](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/agent-reports/physical-loop-physical-operator-obstruction.md:39) instead says \(X=x\); do not inherit that inconsistent notation.

3. **State the precise uniformity ceiling.** The theorem is eventual, for every physical row and the complete prime shell, with constants depending on the fixed profile and no exceptional rows. It is not uniform over unrestricted profiles or arbitrary translated row-energy domains: a row at a multiple of every shell prime has \(G=0\). Singleton coordinate prefixes also have zero deleted row energy. Neither is a counterexample to the stated physical theorem.

4. **Complete the downstream budget and distinguish audited dependencies.** The lane claims at [DERIVATION_PACKAGE.md:149](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:149) need their separate verdict. The short-array/emitter claims are outside this operator audit.

### 3. Physical contract, first fatal mismatch, and no-GO boundary

The source-locked matrix retains
\[
A_q(u,t)=q\kappa((u-t)/H)
\left(1_{u\equiv t\ (q)}-\frac1{q-1}\right)
1_{q\nmid u}1_{q\nmid t}1_{u\ne t}.
\]
This agrees exactly with [TPC247 main.tex:70](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70). The literal lanes retain the Möbius subtraction and \(w(u)=\Lambda(u+2)-b_x^{(z)}(u)\), including the hybrid’s forbidden residue \(-2\) and prime \(2\).

Parameters are \(h_0=2\), \(I=(x/2,x]\cap\mathbb Z\), \(Q=x^{1/3}\), \(H=x^{21/32}\), \(U=x^{133/400}\), and all primes \(Q<q\le2Q\). The full ordered off-diagonal pair domain is retained. Coordinates use increasing integer order; a prime prefix means \(Q<q\le Y\). No maximal-prefix saving is proved. The fixed-\(K\) order remains requested saving parameters \(\to B_{\rm FM}\to K(B_{\rm FM})\to x_0\).

**First fatal mismatch:** none inside P1–P5. For a proposed coefficient-blind power-saving use, however,
\[
\|A\|\gtrsim Q^2/\log Q
\]
contradicts \(\|A\|\ll Q^2x^{-\delta+o(1)}\) for every fixed \(\delta>0\).

**Strongest objection to promotion:** this is an operator-norm obstruction, not a lower bound for \(|\langle w,A\beta\rangle|\). P8 prevents ordinary row-energy normalization from concealing the lane costs; it does not exclude coefficient-sensitive cancellation.

The natural scalar scale is \(xQ^2=x^{5/3}\). The complete terminal ledger divides by \(K_*=x^{2/3+o(1)}\), retains the physical error exponent \(79/96\), and requires
\[
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]
With benchmark \(1/96\) and additional loss exponent \(\ell\), one needs \(\ell<19/2400\), strictly, as well as Gate A. [V58:305](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:305)

**Closest existing results:** V59’s exact variance-minus-diagonal identity and generic-sequence warning, plus TPC247’s literal attachment and external-copy norm toll. No novelty certification follows.

Location remains island ②, image Bridge A, repository Gate B. TPC418 remains the formal endpoint. No gate closure, numbered writer, or arithmetic GO.

### 4. Diagnostics and preservation

In-memory diagnostics only, using a smooth non-even compact profile:

- 15 matrix cases, including \(q=3\), singleton intervals, and unequal residue counts: identity error \(<9\times10^{-16}\), row-energy error \(<5.4\times10^{-15}\).
- 672 variance cases, including \(\alpha=0\) and \(\alpha=\pm1/(2q)\): maximum \(V_q/q=0.55<(\pi+1)^2\).
- Poisson check: correct-sign discrepancy \(8.4\times10^{-9}\); reversed-sign discrepancy \(4.47\).

These support debugging, not asymptotic certification.

All shell commands exited **0**: `pwd`; bounded `sed`, `nl -ba`, `rg -n`, and `wc -l` reads; `sha256sum`; `git rev-parse HEAD origin/main`; porcelain status including `--untracked-files=all`; `git diff --name-only`; `git diff --cached --name-only`; and the inline `python -B -` diagnostic. Public-source web reads succeeded. No writes, builds, regeneration, synchronization, children, or external-model uploads occurred.

Start/end HEAD and local origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Status: **10 tracked dirty / 642 untracked / empty index → unchanged**; no added or removed status entries. Parent-owned unfrozen review/round contents remain authorized, not unexplained drift.

Start/end SHA-256 values were identical:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
round/DERIVATION_PACKAGE.md
2d7c6cc906650edf1be208dc652e9c24d534565b057317603e7ebbfaa321c288
round/PROOF_PACKAGE.md
5f977d1e18dc2ec19dc72f08c5b86407141157aea569518e5f5190bedd0512d1
round/LANE_NORM_PROOF.md
71e7e348f2e0f4332ff1dd4b25330918f9b286c73ee5e44edb16ac4d2a7d155c
```

</details>

### Lane audit — full raw response

<details>
<summary>Complete independent lane audit, round 1</summary>

```json
{
  "schema": "TPC_AGENT_RESULT_V1",
  "task_id": "physical-loop-independent-lane-audit",
  "role": "tpc_proof_auditor",
  "mode": "READ_ONLY_RESEARCH_AND_AUDIT",
  "proof_verdict": "PROVABLE AS STATED, WITH DECLARED OPERATOR DEPENDENCIES IMPORTED",
  "first_fatal_mismatch": null,
  "readiness_score": "9/10 for the exact scoped lane-norm and norm-method theorem",
  "arithmetic_advance": false,
  "publication_GO": false,
  "files_changed": []
}
```

L1–L6 survive the adversarial audit. The main correction is terminology, not mathematics: “positive-density semiprime source” should say “semiprime source of order \(x/\log x\).” The readiness score does not certify novelty, arithmetic saving, or publication readiness.

### Source and physical-object lock

**Source statements.** The hybrid in [fm_local_comparison_compiler.md:727](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/fm_local_comparison_compiler.md:727) agrees literally with the frozen derivation:
\[
b_x^{(z)}(u)=1_I(u)C_zW_z1_{(u+2,P(z))=1}
\prod_{\substack{p\mid u\\p>z}}\frac{p-1}{p-2}.
\]
The small-prime product includes \(2\); its forbidden residue is \(-2\).

[V59:54](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:54) retains
\[
\beta(t)=\Lambda(t)/\log t-\sum_{d\mid t,\ d\le x^{133/400}}\mu(d),
\qquad w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
The physical shift is exactly \(h_0=2\). The outer \(q\), both unit masks, and deleted diagonal agree with
\[
A_q(u,t)=\frac q{q-1}\kappa((u-t)/H)
[(q-1)1_{q\mid u-t}-1]1_{q\nmid u}1_{q\nmid t}1_{u\ne t}.
\]
Thus no additional \(q\) belongs in \(\langle w,A\beta\rangle\).

The scope is the complete dyadic interval \(I=(x/2,x]\cap\mathbb Z\), \(N=\lfloor x\rfloor-\lfloor x/2\rfloor\), all ordered off-diagonal pairs, \(Q=x^{1/3}\), prime \(Q<q\le2Q\), \(H=x^{21/32}\), and \(U=x^{133/400}\). There is no coordinate-prefix or prime-prefix theorem. Increasing coordinate order does not replace this full-domain quantifier.

The frozen drafts use \(x\), not an independently defined uppercase \(X\). The archived report mentions \(x=2X\), but that ancestry lies outside the permitted original-source reads. Add the crosswalk if legacy \(X\)-notation is used; do not identify \(X\) with exact \(N\) silently.

The source explicitly fixes the legal order:
\[
(A_{\rm target},\varpi)\to B_{\rm FM}\to K(B_{\rm FM})\text{ fixed}
\to x\ge x_0.
\]
See [fm_local_comparison_compiler.md:799](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/fm_local_comparison_compiler.md:799). The lane estimates respect this order. They have no exceptional-coordinate set and assert no uniformity for unbounded \(K=K(x)\).

### Independent audit of L1–L6

**L1–L2: valid Euler-product upper bound.** In [LANE_NORM_PROOF.md:10](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:10),
\[
a(p)=2/(p-2)+1/(p-2)^2,\qquad a(p)/p=O(p^{-2}).
\]
Hence \(B_0<\infty\). Expanding the square over squarefree divisors, dropping only nonnegative masks, and extending the interval give
\[
\|b\|_2^2
\le W_z^2\sum_d a(d)\lfloor x/d\rfloor
\le xW_z^2\prod_{p>z}(1+a(p)/p)
\le B_0xW_z^2.
\]
The restrictions on \(d\) are explicitly retained at lines 30–32; there is no hidden extension to unrestricted multiplicative coefficients.

The classical unconditional Mertens product asymptotic implies \(W_z\ll\log z\), as explicitly stated in [Lamzouri, §1 opening paragraph](https://arxiv.org/html/1410.3777v2#S1). No RH-dependent bias theorem is used. Thus, for every fixed \(K>0\),
\[
\|b\|_2=O_K(\sqrt x\log\log x)=o(\sqrt{x\log x}).
\]

**L3: valid shifted-\(\Lambda\) asymptotic.** [LANE_NORM_PROOF.md:46](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:46) uses ordinary PNT and partial summation. The cited primary PNT statement is [Selberg (1949), p.305, (1.1)](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf).

**My verification:** higher prime powers contribute \(O(\sqrt x\log^3x)\); translating the interval by \(2\) changes the sum by \(O(\log^2x)\). Consequently
\[
\|\Lambda(\cdot+2)\|_2^2\sim(x/2)\log x.
\]
Using the two-sided norm comparison
\[
\big|\|w\|_2-\|\Lambda(\cdot+2)\|_2\big|\le\|b\|_2
\]
proves L3 without any orthogonality assumption.

**L4: valid semiprime count and exact constant.** In [LANE_NORM_PROOF.md:64](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:64), \(p>x^{2/5}>U\), while
\[
r>x^{11/20}/2>x^{9/20}\ge p
\]
eventually. Therefore the products have distinct prime factors, are counted once, and have literal \(\beta(pr)=-1\).

For \(y=x/p\), the lower bound \(y/2\ge x^{11/20}/2\to\infty\) makes the ordinary PNT error uniform. Subtracting the two PNT estimates on a dyadic interval retains a nonvanishing main term. No short-interval or arithmetic-progression PNT is required.

For partial summation, set \(E(t)=\pi(t)-\operatorname{li}(t)\). Uniformly on the stated \(p\)-range, \(|E(t)|\le\epsilon_x t/\log t\), \(\epsilon_x\to0\). The endpoints and \(\int E(t)f'(t)\,dt\) contribute \(o(1/\log x)\). The main integral is exactly
\[
\frac1{\log x}\int_{2/5}^{9/20}\frac{da}{a(1-a)}
=\frac{\log(27/22)}{\log x}.
\]
Thus L4’s constant \(\frac12\log(27/22)\) is correct.

**L5: valid divisor-norm upper bound.** [LANE_NORM_PROOF.md:108](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:108) correctly uses \(|\beta(n)|\le2\tau(n)\). The prime-power inequality
\[
(e+1)^2\le {e+3\choose3}
\]
holds also at \(e=0,1\), where equality occurs. Counting four factors gives
\[
\sum_{n\le x}\tau_4(n)
\le x\left(\sum_{m\le x}m^{-1}\right)^3
\le x(1+\log x)^3.
\]

**L6: valid with the assigned imported dependency.** Importing P7 from [PROOF_PACKAGE.md:173](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:173), without claiming a second operator audit,
\[
\liminf\frac{\|\beta\|_2\|w\|_2}{x}
\ge\tfrac12\sqrt{\log(27/22)}
\]
yields precisely
\[
\liminf\frac{\log Q}{xQ^2}
\|A\|\|\beta\|_2\|w\|_2
\ge\tfrac34\sqrt{\log(27/22)}.
\]
For the particular row normalization, the algebraic inequality P8 is correct; its uniform conclusion imports the companion row-energy comparability. See [PROOF_PACKAGE.md:184](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:184).

### Objection, corrections, and no-GO boundary

**Strongest objection to promotion:** a lower bound on the norm-product upper-bound expression says nothing comparable about the actual scalar’s lower bound. The draft correctly preserves this distinction.

The natural numerator scale is \(xQ^2=x^{5/3}\). The norm-product obstruction is \(\gg xQ^2/\log Q\); its ratio to the requested power-saving bound is
\[
x^{\delta-o(1)}/\log Q\longrightarrow\infty
\quad(\delta>0).
\]
Row normalization cannot erase this: \(G\asymp HQ^2/\log Q\), the two weighted lanes restore the row-energy cost, and P8 retains a fixed positive fraction of the unnormalized obstruction.

[V59:79](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:79) requires strictly \(\delta>1/400\). The benchmark \(1/96\) leaves only \(19/2400\) for additional losses. No emitter, coverage, selection, tail, or physical-transfer loss is paid by L1–L6.

Actionable corrections:

- Rename the “positive-density” heading; \(M_x/|I_x|\to0\).
- State \(x\ge x_0(K)\) with \(z\ge2\) explicitly.
- Spell out the two-sided norm comparison above.
- Keep P7 and row-energy comparability explicitly imported; add the \(X\)-crosswalk only with its original source.

**Closest verified existing inputs:** unconditional PNT and Mertens, plus the repository’s literal hybrid definition and V59 scalar identity—not a new cancellation theorem. Archived reports were read only after the drafts, for provenance.

Position: island ②, image Bridge A, repository Gate B. Formal endpoint TPC418; both analytic gates and the distinguished-seed bridge remain open. No numbered writer or arithmetic GO follows.

### Preservation and commands

Start/end `HEAD` and local `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Status: tracked dirty **10→10**, untracked **642→642**, index **empty→empty**; no added or removed status entries. Parent-authorized loop/review paths were already present. This does not assert bytewise immutability of unhashed parent files.

All seven SHA-256 values matched at start and end:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
DERIVATION_PACKAGE.md
2d7c6cc906650edf1be208dc652e9c24d534565b057317603e7ebbfaa321c288
PROOF_PACKAGE.md
5f977d1e18dc2ec19dc72f08c5b86407141157aea569518e5f5190bedd0512d1
LANE_NORM_PROOF.md
71e7e348f2e0f4332ff1dd4b25330918f9b286c73ee5e44edb16ac4d2a7d155c
```

Commands, all exit **0**: `pwd`; scoped `cat`, `nl -ba`, `sed -n`, heading-only `rg -n`; ancestor `AGENTS.md` existence loop; `sha256sum` on the seven named files; and:

```bash
git --no-optional-locks rev-parse HEAD origin/main
git --no-optional-locks status --porcelain=v1 -uall
git --no-optional-locks diff --name-only
git --no-optional-locks diff --cached --name-only
```

Primary-URL retrieval succeeded. In-memory decimal checks were diagnostics only. No children, repository writes, builds, regeneration, synchronization, credential inspection, or external-model upload occurred.

</details>

### Implemented material and verification

The six original side-task reports are archived verbatim in research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/agent-reports/.
The primary wrote the three main proof/derivation drafts, LOCAL_EMITTER_PROOF.md,
FINITE_ATTACHMENT_ERRATUM.md, and a read-only diagnostic program in that folder.
The earlier root-level derivation/proof documents and first reconnaissance folder are untouched.

New diagnostics passed in normal and optimized Python modes with identical stdout:
662 exact rational projection entries, 80 quadratic-emission packets, two finite
physical-index matrix examples, 101 divisor-exponent inequalities and exact semiprime
construction checks. The Gaussian kernel in these diagnostics is explicitly NOT the
source profile. No finite result proves an eventual estimate.

One bounded read command used an incorrect guessed TPC212 path and exited 2; the path
was located afterward with rg --files. No required checker failed. One orchestration
cell had a JavaScript syntax error before execution; retry created only the intended
new files. These incidents caused no repository source rewrite or data loss.

### Continuing work

Bernoulli is deriving a growing-dimensional negative subspace for the literal operator.
The primary is integrating source/notation corrections and preparing independent audit
of that extension. No numbered writer has been started; no commit, rebase, or push occurred.

## Round 1 closure and Round 2 delta review — 2026-09-09 15:25:48 UTC

All three initial independent scoped audits returned 9/10 with no fatal mathematical
defect in their assigned claims. Emitter E1–E6 also passed an integrated-file addendum.
These are readiness scores for precise scoped research statements, not submission scores.

### Emitter audit — full raw original response and addendum

<details>
<summary>Complete independent emitter audit and integrated-file addendum</summary>

## TPC_AGENT_RESULT_V1

`task_id: physical-loop-independent-emitter-audit`  
`role: tpc_proof_auditor`  
`mode: READ_ONLY_RESEARCH_AND_AUDIT`  
`files_changed: []`  
`proof_verdict: EXACT_EMISSION_AND_SATURATION_VERIFIED; COMPRESSION_CRITERION_SUFFICIENT_BUT_UNPROVED`  
`readiness_score: 9/10` for the corrected scoped emission/obstruction theorem—not arithmetic GO.

**No fatal algebraic error found. First transfer-fatal mismatch:** the emitter produces arrays indexed by \(1,\ldots,q-1\), whereas BP’s critical saving requires intervals of length \(O(\sqrt q)\). **Strongest objection:** each unsubtracted emitted quadratic packet exactly saturates its complete-array norm scale.

Location: island ②, image Bridge A, repository Gate B. Formal endpoint remains TPC418.

### 1. Physical source contract

The literal target is
\[
\mathfrak C_x=\sum_{Q<q\le2Q\atop q\ {\rm prime}}q
 \sum_{t,u\in I_x\atop t\ne u,\ q\nmid tu}
 \beta(t)w(u)\kappa((u-t)/H)
 \left(1_{u\equiv t(q)}-\frac1{q-1}\right),
\]
where
\[
X=x,\quad I_x=(x/2,x]\cap\mathbb Z,\quad N_{\rm phys}=|I_x|,
\quad Q=x^{1/3},\ H=x^{21/32},\ U=x^{133/400},
\]
\[
\beta(t)=\frac{\Lambda(t)}{\log t}-\sum_{d\mid t,\ d\le U}\mu(d),
\qquad w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
The fixed physical shift is \(h_0=2\). Both unit masks, all Möbius signs, hybrid subtraction, outer \(q\), and coefficient diagonal deletion remain compulsory. [V59:31]( /root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:31)

The frozen contract specifies
\[
b_x^{(z)}(u)=1_I(u)C_zW_z1_{(u+2,P(z))=1}
 \prod_{p\mid u,\ p>z}\frac{p-1}{p-2},
\]
with \(P(z)=\prod_{p\le z}p\), \(W_z=\prod_{p\le z}p/(p-1)\), and
\(C_z=\prod_{p>z}(1-(p-1)^{-2})\).
Here \(z=(\log x)^K\): choose the requested input exponent, then fixed \(K\), then the \(x\)-threshold. No unrestricted \(z\)-uniformity is established. The inherited profile has negative Fourier convention, integral one, and no hard difference cutoff. These are **contract statements**, not independently re-audited ancestry. [DERIVATION_PACKAGE.md:27](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:27)

The target uses the full ordered-pair domain and full prime shell. Fixed separable integer-prefix masks preserve the algebra without reindexing; no adaptive/maximal-prefix theorem follows. Increasing-prime prefixes are separately distinguished in [V58:344](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:344).

### 2. Independent algebra audit

For one original smooth block pair, set
\(a^{(j)}=\eta_b\beta+i^j\eta_cw\), \(j=0,\ldots,3\). For each real \(v\), define
\[
F_r=\sum_{t\equiv r(q)}a^{(j)}(t)e(vt/H),\qquad
g_r=F_r-\frac1{q-1}\sum_{s\ne0}F_s,\quad r\ne0.
\]
Extend \(g\) by zero at zero, and put
\[
\alpha_m=q^{-1}\sum_{r\ne0}g_re_q(-mr),\qquad
\gamma_n=q^{-1}\sum_{r\ne0}\overline{g_r}e_q(-n\bar r).
\]

**Derived proof:** centering makes both zero-frequency coefficients vanish. Fourier inversion, followed by opening
\(S(m,n;q)=\sum_{r\ne0}e_q(mr+n\bar r)\), gives
\[
\mathcal B_j=\sum_{m,n=1}^{q-1}\alpha_m\gamma_nS(m,n;q)
=\sum_{r\ne0}|g_r|^2.
\]
Parseval and the permutation \(r\mapsto\bar r\) give
\[
\|\alpha\|_2^2=\|\gamma\|_2^2=q^{-1}\|g\|_2^2,
\qquad \boxed{\mathcal B_j=q\|\alpha\|_2\|\gamma\|_2}.
\]
This verifies the archived derivation and saturation, including conjugations. [Archived report:40](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/agent-reports/physical-loop-local-emitter-obligation.md:40)

The diagonal is exactly
\[
d_j(q)=\frac{q-2}{q-1}\sum_{q\nmid t}|a^{(j)}(t)|^2,
\]
and
\[
C_{bc}=\sum_q q\int\psi_+(v)\,
 \frac14\sum_j i^j[\mathcal B_j-d_j(q)]\,dv.
\]
Indeed, \(x\overline y=\frac14\sum_j i^j|x+i^jy|^2\), and the phase integrates to \(\kappa((u-t)/H)\). Smooth blocks give an exact **weighted** pair partition, not disjoint exactly-once coverage. Self-terms cancel before any blockwise triangle. [V59:143](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:143), [V59:275](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:275)

Also, \(U<Q<q\), with exponent gap \(1/1200\); thus every divisor inversion in the report is legitimate.

### 3. BP theorem and chopping budget

**Primary-source statement checked; BP’s full proof was not independently audited.** Theorem 1.1 permits arbitrary complex arrays on integer intervals of cardinalities at most \(N_{\rm BP}\), with \(1\le N_{\rm BP}\le c\), multiplier \(a\) coprime to \(c\), and joint restriction \((m,n,c)=1\). Its bound is
\[
\|\alpha\|_2\|\gamma\|_2c^{1+o(1)}
\left(N_{\rm BP}^{1/8}c^{-3/32}
+N_{\rm BP}^{5/16}c^{-3/16}
+N_{\rm BP}^{2/3}c^{-7/18}\right).
\]
No smoothness hypothesis is required. Here \(c=q\), \(a=1\), and nonzero indices satisfy the gcd condition. At \(N_{\rm BP}\le\lfloor\sqrt q\rfloor\), this gives \(C_\varepsilon q^{31/32+\varepsilon}\|\alpha\|_2\|\gamma\|_2\), uniformly in arrays and interval locations, without an exceptional-prime set. [BP, Theorem 1.1 and §2.1](https://arxiv.org/html/2607.24311v1#Thmtheorem1)

**Derived consequence:** \(N_{\rm BP}=q-1\) is inside the general theorem’s domain, but substitution gives a \(q^{23/18+o(1)}\) ceiling, not the critical saving.

Let \(L=\lfloor\sqrt q\rfloor\), \(K_q=\lceil(q-1)/L\rceil\). Chopping yields \(K_q^2\) rectangles and
\[
\sum_{A,B}\|\alpha_A\|_2\|\gamma_B\|_2
\le K_q\|\alpha\|_2\|\gamma\|_2.
\]
Consequently the worst-case BP/triangle ceiling is
\(q^{47/32+o(1)}\|\alpha\|_2\|\gamma\|_2\), worse than saturation by \(q^{15/32+o(1)}\).

This is a **worst-case reassembly budget**, not a proved physical lower bound on chopping cost. Likewise, “complete-range indexing” does not mean every actual coefficient is nonzero. The report’s \(F=e_1-e_2\) demonstrates possible full support only at the interface level. [Archived report:125](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/agent-reports/physical-loop-local-emitter-obligation.md:125)

### 4. Bounded side question: residual-sensitive obstruction

**New derivation.** Fix a nonzero unsubtracted packet and write \(P=\|\alpha\|_2\|\gamma\|_2\), so \(\mathcal B=qP\). Suppose, at the **value level**,
\[
qP=\sum_\nu\lambda_\nu\mathcal B_q(A_\nu,B_\nu)+R,
\qquad
T=\sum_\nu|\lambda_\nu|\|A_\nu\|_2\|B_\nu\|_2,
\]
where every rectangle satisfies the critical BP hypotheses. Triangle plus BP gives the necessary bound
\[
\boxed{|qP-R|\le C_\varepsilon q^{31/32+\varepsilon}T}.
\]
In particular,
\[
T\ge C_\varepsilon^{-1}q^{1/32-\varepsilon}P
\left(1-\frac{|R|}{qP}\right)_+.
\]

Thus, for fixed \(\theta<1\), residual \(|R|\le\theta qP\) forces
\(T\gg_{\varepsilon,\theta}q^{1/32-\varepsilon}P\).
A fixed-power improvement \(T\ll q^{1/32-\kappa}P\), \(\kappa>0\), cannot coexist with such a residual along growing primes: choose \(\varepsilon<\kappa\).

Do **not** strengthen this to an exact \(q^{1/32}\) lower bound or an exclusion of all logarithmic improvements. Crucially, it does **not** apply automatically to the signed, diagonal-subtracted physical target.

### 5. Compression criterion and actionable corrections

The proposed condition is sufficient if its decomposition, masks, uniformity, and bounds genuinely hold for the **integrated signed**
\[
E_{bcq}=\int\psi_+(v)\frac14\sum_j i^j[\mathcal B_j-d_j(q)]\,dv.
\]
Writing \(\omega_{bc}=(1+|b-c|)^{-A}\), fixed \(A>2\), its assumed cost
\(T_{bcq}\ll\omega_{bc}(H/q)x^{\ell+o(1)}\)
and residual
\(|R_{bcq}|\ll\omega_{bc}Hq^{-1/32}x^{\ell+o(1)}\)
give
\[
|\mathfrak C_x|
\ll (x/H)\,HQ^{2-1/32}x^{\ell+o(1)}
=x^{5/3-1/96+\ell+o(1)}.
\]
All \(o(1)\) terms must be uniform over physical blocks and primes for the fixed inherited profile/hybrid parameters.

The local/global natural scales are \(Q^2H\) and \(xQ^2\). Hence this criterion certifies strict saving only when
\[
\ell<19/2400,\qquad \delta=1/96-\ell>1/400.
\]
The terminal normalization divides by \(x^{2/3+o(1)}\); Gate A remains independently necessary, with
\[
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]
[V59:318](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:318), [V58:305](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:305)

Required corrections: qualify complete support, qualify chopping as worst-case, remove inherited “smooth arrays required” wording, and call \(\ell<19/2400\) necessary **for this sufficient criterion to certify the endpoint**, not universally necessary. Separation decay cannot be extracted from each positive packet before polarization.

Closest checked existing results: [TPC247:70](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70) supplies literal source attachment; [TPC209:156](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:156) supplies fixed-divisor reindexing. Neither supplies this compression.

### 6. Audit receipt and boundary

Proof-writer discipline was applied read-only. Draft source contract preceded the archived report; archived claims were independently rederived.

Commands: `pwd`; `git rev-parse HEAD origin/main`; `git -c core.quotePath=false -c core.fsmonitor=false --no-optional-locks status --porcelain=v1 --untracked-files=all`; `git --no-optional-locks diff --name-only`; `git --no-optional-locks diff --cached --name-only`; `sha256sum` on four controls and three frozen drafts; bounded `rg -n`, `nl -ba`/`sed` reads; inline `python -B -`. **All exited 0.** Primary-URL reads succeeded.

Diagnostics only: 20 cases/80 quadratic packets; maximum discrepancy \(1.16\times10^{-13}\). No physical or asymptotic evidence follows.

Start = end HEAD = origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start = end SHA-256:
```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
DERIVATION_PACKAGE.md
2d7c6cc906650edf1be208dc652e9c24d534565b057317603e7ebbfaa321c288
PROOF_PACKAGE.md
5f977d1e18dc2ec19dc72f08c5b86407141157aea569518e5f5190bedd0512d1
LANE_NORM_PROOF.md
71e7e348f2e0f4332ff1dd4b25330918f9b286c73ee5e44edb16ac4d2a7d155c
```

Tracked dirty **10→10**, untracked **642→642**, index empty; no status-entry additions/removals. Parent-owned loop/review paths were already present and are authorized parent work.

**No-GO boundary:** exact structural identity and scoped obstruction only. Compression remains `NOT CURRENTLY JUSTIFIED`; no arithmetic advance, gate closure, numbered writer, or publication authorization.

---

## Addendum: frozen `LOCAL_EMITTER_PROOF.md`

`task_id: physical-loop-independent-emitter-audit`  
`target_SHA256: dec4ea497b8a24e8bd7e2854de8d71fc40ad1e96ef3360489f794f6df18c2ec4`  
`files_changed: []`  
`integrated_verdict: VERIFIED_SCOPED_E1_E6; E5_COMPRESSION_REMAINS_UNPROVED`  
`readiness_score: 9/10` for the exact scoped document; no publication or arithmetic GO.

**The integrated file faithfully retains the audited mathematical claims. No new fatal proof defect was found.** The original audit above is preserved unchanged; this addendum assesses the concrete integrated target and its added provenance discussion, without repeating the diagnostic work.

### Integrated claim assessment

| Section | Assessment |
|---|---|
| E1 | The Fourier signs, inverse-residue argument, omitted zero frequencies, and unnormalized Kloosterman convention match the audited identity. Both arrays remain complete-range indexed. |
| E2 | The factor \((q-2)/(q-1)\), outer \(q\), kernel orientation, and signed polarization are correct. The explicit prohibition on assigning mixed-expression separation decay to individual positive packets is important and correct. |
| E3 | Exact saturation and the interface-only support example are correctly scoped. No lower bound for the physical signed remainder is asserted. |
| E4 | The critical BP statement and parameters are correctly identified. The displayed chopping inequality supports the stated worst-case upper-bound-method budget, not an inevitable physical loss. |
| E5 | The implication from the stated compression and residual estimates to the strict saving is valid. The document correctly labels those estimates as an unproved sufficient obligation, not a necessary representation or a closed gate. |
| E6 | Its TPC209 provenance and “no free common profiles” conclusion are supported by the cited source, within the qualifications below. |

Exact target anchors: [E1–E2:8](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LOCAL_EMITTER_PROOF.md:8), [E3–E4:65](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LOCAL_EMITTER_PROOF.md:65), [E5:108](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LOCAL_EMITTER_PROOF.md:108), [E6:137](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LOCAL_EMITTER_PROOF.md:137).

The BP source statement was rechecked against the primary page; this does not certify its full proof independently. [BP, Theorem 1.1](https://arxiv.org/html/2607.24311v1#Thmtheorem1)

### E6: source statement versus inference

**Source statements verified:**

- TPC209 assumes a Schwartz \(F_D\) and \((D,q)=1\), then proves the exact reindexing \(Y_{q,D}=U_DB_{q,D}\). [TPC209:143](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:143)
- Its whole-frame formula retains the \(D,E\) cross terms and relative dilation \(D^{-1}E\). Those terms are not disposable errors. [TPC209:195](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:195)
- Its multiplicative-character coordinates contain divisor-dependent profiles. Factoring them into a scalar divisor sum requires an additional common-profile assumption. [TPC209:250](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:250)
- The Gauss crosswalk returns the original nonprincipal-character transform, with its explicit Gauss factor. [TPC209:280](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:280)

**Supported inference:** repeating this exact reindexing alone does not establish E5’s compression estimates. The algebra neither identifies the physical divisor profiles as common nor estimates the other lane. This is not a theorem that coefficient-sensitive Poisson analysis can never help.

### Narrow clarifications recommended

These are precision improvements, not reasons to reject E1–E6:

1. **E4, lines 100–106:** insert “worst-case” before “extra norm reassembly.” The closing qualification already prevents a universal-obstruction reading; this would also prevent interpreting \(q^{1/2}\) as the measured cost of the actual arrays.
2. **E5, lines 125–126:** make the quantifier explicit: constants and \(o(1)\) are uniform over the original block pairs and prime shell for the fixed inherited profile and fixed admissible \(K\), with no unpaid exceptional set.
3. **E6, lines 143–145:** write “Even if an individual smooth divisor strand has controlled short effective dual support…” Schwartz regularity alone supplies decay, not exact compact dual support or a paid truncation error.
4. **E6, line 145:** replace “pay E4” with “pay the compression estimates (E4) in Section E5,” avoiding confusion with Section E4.
5. The residual-sensitive necessary bound in original-audit §4 is not yet included in this integrated file. It can be added as a separate corollary after E3, if desired, with the same \(q^\varepsilon\) qualification and explicit exclusion of the signed diagonal-subtracted target. Its absence is not a defect in the claims currently made.

The first transfer-fatal mismatch and strongest objection remain unchanged: critical length is not supplied, and the raw unsubtracted packets saturate. The integrated text does not claim to have overcome either.

### Addendum preservation receipt

The concrete target hash matched the parent-supplied hash at both start and end:
```text
LOCAL_EMITTER_PROOF.md
dec4ea497b8a24e8bd7e2854de8d71fc40ad1e96ef3360489f794f6df18c2ec4
```

All four locked controls and all three original frozen drafts retained the hashes printed in the original audit. `FINITE_ATTACHMENT_ERRATUM.md` was preservation-hashed only, not proof-audited here:
```text
175312749ce5f24bfbfa90cc1f3bf30efb737aa17d80c5981ac15b0ccde4eae2
```

HEAD and origin/main remained
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

The two newly supplied documents account for untracked **642→644** between the original audit and addendum startup. During this addendum, tracked dirty remained **10→10**, untracked **644→646**, and the index remained empty. The two additional paths were authorized parent archival writes:

- `agent-reports/physical-loop-independent-lane-audit-round1.md`
- `agent-reports/physical-loop-independent-operator-audit-round1.md`

No status entries were removed. Those other agents’ reports were not read or used as proof evidence.

Addendum commands: bounded `nl -ba`/`sed` reads of the target, archived obligation, and directly relevant TPC209 paragraphs; skill-instruction read; the same read-only `git rev-parse`, status, diff, and SHA-256 commands. **All shell commands exited 0; primary-page retrieval succeeded.** No new diagnostics, tests, builds, writes, children, synchronization, or external-model uploads were performed.

**Final addendum boundary:** the frozen integrated document is supported as an exact structural emitter, a scoped full-array saturation statement, and an unproved conditional compression roadmap. Physical fixed-power credit remains zero; Gate A, Gate B, publication GO, and the twin-prime endpoint are unchanged.

</details>

### Implemented corrections

- Restored the original x=2X clock and exact cardinality; explicitly superseded conflicting X=x raw-report notation.
- Defined V_q as the unnormalized sum of squared unit-residue deviations.
- Clarified eventual full-domain, fixed-profile uniformity and the exclusions of arbitrary origins and singleton prefixes.
- Replaced the zero-natural-density semiprime heading, added x>=x0(K), and wrote the two-sided norm comparison.
- Restored the full terminal ledger, including x^(2/3+o(1)), Gate A, 79/96 error and the strict loss margins.
- Qualified emitter chopping as worst-case, made signed integrated uniformity explicit, and distinguished effective dual decay from hard support.
- Added the residual-sensitive critical-rectangle cost corollary with its mandatory epsilon qualification and unsubtracted-only scope.

The initial multi-file correction patch used one wrong path and failed before any file
changed; hashes confirmed the four drafts were still unchanged, then the corrected patch
succeeded. No existing source was overwritten by that failure.

### New bounded follow-up

NEXT_ARITHMETIC_OBLIGATION.md derives the full Kloosterman Gram identity and an
exact one-short/one-complete norm obstruction. Its smooth interior-divisor Fourier
paragraph is being audited specifically for uniform derivative hypotheses; no unpaid
boundary or prime-component smoothness is accepted. A six-prime finite diagnostic
gave Gram error below 5.1e-12 and confirmed the 23/2400 dual-radius exponent.

### Round 2 assignments

Jason (same reviewer) reviews the implemented object/variance/lane-precision deltas.
Leibniz (same reviewer) reviews the emitter deltas plus the new one-sided-support note.
Both tasks are read-only, with baseline 10 tracked dirty, 650 untracked and empty index.
The five updated proof texts are frozen for these audits. Bernoulli continues the
distinct growing-rank physical-operator extension. Publication GO remains false.

## Round 2 — complete; corrections implemented

Scoped scores: operator/precision 9.5/10; emitter/frontier 9/10. No score is
an arithmetic or publication GO. The derivative constants were not present
in the allowed V59 partition statement; NEXT now explicitly assumes them
for the smooth-strand lemma. Its centering and Gram identities remain
unconditional. Added the centered-singleton and post-truncation centering
qualifications, clarified fixed K (not fixed z), literal (possibly complex)
operator, and the arbitrary-origin residue relabeling.

<details><summary>Round-2 operator reviewer — full raw response</summary>

```json
{
  "schema": "TPC_AGENT_RESULT_V1",
  "task_id": "physical-loop-independent-operator-audit-round2",
  "role": "tpc_proof_auditor",
  "mode": "READ_ONLY_RESEARCH_AND_AUDIT",
  "proof_verdict": "PROVABLE AS STATED, importing the separately audited lane core",
  "integration_verdict": "READY_FOR_SCOPED_RESEARCH_INTEGRATION",
  "readiness_score": "9.5/10 for the operator/lane norm-obstruction package only",
  "first_fatal_mismatch": null,
  "arithmetic_advance": false,
  "publication_GO": false,
  "files_changed": []
}
```

The round-1 corrections are correctly implemented. The exact operator theorem and its ordinary/row-normalized lane-cost consequence are ready for unnumbered research integration. This verdict does **not** certify the emitter, next arithmetic obligation, growing-rank extension, novelty, or publication readiness.

### 1. Delta-review findings

| Requested correction | Finding |
|---|---|
| **Source clock and exact cardinality** | Correctly added: \(x=2X\), \(N=\lfloor x\rfloor-\lfloor x/2\rfloor=X+O(1)\). The archived \(X=x\) wording is explicitly superseded without rewriting reports. [DERIVATION_PACKAGE.md:23](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:23) agrees with the original [literal compiler:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md:43). |
| **Eventual uniformity and prefix exclusions** | Correctly states fixed-profile, complete-domain bounds for every physical row, with no exceptional rows. Unrestricted-profile, arbitrary-origin row-energy, and coordinate/prime-prefix extensions are excluded. The singleton zero-energy example is valid. [DERIVATION_PACKAGE.md:168](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:168) |
| **P4 unnormalized variance** | Correct. The explicit definition divides only the residue mean by \(q-1\), not the sum of squared deviations. Thus the factor \(q/N\) in \(R_0\) remains correct, with no missing \(q-1\). [PROOF_PACKAGE.md:132](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:132) matches [V59:230](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:230). |
| **Lane heading, threshold, and clock** | The false positive-density terminology is replaced by “order \(x/\log x\).” The threshold \(x\ge x_0(K)\), including \(z\ge2\), and the inherited clock are explicit. [LANE_NORM_PROOF.md:8](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:8), [line 70](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:70). |
| **Two-sided norm comparison** | Correctly inserted: \(\big|\|w\|_2-\|\Lambda(\cdot+2)\|_2\big|\le\|b_x^{(z)}\|_2\). Together with the imported small-hybrid norm estimate, this justifies the asymptotic without assuming orthogonality. [LANE_NORM_PROOF.md:59](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:59) |
| **Dependencies and terminal ledger** | The derivation identifies separate operator/lane audits and the separately audited emitter report. The \(K_*\), error exponent, Gate-A requirement, and strict three-way margin agree with V58. [DERIVATION_PACKAGE.md:174](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:174) |

**Imported dependency, not a fresh lane-core audit:** the archived [lane verdict:7](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/agent-reports/physical-loop-independent-lane-audit-round1.md:7) accepts L1–L6 with declared operator dependencies. Its [dependency statement:108](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/agent-reports/physical-loop-independent-lane-audit-round1.md:108) imports precisely P7 and row-energy comparability.

There is no circular proof: the operator identities, row-energy estimates, constant-mode bound, and P8 algebra do not require the lane theorem. The independent lane estimates are then combined with those operator results.

### 2. Supported mathematical conclusion

The round-2 changes do not alter the previously audited operator:
\[
A_q(u,t)=q\kappa((u-t)/H)
\left(1_{u\equiv t\pmod q}-\frac1{q-1}\right)
1_{q\nmid u}1_{q\nmid t}1_{u\ne t}.
\]
The outer \(q\), negative centering, both unit masks, deleted diagonal, and kernel orientation remain intact. The exact scalar remains \(\mathfrak C_x=\langle w,A\beta\rangle\). [DERIVATION_PACKAGE.md:89](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:89)

The physical contract remains:

- \(h_0=2\), independent of \(H\), conductor, and \(u-t\).
- \(x=2X\), \(I=(x/2,x]\cap\mathbb Z\), exact \(N=|I|\).
- \(Q=x^{1/3}\), \(H=x^{21/32}\), \(U=x^{133/400}\), all primes \(Q<q\le2Q\).
- \(\beta(t)=\Lambda(t)/\log t-\sum_{d\mid t,\ d\le U}\mu(d)\) and \(w(u)=\Lambda(u+2)-b_x^{(z)}(u)\), retaining the hybrid mask at forbidden residue \(-2\), including prime \(2\).
- \(K\) fixed before the large-\(x\) threshold; constants may depend on \(K\) and the fixed profile.
- Full ordered off-diagonal pairs, not a block substitute. Increasing-coordinate or increasing-prime prefixes are not certified.

**Derived integration consequence.** The audited results combine to give
\[
G\asymp_\psi\frac{HQ^2}{\log Q},\qquad
\|A\|\ge(3/2+o(1))\frac{Q^2}{\log Q},
\qquad
H^{-1}\ll_\psi\|Z\|\ll_\psi\frac{\log Q}{H},
\]
and, importing the audited arithmetic lane bounds,
\[
\liminf_{x\to\infty}
\frac{\log Q}{xQ^2}\,
\|A\|\,\|\beta\|_2\,\|w\|_2
\ge \frac34\sqrt{\log(27/22)}>0.
\]
The particular row normalization retains this obstruction up to fixed profile constants. [LANE_NORM_PROOF.md:128](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:128)

### 3. Full physical budget and boundary

**Source statement:** V58 requires a separate Gate-A estimate and \(\delta>1/400\), divides by \(K_*=x^{2/3+o(1)}\), and yields
\[
|S_x|\ll x^{399/400-\eta+o(1)},\qquad
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]
Its three physical exponents are \(399/400-\eta_A\), \(1-\delta\), and \(79/96\). The revised draft matches this ledger. [V58:305](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:305)

**Derived bookkeeping:** with benchmark \(1/96\) and additional loss exponent \(\ell\), the effective saving is \(\delta=1/96-\ell\); therefore \(\ell<19/2400\), strictly. None of the norm estimates pays that requirement.

**First fatal mismatch:** none in the corrected scoped theorem. The first fatal mismatch in a proposed positive norm-only application remains
\[
\frac{xQ^2/\log Q}{xQ^2x^{-\delta+o(1)}}
=\frac{x^{\delta-o(1)}}{\log Q}\longrightarrow\infty
\quad(\delta>0).
\]

**Strongest objection to promotion:** a lower bound on a norm-product upper-bound expression is not a lower bound on the literal mixed scalar. No coefficient-sensitive cancellation theorem follows.

**Closest existing result:** V59’s exact reduced-residue variance-minus-diagonal identity, now used with an explicit normalization; the current conclusion adds a scoped norm-method obstruction, not Gate-B saving.

Position remains island ②, image Bridge A, repository Gate B. Formal endpoint TPC418 is unchanged. Neither analytic gate nor the dynamics/C bridge is closed.

### 4. Remaining nonblocking precision issues

These do not invalidate research integration:

1. At [LANE_NORM_PROOF.md:6](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:6), replace “fixed \(z=(\log x)^K\)” with “\(z=(\log x)^K\) for fixed \(K>0\).” The surrounding proof already uses the correct quantifier.
2. At [DERIVATION_PACKAGE.md:152](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:152), prefer “literal physical operator” to “real physical operator.” Entries need not be real for the permitted non-even profile.
3. After the residue relabeling at [PROOF_PACKAGE.md:149](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:149), optionally write \(S_j^\#=S_{a+j\bmod q}\); the excluded index satisfies \(a+j\equiv0\pmod q\), not necessarily \(j=q\). The current “relabel” wording supports the correct proof.

The narrow next action is to integrate the scoped operator/lane result with these clarifications, while keeping emitter and growing-rank verdicts separate.

### 5. Preservation and command receipt

No new numerical diagnostics or external theorem checks were needed for this bounded delta review. Prior diagnostics were not rerun or promoted to proof evidence.

All shell commands exited **0**: bounded `sed -n`, `nl -ba`, and targeted `rg -n` reads; `sha256sum`; and:

```text
git --no-optional-locks rev-parse HEAD origin/main
git --no-optional-locks status --porcelain=v1 --untracked-files=all
git --no-optional-locks diff --name-only
git --no-optional-locks diff --cached --name-only
```

Start/end HEAD and local origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Status: **10 tracked dirty / 650 untracked / empty index → unchanged**. No added or removed status entries. Unfrozen parent-owned review/round contents remain authorized and were not claimed bytewise immutable. No writes, children, synchronization, builds, regeneration, downloads, or external-model uploads occurred.

All nine start/end hashes matched the round-2 envelope:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
round/DERIVATION_PACKAGE.md
4f05f03f0e71c7bc84c14cb15fec11bfccdce9b20cb3d36b6303eb381d960b38
round/PROOF_PACKAGE.md
8c8e926c22e77f28a435bd462bbcb3a9b4c6536366feda8ace25b92a899a6571
round/LANE_NORM_PROOF.md
ea3069f5f2c9244f0b0c686a19151eb2e27ae3d0be25257523381b1224a53d35
round/LOCAL_EMITTER_PROOF.md
52b6527cce13e016f8abfb21ba4043d4a6f71c319a9d6af95ab8576e1c932c91
round/NEXT_ARITHMETIC_OBLIGATION.md
268f66c6e0fb21afd5b7b3604a995af63ff9b4603ac67e06e1825db978416247
```

The last two files were hash-checked only, not substantively audited.

</details>

<details><summary>Round-2 emitter reviewer — full raw response</summary>

## TPC_AGENT_RESULT_V1

`task_id: physical-loop-independent-emitter-audit-round2`  
`role: tpc_proof_auditor`  
`mode: READ_ONLY_RESEARCH_AND_AUDIT`  
`files_changed: []`  
`readiness_score: 9/10` for the exact scoped results—not publication readiness.

**Verdict:** implemented emitter corrections and E3a are verified. The new centering identity and F1/F2 are unconditional finite algebra. The Fourier-decay/radius paragraph is **CONDITIONAL on explicit uniform scaled derivative bounds**; those bounds are not established by the allowed V59 partition definition.

**Research integration:** ready after that minimal assumption-label correction. No arithmetic saving or publication GO follows.

### 1. First mismatch and physical contract

**First proof-level qualification:** [NEXT_ARITHMETIC_OBLIGATION.md:16](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/NEXT_ARITHMETIC_OBLIGATION.md:16) attributes quantitative uniform smoothness to the frozen partition. [V59:277](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:277) states a smooth bounded-overlap length-\(H\) partition, but does not record the required scaled derivative constants. Smoothness alone does not imply their uniformity.

**First arithmetic-transfer mismatch:** shortening one smooth divisor strand does not shorten or estimate the second array. **Strongest objection:** the one-short/one-complete operator norm is exactly \(q\), even on the appropriate centered subspaces.

The current source contract retains
\[
I_x=(x/2,x]\cap\mathbb Z,\quad x=2X,\quad
N=|I_x|=X+O(1),
\]
\[
Q=x^{1/3},\quad Q<q\le2Q\ (q\text{ prime}),\quad
H=x^{21/32},\quad U=x^{133/400},
\]
\[
\beta(t)=\frac{\Lambda(t)}{\log t}-\sum_{d\mid t,\ d\le U}\mu(d),
\qquad w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
Thus the earlier archived \(X=x\) notation is superseded. The target remains
\[
\sum_q q\sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
\beta(t)w(u)\kappa((u-t)/H)
\left(1_{u\equiv t(q)}-\frac1{q-1}\right).
\]
The fixed physical shift is \(h_0=2\), not \(H\) or the conductor. The hybrid, Möbius signs, prime-power term, both unit masks, outer \(q\), and diagonal deletion are unchanged. No prefix replacement or maximal-prefix estimate is made. [DERIVATION_PACKAGE.md:16](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:16)

### 2. Implemented emitter corrections and E3a

The corrections are faithful: worst-case chopping is explicitly qualified; E5 states uniformity over original block pairs and the complete prime shell, for fixed inherited profile and admissible \(K\), without unpaid exceptional sets; E6 uses conditional effective-support language and correctly identifies the compression estimates. [LOCAL_EMITTER_PROOF.md:104](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LOCAL_EMITTER_PROOF.md:104)

E3a correctly preserves
\[
|qP-R|\le C_\varepsilon q^{31/32+\varepsilon}T,\qquad
T\ge C_\varepsilon^{-1}q^{1/32-\varepsilon}P
\left(1-\frac{|R|}{qP}\right)_+.
\]
For a family along growing primes, fixed \(|R|\le\theta qP\), \(\theta<1\), excludes a uniform cost \(T\ll q^{1/32-\kappa}P\): choose \(\varepsilon<\kappa\). The text correctly excludes an epsilon-free lower bound, universal logarithmic obstruction, and application to the signed diagonal-subtracted scalar. [LOCAL_EMITTER_PROOF.md:84](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LOCAL_EMITTER_PROOF.md:84)

BP’s primary theorem was rechecked: arbitrary complex interval arrays, unit multiplier, joint gcd restriction, and the critical \(q^{31/32+o(1)}\) bound. No independent certification of its full proof is claimed. [BP, Theorem 1.1](https://arxiv.org/html/2607.24311v1#Thmtheorem1)

### 3. Conditional smooth-strand decay: proof and minimal correction

Replace the attribution at NEXT lines 14–17 with:

> **Conditional smooth-strand lemma.** Assume the original interior cutoffs extend to \(C_c^\infty((x/2,x))\), have support diameter at most \(C_0H\), and satisfy, for every integer \(j\ge0\),
> \[
> \sup_{x,b}H^j\|\eta_b^{(j)}\|_\infty\le C_j<\infty.
> \]
> These quantitative constants are additional hypotheses here, not supplied by V59’s qualitative partition statement.

**Independent derivation:** for
\(F_d(s)=\eta_b(ds)e(vds/H)\),
\[
\widehat F_d(\xi)=d^{-1}\widehat{\eta_b}(\xi/d-v/H).
\]
Integration by parts under the displayed hypotheses gives
\[
|\widehat F_d(\xi)|
\ll_{A,C_0,C_1,\ldots}(H/d)
\left(1+\left|(H/d)\xi-v\right|\right)^{-A}.
\]
Constants are uniform in interior \(b\), \(d\le U\), and \(|v|\le1\). The latter range covers the inherited profile’s support.

Writing \(\rho_d=qd/H\), the center is \(n=\rho_dv\), and
\[
\rho_d\le qU/H=x^{23/2400+o(1)}\ll q^{1/2}.
\]
The exponent is correct.

A precise optional tail statement follows, for \(A>1\), \(T\ge2\):
\[
\sum_{|n|>T\max(1,\rho_d)}
|\widehat F_d(n/q)|\ll_A qT^{1-A}.
\]
This follows by summing the displayed decay bound; it is **not** a paid full-expression residual estimate. Signed representatives give a short interval containing both positive and negative frequencies, with the zero coordinate omitted/set to zero.

The text correctly retains the radius-below-one caveat. Boundary blocks cannot inherit this argument after a sharp interval truncation without additional work. Neither \(\Lambda/\log\), shifted primes, nor the full hybrid becomes smooth. The signed divisor sum, cross terms, and literal coefficients remain mandatory. [NEXT:7](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/NEXT_ARITHMETIC_OBLIGATION.md:7)

### 4. Exact unit-centering cancellation

The formula at [NEXT:37](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/NEXT_ARITHMETIC_OBLIGATION.md:37) is correct without derivative hypotheses.

Let \(B\) denote the strand’s mass on multiples of \(q\). For \(m\ne0\), unit restriction gives \(Y_m-B\); subtracting the unit-residue mean contributes \(+(Y_0-B)/(q-1)\). Therefore
\[
\alpha_m=q^{-1}\left(Y_m-\frac{qB-Y_0}{q-1}\right).
\]
Since \(K\mathbf1=K^*\mathbf1=\mathbf1\) and the other emitted array satisfies \(\sum_n\gamma_n=0\), the constant correction contributes zero to the complete bilinear form.

**Boundary:** this cancellation uses the complete centered second array. After an arbitrary truncation of that array, its sum need not remain zero; the constant cannot then be discarded without compensation.

Relabeling \(r\equiv md\pmod q\) gives \(S(\bar d r,n;q)\). Since \(d\le U<q\), the multiplier is a unit. This exact relabeling does not identify divisor-dependent profiles as common.

### 5. F1/F2: unconditional proof and exact scope

For every prime \(q>2\),
\[
(KK^*)_{m,m'}
=q\sum_{r\ne0}e_q((m-m')r)
-\left(\sum_{r\ne0}e_q(mr)\right)
 \left(\sum_{s\ne0}e_q(-m's)\right)
=q^2 1_{m=m'}-q-1.
\]
Thus
\[
KK^*=q^2I-(q+1)J,\qquad K\mathbf1=K^*\mathbf1=\mathbf1.
\]
The draft’s constants and signs are correct. [NEXT:58](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/NEXT_ARITHMETIC_OBLIGATION.md:58)

For any row set \(\mathcal I\) with at least two indices, choose a unit mean-zero vector \(a\) supported there, extended by zero. Then
\[
\gamma=K^*a/q
\]
is centered and has norm one. Taking \(\alpha=\overline a\) respects the unconjugated bilinear convention and yields
\[
\sum_{m,n}\alpha_m\gamma_nK_{mn}
=a^*KK^*a/q=q.
\]
Together with the Gram upper bound, this proves \(\|K_{\mathcal I}\|=q\), including the both-centered restriction. Unit row permutations preserve the calculation.

The singleton row norm \(\sqrt{q^2-q-1}\) is also correct. Add the clarification that a **centered singleton first vector is necessarily zero**; the both-centered counterexample uses at least two indices.

These extremizers are an interface class, not evidence that the literal arithmetic second lane realizes them.

### 6. Remaining budget and no-GO boundary

The \(23/2400\) radius exponent is neither an arithmetic saving nor automatically a loss exponent. The physical scales remain \(Q^2H\) locally and \(xQ^2\) globally. E5 still requires a paid two-sided decomposition and residual budget giving
\[
|\mathfrak C_x|\ll xQ^2x^{-1/96+\ell+o(1)},\quad
\ell<19/2400,\quad \delta=1/96-\ell>1/400.
\]
Terminal division by \(x^{2/3+o(1)}\) leaves
\[
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\};
\]
Gate A remains separately open. [V59:318](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:318)

Closest existing result: TPC209’s exact fixed-divisor Poisson reindexing, with retained relative permutations and non-common profiles. It supplies provenance, not this unpaid arithmetic estimate. [TPC209:156](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:156), [TPC209:267](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:267)

Position: island ②, image Bridge A/Gate B. Formal endpoint TPC418; no gate closure, numbered writer, publication GO, or physical fixed-power credit.

### 7. Audit receipt

Proof-writer discipline was used read-only. No diagnostics, tests, builds, repository writes, children, synchronization, or external-model uploads ran.

Commands: required startup `sed` reads; bounded `nl -ba`/`sed` reads of allowed sources; `sha256sum` on nine frozen files; `git rev-parse HEAD origin/main`; `git -c core.quotePath=false -c core.fsmonitor=false --no-optional-locks status --porcelain=v1 --untracked-files=all`; `git --no-optional-locks diff --name-only` and `diff --cached --name-only`. **All shell exits 0; primary-page retrieval succeeded.**

Start=end HEAD=origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start=end hashes:
```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
DERIVATION_PACKAGE.md
4f05f03f0e71c7bc84c14cb15fec11bfccdce9b20cb3d36b6303eb381d960b38
PROOF_PACKAGE.md
8c8e926c22e77f28a435bd462bbcb3a9b4c6536366feda8ace25b92a899a6571
LANE_NORM_PROOF.md
ea3069f5f2c9244f0b0c686a19151eb2e27ae3d0be25257523381b1224a53d35
LOCAL_EMITTER_PROOF.md
52b6527cce13e016f8abfb21ba4043d4a6f71c319a9d6af95ab8576e1c932c91
NEXT_ARITHMETIC_OBLIGATION.md
268f66c6e0fb21afd5b7b3604a995af63ff9b4603ac67e06e1825db978416247
```

Tracked dirty **10→10**, untracked **650→650**, index empty; no status additions/removals. Parent-owned round paths remain authorized parent work.

</details>

### Next bounded parent work

Bernoulli's growing-rank extension remains independent work in progress.
The parent is checking whether an explicit admissible partition can supply
uniform derivative constants and whether the boundary terms can be paid
using the already audited ordinary operator bound. This would be a source-
compatible recompilation of the unchanged scalar, not an estimate for an
arbitrary previously chosen partition or any arithmetic gate closure.

## Round 3 — constructive partition and boundary audit

Scoped score 9/10, S1–S5 verified for the declared critical-array benchmark.
The parent implemented the general margin delta=min(delta_int,11/64) and
clarified that weighted packet contributions, not a disjoint set of integer
pairs, are removed collectively. The existing scalar and coefficient sources
are unchanged. NEXT's formerly additional derivative hypothesis is now proved
for the expressly selected admissible interior partition, not arbitrary old
partitions. The signed interior estimate remains open.

<details><summary>Round-3 partition reviewer — full raw response</summary>

## TPC_AGENT_RESULT_V1

`task_id: physical-loop-independent-partition-audit-round3`  
`role: tpc_proof_auditor`  
`mode: READ_ONLY_RESEARCH_AND_AUDIT`  
`files_changed: []`  
`proof_verdict: S1–S5_VERIFIED_FOR_STATED_BENCHMARK; NEXT_CORRECTIONS_VERIFIED`  
`readiness_score: 9/10` for scoped research integration, not publication GO.

**First fatal mismatch: none within the expressly stated benchmark.** The explicit partition supplies the missing derivative bounds, and the collective boundary estimate is correct. One terminal-ledger clarification is needed if the note is later applied beyond that benchmark.

### S1 — Explicit partition: verified

Let \(f(s)=\chi(s)/D(s)\). Local finiteness and the flatness of the standard bump at its endpoints make \(D\) smooth. Every real number lies within \(1/4\) of a half-integer, so
\[
D(s)\ge\min_{|u|\le1/4}\chi(u)>0.
\]
Its \(1/2\)-periodicity gives bounded derivatives of \(D^{-1}\). Moreover,
\[
D(s-j/2)=D(s),\qquad \eta_{j,H}(t)=f(t/H-j/2).
\]
Consequently
\[
H^r\|\eta_{j,H}^{(r)}\|_\infty=\|f^{(r)}\|_\infty,
\]
uniformly in \(x,H,j\). Positivity, partition of unity, support length \(H\), at most three overlapping closed supports, and at most two positive terms follow directly. Relevant centers lie in an interval of length \(x/2+H\), giving \(O(x/H+1)\) labels. [CONSTRUCTIVE_PARTITION_PROOF.md:17](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/CONSTRUCTIVE_PARTITION_PROOF.md:17)

**Partition-selection distinction: correctly preserved.** V59’s weighted pair identity follows from
\(\sum_{j,k}\eta_j(t)\eta_k(u)=1\), so it can be recompiled using this explicit admissible family. This does not identify its individual packets with those from an arbitrary previously frozen partition. Future packet estimates must use these new coefficients explicitly. [V59:277](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:277)

### S2 — Boundary labels and support: verified

A relevant closed support that is not contained in \((a,b)\) must contain \(a\) or \(b\). At most three closed supports contain either endpoint, hence
\[
|\mathcal J_\partial|\le6.
\]
Any point of such a support inside \([a,b]\) lies within \(H\) of the corresponding endpoint. Therefore
\[
\operatorname{supp}_{I_x}\theta_\partial
\subset I_x\cap([a,a+H]\cup[b-H,b]),
\qquad |\operatorname{supp}_{I_x}\theta_\partial|=O(H+1).
\]
The weights lie in \([0,1]\). Every interior cutoff has compact support strictly inside \((a,b)\), so it is genuinely \(C_c^\infty((a,b))\); no sharp truncation is hidden. [Constructive proof:55](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/CONSTRUCTIVE_PARTITION_PROOF.md:55)

### S3 — Literal pointwise envelopes: verified

The included elementary proof of \(\tau(n)\ll_\varepsilon n^\varepsilon\) is valid. Since \(0\le\Lambda(n)/\log n\le1\) for the relevant \(n>1\),
\[
|\beta(n)|\le1+\tau(n).
\]
For fixed \(K>0\), eventually \(z=(\log x)^K\ge2\). All primes in the hybrid’s remaining product exceed \(2\), and
\[
\frac{p-1}{p-2}\le2,\qquad
0\le b_x^{(z)}(n)\le W_z\,2^{\omega(n)}
\le W_z\tau(n).
\]
The imported Mertens bound \(W_z\ll\log z\) applies at exactly this \(z\), giving \(W_z\ll_K\log\log x\). Together with \(\Lambda(n+2)\le\log(x+2)\), this proves
\[
|\beta(n)|+|w(n)|\ll_{\varepsilon,K}x^\varepsilon
\]
uniformly on \(I_x\). Taking a smaller divisor exponent absorbs logarithms.

Thus the stated boundary norms are \(H^{1/2}x^{o(1)}\), and the full-length norms used are \(x^{1/2+o(1)}\). These are upper envelopes only; no physical coefficient is replaced. [Constructive proof:78](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/CONSTRUCTIVE_PARTITION_PROOF.md:78), [LANE_NORM_PROOF.md:39](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/LANE_NORM_PROOF.md:39)

### S4 — Collective boundary cost: verified

The exact identity
\[
\mathfrak C_x-\mathfrak C_x^{\rm int}
=w_\partial^TA\beta+w_{\rm int}^TA\beta_\partial
\]
counts the double-boundary contribution once. It does not require the smooth weights to be projections.

**Imported applicability checked:** equation **(P4)** is an ordinary operator bound for the same \(A\), with its unit masks, outer prime weights, kernel and deleted diagonal:
\[
\|A\|\le4B_\psi(H+4Q^2)+3Q^2\ll_\psi Q^2.
\]
It is partition-independent, and \(H<Q^2\) at the physical scales. This refers to equation (P4), not the separately numbered “P4” section heading. [PROOF_PACKAGE.md:71](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:71)

Euclidean Cauchy–Schwarz therefore gives
\[
|\mathfrak C_x-\mathfrak C_x^{\rm int}|
\ll_{\psi,K}Q^2\sqrt{xH}\,x^{o(1)}
=xQ^2x^{-11/64+o(1)}.
\]
The transpose causes no problem: the physical lanes are real, even when \(A\) is complex Hermitian.

This removes the **weighted packet contribution with a boundary label**, collectively. It is not a claim of disjoint integer-pair deletion or separate absolute bounds for every polarized packet. [Constructive proof:120](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/CONSTRUCTIVE_PARTITION_PROOF.md:120)

### S5 — Scope and exponent ledger: verified with clarification

For this constructed partition, the interior derivative hypotheses in `NEXT` now hold by proof. Boundary error is below the prospective benchmark because
\[
\frac{11}{64}-\frac1{96}=\frac{31}{192}>0.
\]
Hence for \(0\le\ell<19/2400\), it does not consume the intended saving
\(\delta=1/96-\ell>1/400\). [Constructive proof:151](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/CONSTRUCTIVE_PARTITION_PROOF.md:151)

**Minimal clarification:** add:

> If a future interior estimate has saving \(\delta_{\rm int}\) outside this benchmark, this argument certifies the full saving \(\delta=\min(\delta_{\rm int},11/64)\).

Equivalently, the general terminal ledger must include the boundary margin
\(11/64-1/400=271/1600\). For the stated benchmark it is redundant, so the existing ledger is valid:
\[
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]

### Round-two `NEXT` corrections

All requested corrections are faithfully implemented: explicit conditional derivative hypotheses; the individual-strand tail bound and its unpaid-reassembly qualification; complete-centered-second-array requirement for constant annihilation; and the centered-singleton caveat. [NEXT_ARITHMETIC_OBLIGATION.md:14](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/NEXT_ARITHMETIC_OBLIGATION.md:14), [NEXT:53](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/NEXT_ARITHMETIC_OBLIGATION.md:53)

The constructive note discharges those hypotheses **for its selected interior cutoffs only**, not for arbitrary old partitions.

### Physical invariants and remaining objection

The unchanged contract is
\[
x=2X,\quad N=\lfloor x\rfloor-\lfloor x/2\rfloor=X+O(1),\quad
Q=x^{1/3},\ H=x^{21/32},\ U=x^{133/400},
\]
with \(Q<q\le2Q\) prime, \(h_0=2\), literal signed \(\beta,w\), full ordered domain \(t,u\in I_x\), \(t\ne u\), both unit masks and outer \(q\). Local/global natural scales remain \(Q^2H\) and \(xQ^2\). Constants are uniform eventually for fixed bump, inherited profile and admissible \(K\), without an exceptional arithmetic set. No maximal-prefix claim is made. [DERIVATION_PACKAGE.md:16](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:16)

**Strongest remaining objection:** the signed interior estimate, second-array structure and divisor/tail reassembly remain unpaid. The boundary result does not overcome the one-short/one-complete norm obstruction.

**Integration recommendation:** accept as a scoped constructive-partition and boundary-remainder result, with the clarification above. Island ②, image Bridge A/Gate B; TPC418 remains the formal endpoint. No full-scalar saving, gate closure, novelty claim, numbered writer or publication GO.

### Preservation receipt

Proof-writer discipline was used read-only. No other reviewers’ reports, diagnostics or tests were used. No code tests, builds, writes, children or synchronization ran.

Commands: required `sed` startup reads; bounded `rg -n`, `nl -ba`/`sed` source reads; `sha256sum`; `git rev-parse HEAD origin/main`; read-only porcelain status; `git --no-optional-locks diff --name-only` and cached equivalent. **All shell exits 0.**

Start=end HEAD=origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start=end hashes:
```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
CONSTRUCTIVE_PARTITION_PROOF.md
ddc2edc80aef8215bac03eff0cad4079ba0c6322fbf4c61ce69bcf8ce9d259e1
NEXT_ARITHMETIC_OBLIGATION.md
6de599ca72961c747773eb004a2ceb952fb89ce7fe61b8f1cfbf35e2f60e137a
PROOF_PACKAGE.md
177ee528709683c45bbe84e98156d27d297fd3d8fb7938f51eb68d0fd6270bab
LANE_NORM_PROOF.md
4b5182cded6fa2a357135228e3ff3dd710e617ef57c56d83f08fee60ae6a95ef
DERIVATION_PACKAGE.md
51f92d89a5aa314a910f492ddd0248fd3fa0cd5b1bb9e9f0d2da3ef2cab75e5b
```

Tracked dirty **10→10**; untracked **653→654**; index empty. Only addition: authorized parent `DIAGNOSTIC_RECEIPT_ROUND3.md` under the round directory. It was not read or treated as proof evidence.

</details>

### Verification and orchestration record

Extended finite checks passed normal and optimized modes with byte-identical
stdout: 662 rational projection entries, 80 complex packets, 2 physical-index
matrices with an explicitly diagnostic shifted-Gaussian kernel, 6 complete
Kloosterman Gram/saturation cases, and 100 partition configurations (10,100
sampled points). Exact exponent checks retain 23/2400 and 11/64. Complete
outputs are in DIAGNOSTIC_RECEIPT_ROUND3.md; no asymptotic credit is assigned.
A JavaScript orchestrator attempt used unavailable structuredClone after a
reviewer resume; no task message or file write happened in that attempt. It
was immediately retried with JSON cloning and the bounded task was delivered.
No required scientific checker failed. Tracked diff whitespace check passed.

Bernoulli's completed scope acknowledgement correctly restricts the new
negative-subspace theorem to complex dimensions and complex-linear ranks;
a consolidated complete theorem report is requested before archival or use.
No real-only growing-rank theorem or identification with beta,w is claimed.

## Round 3 — growing-rank proof audit

Scoped score 9.5/10; the actual complex-operator theorem is ready for research
integration. The positive compression trace and pointwise deleted diagonal,
not a one-vector extrapolation, prove k_x=(1/4+o(1))Q² negative directions
and the low-rank obstruction. Implemented all minimum scope clarifications:
common threshold enlargement for optional imports, explicit orthogonal
compression, and cutoff necessity only for this proof (no unsupported
counterexample to whole-band negativity).

<details><summary>Round-3 growing-rank reviewer — full raw response</summary>

```json
{
  "schema": "TPC_AGENT_RESULT_V1",
  "task_id": "physical-loop-independent-growing-rank-audit-round3",
  "role": "tpc_proof_auditor",
  "mode": "READ_ONLY_RESEARCH_AND_AUDIT",
  "proof_verdict": "PROVABLE AS STATED",
  "integration_verdict": "READY_FOR_SCOPED_COMPLEX_OPERATOR_RESEARCH_INTEGRATION",
  "readiness_score": "9.5/10 for the stated growing-rank theorem, not arithmetic GO",
  "first_fatal_mismatch": null,
  "arithmetic_advance": false,
  "publication_GO": false,
  "files_changed": []
}
```

The new multiplicity and deflation argument survives independent audit. It does **not** infer multiplicity from P7’s constant-vector witness: the shifted Fourier band, positive-compression trace, pointwise diagonal bound, and spectral cutoff supply the missing argument. No substantive theorem correction is needed; minor scope clarifications are listed below.

### 1. Independent verification of the theorem

**Source identification.** The matrix in [GROWING_RANK_PROOF.md:31](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:31) equals the literal [TPC247 operator:70](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70). Reality of the profile gives \(K_H(-h)=\overline{K_H(h)}\), so \(A_x\) is Hermitian, not necessarily real. The inherited reflection convention is retained.

**1. Positive form, orientation, and normalization — correct.** With
\[
d_q=\frac{q(q-2)}{q-1},\qquad
U_x=A_x+\operatorname{diag}\Delta_x,
\]
direct expansion gives
\[
\langle f,U_xf\rangle
=\sum_q q\int\psi_+(v)\mathcal V_q[f](v)\,dv.
\]
The positive phase in \(T_{q,r}[f](v)\) is correct: conjugating its output factor produces \(e(-vu/H)e(vt/H)\), matching \(K_H(u-t)\). For \(f_j(n)=N^{-1/2}e(jn/N)\), the variance has argument \(j/N+v/H\) and exactly the factor \(1/N\). No extra division by \(q-1\) occurs. [GROWING_RANK_PROOF.md:79](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:79)

**2. Uniform residue estimate — correct.** The incomplete-cycle formula uses representatives \(a+b\), so it does not silently move the excluded residue. For \(0<|\alpha|q\le1/2\),
\[
|G_\ell(\alpha q)|\le(2|\alpha|q)^{-1},\qquad
|e(\alpha b)-1|\le2\pi|\alpha|q.
\]
Every residue sum lies within \(\pi+1\) of a common center. At \(\alpha=0\), the distance is at most \(1\). Minimization over the unit-residue mean therefore yields
\[
V_q^{\rm raw}(\alpha)\le C_0q,\qquad C_0=(\pi+1)^2.
\]
This includes interval edges, incomplete cycles, and the band endpoints. [GROWING_RANK_PROOF.md:118](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:118)

**3. Fourier band and positive-compression trace — correct.** Once \(d_x<N\), the consecutive modes \(-J_x,\ldots,J_x\) are distinct modulo \(N\) and exactly orthonormal on the actual \(N\) consecutive integers. The floor defining \(J_x\) ensures
\[
q|j/N+v/H|\le2Q(J_x/N+1/H)\le\tfrac12
\]
for every retained mode, every \(v\in[-1,1]\), and every shell prime.

Writing \(B_x=F_x^*U_xF_x\) and \(M_1=\sum_q q\),
\[
B_x\succeq0,\qquad
\operatorname{tr}B_x
\le\frac{d_xC_0}{N}\sum_q q^2
\le C_0(1+2Q/N)M_1.
\]
This bounds the **trace**, not the whole-band norm by a single-mode estimate. [GROWING_RANK_PROOF.md:143](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:143)

**4. Pointwise deleted diagonal — correct.** Every physical integer satisfies \(n\le x=Q^3\), so three distinct primes greater than \(Q\) cannot divide it. Each omitted \(d_q<q\le2Q\); hence, at every row,
\[
\Delta_x(n)\ge D_*:=\sum_qd_q-4Q.
\]
Since \(d_q=q-1-1/(q-1)\),
\[
D_*\sim M_1\sim\tfrac32\tau_x,\qquad \tau_x=Q^2/\log Q.
\]
This is the required pointwise bound, not an averaged diagonal estimate. The weighted asymptotics follow by partial summation from the cited [Selberg PNT, p. 305, (1.1)](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf). [GROWING_RANK_PROOF.md:164](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:164)

**5. Cutoff and the constant 35 — correct and conservative.** The number of eigenvalues of \(B_x\) exceeding \(D_*/2\) satisfies
\[
\#\{\lambda>D_*/2\}\le\frac{2\operatorname{tr}B_x}{D_*}
=2C_0(1+o(1))<35.
\]
Indeed \(2(\pi+1)^2<35\); the strict numerical margin is genuine. The integer count is actually at most \(34\), so allowing a loss of \(35\) dimensions is safe.

On the retained spectral subspace,
\[
\langle f,A_xf\rangle
\le(D_*/2-D_*)\|f\|^2
\le-\tau_x\|f\|^2/2.
\]
The cutoff includes eigenvalues equal to \(D_*/2\), correctly. [GROWING_RANK_PROOF.md:179](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:179)

**6. Dimension, constraints, and deflation — correct.** From the exact floor,
\[
k_x=d_x-35
=\frac{N}{2Q}-\frac{2N}{H}+O(1)
=\frac{Q^2}{4}-x^{11/32}+O(1)
\sim Q^2/4.
\]
This is the specified guaranteed dimension, not an exact count of all negative eigenvalues.

Hermitian min–max gives at least \(k_x\) eigenvalues at most \(-\tau_x/2\). For any complex-linear constraint map \(L\) of rank \(r\),
\[
\dim(W_x\cap\ker L)\ge k_x-r.
\]
For any complex-linear \(R_x\), including non-Hermitian matrices, of rank below \(k_x\), choose a surviving unit vector in \(W_x\cap\ker R_x\). Then
\[
\|A_x-R_x\|\ge|\langle f,A_xf\rangle|\ge\tau_x/2.
\]
Thus every fixed rank fraction \(\kappa<1/4\) is covered eventually. No success claim for larger-rank deflation follows. [GROWING_RANK_PROOF.md:200](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:200)

### 2. Optional subspace and normalized version

The predeclared
\[
m_x=\left\lfloor\frac{Q^2}{96C_0}\right\rfloor,\qquad
W_x^0=\operatorname{span}_{\mathbb C}\{f_j:0\le j<m_x\}
\]
also works. With \(N\ge Q^3/3\), \(H\ge8Q\), and eventually \(\#\mathcal Q\le2Q/\log Q\),
\[
\frac{C_0}{N}\sum_q q^2\le\frac{24C_0}{\log Q}.
\]
Multiplying by \(m_x\) bounds the positive compression trace, hence its norm, by \(\tau_x/4\). Subtracting the pointwise diagonal gives the printed \(-3\tau_x/4\) bound. [GROWING_RANK_PROOF.md:220](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:220)

The normalized transfer is also correct. For \(g=D_G^{1/2}f\),
\[
\langle g,Zg\rangle=\langle f,A_xf\rangle
\le-\frac{\tau_x}{2}\|f\|^2
\le-\frac{1}{2C_GH}\|g\|^2,
\]
provided the separately proved \(0<G(u)\le C_GH\tau_x\) holds. The map preserves dimension. For example, the audited row bound permits \(C_G=4B_\kappa^2/3\) eventually, after taking \(S_Q\le2\tau_x\). This constant may depend on the inherited profile. [GROWING_RANK_PROOF.md:245](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:245), [PROOF_PACKAGE.md:119](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:119)

### 3. Uniformity, scope, and minimum clarifications

The main theorem’s conditions (13) are jointly eventual. Its constants are uniform over normalized nonnegative profiles supported on \([-1,1]\); no derivatives or evenness enter this growing-rank argument. The imported row-normalized version has its separate profile-dependent threshold.

Minor clarifications, not blockers:

- Explicitly enlarge the common threshold to include the optional prime-count bound and the imported row-energy conditions.
- At line 205, spell out the orthogonal-compression consequence: if \(P\) is an orthogonal projector with \(\operatorname{codim}\operatorname{Ran}P=r<k_x\), then the compression retains at least \(k_x-r\) negative directions.
- At line 249, prefer “the proof does not establish negativity of the entire large band; the cutoff is needed **for this argument**.” No counterexample proving that the actual whole band fails was supplied.

All ranks, dimensions, homogeneous constraints, and spectral subspaces here are over \(\mathbb C\). The cutoff subspace need not be conjugation-invariant. No real negative-subspace dimension is certified. Fourier-index prefixes are not physical-coordinate or increasing-prime prefixes; no maximal-prefix estimate follows.

### 4. Physical accounting and no-GO boundary

The seven physical fields remain intact:

- Literal coefficient \(q[1_{u\equiv t(q)}-1/(q-1)]\), both unit masks, deleted diagonal, and oriented kernel.
- Fixed \(h_0=2\).
- Full ordered \(t,u\in I_x\), \(t\ne u\), complete shell—not truncated coordinate/prime prefixes.
- \(x=2X\), exact \(N=\lfloor2X\rfloor-\lfloor X\rfloor\), \(Q=x^{1/3}\), \(H=x^{21/32}\), \(U=x^{133/400}\).
- Fixed-profile and fixed-\(K\) quantifiers; no exceptional physical rows or sufficiently large scales.
- \(G=\sum_q\sum_t|A_q(u,t)|^2\), with weighted lane costs retained.
- Natural scalar scale \(xQ^2=x^{5/3}\), required \(\delta>1/400\), benchmark \(1/96\), additional loss strictly below \(19/2400\), and downstream margin
  \[
  0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
  \]

The scalar still uses the literal Möbius lane and \(w(u)=\Lambda(u+2)-b_x^{(z)}(u)\), including the hybrid minus sign and forbidden residue \(-2\). No identification with \(W_x\) or \(D_G^{1/2}W_x\) is proved. [DERIVATION_PACKAGE.md:33](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:33)

**First fatal mismatch:** none in the scoped theorem.  
**Strongest objection to promotion:** many negative operator directions do not control the specified mixed arithmetic scalar or its alignment with those directions.  
**Closest existing inputs:** V59’s exact variance identity, audited P1, and the residue lemma underlying P7—not an existing multiplicity theorem.

Research integration is supported on island ②, image Bridge A / repository Gate B. No arithmetic advance, gate closure, numbered writer, or publication GO; TPC418 remains unchanged.

### 5. Preservation receipt

All shell commands exited **0**: bounded `sed -n`, `nl -ba`, and `wc -l` reads; `sha256sum`; `git --no-optional-locks rev-parse HEAD origin/main`; porcelain status with `--untracked-files=all`; and unstaged/staged name-only diffs. No tests, raw reviewer reports, writes, children, builds, synchronization, or external-model uploads were used.

Start/end HEAD and local origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Status: **10 tracked dirty / 658 untracked / empty index → unchanged**, with no added or removed status entries. Unfrozen parent-owned paths remain authorized; their contents were not claimed immutable.

All supplied control and supplemental draft hashes matched at start and end:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
round/GROWING_RANK_PROOF.md
50c477f5b525e5c813d2f6d63aa00b9579846afebc34daffeb6030b4aecfb682
round/PROOF_PACKAGE.md
177ee528709683c45bbe84e98156d27d297fd3d8fb7938f51eb68d0fd6270bab
round/DERIVATION_PACKAGE.md
51f92d89a5aa314a910f492ddd0248fd3fa0cd5b1bb9e9f0d2da3ef2cab75e5b
```

</details>

An initial clarification patch did not match a wrapped sentence and failed
without changing GROWING_RANK_PROOF.md. After reading the exact sentence,
the corrected patch succeeded. The raw audit archive was already preserved.
No required checker failed.

## Round 4 — final bounded realification audit

The parent wrote a separate real-basis trace argument. It constructs a new
real spectral-cutoff subspace rather than reinterpreting the complex one.
Jason is auditing it, reusing his exact source/core proof context. This is
the fourth and final review round under the selected auto-review-loop skill;
no further optional extension will be added to this cycle. Original controls
and the four audit targets remain frozen while the read-only audit runs.
The expanded diagnostics passed both modes; current complete output is in
DIAGNOSTIC_RECEIPT_ROUND4.md. No matrix-materialization or asymptotic claim
is inferred from the one-scale rational prerequisite check.

### Round-4 result — scoped proof accepted

Score 9.5/10; R1–R4 verified with no minimum necessary corrections. The
parent added the reviewer's important explicit boundary: equality of the
real quadratic forms does not replace the mixed two-lane arithmetic scalar
by its real-part matrix. The complex proof now links the separate real
construction without reinterpreting its own spectral subspace.

<details><summary>Round-4 real-witness reviewer — full raw response</summary>

```json
{
  "schema": "TPC_AGENT_RESULT_V1",
  "task_id": "physical-loop-independent-real-rank-audit-round4",
  "role": "tpc_proof_auditor",
  "mode": "READ_ONLY_RESEARCH_AND_AUDIT",
  "proof_verdict": "PROVABLE AS STATED",
  "integration_verdict": "READY_FOR_SCOPED_REAL_WITNESS_RESEARCH_INTEGRATION",
  "readiness_score": "9.5/10 for R1–R4; not arithmetic or publication GO",
  "first_fatal_mismatch": null,
  "minimum_necessary_corrections": [],
  "arithmetic_advance": false,
  "publication_GO": false,
  "files_changed": []
}
```

R1–R4 are correct. The addendum constructs a separate real spectral-cutoff subspace; it does not reinterpret the earlier complex subspace as real. The trace is preserved without a factor of two, the real-input rank convention is correct, and the normalized congruence retains the stated dimension and bound.

### 1. Round-3 clarifications: all implemented

The revised complex proof now explicitly:

- enlarges the common threshold for the optional prime-count estimate and imported row-energy bounds, allowing profile dependence for the latter; [GROWING_RANK_PROOF.md:225](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:225)
- states the orthogonal-compression consequence with \(\operatorname{codim}\operatorname{Ran}P=r<k_x\); [line 206](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:206)
- limits the cutoff claim to what this argument proves, without asserting a counterexample to whole-band negativity or a success threshold for larger-rank deflation. [line 259](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/GROWING_RANK_PROOF.md:259)

These are faithful scope corrections, not changes to the previously audited complex theorem.

### 2. Independent R1–R4 verification

**R1 — real basis, positivity, and trace: correct.**

Because \(d=2J+1<N\), the symmetric frequencies are distinct modulo \(N\); in particular no retained positive frequency is its own negative. The vectors
\[
v_0=f_0,\qquad c_j=(f_j+f_{-j})/\sqrt2,\qquad
s_j=(f_j-f_{-j})/(i\sqrt2)
\]
are real and orthonormal on the actual consecutive integer interval, regardless of its integer origin.

Their complex span equals the original Fourier band. Therefore
\[
V^TV=I_d,\qquad VV^T=FF^*.
\]
For \(C=V^TUV\), Hermiticity and positivity of \(U\) imply that \(C\) is Hermitian PSD. Write \(C=C_{\mathbb R}+iC_{\mathbb I}\); then \(C_{\mathbb R}\) is real symmetric and \(C_{\mathbb I}\) is real skew-symmetric. For real \(y\),
\[
y^TC_{\mathbb R}y=y^TCy=(Vy)^*U(Vy)\ge0.
\]
Moreover, Hermitian diagonal entries are real, so
\[
\operatorname{tr}C_{\mathbb R}
=\operatorname{tr}C
=\operatorname{tr}(UVV^T)
=\operatorname{tr}(F^*UF).
\]

This is a \(d\)-dimensional change of band coordinates followed by entrywise real part—not the \(2d\)-dimensional block realification of a complex matrix. **There is no factor of two.** [REAL_GROWING_RANK_ADDENDUM.md:12](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/REAL_GROWING_RANK_ADDENDUM.md:12)

**R2 — real cutoff and negative dimension: correct.**

The imported bounds are
\[
\operatorname{tr}(F^*UF)\le C_0(1+2Q/N)M_1,\qquad
\Delta(n)\ge D_*\ge\tau_x,
\]
with
\[
C_0=(\pi+1)^2,\qquad
\tau_x=Q^2/\log Q,\qquad
2\operatorname{tr}(F^*UF)<35D_*.
\]
The trace identity therefore bounds the number of eigenvalues of \(C_{\mathbb R}\) above \(D_*/2\) by a quantity strictly below \(35\). The integer count is at most \(34\); discarding \(35\) dimensions is conservative.

Consequently,
\[
\dim_{\mathbb R}W_{\mathbb R}\ge k_x=d_x-35,
\]
and for real \(f=Vy\) in this separately constructed subspace,
\[
f^TAf=f^T(\operatorname{Re}A)f
\le(D_*/2-D_*)\|f\|^2
\le-\tau_x\|f\|^2/2.
\]
The imaginary skew-symmetric part contributes zero only because the same real vector occupies both slots.

Real symmetric min–max now gives at least \(k_x\) eigenvalues of \(\operatorname{Re}A\) at most \(-\tau_x/2\), with
\[
k_x=\frac{Q^2}{4}-x^{11/32}+O(1)\sim Q^2/4.
\]
Neither \(A\) nor the original complex cutoff subspace is thereby declared real. [REAL_GROWING_RANK_ADDENDUM.md:46](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/REAL_GROWING_RANK_ADDENDUM.md:46)

**R3 — real constraints, deflation, and normalization: correct.**

For a real-linear map \(L\), rank-nullity gives
\[
\dim_{\mathbb R}(W_{\mathbb R}\cap\ker L)
\ge k_x-\operatorname{rank}_{\mathbb R}L.
\]
For \(R:\mathbb R^N\to\mathbb C^N\) of real rank below \(k_x\), a surviving real unit vector satisfies \(Rf=0\). Cauchy–Schwarz then gives
\[
\|A-R\|_{\mathbb R^N\to\mathbb C^N}
\ge\|(A-R)f\|
\ge|f^*(A-R)f|
=|f^TAf|
\ge\tau_x/2.
\]

The distinction from complex rank is essential and correctly stated. For a complex matrix \(M\) restricted to real inputs, the relevant rank is
\[
\operatorname{rank}_{\mathbb R}
\begin{pmatrix}\operatorname{Re}M\\ \operatorname{Im}M\end{pmatrix},
\]
not automatically \(\operatorname{rank}_{\mathbb C}M\), nor automatically twice it. The earlier complex theorem separately uses complex rank and the norm on complex inputs. [REAL_GROWING_RANK_ADDENDUM.md:72](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/REAL_GROWING_RANK_ADDENDUM.md:72)

For the imported positive real weights \(G(n)\le C_GH\tau_x\), put \(g=D_G^{1/2}f\). This map is real, invertible, and dimension-preserving, and
\[
g^TZg=f^TAf
\le-\frac{\tau_x}{2}\|f\|^2
\le-\frac{1}{2C_GH}\|g\|^2.
\]
Thus the normalized claim has the correct direction and constant. Its threshold and \(C_G\) retain the imported profile dependence. [line 96](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/REAL_GROWING_RANK_ADDENDUM.md:96)

**R4 — physical scope: correct.**

The argument adds no evenness or smoothness requirement. The unnormalized real construction inherits the uniform trace and pointwise-diagonal bounds; it introduces no exceptional rows or additional spectral threshold loss. It makes no physical-prefix or arithmetic-lane identification. [REAL_GROWING_RANK_ADDENDUM.md:101](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/REAL_GROWING_RANK_ADDENDUM.md:101)

### 3. Physical contract and no-GO boundary

The audited source object remains
\[
A_q(u,t)=qK_H(u-t)
\left(1_{u\equiv t\pmod q}-\frac1{q-1}\right)
1_{q\nmid u}1_{q\nmid t}1_{u\ne t}.
\]
This retains the literal outer \(q\), negative centering, both unit masks, kernel orientation, and deleted diagonal. [TPC247 main.tex:70](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70)

The remaining physical fields are unchanged:

- \(h_0=2\), not \(H\), conductor, or \(u-t\).
- \(x=2X\), \(I=(X,2X]\cap\mathbb Z\), \(N=\lfloor2X\rfloor-\lfloor X\rfloor\).
- \(Q=x^{1/3}\), \(H=x^{21/32}\), \(U=x^{133/400}\), complete prime shell \(Q<q\le2Q\).
- Literal \(\beta(t)=\Lambda(t)/\log t-\sum_{d\mid t,\ d\le U}\mu(d)\) and \(w(u)=\Lambda(u+2)-b_x^{(z)}(u)\), retaining the hybrid minus sign, prime \(2\), and forbidden residue \(-2\).
- Requested saving parameters precede fixed \(K\), which precedes the large-\(x\) threshold. The real argument is uniform over the inherited normalized nonnegative compact-profile class; normalized row bounds retain their separate profile constants.
- The full ordered off-diagonal pair domain is retained. Increasing-coordinate prefixes and increasing-prime prefixes \(Q<q\le Y\) are not certified by a Fourier-band construction.
- \(G=\sum_q\sum_t|A_q(u,t)|^2\), with both weighted arithmetic lanes still required.

The natural scalar scale remains \(xQ^2=x^{5/3}\). Division by \(K_*=x^{2/3+o(1)}\), physical error exponent \(79/96\), separate Gate A, and
\[
\delta>1/400,\qquad
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}
\]
remain required. At benchmark \(1/96\), additional loss must be strictly below \(19/2400\). [DERIVATION_PACKAGE.md:174](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/DERIVATION_PACKAGE.md:174)

**First fatal mismatch:** none.  
**Minimum necessary fixes:** none.  
**Strongest limitation:** real negative directions do not identify either arithmetic lane with the constructed subspace. In particular, \(f^TAf=f^T\operatorname{Re}(A)f\) for real \(f\) does **not** justify replacing \(w^TA\beta\) by \(w^T\operatorname{Re}(A)\beta\) for different real lanes.  
**Closest existing input:** the separately audited symmetric-band trace theorem and V59’s exact variance-minus-diagonal identity. R1–R4 are an elementary real-coordinate consequence, not a novelty certification.

The scoped real-witness result is ready for research integration. Island ② / image Bridge A / Gate B; TPC418 unchanged. No arithmetic advance, gate closure, numbered writer, or publication GO.

### 4. Preservation and commands

All shell commands exited **0**: bounded `sed -n`, `nl -ba`, and `wc -l` reads; `sha256sum`; and:

```text
git --no-optional-locks rev-parse HEAD origin/main
git --no-optional-locks status --porcelain=v1 --untracked-files=all
git --no-optional-locks diff --name-only
git --no-optional-locks diff --cached --name-only
```

No tests, diagnostics, raw reviews, external-model uploads, writes, children, builds, or synchronization were used.

Start/end HEAD and local origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Status: **10 tracked dirty / 660 untracked / empty index → 10 / 661 / empty index**. The sole added entry was the parent-authorized round file `DIAGNOSTIC_RECEIPT_ROUND4.md`; it was not read. No entries disappeared.

All four controls and all four frozen drafts matched their supplied hashes at start and end:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
round/GROWING_RANK_PROOF.md
9801b2bec27a8059666a1ccd14d1b5aa86835a5e9c092bf58bf5f71c849a9ebb
round/REAL_GROWING_RANK_ADDENDUM.md
617b91ec51ddc5992ccd10ea446901d53e49cc31504ad91bfe5c595733a0e923
round/PROOF_PACKAGE.md
177ee528709683c45bbe84e98156d27d297fd3d8fb7938f51eb68d0fd6270bab
round/DERIVATION_PACKAGE.md
51f92d89a5aa314a910f492ddd0248fd3fa0cd5b1bb9e9f0d2da3ef2cab75e5b
```

</details>

### Final integration and QA boundary

All nine delegated agents are closed; six initial reports, one growing-rank
report, and eight independent round-review responses are preserved verbatim.
No further optional extension was added after the fourth review. The loop
has positive scoped assessments but no arithmetic or publication GO.

The parent updated only the new handoff prefix after all agents closed.
Reconstructing the original header and entire older body reproduces its
starting SHA-256 36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a.
All four locked controls matched their original hashes immediately before
this authorized handoff update. The existing startup wrapper is being rerun
in both modes because the handoff was changed; no historical writer was run.

A naive local-link regex check exited 1: TeX function notation was misparsed,
one valid target had surrounding whitespace, and one immutable raw report
contained a genuine missing directory prefix. The parser was corrected to
exclude math/code and trim targets. SOURCE_LINK_ERRATA.md supplies the correct
existing destination without rewriting raw text. The corrected check exited
0 with 195 local targets checked, no unresolved missing target, and exactly
one explicit preserved-raw erratum. This was a navigation check, not a
failed mathematical theorem or a weakened scientific checker.

## Final state — completed scoped research, no arithmetic GO

The four-round review cycle is complete with positive scoped assessments
(9/10 initially; final complex and real growing-rank audits 9.5/10). All
minimum corrections are implemented and all nine agents are closed. The
actual signed arithmetic saving and publication novelty remain unproved;
no reviewer score is substituted for these gates.

The post-handoff startup suite passed both wrapper modes, covering eight
distinct command/mode forms via fourteen total processes. Current new
diagnostics passed normal and optimized modes with identical output. The
tracked whitespace check passed, the published TPC417/418 sources and wrapper
match HEAD, the index is empty, and the old handoff body is hash-identical.
The final record is [FINAL_QA_RECEIPT.md](research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/FINAL_QA_RECEIPT.md).

Final file scope: 33 new files (two root review files and this new research
round), plus the authorized prefix of the already-dirty TPC_HANDOFF.md.
The starting 10 dirty tracked paths persist; untracked count is 631→664,
with no removed entry or unexplained addition. There was no commit, push,
numbered writer, new PDF or scientific expected-artifact rewrite.
The next admissible mathematical trigger is the precise signed-interior or
paid two-sided coefficient-sensitive theorem recorded in the new handoff;
more generic norm repairs are STOP_SCOPED, not a global impossibility claim.
