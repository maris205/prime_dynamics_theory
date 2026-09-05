# Derivation package

Write `D_p(u)=1_{p not divide u}` and `b_sigma(u)=sum_{p|u}sigma_p a_p`.
For distinct points in a production window, `p>N` prevents a prime from
dividing both points. Expanding the endpoint terms gives
`sum sigma_p a_p D_p(u)D_p(v)=A_sigma-b_sigma(u)-b_sigma(v)`, hence
`M_sigma(u,v)=T_uv[-A_sigma+b_sigma(u)+b_sigma(v)]`. This is exact for the
finite production domain and gives no arithmetic meaning to `sigma`.
