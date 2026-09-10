TPC_AGENT_RESULT_V1

task_id: `recon-gatea-root`  
role: `tpc_source_lock`  
verdict: `ELIMINATED_SCOPED`  
location: Island 2 / image Bridge A / GateA full-shell signed fold  
files_changed: `[]`

### Result: growing arithmetic obstruction to diagonal-majorant marginal saving

One method cell is eliminated: obtaining a fixed-power improvement for the folded Möbius marginal by a nonnegative majorant that retains its literal character diagonal.

This is a quantitative strengthening of an existing V52 obstruction, not a new positive route. No GateA closure, physical cancellation theorem, or publication recommendation follows.

Let \(D_B=\mathcal D(\beta^\circ)\), where the original packet diagonal is
\[
D_B=\|\psi\|_1
\sum_{Q<q\le2Q\atop q\ {\rm prime}}
\frac{q(q-2)}{q-1}
\sum_{t\in I_x,\ q\nmid t}|\beta^\circ(t)|^2.
\]
This is exactly [V52, equation (5.1)](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md:372).

**Derived here from source-backed premises:**
\[
\boxed{\displaystyle
\liminf_{x\to\infty}
\frac{(\log x)^2D_B}{x^{5/3}}
\ \ge\ \frac94\|\psi\|_1\log\frac{27}{22}>0.}
\]

Proof:

1. Restrict the nonnegative diagonal to integers \(t=pr\), with primes
   \[
   x^{2/5}<p\le x^{9/20},
   \qquad \frac{x}{2p}<r\le\frac{x}{p}.
   \]
   For sufficiently large \(x\), \(U<p<r\), \(pr\in I_x\), and \(p,r>2Q\). Consequently every prime-shell unit mask is satisfied, the representation is unique, and there is no square contribution.

2. The literal balanced fold gives
   \[
   \beta^\circ(pr)=
   \frac{-\log r-\log p}{\log(pr)}=-1.
   \]
   No model signs or selected replacement coefficient enter this calculation. See [V51, equations (2.3)–(2.8)](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md:114) and [V52’s semiprime slice](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md:154).

3. The prime number theorem and partial summation give the count
   \[
   \begin{aligned}
   N_x
   &=\sum_{x^{2/5}<p\le x^{9/20}}
      \left[\pi(x/p)-\pi(x/(2p))\right]\\
   &\sim\frac{x}{2\log x}
      \int_{2/5}^{9/20}\frac{da}{a(1-a)}
    =\frac{x}{2\log x}\log\frac{27}{22}.
   \end{aligned}
   \]
   Uniformity requires only the ordinary PNT: all prime-counting arguments are at least \(\tfrac12x^{11/20}\), tending to infinity. The primary theorem used is Selberg’s \(\vartheta(y)\sim y\), equivalent by partial summation to \(\pi(y)\sim y/\log y\). [Selberg, *Annals of Mathematics* 50 (1949), equation (1.1), pp. 305–313](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf).

4. Another partial summation gives
   \[
   \sum_{Q<q\le2Q}\frac{q(q-2)}{q-1}
   \sim\frac{3Q^2}{2\log Q}
   =\frac{9Q^2}{2\log x}.
   \]
   Thus \(D_B\ge\|\psi\|_1N_x\sum_q q(q-2)/(q-1)\), proving the bound.

Therefore any majorant \(M_B\ge D_B\) cannot satisfy
\(M_B\ll x^{5/3-\delta+o(1)}\) for any fixed \(\delta>0\).

### Kill tests and strongest objection

- **Majorant test:** if the proposed marginal proof retains \(D_B\) positively and replaces the remaining terms by nonnegative bounds, its claimed fixed-power improvement is impossible.
- **Signed-cancellation test:** write the true energy as \(\mathcal E_B=D_B+O_B\). A genuine subdiagonal theorem must establish
  \[
  O_B=-D_B+O(x^{5/3-\delta+o(1)}).
  \]
  In particular, \(O_B/D_B\to-1\). Such signed cancellation is **not** excluded.
- **Endpoint test:** the source’s joint packet criterion remains
  \[
  \kappa+\frac{\delta_B+\delta_W}{2}>\frac1{400}.
  \]
  This obstruction disallows positive \(\delta_B\) supplied by the specified majorant method; it does not disallow a saving from the other marginal or the joint angle. [V52 endpoint law](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md:420).

