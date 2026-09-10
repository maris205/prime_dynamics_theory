TPC_AGENT_RESULT_V1

task_id: `physical-loop-finite-attachment-audit`  
role: `tpc_proof_auditor`  
mode: `READ_ONLY_RESEARCH_AND_AUDIT`  
verdict: **Finite attachment survives with an orientation correction and explicit hypotheses. Physical transfer remains STOP_SCOPED; no GO.**  
files_changed: `[]`  
primary_external_URLs: `[]` — only supplied local sources and direct derivations were used.

### 1. First fatal mismatch: the displayed upper-star entry

**Source:** TPC247 defines row \(u\), column \(t\) using \(K_H(u-t)\), with conjugate-linear first Hilbert slot; neither symmetry nor Hermiticity is assumed. [TPC247, main.tex:62](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:62)

Consequently, the [prior attachment report:38](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-physical-attachment.md:38) must read, for \(r\ge1\),
\[
(A_J)_{0r}=-C_-K_{H_x}(-r),\qquad
(A_J)_{r0}=-C_-K_{H_x}(r).
\]
Its interior formula
\[
(A_J)_{rs}=-C K_{H_x}(r-s)\quad(r,s\ge1,\ r\ne s)
\]
is correct. Replacing \(K(-r)\) by \(K(r)\) requires evenness. Real \(\psi_+\) alone gives conjugate symmetry, not evenness.

**Derived correction:** The report’s later definition
\[
F_{rs}=K_{H_x}(r-s)/T_{r-s}
\]
already has the correct orientation. With its \(A\ne0\), \(\lambda=\operatorname{sgn}A\), and diagonal \(R\),
\[
\lambda R_{rr}^{\,2}(-A)=-C\quad(r\ge1),\qquad
\lambda R_{00}R_{rr}P_-=-C_-.
\]
These verify both star directions and every interior entry; the diagonals remain zero. Thus
\[
A_J=\lambda R(F\circ M)R
\]
and the stated real-lane pairing
\[
\mathfrak C_J
=\lambda\left\langle D^{1/2}Rw_J,\,
(F\circ Z)D^{1/2}R\beta_J\right\rangle
\]
are correct after fixing the displayed upper-star entry. No conjugation of \(F\) is needed. For an unconjugated complex \(w\), replace the first lane by \(\overline w\), as TPC247 specifies.

### 2. Schur multiplier and reweighting costs

**Source:** The Fourier convention is
\[
K_{H_x}(d)=\int\psi_+(v)e(-vd/H_x)\,dv.
\]
[Scalar compiler:41](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:41)

**Derivation:** Assume \(\psi_+\in L^1\), and set \(\Gamma=\|\psi_+\|_1\). For
\[
U_v=\operatorname{diag}_r e(-vr/H_x),
\]
the kernel Schur map is \(\int\psi_+(v)U_vYU_v^*\,dv\), so its operator-norm bound is \(\Gamma\), even for complex/non-even kernels.

Let \(B=\operatorname{diag}(r-(n-1)/2)\). Then
\[
((r-s)^2Y_{rs})=B^2Y+YB^2-2BYB,
\]
whose norm is at most \((n-1)^2\|Y\|\). Since \(n=4H_s\),
\[
\|F\circ Z\|
\le\Gamma\left(1+\frac{(n-1)^2}{H_s^2}\right)\|Z\|
<17\Gamma\|Z\|.
\]
The last strict comparison holds here because \(Z\ne0\). This argument never equates \(H_s\) with \(H_x\). Uniformity across a family requires a uniform bound on \(\Gamma\).

The exact diagonal-reweighting norm is
\[
\|R\|^2=
\max\left\{\frac C{|A|},
\frac{C_-^2|A|}{P_-^2C}\right\}.
\]
Therefore a transfer using uniform lane bounds necessarily incurs at least \(C/|A|\), and
\[
\frac C{|A|}\frac{16|A|}{V_-}=\frac{16C}{V_-}.
\]
The alternating-bulk \(|A|\) gain disappears in **this norm-based transfer**. This is not a universal impossibility theorem for source-aware weighted estimates. The finite proxy bound being used is [TPC417, main.tex:35–57](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex:35).

### 3. Degeneracies and diagnostic limits

**Correction to the \(A=0\) warning:** If \(A=0\), the model interior vanishes. Diagonal reweighting and Schur multiplication cannot create a nonzero physical interior entry from it. Thus this attachment fails **provided some corresponding \(K_{H_x}(r-s)\ne0\)**. It does not rule out other representations or direct finite norm bounds.

Moreover, for the report’s single complete shell, \(a_i\) is strictly increasing: pairing adjacent terms gives \(A<0\) for even \(L\), \(A>0\) for odd \(L\). Hence \(A=0\) does not occur in that particular domain; the warning concerns an enlarged family.

For \(L\ge2\), \(D>0\), and under \(A\ne0\), \(R\) is invertible. Therefore the weighted input lane vanishes exactly when \(\beta_J=0\). A nonzero \(\beta_J\) still establishes neither a nonzero fully weighted off-diagonal summand nor a nonzero scalar. The supplied scope does not recover \(b_x^{(z)}\)’s full definition/range or certify \(w_J\).

**Exact in-memory diagnostics, not arithmetic evidence:**

