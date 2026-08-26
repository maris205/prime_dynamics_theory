# TPC-262 proof package

## Claim

`TPC262` proves an exact finite, literal reduced-residue signed-operator
factorization for each additive phase of V59. It also proves a finite
operator-image obstruction: equal packet diagonals and positive-semidefinite
Gram information permit both maximal and vanishing mode zero.

## Theorem 1 — centered unit fiber

For every prime `q >= 3`,

```text
C_q = I - 1/(q-1) 11^T
```

satisfies `C_q^T=C_q`, `C_q^2=C_q`, is positive semidefinite, has rank
`q-2`, and has kernel spanned by `1`.

### Proof

Since `1^T1=q-1`, direct multiplication gives `C_q^2=C_q`. For any real
vector `v`,
`v^T C_q v=||v||^2-|1^Tv|^2/(q-1)>=0` by Cauchy--Schwarz. The constant line
is the kernel and its orthogonal complement is fixed, so the rank is `q-2`.
(square)

## Theorem 1.1 — signed literal remainder operator

Let \(I\) be a finite interval, let \(v\in\mathbb R\), and define the residue
synthesis

~~~text
(S_(q,v)a)_r = sum_(n in I, n = r mod q) a_n exp(2 pi i v n/H),
                r in F_q^*.
~~~

Let \(P_q\) be the diagonal projection onto \(q\)-units. Define

~~~text
J_(q,v)=S_(q,v)^* C_q S_(q,v)-((q-2)/(q-1))P_q.
~~~

Then \(J_{q,v}\) is Hermitian and, for every coefficient vector \(a\),

~~~text
V_q^times(a;v)-D_q^times(a) = <a,J_(q,v)a>,
V_q^times(a;v)=||C_q S_(q,v)a||^2,
D_q^times(a;v)=((q-2)/(q-1))||P_q a||^2.
~~~

### Proof

The first term is the Gram form of \(C_qS_{q,v}\), hence is Hermitian.
Subtracting the real diagonal projection preserves that property. Expanding
the two quadratic forms gives the displayed identity term by term. The
coefficient \(q-2\) is the number of nonprincipal characters of a prime
modulus; it is not replaceable by \(q-1\). (square)

For the V59 common clock, define

~~~text
J_x = integral psi_+(v) sum_(q in Q_x) q J_(q,v) dv.
~~~

The preceding identity gives
\(\mathcal V^\circ_{\mathcal Q,H}(a)=\langle a,J_xa\rangle\).
For the four source packets \(a^{(j)}=\beta+\ii^jw\), exact polarization
then gives

~~~text
C_x = (1/4) sum_(j=0)^3 i^j
      <a^(j), J_x a^(j)>.
~~~

This is an exact signed Hermitian factorization. It supplies no bound for
the growing shell and no fixed-power credit.

## Theorem 2 — literal cross-Gram mode-zero identity

Let `Q` be a finite set of odd primes and let `Y_j` be the weighted
direct-sum outputs `Y(a_j)` defined in the derivation package. With

```text
Gamma_jk = <<Y_j,Y_k>>,
D = sum_j Gamma_jj,
R = sum_{j<k} Re(Gamma_jk),
```

one has the exact identities

```text
||sum_j Y_j||^2 = D+2R,
Yhat_k = (1/2) sum_j i^(-jk)Y_j,
sum_k ||Yhat_k||^2 = D,
||sum_jY_j||^2 = 4||Yhat_0||^2.
```

### Proof

Expand the squared norm and pair conjugate off-diagonal entries. This gives
`D+2R`. The DFT identities follow by orthogonality of the four roots of
unity and Parseval, with the displayed normalization. (square)

## Lemma 2.1 — phase-character separation

For two vectors \(X,Y\), define

~~~text
E_j = ||X+i^jY||^2,
F_k = (1/4) sum_j i^(k j) E_j.
~~~

With the conjugate-linear-first-slot convention,

~~~text
F_0 = ||X||^2+||Y||^2,
F_1 = <Y,X>,
F_2 = 0,
F_3 = <X,Y>.
~~~

### Proof

Expand
\(E_j=||X||^2+||Y||^2+i^j<X,Y>+i^{-j}<Y,X>\) and use the
fourth-root orthogonality relation. (square)

This is a typing firewall: aggregate packet mode zero in Theorem 2 is not
automatically the nontrivial \(C_4\) character selected by V59 polarization.
A future growing-shell theorem must state which quantity it estimates.

## Theorem 3 — exact endpoint criterion

Suppose a literal reassembly has baseline exponent `E_0=5/3`, target
`E_*=1997/1200`, and a finite collection of paid losses. If the cross-Gram
mode-zero expression in Theorem 2 has effective saving `sigma`, then the
finite-lane endpoint compiler closes under the strict condition

```text
sigma > E_0-E_* = 1/400.
```

### Proof

Substitute `D+2R` as the mode-zero output into the TPC-261 finite-lane
compiler. The exponent difference is exactly `1/400`; strictness is needed
to absorb an arbitrary `x^epsilon` loss. (square)

## Theorem 4 — literal finite operator-image obstruction

Take the actual prime shell `Q={5,7,11,13}` and the exact matrices `C_q`.
There is a nonzero packet output `Y` in this literal operator image such that
the two four-packet families

```text
Y_j^+ = Y,
Y_j^- = (-1)^j Y
```

have identical four diagonal entries and identical total packet energy, but

```text
||sum_jY_j^+||^2 = 16||Y||^2,
||sum_jY_j^-||^2 = 0.
```

### Proof

Use the `q=5` source vector `e_1`, set all other prime components to zero,
and let `Y=C_5e_1` in the weighted direct sum. The first theorem shows
`||Y||^2>0`. The two sums are respectively `4Y` and `0`; their packet
norms are all `||Y||`. (square)

## Scope firewall

```text
PROVED = finite unit-class projection; literal signed remainder operator with
         deleted diagonal; weighted cross-Gram identity; exact DFT ledger;
         endpoint criterion under a stated saving;
         finite operator-image adversary
NUMERICALLY_CERTIFIED = rational certificate and independent mutation audit
OPEN = growing V59 kernel character-specific cross-Gram estimate for actual
       beta/w packets
NOT_CLAIMED = arithmetic L2; prime-shell asymptotic counterexample; fixed atom;
              full Gate B; twin-prime theorem
```
