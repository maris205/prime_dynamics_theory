TPC_AGENT_RESULT_V1

task_id: recon-shortwindow-proof-audit  
role: tpc_proof_auditor  
verdict: **VERIFIED_SCOPED_CANDIDATE — NOT publication GO**  
location: Island 2 / image Bridge A / synthetic finite-operator branch  
files_changed: []

The boxed eventual-uniform theorem is correct under the candidate’s complete, nonempty, integer-scale shell contract. Two details should be made explicit: choose \(H_0\) to ensure every shell prefix has at least two primes, and retain the exterior CRT endpoint \(N=4H\) when shortening the coordinate window. Neither requires weakening the eventual theorem.

### Proof verification

**1. Literal masks, signs, and coordinate restriction.**

For an even-index prime, \(o+r\equiv r\pmod p\); because \(0\le r<R\le N<p\), its divisibility indicator is exactly \(\mathbf1_{r=0}\).

For an odd-index prime,
\[
o+r\equiv r-N\pmod p,\qquad -p<-N\le r-N\le-1.
\]
Thus its indicator vanishes throughout every prefix, including \(R<N\). The endpoint remains \(o+N\), not \(o+R\). Distinct window coordinates cannot both be divisible by a selected prime.

Consequently the candidate’s literal coefficient gives
\[
M_{0r}=P_-T_r,\qquad M_{rs}=-AT_{r-s}\quad(r,s\ge1,\ r\ne s),
\]
with zero diagonal. Recomputing the unsigned component energies on precisely \(0,\ldots,R-1\) gives
\[
D_0=V_-S_0^{(R)},\qquad
D_r=V_-S_r^{(R)}+V_+\bigl(S_r^{(R)}-T_r^2\bigr).
\]
These agree with the [TPC417 original identities](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/PROOF_PACKAGE.md:45). The source’s stronger replay inequality \(N<Q_j<p\) is unnecessary here: \(p>N\) suffices.

**2. Counting and kernel bounds, including odd \(R\).**

One side of row \(r\) contains at least
\[
\max(r,R-1-r)\ge\lfloor R/2\rfloor
\]
coordinates. Hence at least \(J_R=\min(H,\lfloor R/2\rfloor)\) terms have distance at most \(H\), proving \(S_r^{(R)}\ge J_R/4\).

For \(R<2H\), the kernel row sum is at most
\[
R-1\le2\lfloor R/2\rfloor=2J_R\le4J_R.
\]
For odd \(R\), the first inequality is equality. For \(R\ge2H\), \(J_R=H\), and the source’s two-sided tail estimate gives \(4H=4J_R\). No boundary failure occurs at \(R=2H\).

**3. Normalized operator bound.**

Write \(m=\lfloor L_k/2\rfloor\ge1\). Positivity follows from \(D_r\ge V_-J_R/4>0\). The star satisfies
\[
\|q\|_2^2
=\frac{P_-^2}{V_-S_0^{(R)}}\sum_{r=1}^{R-1}\frac{T_r^2}{D_r}
\le\frac{4P_-^2}{V_-^2J_R}
\le\frac4{a_{\min,k}^2J_R}.
\]
Here the local sum \(\sum_{r=1}^{R-1}T_r^2=S_0^{(R)}\) is exact.

The symmetric bulk has absolute row sums at most
\[
\frac{4|A_k|}{V_-J_R}(4J_R)=\frac{16|A_k|}{V_-}.
\]
TPC418’s corrected actual block sign
\(\sigma_j=\epsilon_j(-1)^{n_j+1}\), rather than \(\epsilon_j\) alone, gives
\[
|A_k|\le B_{*,k}<3k+1.
\]
Its amplitude argument is valid for integer \(Q_j\ge2\): \(1<a_i<4\). These steps were checked against the [original parity proof](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:67).

The first \(k\) complete shells preserve the original global indices and signs. Therefore
\[
\|Z_{k,R}\|_2
\le\frac2{a_{\min,k}\sqrt{J_R}}
+\frac{16(3k+1)}{\lfloor L_k/2\rfloor}.
\]

**4. Absolute PNT threshold and the singleton-prefix issue.**

The imported premise is valid: Selberg proves \(\vartheta(x)/x\to1\). The following shell census is our consequence of that theorem, not a quoted explicit estimate. [Selberg, 1949, equations (1.1)–(1.2), §4](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf).

Choose an absolute \(x_*\) such that
\[
|\vartheta(x)-x|\le x/6\qquad(x\ge x_*).
\]
Choose an integer \(H_0\ge8\) with \(2H_0\ge x_*\). Each nonempty admissible shell has \(Q_j>2H\), so both PNT endpoints exceed the same threshold. Thus
\[
\vartheta(2Q_j)-\vartheta(Q_j)
\ge(5/6)2Q_j-(7/6)Q_j=Q_j/2,
\]
and, since \(Q/\log(2Q)\) is increasing for \(Q\ge2\),
\[
n_j\ge\frac{Q_j}{2\log(2Q_j)}
\ge\frac H{\log(4H)},\qquad
L_k\ge\frac{kH}{\log(4H)}.
\]
For \(H\ge H_0\), \(H/\log(4H)\ge2\), ensuring \(L_k\ge2\), including \(k=1\).

This qualification matters: at \(H=1\), shells \(Q_1=3,Q_2=6\) have primes \(\{5\},\{7,11\}\). The full pool satisfies \(L\ge2\), but its first shell has \(V_-=0\), making \(D^{-1/2}\) undefined. Accordingly, the preliminary definition must not claim all prefixes are normalized for every \(H\ge1\). The eventual theorem already excludes this problem through \(H_0\).

