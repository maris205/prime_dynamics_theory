# TPC-236 source lock

Frozen from V59/TPC-218 and TPC-235:

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
B_(h,q)(a)=sum_(0<|m|<=floor(hq/H)) psi(Hm/(hq)) 1_(mq^(-1)=a mod h),
C_h=sum_(d:h|d) mu(d)log(d)/d,
K_q(n)=sum_(h,a) C_h B_(h,q)(a)e(na/h).
```

The TPC-236 Bessel theorem acts before cross-`h` rational-frequency reassembly.  It
does not delete `C_h`, the `h`-sum, packet phases, or profile values.  It does not use
row-dependent unit normalization.  One common linear packet transform may be composed
only with its operator norm explicit.
