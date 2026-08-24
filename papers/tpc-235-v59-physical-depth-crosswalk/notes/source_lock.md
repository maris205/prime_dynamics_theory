# TPC-235 source lock

The physical formulas are frozen from V59 and TPC-218:

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
B_(h,q)(a)=sum_m psi(Hm/(hq)) 1_(m q^(-1)=a mod h),
C_h=sum_(d:h|d) mu(d)log(d)/d,
K_q(n)=sum_(h,a) C_h B_(h,q)(a)e(na/h).
```

Packet source lock:

```text
a^(j)=beta+i^j w,
one common physical transform/profile for all j,
1/4 sum_j i^j ||T a^(j)||^2 = <T beta,T w>.
```

TPC-226's `H=4Q^2`, `h=4LQ` is a finite surrogate modeling choice.  TPC-234's unit
normalization is a valid structural transform but is not licensed inside V59 unless a
common input-independent linear weight is carried through the complete source ledger.
