# TPC-303 derivation package

For a positive budget sequence represented by outward intervals
(B_j\in[L_j,U_j]),

\[
 U_{j+1}<L_j \Longrightarrow B_{j+1}<B_j,
 \qquad L_{j+1}>U_j \Longrightarrow B_{j+1}>B_j.
\]

These implications are exact order statements and require no probabilistic or
asymptotic assumption.  A single first implication refutes a claim that the
budget is nondecreasing on the finite path.  It does not refute a lower bound
of the form (B_j\geq C m_j^\alpha) at sufficiently large (m_j).

TPC-302 supplies, for each row and tolerance, a common-prefix budget interval
for each of

\[
 N_\beta=\|\beta\|_2^2,\qquad
 N_{\rm mean}=\operatorname{tr}(M_k)/k,\qquad
 N_{\rm first}=M_k[1,1].
\]

On the fixed-source spine, compare adjacent (Q)-values.  The shell
cardinalities are (10,13,15,17), but the shells themselves move; hence the
statement being tested is cardinality-only monotonicity, not monotonicity under
set inclusion.  A transition with equal (k) is labeled same-prefix and
isolates the shell/target change from a change in profile dimension.
