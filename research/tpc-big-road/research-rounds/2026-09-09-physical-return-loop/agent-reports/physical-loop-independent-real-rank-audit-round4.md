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