- At \(x=64,\ J=\{45,46,47,48\}\), all 12 oriented off-diagonal identities passed.
- A formal complex/non-even kernel \(K(d)=1+id\) exposes the erroneous upper-star sign. This tests algebra, not the physical Fourier kernel.
- All 16 centered-commutator entries passed.
- \(\beta_J=(0,0,0,1)\).
- Support counts reproduce \(18/1352\), and \(5/306\) after requiring \(\beta(t)\ne0\); neither count uses \(w\)-weighted mass.
- At \(t=x=8192\), physical \(\beta=1/13\), while TPC353’s shifted residual is zero because its comparison vanishes on even inputs and \(8194=2\cdot17\cdot241\). Literal substitution is false. [TPC353 code:219](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-353-source-native-masked-l2-polarization/code/tpc353_source_native_masked_l2_polarization.py:219), [code:234](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-353-source-native-masked-l2-polarization/code/tpc353_source_native_masked_l2_polarization.py:234)

### 4. Physical CRT no-cover obstruction: verified

For integer \(o,n\), \(J\subset I_x\) implies
\[
0<o,\qquad o+n-1\le x,\qquad o+n\le x+1.
\]
Endpoint divisibility by distinct shell primes therefore requires
\[
P:=\prod_{p\in\mathcal Q}p\mid o(o+n),
\qquad P\le o(o+n)\le x(x+1).
\]
If seven selected primes exceed \(x^{1/3}\), then
\[
P>x^{7/3}=x^2x^{1/3}>x^2(1+1/x)=x(x+1)
\]
for \(x\ge8\), since \(x^{1/3}\ge2>1+1/x\).

Thus **no such full-shell endpoint-CRT window exists when the physical shell contains at least seven primes**. Unbounded CRT origins do not supply an origin inside \(I_x\).

Also,
\[
\frac{\max q}{4H_x}\le\tfrac12x^{-31/96}<1,
\]
so identifying \(H_s=H_x\) contradicts the required \(n=4H_s<p_{\min}\). These verify the obstructions at [prior report:97–107](/root/autodl-tmp/math_research3/prime_dynamics_theory/research-rounds/2026-09-09-multi-agent-recon/agent-reports/recon-physical-attachment.md:97). TPC235’s separate residue-clock assertion was not used.

### 5. Physical contract and no-GO boundary

- **Literal object:** retain \(\beta=\Lambda/\log-\sum_{d^{400}\le x^{133}}\mu(d)\), \(w=\Lambda(\,\cdot+2)-b_x^{(z)}\), outer \(q\), both unit masks, \(t\ne u\), and \(K(u-t)\). Character reassembly subtracts exactly \(\sum_q q(q-2)/(q-1)\sum_{q\nmid t}\beta(t)w(t)\). [Compiler:53](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:53), [compiler:124](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:124)
- **Shift/domain/order:** \(h_0=2\); \(X=x\), \(I_x=(x/2,x]\cap\mathbb Z\), physical cardinality \(\lfloor x\rfloor-\lfloor x/2\rfloor\). Proxy \(N=n=4H_s\), integer \(H_s\ge1\), \(n<p_{\min}\), \(L\ge2\). Coordinates and primes increase in their original order. No moving-prefix or exactly-once full-cover theorem follows.
- **Ranges/uniformity:** \(Q=x^{1/3}\), \(q\in(Q,2Q]\) prime, \(H_x=x^{21/32}\). The \(z\)-range and arithmetic exceptional quantifiers remain unrecovered.
- **Normalization/budget:** proxy \(D\) is not physical normalization. Natural local/global scales are \(Q^2H_x=x^{127/96}\) and \(xQ^2=x^{5/3}\). Multiplier, reweighting, exact weighted lanes, uncovered terms, tails, prefixes, and block-copy costs remain payable. Required \(\delta>1/400\); the source benchmark \(\delta=1/96\) gives numerator \(x^{53/32+o(1)}\), output \(x^{95/96+o(1)}\), and margin \(19/2400\). The terminal saving must remain below \(\min(\eta_A,\delta-1/400,419/2400)\). None is earned here. [Compiler:318](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:318), [compiler:386](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:386)

**Strongest objection:** this CRT family cannot cover the physical shell once it has seven primes; even a realizable small restriction has unpaid weights and normalization.

**Closest existing results:** TPC247’s exact physical-index attachment and copy-norm obstruction; TPC417/418’s finite endpoint/interior decomposition. Location: islands 3/4 → 2, image Bridge A, Gate B. TPC418 remains the formal endpoint; no gate closure, numbered writer, arithmetic advance, or fixed-power credit.

### 6. Preservation and execution receipt

Start/end `HEAD` and local `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

Start/end control SHA256 values were identical:

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

All six allowed source-file hashes also remained unchanged. Status: **10 tracked-dirty, 631→633 untracked, empty index throughout**. The only additions were authorized parent files `AUTO_REVIEW.md` and `REVIEW_STATE.json`; no removals or unexplained status changes.

Commands included `git rev-parse HEAD refs/remotes/origin/main`, `git --no-optional-locks status --porcelain=v1 --untracked-files=all`, `git diff --name-only`, `git diff --cached --name-only`, explicit-path `sha256sum`, scoped `sed`/`nl -ba`/`rg`/`wc`, and one standalone `python -B -` in-memory diagnostic. **Every command exited 0.** No repository program, build, regeneration, synchronization, download, child agent, credential inspection, or external-model call ran.

The `proof-writer` skill guided the corrections and boundary-case audit; its writing step was overridden by the read-only task.