The strongest objection to overinterpreting this result is decisive: **\(D_B\) is not a lower bound for the true packet energy.** V52 explicitly preserves this distinction at [lines 400–407](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md:400). Nor is this a lower bound for the signed GateA scalar.

### Closest existing attempts; novelty boundary

The closest result is [V52 §6](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_compensated_pair_dilation_and_angular_dispersion.md:475): its equal-norm fixture excludes manufacturing an angle from marginal bounds, and its diagonal-majorant warning identifies this same stopped method. The added evidence here is an explicit growing family of **actual folded coefficients**, with a positive asymptotic diagonal constant—not a new name for PAD.

V51 already excludes [orientation-first absolute reassembly](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md:357) and records the [generic-character-sieve deficit \(403/1200\)](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md:488). No new reciprocity/spectral attachment is claimed.

### Seven-field contract

1. **Literal coefficient/signs/masks.** The target remains
   \[
   \sum_{q\in\mathcal Q}q
   \sum_{\substack{s<\ell,\ s\ell,u\in I_x\\q\nmid s\ell u}}
   \Omega_U(s,\ell)w(u)K_H(u-s\ell)c'_q(u-s\ell),
   \]
   including \(u=s\ell\), with the two-branch \(\Omega_U\) above and
   \(c'_q(h)=1_{q\mid h}-1/(q-1)\). The proved obstruction concerns its literal \(\beta^\circ\)-packet diagonal.

2. **Physical shift.** \(w(u)=\Lambda(u+2)-b_x^{(z)}(u)\): physical \(h_0=2\), not a model index. The diagonal proof is independent of \(w\).

3. **Domain/order.** Full prime shell; hard \(I_x=(x/2,x]\); unordered pairs folded before transformation or absolute values. No moving-\(q\)-prefix assertion. Using the rank-two numerator through Abel still requires uniform product prefixes \(T\in[x/2,x]\): [V51 §3](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_fold_first_long_mobius_compiler.md:169).

4. **Ranges.** \(H=x^{21/32}\), \(Q=x^{1/3}\), \(U=x^{133/400}\), \(x\to\infty\); all shell primes included. \(N_x\) above is a semiprime count, not a substituted physical clock.

5. **Uniformity/exceptions.** Fixed admissible \(\psi\), \(\int\psi=1\); all sufficiently large \(x\), no exceptional moduli or metric qualification. The hybrid’s detailed \(z\)-range was not re-audited and is unnecessary for this \(\beta^\circ\)-only obstruction; no \(z\)-uniform physical theorem is asserted.

6. **Normalization.** Diagonal benchmark \(xQ^2=x^{5/3}\); the exhibited lower bound loses only \((\log x)^2\). GateA demands \(x^{1997/1200-\eta_A+o(1)}\).

7. **Loss ledger.** Credit earned: **zero**. On the selected V58 normalization, \(K_*=x^{2/3+o(1)}\), and the conditional physical margin is
   \[
   0<\eta<\min\{\eta_A,\delta_{\rm GateB}-1/400,419/2400\}.
   \]
   See [V58 Theorem 5.1](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_terminal_scalar_root_and_q_transverse_split.md:293). The alternative V43 transfer additionally retains \(19/2400\) and \(11/600-\varepsilon\); these are not extra saving credits. Both signed roots remain conjectural.

### Execution and preservation

All shell commands exited **0**: `pwd`; `cat` on required instructions and named originals; bounded `rg -n`, `rg --files`, `sed -n`, and `nl -ba … | sed -n …` source reads; `git rev-parse HEAD origin/main`; `sha256sum` on the four controls; porcelain status checks; `git diff --name-only`; `git diff --cached --name-only`; and one inline `python -B -` arithmetic probe.

The probe counted **7,296 / 560,402 / 45,166,389** eligible semiprimes at \(x=10^6,10^8,10^{10}\), respectively. Exact range/unit assertions and rational loss checks passed. These counts are diagnostics, not the asymptotic proof. No repository checker, producer, build, download, or child agent ran.

Start/end HEAD and origin/main:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

All four start/end control SHA256 values matched the supplied envelope exactly; handoff remained
`9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007`.

Status snapshots were identical: the same **10 tracked dirty paths**, **615 untracked files**, empty index; added/removed status entries `[]`. Research-lit and proof-writer guided source locking and the scoped proof; no files were written.
