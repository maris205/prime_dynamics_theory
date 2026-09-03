# TPC-365 derivation package

Let `I=[x,x+N-1]` and let `Q<p<=2Q` range over the literal prime shell.  The
masked base block is

`B_p(u,t)=p K_s(u-t)(1_{p|(u-t)}-1/(p-1))
  1_{u!=t}1_{p not|u}1_{p not|t}`,
`K_s(d)=66^(2s)/(66^2+d^2)^s`.

For an integer beta define

`w_(p,beta)=(p/Q)^beta`,
`B_(p,beta)=w_(p,beta)B_p`,
`A_(beta,epsilon)=sum_p epsilon_p B_(p,beta)`.

The weighted geometry diagonal is

`G_(beta,u)=sum_p sum_t B_(p,beta)(u,t)^2`.

The finite normalized matrix is

`A_(beta,epsilon)^# = D_G^(-1/2) A_(beta,epsilon) D_G^(-1/2)`,

where `D_G=diag(G_(beta,u))`.  Every geometry term is a square of a rational
number in the exact finite model.  The certificate checks positivity for
every audited row.  Consequently the symmetric congruence is well-defined,
and the finite envelopes

`||T||_2 <= max_u sum_t |T(u,t)|`,
`||T||_2 <= (sum_(u,t)|T(u,t)|^2)^(1/2)`

apply without an asymptotic assumption.

## Response-blind selection functional

For a candidate origin `a`, use the pilot values
`I_a^pilot=[a,a+255]`.  For each declared `(Q,s)`, calculate the unsigned
weighted geometry with beta=2 and set

`S(a)=max_(Q,s) max_u G_(2,u)/min_u G_(2,u)`.

Sort candidates by decreasing `S(a)` with origin as the exact tie-break, then
greedily retain a candidate only when it is at least `2048` away from every
previously retained origin.  This finite rule yields
`(413342,410258,416940)`.  It uses no sign law, signed matrix, source vector,
or response value.  It is therefore response-blind, while remaining a
deterministic geometry-based finite selection rather than a random-sampling
claim.

The holdout then evaluates both beta=0 and the predeclared beta=2 on the same
three selected origins, both counts, all four shell anchors, both exponents,
and all four fixed laws.  No beta is chosen after seeing holdout spectra.

## Parent transfer statistic

The TPC-364 beta=2 maximum normalized spectrum was
`0.61628753962786131`.  The fresh-panel maximum is
`0.61633188509480319`, so the signed difference is
`0.000044345466941875245`, below the declared transfer tolerance `0.001`.
This comparison is a finite diagnostic, not a uniform-in-origin statement.
