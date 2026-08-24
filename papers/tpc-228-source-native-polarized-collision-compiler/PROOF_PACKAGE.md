# TPC-228 proof package

## Theorem

Let `Q` be a finite label set and let `U_q,V_q` be vectors in a complex Hilbert space
whose inner product is linear in the first argument. Set

$$
W_q^{(j)}=U_q+i^jV_q,
$$

and define

$$
A_j=\left\|\sum_qW_q^{(j)}\right\|^2-\sum_q\|W_q^{(j)}\|^2.
$$

Then

$$
\frac14\sum_{j=0}^3i^jA_j
=\sum_{q\ne r}\langle U_q,V_r\rangle. \tag{1}
$$

## Proof

Expanding the square and deleting its diagonal gives

$$
A_j=\sum_{q\ne r}\langle U_q+i^jV_q,U_r+i^jV_r\rangle.
$$

The sums are finite, so interchange the `j`-sum and `(q,r)`-sum. For each ordered
pair, the standard identity

$$
\frac14\sum_{j=0}^3i^j\|x+i^jy\|^2=\langle x,y\rangle
$$

applies by polarization to the bilinear expansion as well; equivalently, the
`U_q,U_r` and `V_q,V_r` terms have coefficient `sum i^j=0`, the conjugate cross term
has coefficient `sum i^{2j}=0`, and `\langle U_q,V_r\rangle` has coefficient four.
This proves (1). ∎

## Q25 specialization

Restricting to the two shared coordinates in the TPC-226 first resonance produces

$$
\frac1{400^2}\left(
\beta_{37,3}w_{47,-7}+\beta_{47,-7}w_{37,3}
+\beta_{37,-3}w_{47,7}+\beta_{47,7}w_{37,-3}
\right).
$$

The five exact controls in the certificate show this scalar can have either sign or
vanish under arbitrary finite source amplitudes. Thus collision geometry does not
decide the sign, but the missing signed arithmetic object is now source-labelled and
explicit.

## Claim boundary

The theorem is exact structural algebra. It assumes common-profile row maps and does
not yet prove that the literal V59 `beta,w` sequences realize these primitive atom
amplitudes. That physical crosswalk and any growing-scale cancellation remain open.
