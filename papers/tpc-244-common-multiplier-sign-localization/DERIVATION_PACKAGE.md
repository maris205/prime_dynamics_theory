# TPC-244 derivation package

## 1. Frozen clustered coefficient

The source-locked V59 scales and literal clustered multiplier are

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
C_h=sum_(d in D_x, h|d) mu(d)log(d)/d.
```

TPC-214 proves that reduced rational frequencies must be clustered before the
physical square, producing `|C_h|^2` in an unsigned complete-period energy.
TPC-237 retains primitive representatives exactly once and keeps the same
literal outer `C_h` in every packet.  TPC-228, however, explicitly leaves the
literal `beta,w`-to-primitive-atom crosswalk open.

## 2. Correct invariant object

Let `H_h` be the coefficient coordinates of block `h`.  For local lane vectors
`b_h,w_h` and complex multipliers `C_h`, define

```text
B = direct_sum_h C_h b_h,
W = direct_sum_h C_h w_h.
```

Orthogonality and conjugate-linearity in the first slot give

```text
<W,B> = sum_h conjugate(C_h) C_h <w_h,b_h>
      = sum_h |C_h|^2 <w_h,b_h>.
```

The same calculation gives

```text
||B||^2=sum_h |C_h|^2||b_h||^2,
||W||^2=sum_h |C_h|^2||w_h||^2.
```

Therefore multiplying both lanes in block `h` by one unit scalar `eta_h`
changes none of these three quantities.

## 3. What is and is not erased

The transformation tested above is an **external** blockwise phase:

```text
C_h -> eta_h C_h, |eta_h|=1.
```

It does not alter the summands inside

```text
C_h=sum_(h|d) mu(d)log(d)/d.
```

Changing those internal Möbius signs can change `|C_h|`; the theorem does not
remove or estimate that arithmetic cancellation.  Likewise, if the two lanes
carry different multipliers `C_h^(W)` and `C_h^(B)`, the local factor becomes
`conjugate(C_h^(W)) C_h^(B)` and its phase is visible.

## 4. Nonorthogonal reassembly

Let `J_h:H_h->K` be linear maps into one ambient Hilbert space and put, for
real `C_h` and signs `s_h`,

```text
W(s)=sum_h s_h C_h J_h w_h,
B(s)=sum_h s_h C_h J_h b_h.
```

Writing `M_hk=<J_h w_h,J_k b_k>`, expansion gives

```text
D=sum_h C_h^2 M_hh,
S_hk=C_h C_k(M_hk+M_kh),
Q(s)=<W(s),B(s)>=D+sum_(h<k)s_hs_k S_hk.
```

Relative to the all-positive pattern, exactly the edges cut by `s` change
sign:

```text
Q(s)-Q(1)=-2 sum_(h<k,s_h!=s_k)S_hk.
```

The functions `s_hs_k` are distinct nontrivial Walsh characters.  Hence the
polynomial is constant on the sign cube if and only if every `S_hk` is zero.
For complex baseline multipliers, replace `S_hk` by

```text
conjugate(C_h)C_k M_hk + conjugate(C_k)C_h M_kh.
```

The coefficients `S_hk` may be complex; this is a sensitivity theorem, not an
automatic real-sign theorem.

## 5. Hard-window transfer

TPC-243 supplies, for one common separated-frequency synthesis map `T`,

```text
|N^(-1)<Tu,Tv>-<u,v>| <= epsilon||u||||v||.
```

For common sign or unit-phase patterns in the direct-sum coefficient space,
coefficient covariance and norms are invariant.  Applying the displayed bound
twice and using the triangle inequality yields

```text
|Q_I(s)-Q_I(t)| <= 2epsilon||W||||B||,
Q_I(s)=N^(-1)<TW(s),TB(s)>.
```

At V59 height, `epsilon=x^(-67/200+o(1))`, but the source chain does not yet
bound the coefficient norm product or prove the required two-lane attachment.
No arithmetic saving follows.

## 6. Next invariant

Since the common outer multiplier cannot control the same-block main term, the
next smallest object is the local covariance `<w_h,b_h>`.  A longitudinal /
transverse split inside each block can determine its exact feasible disk from
the two lane energies and their longitudinal moments.  This is the TPC-245
trigger.
