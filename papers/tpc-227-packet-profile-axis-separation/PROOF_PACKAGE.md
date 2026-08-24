# TPC-227 proof package

## Claim

Let `X,Y` be complex Hilbert spaces, let `T,T_0,T_1,T_2,T_3:X->Y` be bounded
linear maps, and use an inner product linear in the first argument. Then

$$
\frac14\sum_{j=0}^3 i^j\|T_j(x+i^jy)\|^2=\langle Tx,Ty\rangle
\quad\text{for every }x,y\in X \tag{1}
$$

if and only if

$$
T_j^*T_j=T^*T\qquad(0\le j\le3). \tag{2}
$$

Consequently:

1. a global unit-modulus multiplier on a packet transform is invisible;
2. bounded packet-dependent profiles are not sufficient for source transfer;
3. the TPC-226 row-dependent odd profile fails the physical aligned Gram criterion on
   the exact `Q=25`, `(37,47)` collision block, with off-diagonal mismatch
   `-1/80000`.

## Status

**PROVABLE AS STATED.** The theorem is exact operator algebra. The application is a
finite structural source-transfer obstruction, not an arithmetic estimate.

## Proof

Put

$$
Q_j=T_j^*T_j,\qquad Q=T^*T,\qquad
A_k=\frac14\sum_{j=0}^3i^{kj}Q_j.
$$

Each `Q_j` is positive self-adjoint. Expanding one summand gives

$$
\begin{aligned}
i^j\|T_j(x+i^jy)\|^2
={}&i^j\langle Q_jx,x\rangle+i^j\langle Q_jy,y\rangle\\
&+\langle Q_jx,y\rangle+i^{2j}\langle Q_jy,x\rangle.
\end{aligned}
$$

Summing yields

$$
F(x,y):=\frac14\sum_{j=0}^3i^j\|T_j(x+i^jy)\|^2
=\langle A_1x,x\rangle+\langle A_1y,y\rangle
 +\langle A_0x,y\rangle+\langle A_2y,x\rangle. \tag{3}
$$

Assume (1). Setting `y=0` in (3) gives
`\langle A_1x,x\rangle=0` for every `x`. The real and imaginary parts of `A_1`
are self-adjoint linear combinations of the `Q_j`; the polarization identity for
Hermitian forms therefore gives `A_1=0`. Since `A_3=A_1^*`, also `A_3=0`.

Equation (3) now reads

$$
\langle A_0x,y\rangle+\langle A_2y,x\rangle=\langle Qx,y\rangle. \tag{4}
$$

Replace `y` by `iy`. Under our convention, the first and target terms acquire `-i`,
whereas the second acquires `+i`. Combining the resulting identity with `-i` times
(4) gives `\langle A_2y,x\rangle=0` for every `x,y`; hence `A_2=0`, and then
`A_0=Q`.

The four-point discrete Fourier transform is invertible, so

$$
Q_j=\sum_{k=0}^3i^{-kj}A_k=Q
$$

for every `j`. This proves necessity. Conversely, if all `Q_j=Q`, then every norm in
(1) equals `\|T(x+i^jy)\|^2`; the ordinary four-phase polarization identity proves
(1).

For the finite witness, one shared TPC-226 residue has physical aligned synthesis row

$$
T=\frac1{400}(1,1)
$$

and odd row-dependent synthesis row

$$
S=\frac1{400}(1,-1).
$$

Thus

$$
S^*S-T^*T
=\frac1{160000}
\begin{pmatrix}0&-2\\-2&0\end{pmatrix},
$$

whose off-diagonal entry is `-1/80000`. Therefore `S^*S != T^*T`, so (1) cannot
hold with the physical target on every source pair. Multiplying a whole operator by a
unit scalar leaves its Gram unchanged, proving the global-phase statement. All claims
follow. ∎

## Source interpretation

V59 has `T_j=T`: packet dependence is in `beta+i^j w`, while `psi_+(v)` is common.
TPC-218 introduced arbitrary `psi_j` only as a bounded structural lift. TPC-226's
balanced fixture remains a valid finite profile theorem, but its row sign is not a
literal V59 source phase. Promoting it requires a separate common-profile source-native
compiler.

## Open theorem

Construct the prime/AP collision representation directly from the V59 coefficient
packets while retaining one common Poisson profile, and determine the resulting signed
`3--7` source correlation without moving the phase to the profile axis.
