# TPC-260 derivation package

Use the conjugate-linear-first-slot convention
`<u,v>=sum_n conjugate(u(n))v(n)`.

## 1. Four-block Haar complement

Let `B_0,...,B_3` be consecutive nonempty blocks with lengths
`s_0,...,s_3` and `N=sum_j s_j`.  The blockwise scaling vector is
`a=(1,1,1,1)`.  The three contrasts inherited from TPC-257 are

```text
z0 = rho0(1/(s0+s1),1/(s0+s1),-1/(s2+s3),-1/(s2+s3)),
z1 = rho1(1/s0,-1/s1,0,0),
z2 = rho2(0,0,1/s2,-1/s3),
```

where `rho0^2=(s0+s1)(s2+s3)/N`,
`rho1^2=s0s1/(s0+s1)`, and `rho2^2=s2s3/(s2+s3)`.
Counting with the weighted block inner product gives an orthonormal family.
Each contrast has weighted sum zero, so `a` is orthogonal to all three.
Thus the missing fourth Haar mode is the scaling direction
`e_scale=a/sqrt(N)`.

The TPC-258 vector

```text
z_null=(L2 z1-L1 z2)/sqrt(L1^2+L2^2),
L1=log(3456/3125), L2=log(884736/823543),
```

is also orthogonal to `e_scale`.

## 2. Null-compatible packet class

Fix a unit pair `z,w` with `<z,w>=0`, and nonnegative packet lengths
`d_0,...,d_3`.  Let

```text
D=sum_j d_j,
d_max=max_j d_j,
r_min=max(2*d_max-D,0),
r_max=D.
```

For phases `theta_j`, take `V_j=d_j exp(i theta_j) w`.  Then every packet
has norm `d_j`, every contrast orthogonal to `w` sees zero, and

```text
<w,sum_j V_j> = sum_j d_j exp(i theta_j).
```

The polygon theorem says that the possible modulus of this sum is exactly
`[r_min,r_max]`.  The lower endpoint is the long-side obstruction; the upper
endpoint is the aligned family.

## 3. Four-packet mode ledger

Define the unitary four-point DFT

```text
Vhat_k = 1/2 sum_(j=0)^3 i^(-jk) V_j,  k=0,1,2,3.
```

Finite Parseval and inversion give

```text
sum_k ||Vhat_k||^2 = sum_j ||V_j||^2,
sum_j V_j = 2 Vhat_0,
||sum_j V_j||^2 = 4 ||Vhat_0||^2.
```

Thus packet diagonal energy fixes only the sum of mode energies.  The target
full reassembly is specifically the unobserved mode `k=0`.

For `V_j=w`, mode zero has energy `4` and the full energy is `16`.  For
`V_j=(-1)^j w`, mode two has energy `4`, mode zero is zero, and the full
energy is zero.  Both families have packet diagonal `(1,1,1,1)`.

## 4. Literal interpretation

The four `V_j` represent the four phase-labelled outputs after the common
V59 transform; any external scalar coefficients can be absorbed into the
packet definition.  The construction is a compatibility audit, not a claim
that the synthetic packets equal the prime shell.  A literal completion must
control the mode-0 cross-Gram sum while retaining the hard window, deleted
diagonal, unit masks, and `w_perp`.
