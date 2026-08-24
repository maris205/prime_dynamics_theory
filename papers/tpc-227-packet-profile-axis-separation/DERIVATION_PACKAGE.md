# TPC-227 derivation package

## 1. Literal source typing

V59 fixes one linear transform `T` containing the common character/Fourier/Poisson
kernel and four source vectors

$$
z_j=x+i^j y,\qquad j=0,1,2,3.
$$

The exact polarization identity is

$$
\langle Tx,Ty\rangle
=\frac14\sum_{j=0}^3 i^j\|Tz_j\|^2. \tag{1}
$$

Replacing `T` by packet-dependent `T_j` is a new modeling operation, not a relabeling.

## 2. Gram Fourier expansion

Let `Q_j=T_j^*T_j` and `Q=T^*T`. With the inner product linear in its first
argument, define

$$
A_k=\frac14\sum_{j=0}^3 i^{kj}Q_j.
$$

Direct expansion gives

$$
\frac14\sum_j i^j\|T_j(x+i^jy)\|^2
=\langle A_1x,x\rangle+\langle A_1y,y\rangle
 +\langle A_0x,y\rangle+\langle A_2y,x\rangle. \tag{2}
$$

Equality with `\langle Qx,y\rangle` for every `x,y` forces

$$
A_0=Q,\qquad A_1=A_2=A_3=0. \tag{3}
$$

Four-point Fourier inversion then yields `Q_j=Q` for all `j`. The converse follows
immediately from (1).

For real finite matrices, the checker uses

$$
\begin{aligned}
A_0&=(Q_0+Q_1+Q_2+Q_3)/4,\\
\Re A_1&=(Q_0-Q_2)/4,\\
\Im A_1&=(Q_1-Q_3)/4,\\
A_2&=(Q_0-Q_1+Q_2-Q_3)/4.
\end{aligned}
$$

## 3. Q=25 resonance witness

At the TPC-226 collision `(p,r)=(37,47)`, one shared residue receives the aligned row

$$
T=\frac1{400}(1,1),
$$

while the row-dependent odd sign gives

$$
T_{\rm odd}=\frac1{400}(1,-1).
$$

Hence

$$
T^*T=\frac1{160000}\begin{pmatrix}1&1\\1&1\end{pmatrix},\qquad
T_{\rm odd}^*T_{\rm odd}=\frac1{160000}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}.
$$

The off-diagonal mismatch is exactly `-2/160000=-1/80000`. This is the local
algebraic reason the odd profile reverses the collision term. It is also exactly why the
profile cannot be renamed as a source packet phase.

## 4. Phase visibility

Multiplying an entire packet transform by a scalar of modulus one changes `T_j` but not
`T_j^*T_j`. Such a global sign is invisible to every squared norm. By contrast, a sign
depending on the row preimage can alter cross-row Gram entries after two rows collide.
The latter is geometric data and requires its own physical source theorem.

## 5. Finite fixtures

The certificate checks six exact fixtures:

| fixture | result | reason |
|---|---:|---|
| common physical transform | pass | all four Grams equal target |
| global packet signs | pass | signs vanish in the Gram |
| row-dependent odd sign | fail | target off-diagonal flips |
| alternating packet scale | fail | `A_0`/`A_2` contamination |
| four unequal scales | fail | diagonal and cross contamination |
| mixed aligned/odd profiles | fail | Fourier moment contamination |

The fixtures prove no asymptotic estimate; they certify the theorem implementation and
the exact TPC-226 witness.
