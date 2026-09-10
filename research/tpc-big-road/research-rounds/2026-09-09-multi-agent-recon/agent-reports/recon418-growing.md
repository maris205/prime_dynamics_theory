TPC_AGENT_RESULT_V1

task_id: recon418-growing  
role: tpc_source_lock  
verdict: PROPOSE_FOR_AUDIT  
location: Island 2 / image Bridge A / synthetic finite-operator branch  
files_changed: []

One candidate survives: a genuinely uniform growing-family **corollary for the exact TPC418 short-window CRT model**, including complete-shell prefixes and sufficiently long, locally renormalized coordinate prefixes. It supplies no physical credit.

### Candidate: uniform short-window growth without a bound on \(K\)

Let \(H\ge1\) be an integer, \(N=4H\), and take any finite number \(K\) of complete shells
\[
\mathcal P_j=\{p:Q_j<p\le2Q_j\},
\quad Q_j\in\mathbb Z_{\ge2},\quad 2Q_j\le Q_{j+1},
\]
with all selected primes \(p>N\). Keep TPC418’s global zero-based alternating signs and TPC417’s CRT origin.

For \(1\le k\le K\), retain the first \(k\) **complete shells**. For \(2\le R\le N\), restrict the coordinate window to \(r=0,\ldots,R-1\), recomputing its local diagonal energies; call the resulting normalized matrix \(Z_{k,R}\).

There exists an absolute \(H_0\) such that, for every \(H\ge H_0\), every admissible family and CRT origin, and every integer \(2\le R_0\le4H\),
\[
\boxed{
\sup_{\substack{1\le k\le K\\R_0\le R\le4H}}
\|Z_{k,R}\|_2
\le
\frac{2}{\sqrt{\min(H,\lfloor R_0/2\rfloor)}}
+\frac{192\log(4H)}{H}.
}
\]
There is **no upper bound on finite \(K\), \(Q_{\max}\), or the admissible origin**. In particular, the full-window bound is \(2H^{-1/2}+192\log(4H)/H\).

Source-backed ingredients are the [TPC418 parity envelope](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/PROOF_PACKAGE.md:83) and [TPC417 exact matrix/energy proof](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/PROOF_PACKAGE.md:45). The displayed uniform theorem and prefix extension are **derived here for audit**, not assertions already registered in those sources.

### Proof of the additional quantifiers

Put \(J_R=\min(H,\lfloor R/2\rfloor)\). Every row of the length-\(R\) prefix has at least \(J_R\) distances at most \(H\), so
\[
S_r^{(R)}\ge J_R/4.
\]
Its kernel row sum is at most \(4J_R\): when \(R<2H\), use \(R-1\le2J_R\); otherwise use TPC417’s two-sided bound \(4H\). Repeating its star and bulk proof therefore gives
\[
\|Z_{k,R}\|_2
\le\frac{2}{a_{\min,k}\sqrt{J_R}}
+\frac{16(3k+1)}{\lfloor L_k/2\rfloor},
\]
where \(L_k\) is the number of primes in the first \(k\) shells.

