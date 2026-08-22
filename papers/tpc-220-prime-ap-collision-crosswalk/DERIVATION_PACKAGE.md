# Derivation Package

## Target

Rewrite literal prime-labelled row reassembly and its q-Gram in the smallest exact
prime-AP and multiplicative-collision form.

## Status

COHERENT AS STATED

## Invariant Object

The invariant is the weighted row family indexed by `(h,q,j)` and primitive residue `a`.
No q label, cutoff, profile, or primitive condition is discarded.

## Assumptions and notation

- `q` is a prime unit modulo `h`;
- `L_(h,q)=floor(hq/H)` and `M_(h,q)={m:0<|m|<=L_(h,q)}`;
- `w_(h,m,q)^j=psi_j(Hm/(hq))`;
- `a` is primitive modulo `h`.

## Derivation Strategy

Use the equivalence `m q^(-1)=a (mod h) <=> q=a^(-1)m (mod h)` and then expand the
product of two rows. The diagonal and off-diagonal cases are kept separate.

## Derivation Map

1. Unit multiplication gives the AP residue class.
2. Swapping the finite `q,m` sums gives the weighted AP crosswalk.
3. Multiplying two congruences gives `m q'=m' q (mod h)`.
4. For `q=q'`, cutoff injectivity forces `m=m'`.

## Main Derivation

Define

```text
Pi_(h,m)^j(r;lambda)
 = sum_(q in Q_x, q=r mod h, |m|<=hq/H)
       lambda_q psi_j(Hm/(hq)).
```

Then

```text
sum_q lambda_q B_(h,q)^j(a)
 = sum_(m != 0) Pi_(h,m)^j(a^(-1)m;lambda).
```

For the primitive row Gram, expand both finite sums and use uniqueness of the common
primitive residue to obtain

```text
Gamma_h^(j,l)(q,q')
 = sum_(m,m' primitive) w_(h,m,q)^j conjugate(w_(h,m',q')^l)
     1_(m q'=m' q mod h).
```

Setting `q=q'` and using `2L_(h,q)<h` reduces the congruence to `m=m'`.

## Boundaries and Non-Claims

The crosswalk is an identity. It does not bound the off-diagonal collision graph, prove
prime distribution in any residue class, or imply a transverse lower bound.

## Open Risks

The off-diagonal congruence may have coherent families. Its quantitative control is the
next paper's separate question.
