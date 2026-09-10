# TPC_AGENT_RESULT_V1

task_id: `physical-loop-prefix-cover-audit`  
role: `tpc_proof_auditor`  
mode: `READ_ONLY_RESEARCH_AND_AUDIT`  
files_changed: `[]`  
verdict: **PROVABLE AS STATED, conditional on (H); counterexample VERIFIED_SCOPED. No physical GO.**

Location: islands ③/④ → ②, upstream of analytic Bridge A. Formal endpoint remains TPC418.

**First fatal mismatch:** none in the conditional covering implication. The unsupported step would be deriving (H) from exceptional logarithmic density or applying it to actual Möbius without additional arithmetic input.

## 1. Source lock and quantifiers

The audited statement is [recon-mobius-prefix.md:19](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-mobius-prefix.md:19). Write \(\theta\) for its covering parameter \(\delta\), to distinguish it from the physical power-saving exponent.

Set
\[
q=as,\quad t(z)=ad+qz,\quad
b_z=\mu(d+sz)\mu(u+az)\rho(z),\quad M=\|\rho\|_\infty,
\]
\[
A(U)=\sum_{0<t(z)\le U}b_z,\qquad
B(N)=\sum_{N<t(z)\le2N}b_z.
\]

**Source statement:** [TPC149 main.tex:220](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-149-small-polylog-determinant-two-mobius-corridor/main.tex:220) supplies absolute constants and, for each sufficiently large \(X\), one common exceptional set, before quantifying over
\[
a,s,R\in\mathbb N,\quad d,u\in\mathbb Z,\quad
(a,s)=1,\quad as\text{ odd},\quad su-ad=2,\quad
qR\le(\log X)^{\eta_0}.
\]
On its complement \(G_X\subset[\sqrt X,X]\),
\[
q|B(N)|\le\varepsilon_X MN,\qquad
\varepsilon_X=C(\log X)^{-\kappa_0},
\]
uniformly over the declared periodic multipliers.