Now \(\lfloor L_k/2\rfloor\ge L_k/3\) and \(3k+1\le4k\) yield
\[
\frac{16(3k+1)}{\lfloor L_k/2\rfloor}
\le\frac{192\log(4H)}H.
\]
Together with monotonicity of \(J_R\), this proves the boxed supremum. The threshold has no dependence on \(k,K,Q_j\), or \(o\). CRT translation makes the matrices identical for all admissible origins; no common origin across different families is required.

The proposed \(H=t^2,K=t,Q_j=2^{j+2}t^2,R_0=H\) example is admissible eventually and gives \(O(t^{-1})\).

### Prefix obstructions and normalization distinctions

At \(R=2\), both diagonals equal \(V_-T_1^2\), so exactly
\[
\|Z_{k,2}\|_2=\frac{P_-}{V_-T_1}>\frac14.
\]
The strict inequality follows from \(V_-<4P_-\) and \(T_1<1\).

Strictly speaking, this example alone excludes \(R_0=2\), not every bounded \(R_0\). The broader necessity assertion is also correct: using \(P_->m\), \(V_-<16m\), \(V_-+V_+<16L_k\), and \(S_r\le R-1\),
\[
\|Z_{k,R}\|_2\ge |Z_{01}|
\ge\frac{T_1}{16\sqrt3(R-1)}
\ge\frac1{32\sqrt3(R-1)}.
\]
Thus any bounded subsequence of \(R_0\) prevents uniform decay.

Ambient-normalized principal compressions do inherit the full-window bound. They are different matrices from locally renormalized prefixes. The noninteger-scale counterexample \(Q=13/2,p=13\), giving \(a=13/3>4\), is also correct.

### Seven-field contract and claim ceiling

1. **Coefficient:** precisely the stated alternating synthetic signs, amplitudes, kernel, divisibility masks, and zero diagonal; no arithmetic-sign identification.
2. **Fixed physical \(h_0\):** absent; \(H\) is kernel height, not \(h_0=2\).
3. **Domain/order:** initial complete-shell prefixes and anchored coordinate prefixes; no arbitrary truncation, reordering, or triangular masking claim.
4. **Ranges:** \(H\ge H_0\), \(N=4H\), integer ordered complete nonempty shells, \(p_{\min}>N\), and \(2\le R\le N\).
5. **Uniformity:** all finite admissible families and prescribed CRT origins, with one absolute threshold; not arbitrary signs or origins.
6. **Normalization:** freshly computed component diagonal energies on each retained domain, not physical normalization.
7. **Losses:** star \(2/\sqrt{J_R}\), bulk \(192\log(4H)/H\); physical identification, reassembly, selection, and physical-\(X\) losses remain unpaid. Strict \(1/400\) unpaid; physical fixed-power credit zero.

**Correctness versus novelty:** this is a genuine uniform *vanishing corollary*, not merely a numerical replay. However, TPC418 already quantifies over arbitrary finite shell families; unbounded finite \(K\) is not itself a newly discovered cancellation quantifier. The substantive addition is eliminating family dependence via a classical shell census and extending the energy bookkeeping to coordinate prefixes. Publication-level novelty is unestablished. Its scoped value is clarifying the uniform consequence and the short-prefix obstruction.

**Strongest overclaim risk:** presenting this synthetic corollary as a new cancellation mechanism, a physical growing theorem, or authority to reopen a Gate or assign a paper number. None follows. The parent long-window draft was neither read nor audited.

### Execution and preservation

Read: entire repository AGENTS.md, island-map guide, proof-writer skill, handoff lines 1–220 and 855–908, both original proof packages and manuscripts, and relevant TPC418 code definitions.

Commands actually run:

- `pwd`, `cat`, `wc -l`, `sed -n`, `nl -ba`, targeted nested-AGENTS existence checks, and `sha256sum`: exit 0.
- `rg -n '^#{1,6}.*(855|908)|§(855|908)' TPC_HANDOFF.md`: exit 1, no matching section labels; subsequently read the requested line range.
- `git --no-optional-locks` with `rev-parse HEAD origin/main`, `status --short --untracked-files=all`, `diff --name-only`, `diff --cached --name-only`, `diff --cached --quiet`, and targeted `diff --exit-code HEAD -- …`: exit 0.
- `git … status --short --untracked-files=all | sha256sum`: exit 0.
- Two standalone `python -B - <<'PY'` exact in-memory diagnostics: first exit 1 on the singleton-prefix fixture; revised domain-aware run exit 0. It checked 1,176 geometry prefixes, 39,776 rows, 12 CRT families, 465 nondegenerate shell/coordinate prefixes, and 8,500 literal off-diagonal pairs; one degenerate prefix was explicitly classified and excluded. These are diagnostics, not proof certificates.
- Primary-source web opening and screenshot requests; no repository download.

Start/end HEAD and observed `origin/main`:
`ab23455ba941e5a14ded27d49de0e874aee811ac`.

All four supplied control hashes matched at both checks. Handoff SHA256:
`9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007`.

The five inspected TPC417/418 original files and map guide retained their hashes and matched HEAD. Full status was byte-identical: the expected 10 tracked-dirty paths, 617 untracked files, empty index. Status SHA256:
`ca8995caf3df79954f955e0d0f10219dc18eb6cf9154d08fe8185ac925d6816a`.

status_delta: none observed. No full-corpus content-hash audit claimed. No children, writes, producers, builds, synchronization, publication, or gate changes.
