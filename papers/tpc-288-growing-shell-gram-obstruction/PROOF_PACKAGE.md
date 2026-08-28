# TPC-288 proof package

## Lemma 1 — finite operator decomposition

For every finite odd-prime shell `S`, the literal matrix is the entrywise
finite sum `A_S=sum_(q in S) A_q`.

**Proof.**  The defining summand for the frozen operator is indexed by `q`.
Partitioning that finite index set by its individual prime label gives the
identity at every `(u,t)`.  The diagonal and divisibility indicators are kept
inside each summand, so no diagonal term is reintroduced. ∎

## Lemma 2 — output and attachment decomposition

For every source vector `beta` and every linear attachment `L_w`,

```text
A_S beta = sum_q A_q beta,
L_w(A_S beta) = sum_q L_w(A_q beta).
```

**Proof.**  Apply the linear map `v -> v beta` to Lemma 1 and then use
linearity of `L_w`.  The four-block functional in the frozen engine is a sum
of a direct weighted term and three linear contrast terms, hence is linear in
`v`. ∎

## Lemma 3 — Gram positivity and energy identity

Let `g_q=A_q beta` and `G_(q,r)=sum_(u in I)g_q(u)g_r(u)`.  Then `G` is real
positive semidefinite and

```text
trace(G) = sum_q ||g_q||_2^2,
1^T G 1 = ||sum_q g_q||_2^2.
```

**Proof.**  For any real `a`, expand the square
`||sum_q a_q g_q||_2^2`; its coefficients are exactly the entries of `G`.
The two identities follow by setting `a` to the coordinate vectors and to
the all-ones vector. ∎

## Lemma 4 — modular full-rank implication

Let `M` be a rational square matrix whose entry denominators are all units in
`F_p`.  If its reduction has rank equal to its size, then `M` is nonsingular
over `Q`.

**Proof.**  Full rank modulo `p` means the reduced determinant is nonzero.
The determinant of `M` therefore has a numerator not divisible by `p`, so it
cannot be zero in `Q`. ∎

## Lemma 5 — PSD plus full rank gives a positive spectrum

If a rational Gram matrix `G` is PSD and its rational rank is its dimension,
then every real eigenvalue of `G` is strictly positive.

**Proof.**  A real symmetric PSD matrix has nonnegative eigenvalues.  Full
rank removes zero eigenvalues. ∎

## Proposition 6 — interval retention upper bound

Suppose intervals `J_q` enclose `C_q`, `J_S` encloses `C_S`, and
`m_minus=sum_q lower(|J_q|)>0`.  Then

```text
|C_S| / sum_q |C_q| <= upper(|J_S|)/m_minus.
```

**Proof.**  The numerator is at most `upper(|J_S|)`, while each denominator
term is at least `lower(|J_q|)`.  Sum the latter bounds and divide by the
positive `m_minus`. ∎

## Finite certificate consequences

The producer evaluates the exact rational outputs and interval attachments on
34 declared rows.  Lemmas 1–3 establish the identities for every row.  The
modular implementation checks the unit-denominator condition and applies
Lemma 4 to six selected aggregate physical matrices and to every output Gram
matrix.  Lemma 5 then gives a positive finite Gram spectrum on all 34 rows.
Proposition 6 and exact rational energy arithmetic certify the 13-row
intersection `R_C^+<1/10` and `R_E>1`.

These consequences are finite certificates.  None supplies a bound uniform
in a growing shell or in the literal source family.
