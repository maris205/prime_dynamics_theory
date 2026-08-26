# TPC-268 derivation package

Author: Liang Wang, School of Mathematics and Statistics, Huazhong University of Science and Technology (HUST)

Let I_N=(N/2,N] and let Q<q<=2Q range over primes. For an integer
z>=2, define the finite comparison

~~~text
b_N^(z)(u)=C_2^(z) 1_(2 does not divide u)
             product_(p<=z) p/(p-1)
             product_(p|u,p>z) (p-1)/(p-2),
~~~

with the value set to zero when (u+2) has a prime factor at most z.
Here C_2^(z)=product_(p>z)(1-(p-1)^(-2)), enclosed by the same finite
Euler product and positive tail bound as TPC-267. Thus z=2 is the
TPC-267 comparator; larger z are explicitly declared finite perturbations.

The source is

~~~text
beta_N(t)=Lambda(t)/log(t)-sum_(d|t,d^400<=N^133) mu(d),
~~~

and w_N(u)=Lambda(u+2)-b_N^(z)(u). The operator is

~~~text
A(u,t)=1_(u!=t) sum_(Q<q<=2Q) q K_(H,s)(u-t) 1_(q does not divide ut)
       (1_(u=t mod q)-1/(q-1)),
K_(H,s)(h)=(1+(h/H)^2)^(-s).
~~~

Let P_3 be the three orthogonal four-block contrasts from TPC-267,
g=A beta, and

~~~text
C=<w,g>=C_3+C_perp,
R^2=||(I-P_3)w||^2 ||(I-P_3)g||^2,
rho^2=|C_perp|^2/R^2.
~~~

All non-logarithmic terms are rational. Decimal logarithm intervals and the
Euler tail are rounded outward to a rational grid. A row is a certified
contraction when rho^2_hi<1/16, and a certified obstruction when
rho^2_lo>1/16.

The matched central pair is

~~~text
(N,H,Q,s,z)=(64,15,4,1,2): rho_hi=0.2320126753,
(N,H,Q,s,z)=(64,15,4,1,3): rho_lo^2=0.0748091943191>1/16.
~~~

The second line is a finite cutoff obstruction. It does not assert that
z=3 is the asymptotic source cutoff.
