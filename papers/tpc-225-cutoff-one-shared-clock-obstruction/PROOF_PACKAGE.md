# TPC-225 proof package

## Claim

Let \(Q\geq3\), let \(\mathcal Q_Q\) be the primes in \((Q,2Q]\), and set
\(H=4Q^2\), \(h=4Q\).  For any finite packet index set and any common
scalar \(C_h\), define

$$
 W_{q,j}(a)=C_h
 \sum_{0<|m|\leq\lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod h}.
$$

With

$$
\begin{aligned}
 E_{\rm diag}&=\sum_{q,j}\|W_{q,j}\|_2^2,&
 E_{\rm AP}&=\sum_j\left\|\sum_qW_{q,j}\right\|_2^2,\\
 E_{\rm pol}&=\sum_q\left\|\sum_jW_{q,j}\right\|_2^2,&
 E_{\rm all}&=\left\|\sum_{q,j}W_{q,j}\right\|_2^2,
\end{aligned}
$$

the exact identities

$$
 E_{\rm AP}=E_{\rm diag},\qquad
 E_{\rm all}=E_{\rm pol}
\tag{1}
$$

hold.  Consequently, whenever \(E_{\rm diag}>0\), no inequality
\(E_{\rm AP}\leq(1-\delta)E_{\rm diag}\) with \(\delta>0\) can hold on this
clock.

## Status and assumptions

The claim is **PROVABLE AS STATED** for the declared finite source-clock
theorem.  It is not an asymptotic assertion about the V46 clock, and it does
not identify \(h=4Q\) with the physical fixed atom \(h_0=2\).

- Every active \(q\) is prime and lies in \((Q,2Q]\).
- The inverse \(q^{-1}\) is taken modulo \(4Q\).
- All channels use the same residue space and the same \(C_h\).
- Real profiles are enough; complex profiles follow with squared moduli.

## Proof strategy

Reduce each row to its \(m=\pm1\) terms, prove the two-point supports are
pairwise disjoint, and apply Pythagoras first to packet sums and then to
prime-row totals.

## Proof

### Step 1: the cutoff

For every active prime,

$$
 1<\frac{hq}{H}=\frac qQ<2
$$

because the upper endpoint \(q=2Q\) cannot be prime for \(Q\geq3\).
Therefore
\[
\left\lfloor\frac{hq}{H}\right\rfloor=1,
\]
and only \(m=1\) and \(m=-1\) can contribute.

### Step 2: the two-point support

Let \(r_q=q^{-1}\pmod{4Q}\), \(t_q=Q/q\), and write

$$
 u_{q,j}=C_h\psi_j(t_q),\qquad
 v_{q,j}=C_h\psi_j(-t_q).
$$

Then

$$
 W_{q,j}=u_{q,j}e_{r_q}+v_{q,j}e_{-r_q}.
\tag{2}
$$

The two coordinates in (2) are distinct: if
\(r_q\equiv-r_q\pmod{4Q}\), then \(4Q\mid2\), which is impossible.

### Step 3: pairwise disjointness

Assume distinct active primes \(q_1,q_2\) have intersecting supports.  Then
for \(\varepsilon\in\{1,-1\}\),

$$
 q_1^{-1}\equiv\varepsilon q_2^{-1}\pmod{4Q},
 \qquad\text{so}\qquad
 q_2\equiv\varepsilon q_1\pmod{4Q}.
$$

For \(\varepsilon=1\), the difference has magnitude less than \(Q<4Q\), so
the congruence forces \(q_1=q_2\), a contradiction.  For
\(\varepsilon=-1\),

$$
 2Q<q_1+q_2\leq4Q.
$$

The sum is divisible by \(4Q\), hence it equals \(4Q\).  Since both primes
are at most \(2Q\), equality would force \(q_1=q_2=2Q\), but \(2Q\) is not
prime for \(Q\geq3\).  The supports
\(S_q=\{r_q,-r_q\}\) are therefore pairwise disjoint.

### Step 4: the AP identity

For fixed \(j\), (2) and disjointness imply

$$
 \left\|\sum_{q\in\mathcal Q_Q}W_{q,j}\right\|_2^2
 =\sum_{q\in\mathcal Q_Q}\|W_{q,j}\|_2^2.
$$

Summing this equality over \(j\) gives
\(E_{\rm AP}=E_{\rm diag}\).

### Step 5: the full/polarized identity

Set \(Y_q=\sum_jW_{q,j}\).  Every \(Y_q\) is supported on \(S_q\), so the
same disjointness gives

$$
 E_{\rm all}
 =\left\|\sum_qY_q\right\|_2^2
 =\sum_q\|Y_q\|_2^2
 =E_{\rm pol}.
$$

This proves (1).  If \(E_{\rm diag}>0\), then the first identity contradicts
any proposed strict factor \(1-\delta\) with \(\delta>0\).  The theorem is
complete.

## Affine corollary

For \(\psi_j(t)=1+s_jt\), \(t_q=Q/q\),
\(S_1=\sum_js_j\), and \(S_2=\sum_js_j^2\), substitution into (2) yields

$$
\begin{aligned}
 E_{\rm diag}=E_{\rm AP}
 &=2C_h^2\sum_q(J+S_2t_q^2),\\
 E_{\rm pol}=E_{\rm all}
 &=2C_h^2\sum_q(J^2+S_1^2t_q^2).
\end{aligned}
$$

For \(s=(0,1,-1,2)/10\), \(J=4\), \(S_1=1/5\), and \(S_2=3/50\).
These are exact rational identities, not fitted regressions.

## Corrections, scope, and open risks

- The theorem is scoped to the named cutoff-one clock.
- A clock with cutoff at least two has additional residue layers and needs a
  new collision analysis.
- The proof does not estimate prime distribution or Möbius cancellation.
- It does not transfer through an unproved physical synthesis map.
- It gives no arithmetic \(L^2\) advance, fixed-atom credit, strict
  \(1/400\) payment, or twin-prime conclusion.
