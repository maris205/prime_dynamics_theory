# TPC_AGENT_RESULT_V1

`task_id`: `physical-loop-growing-rank-obstruction`  
`role`: `tpc_source_lock`  
`mode`: `READ_ONLY_RESEARCH_AND_AUDIT`  
`files_changed`: `[]`  
`proof_verdict`: **PROVABLE under the recovered source premises**  
`independent_growing_rank_audit`: **PENDING**

This is the complete consolidated result. **All vector spaces, dimensions, ranks, constraints, and deflations below are over \(\mathbb C\).** No complex bad vector is identified with the actual real arithmetic lanes.

## 1. Source-locked theorem

The corrected physical clock is
\[
\boxed{x=2X,\quad I_x=(X,2X]\cap\mathbb Z,\quad
N=\lfloor2X\rfloor-\lfloor X\rfloor.}
\]
Earlier statements \(X=x\) are superseded. Source: [literal emitter:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md:43).

Set
\[
Q=x^{1/3},\qquad H=x^{21/32},\qquad
\mathcal Q=\{q\text{ prime}:Q<q\le2Q\}.
\]
Let \(\psi_+\) be the fixed inherited real nonnegative profile, supported on \([-1,1]\), with integral \(1\), and
\[
K_H(h)=\int_{\mathbb R}\psi_+(v)e(-vh/H)\,dv,
\qquad e(t)=\exp(2\pi it).
\]
The profile identification uses the original positive-exponent convention and reflection: [V23:189](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_prime_shell_jutila_and_stable_dynamics.md:189), [V25:87](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_corrected_fourier_factorable_emitter.md:87), [V36:122](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_multiroute_ratio_core_atlas.md:122). No evenness is assumed.

On \(\mathcal H_x=\ell^2(I_x;\mathbb C)\), retain the exact matrix
\[
A_x(u,t)=\mathbf1_{u\ne t}\sum_{q\in\mathcal Q}
q\,\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}K_H(u-t)
\left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right).
\tag{1}
\]
It is Hermitian, possibly complex. This retains both unit masks, outer \(q\), centering sign, orientation, and deleted diagonal. Source: [TPC247 main.tex:70](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70).

Define the exact constants and integers
\[
C_0=(\pi+1)^2,\qquad \boxed{\tau_x=\frac{Q^2}{\log Q}},
\]
\[
J_x=\left\lfloor N\left(\frac1{4Q}-\frac1H\right)\right\rfloor,
\qquad d_x=2J_x+1,\qquad \boxed{k_x=d_x-35}.
\tag{2}
\]

**Theorem.** For every sufficiently large \(x\), there is an explicitly constructed complex subspace \(W_x\) such that
\[
\boxed{\dim_{\mathbb C}W_x\ge k_x,\qquad
\langle f,A_xf\rangle\le-\frac{\tau_x}{2}\|f\|^2
\quad(f\in W_x).}
\tag{3}
\]
Consequently:

- \(A_x\) has at least \(k_x\) eigenvalues at most \(-\tau_x/2\).
- Every complex-linear constraint map of rank \(r<k_x\) leaves a negative subspace of dimension at least \(k_x-r\).
- Every complex-linear matrix \(R_x\), not necessarily Hermitian, with \(\operatorname{rank}_{\mathbb C}R_x<k_x\), satisfies
  \[
  \boxed{\|A_x-R_x\|\ge\tau_x/2.}
  \tag{4}
  \]

Moreover,
\[
k_x=\frac{Q^2}{4}-x^{11/32}+O(1)
=\left(\frac14+o(1)\right)Q^2.
\tag{5}
\]
Thus (4) holds eventually for \(r\le\kappa Q^2\), for every fixed \(\kappa<1/4\).

## 2. Proof

The dependencies are the exact positive undeleted form from audited P1 and the residue lemma underlying audited P7. **P7’s one-vector lower bound alone does not imply multiplicity.** The shifted-band, pointwise-diagonal, trace-cutoff, and rank arguments below supply that implication.

### Step 1: positive form and unnormalized variance

Put
\[
d_q=\frac{q(q-2)}{q-1},\quad
\Delta_x(n)=\sum_qd_q\mathbf1_{q\nmid n},\quad
U_x=A_x+\operatorname{diag}\Delta_x.
\]
For a vector \(f\), let
\[
T_{q,r}[f](v)=\sum_{\substack{n\in I_x\\n\equiv r\pmod q}}
f(n)e(vn/H),
\]
\[
\mathcal V_q[f](v)=
\sum_{r\ne0}\left|T_{q,r}[f](v)
-\frac1{q-1}\sum_{s\ne0}T_{q,s}[f](v)\right|^2.
\]
There is **no division by \(q-1\) outside the squared-deviation sum**. Direct expansion gives
\[
\langle f,U_xf\rangle
=\sum_q q\int\psi_+(v)\mathcal V_q[f](v)\,dv\ge0.
\tag{6}
\]
This is the source variance identity, consistent with [P1:9](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:9) and [V59:230](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:230).

