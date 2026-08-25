# Proof Package

## Theorem 1: exact binary refinement calculus

Let `H=C^I`, with `I` finite and nonempty and inner product conjugate-linear
in the first slot. Let `P` be an exhaustive partition into nonempty coordinate
blocks and let `M_P` be the block-averaging orthogonal projection. Fix `w,g`
with `g=A_x beta`, and define

```text
C_long(P)=<M_P w,M_P g>,
Q_trans(P)=<(I-M_P)w,(I-M_P)g>,
R_trans(P)=sum_(J in P)||w_J^perp||||g_J^perp||.
```

Suppose `P'` splits `J` into `J1,J2`. With `n_i=|J_i|`, `n=n1+n2`, put

```text
z=sqrt(n2/(n1 n))1_J1-sqrt(n1/(n2 n))1_J2.
```

Then

```text
M_P'=M_P+z tensor z,
C_long(P')=C_long(P)+conjugate(<z,w>)<z,g>,
Q_trans(P')=Q_trans(P)-conjugate(<z,w>)<z,g>,
R_trans(P')<=R_trans(P).
```

### Proof

Let `u_K=|K|^(-1/2)1_K`. The support sizes give

```text
||z||^2=n1*n2/(n1 n)+n2*n1/(n2 n)=1.
```

Also

```text
<u_J,z>
=n^(-1/2)[n1 sqrt(n2/(n1 n))-n2 sqrt(n1/(n2 n))]=0.
```

Both `u_J` and `z` are constant on each child, and they are an orthonormal
basis for the two-dimensional child-flat space. Therefore the new averaging
range is the old range orthogonally enlarged by `span{z}`. This proves the
projector update.

Write `Z=z tensor z`. Since `M_P Z=Z M_P=0`,

```text
<M_P'w,M_P'g>
=<M_Pw,M_Pg>+<Zw,Zg>
=C_long(P)+conjugate(<z,w>)<z,g>.
```

The old transverse range is the orthogonal direct sum of `span{z}` and the
new transverse range. Consequently

```text
<(I-M_P')w,(I-M_P')g>
=<(I-M_P)w,(I-M_P)g>-<Zw,Zg>,
```

which is the claimed `Q_trans` formula.

Only the split block can change the radius. Let `w_i^perp,g_i^perp` be the
child residuals and set

```text
x0=|<z,w>|, xi=||w_i^perp||,
y0=|<z,g>|, yi=||g_i^perp||.
```

Pythagoras gives old parent norms

```text
||w_J^perp||^2=x0^2+x1^2+x2^2,
||g_J^perp||^2=y0^2+y1^2+y2^2.
```

The refined contribution is `x1 y1+x2 y2`. Hence

```text
x1 y1+x2 y2
 <=sqrt(x1^2+x2^2)sqrt(y1^2+y2^2)
 <=sqrt(x0^2+x1^2+x2^2)sqrt(y0^2+y1^2+y2^2).
```

Adding the unchanged block contributions proves radius monotonicity. QED.

## Proposition 2: projected Gram update for a fixed family

Fix vectors `v_1,...,v_m` independently of the partition and set

```text
G_P^perp(i,j)=<(I-M_P)v_i,(I-M_P)v_j>.
```

Under the binary split of Theorem 1,

```text
G_P'^perp(i,j)
=G_P^perp(i,j)-conjugate(<z,v_i>)<z,v_j>.
```

### Proof

Since `z` lies in the old transverse range and
`I-M_P'=(I-M_P)-z tensor z`, each new residual equals the old residual minus
`z<z,v_i>`. Expanding its Gram pairing and using orthogonality leaves exactly
the displayed rank-one subtraction. QED.

### Scope firewall

The proposition does not compare the native TPC-251 Gram arrays after a
common input/output repartition. Those probes are
`v_cb=P_c A_x P_b beta`; refinement changes the labels `b,c`, the number of
probes, and their vectors. No canonical matrix identification is supplied.

## Corollary 3: universal singleton collapse

For the singleton partition `S`, every projected native probe and every
projected Gram entry is zero. For every output singleton,

```text
D=L=mu=U=0.
```

Globally,

```text
Q_trans(S)=R_trans(S)=R_coh(S)=0,
C_long(S)=C_x.
```

The TPC-250 parameter `kappa` is undefined, not zero, because `D=0`.

### Proof

Block averaging on singleton coordinates is the identity, so every
transverse projection is zero. All listed probe, Gram, and scalar
consequences follow immediately. The `mu=0` value is TPC-250's fewer-than-two
active-probe convention; its normalized `kappa=L^2/D` is not formed. QED.

## Theorem 4: declared-partition margin optimality

For every fixed `E>=0`, over all exhaustive nonempty declared partitions of
`I`,

```text
max_P [|C_long(P)|-R_coh(P)-E]_+=[|C_x|-E]_+.
```

### Proof

TPC-251 gives

```text
|C_x-C_long(P)|<=R_coh(P).
```

Thus `|C_long(P)|<=|C_x|+R_coh(P)`, or
`|C_long(P)|-R_coh(P)<=|C_x|`. The positive-part map is monotone, so every
partition margin is at most `[|C_x|-E]_+`. Corollary 3 shows that the singleton
partition has `C_long=C_x` and `R_coh=0`, attaining this upper bound. Since
`I` is finite, the legal partition family is finite and the maximum exists.
QED.

## Proposition 5: existential non-invariance and failure of universality

On `C^2`, let

```text
A=[[0,1],[1,0]], beta=(-1,1), w=(1,-1).
```

Then `g=A beta=(1,-1)` and `C_x=2`. For the one-block partition,

```text
C_long=0, Q_trans=2, R_trans=R_coh=2.
```

For the singleton partition,

```text
C_long=2, Q_trans=R_trans=R_coh=0.
```

Thus the decomposition metrics are partition-dependent even though
`A,beta,w` are fixed and unchanged.

### Proof

Both vectors have zero coarse average, so the coarse longitudinal term is
zero and the full scalar is transverse. There is one active coarse projected
probe, so `mu=0`, `D=2`, `L=sqrt(2)`, `U=sqrt(2)`, and the product with
`||w^perp||=sqrt(2)` gives `R_coh=2`. Corollary 3 gives all singleton values.
QED.

This fixture is synthetic and not a literal V59 arithmetic instance. It is an
existence statement, not an every-source claim. Indeed, with the same swap
matrix but `beta=(1,1)` and `w=(2,2)`, both partitions have `C_long=C_x=4`
and zero transverse terms. Universal source instability is therefore
refuted.

## Audit conclusion

The proved ceiling is finite structural L1. `R_trans` monotonicity does not
promote to an `R_coh` monotonicity claim. No actual V59 coarse nonzero
contrast, canonical partition, asymptotic estimate, arithmetic saving, L2,
Route A, fixed-atom credit, Gate-B closure, strict `1/400`, or twin-prime
statement follows.
