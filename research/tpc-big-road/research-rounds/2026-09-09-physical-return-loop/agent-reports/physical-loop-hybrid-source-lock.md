```json
{
  "schema": "TPC_AGENT_RESULT_V1",
  "task_id": "physical-loop-hybrid-source-lock",
  "role": "tpc_source_lock",
  "mode": "READ_ONLY_RESEARCH_AND_AUDIT",
  "verdict": "COEFFICIENT_CONTRACT_RECOVERED_WITH_EXPLICIT_FOURIER_CROSSWALK",
  "physical_saving_proved": false,
  "publication_GO": false,
  "files_changed": []
}
```

The missing hybrid definition is recoverable from original ancestors. Nonnegative, real, smooth compactly supported kernel-profile assumptions are also recoverable, provided the Fourier-sign crosswalk is made explicit. **Evenness is not locked.** Neither recovery establishes physical cancellation.

### 1. Original coefficient and parameter contract

**Source statements.** For real \(z\ge2\), define
\[
\begin{aligned}
P(z)&=\prod_{p\le z}p,&
W_z&=\prod_{p\le z}\frac p{p-1},&
C_z&=\prod_{p>z}\left(1-\frac1{(p-1)^2}\right),\\
b_x^{(z)}(u)
&=\mathbf1_{u\in I_x}\,C_zW_z
 \mathbf1_{(u+2,P(z))=1}
 \prod_{\substack{p\mid u\\p>z}}\frac{p-1}{p-2},
& I_x&=(x/2,x]\cap\mathbb Z.
\end{aligned}
\]
This is the repository’s actual tensor-local hybrid, including the prime \(2\) and the forbidden residue \(-2\). It is not a generic sieve approximant. See [fm_local_comparison_compiler.md:727](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/fm_local_comparison_compiler.md:727).

The identical divisor expansion is
\[
b_x^{(z)}(u)=\mathbf1_{I_x}(u)C_zW_z
\mathbf1_{(u+2,P(z))=1}\sum_{d\mid u}g_z(d),\qquad
g_z(d)=\mu^2(d)\mathbf1_{P^-(d)>z}
       \prod_{p\mid d}\frac1{p-2},
\]
with the usual empty-product convention. The earlier literal emitter explicitly records \(h_0=2\), \(x=2X\), and \(z=(\log x)^K\): [bridge_b_literal_jutila_farey_atom_compiler.md:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_literal_jutila_farey_atom_compiler.md:43).

The downstream lanes are exactly
\[
w(u)=\Lambda(u+2)-b_x^{(z)}(u),\qquad
\beta(t)=\frac{\Lambda(t)}{\log t}
-\sum_{\substack{d\mid t\\d^{400}\le x^{133}}}\mu(d).
\]
Both are real; the hybrid channel has a minus sign. The contracted \(\beta\) preserves the original signed occurrence sum, not an alternating model sequence. [V59:54](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:54)

**Uniformity.** The cancellation-related parameter order is
\[
(A,\varpi)\longrightarrow B_{\rm FM}
\longrightarrow\text{fixed }K=K(B_{\rm FM})
\longrightarrow x\ge x_0(A,\varpi,B_{\rm FM},K).
\]
One fixed finite \(K\) is not an all-\(B\) object. Maximal Type-I constants are not uniform as \(\gamma\uparrow1/2\). [fm compiler:797](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/fm_local_comparison_compiler.md:797), [fm compiler:952](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/fm_local_comparison_compiler.md:952)

### 2. Ordinary size and \(\ell^2\): explicit, but not cancellation

**Source statement.**
\[
0\le b_x^{(z)}(u)\le C(\log z)\tau(u),
\]
and the source declares the fixed-\(K\) subpower envelope. V35 explicitly asserts \(|\beta|,|w|\le x^{o(1)}\). [fm compiler:821](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/fm_local_comparison_compiler.md:821), [V35:203](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_proper_factor_unit_ratio_reduction.md:203)

**My elementary derivation, not a quoted source theorem.** Set
\[
a_p=\left(\frac{p-1}{p-2}\right)^2-1,\qquad
B_0=\prod_{p>2}(1+a_p/p)<\infty.
\]
Because \(a_p/p=O(p^{-2})\), this is an absolute constant. Drop the nonnegative sieve mask, use \(C_z\le1\), expand the product over squarefree divisors, and count multiples by \(x/d\). This gives
\[
\boxed{\|b_x^{(z)}\|_{\ell^2(I_x)}^2\le B_0xW_z^2},
\]
hence, with \(N=\lfloor x\rfloor-\lfloor x/2\rfloor\),
\[
\boxed{\|w\|_2^2
\le2N\log^2(x+2)+2B_0xW_z^2.}
\]
For fixed \(K\), this is \(O_K(x\log^2x)\). In fact the crude bound is uniform for all \(z\ge2\): when \(z\le x+2\), \(W_z\ll\log(x+2)\); when \(z\ge x+2\), the sieve mask makes \(b_x^{(z)}\) identically zero on \(I_x\).

These bounds have no exceptional-coordinate set. They do **not** make the cancellation theorems \(K\)-uniform, estimate weighted row energy, or provide fixed-power saving.

### 3. Original smoothing contract and Fourier seam

