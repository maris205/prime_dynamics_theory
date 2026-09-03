# TPC-364 derivation package

Let `I=[x,x+N-1]` and let `Q<p<=2Q` range over the literal prime shell.  The
base block is

`B_p(u,t)=p K_s(u-t)(1_{p|(u-t)}-1/(p-1))
  1_{u!=t}1_{p not|u}1_{p not|t}`,

where `K_s(d)=66^(2s)/(66^2+d^2)^s`.  For an integer beta define

`w_(p,beta)=(p/Q)^beta`,
`B_(p,beta)=w_(p,beta)B_p`, and
`A_(beta,epsilon)=sum_p epsilon_p B_(p,beta)`.

The geometry diagonal is

`G_(beta,u)=sum_p sum_t B_(p,beta)(u,t)^2`.

Every term is a square of a rational number in the exact finite model.  The
certificate checks `G_(beta,u)>0` for every declared row, so
`D_(G,beta)^(-1/2) A_(beta,epsilon) D_(G,beta)^(-1/2)` is a finite real
symmetric matrix.  The two exact finite envelopes used in the audit are

`||T||_2 <= max_u sum_t |T(u,t)|`,
`||T||_2 <= (sum_(u,t)|T(u,t)|^2)^(1/2)`.

The beta menu is symmetric around the inherited beta=0 normalization.  Since
the phase diagram reports every member of the menu, the beta=2 statement is
descriptive on the frozen panel; it is not a data-independent selection
claim.  The dimensionless effective shell count recorded in the certificate
is `(sum_p w_p^2)^2/(sum_p w_p^4)`, a diagnostic against interpreting the
repair as a one-prime truncation.
