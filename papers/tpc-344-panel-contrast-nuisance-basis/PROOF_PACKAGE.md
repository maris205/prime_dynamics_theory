# TPC-344 proof package

## Proposition 1 — finite contrast reparameterization

For any pair of finite panel nuisance columns `n_1` and `n_2`, define

```text
b=(n_1,n_2),       d=(n_1,-n_2),
u_1=(b+d)/2,       u_2=(b-d)/2.
```

Then `u_1=(n_1,0)`, `u_2=(0,n_2)`, and

```text
span{b,d}=span{u_1,u_2}.
```

### Proof

The displayed formulas give `u_1,u_2` as linear combinations of `b,d`.
Conversely `b=u_1+u_2` and `d=u_1-u_2`.  Each span contains the other.
Applying the argument independently to the three nuisance categories proves
the six-column identity used by TPC-344.  This is an exact statement about
finite vectors.

## Proposition 2 — finite projection identity

For every finite real matrix `N` and vector `Y`,

```text
||Y||_2^2 = ||P_NY||_2^2 + ||(I-P_N)Y||_2^2.
```

### Proof

`P_NY` lies in the column space of `N`, while `(I-P_N)Y` lies in its
orthogonal complement.  Their sum is `Y`, so the Pythagorean theorem applies.
The implementation computes the same projector from the positive singular
vectors and checks the decomposition gap.

## Proposition 3 — finite computational certificate

Conditional on the hash-locked source/operator implementation and the
canonical certificate, the producer and the independently implemented
reverse-shell checker reproduce:

```text
216 raw records, 171 nonempty records, six in-sample rows,
18 contrast holdouts, and four directional crossfits.
```

The raw contrast residual retention is
`0.29621892474890171`, while equal-row contrast retention is
`0.31865066996095742`.  The combined contrast holdout range is
`0.6372238668391691--0.91285435474891141`, and the cross-fit prediction range
is `0.37594867338366317--0.63429341965475916`.

This proposition is a finite numerical certification, not an asymptotic
theorem.  Its arithmetic credit is zero.

## Explicit non-implications

The package does not prove a source-uniform `L2` estimate, a canonical
nuisance basis, a uniform masked operator bound, a strict `1/400` loss
payment, a Route-A/Route-B evaluator pass, or the twin-prime conjecture.
