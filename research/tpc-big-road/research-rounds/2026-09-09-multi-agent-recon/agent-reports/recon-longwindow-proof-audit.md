TPC_AGENT_RESULT_V1

task_id: `recon-longwindow-proof-audit`  
role: `tpc_proof_auditor`  
verdict: **VERIFIED_SCOPED_CANDIDATE — NOT publication GO**  
mode: `READ_ONLY`; children: `0`; files_changed: `[]`  
first_fatal_mismatch: `NONE`

The stated theorem is valid for the explicitly defined full-kernel, full-row-energy-normalized model. It establishes a genuine uniform growing-model bound in the declared long-window regime. It does not establish a bound for the physical \(\mathfrak C_X\), discharge the seven-field physical contract, or change a handoff gate.

### Proof verification

The audited constant uses **\(\mu=\min_p(a_pp)\)**, not \(\min_p a_p\).

1. **Literal source identity and masks: verified.**  
   [TPC401’s original definition](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.tex:33) and its code’s lines 55–67 agree with
   \[
   a_pT_{uv}\big((p-1)\mathbf1_{p\mid u-v}-1\big)
   \mathbf1_{u\ne v}\mathbf1_{p\nmid u}\mathbf1_{p\nmid v},
   \qquad a_p=\frac{p^3}{Q^2(p-1)}.
   \]
   The general positive amplitudes are an explicitly declared extension. No short-window identity is improperly imported.

2. **Full matrix and energy identities: verified.**  
   In [DERIVATION_PACKAGE.md](/root/autodl-tmp/math_research3/prime_dynamics_theory/DERIVATION_PACKAGE.md:64), the diagonal cancellation is exactly
   \((p-1)-1-(p-2)=0\). On active off-diagonal entries, the multipliers are \(p-2\) and \(-1\). Thus
   \[
   (p-2)^2-1=(p-1)(p-3)
   \]
   gives the stated \(G\) identity. When \(N<p\), congruence neighbors disappear and the formula reduces to TPC401/TPC404’s short-window geometry. TPC404’s displayed denominator and TPC417’s star/bulk formulas must **not** be reused unchanged for this long-window model.

3. **Step 1, including \(p=3\), \(H=p\), and boundary rows: verified.**  
   The left/right available distances total \(4H-1\); one side therefore contains distances \(1,\ldots,H\). Its \(\lfloor H/p\rfloor\) multiples of \(p\) are distinct, off-diagonal, and retain both nonunit masks because \(p\nmid u\). Hence
   \[
   G_p(u)\ge \frac{a_p^2(p-2)^2}{4}\lfloor H/p\rfloor
   \ge \frac{a_p^2pH}{72}.
   \]
   Both inequalities hold at \(p=3\) and \(H=p\). Inactive rows are identically zero.

4. **Step 2, multiplicities and integral direction: verified.**  
   The base unit sum counts each eligible entry once; the additional coefficient \(p-3\) changes the same-residue absolute multiplier from \(1\) to \(p-2\). It is nonnegative, including zero at \(p=3\). Extending each side to all positive distances only increases the sums. Monotonicity gives
   \[
   T(kb)\le b^{-1}\int_{(k-1)b}^{kb}T(x)\,dx,
   \]
   so \(W_p(u)\le2\pi a_pH\) and consequently
   \(W_p(u)\le144\pi G_p(u)/(a_pp)\).

5. **Steps 3–4, zero energies and norm: verified.**  
   Triangle inequality applies to every real \(|\varepsilon_p|\le1\), without sign cancellation. Since \(G\) is a sum of nonnegative squares, \(G(u)=0\) forces every component row, and therefore the corresponding symmetric columns, to vanish. With the specified zero inverse,
   \[
   |x^TZx|
   \le \sum_u y(u)^2\sum_v|M(u,v)|
   \le \frac{144\pi}{\mu}\sum_{G(u)>0}x(u)^2
   \le \frac{144\pi}{\mu}\|x\|_2^2.
   \]
   Real symmetry justifies the absolute Rayleigh-quotient characterization. No positivity assumption on \(M\) is needed.

6. **Growing-shell corollary: verified for finite, nonempty scale families.**  
   \(H\ge2\max_jQ_j\) ensures \(H\ge p_{\max}\), and
   \(a_pp>p>Q_{\min}\). Thus
   \[
   \|Z\|_2<576/Q_{\min}
   \]
   uniformly over origins, shell counts, cardinalities, and declared coefficients. This genuinely tends to zero as \(Q_{\min}\to\infty\), allowing the finite family and dimension to grow. Increasing \(H\) or adding shells while retaining a fixed smallest shell does **not** imply convergence to zero. The illustrative exponent comparison is valid because \(21/32-1/3=31/96>0\).

No substantive proof gap was found in [PROOF_PACKAGE.md](/root/autodl-tmp/math_research3/prime_dynamics_theory/PROOF_PACKAGE.md:75). The proof-writer skill supplied the assumption/degeneracy audit structure; its file-writing workflow was not followed because this task expressly forbids writes.

### Nonblocking wording and source cautions

