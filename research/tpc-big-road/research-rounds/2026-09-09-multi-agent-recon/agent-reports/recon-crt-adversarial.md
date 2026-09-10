TPC_AGENT_RESULT_V1

task_id: `recon-crt-adversarial`  
role: `tpc_proof_auditor`  
verdict: `ELIMINATED_SCOPED`  
location: Island ② / image Bridge A / Gate-B model-transfer boundary  
files_changed: `[]`

## Result: one normalized kill test

A sign-agnostic extension of the short-window proxy cannot promise uniform decay: a declared nonalternating sign law gives
\[
\boxed{\|Z\|_2>1/512}
\]
after the actual local diagonal normalization. This holds at both its CRT origin and the bounded origin \(o=1\). It does **not** contradict TPC418’s alternating-sign theorem or establish anything about the physical arithmetic signs.

**Source-backed premises.** The literal short-window component and general signed identity are in [TPC401, main.tex:34](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-401-c1-diagonal-deletion-decomposition/paper/main.tex:34) and [TPC402, main.tex:27](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-402-c1-signed-diagonal-term-audit/paper/main.tex:27). Local energy normalization is defined in [TPC404, main.tex:25](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-404-c1-local-normalization-boundary/paper/main.tex:25). The CRT endpoint/interior decomposition is in [TPC417, main.tex:20](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex:20).

**New derivation, not an existing certified result.** Take integers
\[
H\ge2,\quad N=4H<Q,\quad
\{p_0<\cdots<p_{L-1}\}=\{p:Q<p\le2Q\},\quad L\ge10.
\]
Set \(a_i=p_i^3/[Q^2(p_i-1)]\), and prescribe
\[
\sigma_0=-1,\qquad \sigma_i=+1\quad(i\ge1),\qquad
A=\sum_i\sigma_i a_i,\quad V=\sum_i a_i^2.
\]
For integer \(Q\), \(1<a_i<4\), hence
\[
A>L-5\ge L/2,\qquad V<16L.
\]
The amplitude bounds are proved in [TPC418, main.tex:30](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/paper/main.tex:30).

Use either:

- **CRT profile:** \(o\equiv0\pmod{p_i}\) for \(i\ge1\), and \(o\equiv-N\pmod{p_0}\).
- **Bounded profile:** \(o=1\), so every selected prime is a unit throughout \(I_o\).

For interior offsets \(1\le r,s<N\), \(r\ne s\), both profiles have
\[
M_{rs}=-AT_{r-s},\qquad T_d=\frac{H^2}{H^2+d^2}.
\]
Let \(D_r=G(o+r)>0\), with \(G\) the literal masked sum of component row squares. In either profile,
\[
D_r\le V S_r,\qquad S_r=\sum_{s\ne r}T_{r-s}^2\le4H.
\]
Indeed, \(T_d^2\le T_d\), and splitting the one-sided sum at \(H\) gives \(\sum_{d\ge1}T_d\le2H\).

For \(Z=D^{-1/2}MD^{-1/2}\), choose \(x_r=\sqrt{D_r}\) on \(1\le r\le H\), zero elsewhere. Since \(T_{r-s}\ge1/2\) on this block,
\[
\begin{aligned}
\|Z\|_2
&\ge\frac{|x^\top Zx|}{x^\top x}\\
&=\frac{A\sum_{\substack{1\le r,s\le H\\r\ne s}}T_{r-s}}
        {\sum_{r=1}^{H}D_r}
\ge\frac{A(H-1)}{8HV}
\ge\frac{A}{16V}
>\frac1{512}.
\end{aligned}
\]

**Kill test:** reject any proposed arbitrary-sign short-window bound whose claimed right-hand side is below \(1/512\) on this family. This tests a normalized full-operator assertion, not TPC403’s raw scalar ratio.

## CRT origin budget and the physical clock

For any prescribed positive/negative CRT partition, write
\[
R_+=\prod_{\sigma_p=+1}p,\qquad R_-=\prod_{\sigma_p=-1}p.
\]
The construction requires
\[
R_+\mid o,\qquad R_-\mid o+N.
\]
Thus, for **positive** origins,
\[
o\ge R_+,\qquad o+N\ge R_-,\qquad
Q^L<R_+R_-\le o(o+N).
\]

Consequently, an additional physical-origin contract \(1\le o\le X\) forces
\[
R_+\le X,\quad R_-\le X+N,\quad
L<\frac{\log[X(X+N)]}{\log Q}.
\]
For the original alternating construction, \(o>Q^{\lceil L/2\rceil}\). For the one-negative construction above,
\[
\boxed{Q^{L-1}<o_{\rm CRT}<(2Q)^L}.
\]
The upper bound follows from its least positive CRT representative modulo \(\prod p\).

