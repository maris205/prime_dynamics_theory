# Proof Package

## Theorem

Fix a finite admissible `K`, put `Z_x=(log x)^K`, and let
`w(u)=Lambda(u+2)-b_x^(Z_x)(u)`. For the ordered rank midpoint of TPC-253 and
every fixed `M>0`, as real `x` tends to infinity,

```text
max(|W_L|,|W_R|) <<_(M,K) x/(log x)^M,
|W_L/ell-W_R/r| <<_(M,K) (log x)^(-M),
|<z_mid,w>| <<_(M,K) x^(1/2)(log x)^(-M).
```

Moreover,

```text
|conjugate(<z_mid,w>)<z_mid,A_x beta>|
 <<_(M,K) x^(1/2)(log x)^(-M)||A_x^*z_mid||_2||beta||_2.
```

No bound beyond Cauchy is asserted for the second moment.

## Proof

Freeze `gamma_0=1/4`. The locked H2 maximal Type-I theorem applies for every
fixed exponent below `1/2` and every requested fixed logarithmic strength.
Choose its integer saving parameter sufficiently strongly for the target
`M`. Its left side is a sum over `m<=x^gamma_0` of nonnegative quantities.
For all sufficiently large `x`, the `m=1` term is present and its divisor
weight is `tau(1)^B=1`. Therefore every active consecutive interval `J`
satisfies

```text
|sum_(u in J)w(u)| <<_(M,K) x/(log x)^M.
```

The rank children are exactly the consecutive intervals

```text
L={floor(x/2)+1,...,floor(x/2)+ell},
R={floor(x/2)+ell+1,...,floor(x)}.
```

Taking `J=L,R` proves the first bound. Since
`N=floor(x)-floor(x/2)=x/2+O(1)` and `ell,r=x/4+O(1)`, both child sizes are
bounded below by a positive multiple of `x` for large `x`. Dividing the two
child bounds and using the triangle inequality proves the second estimate.

The exact TPC-253 Haar identity is

```text
<z_mid,w>=rho(W_L/ell-W_R/r), rho^2=ell*r/N.
```

The elementary inequality `ell*r<=N^2/4` gives `rho<=sqrt(N)/2<<sqrt(x)`.
Multiplying by the second estimate proves the third. The sharper parity
ledger follows by writing `ell=r=N/2` for even `N` and
`ell=(N-1)/2`, `r=(N+1)/2` for odd `N`.

Finally, the finite-dimensional adjoint identity and Cauchy give

```text
|<z_mid,A_x beta>|=|<A_x^*z_mid,beta>|
                  <=||A_x^*z_mid||_2||beta||_2.
```

Multiplication by the third estimate proves the safe transfer. This step
contains no estimate of `A_x^*z_mid` and no lower bound. QED.

## Sharpness proposition

Let `N>=2`, let `z` be a real unit vector, and let `sigma` be a derangement.
For real `lambda`, define `A_(i,sigma(i))=lambda z_i`, all other entries zero,
and `beta=1`. Then `A` is real and zero diagonal, while each row sum is
`lambda z_i`; hence `A beta=lambda z` and `<z,A beta>=lambda`.

For `N=2`, take

```text
z=(1/sqrt(2),-1/sqrt(2)),
A=[[0,lambda/sqrt(2)],[-lambda/sqrt(2),0]], beta=(1,1).
```

Direct multiplication gives `A^*z=(lambda/2,lambda/2)`. Therefore

```text
||A^*z||_2^2=lambda^2/2,
||beta||_2^2=2,
|<z,A beta>|^2=lambda^2,
```

and Cauchy is an equality. The proposition is synthetic and says nothing
about realization by the literal V59 operator.

## Open theorem

Estimate the exact literal form

```text
sum_(t in I_x) conjugate((A_x^*z_mid)(t)) beta(t)
```

on the same V59 clock while retaining the prime shell, outer `q` weight, both
unit masks, deleted diagonal, `K_H`, centered residue bracket, and hard rank
midpoint, with a declared improvement over Cauchy.
