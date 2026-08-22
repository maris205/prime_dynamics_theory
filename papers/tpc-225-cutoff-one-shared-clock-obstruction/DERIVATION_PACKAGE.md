# TPC-225 derivation package

## Target

Determine whether the TPC-224 source-surrogate clock
\(x=Q^3,\ H=4Q^2,\ h=4Q\) can produce a prime-label AP marginal saving for
the literal row family, with the same packet profiles and normalization used
in the preceding audit.

## Status

**PROVED_STRUCTURAL_L1 / STOP_SCOPED_FOR_THE_CUTOFF_ONE_CLOCK**

The cutoff-one identity and the resulting orthogonality are exact.  The
conclusion is restricted to this named finite growing clock; it is not an
asymptotic statement about the physical V46 object.

## Invariant object

Let \(Q\geq3\), let \(\mathcal Q_Q\) be the primes in \((Q,2Q]\), and set
\(C_h=1/h\).  The invariant finite family is

$$
 W_{q,j}(a)=C_h
 \sum_{0<|m|\leq\lfloor hq/H\rfloor}
 \psi_j\!\left(\frac{Hm}{hq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod h}.
$$

All energies are formed from this same family:

$$
\begin{aligned}
 E_{\rm diag}&=\sum_{q,j}\|W_{q,j}\|_2^2,\\
 E_{\rm AP}&=\sum_j\left\|\sum_qW_{q,j}\right\|_2^2,\qquad
 E_{\rm pol}=\sum_q\left\|\sum_jW_{q,j}\right\|_2^2,\\
 E_{\rm all}&=\left\|\sum_{q,j}W_{q,j}\right\|_2^2.
\end{aligned}
$$

## Assumptions and notation

- \(Q\) is an integer with \(Q\geq3\).
- Active labels are primes \(Q<q\leq2Q\).
- \(H=4Q^2\), \(h=4Q\), and the same \(C_h\) is used in every channel.
- Packet profile values are real; the orthogonality proof also works for
  complex values after replacing squares by squared moduli.
- \(r_q=q^{-1}\pmod{4Q}\) and
  \(S_q=\{r_q,-r_q\}\).

The inverse exists because \(q\) is odd and cannot divide \(Q\): a prime
dividing \(Q\) is at most \(Q\), while every active \(q\) is larger than
\(Q\).

## Derivation map

1. The clock relations give
   \(\lfloor hq/H\rfloor=\lfloor q/Q\rfloor=1\).
2. Every row reduces to its two \(m=\pm1\) terms and has support \(S_q\).
3. A collision in \(S_{q_1}\) and \(S_{q_2}\) implies
   \(q_2\equiv q_1\) or \(q_2\equiv-q_1\pmod{4Q}\).
4. The interval bounds rule out both alternatives for distinct active primes.
5. Pythagoras across the disjoint blocks gives
   \(E_{\rm AP}=E_{\rm diag}\) and \(E_{\rm all}=E_{\rm pol}\).

## Main derivation

### Step 1: cutoff (IDENTITY)

For \(Q<q\leq2Q\),

$$
 \left\lfloor\frac{hq}{H}\right\rfloor
 =\left\lfloor\frac{4Qq}{4Q^2}\right\rfloor
 =\left\lfloor\frac qQ\right\rfloor=1.
$$

The endpoint \(q=2Q\) is absent from the prime shell for \(Q\geq3\), so the
upper endpoint does not introduce a second layer.

### Step 2: support (IDENTITY)

Writing \(t_q=Q/q\),

$$
 u_{q,j}=C_h\psi_j(t_q),\qquad
 v_{q,j}=C_h\psi_j(-t_q),
 \qquad
 W_{q,j}=u_{q,j}e_{r_q}+v_{q,j}e_{-r_q}.
$$

The two coordinates are distinct because \(4Q\nmid2\).

### Step 3: disjointness (PROVED_EXACT)

Suppose distinct active primes \(q_1,q_2\) have intersecting supports.  Then
for some \(\varepsilon\in\{1,-1\}\),

$$
 q_1^{-1}\equiv\varepsilon q_2^{-1}\pmod{4Q},
 \qquad\text{hence}\qquad
 q_2\equiv\varepsilon q_1\pmod{4Q}.
$$

If \(\varepsilon=1\), then
\(|q_2-q_1|<Q<4Q\), so the congruence forces \(q_1=q_2\).  If
\(\varepsilon=-1\), then
\(2Q<q_1+q_2\leq4Q\); divisibility by \(4Q\) forces
\(q_1+q_2=4Q\).  The upper bounds \(q_i\leq2Q\) then force both to equal
\(2Q\), which is not prime.  Hence the supports are pairwise disjoint.

### Step 4: energy identities (PROVED_STRUCTURAL_L1)

For each packet \(j\), disjointness gives

$$
 \left\|\sum_qW_{q,j}\right\|_2^2
 =\sum_q\|W_{q,j}\|_2^2.
$$

Summing over \(j\) proves \(E_{\rm AP}=E_{\rm diag}\).  If
\(Y_q=\sum_jW_{q,j}\), then the \(Y_q\) also have disjoint prime blocks, so

$$
 E_{\rm all}
 =\left\|\sum_qY_q\right\|_2^2
 =\sum_q\|Y_q\|_2^2
 =E_{\rm pol}.
$$

When \(E_{\rm diag}>0\), the first identity rules out every strict saving
\(E_{\rm AP}\leq(1-\delta)E_{\rm diag}\) with \(\delta>0\).

### Step 5: affine specialization (IDENTITY)

For \(\psi_j(t)=1+s_jt\), set
\(S_1=\sum_js_j\) and \(S_2=\sum_js_j^2\).  The two coordinates of each row
give

$$
\begin{aligned}
 E_{\rm diag}=E_{\rm AP}
 &=2C_h^2\sum_{q\in\mathcal Q_Q}(J+S_2t_q^2),\\
 E_{\rm pol}=E_{\rm all}
 &=2C_h^2\sum_{q\in\mathcal Q_Q}(J^2+S_1^2t_q^2).
\end{aligned}
$$

For the TPC-224 slopes \(s=(0,1,-1,2)/10\),
\(S_1=1/5\) and \(S_2=3/50\), hence

$$
 E_{\rm diag}
 =C_h^2\sum_q\left(8+\frac{3}{25}t_q^2\right),\qquad
 E_{\rm pol}
 =C_h^2\sum_q\left(32+\frac{2}{25}t_q^2\right).
$$

## Interpretation and non-claims

- The obstruction is caused by the cutoff-one geometry, not by floating-point
  cancellation or a failed approximation.
- Packet cancellation remains possible: balanced packet values give
  \(E_{\rm pol}=E_{\rm all}=0\) while \(E_{\rm AP}=E_{\rm diag}>0\).
- Aligned packet values give the opposite packet-direction extreme.
- A clock with a second \(m\)-layer has a different collision graph; this
  theorem cannot be reused there without a new proof.
- No arithmetic \(L^2\) estimate, fixed-atom credit, strict \(1/400\) payment,
  V46 transfer, or twin-prime conclusion is claimed.

## Open risk and next clue

A productive AP route must either use a source-locked clock with
\(\lfloor hq/H\rfloor\geq2\), where genuine multiplicative collisions can
occur, or prove a different physical synthesis map that creates legitimate
overlap.  The next paper should audit the smallest nontrivial-cutoff clock
and separate literal support collisions from any unproved arithmetic
reassembly.
