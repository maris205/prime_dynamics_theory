# TPC-226 derivation package

## Target

Determine the first integer dilation of the TPC-225 source-surrogate clock that creates
a legitimate collision between two distinct literal primitive prime rows, classify all
collisions at that first dilation, and derive their exact signed contribution to the AP
energy.

## Status

**COHERENT AS STATED / PROVED_STRUCTURAL_L1**

The target survives after one essential source correction: every multiplier must remain
primitive modulo the active residue modulus.  Without this correction, `L=3` exhibits a
spurious `m=4` overlap that does not belong to the TPC-220 row.

## Invariant object

For `Q>=8` and `L in {1,2,3,4}`, set

$$
 x=Q^3,\qquad H=4Q^2,\qquad h_L=4LQ,
$$

and let $\mathcal Q_Q$ be the primes in $(Q,2Q)$.  The invariant literal row is

$$
 W_{q,j}^{(L)}(a)=\frac1{h_L}
 \sum_{m\in\mathcal M_L(q)}
 \psi_j\!\left(\frac{mQ}{Lq}\right)
 \mathbf 1_{m q^{-1}\equiv a\pmod{h_L}},
$$

where

$$
 \mathcal M_L(q)=\left\{m\in\mathbb Z:\ 0<|m|\le
 \left\lfloor\frac{Lq}{Q}\right\rfloor,\ (m,h_L)=1\right\}.
$$

All collision and energy statements are derived from this same family.

## Assumptions

- $Q$ is an integer with $Q\ge8$.
- $L\in\{1,2,3,4\}$ is a finite modeling parameter.
- Every active label $q$ is prime and satisfies $Q<q<2Q$.
- Multipliers are primitive: $(m,h_L)=1$.
- All rows use the common normalization $C_h=1/h_L$.
- The finite profiles may be real or complex.  The sign examples use real profiles.

The inverse $q^{-1}\pmod{h_L}$ exists because $q>Q\ge8>L$, $q$ cannot divide $Q$,
and $q$ is odd.

## Notation

- $R_L(q)=\lfloor Lq/Q\rfloor$.
- $S_{q,L}=\{m q^{-1}\pmod{h_L}:m\in\mathcal M_L(q)\}$.
- $E_{\rm diag}=\sum_{q,j}\|W_{q,j}^{(L)}\|_2^2$.
- $E_{\rm AP}=\sum_j\|\sum_qW_{q,j}^{(L)}\|_2^2$.
- $E_{\rm pol}=\sum_q\|\sum_jW_{q,j}^{(L)}\|_2^2$.
- $E_{\rm all}=\|\sum_{q,j}W_{q,j}^{(L)}\|_2^2$.
- $\mathcal R_Q$ is the set of ordered low/high prime pairs $(p,r)$ satisfying
  $7p+3r=16Q$ and the literal shell/cutoff/primitive conditions.

## Derivation strategy

First reduce every support collision to one short integer equation.  Primitive support
forces both absolute multipliers to be odd.  Size, cutoff, and divisibility then eliminate
all dilations below four and classify the dilation-four equation.  Finally, expand
$E_{\rm AP}-E_{\rm diag}$ as a signed sum over the resulting two-coordinate resonances.

## Derivation map

1. A collision is equivalent to $m_1q_2-m_2q_1\equiv0\pmod{4LQ}$.
2. In the stable range $Q\ge8$, equal-sign and zero-wrap collisions are impossible.
3. Opposite signs give $a q_2+b q_1=4LQ$ with odd positive $a,b$.
4. The inequalities $2L<a+b<4L$ and the cutoff constraints settle $L\le3$.
5. At $L=4$, primitive divisibility removes $(5,5)$ and cutoff bounds remove every
   pair except $(3,7)$ and $(7,3)$.
6. Each resonance creates exactly two sign-symmetric shared coordinates.
7. Their cross terms are positive for aligned/affine profiles and negative for balanced
   sign profiles.

## Main derivation

### Step 1: cutoff and internal injectivity (IDENTITY)

Since $Q<q<2Q$,

$$
 L\le R_L(q)\le2L-1.
$$

For $L\le4$, every allowed multiplier has $|m|\le7<q$.  If two multipliers in
one row give the same residue, then $h_L\mid m_1-m_2$.  But
$|m_1-m_2|\le14<h_L$, so $m_1=m_2$.  Thus each literal row has no internal support
folding.

### Step 2: collision equation (IDENTITY)

For distinct active primes $q_1,q_2$, a shared coordinate is equivalent to

$$
 m_1q_1^{-1}\equiv m_2q_2^{-1}\pmod{h_L}
 \quad\Longleftrightarrow\quad
 m_1q_2-m_2q_1\equiv0\pmod{h_L}.
$$

If $m_1,m_2$ have the same sign, then the magnitude of the difference is less than
$(4L-3)Q<h_L$.  Equality to zero is also impossible: distinct primes would force
$q_1\mid m_1$, whereas $0<|m_1|<q_1$.  Therefore a collision must use opposite
signs.  Writing $a=|m_1|$ and $b=|m_2|$ gives

$$
 a q_2+b q_1=4LQ. \tag{1}
$$

The left side is less than $2h_L$, so no higher wrap is possible.

### Step 3: universal size and parity restrictions (PROVED_EXACT)

Because $h_L$ is even and both multipliers are primitive, $a$ and $b$ are odd.
Equation (1) and $Q<q_i<2Q$ imply

$$
 2L<a+b<4L. \tag{2}
$$

