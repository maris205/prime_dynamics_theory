# TPC-366 derivation package

Let `I=[x,x+N-1]` and let `Q<p<=2Q` range over the literal prime shell.  The
masked block is

`B_p(u,t)=p K_s(u-t)(1_{p|(u-t)}-1/(p-1))
  1_{u!=t}1_{p not|u}1_{p not|t}`,

where `K_s(d)=66^(2s)/(66^2+d^2)^s`.  For integer beta, put

`w_(p,beta)=(p/Q)^beta`,
`B_(p,beta)=w_(p,beta)B_p`, and
`A_(beta,epsilon)=sum_p epsilon_p B_(p,beta)`.

The associated square-energy geometry and normalized matrix are

`G_(beta,u)=sum_p sum_t B_(p,beta)(u,t)^2`,

`A_(beta,epsilon)^#=D_G^(-1/2) A_(beta,epsilon) D_G^(-1/2)`.

The geometry is a finite sum of rational squares.  Positivity on the
declared rows makes the congruence well-defined, and the finite inequalities

`||T||_2 <= max_u sum_t |T(u,t)|`,
`||T||_2 <= (sum_(u,t)|T(u,t)|^2)^(1/2)`

are the only operator inequalities used.

## Higher-Q selection functional

For candidate origin `a`, use the pilot interval `[a,a+255]` and calculate
the beta=2 unsigned geometry for every declared `(Q,s)`.  Define

`S(a)=max_(Q,s) max_u G_(2,u)/min_u G_(2,u)`.

Sort by decreasing `S(a)`, break ties by increasing origin, and greedily keep
an origin only if it is at least `2048` from all previously kept origins.
The finite deterministic output is `(623071,631360,629211)`.  No signed
response or source vector enters this functional.

The selected origins are then held fixed while beta=0 and beta=2 are
evaluated on the same counts, five shell anchors, two exponents, and four
fixed laws.  Thus the higher-Q claim tests scale at a frozen rule rather than
selecting a new beta at each Q.

## Scale statistic

The TPC-365 beta=2 maximum was `0.61633188509480319`; the TPC-366 maximum is
`0.62448287758976528`.  Their difference is
`0.0081509924949620949`.  This finite increase is recorded explicitly: the
ladder is not described as monotone decay, and no tolerance is used to turn
it into a uniform theorem.