The missing growth estimate follows from the classical prime number theorem, **not a numerical extrapolation**. Selberg’s original theorem gives \(\vartheta(x)/x\to1\). Thus, for all sufficiently large \(Q\),
\[
\vartheta(2Q)-\vartheta(Q)\ge Q/2,\qquad
|\mathcal P(Q)|\ge\frac{Q}{2\log(2Q)}.
\]
This uses the eventual relative error \(1/6\) at both endpoints. [Selberg, 1949, equations (1.1)–(1.2) and §4](https://www.math.lsu.edu/~mahlburg/teaching/handouts/2014-7230/Selberg-ElemPNT1949.pdf).

A nonempty admissible shell has \(2Q\ge p>4H\), hence \(Q>2H\). Monotonicity of \(Q/\log(2Q)\) yields
\[
L_k\ge\frac{kH}{\log(4H)}.
\]
Finally, \(\lfloor L_k/2\rfloor\ge L_k/3\), \(3k+1\le4k\), and \(a_{\min,k}>1\) give the boxed bound. The prime-number-theorem threshold is absolute, independent of \(k,K,Q_j,o\); its numerical value is not pinned here.

A nonvacuous joint-growth example is
\[
H=t^2,\quad N=4t^2,\quad K=t,\quad
Q_j=2^{j+2}t^2,\quad R_0=H.
\]
Choose any admissible CRT origin \(o_t>t\). For sufficiently large integer \(t\), all shells are nonempty and the displayed supremum is \(O(t^{-1})\). Every listed parameter grows; no common origin across different \(t\) is assumed.

### Seven-field contract

1. **Literal signs, weights, masks.** Globally ordered primes have \(\epsilon_i=(-1)^i\), \(a_i=p_i^3/[Q_i^2(p_i-1)]\), and \(T_d=H^2/(H^2+d^2)\). The off-diagonal coefficient is
   \[
   T_{r-s}\sum_i\epsilon_i a_i
   [-1+\mathbf1_{p_i\mid o+r}+\mathbf1_{p_i\mid o+s}].
   \]
   Diagonal entries are zero. CRT requires \(o\equiv0\pmod{p_i}\) for even \(i\), \(o\equiv-N\pmod{p_i}\) for odd \(i\). See [TPC417 manuscript](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-417-c1-four-shell-finite-operator-bound/paper/main.tex:21). These are synthetic signs, not identified arithmetic coefficients.

2. **Physical \(h_0\) versus model index.** No physical fixed-\(h_0\) identification. \(H\) is the kernel height; \(r,s\) are window coordinates. No \(h_0=2\) claim.

3. **Domain/prefix order.** Shell prefixes follow increasing \(Q_j\); coordinate prefixes follow \(o,o+1,\ldots\). Full operator norm covers every vector. Arbitrary prime-by-prime truncations, reordered shells, and entrywise triangular masks are not claimed.

4. **Ranges.** Integer \(H\ge1\), \(N=4H\), integer \(Q_j\ge2\), ordered disjoint complete nonempty shells, \(L\ge2\), and \(p_{\min}>N\). The stronger \(N<Q_j<p\) appearing in the replay proof is unnecessary: \(p>N\) suffices for both endpoint masks and exclusion of repeated divisibility. Integer \(Q_j\) is essential to the stated \(\alpha<4\) proof; it is explicitly enforced in [TPC418 code, read only](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-418-c1-shell-parity-envelope/code/tpc418_c1_shell_parity_envelope.py:101). No physical \(X\) or physical modulus-\(q\) range is supplied.

5. **Uniformity/exceptions.** Uniform over all admissible finite families and all origins in their prescribed CRT residue class modulo \(\prod p_i\). Not uniform over arbitrary origins or arbitrary signs. Only an absolute finite initial height range is excluded asymptotically; no exceptional shells or admissible origins.

6. **Natural normalization.** For each retained shell/coordinate prefix,
   \[
   D_0=V_-S_0,\qquad
   D_r=V_-S_r+V_+(S_r-T_r^2),\quad
   Z=D^{-1/2}MD^{-1/2}.
   \]
   Here \(P_\pm=\sum_{\epsilon_i=\pm1}a_i\), \(V_\pm=\sum_{\epsilon_i=\pm1}a_i^2\), and \(S_r\) sums only over that coordinate prefix. This is the source’s local diagonal energy, not physical normalization.

7. **Loss ledger.** Star: \(2/\sqrt{J_R}\). Bulk: \(16B_*/V_-\), then shell parity, amplitude lower bound, floor loss, and shell census give \(192\log(4H)/H\). Physical identification, reassembly, selection, and physical-\(X\) losses remain missing. Strict \(1/400\): unpaid; physical fixed-power credit: zero.

### Kill tests, novelty, and strongest objection

- **Unrestricted locally renormalized prefixes fail.** At \(R=2\),
  \[
  \|Z_{k,2}\|_2=\frac{P_-}{V_-T_1}>\frac14,
  \]
  because \(a_i<4\) implies \(V_-<4P_-\). Thus \(R_0\to\infty\) is necessary for the stated uniform decay. This is a prefix-normalization obstruction, not an origin-size investigation.
- **Ambient-normalized prefixes differ.** Every principal compression of the full-window normalized matrix inherits its norm bound, including very short prefixes. One must not substitute that normalization for recomputed prefix energies.
- **Integer-scale kill test:** \(Q=13/2,p=13\) gives \(\alpha=13/3>4\).
- **Closest existing result:** TPC418 already supplies the finite envelope. The added quantifier is a supremum over unbounded finite shell families, their complete-shell prefixes, admissible origins, and growing coordinate prefixes, with one vanishing bound. Strongest objection: this is a straightforward uniform corollary plus prefix bookkeeping, **not a new cancellation mechanism or independent evidence of publication-level novelty**.
- **Parent contrast:** this requires \(p_{\min}>4H\); the parent’s proposed \(H\ge p_{\max}\) long-window regime is disjoint. Its literal-kernel bound was neither audited nor assumed here.

### Execution and preservation

Executed read-only `pwd`, `git rev-parse`, `git status`, `git diff --name-only`, `git diff --cached --name-only/--quiet`, `sha256sum`, `wc`, `sed`, `nl`, and targeted `rg` commands; all enclosing command calls exited 0. A standalone `python -B - <<'PY'` in-memory rational probe exited 0: **408 prefix cases**, heights 1–8, shell scales 32/64/128, zero failures. It checked prefix energy/kernel inequalities and the two-point identity; it was not a repository producer or theorem certificate. No jobs, builds, downloads to the repository, children, or writes.

Start/end HEAD: `ab23455ba941e5a14ded27d49de0e874aee811ac`; observed `origin/main` matches. All four control SHA256 values matched the supplied values at both checks. Status remained the same 10 tracked-dirty paths, 615 untracked files, empty index; observed status delta: none. Two full-status digests agreed:
`53b83be75bc8fe214e68ab552d645361e88e356c6913389a6df9faa4901c9782`.

No STOP, gate, paper number, or publication status was changed.
