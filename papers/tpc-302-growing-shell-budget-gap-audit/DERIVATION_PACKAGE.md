# TPC-302 derivation package

Let (S) be a declared finite prime shell, let (g_q) be the literal output
vector for prime (q), and let (G_{q,r}=langle g_q,g_rangle).  For a sign
vector (ain{\pm1\}^{S}), define

\[
 R(a)=\frac{a^TGa}{\operatorname{tr}G}.
\]

The identity

\[
 a^TGa=\left\|\sum_{q\in S}a_qg_q\right\|_2^2\geq0
\]

is exact.  Since (R(a)=R(-a)), fixing the first shell sign to (+1)
leaves exactly (2^{|S|-1}) global-sign classes.  The reflected Gray update
changes one sign at a time and evaluates every class exactly once after a
common positive denominator is cleared.

The source profiles are

\[
 u_z(t)=\lambda(t)-\sum_{d\leq z,,d\mid t}\mu(d),
 \qquad z\in(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61).
\]

Writing (U_k) for the first (k) columns, (A) for the physical source
operator, (V_k=A^TU_k), and (M_k=U_k^TU_k), the native budget is

\[
 B_{k,\tau}(b)=\min\{c^TM_kc:\|V_kc-b\|_2\leq\tau\|b\|_2\}.
\]

The feasible sets are nested when (\tau) is relaxed or the prefix grows;
therefore the budget cannot increase.  At one common prefix, every positive
target-independent source normalizer cancels from the weighted/positive
quotient.  The producer evaluates the frontier by a monotone ridge parameter
and records outward decimal intervals.

The 34-row grid consists of the 16 TPC-288 growth-path rows and its 18 source
controls, with 430 explicit shell targets.  All physical and profile entries
before the frontier solve are rational.
