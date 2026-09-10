## TPC_AGENT_RESULT_V1

`task_id: recon-recent-analytic-literature`  
`role: tpc_source_lock`  
`verdict: ELIMINATED_SCOPED`  
`files_changed: []`

**Result:** No checked external theorem supplies a new, source-locked physical Gate-B input. Two plausible imports fail for different reasons: the Kloosterman theorem has a fixed-power saving but lacks the literal-packet transfer; the newest logarithmic Chowla claim has strong shift quantifiers but the wrong coefficients and normalization. This eliminates these direct imports—not all possible uses of their methods.

Location: **island 2 → image Bridge A → repository Gate B**. Neither bridge nor gate is declared closed.

### Frozen physical contract

The target is
\[
C=\sum_{\substack{Q<q\le2Q\\q\ {\rm prime}}}q
\sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
\beta(t)w(u)K_H(u-t)
\left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right),
\]
where
\[
I_x=(x/2,x]\cap\mathbb Z,\quad H=x^{21/32},\quad Q=x^{1/3},
\]
\[
\beta(t)=\frac{\Lambda(t)}{\log t}
-\sum_{\substack{d\mid t\\d^{400}\le x^{133}}}\mu(d),
\qquad w(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]

Here \(K_H(h)=\widehat\psi_+(h/H)\). The physical shift is **\(h_0=2\)** in \(w\), not the variable \(u-t\). The detailed \(b_x^{(z)}\) definition and \(z\)-uniformity remain **unlocked in this scout**; no external approximant is substituted. Sources: [V59 coefficient/domain lock](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:35), [signed scalar](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:64).

The required bound is \(C\ll x^{5/3-\delta+o(1)}\), **\(\delta>1/400\)**. This is a signed scalar obligation, not automatically a maximal \(q\)-prefix obligation. The character formulation retains the \((q-2)Z\) subtraction. The complete endpoint ledger is
\[
\eta=\min\{\eta_A,\delta-1/400,419/2400\}>0.
\]
See [diagonal correction](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:124), [loss ledger](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:353).

### Candidate 1 — Blomer–Pascadi, Theorem 1.1

Seven-field import contract:

1. **Coefficients/masks:** arbitrary complex \(\alpha_m,\gamma_n\), classical \(S(am,n;c)\), and \((m,n,c)=1\).
2. **Shift:** no physical \(h_0\); identifying the Kloosterman arguments with the target is missing.
3. **Domain/order:** arbitrary integer intervals \(\mathcal I,\mathcal J\), each containing at most \(N\) integers; no physical block-pair identity is supplied.
4. **Ranges:** integer \(c\ge1\), \(1\le N\le c\), \(a\) a unit modulo \(c\).
5. **Uniformity:** arbitrary arrays and moduli; no exceptional-modulus exclusion.
6. **Normalization:** the theorem bounds the bilinear form by
   \[
   \|\alpha\|_2\|\gamma\|_2c^{1+o(1)}
   \left(N^{1/8}c^{-3/32}+N^{5/16}c^{-3/16}
   +N^{2/3}c^{-7/18}\right).
   \]
   At \(N\asymp\sqrt c\), this saves \(c^{-1/32}\).
7. **Physical losses:** assuming a valid \(c\asymp Q\) compiler, the benchmark is \(x^{-1/96}\); additional exponent loss must be strictly below
   \[
   1/96-1/400=19/2400.
   \]

These are source-stated quantifiers, not a physical transfer. Importantly, **smoothness of the arrays is not required**. [Primary theorem](https://arxiv.org/html/2607.24311v1)

**Kill test:** demand an exact, uniformly controlled decomposition of all four physical polarized packets, preserving masks, centering and diagonal correction, with local normalization \(Q^2H\) and total normalization \(xQ^2\). No checked source supplies it. Failure to exhibit this decomposition kills the direct import before exponent arithmetic.

**Closest existing result:** this engine is already in [V59’s compiler audit](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:397). [TPC247’s source attachment](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/notes/source_lock.md:3) does not itself provide that compiler. Thus this is not a new route under a new name.

### Candidate 2 — Guo, Theorem 1.1, v4

This September 2026 preprint’s **stated theorem** was inspected; its full proof was not independently validated.

Seven-field import contract:

1. **Coefficients/masks:** \(\lambda(n)\lambda(n+h)/n\); no \(\beta,w\), prime-\(q\) sum, unit masks or centered residue kernel.
2. **Shift:** positive integer \(h\); \(h=2\) is permitted asymptotically.
3. **Domain/order:** all initial prefixes \(n\le y\le x\), with logarithmic weight \(1/n\).
4. **Ranges:** sufficiently large \(x\); \(1\le h,H\le x\).
5. **Uniformity:** one exceptional set \(E_x\), independent of \(A\), satisfying for every fixed \(A>0\)
   \[
   |E_x\cap[1,H]|\ll_A H(\log x)^{-A}
   \]
   uniformly in \(H\), and
   \[
   \max_{h\notin E_x}\sup_{y\le x}
   \left|\sum_{n\le y}\frac{\lambda(n)\lambda(n+h)}n\right|
   \ll(\log x)^{1-c}.
   \]
   Thresholds are ineffective.
6. **Normalization:** natural scale \(\log x\), not natural-counting scale \(x\).
7. **Loss:** logarithmic saving only; no positive physical \(\delta\), hence no payment of \(1/400\).

[Primary statement](https://arxiv.org/html/2608.23500v4)

**Important inference:** setting \(H=2\) eventually forces \(E_x\cap[1,2]=\varnothing\). Therefore “fixed shift could be exceptional” is **not** a valid rejection here.

**Kill test—normalization obstruction:** let \(a_n\) indicate
\[
\bigcup_{k\ge1}(2^{2^k},\,2^{2^k+1}].
\]
Then
\[
\sup_{y\le x}\sum_{n\le y}\frac{a_n}{n}=O(\log\log x),
\]
but at \(X_k=2^{2^k+1}\),
\[
\sum_{X_k/2<n\le X_k}a_n=X_k/2.
\]
Thus even stronger logarithmic-prefix control does not imply natural dyadic cancellation for general bounded sequences. This is an elementary transfer obstruction, **not a counterexample for Liouville**. The physical coefficient identification is independently missing.

### Checked-source register

Thirteen focused searches covered correlations, short intervals, varying shifts, BDH and bilinear/spectral Kloosterman estimates. Abstracts/introductions were inspected; theorem statements were read where used above.

| Primary source/version | Import finding |
|---|---|
| [Blomer–Pascadi, 2607.24311v1](https://arxiv.org/html/2607.24311v1) | Fixed-power engine; compiler unpaid. |
| [Pascadi, 2511.08445v2](https://arxiv.org/html/2511.08445v2) | Balanced-semiprime improvement does not identify prime-supported physical packets. |
| [Milićević–Qin–Wu, 2511.07550v1](https://arxiv.org/html/2511.07550v1) | General-modulus engine; square-root saving weaker than the first candidate. |
| [Harper, 2412.19644v1](https://arxiv.org/html/2412.19644v1) | Stated variance range requires \(Q>\sqrt{2x}\), unlike physical \(x^{1/3}\). |
| [Pascadi, 2404.04239v3](https://arxiv.org/html/2404.04239v3) | Sparse-Fourier spectral input; required physical Fourier structure unproved. |
| [Wright, 2604.25177v2](https://arxiv.org/html/2604.25177v2) | Convolution/Siegel–Walfisz hypotheses do not identify this binary packet. Outer absolute sums can restrict to primes. |
| [Matomäki–Shao–Tao–Teräväinen, 2204.03754v4](https://arxiv.org/html/2204.03754v4) | Physical \(H\) meets the \(5/8+\varepsilon\) range; relevant Möbius/prime branches give logarithmic savings and different coefficients. |
| [Matomäki–Radziwiłł–Shao–Tao–Teräväinen, 2411.05770v2](https://arxiv.org/html/2411.05770v2) | Almost-all starting points do not cover every prescribed physical block. |
| [Pilatte, 2310.19357v3](https://arxiv.org/html/2310.19357v3) | Logarithmically weighted two-point saving. |
| [Jaskari–Sachpazis, 2409.10663v3](https://arxiv.org/html/2409.10663v3) | Conditional Siegel-zero regime; full parameter range not source-locked for import. |
| [Wilson, 2408.08726v2](https://arxiv.org/html/2408.08726v2) | Polynomial-family moments, not the designated polynomial. |
| [Tao–Teräväinen, 2512.01739v2](https://arxiv.org/html/2512.01739v2) | Good-scale/logarithmic control; affine coefficients only polylogarithmic in the relevant statement. |
| [Guo, 2608.23500v4](https://arxiv.org/html/2608.23500v4) | Candidate 2; granting the claim still leaves normalization/identification unpaid. |
| [Wang, 2608.16108v1](https://arxiv.org/html/2608.16108v1) | Shift-averaged dynamical statement, not fixed-shift physical cancellation. |

**Strongest objection:** none identifies the actual paired coefficient and pays its complete physical loss ledger. The narrowest next action is auditing an explicit coefficient-preserving compiler—not another generic search for stronger cancellation.

### Read-only receipt

Repository reads: required controls/guide, V58, V59, proper-factor/unit-ratio reduction, and TPC247 manuscript/source lock. No scientific producers, checkers, builds, downloads to the repository, or new drafts were executed.

Observed start/end `HEAD = origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

All four control SHA-256 values remain exactly equal to the supplied baseline; handoff hash:
`9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007`.

Final commands, all exit **0**:

```text
git rev-parse HEAD origin/main
sha256sum AGENTS.md TPC_HANDOFF.md research/tpc-big-road/TPC_ROUTE_MAP.md research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md
git --no-optional-locks status --porcelain=v1 -uall
rg --files papers | rg '^papers/tpc-247-.*(main\.tex|source_lock\.md)$'
```

Final status comparison: original ten tracked modifications preserved; no removed status entries; untracked count **615 → 617**, with exactly the authorized parent additions `PROOF_PACKAGE.md` and `DERIVATION_PACKAGE.md`. Neither draft was treated as proved or audited by this scout.
