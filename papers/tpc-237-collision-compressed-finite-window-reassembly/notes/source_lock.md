# TPC-237 source lock

Baseline:

```text
HEAD = 2cda3928ed2dcc66d2e2fc276b3c869ea2475376
TPC_HANDOFF_SHA256 = 64315a4c8b853a3d6348caf40b60817e7479fc5bf86ccbf0d903b9e34d470446
```

Frozen object:

```text
H=x^(21/32), Q=x^(1/3), U=x^(133/400),
Q_x={q prime:Q<q<=2Q},
D_x={d:H/(4Q)<d<=U, mu(d)^2=1},
C_h=sum_(d in D_x,h|d) mu(d)log(d)/d,

B_(h,q)^(j)(a)
 = sum_(0<|m|<=floor(hq/H))
     psi_j(Hm/(hq)) 1_(m q^(-1)=a mod h),

K_j(n)
 = sum_(h<=U) sum_(a mod h,(a,h)=1)
     C_h (sum_(q in Q_x) B_(h,q)^(j)(a)) e(na/h).
```

Mandatory interface values:

```text
q weight = 1
packet-dependent transform = NONE
row-dependent normalization = NONE
outer coefficient = literal signed C_h
frequency representatives = primitive a/h only
output normalization = N^(-1)
```

The theorem may use TPC-236 only after restricting to primitive coordinates, where
`g=(a,h)=1`.  The additive large sieve must receive those reduced primitive pairs;
unreduced residues are an invalid input because they duplicate rational frequencies.

The finite certificate uses `mu(d)/d` solely to make the marked-divisor fixture exact
over `Fraction`.  It is labeled reproduction and is not substituted for the literal
`mu(d)log(d)/d` theorem coefficient.
