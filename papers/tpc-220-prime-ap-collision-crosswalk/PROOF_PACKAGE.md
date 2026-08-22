# Proof Package

## Claim

Fix `h`, a finite prime set `Q`, profiles `psi_j`, and `H>0`. Assume every `q in Q` is
a unit modulo `h`. Let `L_(h,q)=floor(hq/H)` and define

```text
B_(h,q)^j(a)=sum_(0<|m|<=L_(h,q)) w_(h,m,q)^j
                    1_(m q^(-1)=a mod h),
w_(h,m,q)^j=psi_j(Hm/(hq)).
```

For primitive `a`, define the weighted AP sum

```text
Pi_(h,m)^j(r;lambda)
 = sum_(q in Q, q=r mod h, |m|<=L_(h,q)) lambda_q w_(h,m,q)^j.
```

Then

```text
sum_q lambda_q B_(h,q)^j(a)
 = sum_(m != 0) Pi_(h,m)^j(a^(-1)m;lambda).
```

Moreover, if `2L_(h,q)<h` for every `q`, the primitive row Gram satisfies

```text
Gamma_h^(j,l)(q,q')
 = sum_(m,m') w_(h,m,q)^j conjugate(w_(h,m',q')^l)
     1_(gcd(m,h)=gcd(m',h)=1)
     1_(m q'=m' q mod h),
```

and its diagonal is
`Gamma_h^(j,l)(q,q)=sum_(m primitive)|w_(h,m,q)^j|^2` when `j=l`.

## Status

PROVABLE AS STATED

## Assumptions

- all sums are finite;
- `q` is invertible modulo `h`;
- the Gram sum is over primitive residues;
- the diagonal reduction additionally assumes `2L_(h,q)<h`.

## Proof Strategy

Convert the row congruence using the unit inverse, swap finite sums, and expand the Gram.

## Proof

For primitive `a`, multiplication by `q` is legal and gives

```text
m q^(-1)=a (mod h)  <=>  m=a q (mod h)
                         <=> q=a^(-1)m (mod h).
```

Substituting this equivalence into the row definition and interchanging the finite sums
over `q` and `m` yields the AP crosswalk.

For the Gram, multiply the two row indicators. A common primitive residue exists exactly
when both `m` and `m'` are units modulo `h` and
`m q^(-1)=m' (q')^(-1) (mod h)`. Multiplication by `q q'` changes this to
`m q'=m' q (mod h)`, which gives the displayed collision formula.

When `q=q'`, the congruence becomes `m=m' (mod h)`. The two atoms lie in the interval
`[-L_(h,q),L_(h,q)]`, so their difference has absolute value at most `2L_(h,q)<h`.
The only possible congruent pair is therefore `m=m'`, proving the diagonal statement.
Every step is an exact finite rearrangement. ∎

## Corrections or Missing Assumptions

None.

## Open Risks

The theorem isolates, but does not estimate, the off-diagonal collision congruence.
