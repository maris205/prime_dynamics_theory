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