Let \(V_q^{\rm raw}(\alpha)\) denote the same unnormalized variance for the sequence \(e(\alpha n)\). For
\[
f_j(n)=N^{-1/2}e(jn/N),
\]
equation (6) becomes
\[
\boxed{\langle f_j,U_xf_j\rangle
=\frac1N\sum_q q\int\psi_+(v)
V_q^{\rm raw}(j/N+v/H)\,dv.}
\tag{7}
\]
The coordinate normalization contributes exactly \(1/N\).

### Step 2: residue lemma with incomplete cycles

Write \(I_x=\{a+1,\ldots,a+N\}\), \(N=\ell q+s\), \(0\le s<q\). Label residues by representatives \(a+b\), \(1\le b\le q\). Their exponential sums equal
\[
e(\alpha(a+b))
\left(G_\ell(\alpha q)+\mathbf1_{b\le s}e(\alpha\ell q)\right),
\quad
G_\ell(y)=\sum_{t=0}^{\ell-1}e(ty).
\]
For \(0<|\alpha|q\le1/2\),
\[
|G_\ell(\alpha q)|\le(2|\alpha|q)^{-1},
\qquad |e(\alpha b)-1|\le2\pi|\alpha|q.
\]
Every residue sum is therefore within \(\pi+1\) of the common value
\(e(\alpha a)G_\ell(\alpha q)\). At \(\alpha=0\), every count is within \(1\) of \(\ell\).

The excluded nonunit label depends on \(a\); the bound holds for every label. Restricting to the actual unit subset and minimizing squared distance over the common center proves
\[
V_q^{\rm raw}(\alpha)\le C_0q
\qquad(|\alpha|q\le1/2).
\tag{8}
\]
This is the proof-level P7 input, with the residue relabel made explicit; see [PROOF_PACKAGE.md:149](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-physical-return-loop/PROOF_PACKAGE.md:149).

### Step 3: shifted band and trace

Let \(F_x\) have columns \(f_j\), \(-J_x\le j\le J_x\). Eventually \(d_x<N\), so these consecutive Fourier frequencies are distinct modulo \(N\), and the columns are exactly orthonormal.

For every retained \(j\), \(v\in[-1,1]\), and \(q\le2Q\),
\[
q|j/N+v/H|\le2Q(J_x/N+1/H)\le1/2.
\]
Thus (8) covers the entire integral, without tails:
\[
\langle f_j,U_xf_j\rangle\le\frac{C_0}{N}\sum_q q^2.
\]
The compressed matrix \(B_x=F_x^*U_xF_x\) is positive semidefinite. Writing \(M_1=\sum_q q\),
\[
\operatorname{tr}B_x
\le\frac{d_xC_0}{N}\sum_q q^2
\le C_0(1+2Q/N)M_1,
\tag{9}
\]
using \(q^2\le2Qq\) and \(d_x/N\le1/(2Q)+1/N\).

### Step 4: pointwise deleted diagonal

At most two distinct primes greater than \(Q\) divide any \(n\le x=Q^3\). Consequently
\[
\Delta_x(n)\ge D_*(x):=\sum_qd_q-4Q
\quad(n\in I_x).
\tag{10}
\]
Since \(d_q=q-1-1/(q-1)\), the prime number theorem and partial summation give
\[
D_*(x)\sim M_1\sim\frac32\tau_x.
\tag{11}
\]
The primary input is [Selberg, *An Elementary Proof of the Prime-Number Theorem*, p. 305, (1.1)](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf); the weighted dyadic consequences are derived by partial summation.

### Step 5: construction and rank conclusion

The number of eigenvalues of \(B_x\) exceeding \(D_*(x)/2\) is bounded by
\[
\frac{2\operatorname{tr}B_x}{D_*(x)}
\le2C_0(1+o(1))<35.
\]
Define
\[
\boxed{W_x=
F_x\operatorname{Ran}\mathbf1_{[0,D_*(x)/2]}(B_x).}
\tag{12}
\]
Allowing the conservative loss of \(35\) dimensions gives \(\dim W_x\ge k_x\). For \(f\in W_x\),
\[
\langle f,A_xf\rangle
\le\frac{D_*}{2}\|f\|^2-D_*\|f\|^2
\le-\frac{\tau_x}{2}\|f\|^2
\]
eventually. This proves (3), and \(N=x/2+O(1)\) proves (5).

Hermitian min–max gives the eigenvalue count. For a complex-linear map \(L\) of rank \(r\),
\[
\dim(W_x\cap\ker L)\ge k_x-r.
\]
Taking \(L=R_x\), a surviving unit vector satisfies \(R_xf=0\), and
\(\|A_x-R_x\|\ge|\langle f,A_xf\rangle|\). This proves (4). The same intersection argument proves the constraint and orthogonal-compression assertions. ∎

