TPC_AGENT_RESULT_V1

task_id: `recon-distinguished-seed`  
role: `tpc_source_lock`  
verdict: `ELIMINATED_SCOPED`  
scope: Island 5 → 6, image Bridge B / dynamics-C reserve; **not repository Gate B**.  
files_changed: `[]`

### Result: same-carrier, exact-mass counterexample to metric certificates

**Eliminated candidate:** unique ergodicity, correct moving-event masses, interval variance \(O(N)\), and even an \(L^2\) maximal-discrepancy bound do **not** certify the specified seed for the declared class of moving clopen targets measurable at the original primorial levels.

This is a derived scoped theorem, not a counterexample to the unchanged arithmetic events.

Put
\[
Q_n=\prod_{p\le\sqrt{n+2}}p,\qquad
f_n(r)=\prod_{p\le\sqrt{n+2}}
  1_{p\nmid r}\,1_{p\nmid r+2},\qquad n\ge3.
\]
On \((\widehat{\mathbb Z},T(x)=x+1,\mu_{\rm Haar})\), set
\[
Z_n(x)=f_n(x+n),\quad S_N=\sum_{n=3}^NZ_n,\quad
\alpha_n=\int f_n\,d\mu,\quad A_N=\sum_{n=3}^N\alpha_n.
\]

**Source-backed premises.** CRT gives
\[
\alpha_n=\tfrac12\prod_{2<p\le\sqrt{n+2}}(1-2/p),
\qquad A_N\asymp N/\log^2N.
\]
Also \(Z_n(0)=1\) exactly when \(n,n+2\) are prime. The original resonance/Abel proof gives interval variance \(O(\text{length})\), hence Haar-a.e. recurrence. See [original metric proof, definitions and Theorems 4.1–4.2](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/README.md:5803), [TPC-1 CRT proof](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-1-two-scale-prime-sieve-correlations/main.tex:140), and [primality-exact argument](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-1-two-scale-prime-sieve-correlations/main.tex:652).

**Construction and proof.** Write \([a]_n=a+Q_n\widehat{\mathbb Z}\), \(b_n=f_n(n)\), and define
\[
\widetilde f_n
=f_n-b_n1_{[n]_n}+b_n1_{[0]_n}.
\]
When \(b_n=1\), the first cylinder lies inside the event and the second outside, because \(f_n(0)=0\). They are distinct. Therefore:

- \(\widetilde f_n\) is still a binary clopen observable at level \(Q_n\);
- its mass is **exactly** \(\alpha_n\);
- \(\widetilde f_n(n)=0\) for every \(n\ge3\);
- \(\mu(f_n\ne\widetilde f_n)=2b_n/Q_n\).

Let \(\widetilde Z_n=\widetilde f_n\circ T^n\). Then
\[
\|\widetilde Z_n-Z_n\|_2=\sqrt{2b_n/Q_n},
\qquad
K:=\sum_{n\ge3}\sqrt{2/Q_n}<\infty,
\]
since \(\log Q_n\sim\sqrt n\). Minkowski gives, uniformly over all finite integer intervals \(I\),
\[
\left\|\sum_{n\in I}(\widetilde Z_n-\alpha_n)\right\|_2
\le C\sqrt{|I|}+K.
\]
Thus the modified family retains interval variance \(O(|I|)\).

It also retains metric maximal control:
\[
\left\|\max_{3\le M\le N}
 |\widetilde S_M-S_M|\right\|_2\le K.
\]
For the original family, dyadic prefix decomposition and Cauchy–Schwarz applied to the interval-variance bound give
\[
\left\|\max_{3\le M\le N}|S_M-A_M|\right\|_2
\ll\sqrt N\log N.
\]
The modified family satisfies the same bound. It has Haar-a.e. infinite hits, while
\[
\widetilde S_N(0)=0\quad\text{for every }N.
\]

The carrier itself is uniquely ergodic: every invariant probability projects to the uniform law on every finite cyclic quotient. Finite-cylinder functions uniformly approximate continuous functions, so **every seed, including \(0\), is generic for every fixed continuous observable**. This still does not control the moving diagonal above.

**Kill test:** a proposed certificate depending only on these masses, level measurability, unique ergodicity, and metric variance/maximal bounds accepts this zero-hit family and is therefore insufficient.

### Exact sufficient lemma that survives

A usable certificate must additionally control the designated cylinder, not merely its measure.

Choose integers \(q_N\mid Q_N\), let \(U_N=q_N\widehat{\mathbb Z}\), and define
\[
V_N=\|S_N-A_N\|_2,\qquad
\Omega_N=\sup_{u\in U_N}\bigl(S_N(u)-S_N(0)\bigr).
\]
For any unbounded sequence \(N_j\), the condition
\[
\Omega_{N_j}+\sqrt{q_{N_j}}\,V_{N_j}
\le(1-\eta)A_{N_j}
\tag{*}
\]
with one fixed \(\eta>0\) implies \(S_{N_j}(0)\ge\eta A_{N_j}\to\infty\).

**Proof:** since \(\mu(U_N)=1/q_N\),
\[
S_N(0)\ge q_N\int_{U_N}S_N\,d\mu-\Omega_N
\ge A_N-\sqrt{q_N}V_N-\Omega_N.
\]
There is no exceptional-set or seed substitution.