**Source statements.** The Jutila ancestor fixes
\[
\psi\in C_c^\infty(\mathbb R),\quad
\operatorname{supp}\psi\subset[-1,1],\quad
0\le\psi\le1,\quad \int\psi=1.
\]
See [V23:186](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_prime_shell_jutila_and_stable_dynamics.md:186) and the primary source, [Blomer–Li, §2.1, Lemma 1](https://arxiv.org/html/2511.03294v1#S2.SS1).

There is a notation seam:

- V25 defines \(\widehat\psi_+(\xi)=\int\psi(v)e(+\xi v)\,dv\). [V25:87](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_corrected_fourier_factorable_emitter.md:87)
- V36/V59 write \(\widehat\psi_+(y)=\int\psi_+(v)e(-vy)\,dv\). [V36:122](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_multiroute_ratio_core_atlas.md:122)

**Derived exact crosswalk:** preserving the same transform requires
\[
\boxed{\psi_+(v)=\psi(-v).}
\]
The reflection equation was not explicitly printed in the inspected chain; it follows by substitution/Fourier inversion. It preserves the original kernel, rather than choosing a replacement.

Consequently the inherited profile is real, nonnegative, fixed, compactly supported and Schwartz. For
\[
K_H(h)=\widehat\psi_+(h/H)
\]
one obtains
\[
K_H(0)=1,\quad |K_H(h)|\le1,\quad
K_H(-h)=\overline{K_H(h)},\quad
|K_H(h)|\ll_{\psi,A}(1+|h|/H)^{-A}.
\]
Constants may depend on the fixed profile and its seminorms, but not on \(x,q,H\). No uniformity over unrestricted varying profiles is supplied.

**Not locked:** evenness, real-valued \(K_H\), a particular numerical bump, or hard support \(|h|\le H\). Hermitian symmetry requires reality of the profile, not evenness. Positivity of the profile does not make the diagonal-deleted, centered arithmetic operator positive.

### 4. Physical domain, normalization and loss budget

The actual scalar remains
\[
\mathfrak C_x=
\sum_{\substack{Q<q\le2Q\\q\ {\rm prime}}}q
\sum_{\substack{t,u\in I_x\\t\ne u,\ q\nmid tu}}
\beta(t)w(u)K_H(u-t)
\left(\mathbf1_{u\equiv t\pmod q}-\frac1{q-1}\right),
\]
where \(x=2X,\ H=x^{21/32},\ Q=x^{1/3}\), and **\(h_0=2\)** is independent of \(H\) and conductor. [V59:33](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:33)

Integer coordinates are ordered increasingly. Moving prime prefixes use \(Q<q\le Y\), \(Q<Y\le2Q\); a terminal scalar estimate alone does not control those prefixes. [V58:346](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:346)

The natural local scale is \(Q^2H=x^{127/96}\); reassembly over \(x/H=x^{11/32}\) gives \(xQ^2=x^{5/3}\). Required:
\[
|\mathfrak C_x|\ll x^{5/3-\delta+o(1)},\qquad \delta>1/400.
\]
The exact V58 readout divides by \(K_*=x^{2/3+o(1)}\), with error numerator \(x^{143/96+o(1)}\). With Gate-A margin \(\eta_A\), the physical margin must satisfy
\[
0<\eta<\min\{\eta_A,\delta-1/400,419/2400\}.
\]
At \(\delta=1/96\), additional attachment losses must total **strictly less than \(19/2400\)**. None is paid by the ordinary norm estimate above. [V58:295](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:295)

### 5. Objection, closest result and verdict

**First fatal mismatch for an even/real-kernel attachment:** the source licenses Hermitian symmetry, not evenness or real-valued \(K_H\). Using the unreflected original \(\psi\) under the negative-transform convention also changes orientation unless symmetry is separately proved.

**Strongest objection:** ordinary coefficient norms do not pay normalized weighted lanes or signed collective cancellation. TPC247 proves the exact physical covariance without requiring Hermiticity, but records the copied-lane toll \(\|\mathbf W\|^2=m\|w\|^2\) and possible loss of cross-block cancellation. [TPC247 main.tex:81](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:81), [main.tex:146](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:146)

The closest traced arithmetic input is the fixed-\(K\), arbitrary-fixed-logarithmic maximal interval mean for \(w\), not a power-saving second moment. [Hybrid-mean closure:43](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_source_backed_rank_midpoint_hybrid_mean_closure.md:43)

**Verdict:** definition/regularity recovery succeeds with the explicit reflection crosswalk. Physical saving remains unproved. Position: islands ③/②, image Bridge A, repository Gate B. Formal endpoint TPC418; no GO, gate closure, numbered writer or arithmetic-advance claim.

### 6. Preservation and command audit

Start/end HEAD and local `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start → end: tracked dirty **10 → 10**, untracked **631 → 633**, index **empty → empty**. Additions were only parent-authorized `AUTO_REVIEW.md` and `REVIEW_STATE.json`.

Control SHA-256, **identical at start and end**:

```text
AGENTS.md
6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md
36bda1a25e24d04d83d43088352da4f4f05a8ee9c915af8b8f13fe3113cb8c9a
research/tpc-big-road/TPC_ROUTE_MAP.md
3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md
e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```

Preservation commands, all exit **0**, executed from the repository root:

```bash
git --no-optional-locks rev-parse HEAD origin/main
git -c core.preloadIndex=false --no-optional-locks status --porcelain=v1 -uall
git --no-optional-locks diff --name-only
git --no-optional-locks diff --cached --name-only
sha256sum AGENTS.md TPC_HANDOFF.md research/tpc-big-road/TPC_ROUTE_MAP.md research/tpc-big-road/PAPER_CANDIDATE_LEDGER.md
```

Source inspection used scoped `rg`, `rg --files`, `wc`, `sed`, and `nl`. Two expected no-match searches returned **1**: nested `AGENTS.md` discovery and an explicit reflection/evenness-definition search. Other reads succeeded. Primary web retrieval succeeded. No children, builds, regeneration, repository downloads, synchronization, credential inspection or external-model uploads occurred.
