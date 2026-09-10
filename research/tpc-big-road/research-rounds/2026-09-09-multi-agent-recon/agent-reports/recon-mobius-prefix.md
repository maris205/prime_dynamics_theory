TPC_AGENT_RESULT_V1

task_id: `recon-mobius-prefix`  
role: `tpc_source_lock`  
verdict: `PROPOSE_FOR_AUDIT` — **conditional transfer lemma only**; an estimates-only bad-scale-selection argument is eliminated below.  
location: Islands ③/④ → ②, upstream of Bridge A. No gate reopening, mathematical GO, or publication claim.  
files_changed: `[]`

### 1. Candidate: adaptive good-block covering gives a deterministic prefix maximum

**Source-backed input.** TPC149 supplies the literal periodic Möbius correlation on good scales, with one exceptional set uniform over its declared small-polylogarithmic family. Its proof uses exact quotient lifts and density-normalized periodic reassembly:

- [TPC149 main.tex:133](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-149-small-polylog-determinant-two-mobius-corridor/main.tex:133), with the common-family theorem at line 220.
- [TPC147 main.tex:167](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-147-tt-periodic-residue-reassembly/main.tex:167): no periodic-residue census loss.
- [TPC148 main.tex:103](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-148-quotient-mobius-fiber-lift/main.tex:103): exact Möbius recovery; nonpretentiousness at lines 213–285.

