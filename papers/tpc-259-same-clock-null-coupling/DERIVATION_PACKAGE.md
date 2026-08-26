# TPC-259 derivation package

## 1. Same-clock object

Use the literal V59 clock and four blocks from TPC-258.  Let `z0,z1,z2` be
the exact orthonormal Haar frame and set

```text
L1=log(3456/3125), L2=log(884736/823543),
LT=sqrt(L1^2+L2^2),
z=(L2 z1-L1 z2)/LT.
```

The vector `z` is source-frozen, unit, and orthogonal to `z0`.  It is not
chosen after observing `w`, `beta`, or the output.

## 2. Four-block `w` control

TPC-254 extracts from the nonnegative maximal Type-I sum, at fixed
`gamma_0=1/4`, that every fixed consecutive interval `J` in `I_x` satisfies

```text
|sum_(n in J) w(n)| <<_(M,K) x/(log x)^M.
```

Each of the four source blocks is such an interval.  If `W_j` is its sum and
`rho_j` is the adjacent-block normalization, then

```text
<z1,w>=rho_1(W_1/s1-W_2/s2),
<z2,w>=rho_2(W_3/s3-W_4/s4).
```

Since all block sizes are comparable to `x`, this gives

```text
|<z1,w>|+|<z2,w>| <<_(M,K) sqrt(x)/(log x)^M,
|<z,w>| <<_(M,K) sqrt(x)/(log x)^M.
```

This is a source-backed extension of the TPC-254 child estimate, not a new
claim of uniformity in `M`, `K`, or the clock family.

## 3. Exact rank-one decomposition

For the Hilbert inner product `ip(f,g)=sum conjugate(f)g`, let

```text
c_z=<z,w>, w_parallel=c_z z, w_perp=w-c_z z.
```

Because `w` and `z` are real, `c_z` is real in the literal model, but the
complex-safe identity is

```text
<w,A_x beta>=conjugate(c_z)<z,A_x beta>+<w_perp,A_x beta>.
```

The first summand is the null-channel contribution.  This equality is exact
for every finite clock and every linear operator; no symmetry of the kernel
is needed.

## 4. Coupling suppression

TPC-258 gives

```text
<z,A_x beta>=o(S_x), S_x=x^(7/6)/log^3(x).
```

Multiplying by the source-backed `w` estimate yields, for every fixed `M`,

```text
conjugate(<z,w>)<z,A_x beta>
 =o(x^(5/3)/log^(M+3) x).
```

If the conditional TPC-258 scalar rate is available, then

```text
|null_channel|
 << x^(5/3)/log^(M+4) x
    +x^(79/48+epsilon)/log^M x.
```

The exponent `79/48` is `1/2+55/48`; the residual boundary gap remains
`1/48` relative to `5/3=80/48`.

## 5. Residual obstruction

The exact identity leaves
`<w_perp,A_x beta>`.  A finite real zero-diagonal witness is

```text
z=(1,0), w=(0,1), beta=(1,0),
A=[[0,0],[lambda,0]];
```

Then `w_perp=w`, the null channel is zero, but
`<w,A beta>=lambda`.  Thus null-channel suppression alone cannot be promoted
to a full signed coupling theorem.  This is a synthetic structural witness,
not a literal V59 counterexample.

## 6. Route decision

TPC-259 pays one precise rank-one same-clock channel and identifies the exact
unpaid residual.  The next natural audit is full four-packet signed
reassembly, with this residual treated as an input rather than silently
discarded.  `L2=NONE`, `FULL_GATE_B=OPEN`, and strict global `1/400` remains
unpaid.
