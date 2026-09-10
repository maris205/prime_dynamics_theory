TPC_AGENT_RESULT_V1

task_id: `recon-physical-attachment`  
role: `tpc_source_lock`  
verdict: **PROPOSE_FOR_AUDIT — restricted finite attachment only.** Automatic transfer of the TPC417/418 saving to the full physical scalar is **ELIMINATED_SCOPED**.

Location: Islands 3/4 → 2, image Bridge A, Gate B. No gate reopening, numbering, or publication claim.

*Reissued completed result. No new research or checks were performed for this resend.*

### 1. Candidate: kernel-preserving physical restriction, with explicit norm cost

This is a new derivation from the original definitions, not an existing published theorem or arithmetic estimate.

The actual V59 lanes are
\[
\beta_x(t)=\frac{\Lambda(t)}{\log t}
-\sum_{\substack{d\mid t\\d^{400}\le x^{133}}}\mu(d),
\qquad w_x(u)=\Lambda(u+2)-b_x^{(z)}(u).
\]
They are **not** TPC353’s two components of a shifted \(\Lambda-b\) residual. [V59 definitions](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:31)

Let \(J=\{o,\ldots,o+n-1\}\subset I_x\), \(n=4H_s\), where \(H_s\) is a **proxy height**, not the physical \(H_x=x^{21/32}\). Assume the complete physical shell contains \(L\ge2\) primes \(p_i>n\), indexed from zero, and
\[
p_i\mid o\quad(i\text{ even}),\qquad p_i\mid o+n\quad(i\text{ odd}).
\]
These are the endpoint masks underlying the finite bound. [TPC417](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex:20), [TPC418](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:120)

Write
\[
a_i=\frac{p_i^3}{Q^2(p_i-1)},\quad c_i=\frac{p_i}{p_i-1},\quad
A=P_+-P_-,\quad C=\sum_i c_i,\quad C_-=\sum_{i\ {\rm odd}}c_i,
\]
where \(P_+\) and \(P_-\) sum \(a_i\) over even and odd indices.

For distinct coordinates, the **physical** restricted matrix satisfies
\[
(A_J)_{0r}=-C_-K_{H_x}(r),\qquad
(A_J)_{rs}=-C K_{H_x}(r-s)\quad(r,s\ge1).
\]
This follows directly from TPC247: no nonzero difference inside \(J\) is divisible by a shell prime. [Literal operator](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-247-literal-v59-source-operator-attachment/paper/main.tex:70)

Suppose \(A\ne0\). Set \(\lambda=\operatorname{sgn}A\), and define a real diagonal matrix \(R\) by
\[
R_{rr}=\rho=\sqrt{C/|A|}\ (r\ge1),\qquad
R_{00}=-\lambda C_-/(P_-\rho).
\]
With \(T_d=H_s^2/(H_s^2+d^2)\) and \(F_{rs}=K_{H_x}(r-s)/T_{r-s}\),
\[
\boxed{A_J=\lambda R(F\circ M)R.}
\]
Therefore the original restricted lanes satisfy
\[
\boxed{\mathfrak C_J
=\lambda\langle D^{1/2}Rw_J,\,
(F\circ Z)D^{1/2}R\beta_J\rangle.}
\]
Here \(Z=D^{-1/2}MD^{-1/2}\) uses the original proxy diagonal energies. No packet-dependent unit normalization occurs.

The kernel replacement has an explicit cost. Put \(\Gamma=\int|\psi_+(v)|\,dv\). Fourier conjugation bounds the Schur multiplier associated with \(K_{H_x}\) by \(\Gamma\). For centered coordinate matrix \(B\),
\[
((r-s)^2X_{rs})=B^2X+XB^2-2BXB.
\]
Consequently,
\[
\|F\circ Z\|
\le\Gamma\!\left(1+\frac{(n-1)^2}{H_s^2}\right)\|Z\|
<17\Gamma\|Z\|.
\]
This preserves the actual Fourier kernel without equating the heights. [Physical kernel](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:41)

**Realizable example.** Take \(x=64,Q=4,H_s=1,n=4,o=45\), with complete shell \(\{5,7\}\). Then \(5\mid45\), \(7\mid49\), and \(J=\{45,46,47,48\}\subset I_{64}\). Exact arithmetic gives
\[
\beta_J=(0,0,0,1),\quad
A=-311/192,\quad P_-=343/96,\quad C=29/12,\quad C_-=7/6,
\]
\[
\rho^2=464/311,\qquad R_{00}\rho=16/49.
\]
All 12 off-diagonal coefficient identities were checked exactly, leaving the physical kernel symbolic. This is a nonzero **input** restriction; no nonzero scalar or cancellation claim follows.

**Cost and kill tests.**

- Coverage is only **18/1,352** admissible \((q,t,u)\) triples; requiring \(\beta(t)\ne0\) gives **5/306**. These are support counts, not weighted-mass estimates.
- Uniform norm transfer pays \(\|R\|^2\ge C/|A|\). Thus
  \[
  \frac C{|A|}\frac{16|A|}{V_-}=\frac{16C}{V_-}.
  \]
  Restoring physical prime weights cancels the alternating-bulk gain in this norm-based use.
