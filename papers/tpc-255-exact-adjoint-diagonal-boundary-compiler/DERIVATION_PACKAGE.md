# Derivation package

Let

```text
I_x=(x/2,x] intersect Z,
ell=floor(N/2), r=N-ell,
z=rho(1_L/ell-1_R/r), rho^2=ell*r/N.
```

For `q` in the V59 prime shell and `q` not dividing `t`, define

```text
v_(q,t)(u)=1_(q does not divide u)
            [1_(u=t mod q)-1/(q-1)].
```

With the adjoint-oriented kernel, put

```text
P*_(q,t)=sum_(u in Z) conjugate(K_H(u-t))v_(q,t)(u),
E*_(q,t)=sum_(u not in I_x) conjugate(K_H(u-t))v_(q,t)(u),
J*_(q,t)=sum_(u in I_x) conjugate(K_H(u-t))v_(q,t)(u)[z(u)-z(t)].
```

Adding and subtracting `z(t)` on the full lattice and then deleting `u=t`
gives

```text
(A_x^*z)(t)=sum_q q 1_(q does not divide t)
 [z(t)P*_(q,t)-z(t)E*_(q,t)+J*_(q,t)
  -(q-2)/(q-1)conjugate(K_H(0))z(t)].
```

The reflected-conjugate Fourier profile has the same support `[-1,1]`.
V43 with `d=1` therefore yields `P*=0` whenever `H>2Q`; no evenness of
`K_H` is used.  Since `K_H(0)=1`, this leaves the exterior, child-jump, and
deleted-diagonal lanes.

Because

```text
z_L-z_R=rho(1/ell+1/r)=1/rho,
```

the jump is exactly an opposite-child row with coefficient `-1/rho` for
`t in L` and `+1/rho` for `t in R`.

Pairing with real `beta` gives

```text
<z,A_x beta>=D_(beta,z)-H_(beta,z)+J_(beta,z),
D_(beta,z)=-sum_q q(q-2)/(q-1)
             sum_(t,q does not divide t)z(t)beta(t).
```

Writing `B_Q=sum_q q(q-2)/(q-1)` yields

```text
D_(beta,z)=-B_Q<z,beta>
 +sum_q q(q-2)/(q-1)sum_(t,q divides t)z(t)beta(t).
```

For the output mask,

```text
v_(q,t)=c_(q,t)+d_q,
c_(q,t)=1_(u=t mod q)-1/(q-1),
d_q=1_(q divides u)/(q-1).
```

The two period means are `-1/(q-1)` and `+1/(q-1)`; only their sum is
centered.  The deleted diagonal normalization `K_H(0)=integral psi_+=1`
must not be confused with the residue-class Poisson zero mode
`H psi_+(0)/q`.
