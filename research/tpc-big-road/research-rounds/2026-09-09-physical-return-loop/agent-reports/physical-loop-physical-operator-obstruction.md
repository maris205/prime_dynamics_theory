# TPC_AGENT_RESULT_V1

`task_id`: `physical-loop-physical-operator-obstruction`  
`role`: `tpc_source_lock`  
`mode`: `READ_ONLY_RESEARCH_AND_AUDIT`  
`files_changed`: `[]`  
`proof_verdict`: **PROVABLE under the explicitly fixed, normalized Schwartz-kernel assumption.**

The constant vector proves
\[
\boxed{\|A_x\|\ge \left(\frac32+o(1)\right)\frac{Q^2}{\log Q}.}
\]
This is an obstruction to coefficient-blind fixed-power saving for the literal operator—not a lower bound for the physical \(\langle w,A_x\beta\rangle\).

## 1. Source lock and precise claim

The literal matrix is
\[
A_x(u,t)=\mathbf1_{u\ne t}\sum_{Q<q\le2Q\atop q\ {\rm prime}}
q\,\mathbf1_{q\nmid u}\mathbf1_{q\nmid t}
K_H(u-t)\left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right).
\]
This retains both unit masks, outer \(q\), negative centering, kernel orientation, and deleted diagonal. Source: [TPC247, main.tex:70](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70).