For $L=1$, no odd pair satisfies (2).  For $L=2$, only $(3,3)$ remains, but
allowing multiplier $3$ in both rows requires $q_i\ge3Q/2$, so
$3(q_1+q_2)\ge9Q>8Q$.  For $L=3$, primitivity modulo $12Q$ excludes multiplier
$3$; the only remaining pair allowed by (2) is $(5,5)$.  Its two cutoff conditions
give $q_i\ge5Q/3$, hence $5(q_1+q_2)\ge50Q/3>12Q$.  Therefore

$$
 S_{q_1,L}\cap S_{q_2,L}=\varnothing
 \qquad(L=1,2,3;\ q_1\ne q_2). \tag{3}
$$

### Step 4: first primitive collision classification (PROVED_EXACT)

For $L=4$, positive primitive multipliers lie in $\{1,3,5,7\}$.  Conditions (2) and
the cutoff lower bounds leave the unordered candidates

$$
 (3,7),\qquad(5,5),\qquad(5,7),\qquad(7,7).
$$

The last two exceed $16Q$ once their own cutoff lower bounds are imposed.  The pair
$(5,5)$ would require $5(q_1+q_2)=16Q$, but primitive use of multiplier $5$ implies
$5\nmid Q$, contradicting that equation.  Consequently every collision is, up to
exchange and global sign,

$$
 7p+3r=16Q,\qquad m_p=3,\qquad m_r=-7. \tag{4}
$$

Conversely, any prime pair satisfying (4), the shell inequalities, the cutoff for
$m_r=7$, and $(21,16Q)=1$ yields two shared residues

$$
 3p^{-1}\equiv-7r^{-1},\qquad
 -3p^{-1}\equiv7r^{-1}\pmod{16Q}. \tag{5}
$$

They are distinct because $16Q\nmid6$.

### Step 5: first exact witness (PROVED_EXACT)

At $Q=25$, $(p,r)=(37,47)$ satisfies

$$
 7\cdot37+3\cdot47=400=16Q.
$$

The cutoffs are $5$ and $7$, while primitive support removes multiplier $5$ from
both rows.  Since

$$
 37^{-1}\equiv173,\qquad47^{-1}\equiv383\pmod{400},
$$

the two shared coordinates are

$$
 3\cdot173\equiv-7\cdot383\equiv119,
 \qquad
 -3\cdot173\equiv7\cdot383\equiv281\pmod{400}. \tag{6}
$$

### Step 6: signed resonance formula (IDENTITY)

For a resonance $(p,r)\in\mathcal R_Q$, put

$$
 u_p=\frac{3Q}{4p},\qquad v_r=\frac{7Q}{4r}.
$$

The pair contribution to $E_{\rm AP}-E_{\rm diag}$ is

$$
 \frac{2}{h^2}\Re\sum_j\left[
 \psi_j(u_p)\overline{\psi_j(-v_r)}+
 \psi_j(-u_p)\overline{\psi_j(v_r)}
 \right]. \tag{7}
$$

Summing (7) over all resonance pairs is exact, even when several pairs occur at the
same scale.

### Step 7: profile trichotomy (PROVED_EXACT FINITE STRUCTURE)

For aligned profiles $\psi_j(t)=1$, every resonance contributes $4J/h^2>0$.

For the inherited affine profiles $\psi_j(t)=1+s_jt$ with
$s=(0,1,-1,2)/10$ and $S_2=\sum_js_j^2=3/50$, every resonance contributes

$$
 \frac4{h^2}\left(J-S_2u_pv_r\right)>0. \tag{8}
$$

Let $\chi$ be a smooth compactly supported odd plateau satisfying
$\chi(t)=\operatorname{sgn}(t)$ for $1/8\le |t|\le1$.  Such a plateau exists by
smoothly interpolating on $[-1/8,1/8]$ and multiplying by an even cutoff that equals
one on $[-1,1]$.  Every sampled nonzero argument at $L=4$ lies in this plateau region.
For balanced sign profiles $\psi_j(t)=\alpha_j\chi(t)$, with
$\alpha=(1,-1,1,-1)$, every resonance contributes

$$
 -\frac4{h^2}\left(\sum_j\alpha_j^2\right)<0. \tag{9}
$$

Moreover $\sum_j\psi_j(t)=0$ pointwise, so $E_{\rm pol}=E_{\rm all}=0$.

At the witness $Q=25$, exact full-shell arithmetic gives

$$
 \frac{E_{\rm AP}}{E_{\rm diag}}=
 \begin{cases}
 15/13,&\text{aligned},\\
 14610396266802411880605/12679409642889136447511,
   &\text{inherited affine},\\
 11/13,&\text{balanced sign}.
 \end{cases} \tag{10}
$$

Thus legitimate overlap is necessary for a cross-prime correction but does not choose
its sign.

## Remarks and interpretation

- The first nontrivial cutoff is not the first legitimate primitive collision.
- Primitive support moves the first stable integer-dilation transition from the fake
  `L=3` overlap to the exact `L=4` resonance.
- The collision graph supplies an interface for cancellation; it does not supply the
  sign of cancellation.
- The balanced sign fixture proves structural compatibility of AP saving and packet
  cancellation on one finite clock, but its packet signs remain a modeling choice.

## Boundaries and non-claims

- `h_L=4LQ` is a finite dilated source-surrogate family, not a proved V46 clock.
- No prime-distribution theorem is used to prove that resonances occur at every or
  asymptotically many $Q$.
- The exact multi-scale census is numerical certification, not an asymptotic density
  theorem for solutions of $7p+3r=16Q$.
- No arithmetic $L^2$ estimate, fixed-atom credit, strict `1/400` payment, complete
  Gate B, or twin-prime conclusion is claimed.

## Open risks

The next theorem must source-lock a negative signed correlation for the actual packet
family on the `3`--`7` resonance set, or prove that the physical profile instead aligns
and amplifies it.  Geometry alone is now exhausted at this first-collision interface.