The external premises match [Tao–Teräväinen, Theorem 3.1(ii)](https://arxiv.org/html/2512.01739v2#S3) and [Matomäki–Radziwiłł–Tao, equation (1.12)](https://arxiv.org/html/1503.05121#S1).

**Derived lemma, conditional on one explicit hypothesis.**

Write
\[
q=as,\quad t(z)=ad+qz,\quad
b_z=\mu(d+sz)\mu(u+az)\rho(z),
\]
\[
A_\rho(U)=\sum_{0<t(z)\le U}b_z,\qquad
B_\rho(N)=\sum_{N<t(z)\le2N}b_z.
\]
Let \(G_X\subset[\sqrt X,X]\) be a common good set on which
\[
q|B_\rho(N)|/N\le\varepsilon_X\|\rho\|_\infty,
\qquad \varepsilon_X=C(\log X)^{-\kappa_0}.
\]

Choose
\[
0<\delta\le1/4,\qquad
\sqrt X\le Y,\qquad 2Y/(1-\delta)\le T\le X.
\]

The **single missing hypothesis**, multiplicative predecessor covering, is
\[
\tag{H}
\forall v\in[Y/(1-\delta),T/2],\quad
[(1-\delta)v,v]\cap G_X\ne\varnothing .
\]

Then, with \(J=\lceil\log_2(T/Y)\rceil\),
\[
\boxed{
\frac qT\sup_{0\le U\le T}|A_\rho(U)|
\le\|\rho\|_\infty
\left[
\varepsilon_X+2\delta+
\frac{2Y}{(1-\delta)T}
+\frac{(J+1)q}{T}
\right].}
\]

**Proof.** Starting at \(U_0=U\), while \(U_j\ge2Y/(1-\delta)\), use (H) to choose
\[
U_{j+1}\in G_X\cap[(1-\delta)U_j/2,U_j/2].
\]
The exact identity is
\[
A_\rho(U_j)=A_\rho(U_{j+1})+
B_\rho(U_{j+1})+
\sum_{2U_{j+1}<t(z)\le U_j}b_z.
\]
The last interval has length at most \(\delta U_j\), hence contributes at most
\(\|\rho\|_\infty(\delta U_j/q+1)\).
Furthermore, \(\sum U_{j+1}\le T\), \(\sum U_j\le2T\), there are at most \(J\) steps, and the terminal prefix has fewer than \(2Y/((1-\delta)q)+1\) points. Summing proves the bound.

This is **not TPC159’s dyadic-shadow conclusion**: the original endpoint and its exact dyadic ancestors may be bad. The construction moves each block and explicitly pays its uncovered edge. The closest existing result is [TPC159 main.tex:133](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-159-dyadic-shadow-prefix-lifting/main.tex:133), which requires exact ancestor avoidance.

**Seven-field contract.**

1. **Signs/weights/masks:** literal \(b_z\) above; \(\rho\) bounded periodic. Odd-carrier restriction may be included as \(1_{t(z)\text{ odd}}\), with its period-two contribution charged. No nonperiodic weight or generic phase.
2. **Physical shift:** \(sV-aD=2\), so the shift in \(t\) is exactly \(h_0=2\). The quantity \(q=as\) is progression spacing, not that shift. Full physical-occurrence identification remains missing.
3. **Domain/order:** integer \(z\), increasing \(t(z)\), positive cumulative prefixes \(0<t(z)\le U\). The maximum uses denominator \(T/q\), **not** varying \(U/q\).
4. **Ranges:** positive coprime odd \(a,s\), integral \(d,u\), \(su-ad=2\), \(qR\le(\log X)^{\eta_0}\), and the displayed \(Y,T,\delta\) conditions. \(X\) is the source’s ambient scale, not an identified physical conductor.
5. **Uniformity/exceptions:** retain TPC149’s common exceptional set. Hypothesis (H) must hold for the same good set and selected family. It is **unproved**, not supplied by global logarithmic density.
6. **Normalization:** block mass \(N/q\); terminal comparison mass \(T/q\).
7. **Losses:** source \(\varepsilon_X\); trims \(2\delta\); small prefix \(2Y/((1-\delta)T)\); lattice cost \((J+1)q/T\). No squarefree tail or \(R\)-census loss. With \(\delta=(\log X)^{-b}\), \(Y=T(\log X)^{-A}\), the core log exponent is \(\min(\kappa_0,b,A)\). Physical census, weight/phase return, and occurrence normalization remain missing. Fixed-\(X\)-power credit is **zero**; no strict \(1/400\) credit.

**Kill test:** find a \(v\) whose entire predecessor window misses the actual threshold-defined good set. This kills (H) at the proposed parameters without contradicting TPC149.

### 2. Scoped elimination: global bad-scale density does not supply (H)

The obstruction uses a bounded sequence generating genuine block correlations, rather than an arbitrarily prescribed measurable correlation profile.

Set
\[
L_j=2^{2^j},\qquad
b(n)=1_{\bigcup_j(L_j,2L_j]}(n).
\]
Its block correlation vanishes outside
\[
E=\bigcup_j[L_j/2,2L_j],
\]
and
\[
\frac1{\log X}\int_{E\cap[\sqrt X,X]}\frac{dN}{N}
=O\!\left(\frac{\log\log X}{\log X}\right).
\]
This satisfies every fixed small exponent \(0<\kappa<1\) of the relevant exceptional-density shape.

It also satisfies, for **every** \(\omega(x)\to\infty\),
\[
\sum_{x/\omega(x)<n\le x}\frac{b(n)}n=o(\log\omega(x)).
\]
On the logarithmic axis, the support intervals have bounded length and gaps tending to infinity. Given spacing \(D\), an interval of length \(H\) meets at most a fixed initial number plus \(H/D+2\) support intervals. Divide by \(H\to\infty\), then let \(D\to\infty\). The same domination handles bounded periodic multipliers.

Nevertheless,
\[
\frac1{2L_j}\sum_{n\le2L_j}b(n)\ge\frac12,
\]
and throughout \(N\in[3L_j/4,5L_j/4]\),
\[
\frac1N\sum_{N<n\le2N}b(n)\ge\frac35-O(L_j^{-1}).
\]
Thus positive-width bad-scale clusters survive both estimate types.

This strengthens the abstract selector obstruction in [TPC140 main.tex:108](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-140-exceptional-scale-selector-power-gate/main.tex:108). The frozen source being compared is [TPC137 main.tex:305](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-137-prime-square-fixed-two-log-closure/main.tex:305), based on [Tao, Theorem 1.2](https://arxiv.org/html/1509.05422#S1).

**Seven-field contract:** (1) the displayed \(0/1\) model coefficients, no hidden signs; (2) no Möbius or physical-\(h_0\) identification; (3) natural integer order, displayed blocks and prefixes; (4) \(q=R=1\), all sufficiently large ambient \(X\), sparse endpoints \(2L_j\); (5) one global \(E\), all growing terminal ratios; (6) block normalization \(N\), prefix \(T\), logarithmic \(\log\omega\); (7) no physical saving or loss budget.

**Verdict:** `ELIMINATED_SCOPED` for selection arguments using only these estimates and boundedness. **Strongest objection:** the sequence is not Möbius or multiplicative. It does not disprove an arithmetic-specific route.

### Exact CPU probe

Two inline `python -B` probes used only in-memory integer/Fraction arithmetic; both exited **0**. No repository producer or checker ran.

For \(T=16384,Y=128,\delta=1/16\), the probe evaluated
\[
F_R(N)=\frac qN\sum_{r\bmod R}
\left|\sum_{\substack{N<t(z)\le2N\\z\equiv r\bmod R}}
\mu(D(z))\mu(V(z))\right|,
\]
the exact supremum over \(\|\rho\|_\infty\le1\), using rational event cells at \(N=t,t/2\).

For fibers \((a,s,d,u)=(1,1,1,3),(1,3,1,1)\), \(R=2\), threshold \(1/8\) gave no covering holes. The second fiber had three bad components: covering was not identical to all scales being good.

At threshold \(1/16\), that fiber had four covering holes. An exact failing witness was
\[
v=9053/60,\qquad
[(1-\delta)v,v]=[9053/64,9053/60].
\]
These are finite predicate tests, **not** sourced asymptotic constants or evidence proving (H).

### Commands, hashes, and reconciled preservation

Read/hash/git commands—`cat`, `nl -ba`, `sed`, targeted `rg`, `sha256sum`, `git rev-parse HEAD origin/main`, `git diff --name-only`, `git diff --cached --name-only`, and `git --no-optional-locks status --porcelain=v1 --untracked-files=all`—all exited **0**. Two external retrieval attempts failed; the required primary arXiv HTML sources were subsequently read successfully.

Observed start/end HEAD and `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

All four control SHA256 values exactly matched the task envelope at start and end. All six manuscript hashes were unchanged. The index remained empty; the tracked-dirty list remained the same ten paths.

Untracked count changed **615 → 617**, solely through `PROOF_PACKAGE.md` and `DERIVATION_PACKAGE.md`. The parent subsequently confirmed these as its authorized additions; rechecks confirmed no original path removals or further additions. **The preservation exception is resolved.** This agent neither created nor read those drafts, and provides no mathematical endorsement of them.

The completed reconnaissance therefore retains the conditional lemma and scoped elimination above, with `files_changed=[]`.
