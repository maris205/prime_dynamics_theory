## TPC_AGENT_RESULT_V1

`task_id: physical-loop-local-emitter-obligation`  
`role: tpc_source_lock`  
`mode: READ_ONLY_RESEARCH_AND_AUDIT`  
`proof_verdict: EXACT_LOCAL_IDENTITY_PROVED; CRITICAL_LENGTH_TRANSFER_NOT_JUSTIFIED`  
`files_changed: []`

**Result:** One literal V59 polarized block pair admits an exact Kloosterman emission with conductor **\(c=q\)** and explicitly preserved coefficients. However, its arrays occupy **\(q-1\) coordinates, not \(\sqrt q\)**. Splitting them into critical-length intervals introduces a worst-case norm-reassembly factor \(\asymp\sqrt q\). Moreover, every emitted, unsubtracted quadratic packet exactly saturates its full-length norm scale. This identifies a precise missing **short-array compression of the signed, diagonal-subtracted expression**, not a missing smoothness hypothesis.

Location: island ②, image Bridge A, repository Gate B. No arithmetic advance, gate closure, numbered writer, or publication GO follows.

### 1. Source-locked physical cell

Write \(V59\) for [bridge_b_polarized_local_bdh_scalar_compiler.md](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:31). Its literal data are
\[
I_x=(x/2,x]\cap\mathbb Z,\quad
H=x^{21/32},\quad Q=x^{1/3},\quad U=x^{133/400},
\]
\[
Q<q\le2Q,\quad q\ \text{prime},\qquad
\beta(t)=\frac{\Lambda(t)}{\log t}-\sum_{\substack{d\mid t\\d\le U}}\mu(d),
\quad w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
The fixed physical shift is \(h_0=2\), not \(H\), \(q\), or \(u-t\). The hybrid remains symbolic; no \(z\)-uniform estimate is assumed.

Fix one ordered pair \((b,c)\) from V59’s original real, smooth partition, and retain all four packets
\[
a^{(j)}(t)=\eta_b(t)\beta(t)+i^j\eta_c(t)w(t),
\qquad j=0,1,2,3.
\]
Their exact signed pair reconstruction is [V59:275–304](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:275). No self-term is separately multiplied by the block count.

Ambient \(X=x\); each component block has length \(O(H)\). No block is translated. The following identities also preserve any imposed original integer-prefix indicators, but establish no maximal or adaptive-prefix estimate. V59’s target is the complete signed scalar.

### 2. Derived lemma: exact residue-to-Kloosterman emission

These formulas are **my derivation**, using finite Fourier orthogonality.

For every real \(v\), define, on \(r\in\mathbb F_q^\times\),
\[
F_r^{(j)}
=\sum_{\substack{t\in I_x\\t\equiv r\ (q)}}
a^{(j)}(t)e(vt/H),\qquad
F_r^{(j),0}=F_r^{(j)}-\frac1{q-1}\sum_{s\ne0}F_s^{(j)}.
\]

The actual arithmetic content is explicitly
\[
\begin{aligned}
F_r^{(j)}
={}&\sum_{\substack{t\in I_x\\t\equiv r(q)}}
\eta_b(t)\frac{\Lambda(t)}{\log t}e(vt/H)\\
&-\sum_{1\le d\le U}\mu(d)
 \sum_{\substack{dk\in I_x\\k\equiv r\bar d(q)}}
 \eta_b(dk)e(vdk/H)\\
&+i^j\sum_{\substack{u\in I_x\\u\equiv r(q)}}
 \eta_c(u)\bigl[\Lambda(u+2)-b_x^{(z)}(u)\bigr]e(vu/H).
\end{aligned}
\]
Here \(d<q\), hence \(\bar d\) exists; the inner \(k\)-support has length \(O(H/d)\). This expansion retains the prime-power contribution, every Möbius sign, and the hybrid subtraction **inside the same array**.

For \(1\le m,n\le q-1\), put
\[
\alpha_m^{(j)}
=\frac1q\sum_{r\ne0}F_r^{(j),0}e_q(-mr),\qquad
\gamma_n^{(j)}
=\frac1q\sum_{r\ne0}\overline{F_r^{(j),0}}e_q(-n\bar r).
\]
With the unnormalized convention
\[
S(m,n;q)=\sum_{r\ne0}e_q(mr+n\bar r),
\]
one has
\[
\boxed{\mathcal B_j:=
\sum_{m,n=1}^{q-1}\alpha_m^{(j)}\gamma_n^{(j)}S(m,n;q)
=\sum_{r\ne0}|F_r^{(j),0}|^2.}
\]

**Proof.** Extend the centered vector by zero at residue zero. Both zero-frequency coefficients vanish. Fourier inversion gives
\[
\sum_{m=0}^{q-1}\alpha_m^{(j)}e_q(mr)=F_r^{(j),0},
\quad
\sum_{n=0}^{q-1}\gamma_n^{(j)}e_q(n\bar r)
=\overline{F_r^{(j),0}}.
\]
Open \(S\), interchange finite sums, and multiply these identities. Each unit \(r\) occurs once. ∎

Define the mandatory diagonal
\[
d_j(q)=\frac{q-2}{q-1}
\sum_{\substack{t\in I_x\\q\nmid t}}|a^{(j)}(t)|^2.
\]
Then the **literal block-pair contribution**, including outer \(q\), is
\[
\boxed{
C_{bc}=\sum_{q\in\mathcal Q}q
\int_{\mathbb R}\psi_+(v)\,
\frac14\sum_{j=0}^3 i^j\bigl[\mathcal B_j-d_j(q)\bigr]\,dv.}
\]
The orientation is exact:
\(e(v(t-u)/H)\) integrates to \(K_H(u-t)\). The coefficient diagonal cancels with multiplicity \((q-2)/(q-1)\), as required by [V59:237–259](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:237).

### 3. First fatal mismatch and quantitative obstruction

**First fatal mismatch:** this emitter has \(c=q\), BP multiplier \(a=1\), and **\(N=q-1\)**. It does not have critical length \(N\asymp\sqrt q\).

BP Theorem 1.1 accepts arbitrary complex arrays on integer intervals, with the indicated gcd restriction; smoothness is unnecessary. At critical length its bound is
\[
|\mathcal B|\ll_\varepsilon q^{31/32+\varepsilon}
\|\alpha\|_2\|\gamma\|_2.
\]
Our nonzero indices satisfy its gcd condition. These are uniform theorem-statement quantifiers, not an independently audited proof or physical attachment. [Blomer–Pascadi, Theorem 1.1](https://arxiv.org/html/2607.24311v1#Thmtheorem1)

**Exact normalization:**
\[
\|\alpha^{(j)}\|_2^2=\|\gamma^{(j)}\|_2^2
=\frac1q\|F^{(j),0}\|_2^2,
\qquad
\boxed{\mathcal B_j=q\|\alpha^{(j)}\|_2\|\gamma^{(j)}\|_2.}
\]
Thus the full unsubtracted emitted packet saturates its norm scale whenever nonzero. A uniform power saving for that full form is impossible. This does **not** disprove saving after the physical diagonal subtraction and signed \(j\)-sum.

If the two component supports lie in intervals containing \(\ell_b,\ell_c\) integers, their residue aggregation multiplicity satisfies
\[
M_{bc,q}\le
\left\lceil\frac{\ell_b}{q}\right\rceil+
\left\lceil\frac{\ell_c}{q}\right\rceil
=O(1+H/q),
\quad
\|\alpha^{(j)}\|_2^2\le\frac{M_{bc,q}}q\|a^{(j)}\|_2^2.
\]
No arithmetic cancellation enters this bound.

Partition \(1,\ldots,q-1\) into
\[
L=\lfloor\sqrt q\rfloor,\qquad
K=\lceil(q-1)/L\rceil
\]
intervals. There are exactly \(K^2\) ordered BP rectangles. Their triangle/Cauchy norm budget is
\[
\sum_{A,B}\|\alpha_A\|_2\|\gamma_B\|_2
\le K\|\alpha\|_2\|\gamma\|_2.
\]
Consequently this method gives
\[
q^{31/32+o(1)}K\|\alpha\|_2\|\gamma\|_2
=q^{47/32+o(1)}\|\alpha\|_2\|\gamma\|_2,
\]
worse than the exact full-length norm scale by \(q^{15/32}\).

Full support is not a technical possibility that can simply be excluded: the centered diagnostic vector \(F=e_1-e_2\) gives
\[
\alpha_m=q^{-1}\bigl(e_q(-m)-e_q(-2m)\bigr)\ne0
\quad(1\le m<q).
\]
This is an interface counterexample, **not an assertion about physical \(w\)**.

### 4. Concrete remaining local obligation

Let
\[
E_{bcq}=\int\psi_+(v)\frac14\sum_j i^j[\mathcal B_j-d_j(q)]\,dv.
\]
A sufficient replacement for the failed splitting is an exact decomposition
\[
E_{bcq}=\sum_\nu\lambda_\nu
\mathcal B_q(A_\nu,B_\nu)+R_{bcq},
\]
with both array intervals of length at most \(L\), unchanged unit masks, and quantitative bounds
\[
\sum_\nu|\lambda_\nu|\|A_\nu\|_2\|B_\nu\|_2
\ll \omega_{bc}\frac Hq\,x^{\ell+o(1)},
\quad
|R_{bcq}|\ll
\omega_{bc}Hq^{-1/32}x^{\ell+o(1)}.
\]
Here \(\omega_{bc}=(1+|b-c|)^{-A}\), fixed \(A>2\), must survive the **integrated signed** reconstruction. This is a sufficient new obligation, not a proved or necessary condition.

Uniformly over physical blocks, primes, and the declared hybrid parameters, it would give
\[
|C|\ll xQ^2x^{-1/96+\ell+o(1)}.
\]
Hence \(\ell<19/2400\) is mandatory. Naive splitting already costs \(Q^{1/2}=x^{1/6}\).

The local/global natural scales remain \(Q^2H\) and \(xQ^2=x^{5/3}\); the endpoint still requires
\[
\delta>1/400,\qquad
0<\eta<
\min\{\eta_A,\delta-1/400,419/2400\}.
\]
Source: [V59:318–395](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:318).

**Closest existing results:** [TPC247:70–134](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70) supplies literal source-index attachment, not short-array compression; [TPC209:156–175](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-209-whole-frame-poisson-mobius-obstruction/paper/main.tex:156) supplies fixed-divisor reindexing with divisor-dependent permutations. Neither pays the displayed obligation.

### 5. Audit receipt and no-GO boundary

Formula-derivation and proof-writer discipline separated exact identities, diagnostics, and the unproved compression condition; no proof files were written.

Repository reads: required controls/guide/handoff sections; the three allowed bridge notes; bounded manuscript sections from TPC209/212/213/247; the allowed reconnaissance report.

Commands used: `pwd`, `git rev-parse HEAD origin/main`, `git status --porcelain=v1` and `--untracked-files=all`, final `git --no-optional-locks status`, `git diff --name-only`, `git diff --cached --name-only`, `sha256sum` on the four controls, scoped `rg --files`, `wc -l`, `cat`, `nl`/`sed`, and one inline `python -B -` diagnostic. **All shell invocations exited 0.** No producers, builds, repository downloads, synchronization, children, or external-model uploads ran.

Diagnostics only: 20 arbitrary-coefficient cases, five primes; maximum identity error \(2.85\times10^{-12}\). These supply no physical or asymptotic evidence.

Start/end:
```text
HEAD = origin/main = ab23455ba941e5a14ded27d49de0e874aee811ac

AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```
Tracked dirty count **10→10**; untracked **631→633**; index empty throughout. Only added status entries: authorized parent files `AUTO_REVIEW.md` and `REVIEW_STATE.json`; none removed.

**No-GO boundary:** stop this mechanism cell at the proved full-length emission and its quantified splitting obstruction. Formal endpoint remains TPC418; physical normalization and strict-power credit remain unpaid.