If a proposed transfer additionally requires \(N\le X\) and \(Q\ge X^\theta\), then
\[
L<2/\theta+\frac{\log2}{\log Q}.
\]
These are **conditional clock restrictions**, not a claim that those physical parameter relations have already been sourced. They prevent silently placing a many-prime CRT construction inside that bounded-origin clock. TPC403 itself only asserts an unbounded origin class: [main.tex:32](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-403-c1-crt-origin-proxy-obstruction/paper/main.tex:32), with its bounded-origin disclaimer at line 78.

The distinction matters: the dense CRT mask is astronomical, but the **synthetic sign-imbalance obstruction** also occurs at \(o=1\). Small origins alone therefore do not repair an arbitrary-sign assertion.

## Seven-field contract

1. **Signs, weights, masks:** exactly the \(\sigma_i,a_i,T_d\) above, and
   \[
   K_p(u,v)=p(p/Q)^2T_{u-v}
   \left(\mathbf1_{p\mid u-v}-\frac1{p-1}\right)
   \mathbf1_{u\ne v}\mathbf1_{p\nmid u}\mathbf1_{p\nmid v},
   \quad M=\sum_p\sigma_pK_p.
   \]
   Source: TPC401/402. The new sign law is synthetic, not arithmetic.

2. **Physical \(h_0\):** not identified. \(H\) is kernel height; \(r,s\) are model offsets. Neither is physical fixed \(h_0=2\).

3. **Domain/prefix order:** complete single shell, increasing prime order, zero-based sign index; complete window \(I_o\), increasing integer offsets. Witness block \(r=1,\ldots,H\) belongs to that same window. No cumulative-prefix identification is supplied.

4. **Ranges:** integers \(H\ge2,N=4H<Q\), \(L\ge10\). Physical \(X\), modulus \(q\), and their joint ranges are missing. The origin-cap implications above explicitly add their own assumptions.

5. **Uniformity/exceptions:** the lower bound holds for every admissible tuple and both stated profiles, with constant \(1/512\); no exceptional set. It is not a metric-to-designated-seed result.

6. **Normalization:** \(G(u)=\sum_p\sum_vK_p(u,v)^2\), \(D=\operatorname{diag}G\), \(Z=D^{-1/2}MD^{-1/2}\). Dimensionless model operator norm; physical natural-scale identification remains missing.

7. **Loss ledger:** exact algebra and normalization introduce no estimation loss beyond the displayed constants. Physical attachment, cover, weights, reassembly, tails, and exponent conversion remain unpaid. Physical fixed-power credit \(=0\); strict \(1/400\) is not established.

## Surviving domain, objection, and long-window boundary

The strongest objection is decisive: this changes the alternating sign law. It does not refute TPC418. A possible surviving domain retains source-valid alternating/balanced signs, bounded origins, and a proved common-clock attachment. On the no-mask subclass, \(|A|/V\to0\) is necessary for norm decay; it is not asserted sufficient generally.

The closest existing result is TPC417’s endpoint/interior decomposition plus TPC418’s alternating scalar envelope. The additional content here is the normalized bulk lower bound and quantitative origin exclusion—not a renamed TPC403 route.

For the parent’s long-window task, CRT divisibility constraints survive, but this matrix proof does not. Once \(N\ge p\), masks recur, \(r\equiv N\pmod p\) can occur internally, and active off-diagonal multiples of \(p\) restore the term
\[
+(p-1)a_pT_{u-v}\mathbf1_{p\mid u-v}
\]
inside the unit masks. Both the reduced matrix and its short-window energy formulas cease to apply. No conclusion about the parent’s long-window bound is drawn.

## Execution and preservation

An independent in-memory `python -B -` rational probe checked \((Q,H)=(64,2),(64,8),(256,8)\), both profiles: **4,080 literal entries and 144 energy rows passed; exit 0**. Witness Rayleigh quotients ranged approximately \(0.160\)–\(0.265\). No repository producer/checker was executed.

Read commands (`cat`, specified `sed`, `nl -ba`, targeted `rg`) all returned 0. Read scope: required controls, six original manuscripts, and TPC404/TPC417 independent-checker sources. The proof-writer skill guided assumption checking; its writing step was suppressed.

Start/end checks—`git rev-parse HEAD origin/main`, `sha256sum` on the four supplied controls, `git --no-optional-locks status --porcelain=v1 --untracked-files=all`, and `git diff --cached --name-only`—all exited 0. End `git diff --name-only` also exited 0.

HEAD and origin/main remained `ab23455ba941e5a14ded27d49de0e874aee811ac`. All four control SHA256 values matched the supplied hashes at both observations. Exact status text was unchanged: 10 tracked dirty paths, 615 untracked paths, empty index. `status_delta=[]`.

`primary_external_URLs=[]`; existing originals sufficed. No writes, children, synchronization, publication, or mathematical GO.