## 3. Exact uniformity and explicit Fourier-prefix version

One common threshold \(x_0\) suffices once, for every \(x\ge x_0\),
\[
Q\ge3,\quad H\ge8Q,\quad N\ge Q^3/3,\quad36\le d_x<N,
\]
\[
D_*(x)\ge\tau_x,\qquad
2C_0(1+2Q/N)M_1<35D_*(x).
\tag{13}
\]
These conditions are eventual by (11) and \(2(\pi+1)^2<35\). There are no exceptional rows, primes, or scales. No numerical value of \(x_0\) is claimed.

For a completely predeclared subspace, without a spectral cutoff, set
\[
m_x=\left\lfloor\frac{Q^2}{96(\pi+1)^2}\right\rfloor,\qquad
W_x^0=\operatorname{span}_{\mathbb C}\{f_j:0\le j<m_x\}.
\]
Eventually \(m_x\le N/(8Q)\) and \(\#\mathcal Q\le2Q/\log Q\). Equations (7)–(8) bound each mode’s energy by \(24C_0/\log Q\). The positive compression norm is at most its trace, hence at most \(\tau_x/4\). Therefore
\[
\boxed{\langle f,A_xf\rangle\le-\tfrac34\tau_x\|f\|^2
\quad(f\in W_x^0).}
\]
All constants above are uniform over normalized nonnegative profiles supported on \([-1,1]\).

## 4. Scope, remaining gap, and physical accounting

The large Fourier band is conjugation-invariant, but its spectral-cutoff subspace need not be. **No real negative-subspace dimension or real-only growing-rank theorem is claimed.** The original constant-mode witness is real, so its previously established norm barrier is unaffected.

The actual lanes remain
\[
\beta(t)=\Lambda(t)/\log t-\sum_{d\mid t,\ d\le x^{133/400}}\mu(d),
\qquad w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
The fixed physical shift is \(h_0=2\), not \(H\), \(q\), or \(u-t\). With \(z=(\log x)^K\), the requested input order precedes the choice of fixed \(K\), which precedes the physical threshold. No universal \(K\) for all saving orders is asserted.

The full physical pair domain and complete prime shell remain intact. Fourier-index prefixes are not physical-coordinate or prime prefixes. No maximal-prefix claim follows.

Importing the parent’s separate bound \(0<G(u)\le C_GH\tau_x\), where
\(G(u)=\sum_q\sum_t|A_q(u,t)|^2\), transfers (12) to \(D_G^{1/2}W_x\) for \(Z=D_G^{-1/2}A_xD_G^{-1/2}\), with negative bound \(1/(2C_GH)\). This import does not identify either weighted arithmetic lane with that subspace.

**First fatal mismatch:** none found under the stated premises.  
**Strongest limitation:** the entire large band need not be negative; the cutoff is essential, and no success threshold for larger-rank deflation is proved.  
**Remaining mathematical gap:** none identified in this scoped complex-operator proof; independent growing-rank audit remains pending.  
**Closest existing input:** audited P1 and the residue lemma underlying P7, not a pre-existing multiplicity theorem.

The natural scalar scale remains \(xQ^2=x^{5/3}\). The required \(\delta>1/400\), benchmark \(\delta=1/96\), margin \(19/2400\), and downstream bound
\[
\min(\eta_A,\delta-1/400,419/2400)
\]
remain unpaid. Sources: [V59:79](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:79), [V59:386](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:386).

No arithmetic advance, gate closure, publication GO, numbered writer, or change to TPC418. The separately audited partition work is outside this report.

## 5. Preservation receipt

All shell commands exited **0**: skill read; bounded `nl -ba … | sed -n …` dependency reads; `sha256sum`; Git `rev-parse HEAD origin/main`, `status --porcelain=v1 --untracked-files=all`, and `diff --cached --name-only`, with `GIT_OPTIONAL_LOCKS=0`.

No writes, regeneration, builds, synchronization, children, external-model calls, or new numerical tests occurred.

Start/end HEAD and origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start/end control hashes were identical:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```

Current dependency hashes, start = end:

```text
round/PROOF_PACKAGE.md
177ee528709683c45bbe84e98156d27d297fd3d8fb7938f51eb68d0fd6270bab
round/DERIVATION_PACKAGE.md
51f92d89a5aa314a910f492ddd0248fd3fa0cd5b1bb9e9f0d2da3ef2cab75e5b
```

Status: **10 tracked-dirty / 653 untracked / empty index** at start; **10 / 654 / empty index** at the final check. The sole intervening addition was `round/DIAGNOSTIC_RECEIPT_ROUND3.md`, an authorized parent addition. Parent wording changes are reflected in the dependency hashes above; they are not agent modifications. `files_changed=[]`.