The external source has the corresponding exceptional-set-before-modulus/residue/shift quantifiers: [Tao–Teräväinen, Theorem 3.1(ii)](https://arxiv.org/html/2512.01739v2#S3). The cited nonpretentiousness input is [Matomäki–Radziwiłł–Tao, equation (1.12)](https://arxiv.org/html/1503.05121#S1). Neither supplies (H).

The additional hypothesis is exactly
\[
0<\theta\le\tfrac14,\qquad
\sqrt X\le Y,\qquad K:=\frac{2Y}{1-\theta}\le T\le X,
\]
\[
\tag{H}
\forall v\in[Y/(1-\theta),T/2],\quad
[(1-\theta)v,v]\cap G_X\ne\varnothing.
\]
The common \(G_X\) is fixed before choosing endpoints. No measurability of the adaptive choices is needed: each endpoint requires only finitely many selections.

## 2. Independent proof, including endpoints and lattice costs

**Derivation.** The case \(M=0\) is immediate. Fix any real \(U\in[0,T]\). Starting with \(U_0=U\), while \(U_j\ge K\), choose
\[
U_{j+1}\in G_X\cap[(1-\theta)U_j/2,U_j/2].
\]
These choices are legal: \(U_j/2\) belongs to the interval in (H), and \(U_{j+1}\ge Y\ge\sqrt X\).

The half-open partition gives the exact identity
\[
A(U_j)=A(U_{j+1})+B(U_{j+1})
+\sum_{2U_{j+1}<t(z)\le U_j}b_z.
\]
A point at either boundary is counted exactly once.

Let \(m\) be the number of steps, \(u=U_m<K\), and
\[
S=\sum_{j<m}U_{j+1},\qquad
E=\sum_{j<m}(U_j-2U_{j+1}).
\]
Then
\[
U=S+E+u.
\]
Every half-open interval of length \(L\) contains at most \(L/q+1\) progression points. Consequently,
\[
\frac{q|A(U)|}{M}\le \varepsilon_XS+E+u+(m+1)q.
\]
This includes \(m=0\), empty prefixes, nonintegral endpoints, and endpoints on the lattice.

Since \(S\le T\), \(E\le2\theta T\), \(u<K\), and
\(m\le J:=\lceil\log_2(T/Y)\rceil\), the original bound follows:
\[
\frac qT\sup_{0\le U\le T}|A(U)|
\le M\left[\varepsilon_X+2\theta+\frac KT+\frac{(J+1)q}{T}\right].
\]
The denominator remains **\(T/q\), not \(U/q\)**.

**Useful loss sharpening.** For sufficiently large \(X\), \(\varepsilon_X\le1\). Since
\[
E\le\theta(2S+E),\qquad
E\le\frac{2\theta}{1+\theta}(U-u),
\]
put
\[
c=\frac{\varepsilon_X(1-\theta)+2\theta}{1+\theta}.
\]
Then \(\varepsilon_XS+E+u\le cU+(1-c)u\). Moreover,
\(U_{J-1}\le2Y<K\), so \(m+1\le J\). Thus
\[
\boxed{\frac qT\sup_{U\le T}|A(U)|
\le M\left[c+(1-c)\frac KT+\frac{Jq}{T}\right].}
\]
This improves the explicit finite loss budget; it creates no new asymptotic arithmetic input.

The closest existing result is [TPC159 main.tex:133](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-159-dyadic-shadow-prefix-lifting/main.tex:133): exact dyadic ancestors must avoid the exceptional set. The adaptive lemma instead pays for displaced edges.

## 3. Necessary local-hole test

**New derivation, not a source theorem.** For \((1-\theta)v\le N\le v\),
\[
\frac qM|B(v)-B(N)|\le3(v-N)+2q.
\]
Indeed, the two changed endpoint intervals have lengths \(v-N\) and \(2(v-N)\), each costing at most one extra lattice point.

Hence (H) necessarily implies, for every declared multiplier and every eligible \(v\),
\[
\boxed{\frac{q|B(v)|}{Mv}
\le\varepsilon_X(1-\theta)+3\theta+\frac{2q}{v}.}
\]
A violation forces the entire predecessor window to miss the good set.

**Strongest objection:** when \(\theta,\varepsilon_X,q/Y\to0\), (H) already entails uniform pointwise block cancellation on its \(v\)-range. It is a substantive arithmetic hypothesis, not merely a convenient selection consequence of global density.

## 4. Counterexample audit

The construction is [recon-mobius-prefix.md:89](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-mobius-prefix.md:89):
\[
L_j=2^{2^j}\ (j\ge1),\qquad
b(n)=1_{\bigcup_j(L_j,2L_j]}(n),\qquad
E=\bigcup_j[L_j/2,2L_j].
\]

**Independent verification.**

- Outside \(E\), every block \((N,2N]\) misses the support exactly. Thus its correlation is zero, including after bounded periodic multiplication.
- Each exceptional interval has logarithmic length \(\log4\); only \(O(\log\log X)\) can meet \([\sqrt X,X]\). Therefore the asserted exceptional bound
  \[
  \frac1{\log X}\int_{E\cap[\sqrt X,X]}\frac{dN}{N}
  =O\!\left(\frac{\log\log X}{\log X}\right)
  \]
  holds for all sufficiently large \(X\), implying every fixed exponent \(0<\kappa<1\) claimed there.
- The “every growing ratio” assertion survives discrete summation. Put \(\ell=\log\omega(x)\). A logarithmic interval of length \(\ell\) meets \(O(\log(2+\ell))\) support intervals: their starting coordinates \(2^j\log2\) double. Each complete support interval has harmonic mass
  \[
  \sum_{L_j<n\le2L_j}\frac1n\le\log2.
  \]
  Consequently, uniformly in the window’s position,
  \[
  \sum_{x/\omega(x)<n\le x}\frac{b(n)}n
  =O(\log(2+\log\omega(x)))=o(\log\omega(x)).
  \]
  Bounded multipliers obey the same domination. Thus every admissible \(\omega(x)\to\infty\), however slowly, is covered—not merely a chosen subsequence.
- For real \(N\in[3L_j/4,5L_j/4]\), the contribution from the \(j\)-th interval is exactly
  \[
  \min(\lfloor2N\rfloor,2L_j)-\max(\lfloor N\rfloor,L_j),
  \]
  giving
  \[
  B(N)/N\ge\tfrac35-\frac4{3L_j}.
  \]
  Also \(A(2L_j)/(2L_j)\ge1/2\).

An explicit admissible failure of (H) uses \(X=T=2L_j\), \(Y=\sqrt X\), \(v=L_j\). For every \(0<\theta\le1/4\), its predecessor window lies inside the displayed bad cluster once \(j\) is large.

This validates the estimates-only obstruction beyond the abstract profile in [TPC140 main.tex:108](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-140-exceptional-scale-selector-power-gate/main.tex:108). The logarithmic comparison retains the fixed-data quantifiers of [TPC137 main.tex:305](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-137-prime-square-fixed-two-log-closure/main.tex:305) and [Tao, Theorem 1.2](https://arxiv.org/html/1509.05422#S1).

**Boundary:** this \(0/1\) sequence is neither Möbius nor multiplicative. It refutes estimates-only inference, not an arithmetic-specific theorem.

## 5. Physical contract and no-GO boundary

The literal core has \(t+2=s(u+az)\), hence fixed \(h_0=2\). The spacing \(q=as\) is **not** the physical outer prime \(q\). No physical window parameter \(H\), conductor identification, outer-prime synthesis, or occurrence cover is supplied.

Only bounded periodic signs/masks are included; an odd-carrier mask must charge its combined period. Nonperiodic physical weights and generic phases remain outside scope. Natural masses are \(N/q\) and terminal \(T/q\).

With \(\theta=(\log X)^{-b}\), \(Y=T(\log X)^{-A}\), retaining all range restrictions, the conditional logarithmic exponent is \(\min(\kappa_0,b,A)\). Physical census, weight/phase return, and occurrence normalization remain unpaid. The core has no squarefree truncation tail.

The fixed-power input is \(\sigma_{\rm aff}=0\). Any physical return must still pay selector, census, BV/phase, applicable tail, and occurrence losses as in [TPC140 main.tex:273](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-140-exceptional-scale-selector-power-gate/main.tex:273). No strict physical \(\delta_{\rm phys}>1/400\) is established. Neither analytic gate closes.

## 6. Diagnostics and preservation

The proof-writer skill governed assumption separation and endpoint verification; its file-writing defaults were suppressed by the read-only contract.

One inline `python -B` diagnostic exited **0**: 26,244 rational-chain checks, 420 partition/lattice checks, 131,638 sparse-block probes, and 8,064 local-difference checks. These are diagnostics, not asymptotic evidence.

Commands `pwd`, `cat`, `sed -n`, `nl -ba … | sed -n …`, `wc -l`, `sha256sum`, `git rev-parse HEAD origin/main`, `git diff --name-only`, `git diff --cached --name-only`, and `git --no-optional-locks status --porcelain=v1 --untracked-files=all` all exited **0**. Primary-page retrievals succeeded. No children, builds, regeneration, synchronization, uploads, or repository writes occurred.

Start/end HEAD and `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start/end control SHA256 values were identical:

```text
AGENTS.md                  6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md             36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
TPC_ROUTE_MAP.md           3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md   e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```

The report, map guide, and four manuscript hashes also remained unchanged. Tracked-dirty paths stayed at **10**; index stayed empty. Untracked paths changed **631 → 633**, solely through authorized parent additions `AUTO_REVIEW.md` and `REVIEW_STATE.json`; no removals.

Narrowest next mathematical obligation: prove actual-family predecessor covering—or independently prove the required actual-prefix estimate. **Neither is established by this audit.**
