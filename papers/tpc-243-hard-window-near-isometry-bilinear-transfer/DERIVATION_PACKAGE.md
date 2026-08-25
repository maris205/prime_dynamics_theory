# Derivation Package

## Target

Derive a direct hard-window two-sided frame estimate and its signed bilinear
transfer for a finite separated set of frequencies, then specialize the error
to primitive rational frequencies at the V59 scale.

## Status

`COHERENT AS STATED`

## Invariant Object

The invariant object is the normalized Gram perturbation

$$
A=\frac1N T^*T-I.
$$

Both the quadratic near-isometry and the signed bilinear estimate follow from
one bound on $\lVert A\rVert_{2\to2}$. No quadratic-to-bilinear heuristic is
needed.

## Assumptions

- $\mathcal F\subset\mathbb R/\mathbb Z$ is finite and
  $\delta$-separated, with $0<\delta\leq1/2$.
- $I=\{M,\ldots,M+N-1\}$ and $N\geq1$.
- The complex inner product is conjugate-linear in its first slot.
- For the primitive rational corollary, all frequencies are distinct reduced
  fractions of height at most $U$, where $U\geq2$.
- Finite executable checks are illustrations only and are never substituted
  for the symbolic proof.

## Notation

- $e(t)=\exp(2\pi i t)$.
- $\lVert\theta\rVert_{\mathbb R/\mathbb Z}$ is circular distance to an
  integer.
- $Tz(n)=\sum_{\alpha\in\mathcal F}z_\alpha e(n\alpha)$.
- $K=\lfloor(2\delta)^{-1}\rfloor$ and
  $H_K=\sum_{j=1}^Kj^{-1}$.
- $R_\delta=\delta^{-1}H_K$ and $\epsilon=R_\delta/N$.

## Derivation Strategy

Compute the hard rectangular Gram matrix exactly. Bound each off-diagonal
entry by inverse circular distance, sum those bounds using two-sided packing,
and convert the resulting row estimate into an operator estimate. The
primitive and V59 statements are substitutions into that general estimate.

## Derivation Map

1. The geometric sum gives
   $|G_{\alpha\beta}|\leq(2\lVert\beta-\alpha\rVert)^{-1}$ off the diagonal.
2. Circular separation gives at most two distance lists, each with
   $d_j\geq j\delta$ and $j\leq K$.
3. Therefore every off-diagonal row sum is at most
   $R_\delta=\delta^{-1}H_K$.
4. Hermitian Schur/Gershgorin gives
   $\lVert G-NI\rVert\leq R_\delta$.
5. Quadratic and bilinear estimates follow from the same operator inequality.
6. Primitive spacing supplies $\delta=U^{-2}$.
7. The V59 exponents determine the exact leading coefficient $133/100$.
8. Reversing the coefficient arguments in the bilinear estimate matches the
   TPC-242 selected orientation.

## Main Derivation

### Step 1: Gram entries

For the coefficient basis indexed by $\mathcal F$,

$$
G_{\alpha\beta}
=\sum_{n\in I}e\bigl(n(\beta-\alpha)\bigr).
$$

This direction follows from
$\overline{z_\alpha}w_\beta e(n(\beta-\alpha))$ and is orientation-sensitive.
The diagonal is $N$.

### Step 2: Entrywise geometric bound

For $\theta\notin\mathbb Z$,

$$
\left|\sum_{n\in I}e(n\theta)\right|
=\frac{|\sin(\pi N\theta)|}{|\sin(\pi\theta)|}
\leq\frac1{2\lVert\theta\rVert_{\mathbb R/\mathbb Z}}.
$$

The final inequality uses $\sin(\pi t)\geq2t$ for
$0\leq t\leq1/2$.

### Step 3: Harmonic circular packing

Fix $\alpha$. Assign every other frequency to one shortest oriented arc from
$\alpha$; an antipodal point is assigned to one side only. On either side,
the increasing distances satisfy $d_j\geq j\delta$. Since $d_j\leq1/2$,
there are at most $K=\lfloor(2\delta)^{-1}\rfloor$ points on that side.
Consequently,

$$
\sum_{\beta\ne\alpha}|G_{\alpha\beta}|
\leq2\sum_{j=1}^K\frac1{2j\delta}
=\delta^{-1}H_K=R_\delta.
$$

The factor two is an upper bound for the two sides; the antipodal tie is not
counted twice.

### Step 4: One operator estimate, two consequences

The Hermitian matrix $G-NI$ has every absolute row and column sum at most
$R_\delta$. Hence

$$
\left\|\frac GN-I\right\|_{2\to2}\leq\epsilon.
$$

The quadratic form gives

$$
[1-\epsilon]_+\lVert z\rVert_2^2
\leq N^{-1}\lVert Tz\rVert_2^2
\leq(1+\epsilon)\lVert z\rVert_2^2.
$$

The positive part uses the independent fact $G\succeq0$. Applying the same
operator estimate to $z,w$ gives the identity-to-identity transfer

$$
\left|N^{-1}\langle Tz,Tw\rangle-\langle z,w\rangle\right|
\leq\epsilon\lVert z\rVert_2\lVert w\rVert_2.
$$

### Step 5: Primitive rational specialization

Distinct reduced fractions $a/h,b/k$ of height at most $U$ satisfy

$$
\left\|\frac ah-\frac bk\right\|\geq\frac1{hk}\geq U^{-2}.
$$

Thus

$$
R_U=U^2H_{\lfloor U^2/2\rfloor},\qquad
\epsilon_U=\frac{R_U}{N}.
$$

### Step 6: Exact V59 coefficient

With $U=x^{133/400}$,

$$
U^2=x^{133/200},\qquad
H_{\lfloor U^2/2\rfloor}=2\log U+O(1)
=\frac{133}{200}\log x+O(1).
$$

Since $N=x/2+O(1)$,

$$
\epsilon_U
=\left(\frac{133}{100}+o(1)\right)
x^{-67/200}\log x
=x^{-67/200+o(1)}.
$$

The coefficient $133/100$ is the product of the reciprocal interval density
$2$ and the harmonic logarithmic coefficient $133/200$.

### Step 7: TPC-242 orientation

Set $X=N^{-1/2}Tz$ and $Y=N^{-1/2}Tw$. TPC-242 selects

$$
F_1=\langle Y,X\rangle=N^{-1}\langle Tw,Tz\rangle.
$$

The bilinear theorem applied with first coefficient vector $w$ and second
coefficient vector $z$ yields

$$
|F_1-\langle w,z\rangle|
\leq\epsilon\lVert w\rVert_2\lVert z\rVert_2.
$$

## Remarks and Interpretation

- The hard interval itself supplies the Gram matrix; no triangular minorant is
  inserted.
- The estimate transports complex sign and phase because it controls the full
  bilinear form, not only separate unsigned norms.
- The logarithm is the cost of summing inverse distance over two circular
  sides by absolute values.

## Boundaries and Non-Claims

- TPC-217 already contains the standard upper large-sieve scale.
- No theorem here bounds the physical coefficient norms
  $\lVert z\rVert_2,\lVert w\rVert_2$.
- No literal top-prime attachment or signed $C_h$ theorem is supplied.
- Arithmetic $L2$, fixed-atom credit, strict $1/400$, full Gate B, and a
  twin-prime conclusion remain open.

## Open Risks

- Absolute harmonic packing may be too expensive if a later physical loss
  ledger requires removal of the logarithm.
- A physical coefficient map could use asymmetric lane multipliers, in which
  case the present common synthesis operator is only one component of the
  attachment theorem.
