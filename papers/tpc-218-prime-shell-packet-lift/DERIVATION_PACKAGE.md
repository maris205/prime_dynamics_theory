# TPC-218 Derivation Package

## Frozen scales

~~~
H=x^(21/32), Q=x^(1/3), Y0=H/(4Q), U=x^(133/400),
P=# {q prime: Q<q<=2Q} <= 2Q.
~~~

The useful gaps are

~~~
Q^2/H=x^(1/96),
Q^3/H=x^(11/32),
U^2/x=x^(-67/200),
UQ/H=x^(23/2400).
~~~

## Split object

~~~
B_(h,q)^(j)(a)=sum_m psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h),
C_h=sum_(d:h|d) mu(d)log(d)/d,
K_(j,q)(n)=sum_(h,a primitive) C_h B_(h,q)^(j)(a)e(na/h).
~~~

For distinct atoms in one fixed-q row, 4Q<H implies no collision. Hence

~~~
sum_a |B_(h,q)^(j)(a)|^2 <= 2 M^2 hq/H.
~~~

An active row has h>=H/(2Q), so writing d=hk gives
k<=2UQ/H. The unsigned divisor estimate is

~~~
|C_h| << (log x)^2/h,
sum_h h|C_h|^2 << (log x)^5.
~~~

## Tensor large sieve

Reduced frequencies are U^(-2) separated. With
v_(h,a)=(C_h B_(h,q)^(j)(a))_(q,j), coordinatewise additive large sieve gives

~~~
sum_I ||K_vec||^2
 <= (N+U^2) sum_(h,a)||v_(h,a)||^2
 << (N+U^2) J M^2 (Q^2/H)(log x)^5.
~~~

After dividing by N, this is the split exponent 1/96.

## Collapse ledger

~~~
sum_j|sum_q K_(j,q)|^2
 <= P sum_(j,q)|K_(j,q)|^2,
P<=2Q.
~~~

Thus the scalar exponent is 1/96+1/3=11/32, exactly the TPC-217 envelope.
The finite q-alignment fixture proves that this structural P payment cannot be
deleted by a generic orthogonality assertion.

## Packet matrix

The packet Gram G_I is PSD and omega^*G_I omega<=tr(G_I). The four-point
identity

~~~
x overline(y)=1/4 sum_(j=0)^3 i^j |x+i^j y|^2
~~~

keeps the exact polarization interface, but the trace is unsigned. No signed
arithmetic saving is claimed.