The physical fields are
\[
I_x=(x/2,x]\cap\mathbb Z,\quad N=|I_x|,\quad
Q=x^{1/3},\quad H=x^{21/32},
\]
\[
K_H(h)=\widehat\psi_+(h/H),\qquad
\widehat\psi_+(y)=\int\psi_+(v)e(-vy)\,dv,\qquad \int\psi_+=1,
\]
\[
\beta(t)=\frac{\Lambda(t)}{\log t}
-\sum_{d\mid t,\ d^{400}\le x^{133}}\mu(d),\qquad
w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
Here the fixed physical shift is \(h_0=2\); it is neither \(H\), the conductor, nor the difference \(u-t\). The ambient endpoint is \(X=x\); \(N\) here denotes the exact coordinate count. Source: [V59:36](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:36).

**Kernel assumption:** one fixed kernel profile, independent of \(x,q\), with
\[
M_0=\int|\psi_+(v)|\,dv<\infty,\qquad
M_5=\int |v|^5|\psi_+(v)|\,dv<\infty.
\]
A fixed normalized Hermitian Schwartz profile satisfies this through Fourier inversion. Positivity of \(\psi_+\) is unnecessary. The sources expressly invoke Schwartz behavior: [V52:248](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md:248), [V59:306](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:306).

The theorem concerns the complete physical interval and complete prime shell. It makes no adaptive-prefix or exceptional-set assertion. The proof’s constants are uniform in the interval’s integer origin.

## 2. Derived proof: the constant-vector witness

**Dependency chain:** exact residue variance → incomplete-interval geometric-sum bound → fixed Fourier-tail bound → diagonal subtraction → Rayleigh-quotient lower bound.

Let \(f=N^{-1/2}\mathbf1_{I_x}\). For each unit residue \(r\), define
\[
S_r(\alpha)=\sum_{n\in I_x,\ n\equiv r\pmod q}e(\alpha n),\qquad
V_q(\alpha)=\sum_{r\ne0}|S_r(\alpha)-\overline S^\times(\alpha)|^2.
\]
Direct expansion, with the diagonal deleted only after expansion, gives
\[
\langle f,A_xf\rangle
=\frac1N\sum_q q\int\psi_+(v)V_q(v/H)\,dv-D_x,
\]
where
\[
D_x=\frac1N\sum_q\frac{q(q-2)}{q-1}N_q,\qquad
N_q=\#\{n\in I_x:q\nmid n\}.
\]
This is exactly the source’s variance-minus-diagonal identity, not a restored-diagonal replacement: [V59:226](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:226). The nonprincipal-character multiplicity is \(q-2\), consistent with [NIST’s character orthogonality](https://dlmf.nist.gov/27.8).

**Step 1: control the undeleted variance, including incomplete intervals.**

Write an arbitrary interval as \(a+1,\ldots,a+N\), with \(N=mq+s\), \(0\le s<q\). Its residue sums, labeled by \(1\le j\le q\), are
\[
S_j(\alpha)=e(\alpha(a+j))
\left(G_m(\alpha q)+\mathbf1_{j\le s}e(\alpha mq)\right),
\quad
G_m(z)=\sum_{k=0}^{m-1}e(kz).
\]
For \(0<|\alpha|q\le1/2\),
\[
|G_m(\alpha q)|\le\frac1{2|\alpha|q},\qquad
|e(\alpha j)-1|\le2\pi|\alpha|q.
\]
Consequently every residue sum is within \(\pi+1\) of the same number \(e(\alpha a)G_m(\alpha q)\). At \(\alpha=0\), the corresponding bound is \(1\).

Discarding the actual nonunit residue and using the minimizing property of the unit-residue mean yields
\[
V_q(\alpha)\le q(\pi+1)^2
\quad (|\alpha|q\le1/2).
\]
For every \(\alpha\), independently,
\[
V_q(\alpha)\le q(N/q+1)^2.
\]
No translation changes which residue is excluded.

**Step 2: integrate the fixed kernel.**

For \(N\ge2Q,\ H\ge4Q\), split at \(|v|=H/(2q)\). Since
\[
\int_{|v|>H/(2q)}|\psi_+(v)|\,dv
\le M_5(2q/H)^5,
\]
the undeleted term \(R_x\) satisfies
\[
|R_x|
\ll_\psi
\frac{Q^3}{N\log Q}
+\frac{NQ}{\log Q}\left(\frac QH\right)^5.
\]
This estimate uses absolute values only to bound the error; it does not require positive kernel energy.

**Step 3: subtract the exact diagonal.**

Counting multiples in an interval gives
\[
N_q=N(1-1/q)+O(1).
\]
Therefore
\[
D_x=\sum_q(q-2)+O\!\left(\frac{Q^2}{N\log Q}\right).
\]
Combining the preceding estimates,
\[
\boxed{
\langle f,A_xf\rangle
=-\sum_q(q-2)
+O_\psi\!\left(
\frac{Q^3}{N\log Q}
+\frac{NQ}{\log Q}(Q/H)^5
\right).}
\]

At the frozen physical scales,
\[
Q^3/N\asymp1,\qquad NQ(Q/H)^5\asymp x^{-9/32},
\]
so
\[
\boxed{\langle f,A_xf\rangle
=-\sum_q(q-2)+O_\psi(1/\log Q).}
\]
Thus the suggested \(O(H^2Q/(x\log Q))\) error is unnecessary; the geometric-sum argument is substantially sharper.

Partial summation of the [prime number theorem](https://dlmf.nist.gov/27.2.E3) gives
\[
\sum_{Q<q\le2Q}(q-2)
=\left(\frac32+o(1)\right)\frac{Q^2}{\log Q}.
\]
Finally, \(\|A_x\|\ge|\langle f,A_xf\rangle|\), proving the claim. Hermiticity is not needed for this last inequality.

## 3. Objections, normalization, and no-GO boundary

**First fatal mismatch for coefficient-blind saving:** any proposed
\[
\|A_x\|\ll Q^2x^{-\delta+o(1)},\qquad \delta>0,
\]
contradicts this witness. There is no operator-identification mismatch in the proof above.

**Strongest assumption objection:** “Schwartz for each \(x\)” is insufficient without fixedness or uniform seminorms. For example, the varying normalized family
\[
\psi_x(v)=H^{-2}e^{-\pi(v/H^2)^2}
\]
produces \(K_H(h)=e^{-\pi H^2h^2}\), making the off-diagonal operator exponentially small. The fixed-kernel hypothesis genuinely matters.

**Conditional normalization consequence:** if the parent independently establishes a positive diagonal \(G_x\) with
\[
G_x(u)\le C H Q^2/\log Q,
\]
then, testing \(Z_x=G_x^{-1/2}A_xG_x^{-1/2}\) on \(G_x^{1/2}\mathbf1\),
\[
\|Z_x\|\ge
\frac{|\langle\mathbf1,A_x\mathbf1\rangle|}
{\langle\mathbf1,G_x\mathbf1\rangle}
\gtrsim_\psi H^{-1}.
\]
This uses the parent’s comparison conditionally; I have not duplicated or certified its proof.

**Closest checked existing result:** V59’s exact variance-minus-diagonal identity above and its coefficient-blind obstruction warning at [V59:520](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:520). TPC247’s external-copy obstruction is a different structural norm obstruction. No novelty claim is made.

**Physical budget:** the natural scalar scale remains \(xQ^2=x^{5/3}\). The required numerator saving remains \(\delta>1/400\), with benchmark \(\delta=1/96\), numerator \(x^{53/32+o(1)}\), output \(x^{95/96+o(1)}\), and margin \(19/2400\). The downstream margin also retains
\[
\min(\eta_A,\delta-1/400,419/2400).
\]
Sources: [V59:79](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:79), [V59:386](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:386).

This result earns **zero physical cancellation credit**. Location: island ②, image Bridge A / repository Gate B. Gate A, Gate B, and dynamics/C remain open; endpoint TPC418 unchanged; no GO or numbered writer.

## 4. Diagnostics and preservation receipt

Floating-point diagnostics only:

- Gaussian fixed kernel at \(x=1000,10000,100000\): undeleted normalized remainders \(0.297402,0.234880,0.158453\), versus negative diagonals approximately \(-52,-192,-662\).
- Direct residue summation checked 450 configurations; largest \(V_q/q=0.55\), below \((\pi+1)^2\). These checks are not asymptotic evidence.

All shell commands exited **0**: `pwd`; required `cat`/`sed` reads; bounded `nl -ba`/`rg -n` source reads; `wc -l`; `sha256sum`; `git rev-parse HEAD origin/main`; `git status --porcelain=v1 --untracked-files=all`; `git diff --name-only`; `git diff --cached --name-only`. Subsequent Git reads used `GIT_OPTIONAL_LOCKS=0`. Both in-memory diagnostic executions completed successfully. No builds, regeneration, downloads, synchronization, children, or external-model uploads occurred.

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

All three mathematical-source SHA256 hashes also remained unchanged. Status changed from **10 tracked-dirty / 631 untracked / empty index** to **10 / 633 / empty index**. The only added status entries were `AUTO_REVIEW.md` and `REVIEW_STATE.json`: **authorized parent changes**, not unexplained drift.
