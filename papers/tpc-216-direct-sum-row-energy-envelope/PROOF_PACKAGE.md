# Proof Package

## Claim

Let `x` be sufficiently large and set

$$
H=x^{21/32},\qquad Q=x^{1/3},\qquad
Y_0=H/(4Q),\qquad U=x^{133/400}.
$$

Let `\mathcal Q_x` be the primes in `(Q,2Q]`, let `P=|\mathcal Q_x|`, and let

$$
\mathcal D_x=\{d:Y_0<d\le U,\ \mu(d)^2=1\},\qquad
c_d=\mu(d)\log(d)/d.
$$

For a bounded profile `\psi`, define

$$
B_d(r)=\sum_{q\in\mathcal Q_x}
\sum_{0<|m|\le\lfloor dq/H\rfloor}
\psi\!\left(\frac{Hm}{dq}\right)
\mathbf 1_{m\bar q\equiv r\pmod d}.
$$

On a complete period `L`, define the direct-sum energy

$$
E_{\mathrm{direct}}=L\sum_{d\in\mathcal D_x}|c_d|^2
\sum_{r\bmod d}|B_d(r)|^2.
$$

Then, with `M_\psi=\sup_t|\psi(t)|`,

$$
L^{-1}E_{\mathrm{direct}}
\ll M_\psi^2\frac{Q^3}{H}(\log U)^3
=x^{11/32+o(1)}.
$$

The implied constant is absolute apart from the displayed dependence on
`M_\psi`.

## Status

**PROVABLE AS STATED.** The asymptotic statement is understood for the source
range where `4Q<H` and `U<Q`; these inequalities follow from the displayed
exponents for sufficiently large `x`.

## Assumptions

- `x` is sufficiently large that `4Q<H`, `U<Q`, and `Q>=1`.
- The divisor family is the full squarefree band `\mathcal D_x`.
- The source range has `d<U<Q<q`, so every `q` is a unit modulo every `d`.
- `M_\psi=\sup_t|\psi(t)|` is finite.
- `P=|\mathcal Q_x|`; no prime-counting estimate beyond `P<=2Q` is used.
- `L` is a complete common period for the rational frequencies.  The theorem
  does not identify this complete-period quantity with a finite physical
  interval.

## Notation

- `B_(d,q)` is the contribution to `B_d` from one prime `q`.
- `||v||_(2,d)^2=sum_(r mod d)|v(r)|^2`.
- `M_\psi` is the global profile supremum.
- `P` is the number of primes in the shell.

## Proof Strategy

First prove fixed-q injectivity of the integer-to-residue map.  The bound
`4Q<H` implies `2 floor(dq/H)<d`, so two distinct admissible integers cannot
land in the same residue modulo `d`.  This makes each fixed-q row an exact
orthogonal sum of its individual `m` atoms.  Apply Cauchy only across the
prime shell, sum the resulting row bound against `|c_d|^2`, and use an
elementary harmonic-integral estimate for the remaining divisor sum.

## Dependency Map

1. The source exponent ledger gives `4Q<H` and `U<Q` for large `x`.
2. The unit condition makes `m\bar q mod d` well-defined.
3. `4Q<H` gives fixed-q no-collision and the fixed-q row norm bound.
4. Shell Cauchy gives the `P^2` row envelope.
5. `P<=2Q` turns that envelope into `Q^3/H`.
6. The divisor coefficient identity reduces the remaining sum to
   `sum_(d<=U)(log d)^2/d`, which is `O((log U)^3)`.

## Proof

### Step 1: source inequalities

The exponent identities are

$$
\frac{H}{4Q}=\frac14x^{31/96}\to\infty,
\qquad
\frac{U}{Q}=x^{-1/1200}\to0.
$$

Hence for sufficiently large `x`, `4Q<H` and `U<Q`.  Since every shell prime
satisfies `q<=2Q`, this implies

$$
2q/H\le4Q/H<1.
$$

### Step 2: fixed-q no-collision

Fix `d in \mathcal D_x` and `q in \mathcal Q_x`, and put

$$
n_{d,q}=\left\lfloor\frac{dq}{H}\right\rfloor.
$$

If two distinct integers `m_1,m_2` with `0<|m_i|<=n_(d,q)` produce the same
residue after multiplication by `\bar q`, then `d` divides `m_1-m_2`, because
`q` is a unit modulo `d`.  However,

$$
0<|m_1-m_2|\le2n_{d,q}
\le\frac{2dq}{H}<d.
$$

No positive multiple of `d` lies in this interval, a contradiction.  Thus the
map from admissible `m` to residues modulo `d` is injective.

Writing `B_(d,q)` for the fixed-q row, injectivity removes all cross terms
inside that row and gives

$$
\|B_{(d,q)}\|_{2,d}^2
=\sum_{0<|m|\le n_{d,q}}
\left|\psi\!\left(\frac{Hm}{dq}\right)\right|^2
\le2M_\psi^2n_{d,q}
\le2M_\psi^2\frac{dq}{H}.
$$

### Step 3: shell Cauchy

Since `B_d=sum_q B_(d,q)`, Cauchy in the `P` shell coordinates gives

$$
\begin{aligned}
\|B_d\|_{2,d}^2
&\le P\sum_{q\in\mathcal Q_x}\|B_{(d,q)}\|_{2,d}^2\\
&\le \frac{2M_\psi^2Pd}{H}\sum_{q\in\mathcal Q_x}q
\le\frac{4M_\psi^2P^2dQ}{H}.
\end{aligned}
$$

The last inequality uses `q<=2Q`.  The elementary interval count
`P<=2Q` is sufficient; no prime number theorem is used.  Therefore

$$
\|B_d\|_{2,d}^2\le16M_\psi^2\frac{dQ^3}{H}.
$$

### Step 4: sum over the divisor band

By the definition of `c_d`,

$$
|c_d|^2=\frac{\mu(d)^2(\log d)^2}{d^2}.
$$

Consequently,

$$
\begin{aligned}
L^{-1}E_{\mathrm{direct}}
&\le16M_\psi^2\frac{Q^3}{H}
\sum_{Y_0<d\le U}\frac{\mu(d)^2(\log d)^2}{d}\\
&\le16M_\psi^2\frac{Q^3}{H}
\sum_{1\le d\le U}\frac{(\log d)^2}{d}.
\end{aligned}
$$

For `U>=3`, comparison with the integral of `(log t)^2/t` (and a bounded
initial segment) gives

$$
\sum_{1\le d\le U}\frac{(\log d)^2}{d}
\ll(\log(2U))^3.
$$

Finally,

$$
\frac{Q^3}{H}=x^{1-21/32}=x^{11/32},
\qquad
\log(2U)=O(\log x),
$$

which proves the claim. `\square`

## Corrections or Missing Assumptions

The mnemonic condition `2Q<H` alone would not prove fixed-q injectivity when
the shell extends to `2Q`; the proof uses the stronger source consequence
`4Q<H`.  This is not an added asymptotic hypothesis because
`H/(4Q)=x^{31/96}/4` tends to infinity.

## Open Risks

- The theorem is a complete-period direct-sum envelope, not a finite-window
  off-frequency Gram bound.
- Shell Cauchy is potentially sharp under aligned row supports, as shown by
  the exact rational fixture in this project.
- No Mobius cancellation, prime-shell cancellation, four-packet reassembly,
  arithmetic `L2`, fixed-atom credit, or strict `1/400` payment is proved.
