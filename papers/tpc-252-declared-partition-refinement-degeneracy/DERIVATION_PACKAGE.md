# Derivation Package

## 1. Frozen source object

Let `H=C^I`, where `I` is finite and nonempty, and use an inner product that
is conjugate-linear in its first slot. Freeze

```text
g=A_x beta,                 C_x=<w,g>.
```

For an exhaustive partition `P` of `I` into nonempty coordinate blocks, let

```text
u_J=|J|^(-1/2) 1_J,
M_P=sum_(J in P) u_J tensor u_J,
(u tensor u)h=u<u,h>.
```

Thus `M_P` is the orthogonal block-averaging projection. Define

```text
C_long(P)=<M_P w,M_P g>,
Q_trans(P)=<(I-M_P)w,(I-M_P)g>.
```

Orthogonality gives `C_x=C_long(P)+Q_trans(P)`. For the literal TPC-247
source, this is the global form of the TPC-251 declared-block split with
`lambda_cb=1`.

## 2. One binary split

Suppose `P'` replaces one block `J` by disjoint nonempty blocks `J1,J2`.
Write `n_i=|J_i|` and `n=n1+n2`, and set

```text
z=sqrt(n2/(n1 n)) 1_J1 - sqrt(n1/(n2 n)) 1_J2.
```

The two coefficient squares sum to one after multiplication by their support
sizes, so `||z||=1`. Direct summation gives `<u_J,z>=0`. The two child-flat
directions span the orthogonal direct sum of the old flat direction and the
contrast:

```text
span{u_J1,u_J2}=span{u_J} direct_sum span{z}.
```

All other block-flat directions are unchanged. Hence

```text
M_P'=M_P+z tensor z.
```

## 3. Exact covariance transfer

The old flat range and `span{z}` are orthogonal. Therefore

```text
C_long(P')
 = C_long(P)+<z<z,w>,z<z,g>>
 = C_long(P)+conjugate(<z,w>)<z,g>.
```

Since `I-M_P'=(I-M_P)-z tensor z` and `z` lies in the old transverse
range,

```text
Q_trans(P')
 = Q_trans(P)-conjugate(<z,w>)<z,g>.
```

The two changes cancel, as they must because `C_x` is fixed.

## 4. Exact transverse-radius monotonicity

For the split parent, decompose the old transverse vectors into the contrast
and the two child-transverse pieces:

```text
w_J^perp=z<z,w>+w_1^perp+w_2^perp,
g_J^perp=z<z,g>+g_1^perp+g_2^perp.
```

The three summands in each line are mutually orthogonal. Put

```text
x0=|<z,w>|,  xi=||w_i^perp||,
y0=|<z,g>|,  yi=||g_i^perp||  (i=1,2).
```

The old parent contribution and the new child contributions are respectively

```text
sqrt(x0^2+x1^2+x2^2)sqrt(y0^2+y1^2+y2^2),
x1 y1+x2 y2.
```

Cauchy--Schwarz on the two child coordinates, followed by inclusion of the
nonnegative contrast energies, proves that the second is at most the first.
All untouched blocks have identical contributions, so

```text
R_trans(P')<=R_trans(P).
```

This derivation makes no statement about `R_coh`: native probe indexing,
projected norms, and coherence can all change under common input/output
repartition.

## 5. Fixed-probe projected Gram scope

For a fixed, unchanged family `(v_i)`, define

```text
G_P^perp(i,j)=<(I-M_P)v_i,(I-M_P)v_j>.
```

Then the same orthogonal subtraction gives

```text
G_P'^perp(i,j)
 =G_P^perp(i,j)-conjugate(<z,v_i>)<z,v_j>.
```

This statement is only for a fixed family. The native TPC-251 probes are
`v_cb=P_c A_x P_b beta`; repartition changes both input and output labels and
the vectors themselves. Their before/after arrays are not identified by this
rank-one formula.

## 6. Singleton endpoint

For the singleton partition `S`, block averaging is the identity:

```text
M_S=I.
```

Every native output block is one-dimensional, so every projected probe is
zero. Consequently its projected Gram, `D,L,mu,U` all vanish; TPC-250 sets
`mu=0` because there are fewer than two active probes, and `kappa` is not
formed at `D=0`. Globally,

```text
Q_trans(S)=R_trans(S)=R_coh(S)=0,
C_long(S)=C_x.
```

This applies to every finite literal TPC-247 source scalar.

## 7. Margin optimality

TPC-251 gives `|C_x-C_long(P)|<=R_coh(P)`. Hence

```text
|C_long(P)|-R_coh(P)<=|C_x|.
```

For fixed `E>=0`, subtract `E` and apply the positive-part map. This bounds
every partition margin by `[|C_x|-E]_+`. The singleton partition attains the
bound, proving

```text
max_(legal P) [|C_long(P)|-R_coh(P)-E]_+=[|C_x|-E]_+.
```

The maximization is finite because `I` is finite. The external error remains
an independently certified input and is held fixed while partitions vary.

## 8. Existential same-source witness

On two coordinates take

```text
A=[[0,1],[1,0]], beta=(-1,1), g=(1,-1), w=(1,-1).
```

For the one-block partition,

```text
C_long=0, Q_trans=2, R_trans=R_coh=2.
```

For the singleton partition,

```text
C_long=C_x=2, Q_trans=R_trans=R_coh=0.
```

The unchanged `A,beta,w` therefore yields partition-dependent decomposition
metrics. This is a
`SYNTHETIC_EXACT_FINITE_SOURCE_OPERATOR_REPLAY_NOT_A_LITERAL_V59_ARITHMETIC_INSTANCE`.
It is existential only. With the same swap `A`, taking `beta=(1,1)` and
`w=(2,2)` gives identical coarse and fine values, refuting every-source
instability.

## 9. Boundary ledger

- No `R_coh` refinement monotonicity is derived.
- No actual V59 coarse nonzero contrast is proved.
- No declared partition is selected canonically or arithmetically.
- The finite certificates reproduce structural algebra only.
- Arithmetic status, L2, Route A, Gate B, strict `1/400`, fixed-atom credit,
  and the twin-prime status are unchanged.