**Attainability from existing arithmetic:** the known \(V_N\ll\sqrt N\) pays the variance term if \(q_N=o(N/\log^4N)\). But no read source supplies the required one-sided \(\Omega_N\) estimate on such coarse cylinders. At \(q_N=Q_N\), \(\Omega_N=0\), but the generic variance transfer incurs the exponential \(\sqrt{Q_N}\) loss. This is the existing [V28 full-cylinder Riesz obstruction](/root/autodl-tmp/math_research3/prime_dynamics_theory/research/tpc-big-road/bridge_b_euler_zero_axis_and_kernel_carrier.md:805), **not a new positive route**.

For the modified counterexample, coarse-cylinder averaging actually forces
\(\widetilde\Omega_N\ge A_N-\sqrt{q_N}\widetilde V_N\), exposing exactly the missing term.

### Seven-field contract

| Field | Locked content / limitation |
|---|---|
| 1. Literal coefficients | Arithmetic \(f_n\): unit-weight product of both divisibility masks above. Countermodel explicitly adds \(-b_n1_{[n]_n}+b_n1_{[0]_n}\); it is not the literal arithmetic product. |
| 2. Physical shift | \(h_0=2\), fixed throughout. \(n\) is physical integer time, not a model shift. |
| 3. Domain/prefix | Ordered cumulative prefix \(3\le n\le N\); interval bounds use consecutive integer subintervals. No block/cumulative substitution. |
| 4. Ranges | All integers \(N\ge3\); cutoff \(\sqrt{n+2}\); primes through that cutoff; \(q_N\mid Q_N\). No unrelated analytic packet \(X,N,q\) ranges imported. |
| 5. Uniformity/exceptions | Metric bounds uniform over intervals; recurrence only Haar-a.e. Lemma (*) targets exactly \(0\), along one unbounded sequence with fixed \(\eta\). |
| 6. Normalization | Haar probability \(1/Q_n\) per atom; count scale \(A_N\asymp N/\log^2N\). No logarithmic-time replacement or asserted physical ratio \(1\). |
| 7. Loss ledger | Exact lemma losses are \(\Omega_N+\sqrt{q_N}V_N\). Neither is replaced by checker credit. Analytic packet attachment absent; fixed-power credit \(0\), strict \(1/400\) unpaid. |

**Strongest objection / scope boundary:** the swap does not preserve literal sieve-product structure or target nesting. Consequently this eliminates the stated clopen/metric certificate class, not a future certificate exploiting those exact arithmetic structures.

**Closest existing results:** [TPC-1 rare-event repair theorem](/root/autodl-tmp/math_research3/prime_dynamics_theory/papers/tpc-1-two-scale-prime-sieve-correlations/main.tex:523), [V16 metric-to-seed stopped routes](/root/autodl-tmp/math_research3/prime_dynamics_theory/TPC_HANDOFF.md:45855), and V28’s kernel threshold. The additional scoped content here is the **same odometer + same levels + exactly preserved masses + maximal-control-preserving** adversary, rather than the earlier independent-Bernoulli example.

External primary check: [Haydn–Nicol–Persson–Vaienti, arXiv:1103.2113, p. 4, Proposition 1.2](https://arxiv.org/pdf/1103.2113) explicitly retains an almost-everywhere conclusion even under all-interval second-moment control. It supplies no designated-seed attachment.

### Verification and preservation

All executed shell commands exited `0`. No repository checker/producer, build, download-to-repository, synchronization, or child agent was executed. Original checker code was inspected, not run.

The exact in-memory finite check was:

```sh
python -B -c 'from math import isqrt,prod
for n in range(3,101):
 ps=[p for p in range(2,isqrt(n+2)+1) if all(p%d for d in range(2,isqrt(p)+1))]; Q=prod(ps)
 a=[int(all(r%p and (r+2)%p for p in ps)) for r in range(Q)]; b=a.copy(); h=a[n%Q]; b[n%Q]-=h; b[0]+=h
 if not (set(b)<={0,1} and sum(a)==sum(b) and b[n%Q]==0 and sum(x!=y for x,y in zip(a,b))==2*h): raise RuntimeError(n)
print("98/98 exact cylinder-swap checks; no files written")'
```

Result: `98/98`; finite algebra only, not asymptotic evidence.

Start/end checks used `git rev-parse HEAD origin/main`, `sha256sum` on the four supplied controls, `git --no-optional-locks status`, `git diff --cached --name-only`, and `git ls-files --others --exclude-standard | wc -l`.

Observed start=end:

- HEAD and origin/main: `ab23455ba941e5a14ded27d49de0e874aee811ac`.
- All four control SHA-256 values exactly match the supplied envelope, including handoff `9b5229094d55c20d6fdf5079a9ba91e4a0561fcf5505db23eb590db1090f3007`.
- Full porcelain-status SHA-256: `53b83be75bc8fe214e68ab552d645361e88e356c6913389a6df9faa4901c9782`.
- Same ten tracked dirty paths; empty index; 615 untracked files; observed status delta empty. Untracked contents were not individually hashed.

No route reopening, mathematical GO, numbering, or publication is asserted.