- \(A=0\) kills this diagonal attachment: model interior entries vanish, while the physical coefficient is \(-C\).
- A useful physical theorem must bound the exact weighted lanes and the signed complement \(\mathfrak C_x-\mathfrak C_J\). Neither is supplied.

### 2. Scoped elimination: source substitution and full-window attachment

**Coefficient counterexample.** At \(x=t=8192=2^{13}\), the truncated Möbius divisor sum is zero, hence physical \(\beta_x(t)=1/13\). TPC353’s model residual is zero: its comparison vanishes on even inputs, and \(8194=2\cdot17\cdot241\) is not a prime power. This coordinate lies inside its origin-8001/count-256 panel. All odd-prime input unit masks survive. Literal identification of the input sequences is therefore false—not merely unproved. [TPC353 implementation](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-353-source-native-masked-l2-polarization/code/tpc353_source_native_masked_l2_polarization.py:219), [panel](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-353-source-native-masked-l2-polarization/paper/main.tex:99)

**Same-height domain is empty.**
\[
\frac{\max q}{4H_x}\le\frac12x^{-31/96}<1,
\]
whereas TPC417/418 require every prime to exceed \(n=4H_s\). Setting \(H_s=H_x\) cannot work.

**Shortening alone does not provide coverage.** CRT requires
\[
\prod_{p\in\mathcal Q}p\mid o(o+n),\qquad \prod p\le x(x+1).
\]
For \(x\ge8\), seven selected primes \(p>x^{1/3}\) already violate this inequality. Any physical shell with at least seven primes therefore has **no** full-shell endpoint-CRT subwindow inside \(I_x\). Infinite CRT origins are not prescribed physical origins.

The separate residue-row obstruction remains TPC235’s: \(h=4LQ\) and \(H=4Q^2\) are necessary for that single-clock identification, while physical \(4Q^2/H=4x^{1/96}\). [Original proof](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-235-v59-physical-depth-crosswalk/paper/sections/3_single_clock.tex:7)

### Seven-field contract

1. **Signs/weights/masks:** Original \(\beta,w,K_{H_x}\), outer \(q\), both unit masks, and \(t\ne u\) retained. Character reassembly must subtract exactly
   \[
   \sum_q\frac{q(q-2)}{q-1}\sum_{q\nmid t}\beta(t)w(t).
   \]
   [Diagonal source](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:124)
2. **Physical shift:** \(h_0=2\) remains in \(w(u)\); neither \(H_s\), prime index, nor TPC235’s denominator \(h\) replaces it.
3. **Domain/order:** Increasing physical integer coordinates and increasing primes; restriction \(J\times J\). No moving-prefix theorem or exactly-once global cover.
4. **Ranges:** \(I_x=(x/2,x]\), \(Q=x^{1/3}\), \(H_x=x^{21/32}\); candidate additionally requires integer \(H_s\ge1\), \(n=4H_s<p_{\min}\), CRT masks, \(A\ne0\). Example \(x=64\). Admissible \(z\)-range was not recovered.
5. **Uniformity/exceptions:** Finite algebra is exact under these hypotheses; multiplier cost is explicit in \(\Gamma\). No arithmetic exceptional-set estimate or global source-uniform norm bound.
6. **Normalization:** \(D\) is proxy local diagonal energy, not physical normalization. Physical natural scale is \(xQ^2=x^{5/3}\). [Scale ledger](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_polarized_local_bdh_scalar_compiler.md:318)
7. **Loss ledger:** \(17\Gamma\), diagonal reweighting, weighted-lane norms, support complement, and any block duplication must be paid. Global \(\delta>1/400\) remains missing; fixed-power credit is zero.

**Strongest objection:** the restriction is genuinely physical and finite, but coverage and norm costs prevent transferring the saving. Closest existing results are TPC247’s attachment, TPC235’s clock obstruction, and TPC417/418’s decomposition. Additional content here is the explicit \(R\)/Schur attachment and compulsory cost—not a renamed global route.

### Preservation and execution

`files_changed=[]`; `primary_external_URLs=[]`—all invoked premises were local originals.

Original start/end HEAD and `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

All four start/end control hashes matched:

```text
AGENTS.md                  6014af5a2b1df7a4519fab48b45684c712faab4164c22f981debd5f59b7684cb
TPC_HANDOFF.md             9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007
TPC_ROUTE_MAP.md           3bbd0bcd61e9c5723d473ff89299f75ace08b91d5d4c098459aa463b26197416
PAPER_CANDIDATE_LEDGER.md   e6da1b785a41397e5b0d6a0fc22f57b00901581c6a0a72ecd3f94b0a1abc8526
```

Original scout receipt: empty index, unchanged 10 tracked-dirty paths, unchanged 615 untracked paths, status delta none.

Subsequent preservation-only check verified **617** untracked paths, with exactly the authorized parent additions `PROOF_PACKAGE.md` and `DERIVATION_PACKAGE.md`, no removals, and unchanged controls/HEAD/index. Neither draft was read or used as theorem evidence.

Executed scoped `sed`, `nl -ba`, `rg`, `wc -l`, `sha256sum`, read-only Git status/diff/rev-parse commands, and two standalone `python -B -` in-memory arithmetic probes. All command blocks exited **0**. No producer, repository checker, build, download, child, or external-review call was executed.
