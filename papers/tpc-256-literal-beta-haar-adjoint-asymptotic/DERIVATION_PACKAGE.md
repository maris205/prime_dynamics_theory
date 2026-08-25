# TPC-256 derivation package

## 1. Real-clock rank geometry

Write

```text
a=floor(x/2), b=floor(x), N=b-a,
ell=floor(N/2), r=N-ell, m=a+ell.
```

Then `L={a+1,...,m}`, `R={m+1,...,b}` and

```text
N=x/2+O(1), ell,r=x/4+O(1), m=3x/4+O(1),
rho^2=ell*r/N=x/8+O(1),
rho=sqrt(x)/(2sqrt(2))+O(x^(-1/2)).
```

The exact identities needed later are

```text
rho^2(1/ell+1/r)=1,
rho(1/ell+1/r)=1/rho,
|z_mid(t)|<=1/rho.
```

They remain true when `N` is odd and `ell != r`.

## 2. Divisor-density lane

For a consecutive interval `J` of length `s`,

```text
#{n in J:d|n}=s/d+theta_(J,d), |theta_(J,d)|<=1.
```

For

```text
D_U(t)=sum_(d|t,d<=U) mu(d),
```

the `1/d` terms cancel layer by layer:

```text
<z_mid,D_U>
 =rho sum_(d<=U) mu(d)
   [theta_(L,d)/ell-theta_(R,d)/r].
```

Only after this exact cancellation is triangle inequality applied:

```text
|<z_mid,D_U>|
 <=rho U(1/ell+1/r)
 =U/rho
 =O(x^(133/400-1/2))
 =O(x^(-67/400)).
```

No bound for a Mertens sum is used.

## 3. Prime-power lane

Let

```text
F(y)=sum_(2<=n<=y) Lambda(n)/log(n).
```

Prime-power expansion gives

```text
F(y)=pi(y)+sum_(k>=2) pi(y^(1/k))/k.
```

The tail is `O(sqrt(y)log(y))`.  The source-locked de la Vallée Poussin
estimate therefore yields

```text
F(y)=Li(y)+O(y exp(-c_1 sqrt(log y))).
```

After division by a child length, this error is exponentially smaller than
`log^(-3)x`.

For `y` in `[1/2,1]`,

```text
1/log(xy)=1/log x-log(y)/log^2 x+O(log^(-3)x).
```

The leading child means cancel.  Their second-order difference is

```text
4[ integral_(3/4)^1 log(y)dy
  -integral_(1/2)^(3/4) log(y)dy ]
=2 log(32/27).
```

The `O(1)` rank and endpoint perturbations cost only
`O(1/(x log x))` after normalization.  Hence

```text
mean_L(P)-mean_R(P)
 =2 log(32/27)/log^2 x+O(log^(-3)x).
```

Multiplication by `rho` and subtraction of the divisor lane gives

```text
<z_mid,beta>
 =[log(32/27)/sqrt(2)]sqrt(x)/log^2 x
 +O(sqrt(x)/log^3 x).
```

The main constant is positive.

## 4. Exact adjoint normal form

TPC-255 proves, with first-slot conjugate-linearity and no kernel symmetry,

```text
S_x=<z_mid,A_x beta>
   =-B_Q<z_mid,beta>+R_unit+R_hard+R_jump,

B_Q=sum_(q in Q_x)q(q-2)/(q-1).
```

The signs and objects are

```text
R_unit
 =sum_q q(q-2)/(q-1) sum_(t in I_x,q|t) z_mid(t)beta(t),

R_hard
 =-sum_q q sum_(t in I_x,q∤t) beta(t)z_mid(t)
   sum_(u outside I_x) K_H(u-t)v_(q,t)(u),

R_jump
 =+sum_q q sum_(t in I_x,q∤t) beta(t)
   sum_(u in I_x) K_H(u-t)v_(q,t)(u)
   [z_mid(u)-z_mid(t)].
```

## 5. Diagonal coefficient

Since

```text
q(q-2)/(q-1)=q-1-1/(q-1),
```

weighted PNT gives

```text
B_Q=(3/2+o(1))Q^2/log Q
   =(9/2+o(1))x^(2/3)/log x.
```

## 6. Full unit mask and boundary moment

For `q∤t`, retain

```text
v_(q,t)(t+h)
 =1_(q∤(t+h))[1_(q|h)-1/(q-1)].
```

The residue cases give the pointwise estimate

```text
|v_(q,t)(t+h)|<=1_(q|h)+2/q.
```

Schwartz decay and `H/q>1` give

```text
sum_h |h K_H(h)|[1_(q|h)+2/q] <<_psi H^2/q.
```

For fixed `h`, no more than `|h|` source points cross either an outer endpoint
of `I_x` or the single child boundary.  Also a child jump has exact height
`1/rho`.  With `|beta|<<_epsilon x^epsilon`,

```text
R_hard,R_jump
 <<_(psi,epsilon) (QH^2/rho)x^epsilon
 =O_(psi,epsilon)(x^(55/48+epsilon)).
```

Input multiples give

```text
R_unit
 <<_epsilon rho^(-1) sum_(q~Q)q(x/q+1)x^epsilon
 =O_epsilon(x^(5/6+epsilon)).
```

## 7. Main term and phase

The diagonal exponent is

```text
2/3+1/2=7/6=56/48.
```

The boundary exponent is

```text
1/3+2(21/32)-1/2=55/48.
```

Their difference is `1/48`.  Choosing any fixed `0<epsilon<1/48` proves

```text
S_x
 =-[9 log(32/27)/(2sqrt(2))+o(1)]x^(7/6)/log^3 x
```

as a complex asymptotic.  Therefore `Re(S_x)<0` and `S_x!=0` eventually,
and `S_x/|S_x| -> -1`.  This does not imply that `S_x` is real and does not
select `+pi` rather than `-pi` for a branch-dependent principal argument.