- Derivation lines 92–94 should qualify “\(C_{p,u}\) cannot be dropped”: at **\(p=3\)** its extra energy coefficient is zero. Congruence neighbors still exist and affect the kernel’s signs; their energy is already included in \(S_{p,u}\).
- The empty-prime case is harmless when shell scales remain specified. For an **empty scale index set**, \(Q_{\min}\) and \(\max_jQ_j\) are undefined; state only \(Z=0\).
- TPC401’s prose boundary example \(u=0,v=11,p=11\) has inactive masks and does not itself demonstrate unequal masked kernels. Its code uses active coordinates instead. The candidate proof does not rely on that prose example, so this source blemish does not invalidate it.
- Arbitrary prime ordering causes no model problem: any prefix can be selected by setting excluded coefficients to zero with \(G\) fixed. Recomputing \(G\) for a nonempty prime subset also satisfies the theorem. This supplies no physical prefix identification. Shorter coordinate windows with recomputed energies are not covered.

### Physical contract and overclaim ceiling

Location: **island ②**, an operator-model estimate relevant to image **Bridge A / repository Gate B**; not a bridge crossing.

| Required field | Audited status |
|---|---|
| Literal coefficient, signs, masks, outer labels | Model kernel and masks exact; actual arithmetic coefficients and outer labels unidentified |
| Fixed physical \(h_0\) | Not supplied; \(h_0=2\) cannot be inferred |
| Domain and exact prefix/order | Model interval and finite prime family explicit; physical ordered coverage/attachment absent |
| \(X,N,q\), parameter ranges | \(N=4H,\ H\ge p_{\max}\) proved; illustrative \(X\)-scales are not a physical parameter map; physical \(q\) contract absent |
| Uniformity/exceptions | Fully uniform model estimate, no exceptional origins; no physical exceptional-set theorem |
| Normalization/natural scale | Exact full row energy used; physical normalization and input/output weighted norms unpaid |
| Complete loss ledger | No demonstrated physical saving or strict \(1/400\) endpoint |

**Strongest overclaim risk:** treating the \(O(Q_{\min}^{-1})\) bound after two-sided energy normalization as arithmetic cancellation or physical scalar saving. The gain comes from the denominator and absolute row domination, not canonical arithmetic signs. It is also not automatically a resolution of TPC418’s growing question on that paper’s short-window proxy.

Correctness and novelty are separate: correctness is verified here; novelty is **not assessed**. Scientific value is a rigorous, elementary long-window model envelope that retains congruence contributions and removes origin/sign-law restrictions within this model. Its physical usefulness remains undetermined. Parent diagnostics were not used as proof evidence.

### Baseline, preservation, and execution record

Observed before and after:

- HEAD: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- Index empty; exactly the ten declared tracked-dirty paths.
- Untracked count: `617 → 617`.
- All six supplied SHA-256 locks matched exactly at both checks.
- The four inspected original source/code files have zero diff against HEAD.
- No observed status delta; no edits, builds, producers, downloads, synchronization, publication, or numerical probes.

Observed handoff SHA-256:  
`9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007`

Candidate SHA-256 values:

```text
PROOF_PACKAGE.md
e1b992eff9b2ef676a7bd0ffb8419cc1def4d05f5471b6d66a05e9244c1d5089
DERIVATION_PACKAGE.md
241b01c856d3ee5395af437a6da4b32f4278f92ebcdb18f451f56c0a4947bb9d
```

Preservation evidence is bounded: I did not hash the contents of all 615 original untracked files, which would exceed the assigned read scope.

**Commands actually run:** 31 shell invocations, all exit code `0`. The following inventory compresses repeated commands and long filenames; all ran from the declared repository root.

- `pwd`.
- `cat` separately on `AGENTS.md`, the proof-writer `SKILL.md`, the island-map guide, and both candidate packages.
- `sed -n '1,240p' TPC_HANDOFF.md`; `sed -n '855,908p' TPC_HANDOFF.md`.
- `rg --files -g AGENTS.md -g '*main.tex' -g '*.py' papers/tpc-401-c1-diagonal-deletion-decomposition`.
- `rg --files -g '*main.tex' -g AGENTS.md papers | rg '/tpc-(404|417)-'` — filename discovery only.
- `nl -ba` on TPC401 `paper/main.tex` and both candidate packages.
- `rg -n '^def |kernel|component|geometry|return|amplitude|literal'` on TPC401’s code.
- `nl -ba … | sed -n '1,180p'` on that code; corresponding ranges `20,105p` on TPC404’s manuscript and `20,110p` on TPC417’s manuscript.
- Twice each: `git --no-optional-locks rev-parse HEAD`; `status --short --branch --untracked-files=no`; `diff --name-only`; `diff --cached --name-only`; `ls-files --others --exclude-standard | wc -l`.
- Twice: `sha256sum` on the four declared control paths and both candidate packages.
- Twice: `git --no-optional-locks diff --quiet HEAD --` the TPC401 manuscript/code and TPC404/TPC417 manuscripts.

Narrowest next action: parent may retain this scoped proof verdict, clarify the two minor wording boundaries, and complete its separately assigned novelty and physical attachment/loss audit. **No gate reopening or new paper number follows from this result.**
